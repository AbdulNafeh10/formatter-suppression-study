"""Restore the research evidence, rerun the study, and verify its results."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from tempfile import mkdtemp
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parent
BUNDLE = ROOT / "evidence" / "study.zip"


def unpack():
    with ZipFile(BUNDLE) as archive:
        manifest = json.loads(archive.read("sha256.json"))
        if len(archive.namelist()) != len(manifest) + 1 or set(archive.namelist()) != {
            "sha256.json",
            *manifest,
        }:
            raise ValueError("Unexpected evidence bundle members")
        for name, expected in manifest.items():
            target = ROOT / name
            parts = name.split("/")
            if (
                parts[0]
                not in {
                    "datasets",
                    "reports",
                    "docs",
                    "configs",
                    "LICENSE",
                    "NOTICE",
                    "THIRD_PARTY_NOTICES.md",
                    "third_party",
                }
                or any(part in {"", ".", ".."} for part in parts)
                or "\\" in name
                or ":" in name
                or target.resolve() != target
            ):
                raise ValueError(f"Unsafe evidence path: {name}")
            data = archive.read(name)
            if hashlib.sha256(data).hexdigest() != expected:
                raise ValueError(f"Evidence checksum differs: {name}")
            if target.exists():
                if target.read_bytes() != data:
                    raise ValueError(f"Existing evidence differs: {name}")
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            with target.open("xb") as stream:
                stream.write(data)
    print(f"Verified {len(manifest)} evidence files", flush=True)


def command(*args):
    subprocess.run([sys.executable, *map(str, args)], cwd=ROOT, check=True)


def verify_analysis(output):
    from scripts.build_report import resolve

    ledger = json.loads(
        (ROOT / "reports/publication-phase-b/public_claim_audit.json").read_bytes()
    )
    for key, claim in ledger["claims"].items():
        if resolve(ROOT, claim) != (
            claim["rendered"],
            claim["value"],
            claim["source_sha256"],
        ):
            raise ValueError(f"Report evidence binding differs: {key}")
    original = output / "original"
    reviewed = output / "reviewed"
    figures = output / "figures"
    command(
        "-m", "suppression_study", "analyze", "--output", original, "--figures", figures
    )
    command("scripts/analyze_reviewed_results.py", "--output", reviewed)
    for generated, retained in (
        (original, "reports/phase5/analysis"),
        (reviewed, "reports/publication-phase-a/analysis"),
    ):
        actual = json.loads((generated / "metrics.json").read_bytes())
        expected = json.loads((ROOT / retained / "metrics.json").read_bytes())
        if actual != expected:
            raise ValueError(f"Recalculated metrics differ: {retained}")
    reviewed_figures = output / "reviewed-figures"
    command(
        "scripts/make_reviewed_figures.py",
        "--data",
        reviewed,
        "--output",
        reviewed_figures,
    )
    from PIL import Image, ImageChops

    for original_png in (ROOT.parent / "report" / "figures").glob("*.png"):
        directory = (
            figures if original_png.name.startswith("figure4_") else reviewed_figures
        )
        with (
            Image.open(original_png) as old,
            Image.open(directory / original_png.name) as new,
        ):
            if (
                old.size != new.size
                or ImageChops.difference(
                    old.convert("RGB"), new.convert("RGB")
                ).getbbox()
            ):
                raise ValueError(f"Reproduced plot differs: {original_png.name}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--unpack", action="store_true", help="Restore and check saved files only"
    )
    mode.add_argument(
        "--check",
        action="store_true",
        help="Check saved trials and rerun the analysis without a full formatter run",
    )
    parser.add_argument(
        "--archives", type=Path, help="Check upstream archives in this cache"
    )
    args = parser.parse_args()
    if sys.flags.optimize:
        parser.error("Reproduction checks require assertions to be enabled")
    unpack()
    if args.unpack:
        return
    os.chdir(ROOT)
    local = ROOT / "local"
    local.mkdir(exist_ok=True)
    output = Path(mkdtemp(prefix="study-", dir=local))
    print(f"Study output: {output.relative_to(ROOT)}", flush=True)
    command("-m", "pytest", "-q")
    controlled_repeat = []
    natural_repeat = []
    if not args.check:
        from suppression_study.experiment import run_experiment
        from suppression_study.real_world_experiment import run_real_world

        config = (ROOT / "configs" / "controlled.toml").read_text(encoding="utf-8")
        repeat = output / "controlled"
        new_config = output / "controlled.toml"
        new_config.write_text(
            config.replace('"datasets/results/phase3"', json.dumps(repeat.as_posix())),
            encoding="utf-8",
        )
        run_experiment(new_config)
        controlled_repeat = ["--repeat", repeat]
        repeat = output / "natural"
        run_real_world(ROOT / "datasets" / "real_world" / "phase4", repeat)
        natural_repeat = ["--repeat", repeat]
    command(
        "scripts/verify_phase3.py",
        *controlled_repeat,
        "--report",
        output / "controlled-check.json",
    )
    archive_options = (
        ["--archive-cache", args.archives.resolve()]
        if args.archives
        else ["--allow-missing-archives"]
    )
    command(
        "scripts/verify_phase4.py",
        *natural_repeat,
        *archive_options,
        "--report",
        output / "natural-check.json",
    )
    verify_analysis(output)
    print("Study verification passed", flush=True)


if __name__ == "__main__":
    main()
