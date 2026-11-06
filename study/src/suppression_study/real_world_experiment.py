"""Paired measurements of frozen natural source; no repository code execution."""

from collections import Counter
import csv
import hashlib
import json
from pathlib import Path
import sys

from .classifier import classify
from .experiment import CSV_FIELDS, preliminary_summary
from .pipeline import (
    PINS,
    RULES,
    environment,
    measure,
    parse_diagnostics,
    run_tool,
    save_json,
)

WORLD_FIELDS = CSV_FIELDS + (
    "repository",
    "repository_url",
    "repository_commit",
    "repository_tag",
    "original_path",
    "source_url",
    "file_role",
    "configuration_mode",
    "population_rank",
    "source_acquisition_method",
    "native_config",
)
NATIVE_FIELDS = WORLD_FIELDS + (
    "full_native_passes",
    "full_native_counts",
    "config",
    "stdin_filename",
    "selected_rules",
)


def native_compare(before, after, config, filename, evidence):
    evidence.mkdir(parents=True, exist_ok=False)
    result = {
        "classification": "Execution failure",
        "validation_status": "failed",
        "configuration_mode": "project-config-sensitivity-selected-rule-subset",
        "config": str(config),
        "stdin_filename": str(filename),
        "selected_rules": RULES.split(","),
        "error": None,
        "newly_hidden_count": None,
        "newly_exposed_count": None,
    }
    full, selected = {}, {}
    try:
        for label, source, ignore in (
            ("A_original_visible", before, False),
            ("B_original_underlying", before, True),
            ("C_formatted_visible", after, False),
            ("D_formatted_underlying", after, True),
        ):
            command = [
                sys.executable,
                "-m",
                "ruff",
                "check",
                "--config",
                str(config),
                "--no-cache",
                "--no-fix",
                "--output-format",
                "json",
                "--stdin-filename",
                str(filename),
            ]
            if ignore:
                command.append("--ignore-noqa")
            raw = run_tool(command + ["-"], source, evidence, label)
            if raw["error"] or raw["returncode"] not in (0, 1):
                raise RuntimeError(
                    f"{label}: native-config lint failed; see command record"
                )
            full[label] = parse_diagnostics(raw["stdout"])
            if bool(full[label]) != (raw["returncode"] == 1):
                raise ValueError("Native Ruff output/status disagree")
            save_json(evidence / f"{label}.diagnostics.json", full[label])
            selected[label] = [
                item for item in full[label] if item["code"] in RULES.split(",")
            ]
            result["full_native_passes"] = full
            result["passes"] = selected
        result.update(classify(before, after, selected))
        result["counts"] = {label: len(items) for label, items in selected.items()}
        result["full_native_counts"] = {
            label: len(items) for label, items in full.items()
        }
        result["validation_status"] = "measurement_complete"
    except (ValueError, RuntimeError, OSError, SyntaxError) as exc:
        result["error"] = f"{type(exc).__name__}: {exc}"
    save_json(evidence / "result.json", result)
    return result


def write_row(writer, result):
    writer.writerow(
        {
            key: (
                json.dumps(result[key], ensure_ascii=False)
                if isinstance(result.get(key), (dict, list))
                else result.get(key)
            )
            for key in writer.fieldnames
        }
    )


def world_summary(records):
    per_repository = {}
    for repo in sorted({record["repository"] for record in records}):
        trials = [record for record in records if record["repository"] == repo]
        summary = preliminary_summary(trials, len(trials))
        for formatter, values in summary["by_formatter"].items():
            subset = [record for record in trials if record["formatter"] == formatter]
            values["with_underlying_selected_diagnostics"] = sum(
                bool(r.get("passes", {}).get("B_original_underlying")) for r in subset
            )
            values["with_original_selected_suppression"] = sum(
                bool(r.get("suppressed_within_source", {}).get("original"))
                for r in subset
            )
            values["zero_underlying_diagnostics"] = sum(
                r.get("passes", {}).get("B_original_underlying") == [] for r in subset
            )
        per_repository[repo] = summary
    return per_repository


def run_real_world(dataset: Path, output: Path, repeat=False):
    dataset, output = dataset.resolve(), output.resolve()
    manifest_bytes = (dataset / "manifest.json").read_bytes()
    manifest = json.loads(manifest_bytes)
    cases = sorted(
        [
            case
            for case in manifest["cases"]
            if not repeat or case["reproduction_selected"]
        ],
        key=lambda case: (case["repository"], case["rank"]),
    )
    if len({case["case_id"] for case in cases}) != len(cases):
        raise ValueError("Duplicate case identities")
    for repo in manifest["repositories"]:
        archive = dataset / repo["archive"]
        public_export = manifest.get("public_export", {})
        if (
            archive.exists()
            and hashlib.sha256(archive.read_bytes()).hexdigest()
            != repo["archive_sha256"]
        ):
            raise ValueError("Frozen source archive checksum differs")
        if not archive.exists() and not public_export.get("upstream_archives_omitted"):
            raise ValueError("Frozen source archive is missing")
        context = dataset / "contexts" / repo["repository"].replace("/", "--")
        for path, checksum in repo["context_sha256"].items():
            omitted = public_export.get("omitted_context_files", {}).get(
                repo["repository"], []
            )
            if path in omitted:
                if not (path.startswith("ext/") or path.startswith("docs/_themes/")):
                    raise ValueError(
                        "Public omission cannot bypass a measured source or native config"
                    )
                continue
            if hashlib.sha256((context / path).read_bytes()).hexdigest() != checksum:
                raise ValueError(
                    f"Frozen native-config/license context differs: {path}"
                )
    for case in cases:
        source = (dataset / case["source"]).resolve()
        if (
            dataset not in source.parents
            or hashlib.sha256(source.read_bytes()).hexdigest() != case["input_sha256"]
        ):
            raise ValueError(f"Frozen source tampered or unsafe: {case['case_id']}")
    run_environment = environment()
    if run_environment["tools"] != PINS:
        raise ValueError("Tool pins differ from validated oracle")
    run_environment.update(
        seed=manifest["seed"],
        random_generation=False,
        snapshot_scope="experiment start",
    )
    output.mkdir(parents=True, exist_ok=False)
    (output / "manifest.json").write_bytes(manifest_bytes)
    state = {
        "status": "running",
        "phase": 4,
        "repeat": repeat,
        "planned_comparisons": 2 * len(cases),
        "environment": run_environment,
        "manifest_sha256": hashlib.sha256(manifest_bytes).hexdigest(),
        "archive_validation_scope": (
            "omitted public archive; selected source and retained context hashes checked"
            if manifest.get("public_export", {}).get("upstream_archives_omitted")
            else "full archives checked"
        ),
    }
    save_json(output / "run.json", state)
    records, native_records = [], []
    try:
        with (
            (output / "results.jsonl").open(
                "w", encoding="utf-8", newline="\n"
            ) as jsonl,
            (output / "results.csv").open("w", encoding="utf-8", newline="") as csvfile,
            (output / "native_results.jsonl").open(
                "w", encoding="utf-8", newline="\n"
            ) as native_stream,
            (output / "native_results.csv").open(
                "w", encoding="utf-8", newline=""
            ) as native_csv,
        ):
            writer = csv.DictWriter(csvfile, fieldnames=WORLD_FIELDS)
            writer.writeheader()
            native_writer = csv.DictWriter(native_csv, fieldnames=NATIVE_FIELDS)
            native_writer.writeheader()
            for case in cases:
                source = (dataset / case["source"]).read_bytes().decode("utf-8")
                for formatter in ("black", "ruff"):
                    trial_id = f"{output.name}--{case['case_id']}--{formatter}"
                    metadata = {
                        "case_id": case["case_id"],
                        "repository": case["repository"],
                        "repository_url": case["repository_url"],
                        "repository_commit": case["repository_commit"],
                        "repository_tag": case["repository_tag"],
                        "original_path": case["path"],
                        "source_url": case["source_url"],
                        "file_role": case["file_role"],
                        "configuration_mode": "standardized-study_input.py",
                        "population_rank": case["rank"],
                        "source_acquisition_method": "immutable GitHub commit archive",
                        "native_config": case["native_config"],
                        "reproduction_selected": case["reproduction_selected"],
                        "manifest_sha256": state["manifest_sha256"],
                        "input_structure_sha256": case["input_structure_sha256"],
                    }
                    trial = output / "trials" / case["case_id"] / formatter
                    result = measure(
                        source,
                        trial,
                        formatter=formatter,
                        trial_id=trial_id,
                        dataset_origin="public-repository-validation",
                        ai_assisted=False,
                        study_phase=4,
                        case_metadata=metadata,
                        run_environment=run_environment,
                    )
                    records.append(result)
                    jsonl.write(json.dumps(result, ensure_ascii=False) + "\n")
                    write_row(writer, result)
                    jsonl.flush()
                    csvfile.flush()
                    if not case["native_config"]:
                        native = {
                            "classification": None,
                            "validation_status": "no_project_ruff_config",
                            "newly_hidden_count": None,
                            "newly_exposed_count": None,
                        }
                    elif (
                        not (trial / "after.py").exists()
                        or result["validation_status"] != "measurement_complete"
                    ):
                        native = {
                            "classification": None,
                            "validation_status": "primary_transform_incomplete",
                            "newly_hidden_count": None,
                            "newly_exposed_count": None,
                        }
                    else:
                        native = native_compare(
                            source,
                            (trial / "after.py").read_bytes().decode("utf-8"),
                            (dataset / case["native_config"]).resolve(),
                            (dataset / case["native_context"] / case["path"]).resolve(),
                            trial / "native",
                        )
                    native.update(
                        trial_id=trial_id,
                        case_id=case["case_id"],
                        repository=case["repository"],
                        repository_commit=case["repository_commit"],
                        original_path=case["path"],
                        formatter=formatter,
                        ai_assisted=False,
                        dataset_origin="public-repository-config-sensitivity",
                        phase=4,
                        input_sha256=result["input_sha256"],
                        output_sha256=result.get("output_sha256"),
                        evidence_path=str(
                            trial / "native" if (trial / "native").exists() else trial
                        ),
                        configuration_mode="project-config-sensitivity-selected-rule-subset",
                    )
                    native_records.append(native)
                    native_stream.write(json.dumps(native, ensure_ascii=False) + "\n")
                    write_row(native_writer, native)
                    native_stream.flush()
                    native_csv.flush()
                if len(records) % 10 == 0 or len(records) == 2 * len(cases):
                    print(
                        f"Recorded {len(records)}/{2 * len(cases)} primary comparisons (+ native sensitivity)",
                        flush=True,
                    )
        summary = {
            "primary": world_summary(records),
            "native_status_by_repository": {},
            "native_outcomes_by_repository_formatter": {},
        }
        for repo in sorted({r["repository"] for r in records}):
            subset = [r for r in native_records if r["repository"] == repo]
            summary["native_status_by_repository"][repo] = dict(
                Counter(r["validation_status"] for r in subset)
            )
            summary["native_outcomes_by_repository_formatter"][repo] = {
                formatter: dict(
                    Counter(
                        r["classification"] or r["validation_status"]
                        for r in subset
                        if r["formatter"] == formatter
                    )
                )
                for formatter in ("black", "ruff")
            }
        save_json(output / "preliminary_summary.json", summary)
        state.update(status="complete", recorded_comparisons=len(records))
    except Exception as exc:
        state.update(status="failed", error=f"{type(exc).__name__}: {exc}")
        raise
    finally:
        save_json(output / "run.json", state)
    print(json.dumps(summary, indent=2), flush=True)
    return summary
