"""Verify immutable archives, deterministic selection, exports and repeat pairs."""

import argparse
import csv
import hashlib
import json
from pathlib import Path
import shutil
import tempfile

from suppression_study.pipeline import ROOT, ast_signature, save_json
from suppression_study.evidence import evidence_bytes
from suppression_study.real_world import inspect_archive
from suppression_study.real_world_experiment import (
    NATIVE_FIELDS,
    WORLD_FIELDS,
    world_summary,
)
from verify_phase2 import without_execution_paths


def csv_matches(directory, name, records, fields):
    with (directory / name).open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    assert len(rows) == len(records)
    for row, record in zip(rows, records):
        for field in fields:
            expected = record.get(field)
            if isinstance(expected, (dict, list)):
                assert json.loads(row[field]) == expected, (record["trial_id"], field)
            else:
                assert row[field] == ("" if expected is None else str(expected)), (
                    record["trial_id"],
                    field,
                )


def verify_run(directory, manifest, dataset):
    state = json.loads((directory / "run.json").read_text(encoding="utf-8"))
    assert state["status"] == "complete"
    assert (directory / "manifest.json").read_bytes() == (
        dataset / "manifest.json"
    ).read_bytes()
    records = [
        json.loads(line)
        for line in (directory / "results.jsonl")
        .read_text(encoding="utf-8")
        .splitlines()
    ]
    natives = [
        json.loads(line)
        for line in (directory / "native_results.jsonl")
        .read_text(encoding="utf-8")
        .splitlines()
    ]
    assert len(records) == len(natives) == state["planned_comparisons"]
    csv_matches(directory, "results.csv", records, WORLD_FIELDS)
    csv_matches(directory, "native_results.csv", natives, NATIVE_FIELDS)
    selected = [
        case
        for case in manifest["cases"]
        if not state["repeat"] or case["reproduction_selected"]
    ]
    expected = {
        (case["case_id"], formatter)
        for case in selected
        for formatter in ("black", "ruff")
    }
    assert {(r["case_id"], r["formatter"]) for r in records} == expected
    assert len({r["trial_id"] for r in records}) == len(records)
    cases = {case["case_id"]: case for case in manifest["cases"]}
    indexed, native_indexed = {}, {}
    for result, native in zip(records, natives):
        case = cases[result["case_id"]]
        trial = directory / "trials" / result["case_id"] / result["formatter"]
        assert json.loads((trial / "result.json").read_text(encoding="utf-8")) == result
        assert (
            evidence_bytes(trial / "before.py")
            == (dataset / case["source"]).read_bytes()
        )
        assert (
            hashlib.sha256(evidence_bytes(trial / "before.py")).hexdigest()
            == result["input_sha256"]
        )
        if result.get("output_sha256"):
            assert (
                hashlib.sha256(evidence_bytes(trial / "after.py")).hexdigest()
                == result["output_sha256"]
            )
        if result.get("ast_equivalent") is not None:
            assert (
                ast_signature(evidence_bytes(trial / "before.py").decode())
                == ast_signature(evidence_bytes(trial / "after.py").decode())
            ) == result["ast_equivalent"]
        for label, diagnostics in result.get("passes", {}).items():
            assert (
                json.loads((trial / f"{label}.stdout.txt").read_text(encoding="utf-8"))
                == diagnostics
            )
        assert result["repository_commit"] == case["repository_commit"]
        assert (
            result["original_path"] == case["path"] and result["ai_assisted"] is False
        )
        assert native["trial_id"] == result["trial_id"]
        if (trial / "native/result.json").exists():
            core = json.loads(
                (trial / "native/result.json").read_text(encoding="utf-8")
            )
            assert all(native[key] == value for key, value in core.items())
            for label, diagnostics in native.get("full_native_passes", {}).items():
                assert (
                    json.loads(
                        (trial / "native" / f"{label}.stdout.txt").read_text(
                            encoding="utf-8"
                        )
                    )
                    == diagnostics
                )
        indexed[(result["case_id"], result["formatter"])] = result
        native_indexed[(result["case_id"], result["formatter"])] = native
    assert json.loads(
        (directory / "preliminary_summary.json").read_text(encoding="utf-8")
    )["primary"] == world_summary(records)
    return indexed, native_indexed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dataset", type=Path, default=ROOT / "datasets/real_world/phase4"
    )
    parser.add_argument("--main", type=Path, default=ROOT / "datasets/results/phase4")
    parser.add_argument(
        "--repeat", type=Path, default=ROOT / "datasets/results/phase4-repeat"
    )
    parser.add_argument(
        "--report", type=Path, default=ROOT / "reports/phase4/evidence_checks.json"
    )
    parser.add_argument("--archive-cache", type=Path)
    parser.add_argument("--allow-missing-archives", action="store_true")
    args = parser.parse_args()
    dataset = args.dataset.resolve()
    manifest = json.loads((dataset / "manifest.json").read_text(encoding="utf-8"))
    spec = json.loads((dataset / "specification.json").read_text(encoding="utf-8"))
    archive_root = (
        args.archive_cache.resolve() if args.archive_cache else dataset / "archives"
    )
    archives_present = all(
        (archive_root / Path(repo["archive"]).name).is_file()
        for repo in manifest["repositories"]
    )
    if not archives_present and not args.allow_missing_archives:
        raise FileNotFoundError(
            "Upstream archives are excluded from the public snapshot. Fetch with scripts/fetch_pinned_archives.py, pass --archive-cache, or explicitly use --allow-missing-archives for retained-evidence checks only."
        )
    with tempfile.TemporaryDirectory(prefix="phase4-resample-") as temporary:
        regenerated = Path(temporary)
        (regenerated / "archives").mkdir()
        for repo in manifest["repositories"]:
            if not archives_present:
                continue
            archive = archive_root / Path(repo["archive"]).name
            assert (
                hashlib.sha256(archive.read_bytes()).hexdigest()
                == repo["archive_sha256"]
            )
            copied_archive = regenerated / repo["archive"]
            shutil.copyfile(archive, copied_archive)
            report, cases = inspect_archive(
                copied_archive,
                repo,
                regenerated,
                manifest["seed"],
                spec["sample_per_repository"],
            )
            original_population = json.loads(
                (
                    dataset / f"{repo['repository'].replace('/', '--')}.population.json"
                ).read_text(encoding="utf-8")
            )
            assert report["population"] == original_population["population"]
            assert report["context_sha256"] == repo["context_sha256"]
            assert cases == [
                case
                for case in manifest["cases"]
                if case["repository"] == repo["repository"]
            ]
            for case in cases:
                assert (regenerated / case["source"]).read_bytes() == (
                    dataset / case["source"]
                ).read_bytes()
    first, native_first = verify_run(args.main, manifest, dataset)
    repeat, native_repeat = verify_run(args.repeat, manifest, dataset)
    fields = (
        "input_sha256",
        "output_sha256",
        "classification",
        "validation_status",
        "ast_equivalent",
        "formatting_changed",
        "counts",
        "newly_hidden_count",
        "newly_exposed_count",
        "passes",
        "matched_diagnostic_identities",
        "matching_errors",
        "underlying_changes",
    )
    for identity, record in repeat.items():
        for field in fields:
            assert without_execution_paths(
                first[identity].get(field)
            ) == without_execution_paths(record.get(field)), (identity, field)
        for field in (
            "classification",
            "validation_status",
            "counts",
            "passes",
            "full_native_passes",
            "matched_diagnostic_identities",
        ):
            assert without_execution_paths(
                native_first[identity].get(field)
            ) == without_execution_paths(native_repeat[identity].get(field)), (
                "native",
                identity,
                field,
            )
    result = {
        "archive_hashes_verified": archives_present,
        "population_and_sample_recreated": archives_present,
        "selected_original_bytes_identical": archives_present,
        "archive_check_note": (
            "Full checksum and selection reconstruction"
            if archives_present
            else "Explicitly omitted: archives absent; retained source, diagnostics and repeat checks still performed"
        ),
        "primary_records_checked": len(first),
        "native_status_records_checked": len(native_first),
        "repeat_comparisons_checked": len(repeat),
        "csv_jsonl_raw_evidence_checked": True,
        "repeat_measurements_identical": True,
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    save_json(args.report, result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
