"""Verify deterministic metrics/tables/draws and rendered figure reproduction."""

import argparse
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET

from PIL import Image

from suppression_study.pipeline import ROOT, save_json


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--first", type=Path, default=ROOT / "reports/phase5/analysis")
    parser.add_argument(
        "--repeat", type=Path, default=ROOT / "reports/phase5/reproduction"
    )
    parser.add_argument("--figures", type=Path, default=ROOT / "reports/figures")
    parser.add_argument(
        "--repeat-figures",
        type=Path,
        default=ROOT / "reports/phase5/reproduction/figures",
    )
    parser.add_argument(
        "--report", type=Path, default=ROOT / "reports/phase5/reproduction_checks.json"
    )
    args = parser.parse_args()
    first = json.loads((args.first / "provenance.json").read_text(encoding="utf-8"))
    repeat = json.loads((args.repeat / "provenance.json").read_text(encoding="utf-8"))
    assert first["input_sha256"] == repeat["input_sha256"]
    assert first["analysis_versions"] == repeat["analysis_versions"]
    assert (
        first["analysis_specification_sha256"]
        == repeat["analysis_specification_sha256"]
    )
    assert first["artifacts"] == repeat["artifacts"]
    assert first["figures"] == repeat["figures"]
    for directory, provenance in ((args.first, first), (args.repeat, repeat)):
        for name, checksum in provenance["artifacts"].items():
            assert (
                hashlib.sha256((directory / name).read_bytes()).hexdigest() == checksum
            )
    dimensions = {}
    for directory, provenance in ((args.figures, first), (args.repeat_figures, repeat)):
        assert len(provenance["figures"]) == 8
        for name, checksum in provenance["figures"].items():
            path = directory / name
            assert hashlib.sha256(path.read_bytes()).hexdigest() == checksum
            if path.suffix == ".png":
                with Image.open(path) as bitmap:
                    assert bitmap.width >= 2000 and bitmap.height >= 1000
                    dimensions[name] = list(bitmap.size)
                    bitmap.verify()
            else:
                vector = ET.parse(path)
                assert len(vector.findall(".//{http://www.w3.org/2000/svg}text")) > 10
    result = {
        "input_digests_identical": True,
        "numeric_tables_and_interval_draws_identical": True,
        "all_four_png_svg_pairs_identical": True,
        "png_and_svg_integrity_verified": True,
        "artifacts_checked_per_run": len(first["artifacts"]),
        "figure_dimensions": dimensions,
        "note": "Analysis environment snapshots are provenance, not experimental or detector accuracy evidence.",
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    save_json(args.report, result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
