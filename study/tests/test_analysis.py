import copy
import json

import numpy as np
import pandas as pd
import pytest

from suppression_study.analysis import (
    make_pairs,
    normalized_rows,
    pair_summary,
    summarize_group,
)
from suppression_study.analysis_audit import audit_arithmetic
from suppression_study.pipeline import ROOT
from suppression_study.statistics import (
    cluster_bootstrap,
    finite_population_bounds,
    paired_bounds,
    wilson_interval,
)


@pytest.mark.parametrize(
    "k,n,expected",
    [
        (0, 10, (0, 0.2775327998628892)),
        (10, 10, (0.7224672001371107, 1)),
        (5, 10, (0.236593090512564, 0.7634069094874361)),
    ],
)
def test_wilson_reference_and_boundary_values(k, n, expected):
    assert wilson_interval(k, n) == pytest.approx(expected, abs=1e-12)


@pytest.mark.parametrize("k,n", [(-1, 10), (11, 10), (0, 0), (1.5, 10), (True, 10)])
def test_wilson_rejects_invalid_observation_units(k, n):
    with pytest.raises(ValueError):
        wilson_interval(k, n)


def test_cluster_sampling_preserves_pairs_and_whole_blocks():
    first, draws = cluster_bootstrap([0, 8], [8, 0], [8, 8], seed=7, replicates=1000)
    second, again = cluster_bootstrap([0, 8], [8, 0], [8, 8], seed=7, replicates=1000)
    assert first == second
    np.testing.assert_array_equal(draws, again)
    assert set(draws[:, 0]) == {0, 0.5, 1}
    np.testing.assert_allclose(draws[:, 0] + draws[:, 1], 1)
    np.testing.assert_allclose(draws[:, 2], 2 * draws[:, 0] - 1)
    assert first["clusters"] == 2 and first["paired_cases"] == 16


def test_cluster_weighted_denominator_and_zero_paired_effect():
    result, draws = cluster_bootstrap([1, 0], [1, 0], [1, 9], seed=3, replicates=1000)
    assert result["statistics"]["black_rate"]["estimate"] == pytest.approx(0.1)
    assert set(draws[:, 0]) == {0, 0.1, 1}
    assert result["statistics"]["black_minus_ruff"] == {
        "estimate": 0,
        "lower": 0,
        "upper": 0,
    }


@pytest.mark.parametrize(
    "b,r,n",
    [
        ([], [], []),
        ([2], [0], [1]),
        ([0], [0], [0]),
        ([np.nan], [0], [1]),
        ([0, 1], [0], [1, 1]),
    ],
)
def test_bootstrap_rejects_invalid_clusters(b, r, n):
    with pytest.raises(ValueError):
        cluster_bootstrap(b, r, n, seed=1)


def test_finite_frame_bounds_keep_census_uncertainty_and_unsampled_files():
    assert finite_population_bounds(0, 0, 7, 7) == (0, 0)
    assert finite_population_bounds(0, 1, 13, 13) == pytest.approx((0, 1 / 13))
    assert finite_population_bounds(0, 2, 20, 28) == pytest.approx((0, 10 / 28))
    assert finite_population_bounds(0, 1, 20, 28) == pytest.approx((0, 9 / 28))
    with pytest.raises(ValueError):
        finite_population_bounds(0, 2, 1, 1)


def test_paired_bounds_do_not_impute_unresolved_as_negative():
    assert paired_bounds([1, None], [0, None]) == (0, 1)
    assert paired_bounds([0, None], [0, 0]) == (0, 0.5)
    with pytest.raises(ValueError):
        paired_bounds([], [])


def control_record():
    record = json.loads(
        (
            ROOT / "datasets/results/phase2-validation/list_inline-black/result.json"
        ).read_text(encoding="utf-8")
    )
    # Phase 2 controls predate the main dataset's explicit case_id field.
    record["case_id"] = "fixed-control"
    return record


def test_integrity_audit_checks_occurrence_coverage_and_not_only_counts():
    record = control_record()
    audit_arithmetic(record)
    wrong = copy.deepcopy(record)
    wrong["newly_hidden_count"] += 1
    with pytest.raises(ValueError, match="warning counts"):
        audit_arithmetic(wrong)
    wrong = copy.deepcopy(record)
    wrong["matched_diagnostic_identities"][0]["original"]["visible"] = True
    with pytest.raises(ValueError, match="visibility flag"):
        audit_arithmetic(wrong)
    wrong = copy.deepcopy(record)
    wrong["counts"]["original_suppressed"] = 99
    with pytest.raises(ValueError, match="suppression count"):
        audit_arithmetic(wrong)


def test_unresolved_analysis_rows_have_missing_not_zero_drift():
    record = control_record()
    record.update(
        classification="Ambiguous", newly_hidden_count=None, newly_exposed_count=None
    )
    frame = normalized_rows({"controlled": [record]})
    assert pd.isna(frame.iloc[0]["drift"])
    summary = summarize_group(frame)
    assert summary["attributable"] == 0
    assert summary["confirmed_fraction_resolved"] is None
    assert summary["finite_observed_corpus_bounds"] == [0, 1]
    assert summary["unresolved"] == 1


def test_pairing_uses_cases_not_diagnostic_lines_and_joint_denominator():
    rows = []
    for case, b, r in (
        ("a", "Newly hidden", "Preserved"),
        ("b", "Ambiguous", "Newly exposed"),
        ("c", "Preserved", "Newly hidden"),
    ):
        for formatter, label in (("black", b), ("ruff", r)):
            record = control_record()
            record.update(
                case_id=case,
                trial_id=f"{case}-{formatter}",
                formatter=formatter,
                classification=label,
            )
            if label == "Ambiguous":
                record.update(newly_hidden_count=None, newly_exposed_count=None)
            rows.append(record)
    frame = normalized_rows({"controlled": rows})
    pairs = make_pairs(frame)
    summary = pair_summary(pairs)
    assert summary["common_resolved"] == 2
    assert summary["one_sided_unresolved"] == 1
    assert summary["matrix_rows_black_columns_ruff_0_1"] == [[0, 1], [1, 0]]
    assert summary["contrasts_common_resolved"]["drift"]["black_minus_ruff"] == 0
    frame.loc[frame["formatter"].eq("ruff"), "input_sha256"] = "tampered"
    with pytest.raises(ValueError, match="checksums"):
        make_pairs(frame)
