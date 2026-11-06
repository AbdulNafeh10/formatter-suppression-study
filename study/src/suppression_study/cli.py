"""Compare suppression coverage using a conservative four-pass oracle."""

import argparse
import json
from pathlib import Path

from .pipeline import measure
from .experiment import load_config, run_experiment
from .generator import write_dataset


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    analyze_parser = commands.add_parser(
        "analyze", help="Audit and analyze the retained primary datasets"
    )
    analyze_parser.add_argument(
        "--output", type=Path, default=Path("reports/phase5/analysis")
    )
    analyze_parser.add_argument("--figures", type=Path, default=Path("reports/figures"))
    generate_parser = commands.add_parser(
        "generate", help="Save the controlled factorial dataset"
    )
    generate_parser.add_argument("--config", type=Path, required=True)
    experiment_parser = commands.add_parser(
        "experiment", help="Execute paired comparisons on a saved dataset"
    )
    experiment_parser.add_argument("--config", type=Path, required=True)
    compare = commands.add_parser(
        "compare", help="Measure a supplied UTF-8 source pair"
    )
    compare.add_argument("before", type=Path)
    compare.add_argument("after", type=Path)
    format_parser = commands.add_parser(
        "format", help="Format a temporary copy and measure"
    )
    format_parser.add_argument("before", type=Path)
    format_parser.add_argument("--formatter", choices=("black", "ruff"), required=True)
    for command in (compare, format_parser):
        command.add_argument(
            "--ai-assisted",
            action="store_true",
            default=None,
            help="Identify AI-assisted source generation; otherwise unknown",
        )
        command.add_argument("--origin", default="user-supplied")
        command.add_argument(
            "--evidence", type=Path, required=True, help="New output directory"
        )
    args = parser.parse_args()
    if args.command == "analyze":
        from .analysis import run_analysis

        try:
            run_analysis(args.output, args.figures)
            return 0
        except (OSError, ValueError, RuntimeError) as exc:
            parser.exit(2, f"Analysis/input error: {exc}\n")
    if args.command in {"generate", "experiment"}:
        try:
            if args.command == "generate":
                config = load_config(args.config)
                manifest = write_dataset(config["dataset"], config["seed"])
                accepted = sum(case["accepted"] for case in manifest["cases"])
                print(
                    json.dumps(
                        {
                            "candidates": len(manifest["cases"]),
                            "accepted": accepted,
                            "dataset": str(config["dataset"]),
                        },
                        indent=2,
                    )
                )
                return 0 if accepted == len(manifest["cases"]) else 2
            run_experiment(args.config)
            return 0
        except (OSError, ValueError, RuntimeError) as exc:
            parser.exit(2, f"Experiment/input error: {exc}\n")
    try:
        before = args.before.read_bytes().decode("utf-8")
        after = (
            args.after.read_bytes().decode("utf-8")
            if args.command == "compare"
            else None
        )
        result = measure(
            before,
            args.evidence,
            after=after,
            formatter=args.formatter if args.command == "format" else None,
            dataset_origin=args.origin,
            ai_assisted=args.ai_assisted,
        )
    except (OSError, UnicodeError, ValueError) as exc:
        parser.exit(2, f"Input/evidence error: {exc}\n")
    summary = {
        key: result.get(key)
        for key in (
            "classification",
            "validation_status",
            "ast_equivalent",
            "formatting_changed",
            "counts",
            "newly_hidden_count",
            "newly_exposed_count",
            "explanation",
            "error",
            "evidence_path",
        )
    }
    summary["matched_diagnostic_identities"] = [
        {
            "identity": pair["identity"],
            "rule": pair["original"]["rule"],
            "transition": pair.get("transition"),
            "before_location": pair["original"]["diagnostic"]["location"],
            "after_location": pair["formatted"]["diagnostic"]["location"],
        }
        for pair in result.get("matched_diagnostic_identities") or []
    ]
    print(json.dumps(summary, indent=2))
    if result["validation_status"] != "measurement_complete":
        return 2
    if result["classification"] in {"Newly hidden", "Newly exposed", "Mixed"}:
        return 1
    return 0 if result["classification"] == "Preserved" else 3
