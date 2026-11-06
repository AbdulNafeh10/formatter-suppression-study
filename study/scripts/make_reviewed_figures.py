"""Export supplementary figures without replacing the original research figures."""

import argparse
import hashlib
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch, Rectangle
from matplotlib.ticker import PercentFormatter
import numpy as np
import pandas as pd

from suppression_study.figures import COLORS, FORMATTER, style
from suppression_study.pipeline import ROOT


def run(output, data):
    if output.exists() or not any(
        output.is_relative_to(ROOT / name) for name in ("local", "reports")
    ):
        raise ValueError("Use a new figure directory under local or reports")
    metrics = json.loads((data / "metrics.json").read_bytes())
    frame = pd.read_csv(data / "review_overlay.csv")
    spec = json.loads(
        (ROOT / "datasets/controlled/phase3/specification.json").read_bytes()
    )
    if len(frame) != 400 or frame.duplicated(["case_id", "formatter"]).any():
        raise ValueError("Figure observations are not the approved paired corpus")
    output.mkdir(parents=True)
    style()
    plt.rcParams["svg.hashsalt"] = "suppression-study-public-reviewed-v1"
    captions, plotted = {}, {}

    def export(fig, name, caption, values):
        for suffix in ("png", "svg"):
            metadata = (
                {"Software": "formatter-suppression-study supplementary review"}
                if suffix == "png"
                else {
                    "Date": None,
                    "Creator": "formatter-suppression-study supplementary review",
                }
            )
            fig.savefig(output / f"{name}.{suffix}", dpi=300, metadata=metadata)
        plt.close(fig)
        captions[name] = caption
        plotted[name] = values

    fig, ax = plt.subplots(figsize=(10, 4.3))
    labels, rows = [], []
    for group, title in (
        ("original_controlled", "Original automatic"),
        ("reviewed_controlled", "Supplementary reviewed"),
    ):
        for formatter in ("black", "ruff"):
            summary = metrics[group][formatter]
            rows.append(summary)
            labels.append(f"{title}: {formatter.title()}")
            index = len(rows) - 1
            left = 0
            for outcome in ("Preserved", "Newly hidden", "Newly exposed", "Ambiguous"):
                count = summary["outcomes"][outcome]
                width = count / summary["scheduled"] * 100
                if count:
                    ax.barh(
                        index,
                        width,
                        left=left,
                        color=COLORS[outcome],
                        edgecolor="white",
                        height=0.66,
                    )
                    ax.text(
                        left + width / 2,
                        index,
                        str(count),
                        ha="center",
                        va="center",
                        color=(
                            "white"
                            if outcome in ("Preserved", "Newly hidden")
                            else "black"
                        ),
                        fontsize=10,
                    )
                left += width
            if left != 100:
                raise ValueError("Outcome stack does not cover its denominator")
    ax.set(
        yticks=range(4),
        yticklabels=labels,
        xlim=(0, 100),
        xlabel="Share of 200 controlled comparisons per bar; labels are counts",
    )
    ax.invert_yaxis()
    ax.xaxis.set_major_formatter(PercentFormatter())
    ax.legend(
        handles=[
            Patch(facecolor=COLORS[x], label=x)
            for x in ("Preserved", "Newly hidden", "Newly exposed", "Ambiguous")
        ],
        ncol=4,
        loc="upper center",
        bbox_to_anchor=(0.47, -0.2),
        frameon=False,
    )
    fig.suptitle(
        "Original classifications and supplementary reviewed outcomes", fontsize=13
    )
    fig.text(
        0.5,
        0.02,
        "Reviewed bars accept AI-assisted proposals; they are not independent human ground truth.",
        ha="center",
        fontsize=9,
    )
    fig.subplots_adjust(left=0.26, right=0.98, top=0.85, bottom=0.29)
    export(
        fig,
        "figure1_reviewed_outcomes",
        "Controlled outcomes, 200 comparisons per bar. Reviewed counts accept the AI-assisted proposals; original ambiguity remains visible in the automatic bars.",
        {"labels": labels, "summaries": rows},
    )

    families = pd.read_csv(data / "reviewed_family_counts.csv").set_index(
        "input_family_black"
    )
    order = [t["name"] for t in spec["templates"]]
    families = families.loc[order]
    fig = plt.figure(figsize=(12.8, 9))
    grid = fig.add_gridspec(
        2, 2, height_ratios=[4, 1.2], width_ratios=[1.35, 1], hspace=0.55, wspace=0.38
    )
    profiles, matrix_ax, intervals = (
        fig.add_subplot(grid[0, 0]),
        fig.add_subplot(grid[0, 1]),
        fig.add_subplot(grid[1, :]),
    )
    y = np.arange(len(families))
    profiles.hlines(
        y,
        families["ruff"] / families["n"] * 100,
        families["black"] / families["n"] * 100,
        color=".75",
    )
    for formatter, marker in (("black", "o"), ("ruff", "x")):
        profiles.scatter(
            families[formatter] / families["n"] * 100,
            y,
            marker=marker,
            color=FORMATTER[formatter],
            label=formatter.title(),
            s=24,
            zorder=3,
        )
    profiles.set(
        yticks=y,
        yticklabels=[x.replace("_", " ") for x in order],
        xlim=(-2, 102),
        xlabel="Drift across eight directive modes",
    )
    profiles.tick_params(axis="y", labelsize=8)
    profiles.invert_yaxis()
    profiles.xaxis.set_major_formatter(PercentFormatter())
    profiles.legend(frameon=False, loc="lower right")
    matrix = np.asarray(metrics["reviewed_pairs"]["matrix_rows_black_columns_ruff_0_1"])
    if matrix.sum() != 200:
        raise ValueError("Reviewed pair denominator differs")
    matrix_ax.imshow(matrix, cmap="Blues", vmin=0, vmax=matrix.max())
    for i in range(2):
        for j in range(2):
            matrix_ax.text(
                j,
                i,
                str(matrix[i, j]),
                ha="center",
                va="center",
                fontsize=26,
                color="white" if matrix[i, j] > matrix.max() / 2 else "black",
            )
    matrix_ax.set(
        xticks=[0, 1],
        yticks=[0, 1],
        xticklabels=["No drift", "Drift"],
        yticklabels=["No drift", "Drift"],
        xlabel="Ruff",
        ylabel="Black",
        title="200 reviewed input pairs",
    )
    for index, grouping in enumerate(("family", "category")):
        result = metrics["reviewed_cluster_model_intervals"][grouping]
        statistic = result["statistics"]["black_minus_ruff"]
        point, lo, hi = [100 * statistic[k] for k in ("estimate", "lower", "upper")]
        intervals.errorbar(
            point,
            index,
            xerr=[[point - lo], [hi - point]],
            fmt="o",
            color=FORMATTER["black"] if index == 0 else "#AA4499",
            capsize=4,
        )
        intervals.text(
            hi + 0.8,
            index,
            f"{point:.2f} [{lo:.2f}, {hi:.2f}]",
            va="center",
            fontsize=9,
        )
    intervals.set(
        yticks=[0, 1],
        yticklabels=["25 family clusters", "13 category clusters"],
        ylim=(-0.5, 1.5),
        xlim=(-1, 40),
        xlabel="Black minus Ruff drift difference (percentage points)",
    )
    intervals.axvline(0, color=".5", linestyle="--", linewidth=0.8)
    intervals.invert_yaxis()
    fig.suptitle(
        "Supplementary paired comparison, conditional on the AI-assisted review",
        fontsize=13,
    )
    fig.text(
        0.5,
        0.018,
        "95% exploratory cluster-model intervals; no ecosystem inference or independent human adjudication.",
        ha="center",
        fontsize=9,
    )
    fig.subplots_adjust(left=0.22, right=0.98, top=0.9, bottom=0.1)
    export(
        fig,
        "figure2_reviewed_pairs",
        "Reviewed family profiles, 200-pair table and recalculated 95% cluster-model intervals. Review proposals and independent exchangeable-cluster assumptions remain conditional.",
        {
            "family_counts": families.reset_index().to_dict("records"),
            "matrix": matrix.tolist(),
            "intervals": metrics["reviewed_cluster_model_intervals"],
        },
    )

    categories = list(dict.fromkeys(t["category"] for t in spec["templates"]))
    modes = spec["modes"]
    fig, axes = plt.subplots(1, 2, figsize=(14, 8), sharey=True)
    tables = []
    for ax, formatter in zip(axes, ("black", "ruff")):
        subset = frame[frame["formatter"].eq(formatter)]
        grouped = subset.groupby(["syntax_category", "directive_placement"]).agg(
            drift=("drift", "sum"), n=("case_id", "size")
        )
        values = np.zeros((len(categories), len(modes)))
        for i, category in enumerate(categories):
            for j, mode in enumerate(modes):
                row = grouped.loc[(category, mode)]
                values[i, j] = row["drift"] / row["n"]
                tables.append(
                    {
                        "formatter": formatter,
                        "category": category,
                        "mode": mode,
                        "drift": int(row["drift"]),
                        "n": int(row["n"]),
                    }
                )
        image = ax.imshow(values, vmin=0, vmax=1, cmap="Blues", aspect="auto")
        for i, category in enumerate(categories):
            for j, mode in enumerate(modes):
                row = grouped.loc[(category, mode)]
                ax.text(
                    j,
                    i,
                    f"{int(row['drift'])}/{int(row['n'])}",
                    ha="center",
                    va="center",
                    fontsize=8,
                    color="white" if values[i, j] > 0.55 else "black",
                )
        boundary = categories.index("oracle_boundaries")
        ax.add_patch(
            Rectangle(
                (-0.5, boundary - 0.5),
                len(modes),
                1,
                fill=False,
                edgecolor="#AA4499",
                linewidth=1.8,
            )
        )
        ax.set(
            title=formatter.title(),
            xticks=range(len(modes)),
            xticklabels=[x.replace("_", "\n") for x in modes],
            yticks=range(len(categories)),
            yticklabels=[x.replace("_", " ") for x in categories],
        )
        ax.tick_params(axis="x", labelsize=8)
    fig.suptitle(
        "Supplementary drift by source category and directive mode", fontsize=13
    )
    fig.text(
        0.5,
        0.925,
        "Labels are affected / reviewed comparisons; outlined boundary row uses AI-assisted proposals.",
        ha="center",
        fontsize=9,
    )
    colorbar = fig.colorbar(
        image,
        ax=list(axes),
        orientation="horizontal",
        fraction=0.04,
        pad=0.15,
        ticks=[0, 0.5, 1],
    )
    colorbar.ax.set_xticklabels(["0%", "50%", "100%"])
    fig.text(
        0.5,
        0.02,
        "Related templates are not independent samples of Python projects. Original unresolved cells remain in the original figure.",
        ha="center",
        fontsize=9,
    )
    fig.subplots_adjust(left=0.17, right=0.98, top=0.87, bottom=0.29, wspace=0.08)
    export(
        fig,
        "figure3_reviewed_patterns",
        "Drift / reviewed counts by category and directive mode. The outlined boundary row accepts AI-assisted Preserved proposals; original U2 cells are retained in the original figure.",
        tables,
    )
    for name, value in (("captions.json", captions), ("plotted_values.json", plotted)):
        (output / name).write_bytes((json.dumps(value, indent=2) + "\n").encode())
    inputs = [
        data / name
        for name in ("metrics.json", "review_overlay.csv", "reviewed_family_counts.csv")
    ]
    inputs.append(ROOT / "datasets/controlled/phase3/specification.json")
    provenance = {
        "input_sha256": {
            p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in inputs
        },
        "artifacts": {
            p.name: hashlib.sha256(p.read_bytes()).hexdigest()
            for p in output.iterdir()
            if p.is_file()
        },
    }
    (output / "provenance.json").write_bytes(
        (json.dumps(provenance, indent=2) + "\n").encode()
    )
    print(f"Exported {len(captions)} reviewed figures as PNG/SVG: {output}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output", type=Path, default=ROOT / "reports/figures-reviewed"
    )
    parser.add_argument(
        "--data", type=Path, default=ROOT / "reports/publication-phase-a/analysis"
    )
    args = parser.parse_args()
    run(args.output.resolve(), args.data.resolve())
