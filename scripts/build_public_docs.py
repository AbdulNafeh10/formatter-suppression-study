"""Bind the public drafts to saved evidence, keeping the original report separate."""

import argparse
from collections import Counter
import json
import re

from build_report import ROOT, TOKEN, digest, resolve

DOCUMENTS = {
    "README.md": "report/README_public.template.md",
    "report/research_report_public.md": "report/research_report_public.template.md",
}


def extracted_facts():
    paths = [
        "datasets/controlled/phase3/manifest.json",
        "datasets/real_world/phase4/manifest.json",
        "datasets/results/phase4/results.jsonl",
        "datasets/results/phase4/native_results.jsonl",
        "reports/ambiguous-audit/review_manifest.json",
    ]
    raw = {name: (ROOT / name).read_bytes() for name in paths}
    controlled, natural = [json.loads(raw[name]) for name in paths[:2]]
    primary, native = [
        [json.loads(line) for line in raw[name].splitlines()] for name in paths[2:4]
    ]
    review = json.loads(raw[paths[4]])
    baseline = {r["case_id"]: r for r in primary if r["formatter"] == "black"}
    facts = {
        "families": len({r["input_family"] for r in controlled["cases"]}),
        "modes": len({r["directive_placement"] for r in controlled["cases"]}),
        "natural_files": len(natural["cases"]),
        "natural_comparisons": len(primary),
        "natural_unchanged": sum(not r["formatting_changed"] for r in primary),
        "natural_changed": sum(r["formatting_changed"] for r in primary),
        "natural_ast_exclusions": sum(
            r["classification"] == "AST changed" for r in primary
        ),
        "zero_files": sum(
            not r["passes"]["B_original_underlying"] for r in baseline.values()
        ),
        "zero_comparisons": sum(
            not r["passes"]["B_original_underlying"] for r in primary
        ),
        "native_completed": sum(
            r["validation_status"] == "measurement_complete" for r in native
        ),
        "native_missing": sum(
            r["validation_status"] == "no_project_ruff_config" for r in native
        ),
        "reviewed_comparisons": len(review),
        "fstring_comparisons": sum(
            r["case_id"].startswith("fstring_boundary--") for r in review
        ),
        "exception_comparisons": sum(
            r["case_id"].startswith("exception_binding_boundary--") for r in review
        ),
    }
    if Counter(r["classification"] for r in primary) != {
        "Preserved": 76,
        "AST changed": 4,
    }:
        raise ValueError("Natural results differ from the approved record")
    return {
        "facts": facts,
        "source_sha256": {name: digest(data) for name, data in raw.items()},
    }


def build(check=False):
    facts = extracted_facts()
    facts_path = ROOT / "reports/publication-phase-b/public_facts.json"
    facts_text = json.dumps(facts, indent=2) + "\n"
    if check:
        if facts_path.read_bytes() != facts_text.encode():
            raise ValueError("Public fact extraction is stale")
    else:
        facts_path.parent.mkdir(parents=True, exist_ok=True)
        facts_path.write_bytes(facts_text.encode())
    spec = json.loads((ROOT / "report/public_claim_spec.json").read_bytes())
    templates = {
        name: (ROOT / template).read_text(encoding="utf-8")
        for name, template in DOCUMENTS.items()
    }
    keys = set().union(*(set(TOKEN.findall(s)) for s in templates.values()))
    if keys != set(spec):
        raise ValueError(f"Public claim keys differ: {keys.symmetric_difference(spec)}")
    ledger = {}
    for key, item in spec.items():
        text, value, source_hash = resolve(ROOT, item)
        ledger[key] = dict(item, value=value, rendered=text, source_sha256=source_hash)
    outputs, documents = {}, {}
    for name, template in templates.items():
        text = TOKEN.sub(lambda m: ledger[m[1]]["rendered"], template)
        if (
            "{{" in text
            or "}}" in text
            or not text.isascii()
            or re.search(r"\bwe\b", text, re.I)
        ):
            raise ValueError(
                "Public prose has an unresolved claim, non-ASCII typography or team voice"
            )
        outputs[name] = text
        documents[name] = {
            "template": DOCUMENTS[name],
            "template_sha256": digest(template.encode()),
            "sha256": digest(text.encode()),
        }
    readme_prose = re.sub(r"```.*?```", "", outputs["README.md"], flags=re.S)
    count = len(readme_prose.split())
    if not 400 <= count <= 650:
        raise ValueError(f"README prose length is outside target: {count}")
    for key, item in ledger.items():
        item["locations"] = {
            name: [
                i
                for i, line in enumerate(t.splitlines(), 1)
                if "{{" + key + "}}" in line
            ]
            for name, t in templates.items()
            if "{{" + key + "}}" in t
        }
    outputs["reports/publication-phase-b/public_claim_audit.json"] = (
        json.dumps(
            {
                "scope": "Bound numeric observations; protocol constants, references and prose are reviewed separately.",
                "readme_prose_words": count,
                "documents": documents,
                "claims": ledger,
            },
            indent=2,
        )
        + "\n"
    )
    for name, text in outputs.items():
        path = ROOT / name
        if check:
            if path.read_bytes() != text.encode():
                raise ValueError(f"Public draft or audit is stale: {name}")
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(text.encode())
    print(f"Verified {len(ledger)} public claim bindings; README prose: {count} words")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    build(args.check)
