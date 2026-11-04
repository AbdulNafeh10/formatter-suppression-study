"""Bind report claims to retained JSON evidence; verify without changing evidence."""

import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOKEN = re.compile(r"\{\{([A-Z0-9_]+)\}\}")


def digest(data):
    return hashlib.sha256(data).hexdigest()


def resolve(root, item):
    path = (root / item["source"]).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError("claim source escapes repository")
    raw = path.read_bytes()
    value = json.loads(raw)
    for part in item["pointer"]:
        value = value[part]
    operation = item.get("operation", "identity")
    if operation == "length":
        value = len(value)
    elif operation == "unique":
        value = len({row[item["field"]] for row in value})
    elif operation != "identity":
        raise ValueError(f"unsupported operation: {operation}")
    style = item.get("format", "text")
    if style == "pct2":
        rendered = f"{100 * value:.2f}"
    elif style == "pct1":
        rendered = f"{100 * value:.1f}"
    elif style == "int":
        if int(value) != value:
            raise ValueError("nonintegral integer claim")
        rendered = str(int(value))
    elif style == "text":
        rendered = str(value)
    else:
        raise ValueError(f"unsupported format: {style}")
    return rendered, value, digest(raw)


def build(root=ROOT, check=False):
    template = (root / "report/research_report.template.md").read_text(encoding="utf-8")
    spec = json.loads((root / "report/claim_spec.json").read_text(encoding="utf-8"))
    keys = set(TOKEN.findall(template))
    if keys != set(spec):
        raise ValueError(f"claim keys differ: {keys.symmetric_difference(spec)}")
    ledger = {}
    for key, item in spec.items():
        rendered, value, source_hash = resolve(root, item)
        ledger[key] = dict(
            item, value=value, rendered=rendered, source_sha256=source_hash
        )
    report = TOKEN.sub(lambda m: ledger[m[1]]["rendered"], template)
    if "{{" in report or "}}" in report:
        raise ValueError("unbound or malformed placeholder")
    for key in ledger:
        ledger[key]["template_lines"] = [
            i
            for i, line in enumerate(template.splitlines(), 1)
            if "{{" + key + "}}" in line
        ]
    audit = {
        "scope": "All templated measurements; prose meaning, bibliography, rule IDs and protocol constants require manual review.",
        "template_sha256": digest(template.encode()),
        "report_sha256": digest(report.encode()),
        "claims": ledger,
    }
    outputs = {
        "report/research_report.md": report,
        "reports/phase6/claim_audit.json": json.dumps(audit, indent=2) + "\n",
    }
    for name, content in outputs.items():
        path = root / name
        if check:
            if not path.exists() or path.read_bytes() != content.encode():
                raise ValueError(f"stale or changed output: {name}")
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content.encode())
    return len(ledger)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check", action="store_true", help="verify generated report and ledger"
    )
    args = parser.parse_args()
    print(f"Verified {build(check=args.check)} evidence-bound claims")
