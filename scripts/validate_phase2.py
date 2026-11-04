"""Replay frozen controls through real tools, preserving predictions and checks."""

import argparse
import csv
import hashlib
import json
from pathlib import Path

from suppression_study.pipeline import ROOT, measure, save_json


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    manifest_path = ROOT / "datasets/controls/phase2/manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    results, validations = [], []
    for control in manifest["controls"]:
        before = (ROOT / control["before"]).read_bytes()
        after = (ROOT / control["after"]).read_bytes()
        assert hashlib.sha256(before).hexdigest() == control["before_sha256"]
        assert hashlib.sha256(after).hexdigest() == control["after_sha256"]
        kwargs = {"after": after.decode("utf-8")}
        if control["origin"] == "actual-formatter-output":
            baseline = json.loads(
                (ROOT / control["baseline_evidence"] / "result.json").read_text(
                    encoding="utf-8"
                )
            )
            kwargs = {"formatter": baseline["formatter"]}
        result = measure(
            before.decode("utf-8"),
            args.output / control["id"],
            trial_id=f"{args.output.name}-{control['id']}",
            dataset_origin="phase2-development-validation",
            ai_assisted=True,
            **kwargs,
        )
        pairs = sorted(
            result.get("matched_diagnostic_identities") or [],
            key=lambda pair: (
                pair["original"]["diagnostic"]["location"]["row"],
                pair["original"]["diagnostic"]["location"]["column"],
            ),
        )
        expected_states = [(pre, post) for _, _, pre, post in control["occurrences"]]
        actual_states = [
            (pair["original"]["visible"], pair["formatted"]["visible"])
            for pair in pairs
        ]
        checks = {
            "control_id": control["id"],
            "trial_id": result["trial_id"],
            "expected_classification": control["expected_classification"],
            "observed_classification": result["classification"],
            "source_and_output_match_frozen_control": result.get("input_sha256")
            == control["before_sha256"]
            and result.get("output_sha256") == control["after_sha256"],
            "classification_agrees": result["classification"]
            == control["expected_classification"],
            "occurrence_states_agree": actual_states == expected_states,
            "hidden_count_agrees": result.get("newly_hidden_count")
            == sum(pre and not post for pre, post in expected_states),
            "exposed_count_agrees": result.get("newly_exposed_count")
            == sum(not pre and post for pre, post in expected_states),
            "measurement_complete": result["validation_status"]
            == "measurement_complete",
        }
        checks["passed"] = all(
            value for value in checks.values() if isinstance(value, bool)
        )
        save_json(args.output / control["id"] / "control_validation.json", checks)
        results.append(result)
        validations.append(checks)
        print(
            control["id"],
            result["classification"],
            "PASS" if checks["passed"] else "FAIL",
        )
    (args.output / "results.jsonl").write_text(
        "".join(json.dumps(result, ensure_ascii=False) + "\n" for result in results),
        encoding="utf-8",
    )
    fields = [
        "trial_id",
        "formatter",
        "classification",
        "validation_status",
        "ast_equivalent",
        "formatting_changed",
        "newly_hidden_count",
        "newly_exposed_count",
        "input_sha256",
        "output_sha256",
        "evidence_path",
        "error",
    ]
    with (args.output / "summary.csv").open(
        "w", encoding="utf-8", newline=""
    ) as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        for result in results:
            writer.writerow({key: result.get(key) for key in fields})
    save_json(
        args.output / "validation.json",
        {
            "manifest_sha256": hashlib.sha256(manifest_path.read_bytes()).hexdigest(),
            "purpose": "development validation only; not a held-out detector evaluation",
            "controls": validations,
            "all_passed": all(check["passed"] for check in validations),
        },
    )
    return 0 if all(check["passed"] for check in validations) else 2


if __name__ == "__main__":
    raise SystemExit(main())
