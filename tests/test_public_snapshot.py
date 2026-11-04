import hashlib
import json

import pytest

from suppression_study.evidence import evidence_bytes
from suppression_study.real_world_experiment import run_real_world


def packet(path, source):
    data = source.encode("utf-8")
    item = {
        "public_evidence_schema": 1,
        "logical_filename": path.name,
        "third_party_modification_notice": "Fixture modified for a source-container test",
        "original_sha256": hashlib.sha256(data).hexdigest(),
        "source_text": source,
    }
    path.with_name(path.name + ".evidence.json").write_text(json.dumps(item))
    return item


def test_source_container_preserves_crlf_and_unicode(tmp_path):
    path = tmp_path / "after.py"
    source = '# retained source\r\nvalue = "caf\u00e9"\r\n'
    packet(path, source)
    assert evidence_bytes(path) == source.encode("utf-8")


def test_source_container_rejects_changed_bytes_and_missing_notice(tmp_path):
    path = tmp_path / "after.py"
    item = packet(path, "value = 1\n")
    item["source_text"] = "value = 2\n"
    container = path.with_name(path.name + ".evidence.json")
    container.write_text(json.dumps(item))
    with pytest.raises(ValueError, match="checksum"):
        evidence_bytes(path)
    item = packet(path, "value = 1\n")
    item.pop("third_party_modification_notice")
    container.write_text(json.dumps(item))
    with pytest.raises(ValueError, match="notice"):
        evidence_bytes(path)


def test_public_omissions_cannot_bypass_native_configuration(tmp_path):
    manifest = {
        "cases": [],
        "repositories": [
            {
                "repository": "example/repo",
                "archive": "a.tar.gz",
                "archive_sha256": "0" * 64,
                "context_sha256": {"pyproject.toml": "0" * 64},
            }
        ],
        "public_export": {
            "upstream_archives_omitted": True,
            "omitted_context_files": {"example/repo": ["pyproject.toml"]},
        },
    }
    (tmp_path / "manifest.json").write_text(json.dumps(manifest))
    with pytest.raises(ValueError, match="cannot bypass"):
        run_real_world(tmp_path, tmp_path / "output")


def test_public_export_still_rejects_incorrect_supplied_archive(tmp_path):
    (tmp_path / "a.tar.gz").write_bytes(b"wrong archive")
    manifest = {
        "cases": [],
        "repositories": [
            {
                "repository": "example/repo",
                "archive": "a.tar.gz",
                "archive_sha256": "0" * 64,
                "context_sha256": {},
            }
        ],
        "public_export": {"upstream_archives_omitted": True},
    }
    (tmp_path / "manifest.json").write_text(json.dumps(manifest))
    with pytest.raises(ValueError, match="checksum"):
        run_real_world(tmp_path, tmp_path / "output")
