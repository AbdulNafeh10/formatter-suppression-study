"""Read-only file/history inventory. Findings contain locations, never credentials."""

import argparse
from collections import Counter
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess
import tarfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
BASELINE = "HEAD"
PATTERNS = {
    "private_key_header": rb"-----BEGIN (?:RSA |EC |OPENSSH |DSA |ENCRYPTED )?PRIVATE KEY-----",
    "github_token": rb"(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{50,})",
    "gitlab_token": rb"glpat-[A-Za-z0-9_-]{20,}",
    "aws_access_key_id": rb"(?:AKIA|ASIA)[0-9A-Z]{16}",
    "google_api_key": rb"AIza[0-9A-Za-z_-]{30,}",
    "openai_key_shape": rb"(?<![A-Za-z0-9_])sk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{40,}",
    "slack_token": rb"xox[baprs]-[A-Za-z0-9-]{20,}",
    "url_embedded_password": rb"https?://[^\s/:@\"']+:[^\s/@\"']+@",
    "literal_credential_assignment": rb"(?i)\b(?:api[_-]?key|access[_-]?token|client[_-]?secret|secret[_-]?key|password)\b\s*[:=]\s*[\"']([A-Za-z0-9_+/=-]{16,})[\"']",
}
COMPILED = {name: re.compile(pattern) for name, pattern in PATTERNS.items()}
HOME = re.compile(
    rb"(?:[A-Za-z]:\\{1,8}Users\\{1,8}[^\\\s\"/]+|/(?:Users|home)/[^/\s\"']+)"
)
EMAIL = re.compile(rb"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PRIVATE_NAMES = {
    ".env",
    "id_rsa",
    "id_ed25519",
    "credentials.json",
    "credentials",
    ".netrc",
    ".npmrc",
    ".pypirc",
}


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def scan(data):
    """Return only categories/counts. No matched value is returned."""
    return {
        "credential_patterns": {
            name: len(pattern.findall(data))
            for name, pattern in COMPILED.items()
            if pattern.search(data)
        },
        "home_path_present": bool(HOME.search(data)),
        "email_occurrences": len(EMAIL.findall(data)),
    }


def archive_members(data, name):
    if name.endswith((".tar.gz", ".tgz", ".tar")):
        with tarfile.open(fileobj=io.BytesIO(data), mode="r:*") as archive:
            for member in archive.getmembers():
                if member.isfile():
                    stream = archive.extractfile(member)
                    if stream:
                        yield member.name, stream.read()
    elif name.endswith(".zip"):
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            for member in archive.infolist():
                if not member.is_dir():
                    yield member.filename, archive.read(member)


def read_exact(stream, size):
    data = bytearray()
    while len(data) < size:
        part = stream.read(size - len(data))
        if not part:
            raise ValueError("Git batch stream ended before the declared object size")
        data.extend(part)
    return bytes(data)


def run(output):
    if output.exists() or not output.resolve().is_relative_to(ROOT / "reports"):
        raise ValueError("Choose a new output directory under reports")
    output.mkdir(parents=True)
    baseline = git("rev-parse", BASELINE).decode().strip()
    tree = {}
    for item in git("ls-tree", "-r", "-z", baseline).split(b"\0"):
        if item:
            header, rawpath = item.split(b"\t", 1)
            mode, kind, oid = header.decode().split()
            tree[rawpath.decode("utf-8")] = {"mode": mode, "type": kind, "blob": oid}
    reachable_lines = git("rev-list", "--objects", "--all").decode("utf-8").splitlines()
    paths = {}
    reachable = set()
    for line in reachable_lines:
        parts = line.split(" ", 1)
        reachable.add(parts[0])
        if len(parts) == 2:
            paths.setdefault(parts[0], parts[1])
    for name, item in tree.items():
        paths.setdefault(item["blob"], name)
    metadata = [
        line.split()
        for line in git("cat-file", "--batch-all-objects", "--batch-check")
        .decode()
        .splitlines()
    ]
    objects = Counter(kind for oid, kind, size in metadata)
    findings, archives, object_results = [], [], {}
    process = subprocess.Popen(
        ["git", "cat-file", "--batch"],
        cwd=ROOT,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
    )
    try:
        for index, (oid, kind, rawsize) in enumerate(metadata, 1):
            process.stdin.write((oid + "\n").encode())
            process.stdin.flush()
            actual_oid, actual_kind, actual_size = (
                process.stdout.readline().decode().strip().split()
            )
            if (actual_oid, actual_kind, actual_size) != (oid, kind, rawsize):
                raise ValueError("Git batch metadata differs")
            data = read_exact(process.stdout, int(rawsize))
            if process.stdout.read(1) != b"\n":
                raise ValueError("Git batch object separator differs")
            result = scan(data)
            object_results[oid] = result
            name = paths.get(oid, f"<{kind} object>")
            if result["credential_patterns"]:
                findings.append(
                    {
                        "object": oid,
                        "example_path": name,
                        "reachable": oid in reachable,
                        **result,
                    }
                )
            if kind == "blob" and name.endswith((".tar.gz", ".tgz", ".tar", ".zip")):
                member_findings, members, notices = [], 0, []
                for member, content in archive_members(data, name):
                    members += 1
                    details = scan(content)
                    if details["credential_patterns"]:
                        member_findings.append({"member": member, **details})
                    if re.search(
                        r"(?:^|/)(?:LICENSE[^/]*|COPYING[^/]*|NOTICE[^/]*)$",
                        member,
                        re.I,
                    ):
                        notices.append(
                            {
                                "member": member,
                                "sha256": digest(content),
                                "bytes": len(content),
                            }
                        )
                archives.append(
                    {
                        "object": oid,
                        "example_path": name,
                        "reachable": oid in reachable,
                        "sha256": digest(data),
                        "file_members_scanned": members,
                        "findings": member_findings,
                        "license_notice_members": notices,
                    }
                )
            if index % 5000 == 0:
                print(f"Scanned {index}/{len(metadata)} stored Git objects", flush=True)
    finally:
        process.stdin.close()
        process.stdout.close()
        process.wait()
    current = []
    for name, item in tree.items():
        path = ROOT / name
        if item["type"] != "blob" or not path.is_file():
            raise ValueError("Unsupported tracked entry or missing file")
        data = path.read_bytes()
        current.append(
            {
                "path": name,
                "bytes": len(data),
                "sha256": digest(data),
                "baseline_blob": item["blob"],
                "private_filename": Path(name).name in PRIVATE_NAMES,
                **scan(data),
            }
        )
    identity_lines = (
        git("log", "--all", "--format=%H%x00%an%x00%ae%x00%cn%x00%ce%x00%aI%x00%cI")
        .decode("utf-8")
        .splitlines()
    )
    identities = [line.split("\0") for line in identity_lines]
    if any(len(row) != 7 for row in identities):
        raise ValueError("Unexpected commit metadata format")
    summary = {
        "baseline": baseline,
        "tracked_files_scanned": len(current),
        "tracked_bytes": sum(r["bytes"] for r in current),
        "largest_files": sorted(
            ({"path": r["path"], "bytes": r["bytes"]} for r in current),
            key=lambda r: r["bytes"],
            reverse=True,
        )[:10],
        "stored_git_objects_scanned": len(metadata),
        "objects_by_type": dict(objects),
        "reachable_objects": len(reachable),
        "unreachable_stored_objects": len(metadata) - len(reachable),
        "reachable_commits": len(identities),
        "commit_author_identities": len({tuple(r[1:3]) for r in identities}),
        "commit_committer_identities": len({tuple(r[3:5]) for r in identities}),
        "commit_identity_values_omitted": True,
        "commit_author_date_range": [
            min(r[5] for r in identities),
            max(r[5] for r in identities),
        ],
        "current_home_path_files": sum(r["home_path_present"] for r in current),
        "current_email_files": sum(r["email_occurrences"] > 0 for r in current),
        "stored_objects_with_home_paths": sum(
            r["home_path_present"] for r in object_results.values()
        ),
        "stored_objects_with_emails": sum(
            r["email_occurrences"] > 0 for r in object_results.values()
        ),
        "credential_candidate_objects": len(findings),
        "archive_objects_scanned": len(archives),
        "archive_members_scanned": sum(a["file_members_scanned"] for a in archives),
        "archive_credential_candidate_members": sum(
            len(a["findings"]) for a in archives
        ),
        "private_filename_candidates": [
            r["path"] for r in current if r["private_filename"]
        ],
        "runtime_or_cache_paths_tracked": [
            r["path"]
            for r in current
            if r["path"].startswith(
                (".venv/", "tmp/", ".pytest_cache/", ".ruff_cache/")
            )
        ],
        "scope": "All baseline tracked bytes and all stored Git objects, including unreachable objects; full regular member contents of recognized tar/zip archive blobs. Patterns are not a proof of absence of every secret or personal detail. No matched credential or email value is exported.",
        "git_version": git("--version").decode().strip(),
    }
    for name, value in (
        ("summary.json", summary),
        ("tracked_manifest.json", current),
        ("credential_candidates.json", findings),
        ("archive_inventory.json", archives),
    ):
        (output / name).write_bytes((json.dumps(value, indent=2) + "\n").encode())
    print(
        json.dumps(
            {
                k: summary[k]
                for k in (
                    "tracked_files_scanned",
                    "stored_git_objects_scanned",
                    "reachable_commits",
                    "credential_candidate_objects",
                    "archive_credential_candidate_members",
                    "current_home_path_files",
                )
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output", type=Path, default=ROOT / "reports/release-readiness/security"
    )
    args = parser.parse_args()
    run(args.output.resolve())
