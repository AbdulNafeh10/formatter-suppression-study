"""Comment-only checks on prospectively defined representative drift cases.

This supports selected-case attribution, not independent labels for the full set.
"""

import json

from suppression_study.pipeline import ROOT, ast_signature, lint, save_json
from prepare_phase2_controls import neutralize_noqa, raw_key


def main():
    main_run = ROOT / "datasets/results/phase3"
    records = [
        json.loads(line)
        for line in (main_run / "results.jsonl")
        .read_text(encoding="utf-8")
        .splitlines()
    ]
    groups = {}
    for record in sorted(records, key=lambda r: r["case_id"]):
        if record["classification"] in {"Newly hidden", "Newly exposed", "Mixed"}:
            groups.setdefault((record["formatter"], record["classification"]), record)
    output = ROOT / "datasets/results/phase3-interventions"
    output.mkdir(parents=True, exist_ok=False)
    checks = []
    for (formatter, classification), record in sorted(groups.items()):
        directory = output / record["case_id"] / formatter
        directory.mkdir(parents=True)
        source_evidence = main_run / "trials" / record["case_id"] / formatter
        result = {
            "case_id": record["case_id"],
            "formatter": formatter,
            "oracle_classification": classification,
            "selection": "lexicographically first case per formatter/drift classification",
            "checks": {},
            "error": None,
        }
        try:
            for filename, underlying_pass in (
                ("before.py", "B_original_underlying"),
                ("after.py", "D_formatted_underlying"),
            ):
                source = (source_evidence / filename).read_bytes().decode("utf-8")
                neutralized = neutralize_noqa(source)
                assert ast_signature(source) == ast_signature(neutralized)
                (directory / filename).write_bytes(source.encode("utf-8"))
                (directory / f"neutralized-{filename}").write_bytes(
                    neutralized.encode("utf-8")
                )
                observed = lint(
                    neutralized, False, directory, f"neutralized_{filename[:-3]}"
                )
                assert sorted(map(raw_key, observed)) == sorted(
                    map(raw_key, record["passes"][underlying_pass])
                )
                result["checks"][filename] = True
            result["passed"] = True
        except (AssertionError, ValueError, RuntimeError, OSError) as exc:
            result.update(passed=False, error=f"{type(exc).__name__}: {exc}")
        save_json(directory / "intervention.json", result)
        checks.append(result)
    summary = {
        "representatives_checked": len(checks),
        "all_passed": all(c["passed"] for c in checks),
        "purpose": "selected-case suppression attribution support; not detector ground truth",
        "cases": checks,
    }
    save_json(output / "summary.json", summary)
    print(json.dumps(summary, indent=2))
    return 0 if summary["all_passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
