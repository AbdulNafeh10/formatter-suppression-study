"""Independent fixed-label integration controls and adversarial unit cases."""

import hashlib
import importlib.util
import json

import pytest

from suppression_study.classifier import classify
from suppression_study.matching import MatchError, SourceIndex
from suppression_study.pipeline import ROOT, measure, parse_diagnostics
from suppression_study.cli import main

MANIFEST = json.loads(
    (ROOT / "datasets/controls/phase2/manifest.json").read_text(encoding="utf-8")
)


@pytest.mark.parametrize("control", MANIFEST["controls"], ids=lambda item: item["id"])
def test_frozen_independent_controls_with_actual_ruff(tmp_path, control):
    before = (ROOT / control["before"]).read_bytes()
    after = (ROOT / control["after"]).read_bytes()
    assert hashlib.sha256(before).hexdigest() == control["before_sha256"]
    assert hashlib.sha256(after).hexdigest() == control["after_sha256"]
    result = measure(before.decode(), tmp_path / control["id"], after=after.decode())
    assert result["classification"] == control["expected_classification"], result.get(
        "explanation"
    )
    assert result["validation_status"] == "measurement_complete"
    assert result["newly_hidden_count"] == sum(
        pre and not post for _, _, pre, post in control["occurrences"]
    )
    assert result["newly_exposed_count"] == sum(
        not pre and post for _, _, pre, post in control["occurrences"]
    )
    pairs = result["matched_diagnostic_identities"]
    assert len({pair["identity"] for pair in pairs}) == len(control["occurrences"])
    # Compare expected occurrence-specific coverage, not just aggregate labels.
    by_position = sorted(
        pairs,
        key=lambda pair: (
            pair["original"]["diagnostic"]["location"]["row"],
            pair["original"]["diagnostic"]["location"]["column"],
        ),
    )
    assert [
        (pair["original"]["visible"], pair["formatted"]["visible"])
        for pair in by_position
    ] == [(pre, post) for _, _, pre, post in control["occurrences"]]
    assert (tmp_path / control["id"] / "matching.json").exists()


@pytest.mark.parametrize("formatter", ["black", "ruff"])
def test_actual_formatter_positive_reproduces_frozen_output(tmp_path, formatter):
    control = next(
        c for c in MANIFEST["controls"] if c["id"] == f"semicolon-{formatter}"
    )
    before = (ROOT / control["before"]).read_bytes().decode()
    result = measure(before, tmp_path / formatter, formatter=formatter)
    assert result["output_sha256"] == control["after_sha256"]
    assert result["classification"] == "Newly exposed"
    assert (
        result["matched_diagnostic_identities"][0]["identity"] == "F821@$.body[0].value"
    )


def diagnostic(
    code="F821", row=1, column=5, end=12, message="Undefined name `missing`"
):
    return {
        "code": code,
        "message": message,
        "location": {"row": row, "column": column},
        "end_location": {"row": row, "column": end},
    }


def passes(before, after=None, visible_before=None, visible_after=None):
    after = before if after is None else after
    return {
        "B_original_underlying": before,
        "D_formatted_underlying": after,
        "A_original_visible": before if visible_before is None else visible_before,
        "C_formatted_visible": after if visible_after is None else visible_after,
    }


@pytest.mark.parametrize(
    "items,reason",
    [
        ([diagnostic(code="E501")], "Unsupported"),
        ([diagnostic(row=99)], "Out-of-bounds"),
        ([diagnostic(column=0)], "Out-of-bounds"),
        ([diagnostic(column=12, end=5)], "reversed"),
        ([diagnostic(column=6, end=12)], "complete identifier"),
        ([diagnostic(column=1, end=2)], "found 0"),
        ([diagnostic(), diagnostic()], "Duplicate"),
    ],
)
def test_uncertain_correspondence_is_ambiguous(items, reason):
    result = classify("x = missing\n", "x = missing\n", passes(items))
    assert result["classification"] == "Ambiguous"
    assert reason in result["explanation"]
    assert result["newly_hidden_count"] is None


def test_same_counts_different_underlying_occurrences_is_not_drift():
    source = "x = missing\ny = missing\n"
    first, second = diagnostic(), diagnostic(row=2)
    result = classify(source, source, passes([first], [second], [], [second]))
    assert result["classification"] == "Diagnostic changed"
    assert len(result["underlying_changes"]["removed"]) == 1
    assert len(result["underlying_changes"]["added"]) == 1
    assert result["newly_hidden_count"] is None


def test_changed_message_blocks_attribution():
    original = diagnostic()
    changed = dict(original, message="Different diagnostic description")
    result = classify(
        "x = missing\n", "x = missing\n", passes([original], [changed], [original], [])
    )
    assert result["classification"] == "Diagnostic changed"
    assert result["underlying_changes"]["message_changed"] == ["F821@$.body[0].value"]


def test_subset_violation_and_duplicate_visible_are_not_drift():
    for data in (
        passes([diagnostic()], visible_before=[diagnostic(row=2)]),
        passes([diagnostic()], visible_before=[diagnostic(), diagnostic()]),
    ):
        result = classify("x = missing\n", "x = missing\n", data)
        assert result["classification"] == "Ambiguous"
        assert "subset" in result["explanation"]


def test_reordered_diagnostics_do_not_change_identity():
    first, second = diagnostic(), diagnostic(row=2)
    source = "x = missing\ny = missing\n"
    result = classify(source, source, passes([first, second], [second, first]))
    assert result["classification"] == "Preserved"
    assert len(result["matched_diagnostic_identities"]) == 2


def test_empty_diagnostic_set_and_ast_precedence():
    assert classify("", "\n", passes([]))["classification"] == "Preserved"
    assert (
        classify("x=1\n", "x=2\n", passes([diagnostic(code="E501")]))["classification"]
        == "AST changed"
    )


def test_coordinate_conversion_after_non_ascii_and_crlf():
    source = "é = 1; x = missing\r\n"
    start = source.index("missing") + 1
    anchor = SourceIndex(source).anchor(diagnostic(column=start, end=start + 7))
    assert anchor["ast_path"] == "$.body[1].value"
    assert anchor["diagnostic_tokens"] == [(1, "missing")]


def test_ambiguous_nonunique_anchor_and_context_mismatch(monkeypatch):
    index = SourceIndex("x = missing\n")
    index.nodes += index.nodes
    with pytest.raises(MatchError, match="found 2"):
        index.anchor(diagnostic())
    # Deliberately corrupt token context to exercise the safeguard.
    import suppression_study.classifier as module

    real = module.anchor_diagnostics
    count = 0

    def corrupted(source, diagnostics):
        nonlocal count
        result = real(source, diagnostics)
        count += 1
        if count == 2:
            result["F821@$.body[0].value"]["construct_tokens"] = [(1, "wrong")]
        return result

    monkeypatch.setattr(module, "anchor_diagnostics", corrupted)
    result = classify("x = missing\n", "x = missing\n", passes([diagnostic()]))
    assert result["classification"] == "Ambiguous"
    assert "Mismatched" in result["explanation"]


@pytest.mark.parametrize(
    "source",
    [
        "import os.path as operating_system\n",
        "from os import path as p, getcwd as cwd\n",
        "def f():\n    x, y = (1, 2)\n",
        "items = [unknown(i) for i in range(3)]\n",
        "x = missing + missing\n",
        "é = 1; x = absent\n",
    ],
)
def test_additional_real_constructs_are_preserved(tmp_path, source):
    result = measure(source, tmp_path / "construct", after="\n" + source)
    assert result["classification"] == "Preserved", result.get("explanation")


def test_fstring_inner_name_conservatively_ambiguous(tmp_path):
    result = measure(
        'x = f"{missing}"\n', tmp_path / "fstring", after='x = f"{missing}"\n'
    )
    assert result["classification"] == "Ambiguous"
    assert result["newly_exposed_count"] is None


@pytest.mark.parametrize(
    "raw",
    [
        '[{"code":"F821","message":"x","location":{"row":true,"column":1},"end_location":{"row":1,"column":2}}]',
        '[{"code":null,"message":"x"}]',
    ],
)
def test_more_invalid_json_records(raw):
    with pytest.raises(ValueError):
        parse_diagnostics(raw)


def test_real_f841_unicode_target(tmp_path):
    result = measure(
        "def f():\n    é = 1\n",
        tmp_path / "unicode-local",
        after="def f():\n    é = 1  # noqa: F841\n",
    )
    assert result["classification"] == "Newly hidden"
    assert result["newly_hidden_count"] == 1


@pytest.mark.parametrize(
    "formatter,kind", [("black", "Newly hidden"), ("ruff", "Preserved")]
)
def test_formatter_difference_is_reproduced(tmp_path, formatter, kind):
    control = next(
        c for c in MANIFEST["controls"] if c["id"] == f"list_inline-{formatter}"
    )
    result = measure(
        (ROOT / control["before"]).read_bytes().decode(),
        tmp_path / formatter,
        formatter=formatter,
    )
    assert result["classification"] == kind
    assert result["output_sha256"] == control["after_sha256"]


@pytest.mark.parametrize(
    "control_id,expected_exit", [("manual-hidden", 1), ("list_inline-ruff", 0)]
)
def test_cli_exit_codes_and_affected_identity(
    tmp_path, monkeypatch, capsys, control_id, expected_exit
):
    control = next(c for c in MANIFEST["controls"] if c["id"] == control_id)
    monkeypatch.setattr(
        "sys.argv",
        [
            "suppression_study",
            "compare",
            str(ROOT / control["before"]),
            str(ROOT / control["after"]),
            "--evidence",
            str(tmp_path / "cli"),
        ],
    )
    assert main() == expected_exit
    output = json.loads(capsys.readouterr().out)
    assert output["classification"] == control["expected_classification"]
    assert output["matched_diagnostic_identities"]


def test_neutralization_preserves_strings_unicode_and_case():
    spec = importlib.util.spec_from_file_location(
        "independent_control_check", ROOT / "scripts/prepare_phase2_controls.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    source = 'é = "# noqa: F821"  # NOQA: F401\n'
    assert module.neutralize_noqa(source) == 'é = "# noqa: F821"  # note: F401\n'


@pytest.mark.parametrize(
    "source", ["return 1\n", "break\n", "await f()\n", "x = '\x00'\n"]
)
def test_parseable_but_illegal_source_is_invalid(tmp_path, source):
    result = measure(source, tmp_path / "invalid", after=source)
    assert result["validation_status"] == "invalid_source"
    assert result["classification"] == "Ambiguous"


@pytest.mark.parametrize(
    "before,after,expected",
    [
        (
            "import os  # noqa: F401, F821\nx = absent  # noqa\n",
            "import os\nx = absent\n",
            "Newly exposed",
        ),
        ("x = absent\n", "x = absent  # noqa: F401\n", "Preserved"),
        ("# noqa: F821\nx = absent\n", "x = absent\n", "Preserved"),
        (
            'x = absent\ntext = "# noqa: F821"\n',
            'x = absent\ntext = "# noqa: F821"\n',
            "Preserved",
        ),
        ("# ruff: noqa\nx = absent\n", "x = absent\n", "Newly exposed"),
    ],
)
def test_actual_directive_scope_and_multiple_codes(tmp_path, before, after, expected):
    result = measure(before, tmp_path / "directives", after=after)
    assert result["classification"] == expected


def test_actual_linter_error_retains_command_evidence(tmp_path, monkeypatch):
    import suppression_study.pipeline as module

    real = module.run_tool

    def invalid_option(command, source, evidence, label, **kwargs):
        if label.startswith("A_"):
            command = command[:-1] + ["--invalid-study-option", "-"]
        return real(command, source, evidence, label, **kwargs)

    monkeypatch.setattr(module, "run_tool", invalid_option)
    evidence = tmp_path / "linter-failure"
    result = measure("x=1\n", evidence, after="x=1\n")
    assert result["classification"] == "Execution failure"
    assert result["validation_status"] == "failed"
    command = json.loads((evidence / "A_original_visible.command.json").read_text())
    assert command["returncode"] == 2
    assert command["stderr"]


def test_malformed_json_and_partial_pass_failure(tmp_path, monkeypatch):
    import suppression_study.pipeline as module

    real = module.run_tool

    def malformed(command, source, evidence, label, **kwargs):
        if label.startswith("B_"):
            return {"error": None, "returncode": 0, "stdout": "not-json"}
        return real(command, source, evidence, label, **kwargs)

    monkeypatch.setattr(module, "run_tool", malformed)
    evidence = tmp_path / "malformed"
    result = measure("x=1\n", evidence, after="x=1\n")
    assert result["classification"] == "Execution failure"
    assert list(result["passes"]) == ["A_original_visible"]
    assert (evidence / "A_original_visible.diagnostics.json").exists()


def test_pipeline_subset_failure_is_ambiguous(tmp_path, monkeypatch):
    import suppression_study.pipeline as module

    def inconsistent_lint(source, ignore, evidence, label):
        return [] if ignore else [diagnostic()]

    monkeypatch.setattr(module, "lint", inconsistent_lint)
    result = measure("x = missing\n", tmp_path / "inconsistent", after="x = missing\n")
    assert result["classification"] == "Ambiguous"
    assert result["newly_hidden_count"] is None


@pytest.mark.parametrize(
    "before,after", [("x=1\n", "x=2\n"), ('x = f"{missing}"\n', 'x = f"{missing}"\n')]
)
def test_cli_inconclusive_exit(tmp_path, monkeypatch, capsys, before, after):
    first, second = tmp_path / "before.py", tmp_path / "after.py"
    first.write_text(before, encoding="utf-8")
    second.write_text(after, encoding="utf-8")
    monkeypatch.setattr(
        "sys.argv",
        [
            "suppression_study",
            "compare",
            str(first),
            str(second),
            "--evidence",
            str(tmp_path / "cli"),
        ],
    )
    assert main() == 3
    assert json.loads(capsys.readouterr().out)["classification"] in {
        "AST changed",
        "Ambiguous",
    }


def test_repeated_same_name_coverage_swap_is_mixed(tmp_path):
    before = "x = missing  # noqa: F821\ny = missing\n"
    after = "x = missing\ny = missing  # noqa: F821\n"
    result = measure(before, tmp_path / "same-count-swap", after=after)
    assert result["classification"] == "Mixed"
    assert result["newly_hidden_count"] == result["newly_exposed_count"] == 1
    assert (
        result["counts"]["A_original_visible"]
        == result["counts"]["C_formatted_visible"]
        == 1
    )


def test_non_bmp_unicode_before_diagnostic(tmp_path):
    source = 'emoji = "🙂"; x = absent\n'
    result = measure(source, tmp_path / "emoji", after=source + "\n")
    assert result["classification"] == "Preserved"
    assert (
        result["matched_diagnostic_identities"][0]["identity"] == "F821@$.body[1].value"
    )
