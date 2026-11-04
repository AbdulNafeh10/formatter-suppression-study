import csv
import hashlib
import json

import pytest

from suppression_study.generator import (
    MODES,
    TEMPLATES,
    Template,
    render,
    write_dataset,
)
from suppression_study.experiment import load_config, run_experiment
from suppression_study.pipeline import ROOT, measure


def config_file(tmp_path, dataset, output, repeat=True):
    config = tmp_path / "config.toml"
    text = (ROOT / "configs/controlled.toml").read_text(encoding="utf-8")
    text = text.replace(
        'dataset = "datasets/controlled/phase3"',
        f"dataset = {json.dumps(dataset.as_posix())}",
    )
    text = text.replace(
        'output = "datasets/results/phase3"',
        f"output = {json.dumps(output.as_posix())}",
    )
    if repeat:
        text = text.replace("repeat_only = false", "repeat_only = true")
    config.write_text(text, encoding="utf-8")
    return config


def test_full_factorial_generation_is_valid_diverse_and_repeatable(tmp_path):
    first = write_dataset(tmp_path / "one")
    second = write_dataset(tmp_path / "two")
    assert first == second
    assert len(first["cases"]) == 200
    assert all(case["accepted"] for case in first["cases"])
    assert len({case["input_sha256"] for case in first["cases"]}) == 200
    assert len({case["input_structure_sha256"] for case in first["cases"]}) == 25
    assert len({case["syntax_category"] for case in first["cases"]}) >= 10
    assert sum(case["reproduction_selected"] for case in first["cases"]) == 25
    assert {
        case["directive_placement"]
        for case in first["cases"]
        if case["reproduction_selected"]
    } == set(MODES)
    assert {
        case["input_family"] for case in first["cases"] if case["reproduction_selected"]
    } == {t.name for t in TEMPLATES}
    for case in first["cases"]:
        assert (tmp_path / "one" / case["source"]).read_bytes() == (
            tmp_path / "two" / case["source"]
        ).read_bytes()
        assert case["ai_assisted"] is True


def test_changed_seed_changes_order_not_sources(tmp_path):
    first = write_dataset(tmp_path / "one", seed=1)
    second = write_dataset(tmp_path / "two", seed=2)
    assert first["execution_order"] != second["execution_order"]
    assert [c["input_sha256"] for c in first["cases"]] == [
        c["input_sha256"] for c in second["cases"]
    ]


def test_invalid_and_duplicate_candidates_are_retained(tmp_path):
    template = Template("invalid", "invalid", "F821", "def (@FIRST@\n x@LAST@\n")
    original = TEMPLATES[0]
    duplicate = Template("duplicate", original.category, original.rule, original.source)
    manifest = write_dataset(
        tmp_path / "dataset", templates=(original, duplicate, template)
    )
    assert len(manifest["cases"]) == 24
    assert sum(c["accepted"] for c in manifest["cases"]) == 8
    assert all(c["duplicate_of"] for c in manifest["cases"][8:16])
    assert all(c["syntax_error"] for c in manifest["cases"][16:])
    assert all((tmp_path / "dataset" / c["source"]).exists() for c in manifest["cases"])


def test_metadata_cannot_override_findings(tmp_path):
    with pytest.raises(ValueError, match="reserved"):
        measure(
            "x=1\n",
            tmp_path / "evidence",
            after="x=1\n",
            case_metadata={"classification": "Preserved"},
        )


def test_bad_modes_and_template_markers():
    with pytest.raises(ValueError):
        render(TEMPLATES[0], "unknown")
    with pytest.raises(ValueError):
        render(Template("bad", "bad", "F821", "x=1\n"), "none")


def test_actual_paired_experiment_exports_metadata_and_raw_diagnostics(tmp_path):
    dataset, output = tmp_path / "dataset", tmp_path / "results"
    write_dataset(dataset, templates=(TEMPLATES[3],))
    config = config_file(tmp_path, dataset, output)
    summary = run_experiment(config)
    assert summary["recorded_comparisons"] == 2
    records = [
        json.loads(line)
        for line in (output / "results.jsonl").read_text(encoding="utf-8").splitlines()
    ]
    with (output / "results.csv").open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    assert len(records) == len(rows) == 2
    for record, row in zip(records, rows):
        assert record["phase"] == 3
        assert record["generation_seed"] == 20261103
        assert record["input_family"] == "list_short"
        assert record["classification"] == "Preserved"
        assert record["environment"]["seed"] == 20261103
        assert (
            record["manifest_sha256"]
            == hashlib.sha256((dataset / "manifest.json").read_bytes()).hexdigest()
        )
        assert json.loads(row["passes"]) == record["passes"]
        assert (
            json.loads(row["matched_diagnostic_identities"])
            == record["matched_diagnostic_identities"]
        )
    assert records[0]["input_sha256"] == records[1]["input_sha256"]
    assert json.loads((output / "run.json").read_text())["status"] == "complete"
    with pytest.raises(FileExistsError):
        run_experiment(config)


def test_source_tampering_fails_before_tool_execution(tmp_path):
    dataset, output = tmp_path / "dataset", tmp_path / "results"
    manifest = write_dataset(dataset, templates=(TEMPLATES[0],))
    case = next(c for c in manifest["cases"] if c["reproduction_selected"])
    (dataset / case["source"]).write_text("x=1\n", encoding="utf-8")
    with pytest.raises(ValueError, match="checksum"):
        run_experiment(config_file(tmp_path, dataset, output))
    assert not output.exists()


def test_relevance_exclusion_is_exported_without_fabricated_classification(tmp_path):
    dataset, output = tmp_path / "dataset", tmp_path / "results"
    write_dataset(
        dataset,
        templates=(Template("clean", "control", "F821", "x=1@FIRST@\ny=2@LAST@\n"),),
    )
    summary = run_experiment(config_file(tmp_path, dataset, output))
    assert summary["excluded_preflight"] == 2
    records = [
        json.loads(line) for line in (output / "results.jsonl").read_text().splitlines()
    ]
    assert all(
        r["validation_status"] == "excluded_preflight" and r["classification"] is None
        for r in records
    )


def test_config_cannot_change_validated_rules_or_overlap_dataset(tmp_path):
    config = config_file(tmp_path, tmp_path / "dataset", tmp_path / "results")
    config.write_text(config.read_text().replace('"F841"', '"E501"'))
    with pytest.raises(ValueError, match="settings"):
        load_config(config)
    config = config_file(
        tmp_path, tmp_path / "dataset", tmp_path / "dataset" / "results"
    )
    with pytest.raises(ValueError, match="overlap"):
        load_config(config)
