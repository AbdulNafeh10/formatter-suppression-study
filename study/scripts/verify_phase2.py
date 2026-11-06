"""Check retained validation exports and deterministic repeat correspondence."""

import argparse
import csv
import hashlib
import json
from pathlib import Path

from suppression_study.pipeline import ROOT, ast_signature, save_json


def load(directory):
    manifest_path = ROOT / "datasets/controls/phase2/manifest.json"
    expected = json.loads(manifest_path.read_text(encoding="utf-8"))
    validation = json.loads((directory / "validation.json").read_text(encoding="utf-8"))
    assert (
        validation["manifest_sha256"]
        == hashlib.sha256(manifest_path.read_bytes()).hexdigest()
    )
    assert validation["all_passed"] is True
    assert len(validation["controls"]) == len(expected["controls"])
    records = [
        json.loads(line)
        for line in (directory / "results.jsonl")
        .read_text(encoding="utf-8")
        .splitlines()
    ]
    with (directory / "summary.csv").open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    assert len(records) == len(rows) == len(expected["controls"])
    result_by_control = {}
    for control, record, row in zip(expected["controls"], records, rows):
        evidence = directory / control["id"]
        assert (
            json.loads((evidence / "result.json").read_text(encoding="utf-8")) == record
        )
        for name, field in (
            ("before.py", "input_sha256"),
            ("after.py", "output_sha256"),
        ):
            assert (
                hashlib.sha256((evidence / name).read_bytes()).hexdigest()
                == record[field]
                == control[name.replace(".py", "_sha256")]
            )
        assert ast_signature(
            (evidence / "before.py").read_bytes().decode()
        ) == ast_signature((evidence / "after.py").read_bytes().decode())
        for label, diagnostics in record["passes"].items():
            assert (
                json.loads(
                    (evidence / f"{label}.stdout.txt").read_text(encoding="utf-8")
                )
                == diagnostics
            )
        assert row["trial_id"] == record["trial_id"]
        assert (
            row["classification"]
            == record["classification"]
            == control["expected_classification"]
        )
        assert row["output_sha256"] == record["output_sha256"]
        assert int(row["newly_hidden_count"]) == record["newly_hidden_count"]
        assert int(row["newly_exposed_count"]) == record["newly_exposed_count"]
        result_by_control[control["id"]] = record
    return result_by_control


def without_execution_paths(value):
    if isinstance(value, dict):
        return {
            key: without_execution_paths(item)
            for key, item in value.items()
            if key != "filename"
        }
    if isinstance(value, list):
        return [without_execution_paths(item) for item in value]
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("first", type=Path)
    parser.add_argument("repeat", type=Path)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    first, second = load(args.first), load(args.repeat)
    assert first.keys() == second.keys()
    fields = (
        "input_sha256",
        "output_sha256",
        "classification",
        "counts",
        "ast_equivalent",
        "formatting_changed",
        "newly_hidden_count",
        "newly_exposed_count",
        "passes",
        "matched_diagnostic_identities",
        "underlying_changes",
    )
    for control_id in first:
        for field in fields:
            assert without_execution_paths(
                first[control_id][field]
            ) == without_execution_paths(second[control_id][field]), (control_id, field)
    summary = {
        "export_and_source_integrity": True,
        "repeatability": True,
        "controls_checked": len(first),
        "development_validation_only": True,
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    save_json(args.report, summary)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
