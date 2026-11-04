"""Describe uncertainty without changing the frozen oracle's classifications."""

import argparse
import ast
from collections import Counter
import json
from pathlib import Path
import tokenize

from suppression_study.pipeline import ROOT, lint, save_json
from suppression_study.matching import MatchError, SourceIndex, diagnostic_span
from prepare_phase2_controls import neutralize_noqa, raw_key


def type_ignore_position_only(before, after):
    def normalized(source):
        tree = ast.parse(source, type_comments=True, feature_version=(3, 11))
        for node in ast.walk(tree):
            if isinstance(node, ast.TypeIgnore):
                node.lineno = 0
        return ast.dump(tree, include_attributes=False)

    return normalized(before) == normalized(after)


def ast_differences(before, after):
    differences = []

    def compare(a, b, path):
        if isinstance(a, ast.AST) and isinstance(b, ast.AST) and type(a) is type(b):
            for field, value in ast.iter_fields(a):
                compare(value, getattr(b, field), f"{path}.{field}")
        elif isinstance(a, list) and isinstance(b, list):
            if len(a) != len(b):
                differences.append(
                    {"path": path, "before_length": len(a), "after_length": len(b)}
                )
            for index, (left, right) in enumerate(zip(a, b)):
                compare(left, right, f"{path}[{index}]")
        elif a != b:
            differences.append(
                {"path": path, "before": str(a)[:200], "after": str(b)[:200]}
            )

    compare(
        ast.parse(before, type_comments=True), ast.parse(after, type_comments=True), "$"
    )
    return {"total_field_differences": len(differences), "first_25": differences[:25]}


def anchor_failures(before, after, passes):
    errors = []
    for label, source in (
        ("B_original_underlying", before),
        ("D_formatted_underlying", after),
    ):
        index = SourceIndex(source)
        for diagnostic in passes.get(label, []):
            try:
                index.anchor(diagnostic)
            except MatchError as exc:
                span = diagnostic_span(diagnostic, index.lines)
                line = index.lines[span[0][0] - 1]
                surrounding = [
                    t for t in index.tokens if t.start <= span[0] and span[1] <= t.end
                ]
                reason = (
                    "string_embedded_name"
                    if diagnostic["code"] == "F821"
                    and any(t.type == tokenize.STRING for t in surrounding)
                    else (
                        "exception_handler_binding"
                        if diagnostic["code"] == "F841"
                        and line.lstrip().startswith("except")
                        else "other_span_or_binding"
                    )
                )
                errors.append(
                    {
                        "pass": label,
                        "rule": diagnostic["code"],
                        "message": diagnostic["message"],
                        "location": diagnostic["location"],
                        "source_line": line[:300],
                        "error": str(exc),
                        "reason": reason,
                    }
                )
    return errors


def investigate(records, mode, output, run_directory):
    investigations, interventions = [], []
    for record in records:
        if record.get("classification") in {
            "Ambiguous",
            "AST changed",
            "Diagnostic changed",
            "Execution failure",
        }:
            evidence = (
                output / "findings" / mode / record["case_id"] / record["formatter"]
            )
            evidence.mkdir(parents=True)
            finding = {
                "trial_id": record["trial_id"],
                "repository": record["repository"],
                "original_path": record["original_path"],
                "formatter": record["formatter"],
                "classification_retained": record["classification"],
                "matching_errors": record.get("matching_errors"),
                "execution_error": record.get("error"),
                "explanation": record.get("explanation"),
                "mode": mode,
            }
            trial = run_directory / "trials" / record["case_id"] / record["formatter"]
            before = (trial / "before.py").read_bytes().decode()
            after = (
                (trial / "after.py").read_bytes().decode()
                if (trial / "after.py").exists()
                else None
            )
            if record["classification"] == "AST changed":
                finding["type_ignore_line_metadata_only"] = type_ignore_position_only(
                    before, after
                )
                finding["ast_field_differences"] = ast_differences(before, after)
                finding["interpretation"] = (
                    "TypeIgnore line metadata differs; strict primary AST outcome retained."
                    if finding["type_ignore_line_metadata_only"]
                    else "Other AST content differs; strict AST exclusion retained, no drift attribution."
                )
            elif record["classification"] == "Ambiguous" and after is not None:
                finding["anchor_failures"] = anchor_failures(
                    before, after, record.get("passes", {})
                )
                finding["anchor_failure_reason_counts"] = dict(
                    Counter(error["reason"] for error in finding["anchor_failures"])
                )
            save_json(evidence / "investigation.json", finding)
            investigations.append(finding)
        if mode == "standardized" and record.get("classification") in {
            "Newly hidden",
            "Newly exposed",
            "Mixed",
        }:
            trial = run_directory / "trials" / record["case_id"] / record["formatter"]
            evidence = (
                output / "interventions" / record["case_id"] / record["formatter"]
            )
            evidence.mkdir(parents=True)
            intervention = {
                "trial_id": record["trial_id"],
                "classification": record["classification"],
                "passed": False,
                "error": None,
            }
            try:
                for filename, underlying in (
                    ("before.py", "B_original_underlying"),
                    ("after.py", "D_formatted_underlying"),
                ):
                    source = (trial / filename).read_bytes().decode()
                    neutralized = neutralize_noqa(source)
                    (evidence / f"neutralized-{filename}").write_bytes(
                        neutralized.encode()
                    )
                    observed = lint(neutralized, False, evidence, filename[:-3])
                    assert sorted(map(raw_key, observed)) == sorted(
                        map(raw_key, record["passes"][underlying])
                    )
                intervention["passed"] = True
            except (AssertionError, ValueError, RuntimeError, OSError) as exc:
                intervention["error"] = f"{type(exc).__name__}: {exc}"
            save_json(evidence / "intervention.json", intervention)
            interventions.append(intervention)
    return investigations, interventions


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=ROOT / "datasets/results/phase4")
    parser.add_argument(
        "--output", type=Path, default=ROOT / "datasets/results/phase4-investigation"
    )
    args = parser.parse_args()
    directory = args.output.resolve()
    directory.mkdir(parents=True, exist_ok=False)
    records = [
        json.loads(line)
        for line in (args.input / "results.jsonl")
        .read_text(encoding="utf-8")
        .splitlines()
    ]
    native = [
        json.loads(line)
        for line in (args.input / "native_results.jsonl")
        .read_text(encoding="utf-8")
        .splitlines()
    ]
    primary_findings, interventions = investigate(
        records, "standardized", directory, args.input
    )
    native_findings, _ = investigate(native, "project_config", directory, args.input)
    summary = {
        "primary_uncertain_trials": len(primary_findings),
        "native_uncertain_trials": len(native_findings),
        "primary_reason_counts": dict(
            Counter(
                (
                    f["classification_retained"]
                    + ": "
                    + "; ".join(f["matching_errors"] or [])
                    + (
                        " TypeIgnore metadata only"
                        if f.get("type_ignore_line_metadata_only")
                        else ""
                    )
                )
                for f in primary_findings
            )
        ),
        "primary_drift_interventions": len(interventions),
        "all_interventions_passed": all(i["passed"] for i in interventions),
        "interpretation": "Original classifications retained. Zero interventions means no primary drift to audit, not validated detector accuracy.",
        "interventions": interventions,
    }
    save_json(directory / "summary.json", summary)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
