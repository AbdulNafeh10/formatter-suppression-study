"""The supplementary overlay must never replace or silently impute primary labels."""

import copy
import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "reviewed_analysis", ROOT / "scripts/analyze_reviewed_results.py"
)
analysis = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(analysis)


def example():
    original = [
        {
            "case_id": "example",
            "formatter": "black",
            "classification": "Ambiguous",
            "input_sha256": "before",
            "output_sha256": "after",
        }
    ]
    review = [
        {
            "case_id": "example",
            "formatter": "black",
            "original_classification": "Ambiguous",
            "before_sha256": "before",
            "after_sha256": "after",
            "review": {
                "proposed_resolution": "Preserved",
                "hidden": 0,
                "exposed": 0,
                "uncertainty": None,
                "warnings": [{"before": {"visible": True}, "after": {"visible": True}}],
            },
        }
    ]
    return original, review


def test_overlay_leaves_primary_labels_unchanged():
    original, review = example()
    before = copy.deepcopy(original)
    revised = analysis.reviewed_copy(original, review)
    assert original == before
    assert revised[0]["original_classification"] == "Ambiguous"
    assert revised[0]["classification"] == "Preserved"


@pytest.mark.parametrize(
    "change", ["missing", "duplicate", "wrong_hash", "visibility_change", "uncertain"]
)
def test_overlay_rejects_unjustified_reclassification(change):
    original, review = example()
    if change == "missing":
        review = []
    elif change == "duplicate":
        review *= 2
    elif change == "wrong_hash":
        review[0]["before_sha256"] = "another source"
    elif change == "visibility_change":
        review[0]["review"]["warnings"][0]["after"]["visible"] = False
    else:
        review[0]["review"]["uncertainty"] = "unresolved"
    with pytest.raises(ValueError):
        analysis.reviewed_copy(original, review)
