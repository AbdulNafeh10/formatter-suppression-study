"""Integrity checks on retained observations; not detector ground-truth labels."""

from collections import Counter
import hashlib
import json

from .pipeline import PINS, ROOT
from .evidence import evidence_bytes

RESOLVED = {"Preserved", "Newly hidden", "Newly exposed", "Mixed"}
DRIFT = {"Newly hidden", "Newly exposed", "Mixed"}
LABELS = (
    "A_original_visible",
    "B_original_underlying",
    "C_formatted_visible",
    "D_formatted_underlying",
)


def require(condition, reason):
    if not condition:
        raise ValueError(f"Analysis integrity failure: {reason}")


def diagnostic_key(item):
    return (
        item["code"],
        item["message"],
        item["location"]["row"],
        item["location"]["column"],
        item["end_location"]["row"],
        item["end_location"]["column"],
    )


def audit_arithmetic(record):
    """Check occurrence-specific transitions and within-source set arithmetic."""
    passes = record.get("passes", {})
    if record["validation_status"] != "measurement_complete":
        require(
            record["classification"] not in RESOLVED,
            "incomplete trial claims attribution",
        )
        require(
            record.get("newly_hidden_count") is None
            and record.get("newly_exposed_count") is None,
            "incomplete trial has drift counts",
        )
        return
    require(set(passes) == set(LABELS), "complete trial lacks four passes")
    for underlying, visible, side in (
        (LABELS[1], LABELS[0], "original"),
        (LABELS[3], LABELS[2], "formatted"),
    ):
        u, v = Counter(map(diagnostic_key, passes[underlying])), Counter(
            map(diagnostic_key, passes[visible])
        )
        require(not v - u, "visible findings not a within-source subset")
        if "suppressed_within_source" in record:
            require(
                Counter(map(diagnostic_key, record["suppressed_within_source"][side]))
                == u - v,
                "suppression subtraction disagrees with raw passes",
            )
        if "counts" in record:
            require(
                record["counts"][underlying] == len(passes[underlying])
                and record["counts"][visible] == len(passes[visible]),
                "diagnostic counts disagree with raw arrays",
            )
            count_key = f"{side}_suppressed"
            if count_key in record["counts"]:
                require(
                    record["counts"][count_key] == sum((u - v).values()),
                    "stored suppression count differs",
                )
    if record["classification"] not in RESOLVED:
        require(
            record.get("newly_hidden_count") is None
            and record.get("newly_exposed_count") is None,
            "unresolved trial has attributed drift counts",
        )
        return
    require(
        record.get("ast_equivalent", True) is True, "attribution despite AST failure"
    )
    pairs = record["matched_diagnostic_identities"]
    require(
        len({p["identity"] for p in pairs}) == len(pairs),
        "duplicate matched occurrence",
    )
    require(
        len(pairs) == len(passes[LABELS[1]]) == len(passes[LABELS[3]]),
        "incomplete underlying correspondence",
    )
    visible_before = set(map(diagnostic_key, passes[LABELS[0]]))
    visible_after = set(map(diagnostic_key, passes[LABELS[2]]))
    before_keys, after_keys, hidden, exposed = [], [], 0, 0
    for pair in pairs:
        original, formatted = pair["original"], pair["formatted"]
        require(
            pair["identity"] == original["identity"] == formatted["identity"],
            "matched identities disagree",
        )
        for field in (
            "rule",
            "ast_path",
            "node_context",
            "construct_tokens",
            "diagnostic_tokens",
        ):
            require(
                original[field] == formatted[field],
                f"matching context differs: {field}",
            )
        require(
            original["diagnostic"]["message"] == formatted["diagnostic"]["message"],
            "underlying message changed",
        )
        require(
            original["rule"]
            == original["diagnostic"]["code"]
            == formatted["diagnostic"]["code"],
            "rule identity differs",
        )
        before_key, after_key = diagnostic_key(original["diagnostic"]), diagnostic_key(
            formatted["diagnostic"]
        )
        before_keys.append(before_key)
        after_keys.append(after_key)
        was, now = before_key in visible_before, after_key in visible_after
        require(
            was == original["visible"] and now == formatted["visible"],
            "visibility flag differs from raw pass",
        )
        transition = (
            "newly_hidden"
            if was and not now
            else "newly_exposed" if now and not was else "preserved"
        )
        require(pair["transition"] == transition, "wrong occurrence transition")
        hidden += int(was and not now)
        exposed += int(now and not was)
    require(
        Counter(before_keys) == Counter(map(diagnostic_key, passes[LABELS[1]])),
        "matched originals differ from underlying pass",
    )
    require(
        Counter(after_keys) == Counter(map(diagnostic_key, passes[LABELS[3]])),
        "matched formatted findings differ from underlying pass",
    )
    expected = (
        "Mixed"
        if hidden and exposed
        else "Newly hidden" if hidden else "Newly exposed" if exposed else "Preserved"
    )
    require(
        record["classification"] == expected,
        "outcome disagrees with occurrence transitions",
    )
    require(
        record["newly_hidden_count"] == hidden
        and record["newly_exposed_count"] == exposed,
        "attributed warning counts disagree",
    )


def load_and_audit(root=ROOT):
    paths = {
        "controlled": root / "datasets/results/phase3",
        "natural": root / "datasets/results/phase4",
    }
    datasets, summary, hashes = {}, {}, {}
    for dataset, directory in paths.items():
        state = json.loads((directory / "run.json").read_text(encoding="utf-8"))
        require(state["status"] == "complete", "incomplete experiment run")
        source_manifest_path = root / (
            "datasets/controlled/phase3/manifest.json"
            if dataset == "controlled"
            else "datasets/real_world/phase4/manifest.json"
        )
        manifest_bytes = source_manifest_path.read_bytes()
        require(
            (directory / "manifest.json").read_bytes() == manifest_bytes,
            "run and frozen source manifests differ",
        )
        require(
            hashlib.sha256(manifest_bytes).hexdigest() == state["manifest_sha256"],
            "frozen manifest checksum differs",
        )
        manifest_cases = {
            case["case_id"]: case for case in json.loads(manifest_bytes)["cases"]
        }
        hashes[source_manifest_path.relative_to(root).as_posix()] = hashlib.sha256(
            manifest_bytes
        ).hexdigest()
        records = [
            json.loads(line)
            for line in (directory / "results.jsonl")
            .read_text(encoding="utf-8")
            .splitlines()
        ]
        require(
            len(records) == state["planned_comparisons"],
            "missing scheduled observations",
        )
        require(
            len({r["trial_id"] for r in records}) == len(records), "duplicate trial IDs"
        )
        groups = {}
        for record in records:
            audit_arithmetic(record)
            require(record["case_id"] in manifest_cases, "unknown source case")
            require(
                record["input_sha256"]
                == manifest_cases[record["case_id"]]["input_sha256"],
                "input differs from frozen source",
            )
            require(record["environment"]["tools"] == PINS, "tool versions changed")
            require(
                record["configuration"]["rules"] == ["F401", "F821", "F841"],
                "different primary lint rules",
            )
            require(
                record["configuration"]["isolated_lint"] is True,
                "nonstandard primary lint condition",
            )
            require(
                record["ai_assisted"] is (dataset == "controlled"),
                "input-generation origin mislabeled",
            )
            group = groups.setdefault(record["case_id"], {})
            require(record["formatter"] not in group, "duplicate formatter/case record")
            group[record["formatter"]] = record
            trial = directory / "trials" / record["case_id"] / record["formatter"]
            before = evidence_bytes(trial / "before.py")
            require(
                hashlib.sha256(before).hexdigest() == record["input_sha256"],
                "input bytes differ",
            )
            if record.get("output_sha256"):
                after = evidence_bytes(trial / "after.py")
                require(
                    hashlib.sha256(after).hexdigest() == record["output_sha256"],
                    "output bytes differ",
                )
                require(
                    (before != after) == record["formatting_changed"],
                    "wrong text-change flag",
                )
                formatter = json.loads(
                    (trial / "formatter.command.json").read_text(encoding="utf-8")
                )
                require(
                    formatter["returncode"] == 0 and formatter["error"] is None,
                    "formatter invocation failed",
                )
                require(
                    formatter["stdout"].encode("utf-8") == after,
                    "formatter output differs from analyzed bytes",
                )
            for label, diagnostics in record.get("passes", {}).items():
                command = json.loads(
                    (trial / f"{label}.command.json").read_text(encoding="utf-8")
                )
                require(
                    command["error"] is None and command["returncode"] in (0, 1),
                    "stored lint invocation failed",
                )
                require(
                    json.loads(command["stdout"]) == diagnostics,
                    "command output differs from analyzed diagnostics",
                )
                require(
                    ("--ignore-noqa" in command["command"])
                    == (label in (LABELS[1], LABELS[3])),
                    "wrong noqa pass flag",
                )
                args = command["command"]
                require(
                    "--isolated" in args
                    and "--no-fix" in args
                    and args[args.index("--select") + 1] == "F401,F821,F841",
                    "primary command settings differ",
                )
        require(
            set(groups) == set(manifest_cases),
            "source population/sample coverage differs",
        )
        for group in groups.values():
            require(set(group) == {"black", "ruff"}, "unpaired case")
            require(
                group["black"]["input_sha256"] == group["ruff"]["input_sha256"],
                "formatter inputs differ",
            )
            for label in LABELS[:2]:
                if label in group["black"].get("passes", {}) and label in group[
                    "ruff"
                ].get("passes", {}):
                    require(
                        Counter(map(diagnostic_key, group["black"]["passes"][label]))
                        == Counter(map(diagnostic_key, group["ruff"]["passes"][label])),
                        "original diagnostic content differs between formatters",
                    )
        summary[dataset] = {
            "records": len(records),
            "paired_cases": len(groups),
            "arithmetic_and_provenance_passed": True,
        }
        datasets[dataset] = records
        for filename in ("results.jsonl", "results.csv", "manifest.json", "run.json"):
            path = directory / filename
            hashes[path.relative_to(root).as_posix()] = hashlib.sha256(
                path.read_bytes()
            ).hexdigest()
    native_path = paths["natural"] / "native_results.jsonl"
    native = [
        json.loads(line)
        for line in native_path.read_text(encoding="utf-8").splitlines()
    ]
    require(len(native) == len(datasets["natural"]), "missing native status records")
    for record in native:
        if record["validation_status"] == "measurement_complete":
            require(
                record["passes"]
                == {
                    label: [
                        d for d in diagnostics if d["code"] in {"F401", "F821", "F841"}
                    ]
                    for label, diagnostics in record["full_native_passes"].items()
                },
                "native rule subset mismatch",
            )
            audit_arithmetic(record)
    hashes[native_path.relative_to(root).as_posix()] = hashlib.sha256(
        native_path.read_bytes()
    ).hexdigest()
    native_csv = paths["natural"] / "native_results.csv"
    hashes[native_csv.relative_to(root).as_posix()] = hashlib.sha256(
        native_csv.read_bytes()
    ).hexdigest()
    summary["native"] = {
        "status_records": len(native),
        "completed_comparisons": sum(
            r["validation_status"] == "measurement_complete" for r in native
        ),
    }
    return datasets, native, summary, hashes
