"""Descriptive results and explicitly conditional cluster-model uncertainty."""

from collections import Counter
import hashlib
from importlib.metadata import version
import json
from pathlib import Path

import pandas as pd

from .analysis_audit import DRIFT, RESOLVED, load_and_audit, require
from .experiment import OUTCOMES
from .pipeline import ROOT, environment, save_json
from .statistics import (
    cluster_bootstrap,
    finite_population_bounds,
    paired_bounds,
    wilson_interval,
)

ANALYSIS_PINS = {"numpy": "2.2.6", "pandas": "2.2.3", "matplotlib": "3.10.3"}


def normalized_rows(datasets):
    rows = []
    for dataset, records in datasets.items():
        for r in records:
            resolved = r["classification"] in RESOLVED
            rows.append(
                {
                    "dataset": dataset,
                    "trial_id": r["trial_id"],
                    "case_id": r["case_id"],
                    "formatter": r["formatter"],
                    "repository": r.get("repository", "controlled_suite"),
                    "original_path": r.get("original_path"),
                    "input_family": r.get("input_family"),
                    "syntax_category": r.get("syntax_category"),
                    "directive_placement": r.get("directive_placement"),
                    "suppression_type": r.get("suppression_type"),
                    "classification": r["classification"],
                    "validation_status": r["validation_status"],
                    "resolved": resolved,
                    "drift": int(r["classification"] in DRIFT) if resolved else None,
                    "hiding": (
                        int(r["classification"] in {"Newly hidden", "Mixed"})
                        if resolved
                        else None
                    ),
                    "exposing": (
                        int(r["classification"] in {"Newly exposed", "Mixed"})
                        if resolved
                        else None
                    ),
                    "hidden_diagnostics": r.get("newly_hidden_count"),
                    "exposed_diagnostics": r.get("newly_exposed_count"),
                    "text_changed": r.get("formatting_changed"),
                    "ast_equivalent": r.get("ast_equivalent"),
                    "underlying_original": (
                        len(r["passes"]["B_original_underlying"])
                        if r.get("passes", {}).get("B_original_underlying") is not None
                        else None
                    ),
                    "suppressed_original": (
                        len(r["suppressed_within_source"]["original"])
                        if r.get("suppressed_within_source") is not None
                        else None
                    ),
                    "input_sha256": r["input_sha256"],
                }
            )
    frame = pd.DataFrame(rows)
    for field in (
        "drift",
        "hiding",
        "exposing",
        "hidden_diagnostics",
        "exposed_diagnostics",
        "underlying_original",
        "suppressed_original",
    ):
        frame[field] = pd.array(frame[field], dtype="Int64")
    return frame


def summarize_group(frame):
    scheduled, resolved = len(frame), int(frame["resolved"].sum())
    require(scheduled > 0, "empty summary group")
    confirmed = int((frame["classification"].isin(DRIFT)).sum())
    unknown = scheduled - resolved
    counts = {
        label: int((frame["classification"] == label).sum()) for label in OUTCOMES
    }
    changed = frame["text_changed"].eq(True)
    return {
        "scheduled": scheduled,
        "measurement_complete": int(
            frame["validation_status"].eq("measurement_complete").sum()
        ),
        "attributable": resolved,
        "unresolved": unknown,
        "outcomes": counts,
        "outcome_proportions_scheduled": {
            label: count / scheduled for label, count in counts.items()
        },
        "confirmed_drift": confirmed,
        "confirmed_fraction_scheduled": confirmed / scheduled,
        "confirmed_fraction_resolved": confirmed / resolved if resolved else None,
        "finite_observed_corpus_bounds": list(
            finite_population_bounds(confirmed, unknown, scheduled, scheduled)
        ),
        "newly_hidden_diagnostics": int(frame["hidden_diagnostics"].dropna().sum()),
        "newly_exposed_diagnostics": int(frame["exposed_diagnostics"].dropna().sum()),
        "text_changed": int(changed.sum()),
        "text_unchanged": int(frame["text_changed"].eq(False).sum()),
        "text_changed_preserved": int(
            (changed & frame["classification"].eq("Preserved")).sum()
        ),
        "changed_and_resolved": int((changed & frame["resolved"]).sum()),
        "changed_resolved_original_suppression": int(
            (
                changed
                & frame["resolved"]
                & frame["suppressed_original"].gt(0).fillna(False)
            ).sum()
        ),
        "original_zero_underlying": int(frame["underlying_original"].eq(0).sum()),
        "original_with_suppression": int(frame["suppressed_original"].gt(0).sum()),
    }


def make_pairs(frame):
    columns = [
        "case_id",
        "repository",
        "input_family",
        "syntax_category",
        "input_sha256",
        "classification",
        "resolved",
        "drift",
        "hiding",
        "exposing",
    ]
    black = frame[frame["formatter"].eq("black")][columns]
    ruff = frame[frame["formatter"].eq("ruff")][columns]
    paired = black.merge(
        ruff, on="case_id", suffixes=("_black", "_ruff"), validate="one_to_one"
    )
    require(len(paired) * 2 == len(frame), "unpaired analysis observations")
    require(
        paired["input_sha256_black"].equals(paired["input_sha256_ruff"]),
        "paired input checksums differ",
    )
    paired["both_resolved"] = paired["resolved_black"] & paired["resolved_ruff"]
    return paired.sort_values("case_id").reset_index(drop=True)


def pair_summary(pairs):
    common = pairs[pairs["both_resolved"]]
    matrix = [
        [
            int(((common["drift_black"] == b) & (common["drift_ruff"] == r)).sum())
            for r in (0, 1)
        ]
        for b in (0, 1)
    ]
    contrast = {}
    for event in ("drift", "hiding", "exposing"):
        contrast[event] = {
            "black": int(common[f"{event}_black"].sum()),
            "ruff": int(common[f"{event}_ruff"].sum()),
            "denominator": len(common),
            "black_minus_ruff": (
                float(
                    (common[f"{event}_black"].sum() - common[f"{event}_ruff"].sum())
                    / len(common)
                )
                if len(common)
                else None
            ),
        }
    b = [None if pd.isna(value) else int(value) for value in pairs["drift_black"]]
    r = [None if pd.isna(value) else int(value) for value in pairs["drift_ruff"]]
    return {
        "paired_inputs": len(pairs),
        "common_resolved": len(common),
        "one_sided_unresolved": int(
            (pairs["resolved_black"] != pairs["resolved_ruff"]).sum()
        ),
        "both_unresolved": int(
            (~pairs["resolved_black"] & ~pairs["resolved_ruff"]).sum()
        ),
        "matrix_rows_black_columns_ruff_0_1": matrix,
        "contrasts_common_resolved": contrast,
        "finite_all_scheduled_contrast_bounds": list(paired_bounds(b, r)),
    }


def group_table(frame, dimensions):
    rows = []
    for keys, subset in frame.groupby(dimensions, sort=True, dropna=False):
        keys = keys if isinstance(keys, tuple) else (keys,)
        summary = summarize_group(subset)
        row = dict(zip(dimensions, keys))
        for key, value in summary.items():
            if key == "outcomes":
                row.update(
                    {
                        f"outcome_{label.lower().replace(' ', '_')}": count
                        for label, count in value.items()
                    }
                )
            elif not isinstance(value, (dict, list)):
                row[key] = value
        rows.append(row)
    return pd.DataFrame(rows)


def write_frame(frame, path):
    frame.to_csv(
        path, index=False, encoding="utf-8", lineterminator="\n", float_format="%.17g"
    )


def run_analysis(output: Path, figures: Path, root=ROOT):
    output, figures = output.resolve(), figures.resolve()
    require(output != figures, "data and figure directories must differ")
    require(
        not output.exists() and not figures.exists(),
        "analysis/figure output directory already exists",
    )
    versions = {name: version(name) for name in ANALYSIS_PINS}
    require(versions == ANALYSIS_PINS, "analysis dependencies differ from pins")
    datasets, native, audit, hashes = load_and_audit(root)
    frame = normalized_rows(datasets)
    controlled = frame[frame["dataset"].eq("controlled")]
    natural = frame[frame["dataset"].eq("natural")]
    output.mkdir(parents=True)
    figures.mkdir(parents=True)
    write_frame(frame, output / "observations.csv")
    metrics = {
        "schema_version": 1,
        "interpretation": "fixed-corpus descriptive results and exploratory conditional models",
        "controlled": {
            formatter: summarize_group(
                controlled[controlled["formatter"].eq(formatter)]
            )
            for formatter in ("black", "ruff")
        },
        "natural": {},
        "natural_pairs": {},
        "natural_finite_frame_bounds": [],
        "native": {},
        "detector_accuracy_evaluated": False,
    }
    pairs = make_pairs(controlled)
    write_frame(pairs, output / "controlled_pairs.csv")
    metrics["controlled_pairs"] = pair_summary(pairs)
    common = pairs[pairs["both_resolved"]]
    metrics["cluster_model_intervals"] = {}
    for grouping, column, seed in (
        ("family", "input_family_black", 20261103),
        ("category", "syntax_category_black", 20261104),
    ):
        clusters = common.groupby(column, sort=True).agg(
            black=("drift_black", "sum"),
            ruff=("drift_ruff", "sum"),
            n=("case_id", "size"),
        )
        result, draws = cluster_bootstrap(
            clusters["black"], clusters["ruff"], clusters["n"], seed=seed
        )
        metrics["cluster_model_intervals"][grouping] = result
        write_frame(clusters.reset_index(), output / f"{grouping}_cluster_counts.csv")
        write_frame(
            pd.DataFrame(
                draws, columns=["black_rate", "ruff_rate", "black_minus_ruff"]
            ),
            output / f"{grouping}_bootstrap_draws.csv",
        )
    metrics["family_wilson_model_sensitivity"] = []
    for formatter in ("black", "ruff"):
        families = (
            controlled[controlled["formatter"].eq(formatter)]
            .groupby("input_family")
            .agg(
                n=("case_id", "size"),
                resolved=("resolved", "sum"),
                confirmed=("drift", "sum"),
            )
        )
        complete = families[families["n"].eq(families["resolved"])]
        k, n = int(complete["confirmed"].gt(0).sum()), len(complete)
        low, high = wilson_interval(k, n)
        metrics["family_wilson_model_sensitivity"].append(
            {
                "formatter": formatter,
                "families_with_any_confirmed_drift": k,
                "complete_families": n,
                "excluded_incomplete_families": len(families) - n,
                "fraction": k / n,
                "lower": low,
                "upper": high,
                "level": 0.95,
                "unit": "wholly resolved template family",
                "interpretation": "hypothetical independent/exchangeable-family Bernoulli model only",
            }
        )
    manifest = json.loads(
        (root / "datasets/real_world/phase4/manifest.json").read_text(encoding="utf-8")
    )
    populations = {
        repo["repository"]: repo["eligible_noqa_files"]
        for repo in manifest["repositories"]
    }
    natural_pair_rows = []
    for repo, subset in natural.groupby("repository", sort=True):
        metrics["natural"][repo] = {
            formatter: summarize_group(subset[subset["formatter"].eq(formatter)])
            for formatter in ("black", "ruff")
        }
        repo_pairs = make_pairs(subset)
        metrics["natural_pairs"][repo] = pair_summary(repo_pairs)
        natural_pair_rows.append(repo_pairs)
        for formatter in ("black", "ruff"):
            observed = metrics["natural"][repo][formatter]
            low, high = finite_population_bounds(
                observed["confirmed_drift"],
                observed["unresolved"],
                observed["scheduled"],
                populations[repo],
            )
            metrics["natural_finite_frame_bounds"].append(
                {
                    "repository": repo,
                    "formatter": formatter,
                    "population_eligible_files": populations[repo],
                    "sampled_files": observed["scheduled"],
                    "confirmed": observed["confirmed_drift"],
                    "sampled_unresolved": observed["unresolved"],
                    "unsampled": populations[repo] - observed["scheduled"],
                    "lower": low,
                    "upper": high,
                    "interpretation": "finite eligible-archive bounds, not confidence intervals or ecosystem rates",
                }
            )
        secondary = [r for r in native if r["repository"] == repo]
        primary_by_id = {
            r["trial_id"]: r for r in datasets["natural"] if r["repository"] == repo
        }
        completed = [
            r for r in secondary if r["validation_status"] == "measurement_complete"
        ]
        metrics["native"][repo] = {
            "status_records": len(secondary),
            "completed": len(completed),
            "statuses": dict(Counter(r["validation_status"] for r in secondary)),
            "classifications": dict(Counter(r["classification"] for r in completed)),
            "same_primary_classification": sum(
                r["classification"] == primary_by_id[r["trial_id"]]["classification"]
                for r in completed
            ),
            "zero_selected_underlying": sum(
                not r["passes"]["B_original_underlying"] for r in completed
            ),
        }
    write_frame(
        pd.concat(natural_pair_rows, ignore_index=True), output / "natural_pairs.csv"
    )
    tables = {
        "primary_summary": group_table(frame, ["dataset", "repository", "formatter"]),
        "family_wilson_model_sensitivity": pd.DataFrame(
            metrics["family_wilson_model_sensitivity"]
        ),
        "natural_finite_frame_bounds": pd.DataFrame(
            metrics["natural_finite_frame_bounds"]
        ),
        "controlled_by_category": group_table(
            controlled, ["syntax_category", "formatter"]
        ),
        "controlled_by_family": group_table(controlled, ["input_family", "formatter"]),
        "controlled_by_treatment": group_table(
            controlled, ["directive_placement", "formatter"]
        ),
        "controlled_by_suppression_type": group_table(
            controlled, ["suppression_type", "formatter"]
        ),
        "category_treatment": group_table(
            controlled, ["syntax_category", "directive_placement", "formatter"]
        ),
        "natural_by_repository": group_table(natural, ["repository", "formatter"]),
    }
    for name, table in tables.items():
        write_frame(table, output / f"{name}.csv")
    save_json(output / "metrics.json", metrics)
    save_json(output / "integrity.json", audit)
    from .figures import make_figures

    captions = make_figures(frame, pairs, metrics, tables, figures, root)
    save_json(output / "figure_captions.json", captions)
    provenance = {
        "analysis_versions": versions,
        "environment": environment(),
        "input_sha256": hashes,
        "analysis_specification_sha256": hashlib.sha256(
            (root / "docs/phase5_analysis_spec.md").read_bytes()
        ).hexdigest(),
        "artifacts": {
            str(path.relative_to(output)): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in sorted(output.iterdir())
            if path.is_file()
        },
        "figures": {
            path.name: hashlib.sha256(path.read_bytes()).hexdigest()
            for path in sorted(figures.iterdir())
            if path.suffix in {".png", ".svg"}
        },
    }
    save_json(output / "provenance.json", provenance)
    print(
        json.dumps(
            {
                "controlled_records": len(controlled),
                "natural_records": len(natural),
                "paired_controlled": metrics["controlled_pairs"],
                "cluster_model_intervals": metrics["cluster_model_intervals"],
                "output": str(output),
                "figures": str(figures),
            },
            indent=2,
        )
    )
    return metrics
