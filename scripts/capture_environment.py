"""Save installed help/version evidence and a full exact dependency snapshot."""

import argparse
from importlib.metadata import distributions
import json
from pathlib import Path
import sys

from suppression_study.pipeline import ROOT, environment, run_tool, save_json


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output", type=Path, default=ROOT / "reports" / "phase1" / "tool_verification"
    )
    evidence = parser.parse_args().output.resolve()
    evidence.mkdir(parents=True, exist_ok=False)
    commands = {
        "black_version": (["black", "--version"], ["25.1.0"]),
        "ruff_version": (["ruff", "--version"], ["0.11.13"]),
        "pytest_version": (["pytest", "--version"], ["8.3.5"]),
        "black_help": (["black", "--help"], ["--config", "--target-version"]),
        "ruff_check_help": (
            ["ruff", "check", "--help"],
            [
                "--ignore-noqa",
                "--isolated",
                "--no-cache",
                "--output-format",
                "--select",
                "--target-version",
                "--stdin-filename",
                "--no-fix",
            ],
        ),
        "ruff_format_help": (
            ["ruff", "format", "--help"],
            [
                "--isolated",
                "--line-length",
                "--target-version",
                "--stdin-filename",
            ],
        ),
        "pip_check": (["pip", "check"], ["No broken requirements found"]),
    }
    checks = {}
    for label, (arguments, expected) in commands.items():
        record = run_tool([sys.executable, "-m", *arguments], "", evidence, label)
        output = record["stdout"] + record["stderr"]
        checks[label] = (
            not record["error"]
            and record["returncode"] == 0
            and all(phrase in output for phrase in expected)
        )
    installed = sorted(
        {
            f"{dist.metadata['Name']}=={dist.version}"
            for dist in distributions()
            if dist.metadata["Name"].lower().replace("_", "-")
            != "formatter-suppression-study"
        },
        key=str.lower,
    )
    (ROOT / "requirements-lock.txt").write_text(
        "# Exact installed Phase 1 environment; Python 3.11 on Windows x64.\n"
        + "\n".join(installed)
        + "\n",
        encoding="utf-8",
    )
    save_json(evidence / "environment.json", environment())
    save_json(evidence / "checks.json", checks)
    print(json.dumps(checks, indent=2))
    return 0 if all(checks.values()) else 2


if __name__ == "__main__":
    raise SystemExit(main())
