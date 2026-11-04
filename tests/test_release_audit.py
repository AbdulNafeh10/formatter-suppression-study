"""Scanner coverage and output privacy; injected strings are not real credentials."""

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "release_audit", ROOT / "scripts/audit_release_readiness.py"
)
audit = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(audit)


def test_detection_never_returns_matched_credentials():
    candidate = b"ghp_" + b"Z" * 36
    result = audit.scan(b'api_key="' + candidate + b'"')
    assert result["credential_patterns"]["github_token"] == 1
    assert candidate.decode() not in str(result)


def test_encoded_home_paths_and_contact_locations():
    data = (
        b"C:"
        + b"\\" * 4
        + b"Users"
        + b"\\" * 4
        + b"test_person"
        + b" text reader@example.org"
    )
    result = audit.scan(data)
    assert result["home_path_present"] and result["email_occurrences"] == 1
    assert "test_person" not in str(result)
    assert not result["credential_patterns"]


def test_archive_commit_path_does_not_look_like_api_key():
    candidate = b"sk-" + b"a" * 40
    assert audit.scan(candidate)["credential_patterns"]["openai_key_shape"] == 1
    archive_member = b"fla" + candidate + b"/LICENSE"
    assert not audit.scan(archive_member)["credential_patterns"]
