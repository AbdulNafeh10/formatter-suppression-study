"""Standalone research figures from executed observations only."""

import json

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch, Rectangle
from matplotlib.ticker import PercentFormatter
import numpy as np

from .generator import MODES

COLORS = {
    "Preserved": "#4477AA",
    "Newly hidden": "#CC6677",
    "Newly exposed": "#DDCC77",
    "Ambiguous": "#999999",
    "AST changed": "#AA4499",
}
FORMATTER = {"black": "#332288", "ruff": "#117733"}
REPOS = ("psf/requests", "pallets/flask", "pytest-dev/pytest")
REPO_NAMES = {
    "psf/requests": "Requests",
    "pallets/flask": "Flask",
    "pytest-dev/pytest": "pytest",
}


def style():
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 9,
            "axes.titlesize": 11,
            "axes.labelsize": 9,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "svg.fonttype": "none",
            "svg.hashsalt": "suppression-study-phase5-v1",
            "savefig.facecolor": "white",
            "figure.facecolor": "white",
        }
    )


def export(fig, directory, name):
    fig.savefig(
        directory / f"{name}.png",
        dpi=300,
        metadata={"Software": "formatter-suppression-study Phase 5"},
    )
    fig.savefig(
        directory / f"{name}.svg",
        metadata={"Date": None, "Creator": "formatter-suppression-study Phase 5"},
    )
    plt.close(fig)


def stacked_outcomes(ax, rows):
    for y, (label, summary) in enumerate(rows):
        left = 0
        for outcome, color in COLORS.items():
            count = summary["outcomes"].get(outcome, 0)
            width = 100 * count / summary["scheduled"]
            if count:
                ax.barh(
                    y,
                    width,
                    left=left,
                    color=color,
                    edgecolor="white",
                    linewidth=0.7,
                    height=0.65,
                    hatch="///" if outcome == "AST changed" else None,
                )
                ax.text(
                    left + width / 2,
                    y,
                    str(count),
                    ha="center",
                    va="center",
                    fontsize=9,
                    color=(
                        "black"
                        if outcome in {"Newly exposed", "Ambiguous"}
                        else "white"
                    ),
                )
            left += width
    ax.set_yticks(range(len(rows)), [label for label, _ in rows])
    ax.set_ylim(len(rows) - 0.45, -0.55)
    ax.set_xlim(0, 100)
    ax.xaxis.set_major_formatter(PercentFormatter(100, decimals=0))
    ax.set_xticks([0, 25, 50, 75, 100])
    ax.set_axisbelow(True)
    ax.grid(axis="x", alpha=0.16)
    ax.tick_params(axis="y", length=0, pad=9)


def figure_outcomes(metrics, directory):
    fig = plt.figure(figsize=(11.4, 7.2))
    grid = fig.add_gridspec(
        2,
        1,
        height_ratios=[1, 2.4],
        left=0.23,
        right=0.98,
        top=0.87,
        bottom=0.19,
        hspace=0.40,
    )
    a, b = fig.add_subplot(grid[0]), fig.add_subplot(grid[1])
    stacked_outcomes(
        a,
        [
            (f"{formatter.title()} · n=200", metrics["controlled"][formatter])
            for formatter in ("black", "ruff")
        ],
    )
    rows = [
        (
            f"{REPO_NAMES[repo]} · {formatter.title()} · n={metrics['natural'][repo][formatter]['scheduled']}",
            metrics["natural"][repo][formatter],
        )
        for repo in REPOS
        for formatter in ("black", "ruff")
    ]
    stacked_outcomes(b, rows)
    a.set_title("A  Controlled stress suite", loc="left", pad=10)
    b.set_title(
        "B  Natural-source sample · repositories kept separate", loc="left", pad=10
    )
    b.set_xlabel("Share of scheduled comparisons · segment labels are counts")
    fig.suptitle(
        "Suppression outcomes under fixed tool settings",
        x=0.23,
        y=0.97,
        ha="left",
        fontsize=14,
    )
    fig.text(
        0.23,
        0.918,
        "Primary observations only; repeats and native-config sensitivity excluded.",
        fontsize=9,
    )
    handles = [
        Patch(
            facecolor=color,
            label="Strict AST exclusion" if label == "AST changed" else label,
            hatch="///" if label == "AST changed" else None,
        )
        for label, color in COLORS.items()
    ]
    fig.legend(
        handles=handles,
        loc="lower center",
        bbox_to_anchor=(0.59, 0.035),
        ncol=3,
        frameon=False,
        fontsize=9,
    )
    export(fig, directory, "figure1_outcomes")


def figure_pairs(pairs, metrics, directory, root):
    spec = json.loads(
        (root / "datasets/controlled/phase3/specification.json").read_text(
            encoding="utf-8"
        )
    )
    family_order = [template["name"] for template in spec["templates"]]
    common = pairs[pairs["both_resolved"]]
    family_rates = common.groupby("input_family_black")[
        ["drift_black", "drift_ruff"]
    ].mean()
    resolved_order = [name for name in family_order if name in family_rates.index]
    fig = plt.figure(figsize=(12.8, 9.1))
    grid = fig.add_gridspec(
        2,
        2,
        height_ratios=[3.3, 1],
        width_ratios=[1.4, 1],
        left=0.22,
        right=0.97,
        top=0.91,
        bottom=0.15,
        hspace=0.53,
        wspace=0.48,
    )
    slopes, matrix_ax, interval_ax = (
        fig.add_subplot(grid[0, 0]),
        fig.add_subplot(grid[0, 1]),
        fig.add_subplot(grid[1, :]),
    )
    for y, family in enumerate(resolved_order):
        black, ruff = [
            float(family_rates.loc[family, column]) * 100
            for column in ("drift_black", "drift_ruff")
        ]
        slopes.plot([black, ruff], [y, y], color="#bbbbbb", linewidth=1.3, zorder=1)
        slopes.scatter(black, y, color=FORMATTER["black"], s=23, zorder=3, marker="o")
        slopes.scatter(ruff, y, color=FORMATTER["ruff"], s=27, zorder=4, marker="x")
    slopes.set_yticks(
        range(len(resolved_order)),
        [name.replace("_", " ") for name in resolved_order],
        fontsize=7.5,
    )
    slopes.set_ylim(len(resolved_order) - 0.5, -0.8)
    slopes.set_xlim(-3, 103)
    slopes.xaxis.set_major_formatter(PercentFormatter(100, decimals=0))
    slopes.set_xlabel("Confirmed drift across eight treatments")
    slopes.set_title("A  Paired template profiles", loc="left")
    slopes.grid(axis="x", alpha=0.16)
    slopes.tick_params(axis="y", length=0)
    slopes.scatter([], [], color=FORMATTER["black"], s=25, label="Black", marker="o")
    slopes.scatter([], [], color=FORMATTER["ruff"], s=25, label="Ruff", marker="x")
    slopes.legend(loc="upper right", frameon=False, fontsize=8)
    matrix = np.asarray(
        metrics["controlled_pairs"]["matrix_rows_black_columns_ruff_0_1"]
    )
    matrix_ax.imshow(matrix, cmap="Blues", vmin=0, vmax=max(1, matrix.max()))
    for (i, j), count in np.ndenumerate(matrix):
        matrix_ax.text(
            j,
            i,
            str(count),
            ha="center",
            va="center",
            fontsize=23,
            color="white" if count > matrix.max() * 0.55 else "#222222",
        )
    matrix_ax.set_xticks([0, 1], ["No drift", "Drift"])
    matrix_ax.set_yticks([0, 1], ["No drift", "Drift"])
    matrix_ax.set_xlabel("Ruff outcome")
    matrix_ax.set_ylabel("Black outcome")
    matrix_ax.set_title("B  Common-resolved input pairs", loc="left", pad=14)
    unresolved = (
        metrics["controlled_pairs"]["paired_inputs"]
        - metrics["controlled_pairs"]["common_resolved"]
    )
    matrix_ax.text(
        0.5,
        -0.24,
        f"n={int(matrix.sum())} pairs; {unresolved} unresolved pairs omitted",
        transform=matrix_ax.transAxes,
        ha="center",
        fontsize=8,
    )
    intervals = metrics["cluster_model_intervals"]
    limits = []
    for y, (grouping, color) in enumerate(
        (("family", "#332288"), ("category", "#882255"))
    ):
        data = intervals[grouping]
        value = data["statistics"]["black_minus_ruff"]
        lo, hi, point = [value[field] * 100 for field in ("lower", "upper", "estimate")]
        interval_ax.hlines(y, lo, hi, color=color, linewidth=2)
        interval_ax.vlines([lo, hi], y - 0.08, y + 0.08, color=color)
        interval_ax.scatter(point, y, color=color, s=25, zorder=3)
        interval_ax.text(
            hi + 1.2, y, f"{point:.1f} pp [{lo:.1f}, {hi:.1f}]", va="center", fontsize=8
        )
        limits += [lo, hi]
    interval_ax.axvline(0, color="#888888", linestyle="--", linewidth=0.8)
    interval_ax.set_yticks(
        [0, 1],
        [
            f"{intervals['family']['clusters']} template clusters",
            f"{intervals['category']['clusters']} category clusters",
        ],
    )
    interval_ax.set_ylim(1.6, -0.6)
    interval_ax.set_xlim(min(0, min(limits)) - 2, max(limits) + 17)
    interval_ax.set_xlabel(
        "Black − Ruff confirmed-drift difference (percentage points)"
    )
    interval_ax.set_title(
        "C  Exploratory 95% whole-cluster model intervals · common-resolved inputs",
        loc="left",
        pad=13,
        fontsize=10,
    )
    interval_ax.grid(axis="x", alpha=0.13)
    fig.suptitle(
        "Paired formatter comparison in the controlled suite",
        x=0.22,
        y=0.976,
        ha="left",
        fontsize=14,
    )
    fig.text(
        0.22,
        0.939,
        "Two boundary templates are unassessed; template order follows the saved specification.",
        fontsize=8.5,
    )
    fig.text(
        0.06,
        0.038,
        "Intervals assume independent, exchangeable clusters. Templates were hand-selected: nominal population coverage is unverified.\n"
        "The two cluster groupings are sensitivity analyses; neither establishes ecosystem rates or formatter superiority.",
        fontsize=8,
    )
    export(fig, directory, "figure2_paired_comparison")


def figure_patterns(tables, directory, root):
    spec = json.loads(
        (root / "datasets/controlled/phase3/specification.json").read_text(
            encoding="utf-8"
        )
    )
    categories = list(
        dict.fromkeys(template["category"] for template in spec["templates"])
    )
    data = tables["category_treatment"]
    labels = [
        "None",
        "Own\nline",
        "First\nspecific",
        "First\nblanket",
        "First\nmulti",
        "Last\nspecific",
        "Last\nblanket",
        "File\nspecific",
    ]
    fig, axes = plt.subplots(1, 2, figsize=(14, 8.4), sharey=True)
    fig.subplots_adjust(left=0.19, right=0.98, top=0.85, bottom=0.25, wspace=0.12)
    cmap = plt.get_cmap("Blues").copy()
    cmap.set_bad("#e7e7e7")
    for ax, formatter in zip(axes, ("black", "ruff")):
        values = np.full((len(categories), len(MODES)), np.nan)
        texts = {}
        for i, category in enumerate(categories):
            for j, mode in enumerate(MODES):
                row = data[
                    (data["syntax_category"] == category)
                    & (data["directive_placement"] == mode)
                    & (data["formatter"] == formatter)
                ].iloc[0]
                if row["attributable"]:
                    values[i, j] = row["confirmed_drift"] / row["attributable"]
                    texts[i, j] = (
                        f"{int(row['confirmed_drift'])}/{int(row['attributable'])}"
                    )
                else:
                    texts[i, j] = f"U{int(row['unresolved'])}"
        image = ax.imshow(
            np.ma.masked_invalid(values), vmin=0, vmax=1, cmap=cmap, aspect="auto"
        )
        for (i, j), label in texts.items():
            ax.text(
                j,
                i,
                label,
                ha="center",
                va="center",
                fontsize=8,
                color=(
                    "white"
                    if np.isfinite(values[i, j]) and values[i, j] >= 0.6
                    else "#222222"
                ),
            )
            if not np.isfinite(values[i, j]):
                ax.add_patch(
                    Rectangle(
                        (j - 0.5, i - 0.5),
                        1,
                        1,
                        fill=False,
                        hatch="///",
                        edgecolor="#bdbdbd",
                        linewidth=0,
                    )
                )
        ax.set_xticks(range(len(MODES)), labels, fontsize=8)
        ax.set_yticks(
            range(len(categories)),
            [category.replace("_", " ") for category in categories],
            fontsize=9,
        )
        ax.set_xticks(np.arange(-0.5, len(MODES), 1), minor=True)
        ax.set_yticks(np.arange(-0.5, len(categories), 1), minor=True)
        ax.grid(which="minor", color="white", linewidth=0.8)
        ax.tick_params(which="both", length=0)
        ax.set_title(formatter.title(), pad=13, fontsize=12)
    color_ax = fig.add_axes([0.35, 0.13, 0.48, 0.02])
    colorbar = fig.colorbar(image, cax=color_ax, orientation="horizontal")
    colorbar.ax.xaxis.set_major_formatter(PercentFormatter(1, decimals=0))
    colorbar.set_label(
        "Confirmed drift / resolved comparisons in each cell", fontsize=9
    )
    fig.suptitle(
        "Structural and directive patterns in the controlled suite",
        x=0.19,
        y=0.969,
        ha="left",
        fontsize=14,
    )
    fig.text(
        0.19,
        0.914,
        "Cells show affected/resolved counts, not independent replicates. U marks unresolved comparisons, not zeros.",
        fontsize=9,
    )
    fig.text(
        0.19,
        0.04,
        "Each cell contains one to three related templates. The same eight treatments and inputs are paired across formatters.\n"
        "Boundary templates remain unclassified; no per-cell significance tests or population interpretation.",
        fontsize=8.5,
    )
    export(fig, directory, "figure3_structural_patterns")


def figure_relevance(frame, directory):
    natural = frame[(frame["dataset"] == "natural") & (frame["formatter"] == "black")]
    fig, ax = plt.subplots(figsize=(10, 4.5))
    fig.subplots_adjust(left=0.19, right=0.96, top=0.79, bottom=0.29)
    groups = (
        "No selected diagnostics",
        "Selected warnings; none suppressed",
        "Original selected-rule suppression",
    )
    colors = ("#cccccc", "#DDCC77", "#117733")
    for y, repo in enumerate(REPOS):
        subset = natural[natural["repository"] == repo]
        values = [
            int(subset["underlying_original"].eq(0).sum()),
            int(
                (
                    subset["underlying_original"].gt(0)
                    & subset["suppressed_original"].eq(0)
                ).sum()
            ),
            int(subset["suppressed_original"].gt(0).sum()),
        ]
        left = 0
        for value, color in zip(values, colors):
            if value:
                ax.barh(y, value, left=left, color=color, edgecolor="white", height=0.6)
                ax.text(
                    left + value / 2,
                    y,
                    str(value),
                    ha="center",
                    va="center",
                    fontsize=10,
                    color="white" if color == "#117733" else "#222222",
                )
            left += value
        ax.text(left + 0.35, y, f"n={left}", va="center", fontsize=9)
    ax.set_yticks(range(3), [REPO_NAMES[repo] for repo in REPOS])
    ax.set_ylim(2.55, -0.65)
    ax.set_xlim(0, 23)
    ax.set_xticks([0, 5, 10, 15, 20])
    ax.set_xlabel("Original files · each counted once before either formatter")
    ax.grid(axis="x", alpha=0.14)
    ax.set_axisbelow(True)
    fig.suptitle(
        "Diagnostic relevance of the natural-source sample",
        x=0.19,
        y=0.96,
        ha="left",
        fontsize=14,
    )
    fig.text(
        0.19,
        0.855,
        "Rules F401/F821/F841 only; natural noqa may instead target other rules.",
        fontsize=9,
    )
    fig.legend(
        [Patch(facecolor=color) for color in colors],
        groups,
        loc="lower center",
        bbox_to_anchor=(0.56, 0.015),
        ncol=1,
        frameon=False,
        fontsize=8.5,
    )
    export(fig, directory, "figure4_natural_relevance")


def make_figures(frame, pairs, metrics, tables, directory, root):
    style()
    figure_outcomes(metrics, directory)
    figure_pairs(pairs, metrics, directory, root)
    figure_patterns(tables, directory, root)
    figure_relevance(frame, directory)
    return {
        "figure1_outcomes": "Primary outcome distribution. Counts are labeled; fractions use scheduled denominators (200 per controlled formatter; 7/13/20 per natural repository). Ambiguity and strict AST exclusions remain visible. No experimental failures, mixed or underlying-change outcomes were observed. These exact corpus summaries need no IID trial-level intervals.",
        "figure2_paired_comparison": "Controlled paired template profiles and common-resolved 2x2 counts. Cluster model intervals use 20,000 paired whole-cluster resamples, template seed 20261103 and category seed 20261104. Intervals are exploratory conditional sensitivity, not ecosystem coverage; two unresolved boundary templates are excluded from this conditional comparison.",
        "figure3_structural_patterns": "Controlled syntax category by directive treatment. Labels are confirmed drift / attributable comparisons; hatched U cells indicate unresolved counts. Small, related template groups and paired inputs imply dependence. Color is descriptive and supplies no population or significance claim.",
        "figure4_natural_relevance": "Original natural-source diagnostic relevance on 40 unique files, counted once. Twenty-two files have no selected underlying warnings. The three mutually exclusive relevance groups describe the baseline; they are not eligibility filters or necessary conditions for every possible drift mechanism.",
    }
