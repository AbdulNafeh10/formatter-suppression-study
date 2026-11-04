"""Bounded tool execution, raw evidence capture, and four-pass measurements.

No analyzed program is executed. Positions identify diagnostics only within an
identical source snapshot, never across formatting transformations.
"""

from __future__ import annotations

import ast
from collections import Counter
from datetime import datetime, timezone
import hashlib
from importlib.metadata import version
import json
from pathlib import Path
import platform
import subprocess
import sys
import tempfile
from typing import Any

from .classifier import classify
from .matching import MatchError

ROOT = Path(__file__).resolve().parents[2]
RULES = "F401,F821,F841"
TIMEOUT = 30
PINS = {"black": "25.1.0", "ruff": "0.11.13", "pytest": "8.3.5"}


def save_json(path: Path, value: Any) -> None:
    path.write_text(
        json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def run_tool(
    command: list[str],
    source: str,
    evidence: Path,
    label: str,
    timeout: float = TIMEOUT,
) -> dict:
    """Preserve successful, nonzero, timeout, and launch-failure outcomes."""
    record: dict[str, Any] = {
        "command": command,
        "timeout_seconds": timeout,
        "returncode": None,
        "stdout": "",
        "stderr": "",
        "error": None,
    }
    try:
        with tempfile.TemporaryDirectory(prefix="suppression-study-") as directory:
            record["cwd"] = directory
            completed = subprocess.run(
                command,
                input=source.encode("utf-8"),
                capture_output=True,
                cwd=directory,
                timeout=timeout,
                check=False,
            )
        record.update(
            returncode=completed.returncode,
            stdout=completed.stdout.decode("utf-8"),
            stderr=completed.stderr.decode("utf-8"),
        )
    except subprocess.TimeoutExpired as exc:
        record.update(
            error="timeout",
            stdout=(exc.stdout or b"").decode("utf-8", errors="replace"),
            stderr=(exc.stderr or b"").decode("utf-8", errors="replace"),
        )
    except (OSError, UnicodeError) as exc:
        record["error"] = f"{type(exc).__name__}: {exc}"
    save_json(evidence / f"{label}.command.json", record)
    (evidence / f"{label}.stdout.txt").write_bytes(record["stdout"].encode("utf-8"))
    (evidence / f"{label}.stderr.txt").write_bytes(record["stderr"].encode("utf-8"))
    return record


def parse_diagnostics(raw: str) -> list[dict]:
    data = json.loads(raw)
    if not isinstance(data, list):
        raise ValueError("Ruff output is not a JSON list")
    for item in data:
        if not isinstance(item, dict):
            raise ValueError("Diagnostic is not an object")
        if not isinstance(item.get("code"), str) or not isinstance(
            item.get("message"), str
        ):
            raise ValueError("Diagnostic lacks a rule code or message")
        for field in ("location", "end_location"):
            location = item.get(field)
            if not isinstance(location, dict) or any(
                type(location.get(axis)) is not int or location[axis] < 1
                for axis in ("row", "column")
            ):
                raise ValueError("Diagnostic lacks valid source coordinates")
    return data


def lint(source: str, ignore_noqa: bool, evidence: Path, label: str) -> list[dict]:
    command = [
        sys.executable,
        "-m",
        "ruff",
        "check",
        "--isolated",
        "--no-cache",
        "--select",
        RULES,
        "--target-version",
        "py311",
        "--output-format",
        "json",
        "--no-fix",
        "--stdin-filename",
        "study_input.py",
    ]
    if ignore_noqa:
        command.append("--ignore-noqa")
    record = run_tool(command + ["-"], source, evidence, label)
    if record["error"] or record["returncode"] not in (0, 1):
        raise RuntimeError(f"{label}: Ruff execution failed; see command evidence")
    diagnostics = parse_diagnostics(record["stdout"])
    if bool(diagnostics) != (record["returncode"] == 1):
        raise ValueError(f"{label}: Ruff status and diagnostic output disagree")
    save_json(evidence / f"{label}.diagnostics.json", diagnostics)
    return diagnostics


def ast_signature(source: str) -> str:
    # Deliberately strict: type comments included; source coordinates excluded.
    tree = ast.parse(source, type_comments=True, feature_version=(3, 11))
    # Compile for legality (e.g. return outside a function); never execute it.
    compile(tree, "<study-input>", "exec", dont_inherit=True, optimize=0)
    return ast.dump(tree, annotate_fields=True, include_attributes=False)


def same_source_suppressed(underlying: list[dict], visible: list[dict]) -> list[dict]:
    """Safe positional subtraction ONLY between passes on identical source."""

    def key(item: dict) -> tuple:
        return (
            item["code"],
            item["message"],
            item["location"]["row"],
            item["location"]["column"],
            item["end_location"]["row"],
            item["end_location"]["column"],
        )

    remaining = Counter(key(item) for item in visible)
    underlying_keys = Counter(key(item) for item in underlying)
    if remaining - underlying_keys:
        raise MatchError(
            "Visible diagnostics are not a subset of underlying diagnostics"
        )
    suppressed = []
    for item in underlying:
        identity = key(item)
        if remaining[identity]:
            remaining[identity] -= 1
        else:
            suppressed.append(item)
    return suppressed


def environment() -> dict:
    commit = subprocess.run(
        ["git", "-C", str(ROOT), "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
        timeout=TIMEOUT,
        check=False,
    )
    status = subprocess.run(
        ["git", "-C", str(ROOT), "status", "--porcelain"],
        capture_output=True,
        text=True,
        timeout=TIMEOUT,
        check=False,
    )
    return {
        "os": platform.platform(),
        "python": sys.version,
        "python_executable": sys.executable,
        "tools": {name: version(name) for name in PINS},
        "repository_commit": commit.stdout.strip() if commit.returncode == 0 else None,
        "repository_dirty": (
            bool(status.stdout.strip()) if status.returncode == 0 else None
        ),
        "seed": 0,
        "random_generation": False,
    }


def measure(
    before: str,
    evidence: Path,
    *,
    after: str | None = None,
    formatter: str | None = None,
    trial_id: str | None = None,
    dataset_origin: str = "user-supplied",
    ai_assisted: bool | None = None,
    study_phase: int = 2,
    case_metadata: dict | None = None,
    run_environment: dict | None = None,
) -> dict:
    """Create a new evidence directory. Existing evidence is never overwritten."""
    if (after is None) == (formatter is None):
        raise ValueError("Supply exactly one of after or formatter")
    if formatter is not None and formatter not in ("black", "ruff"):
        raise ValueError("Unsupported formatter")
    allowed_metadata = {
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
        "manifest_sha256",
        "repository",
        "repository_url",
        "repository_commit",
        "repository_tag",
        "original_path",
        "source_url",
        "file_role",
        "configuration_mode",
        "population_rank",
        "source_acquisition_method",
        "native_config",
    }
    if case_metadata and set(case_metadata) - allowed_metadata:
        raise ValueError("Case metadata contains unsupported/reserved fields")
    evidence = evidence.resolve()
    evidence.mkdir(parents=True, exist_ok=False)
    result: dict[str, Any] = {
        "schema_version": 2,
        "phase": study_phase,
        "trial_id": trial_id or evidence.name,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "dataset_origin": dataset_origin,
        "ai_assisted": ai_assisted,
        "formatter": formatter,
        "evidence_path": str(evidence),
        "classification": "Execution failure",
        "validation_status": "failed",
        "ast_equivalent": None,
        "formatting_changed": None,
        "matched_diagnostic_identities": None,
        "newly_hidden_count": None,
        "newly_exposed_count": None,
        "configuration": {
            "rules": RULES.split(","),
            "target_version": "py311",
            "line_length": 88,
            "preview": False,
            "timeout_seconds": TIMEOUT,
            "isolated_lint": True,
        },
        "error": None,
    }
    result.update(case_metadata or {})
    (evidence / "before.py").write_bytes(before.encode("utf-8"))
    result["input_sha256"] = hashlib.sha256(before.encode("utf-8")).hexdigest()
    if after is not None:
        (evidence / "after.py").write_bytes(after.encode("utf-8"))
    try:
        result["environment"] = (
            environment() if run_environment is None else dict(run_environment)
        )
        if result["environment"]["tools"] != PINS:
            raise RuntimeError("Tool versions do not match study pins")
        signature_before = ast_signature(before)
        (evidence / "before.ast.txt").write_text(signature_before, encoding="utf-8")
        if formatter == "black":
            config = (ROOT / "configs" / "black.toml").read_bytes()
            (evidence / "black.toml").write_bytes(config)
            command = [
                sys.executable,
                "-m",
                "black",
                "--config",
                str(evidence / "black.toml"),
                "-",
            ]
        elif formatter == "ruff":
            command = [
                sys.executable,
                "-m",
                "ruff",
                "format",
                "--isolated",
                "--line-length",
                "88",
                "--target-version",
                "py311",
                "--stdin-filename",
                "study_input.py",
                "-",
            ]
        if formatter:
            formatting = run_tool(command, before, evidence, "formatter")
            if formatting["error"] or formatting["returncode"] != 0:
                raise RuntimeError("Formatter execution failed; see command evidence")
            after = formatting["stdout"]
            (evidence / "after.py").write_bytes(after.encode("utf-8"))
        assert after is not None
        result["output_sha256"] = hashlib.sha256(after.encode("utf-8")).hexdigest()
        result["formatting_changed"] = before != after
        signature_after = ast_signature(after)
        (evidence / "after.ast.txt").write_text(signature_after, encoding="utf-8")
        result["ast_equivalent"] = signature_before == signature_after
        passes = {}
        for label, source, ignore in (
            ("A_original_visible", before, False),
            ("B_original_underlying", before, True),
            ("C_formatted_visible", after, False),
            ("D_formatted_underlying", after, True),
        ):
            passes[label] = lint(source, ignore, evidence, label)
            # Retain completed passes even if a subsequent pass fails.
            result["passes"] = passes
        original_suppressed = same_source_suppressed(
            passes["B_original_underlying"], passes["A_original_visible"]
        )
        formatted_suppressed = same_source_suppressed(
            passes["D_formatted_underlying"], passes["C_formatted_visible"]
        )
        result["suppressed_within_source"] = {
            "original": original_suppressed,
            "formatted": formatted_suppressed,
        }
        result["counts"] = {label: len(items) for label, items in passes.items()}
        result["counts"].update(
            original_suppressed=len(original_suppressed),
            formatted_suppressed=len(formatted_suppressed),
        )
        result["validation_status"] = "measurement_complete"
        result.update(classify(before, after, passes))
        save_json(
            evidence / "matching.json",
            {
                key: result.get(key)
                for key in (
                    "classification",
                    "anchors",
                    "matched_diagnostic_identities",
                    "underlying_changes",
                    "matching_errors",
                    "explanation",
                )
            },
        )
    except MatchError as exc:
        result.update(
            classification="Ambiguous",
            validation_status="measurement_complete",
            explanation=f"Within-source diagnostic consistency could not be established: {exc}",
            matching_errors=[str(exc)],
        )
    except SyntaxError as exc:
        result.update(
            classification="Ambiguous",
            validation_status="invalid_source",
            error=f"SyntaxError: {exc}",
        )
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as exc:
        result["error"] = f"{type(exc).__name__}: {exc}"
    save_json(evidence / "result.json", result)
    return result
