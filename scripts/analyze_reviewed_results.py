"""Calculate a separate sensitivity analysis using the saved ambiguity review."""

import argparse
import copy
import hashlib
import importlib.util
from importlib.metadata import version
import json
from pathlib import Path
import subprocess

import pandas as pd

from suppression_study.analysis import (
    ANALYSIS_PINS,
    group_table,
    make_pairs,
    normalized_rows,
    pair_summary,
    summarize_group,
    write_frame,
)
from suppression_study.analysis_audit import load_and_audit
from suppression_study.pipeline import ROOT
from suppression_study.statistics import cluster_bootstrap, wilson_interval


def save(path, data):
    path.write_bytes((json.dumps(data, indent=2) + "\n").encode())


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def reviewed_copy(original, review):
    """Use only explicitly supported proposals; keep original rows unchanged."""
    proposals = {(r["case_id"], r["formatter"]): r for r in review}
    expected = {
        (r["case_id"], r["formatter"])
        for r in original
        if r["classification"] == "Ambiguous"
    }
    if len(proposals) != len(review) or set(proposals) != expected:
        raise ValueError("Review coverage differs from the original ambiguity cohort")
    result = copy.deepcopy(original)
    for row in result:
        identity = row["case_id"], row["formatter"]
        row["original_classification"] = row["classification"]
        row["supplementary_proposal_used"] = identity in proposals
        if identity not in proposals:
            continue
        proposal = proposals[identity]
        judgment = proposal["review"]
        if (
            proposal["original_classification"] != "Ambiguous"
            or proposal["before_sha256"] != row["input_sha256"]
            or proposal["after_sha256"] != row["output_sha256"]
            or judgment["proposed_resolution"] != "Preserved"
            or judgment["hidden"] != 0
            or judgment["exposed"] != 0
            or judgment["uncertainty"] is not None
            or not judgment["warnings"]
            or any(
                w["before"]["visible"] != w["after"]["visible"]
                for w in judgment["warnings"]
            )
        ):
            raise ValueError("A proposal lacks the required preservation evidence")
        row["classification"] = "Preserved"
        row["newly_hidden_count"] = row["newly_exposed_count"] = 0
    return result


def verify_review_records(review, audit):
    """Check stored replay/intervention records without running new experiments."""

    def portable(value):
        if isinstance(value, dict):
            return {k: portable(v) for k, v in value.items() if k != "filename"}
        if isinstance(value, list):
            return [portable(v) for v in value]
        return value

    passes_checked = interventions_checked = identical = spacing = 0
    for row in review:
        original = ROOT / row["original_directory"]
        exported = audit / "exports" / row["case_id"] / row["formatter"]
        rechecks = exported / "rechecks"
        before = (original / "before.py").read_bytes()
        after = (original / "after.py").read_bytes()
        if row["case_id"].startswith("fstring_boundary--"):
            if before != after:
                raise ValueError("The f-string preservation argument no longer holds")
            identical += 1
        elif row["case_id"].startswith("exception_binding_boundary--"):
            if before.replace(b"leftover=1", b"leftover = 1") != after:
                raise ValueError("The exception-source difference is not just spacing")
            spacing += 1
        else:
            raise ValueError("Unexpected review family")
        for label in (
            "A_original_visible",
            "B_original_underlying",
            "C_formatted_visible",
            "D_formatted_underlying",
        ):
            saved = json.loads((original / (label + ".stdout.txt")).read_bytes())
            replay = json.loads((rechecks / (label + ".stdout.txt")).read_bytes())
            command = json.loads((rechecks / (label + ".command.json")).read_bytes())
            if portable(saved) != portable(replay) or command["returncode"] != bool(
                replay
            ):
                raise ValueError("A saved replay does not match original diagnostics")
            if ("--ignore-noqa" in command["command"]) != label.startswith(
                ("B_", "D_")
            ):
                raise ValueError("Replay directive handling differs")
            passes_checked += 1
        for side, label in (
            ("before", "B_original_underlying"),
            ("after", "D_formatted_underlying"),
        ):
            source = (rechecks / (side + ".noqa-neutralized.py")).read_bytes().decode()
            if source != audit_neutralize(
                (original / (side + ".py")).read_bytes().decode()
            ):
                raise ValueError("Saved intervention source differs")
            observed = json.loads(
                (rechecks / (side + "_neutralized_visible.stdout.txt")).read_bytes()
            )
            reference = json.loads((original / (label + ".stdout.txt")).read_bytes())
            if portable(observed) != portable(reference):
                raise ValueError(
                    "Saved intervention does not recover underlying warnings"
                )
            interventions_checked += 1
    return {
        "saved_lint_replays_verified": passes_checked,
        "saved_comment_interventions_verified": interventions_checked,
        "byte_identical_fstring_comparisons": identical,
        "spacing_only_exception_comparisons": spacing,
        "new_formatter_or_linter_invocations": 0,
    }


AUDIT_SPEC = importlib.util.spec_from_file_location(
    "saved_ambiguity_audit", ROOT / "scripts/audit_ambiguities.py"
)
AUDIT_MODULE = importlib.util.module_from_spec(AUDIT_SPEC)
AUDIT_SPEC.loader.exec_module(AUDIT_MODULE)
audit_neutralize = AUDIT_MODULE.neutralize


def run(output):
    if output.exists() or not any(
        output.is_relative_to(ROOT / name) for name in ("local", "reports")
    ):
        raise ValueError("Choose a new output directory under local or reports")
    if {name: version(name) for name in ANALYSIS_PINS} != ANALYSIS_PINS:
        raise ValueError("Analysis dependencies differ from the retained pins")
    audit = ROOT / "reports/ambiguous-audit"
    AUDIT_MODULE.verify(audit)
    datasets, native, primary_checks, hashes = load_and_audit(ROOT)
    print("Original primary evidence audit passed", flush=True)
    original = datasets["controlled"]
    untouched = copy.deepcopy(original)
    review = json.loads((audit / "review_manifest.json").read_bytes())
    review_checks = verify_review_records(review, audit)
    revised = reviewed_copy(original, review)
    if original != untouched:
        raise ValueError("Original in-memory classifications were changed")
    baseline_metrics = json.loads(
        (ROOT / "reports/phase5/analysis/metrics.json").read_bytes()
    )
    original_frame = normalized_rows({"controlled": original})
    frame = normalized_rows({"controlled": revised})
    summaries = {}
    for formatter in ("black", "ruff"):
        first = summarize_group(
            original_frame[original_frame["formatter"].eq(formatter)]
        )
        if first != baseline_metrics["controlled"][formatter]:
            raise ValueError("Recalculated original metrics differ from Phase 5")
        summaries[formatter] = summarize_group(frame[frame["formatter"].eq(formatter)])
    pairs = make_pairs(frame)
    original_pairs = pair_summary(make_pairs(original_frame))
    if original_pairs != baseline_metrics["controlled_pairs"]:
        raise ValueError("Original paired summary differs from Phase 5")
    natural = normalized_rows({"natural": datasets["natural"]})
    for (repo, formatter), group in natural.groupby(["repository", "formatter"]):
        if summarize_group(group) != baseline_metrics["natural"][repo][formatter]:
            raise ValueError("Natural-source summary differs from Phase 5")
    output.mkdir(parents=True)
    overlay = frame.copy()
    originals = {(r["case_id"], r["formatter"]): r["classification"] for r in original}
    overlay.insert(
        0,
        "original_classification",
        [originals[(r.case_id, r.formatter)] for r in overlay.itertuples()],
    )
    overlay.insert(
        1, "review_applied", overlay["original_classification"].eq("Ambiguous")
    )
    overlay = overlay.rename(columns={"classification": "supplementary_classification"})
    write_frame(overlay, output / "review_overlay.csv")
    write_frame(pairs, output / "reviewed_pairs.csv")
    metrics = {
        "status": "supplementary sensitivity conditional on AI-assisted review proposals; not independent human ground truth",
        "original_reference": "reports/phase5/analysis/metrics.json",
        "original_controlled": baseline_metrics["controlled"],
        "original_pairs": original_pairs,
        "reviewed_controlled": summaries,
        "reviewed_pairs": pair_summary(pairs),
        "review_proposals_used": len(review),
        "natural_primary_results_changed": False,
        "original_intervals_reused_for_reviewed_data": False,
        "reviewed_cluster_model_intervals": {},
        "reviewed_family_wilson_sensitivity": [],
    }
    for grouping, column, seed in (
        ("family", "input_family_black", 20261103),
        ("category", "syntax_category_black", 20261104),
    ):
        clusters = pairs.groupby(column, sort=True).agg(
            black=("drift_black", "sum"),
            ruff=("drift_ruff", "sum"),
            n=("case_id", "size"),
        )
        interval, draws = cluster_bootstrap(
            clusters["black"], clusters["ruff"], clusters["n"], seed=seed
        )
        metrics["reviewed_cluster_model_intervals"][grouping] = interval
        write_frame(clusters.reset_index(), output / f"reviewed_{grouping}_counts.csv")
        write_frame(
            pd.DataFrame(
                draws, columns=["black_rate", "ruff_rate", "black_minus_ruff"]
            ),
            output / f"reviewed_{grouping}_draws.csv",
        )
    for formatter in ("black", "ruff"):
        families = (
            frame[frame["formatter"].eq(formatter)]
            .groupby("input_family")
            .agg(
                n=("case_id", "size"),
                resolved=("resolved", "sum"),
                confirmed=("drift", "sum"),
            )
        )
        if not families["n"].eq(families["resolved"]).all():
            raise ValueError("A family remains unresolved in the reviewed sensitivity")
        k, n = int(families["confirmed"].gt(0).sum()), len(families)
        low, high = wilson_interval(k, n)
        metrics["reviewed_family_wilson_sensitivity"].append(
            {
                "formatter": formatter,
                "families_with_drift": k,
                "reviewed_families": n,
                "fraction": k / n,
                "lower": low,
                "upper": high,
                "level": 0.95,
                "interpretation": "hypothetical independent exchangeable-family model, conditional on the review",
            }
        )
    for group in ("input_family", "syntax_category", "directive_placement"):
        write_frame(
            group_table(frame, [group, "formatter"]), output / f"reviewed_{group}.csv"
        )
    save(output / "metrics.json", metrics)
    save(
        output / "evidence_checks.json",
        {
            "primary": primary_checks,
            "supplementary": review_checks,
            "original_metrics_reproduced": True,
            "original_in_memory_rows_unchanged": True,
            "natural_summaries_reproduced": True,
        },
    )
    for name in (
        "reports/phase5/analysis/metrics.json",
        "reports/ambiguous-audit/review_manifest.json",
        "reports/ambiguous-audit/integrity.json",
        "reports/ambiguous-audit/artifact_hashes.json",
        "scripts/audit_ambiguities.py",
        "scripts/analyze_reviewed_results.py",
        "src/suppression_study/statistics.py",
    ):
        hashes[name] = digest(ROOT / name)
    for name, expected in hashes.items():
        if digest(ROOT / name) != expected:
            raise ValueError("An analysis input changed")
    save(
        output / "provenance.json",
        {
            "input_sha256": hashes,
            "versions": {name: version(name) for name in ANALYSIS_PINS},
            "source_commit": subprocess.check_output(
                ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
            ).strip(),
            "new_primary_observations": 0,
            "figures_created": 0,
            "interpretation": metrics["status"],
        },
    )
    save(
        output / "artifact_hashes.json",
        {p.name: digest(p) for p in sorted(output.iterdir()) if p.is_file()},
    )
    print(
        json.dumps(
            {
                "reviewed_pairs": metrics["reviewed_pairs"],
                "reviewed_intervals": metrics["reviewed_cluster_model_intervals"],
                "family_incidence": metrics["reviewed_family_wilson_sensitivity"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output", type=Path, default=ROOT / "reports/publication-phase-a/analysis"
    )
    args = parser.parse_args()
    run(args.output.resolve())
