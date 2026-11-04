import argparse
from pathlib import Path

from suppression_study.pipeline import ROOT
from suppression_study.real_world_experiment import run_real_world

parser = argparse.ArgumentParser(description="Run frozen natural-source comparisons")
parser.add_argument("--repeat", action="store_true")
parser.add_argument("--output")
parser.add_argument("--dataset", type=Path, default=ROOT / "datasets/real_world/phase4")
args = parser.parse_args()
output = ROOT / (
    args.output
    or ("datasets/results/phase4-repeat" if args.repeat else "datasets/results/phase4")
)
run_real_world(args.dataset, output, repeat=args.repeat)
