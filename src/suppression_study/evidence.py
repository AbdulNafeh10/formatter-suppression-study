"""Decode public source containers without changing measured source bytes."""

import hashlib
import json
from pathlib import Path


def evidence_bytes(path):
    path = Path(path)
    if path.is_file():
        return path.read_bytes()
    container = path.with_name(path.name + ".evidence.json")
    packet = json.loads(container.read_text(encoding="utf-8"))
    if (
        packet.get("public_evidence_schema") != 1
        or packet.get("logical_filename") != path.name
    ):
        raise ValueError("Unsupported or mismatched public evidence container")
    if not packet.get("third_party_modification_notice"):
        raise ValueError("Public source container lacks its modification notice")
    data = packet["source_text"].encode("utf-8")
    if hashlib.sha256(data).hexdigest() != packet["original_sha256"]:
        raise ValueError("Decoded evidence differs from the original source checksum")
    return data
