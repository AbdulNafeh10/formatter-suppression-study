"""Freeze hand-assigned control labels using raw Ruff and comment intervention.

Run before the structural matcher exists. This procedure imports no matcher or
classifier and does not derive expected classifications from detector output.
"""

import hashlib
import io
import json
import re
import tokenize

from suppression_study.pipeline import ROOT, ast_signature, lint, measure, save_json

# Explicitly reviewed expectations in source-occurrence order, not matcher IDs.
# Each occurrence is (rule, lexeme, visible before, visible after).
SPECS = [
    (
        "semicolon-black",
        "Newly exposed",
        [("F821", "missing_a", False, True), ("F821", "missing_b", False, False)],
    ),
    (
        "semicolon-ruff",
        "Newly exposed",
        [("F821", "missing_a", False, True), ("F821", "missing_b", False, False)],
    ),
    (
        "list_inline-black",
        "Newly hidden",
        [("F821", "missing_a", False, False), ("F821", "missing_b", True, False)],
    ),
    (
        "list_inline-ruff",
        "Preserved",
        [("F821", "missing_a", False, False), ("F821", "missing_b", True, True)],
    ),
    (
        "import_inline-black",
        "Preserved",
        [("F401", "path", False, False), ("F401", "getcwd", True, True)],
    ),
    (
        "local_semicolon-ruff",
        "Newly exposed",
        [("F841", "a", False, True), ("F841", "b", False, False)],
    ),
    (
        "repeated_name-black",
        "Newly exposed",
        [("F821", "missing", False, True), ("F821", "missing", False, False)],
    ),
    (
        "unicode-black",
        "Newly exposed",
        [("F821", "absent", False, True), ("F821", "missing", False, False)],
    ),
    ("manual-hidden", "Newly hidden", [("F821", "missing_a", True, False)]),
    (
        "manual-mixed",
        "Mixed",
        [("F821", "missing_a", False, True), ("F821", "missing_b", True, False)],
    ),
]
MANUAL = {
    "manual-hidden": ("x = missing_a\n", "x = missing_a  # noqa: F821\n"),
    "manual-mixed": (
        "x = missing_a  # noqa: F821\ny = missing_b\n",
        "x = missing_a\ny = missing_b  # noqa: F821\n",
    ),
}


def neutralize_noqa(source):
    """Same-length replacement inside COMMENT tokens only, leaving code intact."""
    lines = source.splitlines(keepends=True)
    for token in tokenize.generate_tokens(io.StringIO(source).readline):
        if token.type == tokenize.COMMENT:
            row, column = token.start
            end = token.end[1]
            lines[row - 1] = (
                lines[row - 1][:column]
                + re.sub(r"\bnoqa\b", "note", token.string, flags=re.IGNORECASE)
                + lines[row - 1][end:]
            )
    transformed = "".join(lines)

    def code_tokens(text):
        return [
            (t.type, t.string)
            for t in tokenize.generate_tokens(io.StringIO(text).readline)
            if t.type != tokenize.COMMENT
        ]

    assert code_tokens(source) == code_tokens(transformed)
    assert ast_signature(source) == ast_signature(transformed)
    return transformed


def raw_key(item):
    return (
        item["code"],
        item["message"],
        item["location"]["row"],
        item["location"]["column"],
        item["end_location"]["row"],
        item["end_location"]["column"],
    )


def main():
    directory = ROOT / "datasets" / "controls" / "phase2"
    directory.mkdir(parents=True, exist_ok=False)
    manifest = {
        "schema_version": 1,
        "label_method": "literal occurrence review plus comment-only intervention; no classifier",
        "controls": [],
    }
    for control_id, expected, occurrences in SPECS:
        evidence = directory / control_id
        evidence.mkdir()
        if control_id in MANUAL:
            before, after = MANUAL[control_id]
            original = evidence / "baseline"
            record = measure(
                before,
                original,
                after=after,
                dataset_origin="phase2-manual-directive-intervention",
                ai_assisted=True,
            )
            origin = "manual-directive-intervention"
        else:
            original = ROOT / "datasets" / "results" / "phase2-probes" / control_id
            record = json.loads((original / "result.json").read_text(encoding="utf-8"))
            before = (original / "before.py").read_bytes().decode("utf-8")
            after = (original / "after.py").read_bytes().decode("utf-8")
            origin = "actual-formatter-output"
        assert record["validation_status"] == "measurement_complete"
        assert ast_signature(before) == ast_signature(after)
        review = {}
        for side, source, visible_label, underlying_label in (
            ("before", before, "A_original_visible", "B_original_underlying"),
            ("after", after, "C_formatted_visible", "D_formatted_underlying"),
        ):
            (evidence / f"{side}.py").write_bytes(source.encode("utf-8"))
            underlying = sorted(record["passes"][underlying_label], key=raw_key)
            # Source ordering is an explicit independent label convention here.
            underlying.sort(
                key=lambda item: (item["location"]["row"], item["location"]["column"])
            )
            visible = {raw_key(item) for item in record["passes"][visible_label]}
            assert len(underlying) == len(occurrences)
            details = []
            for diagnostic, (rule, lexeme, pre, post) in zip(underlying, occurrences):
                start, end = diagnostic["location"], diagnostic["end_location"]
                assert start["row"] == end["row"]
                actual_lexeme = source.splitlines()[start["row"] - 1][
                    start["column"] - 1 : end["column"] - 1
                ]
                assert (diagnostic["code"], actual_lexeme) == (rule, lexeme)
                actual_visible = raw_key(diagnostic) in visible
                assert actual_visible == (pre if side == "before" else post)
                details.append(
                    {
                        "rule": rule,
                        "lexeme": lexeme,
                        "visible": actual_visible,
                        "location": start,
                        "end_location": end,
                    }
                )
            neutralized = neutralize_noqa(source)
            (evidence / f"{side}.neutralized.py").write_bytes(
                neutralized.encode("utf-8")
            )
            ordinary = lint(neutralized, False, evidence, f"{side}_neutralized")
            assert sorted(map(raw_key, ordinary)) == sorted(map(raw_key, underlying))
            review[side] = details
        save_json(evidence / "independent_review.json", review)
        manifest["controls"].append(
            {
                "id": control_id,
                "origin": origin,
                "ai_assisted": True,
                "expected_classification": expected,
                "occurrences": occurrences,
                "baseline_evidence": original.relative_to(ROOT).as_posix(),
                "before": (evidence / "before.py").relative_to(ROOT).as_posix(),
                "after": (evidence / "after.py").relative_to(ROOT).as_posix(),
                "before_sha256": hashlib.sha256(before.encode("utf-8")).hexdigest(),
                "after_sha256": hashlib.sha256(after.encode("utf-8")).hexdigest(),
            }
        )
        print(control_id, expected, "independent checks passed")
    save_json(directory / "manifest.json", manifest)


if __name__ == "__main__":
    main()
