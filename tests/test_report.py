"""Guard the evidence-to-report boundary, including accidental hand-edits."""

import importlib.util
import json
from pathlib import Path

import pytest

MODULE = Path(__file__).resolve().parents[1] / "scripts/build_report.py"
SPEC = importlib.util.spec_from_file_location("report_builder", MODULE)
builder = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(builder)


@pytest.fixture
def report_root(tmp_path):
    (tmp_path / "report").mkdir()
    (tmp_path / "evidence.json").write_text('{"count": 7}')
    (tmp_path / "report/research_report.template.md").write_text("Count: {{N}}\n")
    (tmp_path / "report/claim_spec.json").write_text(
        json.dumps(
            {"N": {"source": "evidence.json", "pointer": ["count"], "format": "int"}}
        )
    )
    return tmp_path


def test_report_rejects_stale_measurement_and_hand_edits(report_root):
    builder.build(report_root)
    builder.build(report_root, check=True)
    (report_root / "evidence.json").write_text('{"count": 8}')
    with pytest.raises(ValueError, match="stale or changed"):
        builder.build(report_root, check=True)
    builder.build(report_root)
    (report_root / "report/research_report.md").write_text("Count: 900\n")
    with pytest.raises(ValueError, match="stale or changed"):
        builder.build(report_root, check=True)


def test_report_rejects_unbound_claim(report_root):
    (report_root / "report/research_report.template.md").write_text("{{UNKNOWN}}")
    with pytest.raises(ValueError, match="claim keys differ"):
        builder.build(report_root)


def test_report_rejects_source_escape(report_root):
    with pytest.raises(ValueError, match="escapes repository"):
        builder.resolve(report_root, {"source": "../outside.json", "pointer": []})
