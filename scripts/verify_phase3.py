"""Verify all exports, source regeneration and the prospectively selected repeat."""

import argparse
import csv
import hashlib
import json
from pathlib import Path
import tempfile

from suppression_study.experiment import CSV_FIELDS, preliminary_summary
from suppression_study.generator import write_dataset
from suppression_study.pipeline import ROOT, ast_signature, save_json
from verify_phase2 import without_execution_paths


def verify_run(directory, manifest):
    state = json.loads((directory / "run.json").read_text(encoding="utf-8"))
    assert state["status"] == "complete"
    manifest_bytes = (ROOT / "datasets/controlled/phase3/manifest.json").read_bytes()
    assert (directory / "manifest.json").read_bytes() == manifest_bytes
    assert state["manifest_sha256"] == hashlib.sha256(manifest_bytes).hexdigest()
    records = [
        json.loads(line)
        for line in (directory / "results.jsonl")
        .read_text(encoding="utf-8")
        .splitlines()
    ]
    with (directory / "results.csv").open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    assert len(records) == len(rows) == state["planned_comparisons"]
    cases = {case["case_id"]: case for case in manifest["cases"]}
    selected = {
        case_id
        for case_id, case in cases.items()
        if not state["repeat_only"] or case["reproduction_selected"]
    }
    assert {(r["case_id"], r["formatter"]) for r in records} == {
        (case_id, formatter) for case_id in selected for formatter in ("black", "ruff")
    }
    assert len({r["trial_id"] for r in records}) == len(records)
    indexed = {}
    for result, row in zip(records, rows):
        case = cases[result["case_id"]]
        assert result["input_sha256"] == case["input_sha256"]
        assert result["manifest_sha256"] == state["manifest_sha256"]
        assert result["environment"]["seed"] == manifest["seed"]
        for field in CSV_FIELDS:
            expected = result.get(field)
            if isinstance(expected, (dict, list)):
                assert json.loads(row[field]) == expected, (result["trial_id"], field)
            else:
                assert row[field] == ("" if expected is None else str(expected)), (
                    result["trial_id"],
                    field,
                )
        if result["validation_status"] != "excluded_preflight":
            evidence = directory / "trials" / result["case_id"] / result["formatter"]
            assert (
                json.loads((evidence / "result.json").read_text(encoding="utf-8"))
                == result
            )
            for filename, field in (
                ("before.py", "input_sha256"),
                ("after.py", "output_sha256"),
            ):
                if field in result:
                    assert (
                        hashlib.sha256((evidence / filename).read_bytes()).hexdigest()
                        == result[field]
                    )
            if result.get("ast_equivalent") is not None:
                assert (
                    ast_signature((evidence / "before.py").read_bytes().decode())
                    == ast_signature((evidence / "after.py").read_bytes().decode())
                ) == result["ast_equivalent"]
            for label, diagnostics in result.get("passes", {}).items():
                assert (
                    json.loads(
                        (evidence / f"{label}.stdout.txt").read_text(encoding="utf-8")
                    )
                    == diagnostics
                )
                assert (
                    json.loads(
                        (evidence / f"{label}.diagnostics.json").read_text(
                            encoding="utf-8"
                        )
                    )
                    == diagnostics
                )
            if (
                "matched_diagnostic_identities" in result
                and (evidence / "matching.json").exists()
            ):
                matching = json.loads(
                    (evidence / "matching.json").read_text(encoding="utf-8")
                )
                assert (
                    matching["matched_diagnostic_identities"]
                    == result["matched_diagnostic_identities"]
                )
        indexed[(result["case_id"], result["formatter"])] = result
    assert json.loads(
        (directory / "preliminary_summary.json").read_text(encoding="utf-8")
    ) == preliminary_summary(records, len(records))
    return indexed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--main", type=Path, default=ROOT / "datasets/results/phase3")
    parser.add_argument(
        "--repeat", type=Path, default=ROOT / "datasets/results/phase3-repeat"
    )
    parser.add_argument(
        "--report", type=Path, default=ROOT / "reports/phase3/evidence_checks.json"
    )
    args = parser.parse_args()
    dataset = ROOT / "datasets/controlled/phase3"
    manifest = json.loads((dataset / "manifest.json").read_text(encoding="utf-8"))
    with tempfile.TemporaryDirectory(prefix="phase3-regeneration-") as temporary:
        regenerated = Path(temporary) / "dataset"
        assert write_dataset(regenerated, manifest["seed"]) == manifest
        assert (regenerated / "manifest.json").read_bytes() == (
            dataset / "manifest.json"
        ).read_bytes()
        assert (regenerated / "specification.json").read_bytes() == (
            dataset / "specification.json"
        ).read_bytes()
        for case in manifest["cases"]:
            assert (regenerated / case["source"]).read_bytes() == (
                dataset / case["source"]
            ).read_bytes()
    first, repeat = verify_run(args.main, manifest), verify_run(args.repeat, manifest)
    fields = (
        "input_sha256",
        "output_sha256",
        "classification",
        "validation_status",
        "counts",
        "ast_equivalent",
        "formatting_changed",
        "newly_hidden_count",
        "newly_exposed_count",
        "passes",
        "matched_diagnostic_identities",
        "underlying_changes",
        "matching_errors",
    )
    for identity, record in repeat.items():
        for field in fields:
            assert without_execution_paths(
                first[identity].get(field)
            ) == without_execution_paths(record.get(field)), (identity, field)
    result = {
        "source_regeneration_identical": True,
        "sources_checked": len(manifest["cases"]),
        "main_records_checked": len(first),
        "repeat_records_checked": len(repeat),
        "all_csv_and_jsonl_fields_checked": True,
        "raw_diagnostics_and_matching_checked": True,
        "repeat_measurements_identical": True,
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    save_json(args.report, result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
