"""Run exactly one Phase 1 example per formatter, preserving measurements.

Usage: python scripts/run_feasibility.py --output datasets/results/phase1
This is a smoke experiment, not the future configurable dataset experiment CLI.
"""

import argparse
import csv
import json
from pathlib import Path

from suppression_study.pipeline import ROOT, measure


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    source = (ROOT / "examples" / "feasibility.py").read_bytes().decode("utf-8")
    results = []
    for formatter in ("black", "ruff"):
        results.append(
            measure(
                source,
                args.output / formatter,
                formatter=formatter,
                trial_id=f"phase1-feasibility-{formatter}",
                dataset_origin="phase1-controlled-feasibility",
                ai_assisted=True,
            )
        )
    with (args.output / "results.jsonl").open(
        "w", encoding="utf-8", newline="\n"
    ) as stream:
        for result in results:
            stream.write(json.dumps(result, ensure_ascii=False) + "\n")
    fields = [
        "trial_id",
        "dataset_origin",
        "ai_assisted",
        "formatter",
        "input_sha256",
        "output_sha256",
        "formatting_changed",
        "ast_equivalent",
        "classification",
        "validation_status",
        "newly_hidden_count",
        "newly_exposed_count",
        "error",
        "evidence_path",
    ]
    with (args.output / "summary.csv").open(
        "w", encoding="utf-8", newline=""
    ) as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        for result in results:
            writer.writerow({key: result.get(key) for key in fields})
    for result in results:
        print(result["trial_id"], result["validation_status"], result.get("counts"))
    return (
        0
        if all(r["validation_status"] == "measurement_complete" for r in results)
        else 2
    )


if __name__ == "__main__":
    raise SystemExit(main())
