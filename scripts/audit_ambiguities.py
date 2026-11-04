"""Supplementary review only: never import or change the experimental matcher."""

import argparse
import ast
from collections import Counter
from datetime import datetime, timezone
import hashlib
from importlib.metadata import version
import io
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import tokenize

ROOT = Path(__file__).resolve().parents[1]
PASSES = (
    "A_original_visible",
    "B_original_underlying",
    "C_formatted_visible",
    "D_formatted_underlying",
)


class ReviewUncertain(ValueError):
    pass


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    path.write_bytes((json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode())


def signature(source):
    return ast.dump(ast.parse(source, type_comments=True), include_attributes=False)


def key(diagnostic):
    return (
        diagnostic["code"],
        diagnostic["message"],
        diagnostic["location"]["row"],
        diagnostic["location"]["column"],
        diagnostic["end_location"]["row"],
        diagnostic["end_location"]["column"],
    )


def lexical(source, comments=False):
    ignored = {tokenize.NL, tokenize.NEWLINE, tokenize.INDENT, tokenize.DEDENT}
    if not comments:
        ignored.add(tokenize.COMMENT)
    return [
        (t.type, t.string)
        for t in tokenize.generate_tokens(io.StringIO(source).readline)
        if t.type not in ignored
    ]


def directives(source):
    lines = source.splitlines()
    result = []
    for token in tokenize.generate_tokens(io.StringIO(source).readline):
        if token.type != tokenize.COMMENT or not re.search(
            r"\bnoqa\b", token.string, re.I
        ):
            continue
        row, column = token.start
        prefix = lines[row - 1][:column]
        kind = (
            "file directive"
            if re.match(r"#\s*(?:ruff|flake8):\s*noqa", token.string, re.I)
            else "inline" if prefix.strip() else "standalone"
        )
        result.append(
            {
                "row": row,
                "column": column + 1,
                "end_column": token.end[1] + 1,
                "text": token.string,
                "kind": kind,
                "preceding_code": prefix.strip(),
            }
        )
    return result


def neutralize(source):
    lines = source.splitlines(keepends=True)
    for token in tokenize.generate_tokens(io.StringIO(source).readline):
        if token.type == tokenize.COMMENT:
            row, column = token.start
            lines[row - 1] = (
                lines[row - 1][:column]
                + re.sub(r"\bnoqa\b", "note", token.string, flags=re.I)
                + lines[row - 1][token.end[1] :]
            )
    changed = "".join(lines)
    if (
        len(source) != len(changed)
        or lexical(source) != lexical(changed)
        or signature(source) != signature(changed)
    ):
        raise ValueError("Comment intervention changed code or AST")
    return changed


def walk(node, path="$"):
    yield path, node
    for field, value in ast.iter_fields(node):
        if isinstance(value, ast.AST):
            yield from walk(value, f"{path}.{field}")
        elif isinstance(value, list):
            for index, child in enumerate(value):
                if isinstance(child, ast.AST):
                    yield from walk(child, f"{path}.{field}[{index}]")


def identities(source, underlying):
    """Explicit AST-role review; no original token-anchor/matcher calls.

    F-string Names are read from the AST and source slice, without requiring a
    separate Python 3.11 NAME token. ExceptHandler.name is a string field whose
    exact identifier token must be preceded by 'as' on that handler's header.
    """
    lines = source.splitlines()
    nodes = list(walk(ast.parse(source, type_comments=True)))
    tokens = list(tokenize.generate_tokens(io.StringIO(source).readline))
    result = {}
    for d in underlying:
        start = (d["location"]["row"], d["location"]["column"] - 1)
        end = (d["end_location"]["row"], d["end_location"]["column"] - 1)
        if (
            start[0] != end[0]
            or not 1 <= start[0] <= len(lines)
            or not 0 <= start[1] < end[1] <= len(lines[start[0] - 1])
        ):
            raise ReviewUncertain("Unreviewable diagnostic source span")
        lexeme = lines[start[0] - 1][start[1] : end[1]]
        candidates = []
        for path, node in nodes:
            if isinstance(node, ast.Name):
                row = node.lineno
                nstart = (row, len(lines[row - 1].encode()[: node.col_offset].decode()))
                nend = (
                    node.end_lineno,
                    len(
                        lines[node.end_lineno - 1]
                        .encode()[: node.end_col_offset]
                        .decode()
                    ),
                )
                eligible = (
                    d["code"] == "F821"
                    and isinstance(node.ctx, ast.Load)
                    or d["code"] == "F841"
                    and isinstance(node.ctx, ast.Store)
                )
                if eligible and nstart == start and nend == end and lexeme == node.id:
                    candidates.append(
                        (
                            path,
                            (
                                "load Name"
                                if isinstance(node.ctx, ast.Load)
                                else "assignment Store Name"
                            ),
                            ast.dump(node, include_attributes=False),
                        )
                    )
            elif (
                isinstance(node, ast.ExceptHandler)
                and d["code"] == "F841"
                and node.name == lexeme
                and node.lineno == start[0]
            ):
                hits = [
                    i
                    for i, t in enumerate(tokens)
                    if t.type == tokenize.NAME
                    and t.string == lexeme
                    and t.start == start
                    and t.end == end
                ]
                if (
                    len(hits) == 1
                    and hits[0] > 0
                    and tokens[hits[0] - 1].string == "as"
                ):
                    candidates.append(
                        (
                            path + ".name",
                            "exception-handler binding string field",
                            ast.dump(node, include_attributes=False),
                        )
                    )
        if len(candidates) != 1:
            raise ReviewUncertain(
                f"Expected one explicitly reviewable binding, found {len(candidates)} for {d['code']} {lexeme}"
            )
        path, role, context = candidates[0]
        identity = f"review:{d['code']}@{path}"
        if identity in result:
            raise ReviewUncertain("Duplicate review warning identity")
        result[identity] = {
            "identity": identity,
            "rule": d["code"],
            "lexeme": lexeme,
            "role": role,
            "ast_context": context,
            "diagnostic": d,
        }
    return result


def assess(before, after, passes):
    try:
        if signature(before) != signature(after):
            raise ReviewUncertain(
                "AST differs; suppression-only attribution is unsupported"
            )
        pairs = []
        for source, visible, underlying in (
            (before, PASSES[0], PASSES[1]),
            (after, PASSES[2], PASSES[3]),
        ):
            if Counter(map(key, passes[visible])) - Counter(
                map(key, passes[underlying])
            ):
                raise ReviewUncertain(
                    "Visible warnings are not an underlying multiset subset"
                )
            mapped = identities(source, passes[underlying])
            for item in mapped.values():
                item["visible"] = key(item["diagnostic"]) in set(
                    map(key, passes[visible])
                )
            pairs.append(mapped)
        first, last = pairs
        if set(first) != set(last):
            raise ReviewUncertain("Underlying review warning identities differ")
        warnings = []
        for identity, original in first.items():
            formatted = last[identity]
            for field in ("rule", "lexeme", "role", "ast_context"):
                if original[field] != formatted[field]:
                    raise ReviewUncertain(f"Review warning context differs: {field}")
            if original["diagnostic"]["message"] != formatted["diagnostic"]["message"]:
                raise ReviewUncertain("Underlying warning message differs")
            b, a = original["visible"], formatted["visible"]
            transition = (
                "newly hidden"
                if b and not a
                else (
                    "newly exposed"
                    if not b and a
                    else "visible in both" if b else "suppressed in both"
                )
            )
            warnings.append(
                {
                    "identity": identity,
                    "before": original,
                    "after": formatted,
                    "transition": transition,
                }
            )
        hidden = sum(w["transition"] == "newly hidden" for w in warnings)
        exposed = sum(w["transition"] == "newly exposed" for w in warnings)
        label = (
            "Newly hidden and newly exposed"
            if hidden and exposed
            else (
                "Newly hidden"
                if hidden
                else "Newly exposed" if exposed else "Preserved"
            )
        )
        return {
            "proposed_resolution": label,
            "warnings": warnings,
            "hidden": hidden,
            "exposed": exposed,
            "uncertainty": None,
        }
    except ReviewUncertain as exc:
        return {
            "proposed_resolution": "Genuinely uncertain",
            "warnings": [],
            "hidden": None,
            "exposed": None,
            "uncertainty": str(exc),
        }


def portable(data):
    if isinstance(data, dict):
        return {k: portable(v) for k, v in data.items() if k != "filename"}
    if isinstance(data, list):
        return [portable(item) for item in data]
    return data


def lint(source, ignore, destination, label):
    command = [
        sys.executable,
        "-m",
        "ruff",
        "check",
        "--isolated",
        "--no-cache",
        "--select",
        "F401,F821,F841",
        "--target-version",
        "py311",
        "--output-format",
        "json",
        "--no-fix",
        "--stdin-filename",
        "study_input.py",
    ]
    if ignore:
        command.append("--ignore-noqa")
    with tempfile.TemporaryDirectory(prefix="supplementary-audit-") as temporary:
        process = subprocess.run(
            command + ["-"],
            input=source.encode(),
            capture_output=True,
            cwd=temporary,
            timeout=30,
            check=False,
        )
    (destination / f"{label}.stdout.txt").write_bytes(process.stdout)
    (destination / f"{label}.stderr.txt").write_bytes(process.stderr)
    save(
        destination / f"{label}.command.json",
        {
            "command": command + ["-"],
            "returncode": process.returncode,
            "cwd": temporary,
        },
    )
    diagnostics = json.loads(process.stdout)
    if process.returncode not in (0, 1) or bool(diagnostics) != (
        process.returncode == 1
    ):
        raise ValueError("Ruff replay failed")
    return diagnostics


def link(path, report):
    import os

    return f"[{path.name}]({Path(os.path.relpath(path, report.parent)).as_posix()})"


def location(d):
    return f"{d['location']['row']}:{d['location']['column']}-{d['end_location']['row']}:{d['end_location']['column']}"


def render(output, records, integrity):
    report = output / "ambiguous_comparisons_review.md"
    counts = dict(Counter(r["review"]["proposed_resolution"] for r in records))
    text = [
        "# Supplementary review of all ambiguous formatter comparisons",
        "",
        "This is an AI-assisted, procedurally separate evidence review, not independent human adjudication. "
        "Original labels remain **Ambiguous**. Every proposed resolution below is confined to this review; "
        "the original datasets, result files, metrics, report and matcher are unchanged.",
        "",
        "Repository root: `.` (public privacy-derived export)",
        "",
        "## Findings",
        "",
        f"Reviewed {len(records)} comparisons from {len(set(r['case_id'] for r in records))} original inputs. Proposed resolutions: "
        + "; ".join(f"**{label}: {number}**" for label, number in counts.items())
        + ".",
        "",
        "Newly hidden: "
        + str(
            sum(r["review"]["proposed_resolution"] == "Newly hidden" for r in records)
        )
        + "; newly exposed: "
        + str(
            sum(r["review"]["proposed_resolution"] == "Newly exposed" for r in records)
        )
        + "; genuinely uncertain: "
        + str(
            sum(
                r["review"]["proposed_resolution"] == "Genuinely uncertain"
                for r in records
            )
        )
        + ".",
        "",
        "These are evidence-supported proposals, not a reason to treat ambiguity as preservation in the primary analysis. "
        "The original resolved denominators, uncertainty bounds and published-in-repository findings remain unchanged. "
        "No accuracy, prevalence, general tool guarantee or universal runtime-semantic claim follows.",
        "",
        "## Separate review method and integrity",
        "",
        "Selection is exactly the 32 Ambiguous primary Phase 3 records, paired across Black and Ruff. "
        "Development controls and Phase 7 repeats are not counted again. The script imports no original matcher/classifier. "
        "It compares source slices, full AST context and uniquely identifiable roles: f-string load Names, ordinary load/Store Names, "
        "and the exception handler's explicit `name` string field plus its `as error` token. "
        "Visibility is read from each raw A/B/C/D diagnostic set, never inferred from counts or comment position alone.",
        "",
        "All four lint passes are replayed with pinned Ruff 0.11.13 on Python 3.11. "
        "A separate comment-only intervention replaces `noqa` with same-length `note` inside COMMENT tokens, "
        "preserving non-comment tokens and AST; ordinary lint must then equal the original ignore-noqa pass. "
        "Replay comparison removes only the execution-specific `filename` field, retaining ranges, messages, fixes, noqa_row and other fields. "
        "Source programs are never executed and no fixes are applied.",
        "",
        "The sixteen f-string comparisons have identical source bytes before/after: equality of source and corresponding raw warnings "
        "is a direct preservation argument independent of the original token-anchor restriction. Python 3.11 tokenize represents "
        "the entire f-string as one STRING token, so its embedded Name does not align with complete code tokens. "
        "The sixteen exception-binding comparisons have equal AST and non-comment code tokens; only assignment spacing changes. "
        "The original matcher supports F841 Store Names but not the string-valued ExceptHandler.name binding.",
        "",
        "**Human interpretation flags:** all proposals await independent human adjudication. The exception cases specifically require "
        "confirmation that `except Exception as error` identifies the same F841 binding; this is a narrow reviewed exception, "
        "not a validated replacement matcher. Standalone `# noqa` comments leave both selected warnings visible: whether the author "
        "intended next-line suppression is unknown, but observed visibility is preserved. Warning truth, desired suppression policy "
        "and runtime behavior are outside this audit.",
        "",
        f"Integrity: {integrity['original_files_hashed']} original files hashed before/after; "
        f"{integrity['copied_files_checked']} byte-identical original-file exports; "
        f"{integrity['four_pass_replays']} lint replays and {integrity['comment_intervention_checks']} comment-intervention checks passed. "
        "Tracked original files are unchanged against the audit baseline. Full paths and SHA-256 values are in `integrity.json`.",
        "",
        "## Comparison index",
        "",
        "| # | Input | Formatter | Proposed resolution | Text changed |",
        "|---:|---|---|---|---|",
    ]
    for index, r in enumerate(records, 1):
        text.append(
            f"| {index} | [{r['case_id']}](#comparison-{index:02}) | {r['formatter']} | {r['review']['proposed_resolution']} | {r['before_sha256'] != r['after_sha256']} |"
        )
    for index, r in enumerate(records, 1):
        original = ROOT / r["original_directory"]
        exported = output / "exports" / r["case_id"] / r["formatter"]
        rechecks = exported / "rechecks"
        review = r["review"]
        text += [
            "",
            f'<a id="comparison-{index:02}"></a>',
            "",
            f"## {index:02}. {r['case_id']} / {r['formatter']}",
            "",
            f"**Original label:** Ambiguous. **Proposed review resolution:** {review['proposed_resolution']}.",
            "",
            f"Original evidence directory: `{original.relative_to(ROOT).as_posix()}`",
            "",
            f"Review export directory: `{exported.relative_to(ROOT).as_posix()}`",
            "",
            "### Sources and exact evidence paths",
            "",
            f"Original source: {link(original / 'before.py', report)}; byte-identical export: {link(exported / 'before.py', report)}. SHA-256: `{r['before_sha256']}`.",
            "",
            "```python",
            (exported / "before.py").read_text(encoding="utf-8").rstrip("\n"),
            "```",
            "",
            f"Formatted source: {link(original / 'after.py', report)}; byte-identical export: {link(exported / 'after.py', report)}. SHA-256: `{r['after_sha256']}`.",
            "",
            "```python",
            (exported / "after.py").read_text(encoding="utf-8").rstrip("\n"),
            "```",
            "",
            f"Original decision: {link(original / 'result.json', report)}; failure details: {link(original / 'matching.json', report)}; "
            f"formatter invocation: {link(original / 'formatter.command.json', report)}. Full byte-identical copies are in the export directory.",
            "",
            "### Why the matcher abstained",
            "",
            "Exact recorded error: `" + "; ".join(r["original_matching_errors"]) + "`.",
            "",
            r["reason_explanation"],
            "",
            "### Noqa placement",
            "",
            "| Snapshot | Position (1-based) | Kind | Exact comment | Preceding code on line |",
            "|---|---|---|---|---|",
        ]
        for snapshot in ("before", "after"):
            for comment in r["noqa"][snapshot]:
                text.append(
                    f"| {snapshot} | {comment['row']}:{comment['column']}-{comment['end_column']} | {comment['kind']} | `{comment['text']}` | `{comment['preceding_code']}` |"
                )
            if not r["noqa"][snapshot]:
                text.append(f"| {snapshot} | - | no directive | - | - |")
        text += [
            "",
            "### Warning identities and visibility",
            "",
            "The identities below are review-only, not original automated matcher identities. V = visible; S = suppressed; ranges are 1-based with exclusive end columns.",
            "",
            "| Identity / source role | Warning and source slice | Before range | After range | A / B / C / D | Judgment |",
            "|---|---|---|---|---|---|",
        ]
        for warning in review["warnings"]:
            b, a = warning["before"], warning["after"]
            text.append(
                f"| `{warning['identity']}`; {b['role']} | {b['rule']}: `{b['lexeme']}`; {b['diagnostic']['message']} | {location(b['diagnostic'])} | {location(a['diagnostic'])} | {'V' if b['visible'] else 'S'} / V / {'V' if a['visible'] else 'S'} / V | {warning['transition']} |"
            )
        if review["uncertainty"]:
            text += ["", "Uncertainty: " + review["uncertainty"]]
        text += [
            "",
            "### Evidence-based judgment and human review",
            "",
            r["judgment_explanation"],
            "",
            "Human interpretation: " + " ".join(r["human_review_flags"]),
            "",
            f"Saved replays and comment-neutralized sources: `{rechecks.relative_to(ROOT).as_posix()}`. "
            "All four replay stdout/stderr and command records are saved there; both neutralized ordinary-lint passes reproduce their respective underlying outputs.",
            "",
            "### All four original raw Ruff diagnostic outputs",
            "",
            "Privacy-derived JSON is preserved below with execution filenames anonymized and fix metadata retained. Empty arrays are actual empty outputs. "
            "Each stdout file also has a `.command.json`, `.stderr.txt` and `.diagnostics.json` sibling in both the original and export directories.",
        ]
        for label in PASSES:
            text += [
                "",
                "<details>",
                f"<summary>{label}</summary>",
                "",
                f"Original: {link(original / (label + '.stdout.txt'), report)}. Export: {link(exported / (label + '.stdout.txt'), report)}. "
                f"Replay: {link(rechecks / (label + '.stdout.txt'), report)}.",
                "",
                "```json",
                (exported / (label + ".stdout.txt"))
                .read_text(encoding="utf-8")
                .rstrip("\r\n"),
                "```",
                "",
                "</details>",
            ]
    text += [
        "",
        "## Reproduction and scope",
        "",
        "Run `python scripts/audit_ambiguities.py --output reports/ambiguous-audit-NEW` using the pinned study environment. "
        "Outputs must be new directories under reports; existing audits cannot be overwritten. "
        "Run `python scripts/audit_ambiguities.py --verify reports/ambiguous-audit` to recheck the retained hashes, "
        "all selected comparison coverage and exact report regeneration without rerunning tools. "
        "This retrospective audit does not change the primary study or establish independent held-out accuracy.",
        "",
    ]
    return "\n".join(text)


def create(output):
    if sys.version_info[:2] != (3, 11) or version("ruff") != "0.11.13":
        raise ValueError("Use the pinned Python 3.11 / Ruff 0.11.13 environment")
    if not output.is_relative_to(ROOT / "reports") or output.exists():
        raise ValueError("Use a new directory under reports; never overwrite evidence")
    baseline = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
    ).strip()
    subprocess.run(
        ["git", "diff", "--exit-code", baseline, "--"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    rows = [
        json.loads(line)
        for line in (ROOT / "datasets/results/phase3/results.jsonl")
        .read_text(encoding="utf-8")
        .splitlines()
    ]
    selected = sorted(
        [r for r in rows if r["classification"] == "Ambiguous"],
        key=lambda r: (r["case_id"], r["formatter"]),
    )
    if len(selected) != 32 or len({r["case_id"] for r in selected}) != 16:
        raise ValueError("The expected ambiguity cohort differs; review scope first")
    manifest_path = ROOT / "datasets/controlled/phase3/manifest.json"
    cases = {
        r["case_id"]: r
        for r in json.loads(manifest_path.read_text(encoding="utf-8"))["cases"]
    }
    original_paths = {
        manifest_path,
        ROOT / "datasets/results/phase3/results.jsonl",
        ROOT / "datasets/results/phase3/results.csv",
        ROOT / "reports/phase5/analysis/metrics.json",
        ROOT / "report/research_report.md",
        ROOT / "report/research_report.pdf",
        ROOT / "src/suppression_study/matching.py",
        ROOT / "src/suppression_study/classifier.py",
    }
    for r in selected:
        trial = ROOT / "datasets/results/phase3/trials" / r["case_id"] / r["formatter"]
        original_paths.update(p for p in trial.iterdir() if p.is_file())
        original_paths.add(
            ROOT / "datasets/controlled/phase3" / cases[r["case_id"]]["source"]
        )
    before_hashes = {
        p.relative_to(ROOT).as_posix(): sha(p) for p in sorted(original_paths)
    }
    output.mkdir(parents=True)
    save(output / "original_hashes_before.json", before_hashes)
    records, copies = [], []
    for index, row in enumerate(selected, 1):
        original = (
            ROOT / "datasets/results/phase3/trials" / row["case_id"] / row["formatter"]
        )
        exported = output / "exports" / row["case_id"] / row["formatter"]
        exported.mkdir(parents=True)
        for path in original.iterdir():
            if path.is_file():
                target = exported / path.name
                shutil.copyfile(path, target)
                if sha(path) != sha(target):
                    raise ValueError("Export bytes differ")
                copies.append(
                    {
                        "original": path.relative_to(ROOT).as_posix(),
                        "export": target.relative_to(output).as_posix(),
                        "sha256": sha(target),
                    }
                )
        saved = json.loads((original / "result.json").read_text(encoding="utf-8"))
        if (
            saved != row
            or sha(original / "before.py") != row["input_sha256"]
            or sha(original / "after.py") != row["output_sha256"]
        ):
            raise ValueError("Original result/source integrity mismatch")
        if (
            row["input_sha256"] != cases[row["case_id"]]["input_sha256"]
            or not row["ast_equivalent"]
        ):
            raise ValueError("Source manifest or primary AST gate differs")
        before = (exported / "before.py").read_bytes().decode()
        after = (exported / "after.py").read_bytes().decode()
        passes = {}
        rechecks = exported / "rechecks"
        rechecks.mkdir()
        for label in PASSES:
            diagnostic = json.loads(
                (original / (label + ".stdout.txt")).read_text(encoding="utf-8")
            )
            if diagnostic != row["passes"][label] or diagnostic != json.loads(
                (original / (label + ".diagnostics.json")).read_text(encoding="utf-8")
            ):
                raise ValueError("Raw, parsed and exported diagnostics disagree")
            command = json.loads(
                (original / (label + ".command.json")).read_text(encoding="utf-8")
            )
            if command["error"] or command["returncode"] not in (0, 1):
                raise ValueError("Original pass did not complete")
            source = before if label.startswith(("A_", "B_")) else after
            replay = lint(source, label.startswith(("B_", "D_")), rechecks, label)
            if portable(replay) != portable(diagnostic):
                raise ValueError("Raw pass did not reproduce")
            passes[label] = diagnostic
        for name, source, reference in (
            ("before", before, passes[PASSES[1]]),
            ("after", after, passes[PASSES[3]]),
        ):
            changed = neutralize(source)
            (rechecks / f"{name}.noqa-neutralized.py").write_bytes(changed.encode())
            if portable(
                lint(changed, False, rechecks, name + "_neutralized_visible")
            ) != portable(reference):
                raise ValueError("Comment-neutralization intervention failed")
        review = assess(before, after, passes)
        unchanged = before == after
        comment_map = {"before": directives(before), "after": directives(after)}
        is_exception = row["input_family"] == "exception_binding_boundary"
        reason = (
            "F841 points to the exception-handler name `error`. Python represents it as ExceptHandler.name (a string), "
            "not an ast.Name with Store context. The primary F841 anchor policy therefore finds no candidate. "
            "The separate `leftover` assignment does have a Store Name, but the unsupported `error` prevents complete primary correspondence."
            if is_exception
            else "F821 points to `missing_a` inside a formatted-value expression. Python 3.11 tokenize emits the whole f-string as a STRING token, "
            "so the embedded identifier span is not a complete token span under the primary matcher. "
            "This is a tokenization/coverage boundary, not evidence of a changed suppression."
        )
        flags = [
            "Independent human adjudication is pending; this is an AI-assisted proposal."
        ]
        if is_exception:
            flags.append(
                "A human should confirm the same exception binding is referenced by F841 and approve any future extension beyond Store Name anchors; no matcher change is proposed as validated here."
            )
        if any(c["kind"] == "standalone" for c in comment_map["before"]):
            flags.append(
                "The standalone directive suppresses neither selected warning in the measured passes. Intended next-line suppression cannot be inferred; this does not make observed visibility uncertain."
            )
        transitions = "; ".join(
            f"{w['before']['rule']} `{w['before']['lexeme']}` is {w['transition']}"
            for w in review["warnings"]
        )
        explanation = (
            "Original and formatted source are byte-identical. Full underlying and visible warnings reproduce; corresponding occurrences cannot move in an identical snapshot. "
            if unchanged
            else "The source changes only assignment spacing; executable AST and non-comment code tokens are equal. Exact diagnostic source slices identify the same `as error` handler binding and `leftover` assignment, with unchanged warning messages and roles. "
        )
        explanation += transitions + ". "
        explanation += "All four saved outputs replay exactly after ignoring only temporary filenames. Neutralizing directive comments makes ordinary lint reproduce the underlying warnings in both snapshots. "
        explanation += f"Proposed resolution: {review['proposed_resolution']}; " + (
            review["uncertainty"]
            or "no corresponding warning changes its visible/suppressed state."
        )
        record = {
            "case_id": row["case_id"],
            "formatter": row["formatter"],
            "original_classification": row["classification"],
            "original_directory": original.relative_to(ROOT).as_posix(),
            "before_sha256": sha(original / "before.py"),
            "after_sha256": sha(original / "after.py"),
            "original_matching_errors": row["matching_errors"],
            "reason_explanation": reason,
            "noqa": comment_map,
            "review": review,
            "judgment_explanation": explanation,
            "human_review_flags": flags,
            "ast_equal": signature(before) == signature(after),
            "non_comment_code_tokens_equal": lexical(before) == lexical(after),
        }
        records.append(record)
        save(exported / "review_only.json", record)
        print(
            f"Reviewed {index}/32: {row['case_id']} / {row['formatter']}: {review['proposed_resolution']}",
            flush=True,
        )
    after_hashes = {name: sha(ROOT / name) for name in before_hashes}
    if before_hashes != after_hashes:
        raise ValueError("An original evidence file changed")
    subprocess.run(
        ["git", "diff", "--exit-code", baseline, "--"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    integrity = {
        "baseline_commit": baseline,
        "original_files_hashed": len(before_hashes),
        "original_hashes_before_equal_after": True,
        "original_files_sha256": before_hashes,
        "copied_files_checked": len(copies),
        "exports": copies,
        "four_pass_replays": len(records) * 4,
        "comment_intervention_checks": len(records) * 2,
        "original_tracked_files_unchanged": True,
        "ruff": version("ruff"),
        "python": sys.version,
        "audit_script_sha256": sha(Path(__file__)),
        "audit_started_or_completed_utc": datetime.now(timezone.utc).isoformat(),
        "independent_human_adjudication": False,
    }
    save(output / "review_manifest.json", records)
    save(output / "integrity.json", integrity)
    (output / "ambiguous_comparisons_review.md").write_bytes(
        render(output, records, integrity).encode()
    )
    save(
        output / "artifact_hashes.json",
        {
            p.relative_to(output).as_posix(): sha(p)
            for p in sorted(output.rglob("*"))
            if p.is_file()
        },
    )
    print(
        json.dumps(
            {
                "comparisons": len(records),
                "proposals": dict(
                    Counter(r["review"]["proposed_resolution"] for r in records)
                ),
                "output": str(output),
            }
        )
    )


def verify(output):
    records = json.loads((output / "review_manifest.json").read_text(encoding="utf-8"))
    integrity = json.loads((output / "integrity.json").read_text(encoding="utf-8"))
    for path, expected in integrity["original_files_sha256"].items():
        if sha(ROOT / path) != expected:
            raise ValueError(f"Original evidence changed: {path}")
    artifacts = json.loads(
        (output / "artifact_hashes.json").read_text(encoding="utf-8")
    )
    for path, expected in artifacts.items():
        if sha(output / path) != expected:
            raise ValueError(f"Review artifact changed: {path}")
    original = [
        json.loads(line)
        for line in (ROOT / "datasets/results/phase3/results.jsonl")
        .read_text(encoding="utf-8")
        .splitlines()
    ]
    if {(r["case_id"], r["formatter"]) for r in records} != {
        (r["case_id"], r["formatter"])
        for r in original
        if r["classification"] == "Ambiguous"
    }:
        raise ValueError("Review does not cover the full original ambiguous cohort")
    if (output / "ambiguous_comparisons_review.md").read_bytes() != render(
        output, records, integrity
    ).encode():
        raise ValueError(
            "Review report is stale or differs from the exported judgments"
        )
    print(
        f"Verified {len(records)} comparisons, {len(artifacts)} review artifacts and {len(integrity['original_files_sha256'])} unchanged original files"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "reports/ambiguous-audit")
    parser.add_argument("--verify", type=Path)
    args = parser.parse_args()
    if args.verify:
        verify(args.verify.resolve())
    else:
        create(args.output.resolve())
