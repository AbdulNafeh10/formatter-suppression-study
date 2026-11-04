"""Collect pinned immutable archives; do not execute repository code."""

import argparse
from pathlib import Path

from suppression_study.pipeline import ROOT
from suppression_study.real_world import collect

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--spec", type=Path, default=ROOT / "configs/repositories.json")
parser.add_argument("--output", type=Path, default=ROOT / "datasets/real_world/phase4")
args = parser.parse_args()
manifest = collect(args.spec, args.output)
raise SystemExit(
    0 if len(manifest["repositories"]) >= 3 and not manifest["failures"] else 2
)
