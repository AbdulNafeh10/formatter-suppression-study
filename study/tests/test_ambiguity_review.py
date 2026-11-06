"""Adversarial checks of review decisions; injected cases are not study findings."""

import importlib.util
from pathlib import Path

import pytest

PATH = Path(__file__).resolve().parents[1] / "scripts/audit_ambiguities.py"
SPEC = importlib.util.spec_from_file_location("ambiguity_review", PATH)
audit = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(audit)


def warning(source, name, code="F821"):
    rows = source.splitlines()
    row = next(i for i, line in enumerate(rows, 1) if name in line)
    column = rows[row - 1].index(name) + 1
    return {
        "code": code,
        "message": f"Review-test warning: {name}",
        "location": {"row": row, "column": column},
        "end_location": {"row": row, "column": column + len(name)},
    }


def passes(before, after, before_visible, after_visible, code="F821"):
    names = ["missing_a", "missing_b"] if code == "F821" else ["error", "leftover"]
    first = [warning(before, name, code) for name in names]
    last = [warning(after, name, code) for name in names]
    return dict(
        zip(
            audit.PASSES,
            (
                [first[i] for i in before_visible],
                first,
                [last[i] for i in after_visible],
                last,
            ),
        )
    )


@pytest.mark.parametrize(
    "visible_before,visible_after,label",
    [
        ([0, 1], [0, 1], "Preserved"),
        ([0, 1], [1], "Newly hidden"),
        ([1], [0, 1], "Newly exposed"),
        ([0], [1], "Newly hidden and newly exposed"),
    ],
)
def test_review_uses_identity_transitions_not_counts(
    visible_before, visible_after, label
):
    before = 'text = f"{missing_a}"\nother = missing_b\n'
    after = 'text = f"{missing_a}"  # noqa: F821\nother = missing_b\n'
    result = audit.assess(
        before, after, passes(before, after, visible_before, visible_after)
    )
    assert result["proposed_resolution"] == label
    assert len(result["warnings"]) == 2


def test_review_supports_exception_string_binding_explicitly():
    before = "def f():\n    try:\n        pass\n    except Exception as error:\n        pass\n    leftover=1\n"
    after = before.replace("leftover=1", "leftover = 1")
    result = audit.assess(before, after, passes(before, after, [0, 1], [0, 1], "F841"))
    assert result["proposed_resolution"] == "Preserved"
    assert any(
        w["before"]["role"] == "exception-handler binding string field"
        for w in result["warnings"]
    )


def test_unknown_or_non_subset_warnings_stay_uncertain():
    source = "x = missing_a\ny = missing_b\n"
    data = passes(source, source, [0, 1], [0, 1])
    data[audit.PASSES[0]].append(warning(source, "missing_a", "F999"))
    assert (
        audit.assess(source, source, data)["proposed_resolution"]
        == "Genuinely uncertain"
    )
    unknown = {key: [warning(source, "missing_a", "F999")] for key in audit.PASSES}
    assert (
        audit.assess(source, source, unknown)["proposed_resolution"]
        == "Genuinely uncertain"
    )


def test_intervention_changes_only_comment_noqa():
    source = 'text = "noqa"\nx = missing  # noqa: F821\n'
    changed = audit.neutralize(source)
    assert '"noqa"' in changed
    assert "# note: F821" in changed
    assert audit.signature(source) == audit.signature(changed)
