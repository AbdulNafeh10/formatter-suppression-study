"""Deterministic factorial stress suite; no model calls or outcome-based search."""

from dataclasses import asdict, dataclass
import hashlib
from pathlib import Path

from .pipeline import ast_signature, save_json

SEED = 20261103
GENERATOR_VERSION = 1
MODES = (
    "none",
    "standalone_first",
    "specific_first",
    "blanket_first",
    "multicode_first",
    "specific_last",
    "blanket_last",
    "file_specific",
)


@dataclass(frozen=True)
class Template:
    name: str
    category: str
    rule: str
    source: str
    boundary: bool = False


TEMPLATES = (
    Template(
        "call_positional",
        "function_calls",
        "F821",
        "print(\n    missing_a,@FIRST@\n    missing_b,@LAST@\n)\n",
    ),
    Template(
        "call_keywords_long",
        "function_calls",
        "F821",
        'value = dict(\n    primary=missing_a,@FIRST@\n    secondary=missing_b,@LAST@\n    description="A deliberately long description that exceeds the common formatter line length when placed beside the other arguments",\n)\n',
    ),
    Template(
        "call_nested",
        "nested_expressions",
        "F821",
        "print(\n    tuple([missing_a]),@FIRST@\n    sorted([missing_b]),@LAST@\n)\n",
    ),
    Template(
        "list_short",
        "lists",
        "F821",
        "value = [missing_a,@FIRST@\n    missing_b]@LAST@\n",
    ),
    Template(
        "list_long",
        "lists",
        "F821",
        'value = [missing_a, "A long string intended to make the collection exceed eighty-eight columns when flattened",@FIRST@\n    missing_b, "Another long string maintaining the need for wrapping in the formatted collection"]@LAST@\n',
    ),
    Template(
        "tuple_plain",
        "tuples",
        "F821",
        "value = (missing_a,@FIRST@\n    missing_b)@LAST@\n",
    ),
    Template(
        "tuple_starred",
        "tuples",
        "F821",
        "value = (*missing_a,@FIRST@\n    missing_b,)@LAST@\n",
    ),
    Template(
        "dict_pairs",
        "dictionaries",
        "F821",
        'value = {"first": missing_a,@FIRST@\n    "second": missing_b}@LAST@\n',
    ),
    Template(
        "dict_unpacking",
        "dictionaries",
        "F821",
        "value = {**missing_a,@FIRST@\n    **missing_b}@LAST@\n",
    ),
    Template(
        "binary_short",
        "multiline_expressions",
        "F821",
        "value = (missing_a@FIRST@\n    + missing_b)@LAST@\n",
    ),
    Template(
        "binary_long",
        "long_expressions",
        "F821",
        'value = (\n    missing_a + "A deliberately long string operand intended to provoke line wrapping across the expression"@FIRST@\n    + missing_b + "A second deliberately long string operand making a single-line form impossible"@LAST@\n)\n',
    ),
    Template(
        "boolean_nested",
        "nested_expressions",
        "F821",
        "value = (missing_a and@FIRST@\n    (missing_b or False))@LAST@\n",
    ),
    Template(
        "conditional",
        "conditional_expressions",
        "F821",
        "value = (missing_a if True@FIRST@\n    else missing_b)@LAST@\n",
    ),
    Template(
        "list_comprehension",
        "comprehensions",
        "F821",
        "value = [\n    missing_a(item)@FIRST@\n    for item in missing_b@LAST@\n]\n",
    ),
    Template(
        "dict_comprehension",
        "comprehensions",
        "F821",
        "value = {\n    key: missing_a(key)@FIRST@\n    for key in missing_b@LAST@\n}\n",
    ),
    Template(
        "generator_expression",
        "comprehensions",
        "F821",
        "value = tuple(\n    missing_a(item)@FIRST@\n    for item in missing_b@LAST@\n)\n",
    ),
    Template(
        "function_defaults",
        "function_definitions",
        "F821",
        "def compute(\n    first=missing_a,@FIRST@\n    second=missing_b,@LAST@\n):\n    return first, second\n",
    ),
    Template(
        "function_locals",
        "function_definitions",
        "F841",
        "def compute():\n    first=1@FIRST@\n    second=2@LAST@\n    return None\n",
    ),
    Template(
        "import_multiple",
        "imports",
        "F401",
        "import os, sys@FIRST@\nimport math@LAST@\n",
    ),
    Template(
        "import_from",
        "imports",
        "F401",
        "from os import (\n    path,@FIRST@\n    getcwd,@LAST@\n)\n",
    ),
    Template(
        "semicolon_module",
        "multiple_statements",
        "F821",
        "first=missing_a; second=missing_b@FIRST@\nthird=missing_c@LAST@\n",
    ),
    Template(
        "semicolon_function",
        "multiple_statements",
        "F841",
        "def compute():\n    first=1; second=2@FIRST@\n    third=3@LAST@\n",
    ),
    Template(
        "nested_container",
        "nested_expressions",
        "F821",
        'value = {\n    "items": [missing_a],@FIRST@\n    "lookup": {"key": missing_b},@LAST@\n}\n',
    ),
    Template(
        "fstring_boundary",
        "oracle_boundaries",
        "F821",
        'text = f"{missing_a}"@FIRST@\nother = missing_b@LAST@\n',
        True,
    ),
    Template(
        "exception_binding_boundary",
        "oracle_boundaries",
        "F841",
        "def compute():\n    try:\n        1 / 0\n    except Exception as error:@FIRST@\n        pass\n    leftover=1@LAST@\n",
        True,
    ),
)


def render(template: Template, mode: str) -> str:
    if mode not in MODES:
        raise ValueError(f"Unknown treatment: {mode}")
    source = template.source
    if source.count("@FIRST@") != 1 or source.count("@LAST@") != 1:
        raise ValueError("Each template must specify exactly two directive sites")
    if mode == "standalone_first":
        lines = source.splitlines(keepends=True)
        for index, line in enumerate(lines):
            if "@FIRST@" in line:
                indent = line[: len(line) - len(line.lstrip())]
                lines.insert(index, f"{indent}# noqa: {template.rule}\n")
                break
        source = "".join(lines)
    first = last = ""
    if mode == "specific_first":
        first = f"  # noqa: {template.rule}"
    elif mode == "blanket_first":
        first = "  # noqa"
    elif mode == "multicode_first":
        first = "  # noqa: F401, F821, F841"
    elif mode == "specific_last":
        last = f"  # noqa: {template.rule}"
    elif mode == "blanket_last":
        last = "  # noqa"
    source = source.replace("@FIRST@", first).replace("@LAST@", last)
    if mode == "file_specific":
        source = f"# ruff: noqa: {template.rule}\n" + source
    return source


def write_dataset(output: Path, seed: int = SEED, templates=TEMPLATES) -> dict:
    """Save every candidate, including invalid/duplicate exclusions."""
    output = output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    (output / "cases").mkdir()
    specification = {
        "generator_version": GENERATOR_VERSION,
        "seed": seed,
        "seed_purpose": "execution ordering only; sources are deterministic",
        "modes": list(MODES),
        "templates": [asdict(t) for t in templates],
    }
    save_json(output / "specification.json", specification)
    cases, hashes = [], {}
    for index, template in enumerate(templates):
        for treatment_index, mode in enumerate(MODES):
            case_id = f"{template.name}--{mode}"
            source = render(template, mode)
            source_path = f"cases/{case_id}.py"
            (output / source_path).write_bytes(source.encode("utf-8"))
            checksum = hashlib.sha256(source.encode("utf-8")).hexdigest()
            error = duplicate = structure = None
            try:
                structure = hashlib.sha256(
                    ast_signature(source).encode("utf-8")
                ).hexdigest()
            except (SyntaxError, ValueError) as exc:
                error = f"{type(exc).__name__}: {exc}"
            if checksum in hashes:
                duplicate = hashes[checksum]
            else:
                hashes[checksum] = case_id
            cases.append(
                {
                    "case_id": case_id,
                    "source": source_path,
                    "input_sha256": checksum,
                    "input_structure_sha256": structure,
                    "input_family": template.name,
                    "syntax_category": template.category,
                    "primary_rule": template.rule,
                    "suppression_type": (
                        "none"
                        if mode == "none"
                        else (
                            "standalone"
                            if mode == "standalone_first"
                            else (
                                "blanket"
                                if mode.startswith("blanket")
                                else (
                                    "multicode"
                                    if mode == "multicode_first"
                                    else (
                                        "file_specific"
                                        if mode == "file_specific"
                                        else "specific"
                                    )
                                )
                            )
                        )
                    ),
                    "directive_placement": mode,
                    "syntax_valid": error is None,
                    "accepted": error is None and duplicate is None,
                    "syntax_error": error,
                    "duplicate_of": duplicate,
                    "known_oracle_boundary": template.boundary,
                    "ai_assisted": True,
                    "generation_seed": seed,
                    "generation_method": "AI-authored factorial templates; deterministic rendering",
                    "reproduction_selected": treatment_index == index % len(MODES),
                }
            )
    order = sorted(
        (case["case_id"] for case in cases),
        key=lambda case_id: hashlib.sha256(f"{seed}:{case_id}".encode()).hexdigest(),
    )
    manifest = {
        "schema_version": 1,
        "dataset_origin": "phase3-controlled-factorial",
        "generator_version": GENERATOR_VERSION,
        "seed": seed,
        "specification_sha256": hashlib.sha256(
            (output / "specification.json").read_bytes()
        ).hexdigest(),
        "planned_candidates": len(templates) * len(MODES),
        "execution_order": order,
        "cases": cases,
    }
    save_json(output / "manifest.json", manifest)
    return manifest
