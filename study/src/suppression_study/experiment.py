"""Sequential paired experiments, preflight validation and lossless exports."""

from collections import Counter
import csv
import hashlib
import json
from pathlib import Path
import tomllib

from .pipeline import ROOT, RULES, TIMEOUT, PINS, environment, lint, measure, save_json

OUTCOMES = (
    "Preserved",
    "Newly hidden",
    "Newly exposed",
    "Mixed",
    "Diagnostic changed",
    "AST changed",
    "Ambiguous",
    "Execution failure",
)
METADATA = (
    "case_id",
    "input_family",
    "syntax_category",
    "primary_rule",
    "suppression_type",
    "directive_placement",
    "generation_seed",
    "generation_method",
    "input_structure_sha256",
    "known_oracle_boundary",
    "reproduction_selected",
)
CSV_FIELDS = (
    "trial_id",
    "phase",
    "case_id",
    "dataset_origin",
    "ai_assisted",
    "input_family",
    "syntax_category",
    "primary_rule",
    "suppression_type",
    "directive_placement",
    "generation_seed",
    "generation_method",
    "known_oracle_boundary",
    "reproduction_selected",
    "manifest_sha256",
    "input_structure_sha256",
    "formatter",
    "input_sha256",
    "output_sha256",
    "formatting_changed",
    "ast_equivalent",
    "classification",
    "validation_status",
    "newly_hidden_count",
    "newly_exposed_count",
    "counts",
    "environment",
    "configuration",
    "passes",
    "matched_diagnostic_identities",
    "underlying_changes",
    "matching_errors",
    "explanation",
    "error",
    "evidence_path",
)


def load_config(path: Path) -> dict:
    config = tomllib.loads(path.read_text(encoding="utf-8"))
    required = {
        "dataset",
        "output",
        "seed",
        "formatters",
        "rules",
        "target_version",
        "line_length",
        "preview",
        "subprocess_timeout_seconds",
        "repeat_only",
    }
    if set(config) != required:
        raise ValueError("Experiment config fields do not match the fixed protocol")
    expected = {
        "formatters": ["black", "ruff"],
        "rules": RULES.split(","),
        "target_version": "py311",
        "line_length": 88,
        "preview": False,
        "subprocess_timeout_seconds": TIMEOUT,
    }
    if any(config[key] != value for key, value in expected.items()):
        raise ValueError("Config conflicts with the validated tool settings")
    if type(config["seed"]) is not int or type(config["repeat_only"]) is not bool:
        raise ValueError("Invalid seed/repeat_only types")
    for key in ("dataset", "output"):
        value = Path(config[key])
        config[key] = (
            value.resolve() if value.is_absolute() else (ROOT / value).resolve()
        )
    if (
        config["dataset"] == config["output"]
        or config["dataset"] in config["output"].parents
        or config["output"] in config["dataset"].parents
    ):
        raise ValueError("Dataset and result directories must not overlap")
    return config


def preliminary_summary(records, planned):
    summary = {
        "planned_comparisons": planned,
        "recorded_comparisons": len(records),
        "excluded_preflight": sum(
            r["validation_status"] == "excluded_preflight" for r in records
        ),
        "by_formatter": {},
    }
    for formatter in ("black", "ruff"):
        trials = [
            r
            for r in records
            if r["formatter"] == formatter
            and r["validation_status"] != "excluded_preflight"
        ]
        classified = [
            r
            for r in trials
            if r["classification"]
            in {"Preserved", "Newly hidden", "Newly exposed", "Mixed"}
        ]
        outcomes = Counter(r["classification"] for r in trials)
        summary["by_formatter"][formatter] = {
            "executed": len(trials),
            "attributable": len(classified),
            "outcomes": {name: outcomes[name] for name in OUTCOMES},
            "formatting_changed": sum(
                r.get("formatting_changed") is True for r in trials
            ),
            "formatting_unchanged": sum(
                r.get("formatting_changed") is False for r in trials
            ),
            "newly_hidden_diagnostics": sum(
                r.get("newly_hidden_count") or 0 for r in classified
            ),
            "newly_exposed_diagnostics": sum(
                r.get("newly_exposed_count") or 0 for r in classified
            ),
        }
    return summary


def run_experiment(config_path: Path) -> dict:
    config = load_config(config_path)
    dataset, output = config["dataset"], config["output"]
    manifest_bytes = (dataset / "manifest.json").read_bytes()
    manifest = json.loads(manifest_bytes)
    specification_bytes = (dataset / "specification.json").read_bytes()
    if (
        hashlib.sha256(specification_bytes).hexdigest()
        != manifest["specification_sha256"]
    ):
        raise ValueError("Frozen generation specification checksum differs")
    if manifest["seed"] != config["seed"]:
        raise ValueError("Configuration seed differs from the frozen source manifest")
    cases = {case["case_id"]: case for case in manifest["cases"]}
    if (
        len(cases) != len(manifest["cases"])
        or set(cases) != set(manifest["execution_order"])
        or len(cases) != len(manifest["execution_order"])
    ):
        raise ValueError("Manifest case/order identities are not unique and complete")
    ordered = [
        cases[case_id]
        for case_id in manifest["execution_order"]
        if not config["repeat_only"] or cases[case_id]["reproduction_selected"]
    ]
    # Validate the frozen input bytes before creating output or executing tools.
    for case in ordered:
        source_path = (dataset / case["source"]).resolve()
        if dataset not in source_path.parents:
            raise ValueError("Source path escapes the dataset")
        if hashlib.sha256(source_path.read_bytes()).hexdigest() != case["input_sha256"]:
            raise ValueError(f"Frozen source checksum differs: {case['case_id']}")
    run_environment = environment()
    if run_environment["tools"] != PINS:
        raise ValueError("Installed tools differ from validated pins")
    output.mkdir(parents=True, exist_ok=False)
    (output / "config.toml").write_bytes(config_path.read_bytes())
    (output / "manifest.json").write_bytes(manifest_bytes)
    (output / "specification.json").write_bytes(specification_bytes)
    run_environment.update(
        seed=config["seed"],
        random_generation=False,
        snapshot_scope="experiment start; no repeated Git discovery per trial",
    )
    state = {
        "status": "running",
        "planned_comparisons": len(ordered) * 2,
        "manifest_sha256": hashlib.sha256(manifest_bytes).hexdigest(),
        "environment": run_environment,
        "repeat_only": config["repeat_only"],
    }
    save_json(output / "run.json", state)
    preflight = []
    # Finish every original-source relevance check before any main formatting.
    for case in ordered:
        path = output / "preflight" / case["case_id"]
        path.mkdir(parents=True)
        validation = {
            "case_id": case["case_id"],
            "eligible": False,
            "error": None,
            "diagnostic_count": None,
            "syntax_valid": case["syntax_valid"],
            "duplicate_of": case["duplicate_of"],
        }
        if not case["accepted"]:
            validation["error"] = (
                case["syntax_error"] or f"Byte duplicate of {case['duplicate_of']}"
            )
        else:
            try:
                diagnostics = lint(
                    (dataset / case["source"]).read_bytes().decode("utf-8"),
                    True,
                    path,
                    "underlying",
                )
                validation["diagnostic_count"] = len(diagnostics)
                validation["eligible"] = bool(diagnostics)
                if not diagnostics:
                    validation["error"] = (
                        "No selected underlying diagnostic; excluded by prospective relevance rule"
                    )
            except (ValueError, RuntimeError, OSError) as exc:
                validation["error"] = f"{type(exc).__name__}: {exc}"
        save_json(path / "validation.json", validation)
        preflight.append(validation)
    save_json(output / "preflight.json", preflight)
    eligible = {item["case_id"] for item in preflight if item["eligible"]}
    reasons = {item["case_id"]: item["error"] for item in preflight}
    records = []
    try:
        with (
            (output / "results.jsonl").open(
                "w", encoding="utf-8", newline="\n"
            ) as jsonl,
            (output / "results.csv").open("w", encoding="utf-8", newline="") as csvfile,
        ):
            writer = csv.DictWriter(csvfile, fieldnames=CSV_FIELDS)
            writer.writeheader()
            for case in ordered:
                for formatter in config["formatters"]:
                    trial_id = f"{output.name}--{case['case_id']}--{formatter}"
                    metadata = {key: case[key] for key in METADATA}
                    metadata["manifest_sha256"] = state["manifest_sha256"]
                    if case["case_id"] in eligible:
                        result = measure(
                            (dataset / case["source"]).read_bytes().decode("utf-8"),
                            output / "trials" / case["case_id"] / formatter,
                            formatter=formatter,
                            trial_id=trial_id,
                            dataset_origin=manifest["dataset_origin"],
                            ai_assisted=True,
                            study_phase=3,
                            case_metadata=metadata,
                            run_environment=run_environment,
                        )
                    else:
                        result = {
                            **metadata,
                            "schema_version": 2,
                            "phase": 3,
                            "trial_id": trial_id,
                            "formatter": formatter,
                            "dataset_origin": manifest["dataset_origin"],
                            "ai_assisted": True,
                            "input_sha256": case["input_sha256"],
                            "classification": None,
                            "validation_status": "excluded_preflight",
                            "error": reasons[case["case_id"]],
                            "environment": run_environment,
                            "evidence_path": str(
                                output / "preflight" / case["case_id"]
                            ),
                        }
                    records.append(result)
                    jsonl.write(json.dumps(result, ensure_ascii=False) + "\n")
                    writer.writerow(
                        {
                            key: (
                                json.dumps(result[key], ensure_ascii=False)
                                if isinstance(result.get(key), (dict, list))
                                else result.get(key)
                            )
                            for key in CSV_FIELDS
                        }
                    )
                    jsonl.flush()
                    csvfile.flush()
                if len(records) % 40 == 0 or len(records) == len(ordered) * 2:
                    print(
                        f"Recorded {len(records)}/{len(ordered) * 2} comparisons",
                        flush=True,
                    )
        summary = preliminary_summary(records, len(ordered) * 2)
        save_json(output / "preliminary_summary.json", summary)
        state.update(
            status="complete",
            recorded_comparisons=len(records),
            eligible_cases=len(eligible),
            excluded_cases=len(ordered) - len(eligible),
        )
    except Exception as exc:
        state.update(status="failed", error=f"{type(exc).__name__}: {exc}")
        raise
    finally:
        save_json(output / "run.json", state)
    print(json.dumps(summary, indent=2), flush=True)
    return summary
