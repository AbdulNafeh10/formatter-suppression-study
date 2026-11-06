import json
import subprocess

import pytest

from suppression_study import pipeline
from suppression_study.cli import main


EXAMPLE = (pipeline.ROOT / "tests" / "fixtures" / "feasibility.txt").read_text(
    encoding="utf-8"
)


def test_ast_ignores_positions_but_detects_code_and_type_comments():
    assert pipeline.ast_signature("x=1\n") == pipeline.ast_signature("\nx = 1\n")
    assert pipeline.ast_signature("x=1\n") != pipeline.ast_signature("x=2\n")
    assert pipeline.ast_signature("x=1 # type: int\n") != pipeline.ast_signature(
        "x=1\n"
    )


@pytest.mark.parametrize("raw", ["{}", "[1]", '[{"code": "F821"}]', "not json"])
def test_rejects_malformed_diagnostics(raw):
    with pytest.raises(ValueError):
        pipeline.parse_diagnostics(raw)


@pytest.mark.parametrize("formatter", ["black", "ruff"])
def test_real_formatter_four_passes_and_repeatability(tmp_path, formatter):
    first = pipeline.measure(EXAMPLE, tmp_path / "first", formatter=formatter)
    second = pipeline.measure(EXAMPLE, tmp_path / "second", formatter=formatter)
    assert first["error"] is None
    assert first["validation_status"] == "measurement_complete"
    assert first["ast_equivalent"] is True
    assert first["formatting_changed"] is True
    assert first["counts"] == {
        "A_original_visible": 1,
        "B_original_underlying": 3,
        "C_formatted_visible": 1,
        "D_formatted_underlying": 3,
        "original_suppressed": 2,
        "formatted_suppressed": 2,
    }
    assert first["classification"] == "Preserved"
    assert first["newly_hidden_count"] == 0
    assert first["newly_exposed_count"] == 0
    assert first["output_sha256"] == second["output_sha256"]

    # Ruff embeds a different absolute temporary filename in every invocation.
    # Ignore only that execution path, retaining codes, messages and positions.
    def without_temporary_filename(passes):
        return {
            label: [
                {key: value for key, value in item.items() if key != "filename"}
                for item in diagnostics
            ]
            for label, diagnostics in passes.items()
        }

    assert without_temporary_filename(first["passes"]) == without_temporary_filename(
        second["passes"]
    )
    assert first["environment"]["tools"] == pipeline.PINS
    for label in first["passes"]:
        command = json.loads((tmp_path / "first" / f"{label}.command.json").read_text())
        assert command["returncode"] in (0, 1)
        assert command["error"] is None
        assert ("--ignore-noqa" in command["command"]) == (label[0] in "BD")
        assert (tmp_path / "first" / f"{label}.diagnostics.json").exists()


@pytest.mark.parametrize(
    "source,count,suppressed",
    [
        ("x = absent\n", 1, 0),
        ("x = absent  # noqa\n", 1, 1),
        ("import os  # noqa: F401\nx = absent  # noqa: F821\n", 2, 2),
        ('café = "λ"\nraise RuntimeError("Analyzed programs must never run")\n', 0, 0),
    ],
)
def test_real_supplied_identical_source(tmp_path, source, count, suppressed):
    result = pipeline.measure(source, tmp_path / "evidence", after=source)
    assert result["validation_status"] == "measurement_complete"
    assert result["formatting_changed"] is False
    assert result["ast_equivalent"] is True
    assert result["counts"]["B_original_underlying"] == count
    assert result["counts"]["original_suppressed"] == suppressed
    assert result["counts"]["A_original_visible"] == count - suppressed


def test_ast_changed_pair_is_not_drift(tmp_path):
    result = pipeline.measure("x = absent\n", tmp_path / "changed", after="x = 1\n")
    assert result["classification"] == "AST changed"
    assert result["validation_status"] == "measurement_complete"
    assert result["newly_exposed_count"] is None


@pytest.mark.parametrize("before,after", [("def (\n", "x=1\n"), ("x=1\n", "def (\n")])
def test_invalid_source_retained(tmp_path, before, after):
    evidence = tmp_path / "invalid"
    result = pipeline.measure(before, evidence, after=after)
    assert result["validation_status"] == "invalid_source"
    assert result["classification"] == "Ambiguous"
    assert (evidence / "before.py").read_bytes() == before.encode()
    assert (evidence / "after.py").read_bytes() == after.encode()
    assert (evidence / "result.json").exists()


def test_existing_evidence_cannot_be_overwritten(tmp_path):
    with pytest.raises(FileExistsError):
        pipeline.measure("x=1\n", tmp_path, after="x=1\n")


def test_timeout_keeps_partial_output(tmp_path, monkeypatch):
    def timeout(*args, **kwargs):
        raise subprocess.TimeoutExpired(args[0], 1, output=b"partial", stderr=b"error")

    monkeypatch.setattr(pipeline.subprocess, "run", timeout)
    record = pipeline.run_tool(["unused"], "", tmp_path, "timeout", timeout=1)
    assert record["error"] == "timeout"
    assert (tmp_path / "timeout.stdout.txt").read_bytes() == b"partial"
    assert record["returncode"] is None


def test_real_launch_failure_is_recorded(tmp_path):
    record = pipeline.run_tool(
        [str(tmp_path / "nonexistent.exe")], "", tmp_path, "launch"
    )
    assert "FileNotFoundError" in record["error"]
    assert (tmp_path / "launch.command.json").exists()


def test_failed_formatter_is_not_success(tmp_path, monkeypatch):
    monkeypatch.setattr(
        pipeline, "run_tool", lambda *args: {"error": None, "returncode": 2}
    )
    result = pipeline.measure("x=1\n", tmp_path / "failure", formatter="black")
    assert result["classification"] == "Execution failure"
    assert result["validation_status"] == "failed"
    assert "Formatter execution failed" in result["error"]


def test_cli_real_compare_and_invalid_input(tmp_path, monkeypatch, capsys):
    before = tmp_path / "before.py"
    before.write_text("x = absent  # noqa: F821\n", encoding="utf-8")
    monkeypatch.setattr(
        "sys.argv",
        [
            "suppression_study",
            "compare",
            str(before),
            str(before),
            "--evidence",
            str(tmp_path / "cli"),
        ],
    )
    assert main() == 0
    assert json.loads(capsys.readouterr().out)["classification"] == "Preserved"
    assert (
        json.loads((tmp_path / "cli" / "result.json").read_text())["ai_assisted"]
        is None
    )
    before.write_text("def (", encoding="utf-8")
    monkeypatch.setattr(
        "sys.argv",
        [
            "suppression_study",
            "compare",
            str(before),
            str(before),
            "--evidence",
            str(tmp_path / "invalid-cli"),
        ],
    )
    assert main() == 2
