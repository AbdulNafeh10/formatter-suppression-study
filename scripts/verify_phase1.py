"""Verify saved Phase 1 source hashes, exports, and repeat measurements."""

import csv
import hashlib
import json

from suppression_study.pipeline import ROOT, ast_signature, save_json


def diagnostics_without_paths(passes):
    return {
        label: [
            {key: value for key, value in item.items() if key != "filename"}
            for item in items
        ]
        for label, items in passes.items()
    }


def main():
    checks = {}
    for dataset in ("phase1", "phase1-repeat"):
        directory = ROOT / "datasets" / "results" / dataset
        jsonl = [
            json.loads(line)
            for line in (directory / "results.jsonl")
            .read_text(encoding="utf-8")
            .splitlines()
        ]
        with (directory / "summary.csv").open(encoding="utf-8", newline="") as stream:
            rows = list(csv.DictReader(stream))
        assert len(jsonl) == len(rows) == 2
        for index, formatter in enumerate(("black", "ruff")):
            evidence = directory / formatter
            result = json.loads((evidence / "result.json").read_text(encoding="utf-8"))
            assert jsonl[index] == result
            assert rows[index]["trial_id"] == result["trial_id"]
            assert rows[index]["output_sha256"] == result["output_sha256"]
            for name, field in (
                ("before.py", "input_sha256"),
                ("after.py", "output_sha256"),
            ):
                assert (
                    hashlib.sha256((evidence / name).read_bytes()).hexdigest()
                    == result[field]
                )
            assert ast_signature(
                (evidence / "before.py").read_bytes().decode("utf-8")
            ) == ast_signature((evidence / "after.py").read_bytes().decode("utf-8"))
            for label, diagnostics in result["passes"].items():
                assert (
                    json.loads(
                        (evidence / f"{label}.stdout.txt").read_text(encoding="utf-8")
                    )
                    == diagnostics
                )
            assert result["validation_status"] == "measurement_complete"
            checks[f"{dataset}_{formatter}_evidence_and_export"] = True
    for formatter in ("black", "ruff"):
        results = [
            json.loads(
                (
                    ROOT / "datasets" / "results" / dataset / formatter / "result.json"
                ).read_text(encoding="utf-8")
            )
            for dataset in ("phase1", "phase1-repeat")
        ]
        for field in (
            "input_sha256",
            "output_sha256",
            "counts",
            "ast_equivalent",
            "formatting_changed",
            "classification",
        ):
            assert results[0][field] == results[1][field]
        assert diagnostics_without_paths(
            results[0]["passes"]
        ) == diagnostics_without_paths(results[1]["passes"])
        checks[f"{formatter}_repeatability"] = True
    save_json(ROOT / "reports" / "phase1" / "evidence_checks.json", checks)
    print(json.dumps(checks, indent=2))


if __name__ == "__main__":
    main()
