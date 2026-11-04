"""Download checksum-pinned upstream archives into an ignored local cache."""

import argparse
import hashlib
import json
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parents[1]


def fetch(output):
    manifest = json.loads(
        (ROOT / "datasets/real_world/phase4/manifest.json").read_text(encoding="utf-8")
    )
    output.mkdir(parents=True, exist_ok=True)
    results = []
    for repository in manifest["repositories"]:
        url = repository["archive_url"]
        if not url.startswith("https://codeload.github.com/"):
            raise ValueError("Archive source must be the pinned GitHub codeload URL")
        target = output / Path(repository["archive"]).name
        if target.exists():
            data = target.read_bytes()
        else:
            request = urllib.request.Request(
                url, headers={"User-Agent": "research-reproduction"}
            )
            with urllib.request.urlopen(request, timeout=90) as response:
                data = response.read(32 * 1024 * 1024 + 1)
            if len(data) > 32 * 1024 * 1024:
                raise ValueError("Archive exceeds the download size limit")
        digest = hashlib.sha256(data).hexdigest()
        if digest != repository["archive_sha256"]:
            raise ValueError(
                f"Pinned archive checksum differs: {repository['repository']}"
            )
        if not target.exists():
            target.write_bytes(data)
        results.append({"repository": repository["repository"], "sha256": digest})
    print(json.dumps({"downloaded_or_verified": results}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "local/upstream-archives")
    fetch(parser.parse_args().output.resolve())
