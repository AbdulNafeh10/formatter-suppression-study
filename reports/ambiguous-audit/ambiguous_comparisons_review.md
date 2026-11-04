# Supplementary review of all ambiguous formatter comparisons

This is an AI-assisted, procedurally separate evidence review, not independent human adjudication. Original labels remain **Ambiguous**. Every proposed resolution below is confined to this review; the original datasets, result files, metrics, report and matcher are unchanged.

Repository root: `.` (public privacy-derived export)

## Findings

Reviewed 32 comparisons from 16 original inputs. Proposed resolutions: **Preserved: 32**.

Newly hidden: 0; newly exposed: 0; genuinely uncertain: 0.

These are evidence-supported proposals, not a reason to treat ambiguity as preservation in the primary analysis. The original resolved denominators, uncertainty bounds and published-in-repository findings remain unchanged. No accuracy, prevalence, general tool guarantee or universal runtime-semantic claim follows.

## Separate review method and integrity

Selection is exactly the 32 Ambiguous primary Phase 3 records, paired across Black and Ruff. Development controls and Phase 7 repeats are not counted again. The script imports no original matcher/classifier. It compares source slices, full AST context and uniquely identifiable roles: f-string load Names, ordinary load/Store Names, and the exception handler's explicit `name` string field plus its `as error` token. Visibility is read from each raw A/B/C/D diagnostic set, never inferred from counts or comment position alone.

All four lint passes are replayed with pinned Ruff 0.11.13 on Python 3.11. A separate comment-only intervention replaces `noqa` with same-length `note` inside COMMENT tokens, preserving non-comment tokens and AST; ordinary lint must then equal the original ignore-noqa pass. Replay comparison removes only the execution-specific `filename` field, retaining ranges, messages, fixes, noqa_row and other fields. Source programs are never executed and no fixes are applied.

The sixteen f-string comparisons have identical source bytes before/after: equality of source and corresponding raw warnings is a direct preservation argument independent of the original token-anchor restriction. Python 3.11 tokenize represents the entire f-string as one STRING token, so its embedded Name does not align with complete code tokens. The sixteen exception-binding comparisons have equal AST and non-comment code tokens; only assignment spacing changes. The original matcher supports F841 Store Names but not the string-valued ExceptHandler.name binding.

**Human interpretation flags:** all proposals await independent human adjudication. The exception cases specifically require confirmation that `except Exception as error` identifies the same F841 binding; this is a narrow reviewed exception, not a validated replacement matcher. Standalone `# noqa` comments leave both selected warnings visible: whether the author intended next-line suppression is unknown, but observed visibility is preserved. Warning truth, desired suppression policy and runtime behavior are outside this audit.

Integrity: 840 original files hashed before/after; 816 byte-identical original-file exports; 128 lint replays and 64 comment-intervention checks passed. Tracked original files are unchanged against the audit baseline. Full paths and SHA-256 values are in `integrity.json`.

## Comparison index

| # | Input | Formatter | Proposed resolution | Text changed |
|---:|---|---|---|---|
| 1 | [exception_binding_boundary--blanket_first](#comparison-01) | black | Preserved | True |
| 2 | [exception_binding_boundary--blanket_first](#comparison-02) | ruff | Preserved | True |
| 3 | [exception_binding_boundary--blanket_last](#comparison-03) | black | Preserved | True |
| 4 | [exception_binding_boundary--blanket_last](#comparison-04) | ruff | Preserved | True |
| 5 | [exception_binding_boundary--file_specific](#comparison-05) | black | Preserved | True |
| 6 | [exception_binding_boundary--file_specific](#comparison-06) | ruff | Preserved | True |
| 7 | [exception_binding_boundary--multicode_first](#comparison-07) | black | Preserved | True |
| 8 | [exception_binding_boundary--multicode_first](#comparison-08) | ruff | Preserved | True |
| 9 | [exception_binding_boundary--none](#comparison-09) | black | Preserved | True |
| 10 | [exception_binding_boundary--none](#comparison-10) | ruff | Preserved | True |
| 11 | [exception_binding_boundary--specific_first](#comparison-11) | black | Preserved | True |
| 12 | [exception_binding_boundary--specific_first](#comparison-12) | ruff | Preserved | True |
| 13 | [exception_binding_boundary--specific_last](#comparison-13) | black | Preserved | True |
| 14 | [exception_binding_boundary--specific_last](#comparison-14) | ruff | Preserved | True |
| 15 | [exception_binding_boundary--standalone_first](#comparison-15) | black | Preserved | True |
| 16 | [exception_binding_boundary--standalone_first](#comparison-16) | ruff | Preserved | True |
| 17 | [fstring_boundary--blanket_first](#comparison-17) | black | Preserved | False |
| 18 | [fstring_boundary--blanket_first](#comparison-18) | ruff | Preserved | False |
| 19 | [fstring_boundary--blanket_last](#comparison-19) | black | Preserved | False |
| 20 | [fstring_boundary--blanket_last](#comparison-20) | ruff | Preserved | False |
| 21 | [fstring_boundary--file_specific](#comparison-21) | black | Preserved | False |
| 22 | [fstring_boundary--file_specific](#comparison-22) | ruff | Preserved | False |
| 23 | [fstring_boundary--multicode_first](#comparison-23) | black | Preserved | False |
| 24 | [fstring_boundary--multicode_first](#comparison-24) | ruff | Preserved | False |
| 25 | [fstring_boundary--none](#comparison-25) | black | Preserved | False |
| 26 | [fstring_boundary--none](#comparison-26) | ruff | Preserved | False |
| 27 | [fstring_boundary--specific_first](#comparison-27) | black | Preserved | False |
| 28 | [fstring_boundary--specific_first](#comparison-28) | ruff | Preserved | False |
| 29 | [fstring_boundary--specific_last](#comparison-29) | black | Preserved | False |
| 30 | [fstring_boundary--specific_last](#comparison-30) | ruff | Preserved | False |
| 31 | [fstring_boundary--standalone_first](#comparison-31) | black | Preserved | False |
| 32 | [fstring_boundary--standalone_first](#comparison-32) | ruff | Preserved | False |

<a id="comparison-01"></a>

## 01. exception_binding_boundary--blanket_first / black

**Original label:** Ambiguous. **Proposed review resolution:** Preserved.

Original evidence directory: `datasets/results/phase3/trials/exception_binding_boundary--blanket_first/black`

Review export directory: `reports/ambiguous-audit/exports/exception_binding_boundary--blanket_first/black`

### Sources and exact evidence paths

Original source: [before.py](../../datasets/results/phase3/trials/exception_binding_boundary--blanket_first/black/before.py); byte-identical export: [before.py](exports/exception_binding_boundary--blanket_first/black/before.py). SHA-256: `4464a1e240aa35ced76297c3085eeb24e2b9dc434d52f481ed69edd213459830`.

```python
def compute():
    try:
        1 / 0
    except Exception as error:  # noqa
        pass
    leftover=1
```

Formatted source: [after.py](../../datasets/results/phase3/trials/exception_binding_boundary--blanket_first/black/after.py); byte-identical export: [after.py](exports/exception_binding_boundary--blanket_first/black/after.py). SHA-256: `b4a1108e52cdb7b9c2342f811512685834eccbfdc177b10be62b687dc9ddf06e`.

```python
def compute():
    try:
        1 / 0
    except Exception as error:  # noqa
        pass
    leftover = 1
```

Original decision: [result.json](../../datasets/results/phase3/trials/exception_binding_boundary--blanket_first/black/result.json); failure details: [matching.json](../../datasets/results/phase3/trials/exception_binding_boundary--blanket_first/black/matching.json); formatter invocation: [formatter.command.json](../../datasets/results/phase3/trials/exception_binding_boundary--blanket_first/black/formatter.command.json). Full byte-identical copies are in the export directory.

### Why the matcher abstained

Exact recorded error: `Expected one relevant AST anchor, found 0`.

F841 points to the exception-handler name `error`. Python represents it as ExceptHandler.name (a string), not an ast.Name with Store context. The primary F841 anchor policy therefore finds no candidate. The separate `leftover` assignment does have a Store Name, but the unsupported `error` prevents complete primary correspondence.

### Noqa placement

| Snapshot | Position (1-based) | Kind | Exact comment | Preceding code on line |
|---|---|---|---|---|
| before | 4:33-39 | inline | `# noqa` | `except Exception as error:` |
| after | 4:33-39 | inline | `# noqa` | `except Exception as error:` |

### Warning identities and visibility

The identities below are review-only, not original automated matcher identities. V = visible; S = suppressed; ranges are 1-based with exclusive end columns.

| Identity / source role | Warning and source slice | Before range | After range | A / B / C / D | Judgment |
|---|---|---|---|---|---|
| `review:F841@$.body[0].body[0].handlers[0].name`; exception-handler binding string field | F841: `error`; Local variable `error` is assigned to but never used | 4:25-4:30 | 4:25-4:30 | S / V / S / V | suppressed in both |
| `review:F841@$.body[0].body[1].targets[0]`; assignment Store Name | F841: `leftover`; Local variable `leftover` is assigned to but never used | 6:5-6:13 | 6:5-6:13 | V / V / V / V | visible in both |

### Evidence-based judgment and human review

The source changes only assignment spacing; executable AST and non-comment code tokens are equal. Exact diagnostic source slices identify the same `as error` handler binding and `leftover` assignment, with unchanged warning messages and roles. F841 `error` is suppressed in both; F841 `leftover` is visible in both. All four saved outputs replay exactly after ignoring only temporary filenames. Neutralizing directive comments makes ordinary lint reproduce the underlying warnings in both snapshots. Proposed resolution: Preserved; no corresponding warning changes its visible/suppressed state.

Human interpretation: Independent human adjudication is pending; this is an AI-assisted proposal. A human should confirm the same exception binding is referenced by F841 and approve any future extension beyond Store Name anchors; no matcher change is proposed as validated here.

Saved replays and comment-neutralized sources: `reports/ambiguous-audit/exports/exception_binding_boundary--blanket_first/black/rechecks`. All four replay stdout/stderr and command records are saved there; both neutralized ordinary-lint passes reproduce their respective underlying outputs.

### All four original raw Ruff diagnostic outputs

Privacy-derived JSON is preserved below with execution filenames anonymized and fix metadata retained. Empty arrays are actual empty outputs. Each stdout file also has a `.command.json`, `.stderr.txt` and `.diagnostics.json` sibling in both the original and export directories.

<details>
<summary>A_original_visible</summary>

Original: [A_original_visible.stdout.txt](../../datasets/results/phase3/trials/exception_binding_boundary--blanket_first/black/A_original_visible.stdout.txt). Export: [A_original_visible.stdout.txt](exports/exception_binding_boundary--blanket_first/black/A_original_visible.stdout.txt). Replay: [A_original_visible.stdout.txt](exports/exception_binding_boundary--blanket_first/black/rechecks/A_original_visible.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 13,
      "row": 6
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-hk3ls2z7\\study_input.py",
    "fix": {
      "applicability": "unsafe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 1,
            "row": 7
          },
          "location": {
            "column": 1,
            "row": 6
          }
        }
      ],
      "message": "Remove assignment to unused variable `leftover`"
    },
    "location": {
      "column": 5,
      "row": 6
    },
    "message": "Local variable `leftover` is assigned to but never used",
    "noqa_row": 6,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  }
]
```

</details>

<details>
<summary>B_original_underlying</summary>

Original: [B_original_underlying.stdout.txt](../../datasets/results/phase3/trials/exception_binding_boundary--blanket_first/black/B_original_underlying.stdout.txt). Export: [B_original_underlying.stdout.txt](exports/exception_binding_boundary--blanket_first/black/B_original_underlying.stdout.txt). Replay: [B_original_underlying.stdout.txt](exports/exception_binding_boundary--blanket_first/black/rechecks/B_original_underlying.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 30,
      "row": 4
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-lyice0i9\\study_input.py",
    "fix": {
      "applicability": "safe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 30,
            "row": 4
          },
          "location": {
            "column": 21,
            "row": 4
          }
        }
      ],
      "message": "Remove assignment to unused variable `error`"
    },
    "location": {
      "column": 25,
      "row": 4
    },
    "message": "Local variable `error` is assigned to but never used",
    "noqa_row": 4,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  },
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 13,
      "row": 6
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-lyice0i9\\study_input.py",
    "fix": {
      "applicability": "unsafe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 1,
            "row": 7
          },
          "location": {
            "column": 1,
            "row": 6
          }
        }
      ],
      "message": "Remove assignment to unused variable `leftover`"
    },
    "location": {
      "column": 5,
      "row": 6
    },
    "message": "Local variable `leftover` is assigned to but never used",
    "noqa_row": 6,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  }
]
```

</details>

<details>
<summary>C_formatted_visible</summary>

Original: [C_formatted_visible.stdout.txt](../../datasets/results/phase3/trials/exception_binding_boundary--blanket_first/black/C_formatted_visible.stdout.txt). Export: [C_formatted_visible.stdout.txt](exports/exception_binding_boundary--blanket_first/black/C_formatted_visible.stdout.txt). Replay: [C_formatted_visible.stdout.txt](exports/exception_binding_boundary--blanket_first/black/rechecks/C_formatted_visible.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 13,
      "row": 6
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-9ezf4hfn\\study_input.py",
    "fix": {
      "applicability": "unsafe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 1,
            "row": 7
          },
          "location": {
            "column": 1,
            "row": 6
          }
        }
      ],
      "message": "Remove assignment to unused variable `leftover`"
    },
    "location": {
      "column": 5,
      "row": 6
    },
    "message": "Local variable `leftover` is assigned to but never used",
    "noqa_row": 6,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  }
]
```

</details>

<details>
<summary>D_formatted_underlying</summary>

Original: [D_formatted_underlying.stdout.txt](../../datasets/results/phase3/trials/exception_binding_boundary--blanket_first/black/D_formatted_underlying.stdout.txt). Export: [D_formatted_underlying.stdout.txt](exports/exception_binding_boundary--blanket_first/black/D_formatted_underlying.stdout.txt). Replay: [D_formatted_underlying.stdout.txt](exports/exception_binding_boundary--blanket_first/black/rechecks/D_formatted_underlying.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 30,
      "row": 4
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-8um86_by\\study_input.py",
    "fix": {
      "applicability": "safe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 30,
            "row": 4
          },
          "location": {
            "column": 21,
            "row": 4
          }
        }
      ],
      "message": "Remove assignment to unused variable `error`"
    },
    "location": {
      "column": 25,
      "row": 4
    },
    "message": "Local variable `error` is assigned to but never used",
    "noqa_row": 4,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  },
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 13,
      "row": 6
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-8um86_by\\study_input.py",
    "fix": {
      "applicability": "unsafe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 1,
            "row": 7
          },
          "location": {
            "column": 1,
            "row": 6
          }
        }
      ],
      "message": "Remove assignment to unused variable `leftover`"
    },
    "location": {
      "column": 5,
      "row": 6
    },
    "message": "Local variable `leftover` is assigned to but never used",
    "noqa_row": 6,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  }
]
```

</details>

<a id="comparison-02"></a>

## 02. exception_binding_boundary--blanket_first / ruff

**Original label:** Ambiguous. **Proposed review resolution:** Preserved.

Original evidence directory: `datasets/results/phase3/trials/exception_binding_boundary--blanket_first/ruff`

Review export directory: `reports/ambiguous-audit/exports/exception_binding_boundary--blanket_first/ruff`

### Sources and exact evidence paths

Original source: [before.py](../../datasets/results/phase3/trials/exception_binding_boundary--blanket_first/ruff/before.py); byte-identical export: [before.py](exports/exception_binding_boundary--blanket_first/ruff/before.py). SHA-256: `4464a1e240aa35ced76297c3085eeb24e2b9dc434d52f481ed69edd213459830`.

```python
def compute():
    try:
        1 / 0
    except Exception as error:  # noqa
        pass
    leftover=1
```

Formatted source: [after.py](../../datasets/results/phase3/trials/exception_binding_boundary--blanket_first/ruff/after.py); byte-identical export: [after.py](exports/exception_binding_boundary--blanket_first/ruff/after.py). SHA-256: `b4a1108e52cdb7b9c2342f811512685834eccbfdc177b10be62b687dc9ddf06e`.

```python
def compute():
    try:
        1 / 0
    except Exception as error:  # noqa
        pass
    leftover = 1
```

Original decision: [result.json](../../datasets/results/phase3/trials/exception_binding_boundary--blanket_first/ruff/result.json); failure details: [matching.json](../../datasets/results/phase3/trials/exception_binding_boundary--blanket_first/ruff/matching.json); formatter invocation: [formatter.command.json](../../datasets/results/phase3/trials/exception_binding_boundary--blanket_first/ruff/formatter.command.json). Full byte-identical copies are in the export directory.

### Why the matcher abstained

Exact recorded error: `Expected one relevant AST anchor, found 0`.

F841 points to the exception-handler name `error`. Python represents it as ExceptHandler.name (a string), not an ast.Name with Store context. The primary F841 anchor policy therefore finds no candidate. The separate `leftover` assignment does have a Store Name, but the unsupported `error` prevents complete primary correspondence.

### Noqa placement

| Snapshot | Position (1-based) | Kind | Exact comment | Preceding code on line |
|---|---|---|---|---|
| before | 4:33-39 | inline | `# noqa` | `except Exception as error:` |
| after | 4:33-39 | inline | `# noqa` | `except Exception as error:` |

### Warning identities and visibility

The identities below are review-only, not original automated matcher identities. V = visible; S = suppressed; ranges are 1-based with exclusive end columns.

| Identity / source role | Warning and source slice | Before range | After range | A / B / C / D | Judgment |
|---|---|---|---|---|---|
| `review:F841@$.body[0].body[0].handlers[0].name`; exception-handler binding string field | F841: `error`; Local variable `error` is assigned to but never used | 4:25-4:30 | 4:25-4:30 | S / V / S / V | suppressed in both |
| `review:F841@$.body[0].body[1].targets[0]`; assignment Store Name | F841: `leftover`; Local variable `leftover` is assigned to but never used | 6:5-6:13 | 6:5-6:13 | V / V / V / V | visible in both |

### Evidence-based judgment and human review

The source changes only assignment spacing; executable AST and non-comment code tokens are equal. Exact diagnostic source slices identify the same `as error` handler binding and `leftover` assignment, with unchanged warning messages and roles. F841 `error` is suppressed in both; F841 `leftover` is visible in both. All four saved outputs replay exactly after ignoring only temporary filenames. Neutralizing directive comments makes ordinary lint reproduce the underlying warnings in both snapshots. Proposed resolution: Preserved; no corresponding warning changes its visible/suppressed state.

Human interpretation: Independent human adjudication is pending; this is an AI-assisted proposal. A human should confirm the same exception binding is referenced by F841 and approve any future extension beyond Store Name anchors; no matcher change is proposed as validated here.

Saved replays and comment-neutralized sources: `reports/ambiguous-audit/exports/exception_binding_boundary--blanket_first/ruff/rechecks`. All four replay stdout/stderr and command records are saved there; both neutralized ordinary-lint passes reproduce their respective underlying outputs.

### All four original raw Ruff diagnostic outputs

Privacy-derived JSON is preserved below with execution filenames anonymized and fix metadata retained. Empty arrays are actual empty outputs. Each stdout file also has a `.command.json`, `.stderr.txt` and `.diagnostics.json` sibling in both the original and export directories.

<details>
<summary>A_original_visible</summary>

Original: [A_original_visible.stdout.txt](../../datasets/results/phase3/trials/exception_binding_boundary--blanket_first/ruff/A_original_visible.stdout.txt). Export: [A_original_visible.stdout.txt](exports/exception_binding_boundary--blanket_first/ruff/A_original_visible.stdout.txt). Replay: [A_original_visible.stdout.txt](exports/exception_binding_boundary--blanket_first/ruff/rechecks/A_original_visible.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 13,
      "row": 6
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-v32wm5lg\\study_input.py",
    "fix": {
      "applicability": "unsafe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 1,
            "row": 7
          },
          "location": {
            "column": 1,
            "row": 6
          }
        }
      ],
      "message": "Remove assignment to unused variable `leftover`"
    },
    "location": {
      "column": 5,
      "row": 6
    },
    "message": "Local variable `leftover` is assigned to but never used",
    "noqa_row": 6,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  }
]
```

</details>

<details>
<summary>B_original_underlying</summary>

Original: [B_original_underlying.stdout.txt](../../datasets/results/phase3/trials/exception_binding_boundary--blanket_first/ruff/B_original_underlying.stdout.txt). Export: [B_original_underlying.stdout.txt](exports/exception_binding_boundary--blanket_first/ruff/B_original_underlying.stdout.txt). Replay: [B_original_underlying.stdout.txt](exports/exception_binding_boundary--blanket_first/ruff/rechecks/B_original_underlying.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 30,
      "row": 4
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-x8v6emd5\\study_input.py",
    "fix": {
      "applicability": "safe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 30,
            "row": 4
          },
          "location": {
            "column": 21,
            "row": 4
          }
        }
      ],
      "message": "Remove assignment to unused variable `error`"
    },
    "location": {
      "column": 25,
      "row": 4
    },
    "message": "Local variable `error` is assigned to but never used",
    "noqa_row": 4,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  },
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 13,
      "row": 6
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-x8v6emd5\\study_input.py",
    "fix": {
      "applicability": "unsafe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 1,
            "row": 7
          },
          "location": {
            "column": 1,
            "row": 6
          }
        }
      ],
      "message": "Remove assignment to unused variable `leftover`"
    },
    "location": {
      "column": 5,
      "row": 6
    },
    "message": "Local variable `leftover` is assigned to but never used",
    "noqa_row": 6,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  }
]
```

</details>

<details>
<summary>C_formatted_visible</summary>

Original: [C_formatted_visible.stdout.txt](../../datasets/results/phase3/trials/exception_binding_boundary--blanket_first/ruff/C_formatted_visible.stdout.txt). Export: [C_formatted_visible.stdout.txt](exports/exception_binding_boundary--blanket_first/ruff/C_formatted_visible.stdout.txt). Replay: [C_formatted_visible.stdout.txt](exports/exception_binding_boundary--blanket_first/ruff/rechecks/C_formatted_visible.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 13,
      "row": 6
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-6hzezv00\\study_input.py",
    "fix": {
      "applicability": "unsafe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 1,
            "row": 7
          },
          "location": {
            "column": 1,
            "row": 6
          }
        }
      ],
      "message": "Remove assignment to unused variable `leftover`"
    },
    "location": {
      "column": 5,
      "row": 6
    },
    "message": "Local variable `leftover` is assigned to but never used",
    "noqa_row": 6,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  }
]
```

</details>

<details>
<summary>D_formatted_underlying</summary>

Original: [D_formatted_underlying.stdout.txt](../../datasets/results/phase3/trials/exception_binding_boundary--blanket_first/ruff/D_formatted_underlying.stdout.txt). Export: [D_formatted_underlying.stdout.txt](exports/exception_binding_boundary--blanket_first/ruff/D_formatted_underlying.stdout.txt). Replay: [D_formatted_underlying.stdout.txt](exports/exception_binding_boundary--blanket_first/ruff/rechecks/D_formatted_underlying.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 30,
      "row": 4
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-hnihqfey\\study_input.py",
    "fix": {
      "applicability": "safe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 30,
            "row": 4
          },
          "location": {
            "column": 21,
            "row": 4
          }
        }
      ],
      "message": "Remove assignment to unused variable `error`"
    },
    "location": {
      "column": 25,
      "row": 4
    },
    "message": "Local variable `error` is assigned to but never used",
    "noqa_row": 4,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  },
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 13,
      "row": 6
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-hnihqfey\\study_input.py",
    "fix": {
      "applicability": "unsafe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 1,
            "row": 7
          },
          "location": {
            "column": 1,
            "row": 6
          }
        }
      ],
      "message": "Remove assignment to unused variable `leftover`"
    },
    "location": {
      "column": 5,
      "row": 6
    },
    "message": "Local variable `leftover` is assigned to but never used",
    "noqa_row": 6,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  }
]
```

</details>

<a id="comparison-03"></a>

## 03. exception_binding_boundary--blanket_last / black

**Original label:** Ambiguous. **Proposed review resolution:** Preserved.

Original evidence directory: `datasets/results/phase3/trials/exception_binding_boundary--blanket_last/black`

Review export directory: `reports/ambiguous-audit/exports/exception_binding_boundary--blanket_last/black`

### Sources and exact evidence paths

Original source: [before.py](../../datasets/results/phase3/trials/exception_binding_boundary--blanket_last/black/before.py); byte-identical export: [before.py](exports/exception_binding_boundary--blanket_last/black/before.py). SHA-256: `876969ab9eb8a96f1b8105921d542d30f1a30bed384434a048a9b1b3d319dade`.

```python
def compute():
    try:
        1 / 0
    except Exception as error:
        pass
    leftover=1  # noqa
```

Formatted source: [after.py](../../datasets/results/phase3/trials/exception_binding_boundary--blanket_last/black/after.py); byte-identical export: [after.py](exports/exception_binding_boundary--blanket_last/black/after.py). SHA-256: `ea65106d9cad9965684d112d8dbf758e689a47c83d4dcd168df92c581dd0687f`.

```python
def compute():
    try:
        1 / 0
    except Exception as error:
        pass
    leftover = 1  # noqa
```

Original decision: [result.json](../../datasets/results/phase3/trials/exception_binding_boundary--blanket_last/black/result.json); failure details: [matching.json](../../datasets/results/phase3/trials/exception_binding_boundary--blanket_last/black/matching.json); formatter invocation: [formatter.command.json](../../datasets/results/phase3/trials/exception_binding_boundary--blanket_last/black/formatter.command.json). Full byte-identical copies are in the export directory.

### Why the matcher abstained

Exact recorded error: `Expected one relevant AST anchor, found 0`.

F841 points to the exception-handler name `error`. Python represents it as ExceptHandler.name (a string), not an ast.Name with Store context. The primary F841 anchor policy therefore finds no candidate. The separate `leftover` assignment does have a Store Name, but the unsupported `error` prevents complete primary correspondence.

### Noqa placement

| Snapshot | Position (1-based) | Kind | Exact comment | Preceding code on line |
|---|---|---|---|---|
| before | 6:17-23 | inline | `# noqa` | `leftover=1` |
| after | 6:19-25 | inline | `# noqa` | `leftover = 1` |

### Warning identities and visibility

The identities below are review-only, not original automated matcher identities. V = visible; S = suppressed; ranges are 1-based with exclusive end columns.

| Identity / source role | Warning and source slice | Before range | After range | A / B / C / D | Judgment |
|---|---|---|---|---|---|
| `review:F841@$.body[0].body[0].handlers[0].name`; exception-handler binding string field | F841: `error`; Local variable `error` is assigned to but never used | 4:25-4:30 | 4:25-4:30 | V / V / V / V | visible in both |
| `review:F841@$.body[0].body[1].targets[0]`; assignment Store Name | F841: `leftover`; Local variable `leftover` is assigned to but never used | 6:5-6:13 | 6:5-6:13 | S / V / S / V | suppressed in both |

### Evidence-based judgment and human review

The source changes only assignment spacing; executable AST and non-comment code tokens are equal. Exact diagnostic source slices identify the same `as error` handler binding and `leftover` assignment, with unchanged warning messages and roles. F841 `error` is visible in both; F841 `leftover` is suppressed in both. All four saved outputs replay exactly after ignoring only temporary filenames. Neutralizing directive comments makes ordinary lint reproduce the underlying warnings in both snapshots. Proposed resolution: Preserved; no corresponding warning changes its visible/suppressed state.

Human interpretation: Independent human adjudication is pending; this is an AI-assisted proposal. A human should confirm the same exception binding is referenced by F841 and approve any future extension beyond Store Name anchors; no matcher change is proposed as validated here.

Saved replays and comment-neutralized sources: `reports/ambiguous-audit/exports/exception_binding_boundary--blanket_last/black/rechecks`. All four replay stdout/stderr and command records are saved there; both neutralized ordinary-lint passes reproduce their respective underlying outputs.

### All four original raw Ruff diagnostic outputs

Privacy-derived JSON is preserved below with execution filenames anonymized and fix metadata retained. Empty arrays are actual empty outputs. Each stdout file also has a `.command.json`, `.stderr.txt` and `.diagnostics.json` sibling in both the original and export directories.

<details>
<summary>A_original_visible</summary>

Original: [A_original_visible.stdout.txt](../../datasets/results/phase3/trials/exception_binding_boundary--blanket_last/black/A_original_visible.stdout.txt). Export: [A_original_visible.stdout.txt](exports/exception_binding_boundary--blanket_last/black/A_original_visible.stdout.txt). Replay: [A_original_visible.stdout.txt](exports/exception_binding_boundary--blanket_last/black/rechecks/A_original_visible.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 30,
      "row": 4
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-5eyebyq4\\study_input.py",
    "fix": {
      "applicability": "safe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 30,
            "row": 4
          },
          "location": {
            "column": 21,
            "row": 4
          }
        }
      ],
      "message": "Remove assignment to unused variable `error`"
    },
    "location": {
      "column": 25,
      "row": 4
    },
    "message": "Local variable `error` is assigned to but never used",
    "noqa_row": 4,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  }
]
```

</details>

<details>
<summary>B_original_underlying</summary>

Original: [B_original_underlying.stdout.txt](../../datasets/results/phase3/trials/exception_binding_boundary--blanket_last/black/B_original_underlying.stdout.txt). Export: [B_original_underlying.stdout.txt](exports/exception_binding_boundary--blanket_last/black/B_original_underlying.stdout.txt). Replay: [B_original_underlying.stdout.txt](exports/exception_binding_boundary--blanket_last/black/rechecks/B_original_underlying.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 30,
      "row": 4
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-v9c5r014\\study_input.py",
    "fix": {
      "applicability": "safe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 30,
            "row": 4
          },
          "location": {
            "column": 21,
            "row": 4
          }
        }
      ],
      "message": "Remove assignment to unused variable `error`"
    },
    "location": {
      "column": 25,
      "row": 4
    },
    "message": "Local variable `error` is assigned to but never used",
    "noqa_row": 4,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  },
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 13,
      "row": 6
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-v9c5r014\\study_input.py",
    "fix": {
      "applicability": "unsafe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 1,
            "row": 7
          },
          "location": {
            "column": 1,
            "row": 6
          }
        }
      ],
      "message": "Remove assignment to unused variable `leftover`"
    },
    "location": {
      "column": 5,
      "row": 6
    },
    "message": "Local variable `leftover` is assigned to but never used",
    "noqa_row": 6,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  }
]
```

</details>

<details>
<summary>C_formatted_visible</summary>

Original: [C_formatted_visible.stdout.txt](../../datasets/results/phase3/trials/exception_binding_boundary--blanket_last/black/C_formatted_visible.stdout.txt). Export: [C_formatted_visible.stdout.txt](exports/exception_binding_boundary--blanket_last/black/C_formatted_visible.stdout.txt). Replay: [C_formatted_visible.stdout.txt](exports/exception_binding_boundary--blanket_last/black/rechecks/C_formatted_visible.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 30,
      "row": 4
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-pd957qu4\\study_input.py",
    "fix": {
      "applicability": "safe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 30,
            "row": 4
          },
          "location": {
            "column": 21,
            "row": 4
          }
        }
      ],
      "message": "Remove assignment to unused variable `error`"
    },
    "location": {
      "column": 25,
      "row": 4
    },
    "message": "Local variable `error` is assigned to but never used",
    "noqa_row": 4,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  }
]
```

</details>

<details>
<summary>D_formatted_underlying</summary>

Original: [D_formatted_underlying.stdout.txt](../../datasets/results/phase3/trials/exception_binding_boundary--blanket_last/black/D_formatted_underlying.stdout.txt). Export: [D_formatted_underlying.stdout.txt](exports/exception_binding_boundary--blanket_last/black/D_formatted_underlying.stdout.txt). Replay: [D_formatted_underlying.stdout.txt](exports/exception_binding_boundary--blanket_last/black/rechecks/D_formatted_underlying.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 30,
      "row": 4
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-3rzukp6b\\study_input.py",
    "fix": {
      "applicability": "safe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 30,
            "row": 4
          },
          "location": {
            "column": 21,
            "row": 4
          }
        }
      ],
      "message": "Remove assignment to unused variable `error`"
    },
    "location": {
      "column": 25,
      "row": 4
    },
    "message": "Local variable `error` is assigned to but never used",
    "noqa_row": 4,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  },
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 13,
      "row": 6
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-3rzukp6b\\study_input.py",
    "fix": {
      "applicability": "unsafe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 1,
            "row": 7
          },
          "location": {
            "column": 1,
            "row": 6
          }
        }
      ],
      "message": "Remove assignment to unused variable `leftover`"
    },
    "location": {
      "column": 5,
      "row": 6
    },
    "message": "Local variable `leftover` is assigned to but never used",
    "noqa_row": 6,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  }
]
```

</details>

<a id="comparison-04"></a>

## 04. exception_binding_boundary--blanket_last / ruff

**Original label:** Ambiguous. **Proposed review resolution:** Preserved.

Original evidence directory: `datasets/results/phase3/trials/exception_binding_boundary--blanket_last/ruff`

Review export directory: `reports/ambiguous-audit/exports/exception_binding_boundary--blanket_last/ruff`

### Sources and exact evidence paths

Original source: [before.py](../../datasets/results/phase3/trials/exception_binding_boundary--blanket_last/ruff/before.py); byte-identical export: [before.py](exports/exception_binding_boundary--blanket_last/ruff/before.py). SHA-256: `876969ab9eb8a96f1b8105921d542d30f1a30bed384434a048a9b1b3d319dade`.

```python
def compute():
    try:
        1 / 0
    except Exception as error:
        pass
    leftover=1  # noqa
```

Formatted source: [after.py](../../datasets/results/phase3/trials/exception_binding_boundary--blanket_last/ruff/after.py); byte-identical export: [after.py](exports/exception_binding_boundary--blanket_last/ruff/after.py). SHA-256: `ea65106d9cad9965684d112d8dbf758e689a47c83d4dcd168df92c581dd0687f`.

```python
def compute():
    try:
        1 / 0
    except Exception as error:
        pass
    leftover = 1  # noqa
```

Original decision: [result.json](../../datasets/results/phase3/trials/exception_binding_boundary--blanket_last/ruff/result.json); failure details: [matching.json](../../datasets/results/phase3/trials/exception_binding_boundary--blanket_last/ruff/matching.json); formatter invocation: [formatter.command.json](../../datasets/results/phase3/trials/exception_binding_boundary--blanket_last/ruff/formatter.command.json). Full byte-identical copies are in the export directory.

### Why the matcher abstained

Exact recorded error: `Expected one relevant AST anchor, found 0`.

F841 points to the exception-handler name `error`. Python represents it as ExceptHandler.name (a string), not an ast.Name with Store context. The primary F841 anchor policy therefore finds no candidate. The separate `leftover` assignment does have a Store Name, but the unsupported `error` prevents complete primary correspondence.

### Noqa placement

| Snapshot | Position (1-based) | Kind | Exact comment | Preceding code on line |
|---|---|---|---|---|
| before | 6:17-23 | inline | `# noqa` | `leftover=1` |
| after | 6:19-25 | inline | `# noqa` | `leftover = 1` |

### Warning identities and visibility

The identities below are review-only, not original automated matcher identities. V = visible; S = suppressed; ranges are 1-based with exclusive end columns.

| Identity / source role | Warning and source slice | Before range | After range | A / B / C / D | Judgment |
|---|---|---|---|---|---|
| `review:F841@$.body[0].body[0].handlers[0].name`; exception-handler binding string field | F841: `error`; Local variable `error` is assigned to but never used | 4:25-4:30 | 4:25-4:30 | V / V / V / V | visible in both |
| `review:F841@$.body[0].body[1].targets[0]`; assignment Store Name | F841: `leftover`; Local variable `leftover` is assigned to but never used | 6:5-6:13 | 6:5-6:13 | S / V / S / V | suppressed in both |

### Evidence-based judgment and human review

The source changes only assignment spacing; executable AST and non-comment code tokens are equal. Exact diagnostic source slices identify the same `as error` handler binding and `leftover` assignment, with unchanged warning messages and roles. F841 `error` is visible in both; F841 `leftover` is suppressed in both. All four saved outputs replay exactly after ignoring only temporary filenames. Neutralizing directive comments makes ordinary lint reproduce the underlying warnings in both snapshots. Proposed resolution: Preserved; no corresponding warning changes its visible/suppressed state.

Human interpretation: Independent human adjudication is pending; this is an AI-assisted proposal. A human should confirm the same exception binding is referenced by F841 and approve any future extension beyond Store Name anchors; no matcher change is proposed as validated here.

Saved replays and comment-neutralized sources: `reports/ambiguous-audit/exports/exception_binding_boundary--blanket_last/ruff/rechecks`. All four replay stdout/stderr and command records are saved there; both neutralized ordinary-lint passes reproduce their respective underlying outputs.

### All four original raw Ruff diagnostic outputs

Privacy-derived JSON is preserved below with execution filenames anonymized and fix metadata retained. Empty arrays are actual empty outputs. Each stdout file also has a `.command.json`, `.stderr.txt` and `.diagnostics.json` sibling in both the original and export directories.

<details>
<summary>A_original_visible</summary>

Original: [A_original_visible.stdout.txt](../../datasets/results/phase3/trials/exception_binding_boundary--blanket_last/ruff/A_original_visible.stdout.txt). Export: [A_original_visible.stdout.txt](exports/exception_binding_boundary--blanket_last/ruff/A_original_visible.stdout.txt). Replay: [A_original_visible.stdout.txt](exports/exception_binding_boundary--blanket_last/ruff/rechecks/A_original_visible.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 30,
      "row": 4
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-acwry6s4\\study_input.py",
    "fix": {
      "applicability": "safe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 30,
            "row": 4
          },
          "location": {
            "column": 21,
            "row": 4
          }
        }
      ],
      "message": "Remove assignment to unused variable `error`"
    },
    "location": {
      "column": 25,
      "row": 4
    },
    "message": "Local variable `error` is assigned to but never used",
    "noqa_row": 4,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  }
]
```

</details>

<details>
<summary>B_original_underlying</summary>

Original: [B_original_underlying.stdout.txt](../../datasets/results/phase3/trials/exception_binding_boundary--blanket_last/ruff/B_original_underlying.stdout.txt). Export: [B_original_underlying.stdout.txt](exports/exception_binding_boundary--blanket_last/ruff/B_original_underlying.stdout.txt). Replay: [B_original_underlying.stdout.txt](exports/exception_binding_boundary--blanket_last/ruff/rechecks/B_original_underlying.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 30,
      "row": 4
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-hqphkzap\\study_input.py",
    "fix": {
      "applicability": "safe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 30,
            "row": 4
          },
          "location": {
            "column": 21,
            "row": 4
          }
        }
      ],
      "message": "Remove assignment to unused variable `error`"
    },
    "location": {
      "column": 25,
      "row": 4
    },
    "message": "Local variable `error` is assigned to but never used",
    "noqa_row": 4,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  },
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 13,
      "row": 6
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-hqphkzap\\study_input.py",
    "fix": {
      "applicability": "unsafe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 1,
            "row": 7
          },
          "location": {
            "column": 1,
            "row": 6
          }
        }
      ],
      "message": "Remove assignment to unused variable `leftover`"
    },
    "location": {
      "column": 5,
      "row": 6
    },
    "message": "Local variable `leftover` is assigned to but never used",
    "noqa_row": 6,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  }
]
```

</details>

<details>
<summary>C_formatted_visible</summary>

Original: [C_formatted_visible.stdout.txt](../../datasets/results/phase3/trials/exception_binding_boundary--blanket_last/ruff/C_formatted_visible.stdout.txt). Export: [C_formatted_visible.stdout.txt](exports/exception_binding_boundary--blanket_last/ruff/C_formatted_visible.stdout.txt). Replay: [C_formatted_visible.stdout.txt](exports/exception_binding_boundary--blanket_last/ruff/rechecks/C_formatted_visible.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 30,
      "row": 4
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-_60icf62\\study_input.py",
    "fix": {
      "applicability": "safe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 30,
            "row": 4
          },
          "location": {
            "column": 21,
            "row": 4
          }
        }
      ],
      "message": "Remove assignment to unused variable `error`"
    },
    "location": {
      "column": 25,
      "row": 4
    },
    "message": "Local variable `error` is assigned to but never used",
    "noqa_row": 4,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  }
]
```

</details>

<details>
<summary>D_formatted_underlying</summary>

Original: [D_formatted_underlying.stdout.txt](../../datasets/results/phase3/trials/exception_binding_boundary--blanket_last/ruff/D_formatted_underlying.stdout.txt). Export: [D_formatted_underlying.stdout.txt](exports/exception_binding_boundary--blanket_last/ruff/D_formatted_underlying.stdout.txt). Replay: [D_formatted_underlying.stdout.txt](exports/exception_binding_boundary--blanket_last/ruff/rechecks/D_formatted_underlying.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 30,
      "row": 4
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-c2yfezxx\\study_input.py",
    "fix": {
      "applicability": "safe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 30,
            "row": 4
          },
          "location": {
            "column": 21,
            "row": 4
          }
        }
      ],
      "message": "Remove assignment to unused variable `error`"
    },
    "location": {
      "column": 25,
      "row": 4
    },
    "message": "Local variable `error` is assigned to but never used",
    "noqa_row": 4,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  },
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 13,
      "row": 6
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-c2yfezxx\\study_input.py",
    "fix": {
      "applicability": "unsafe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 1,
            "row": 7
          },
          "location": {
            "column": 1,
            "row": 6
          }
        }
      ],
      "message": "Remove assignment to unused variable `leftover`"
    },
    "location": {
      "column": 5,
      "row": 6
    },
    "message": "Local variable `leftover` is assigned to but never used",
    "noqa_row": 6,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  }
]
```

</details>

<a id="comparison-05"></a>

## 05. exception_binding_boundary--file_specific / black

**Original label:** Ambiguous. **Proposed review resolution:** Preserved.

Original evidence directory: `datasets/results/phase3/trials/exception_binding_boundary--file_specific/black`

Review export directory: `reports/ambiguous-audit/exports/exception_binding_boundary--file_specific/black`

### Sources and exact evidence paths

Original source: [before.py](../../datasets/results/phase3/trials/exception_binding_boundary--file_specific/black/before.py); byte-identical export: [before.py](exports/exception_binding_boundary--file_specific/black/before.py). SHA-256: `9f8e523b17e7041b4eb2614dbe4c2b9986a0353bf52974f6f5925d8e00b91377`.

```python
# ruff: noqa: F841
def compute():
    try:
        1 / 0
    except Exception as error:
        pass
    leftover=1
```

Formatted source: [after.py](../../datasets/results/phase3/trials/exception_binding_boundary--file_specific/black/after.py); byte-identical export: [after.py](exports/exception_binding_boundary--file_specific/black/after.py). SHA-256: `c3377c8afeb4865566e3fc301e721e96d1d4e27ae4416e80d6409bee45db3dc6`.

```python
# ruff: noqa: F841
def compute():
    try:
        1 / 0
    except Exception as error:
        pass
    leftover = 1
```

Original decision: [result.json](../../datasets/results/phase3/trials/exception_binding_boundary--file_specific/black/result.json); failure details: [matching.json](../../datasets/results/phase3/trials/exception_binding_boundary--file_specific/black/matching.json); formatter invocation: [formatter.command.json](../../datasets/results/phase3/trials/exception_binding_boundary--file_specific/black/formatter.command.json). Full byte-identical copies are in the export directory.

### Why the matcher abstained

Exact recorded error: `Expected one relevant AST anchor, found 0`.

F841 points to the exception-handler name `error`. Python represents it as ExceptHandler.name (a string), not an ast.Name with Store context. The primary F841 anchor policy therefore finds no candidate. The separate `leftover` assignment does have a Store Name, but the unsupported `error` prevents complete primary correspondence.

### Noqa placement

| Snapshot | Position (1-based) | Kind | Exact comment | Preceding code on line |
|---|---|---|---|---|
| before | 1:1-19 | file directive | `# ruff: noqa: F841` | `` |
| after | 1:1-19 | file directive | `# ruff: noqa: F841` | `` |

### Warning identities and visibility

The identities below are review-only, not original automated matcher identities. V = visible; S = suppressed; ranges are 1-based with exclusive end columns.

| Identity / source role | Warning and source slice | Before range | After range | A / B / C / D | Judgment |
|---|---|---|---|---|---|
| `review:F841@$.body[0].body[0].handlers[0].name`; exception-handler binding string field | F841: `error`; Local variable `error` is assigned to but never used | 5:25-5:30 | 5:25-5:30 | S / V / S / V | suppressed in both |
| `review:F841@$.body[0].body[1].targets[0]`; assignment Store Name | F841: `leftover`; Local variable `leftover` is assigned to but never used | 7:5-7:13 | 7:5-7:13 | S / V / S / V | suppressed in both |

### Evidence-based judgment and human review

The source changes only assignment spacing; executable AST and non-comment code tokens are equal. Exact diagnostic source slices identify the same `as error` handler binding and `leftover` assignment, with unchanged warning messages and roles. F841 `error` is suppressed in both; F841 `leftover` is suppressed in both. All four saved outputs replay exactly after ignoring only temporary filenames. Neutralizing directive comments makes ordinary lint reproduce the underlying warnings in both snapshots. Proposed resolution: Preserved; no corresponding warning changes its visible/suppressed state.

Human interpretation: Independent human adjudication is pending; this is an AI-assisted proposal. A human should confirm the same exception binding is referenced by F841 and approve any future extension beyond Store Name anchors; no matcher change is proposed as validated here.

Saved replays and comment-neutralized sources: `reports/ambiguous-audit/exports/exception_binding_boundary--file_specific/black/rechecks`. All four replay stdout/stderr and command records are saved there; both neutralized ordinary-lint passes reproduce their respective underlying outputs.

### All four original raw Ruff diagnostic outputs

Privacy-derived JSON is preserved below with execution filenames anonymized and fix metadata retained. Empty arrays are actual empty outputs. Each stdout file also has a `.command.json`, `.stderr.txt` and `.diagnostics.json` sibling in both the original and export directories.

<details>
<summary>A_original_visible</summary>

Original: [A_original_visible.stdout.txt](../../datasets/results/phase3/trials/exception_binding_boundary--file_specific/black/A_original_visible.stdout.txt). Export: [A_original_visible.stdout.txt](exports/exception_binding_boundary--file_specific/black/A_original_visible.stdout.txt). Replay: [A_original_visible.stdout.txt](exports/exception_binding_boundary--file_specific/black/rechecks/A_original_visible.stdout.txt).

```json
[]
```

</details>

<details>
<summary>B_original_underlying</summary>

Original: [B_original_underlying.stdout.txt](../../datasets/results/phase3/trials/exception_binding_boundary--file_specific/black/B_original_underlying.stdout.txt). Export: [B_original_underlying.stdout.txt](exports/exception_binding_boundary--file_specific/black/B_original_underlying.stdout.txt). Replay: [B_original_underlying.stdout.txt](exports/exception_binding_boundary--file_specific/black/rechecks/B_original_underlying.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 30,
      "row": 5
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-8llnwk8s\\study_input.py",
    "fix": {
      "applicability": "safe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 30,
            "row": 5
          },
          "location": {
            "column": 21,
            "row": 5
          }
        }
      ],
      "message": "Remove assignment to unused variable `error`"
    },
    "location": {
      "column": 25,
      "row": 5
    },
    "message": "Local variable `error` is assigned to but never used",
    "noqa_row": 5,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  },
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 13,
      "row": 7
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-8llnwk8s\\study_input.py",
    "fix": {
      "applicability": "unsafe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 1,
            "row": 8
          },
          "location": {
            "column": 1,
            "row": 7
          }
        }
      ],
      "message": "Remove assignment to unused variable `leftover`"
    },
    "location": {
      "column": 5,
      "row": 7
    },
    "message": "Local variable `leftover` is assigned to but never used",
    "noqa_row": 7,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  }
]
```

</details>

<details>
<summary>C_formatted_visible</summary>

Original: [C_formatted_visible.stdout.txt](../../datasets/results/phase3/trials/exception_binding_boundary--file_specific/black/C_formatted_visible.stdout.txt). Export: [C_formatted_visible.stdout.txt](exports/exception_binding_boundary--file_specific/black/C_formatted_visible.stdout.txt). Replay: [C_formatted_visible.stdout.txt](exports/exception_binding_boundary--file_specific/black/rechecks/C_formatted_visible.stdout.txt).

```json
[]
```

</details>

<details>
<summary>D_formatted_underlying</summary>

Original: [D_formatted_underlying.stdout.txt](../../datasets/results/phase3/trials/exception_binding_boundary--file_specific/black/D_formatted_underlying.stdout.txt). Export: [D_formatted_underlying.stdout.txt](exports/exception_binding_boundary--file_specific/black/D_formatted_underlying.stdout.txt). Replay: [D_formatted_underlying.stdout.txt](exports/exception_binding_boundary--file_specific/black/rechecks/D_formatted_underlying.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 30,
      "row": 5
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-r9h9rgt9\\study_input.py",
    "fix": {
      "applicability": "safe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 30,
            "row": 5
          },
          "location": {
            "column": 21,
            "row": 5
          }
        }
      ],
      "message": "Remove assignment to unused variable `error`"
    },
    "location": {
      "column": 25,
      "row": 5
    },
    "message": "Local variable `error` is assigned to but never used",
    "noqa_row": 5,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  },
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 13,
      "row": 7
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-r9h9rgt9\\study_input.py",
    "fix": {
      "applicability": "unsafe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 1,
            "row": 8
          },
          "location": {
            "column": 1,
            "row": 7
          }
        }
      ],
      "message": "Remove assignment to unused variable `leftover`"
    },
    "location": {
      "column": 5,
      "row": 7
    },
    "message": "Local variable `leftover` is assigned to but never used",
    "noqa_row": 7,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  }
]
```

</details>

<a id="comparison-06"></a>

## 06. exception_binding_boundary--file_specific / ruff

**Original label:** Ambiguous. **Proposed review resolution:** Preserved.

Original evidence directory: `datasets/results/phase3/trials/exception_binding_boundary--file_specific/ruff`

Review export directory: `reports/ambiguous-audit/exports/exception_binding_boundary--file_specific/ruff`

### Sources and exact evidence paths

Original source: [before.py](../../datasets/results/phase3/trials/exception_binding_boundary--file_specific/ruff/before.py); byte-identical export: [before.py](exports/exception_binding_boundary--file_specific/ruff/before.py). SHA-256: `9f8e523b17e7041b4eb2614dbe4c2b9986a0353bf52974f6f5925d8e00b91377`.

```python
# ruff: noqa: F841
def compute():
    try:
        1 / 0
    except Exception as error:
        pass
    leftover=1
```

Formatted source: [after.py](../../datasets/results/phase3/trials/exception_binding_boundary--file_specific/ruff/after.py); byte-identical export: [after.py](exports/exception_binding_boundary--file_specific/ruff/after.py). SHA-256: `c3377c8afeb4865566e3fc301e721e96d1d4e27ae4416e80d6409bee45db3dc6`.

```python
# ruff: noqa: F841
def compute():
    try:
        1 / 0
    except Exception as error:
        pass
    leftover = 1
```

Original decision: [result.json](../../datasets/results/phase3/trials/exception_binding_boundary--file_specific/ruff/result.json); failure details: [matching.json](../../datasets/results/phase3/trials/exception_binding_boundary--file_specific/ruff/matching.json); formatter invocation: [formatter.command.json](../../datasets/results/phase3/trials/exception_binding_boundary--file_specific/ruff/formatter.command.json). Full byte-identical copies are in the export directory.

### Why the matcher abstained

Exact recorded error: `Expected one relevant AST anchor, found 0`.

F841 points to the exception-handler name `error`. Python represents it as ExceptHandler.name (a string), not an ast.Name with Store context. The primary F841 anchor policy therefore finds no candidate. The separate `leftover` assignment does have a Store Name, but the unsupported `error` prevents complete primary correspondence.

### Noqa placement

| Snapshot | Position (1-based) | Kind | Exact comment | Preceding code on line |
|---|---|---|---|---|
| before | 1:1-19 | file directive | `# ruff: noqa: F841` | `` |
| after | 1:1-19 | file directive | `# ruff: noqa: F841` | `` |

### Warning identities and visibility

The identities below are review-only, not original automated matcher identities. V = visible; S = suppressed; ranges are 1-based with exclusive end columns.

| Identity / source role | Warning and source slice | Before range | After range | A / B / C / D | Judgment |
|---|---|---|---|---|---|
| `review:F841@$.body[0].body[0].handlers[0].name`; exception-handler binding string field | F841: `error`; Local variable `error` is assigned to but never used | 5:25-5:30 | 5:25-5:30 | S / V / S / V | suppressed in both |
| `review:F841@$.body[0].body[1].targets[0]`; assignment Store Name | F841: `leftover`; Local variable `leftover` is assigned to but never used | 7:5-7:13 | 7:5-7:13 | S / V / S / V | suppressed in both |

### Evidence-based judgment and human review

The source changes only assignment spacing; executable AST and non-comment code tokens are equal. Exact diagnostic source slices identify the same `as error` handler binding and `leftover` assignment, with unchanged warning messages and roles. F841 `error` is suppressed in both; F841 `leftover` is suppressed in both. All four saved outputs replay exactly after ignoring only temporary filenames. Neutralizing directive comments makes ordinary lint reproduce the underlying warnings in both snapshots. Proposed resolution: Preserved; no corresponding warning changes its visible/suppressed state.

Human interpretation: Independent human adjudication is pending; this is an AI-assisted proposal. A human should confirm the same exception binding is referenced by F841 and approve any future extension beyond Store Name anchors; no matcher change is proposed as validated here.

Saved replays and comment-neutralized sources: `reports/ambiguous-audit/exports/exception_binding_boundary--file_specific/ruff/rechecks`. All four replay stdout/stderr and command records are saved there; both neutralized ordinary-lint passes reproduce their respective underlying outputs.

### All four original raw Ruff diagnostic outputs

Privacy-derived JSON is preserved below with execution filenames anonymized and fix metadata retained. Empty arrays are actual empty outputs. Each stdout file also has a `.command.json`, `.stderr.txt` and `.diagnostics.json` sibling in both the original and export directories.

<details>
<summary>A_original_visible</summary>

Original: [A_original_visible.stdout.txt](../../datasets/results/phase3/trials/exception_binding_boundary--file_specific/ruff/A_original_visible.stdout.txt). Export: [A_original_visible.stdout.txt](exports/exception_binding_boundary--file_specific/ruff/A_original_visible.stdout.txt). Replay: [A_original_visible.stdout.txt](exports/exception_binding_boundary--file_specific/ruff/rechecks/A_original_visible.stdout.txt).

```json
[]
```

</details>

<details>
<summary>B_original_underlying</summary>

Original: [B_original_underlying.stdout.txt](../../datasets/results/phase3/trials/exception_binding_boundary--file_specific/ruff/B_original_underlying.stdout.txt). Export: [B_original_underlying.stdout.txt](exports/exception_binding_boundary--file_specific/ruff/B_original_underlying.stdout.txt). Replay: [B_original_underlying.stdout.txt](exports/exception_binding_boundary--file_specific/ruff/rechecks/B_original_underlying.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 30,
      "row": 5
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-dno7a2b0\\study_input.py",
    "fix": {
      "applicability": "safe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 30,
            "row": 5
          },
          "location": {
            "column": 21,
            "row": 5
          }
        }
      ],
      "message": "Remove assignment to unused variable `error`"
    },
    "location": {
      "column": 25,
      "row": 5
    },
    "message": "Local variable `error` is assigned to but never used",
    "noqa_row": 5,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  },
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 13,
      "row": 7
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-dno7a2b0\\study_input.py",
    "fix": {
      "applicability": "unsafe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 1,
            "row": 8
          },
          "location": {
            "column": 1,
            "row": 7
          }
        }
      ],
      "message": "Remove assignment to unused variable `leftover`"
    },
    "location": {
      "column": 5,
      "row": 7
    },
    "message": "Local variable `leftover` is assigned to but never used",
    "noqa_row": 7,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  }
]
```

</details>

<details>
<summary>C_formatted_visible</summary>

Original: [C_formatted_visible.stdout.txt](../../datasets/results/phase3/trials/exception_binding_boundary--file_specific/ruff/C_formatted_visible.stdout.txt). Export: [C_formatted_visible.stdout.txt](exports/exception_binding_boundary--file_specific/ruff/C_formatted_visible.stdout.txt). Replay: [C_formatted_visible.stdout.txt](exports/exception_binding_boundary--file_specific/ruff/rechecks/C_formatted_visible.stdout.txt).

```json
[]
```

</details>

<details>
<summary>D_formatted_underlying</summary>

Original: [D_formatted_underlying.stdout.txt](../../datasets/results/phase3/trials/exception_binding_boundary--file_specific/ruff/D_formatted_underlying.stdout.txt). Export: [D_formatted_underlying.stdout.txt](exports/exception_binding_boundary--file_specific/ruff/D_formatted_underlying.stdout.txt). Replay: [D_formatted_underlying.stdout.txt](exports/exception_binding_boundary--file_specific/ruff/rechecks/D_formatted_underlying.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 30,
      "row": 5
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-qmdh4iye\\study_input.py",
    "fix": {
      "applicability": "safe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 30,
            "row": 5
          },
          "location": {
            "column": 21,
            "row": 5
          }
        }
      ],
      "message": "Remove assignment to unused variable `error`"
    },
    "location": {
      "column": 25,
      "row": 5
    },
    "message": "Local variable `error` is assigned to but never used",
    "noqa_row": 5,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  },
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 13,
      "row": 7
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-qmdh4iye\\study_input.py",
    "fix": {
      "applicability": "unsafe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 1,
            "row": 8
          },
          "location": {
            "column": 1,
            "row": 7
          }
        }
      ],
      "message": "Remove assignment to unused variable `leftover`"
    },
    "location": {
      "column": 5,
      "row": 7
    },
    "message": "Local variable `leftover` is assigned to but never used",
    "noqa_row": 7,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  }
]
```

</details>

<a id="comparison-07"></a>

## 07. exception_binding_boundary--multicode_first / black

**Original label:** Ambiguous. **Proposed review resolution:** Preserved.

Original evidence directory: `datasets/results/phase3/trials/exception_binding_boundary--multicode_first/black`

Review export directory: `reports/ambiguous-audit/exports/exception_binding_boundary--multicode_first/black`

### Sources and exact evidence paths

Original source: [before.py](../../datasets/results/phase3/trials/exception_binding_boundary--multicode_first/black/before.py); byte-identical export: [before.py](exports/exception_binding_boundary--multicode_first/black/before.py). SHA-256: `0ea3acd658284a46aeac47afc82e4834ce03d4c468f57a05256b4383524bbf70`.

```python
def compute():
    try:
        1 / 0
    except Exception as error:  # noqa: F401, F821, F841
        pass
    leftover=1
```

Formatted source: [after.py](../../datasets/results/phase3/trials/exception_binding_boundary--multicode_first/black/after.py); byte-identical export: [after.py](exports/exception_binding_boundary--multicode_first/black/after.py). SHA-256: `571f09a8e44984b8e4b5b0bd94d274b42b405c4b1278822f49424e56869c0240`.

```python
def compute():
    try:
        1 / 0
    except Exception as error:  # noqa: F401, F821, F841
        pass
    leftover = 1
```

Original decision: [result.json](../../datasets/results/phase3/trials/exception_binding_boundary--multicode_first/black/result.json); failure details: [matching.json](../../datasets/results/phase3/trials/exception_binding_boundary--multicode_first/black/matching.json); formatter invocation: [formatter.command.json](../../datasets/results/phase3/trials/exception_binding_boundary--multicode_first/black/formatter.command.json). Full byte-identical copies are in the export directory.

### Why the matcher abstained

Exact recorded error: `Expected one relevant AST anchor, found 0`.

F841 points to the exception-handler name `error`. Python represents it as ExceptHandler.name (a string), not an ast.Name with Store context. The primary F841 anchor policy therefore finds no candidate. The separate `leftover` assignment does have a Store Name, but the unsupported `error` prevents complete primary correspondence.

### Noqa placement

| Snapshot | Position (1-based) | Kind | Exact comment | Preceding code on line |
|---|---|---|---|---|
| before | 4:33-57 | inline | `# noqa: F401, F821, F841` | `except Exception as error:` |
| after | 4:33-57 | inline | `# noqa: F401, F821, F841` | `except Exception as error:` |

### Warning identities and visibility

The identities below are review-only, not original automated matcher identities. V = visible; S = suppressed; ranges are 1-based with exclusive end columns.

| Identity / source role | Warning and source slice | Before range | After range | A / B / C / D | Judgment |
|---|---|---|---|---|---|
| `review:F841@$.body[0].body[0].handlers[0].name`; exception-handler binding string field | F841: `error`; Local variable `error` is assigned to but never used | 4:25-4:30 | 4:25-4:30 | S / V / S / V | suppressed in both |
| `review:F841@$.body[0].body[1].targets[0]`; assignment Store Name | F841: `leftover`; Local variable `leftover` is assigned to but never used | 6:5-6:13 | 6:5-6:13 | V / V / V / V | visible in both |

### Evidence-based judgment and human review

The source changes only assignment spacing; executable AST and non-comment code tokens are equal. Exact diagnostic source slices identify the same `as error` handler binding and `leftover` assignment, with unchanged warning messages and roles. F841 `error` is suppressed in both; F841 `leftover` is visible in both. All four saved outputs replay exactly after ignoring only temporary filenames. Neutralizing directive comments makes ordinary lint reproduce the underlying warnings in both snapshots. Proposed resolution: Preserved; no corresponding warning changes its visible/suppressed state.

Human interpretation: Independent human adjudication is pending; this is an AI-assisted proposal. A human should confirm the same exception binding is referenced by F841 and approve any future extension beyond Store Name anchors; no matcher change is proposed as validated here.

Saved replays and comment-neutralized sources: `reports/ambiguous-audit/exports/exception_binding_boundary--multicode_first/black/rechecks`. All four replay stdout/stderr and command records are saved there; both neutralized ordinary-lint passes reproduce their respective underlying outputs.

### All four original raw Ruff diagnostic outputs

Privacy-derived JSON is preserved below with execution filenames anonymized and fix metadata retained. Empty arrays are actual empty outputs. Each stdout file also has a `.command.json`, `.stderr.txt` and `.diagnostics.json` sibling in both the original and export directories.

<details>
<summary>A_original_visible</summary>

Original: [A_original_visible.stdout.txt](../../datasets/results/phase3/trials/exception_binding_boundary--multicode_first/black/A_original_visible.stdout.txt). Export: [A_original_visible.stdout.txt](exports/exception_binding_boundary--multicode_first/black/A_original_visible.stdout.txt). Replay: [A_original_visible.stdout.txt](exports/exception_binding_boundary--multicode_first/black/rechecks/A_original_visible.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 13,
      "row": 6
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-h6dgmhyf\\study_input.py",
    "fix": {
      "applicability": "unsafe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 1,
            "row": 7
          },
          "location": {
            "column": 1,
            "row": 6
          }
        }
      ],
      "message": "Remove assignment to unused variable `leftover`"
    },
    "location": {
      "column": 5,
      "row": 6
    },
    "message": "Local variable `leftover` is assigned to but never used",
    "noqa_row": 6,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  }
]
```

</details>

<details>
<summary>B_original_underlying</summary>

Original: [B_original_underlying.stdout.txt](../../datasets/results/phase3/trials/exception_binding_boundary--multicode_first/black/B_original_underlying.stdout.txt). Export: [B_original_underlying.stdout.txt](exports/exception_binding_boundary--multicode_first/black/B_original_underlying.stdout.txt). Replay: [B_original_underlying.stdout.txt](exports/exception_binding_boundary--multicode_first/black/rechecks/B_original_underlying.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 30,
      "row": 4
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-ul2_6kx0\\study_input.py",
    "fix": {
      "applicability": "safe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 30,
            "row": 4
          },
          "location": {
            "column": 21,
            "row": 4
          }
        }
      ],
      "message": "Remove assignment to unused variable `error`"
    },
    "location": {
      "column": 25,
      "row": 4
    },
    "message": "Local variable `error` is assigned to but never used",
    "noqa_row": 4,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  },
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 13,
      "row": 6
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-ul2_6kx0\\study_input.py",
    "fix": {
      "applicability": "unsafe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 1,
            "row": 7
          },
          "location": {
            "column": 1,
            "row": 6
          }
        }
      ],
      "message": "Remove assignment to unused variable `leftover`"
    },
    "location": {
      "column": 5,
      "row": 6
    },
    "message": "Local variable `leftover` is assigned to but never used",
    "noqa_row": 6,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  }
]
```

</details>

<details>
<summary>C_formatted_visible</summary>

Original: [C_formatted_visible.stdout.txt](../../datasets/results/phase3/trials/exception_binding_boundary--multicode_first/black/C_formatted_visible.stdout.txt). Export: [C_formatted_visible.stdout.txt](exports/exception_binding_boundary--multicode_first/black/C_formatted_visible.stdout.txt). Replay: [C_formatted_visible.stdout.txt](exports/exception_binding_boundary--multicode_first/black/rechecks/C_formatted_visible.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 13,
      "row": 6
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-dosz8u9x\\study_input.py",
    "fix": {
      "applicability": "unsafe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 1,
            "row": 7
          },
          "location": {
            "column": 1,
            "row": 6
          }
        }
      ],
      "message": "Remove assignment to unused variable `leftover`"
    },
    "location": {
      "column": 5,
      "row": 6
    },
    "message": "Local variable `leftover` is assigned to but never used",
    "noqa_row": 6,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  }
]
```

</details>

<details>
<summary>D_formatted_underlying</summary>

Original: [D_formatted_underlying.stdout.txt](../../datasets/results/phase3/trials/exception_binding_boundary--multicode_first/black/D_formatted_underlying.stdout.txt). Export: [D_formatted_underlying.stdout.txt](exports/exception_binding_boundary--multicode_first/black/D_formatted_underlying.stdout.txt). Replay: [D_formatted_underlying.stdout.txt](exports/exception_binding_boundary--multicode_first/black/rechecks/D_formatted_underlying.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 30,
      "row": 4
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-yf5kiee7\\study_input.py",
    "fix": {
      "applicability": "safe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 30,
            "row": 4
          },
          "location": {
            "column": 21,
            "row": 4
          }
        }
      ],
      "message": "Remove assignment to unused variable `error`"
    },
    "location": {
      "column": 25,
      "row": 4
    },
    "message": "Local variable `error` is assigned to but never used",
    "noqa_row": 4,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  },
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 13,
      "row": 6
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-yf5kiee7\\study_input.py",
    "fix": {
      "applicability": "unsafe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 1,
            "row": 7
          },
          "location": {
            "column": 1,
            "row": 6
          }
        }
      ],
      "message": "Remove assignment to unused variable `leftover`"
    },
    "location": {
      "column": 5,
      "row": 6
    },
    "message": "Local variable `leftover` is assigned to but never used",
    "noqa_row": 6,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  }
]
```

</details>

<a id="comparison-08"></a>

## 08. exception_binding_boundary--multicode_first / ruff

**Original label:** Ambiguous. **Proposed review resolution:** Preserved.

Original evidence directory: `datasets/results/phase3/trials/exception_binding_boundary--multicode_first/ruff`

Review export directory: `reports/ambiguous-audit/exports/exception_binding_boundary--multicode_first/ruff`

### Sources and exact evidence paths

Original source: [before.py](../../datasets/results/phase3/trials/exception_binding_boundary--multicode_first/ruff/before.py); byte-identical export: [before.py](exports/exception_binding_boundary--multicode_first/ruff/before.py). SHA-256: `0ea3acd658284a46aeac47afc82e4834ce03d4c468f57a05256b4383524bbf70`.

```python
def compute():
    try:
        1 / 0
    except Exception as error:  # noqa: F401, F821, F841
        pass
    leftover=1
```

Formatted source: [after.py](../../datasets/results/phase3/trials/exception_binding_boundary--multicode_first/ruff/after.py); byte-identical export: [after.py](exports/exception_binding_boundary--multicode_first/ruff/after.py). SHA-256: `571f09a8e44984b8e4b5b0bd94d274b42b405c4b1278822f49424e56869c0240`.

```python
def compute():
    try:
        1 / 0
    except Exception as error:  # noqa: F401, F821, F841
        pass
    leftover = 1
```

Original decision: [result.json](../../datasets/results/phase3/trials/exception_binding_boundary--multicode_first/ruff/result.json); failure details: [matching.json](../../datasets/results/phase3/trials/exception_binding_boundary--multicode_first/ruff/matching.json); formatter invocation: [formatter.command.json](../../datasets/results/phase3/trials/exception_binding_boundary--multicode_first/ruff/formatter.command.json). Full byte-identical copies are in the export directory.

### Why the matcher abstained

Exact recorded error: `Expected one relevant AST anchor, found 0`.

F841 points to the exception-handler name `error`. Python represents it as ExceptHandler.name (a string), not an ast.Name with Store context. The primary F841 anchor policy therefore finds no candidate. The separate `leftover` assignment does have a Store Name, but the unsupported `error` prevents complete primary correspondence.

### Noqa placement

| Snapshot | Position (1-based) | Kind | Exact comment | Preceding code on line |
|---|---|---|---|---|
| before | 4:33-57 | inline | `# noqa: F401, F821, F841` | `except Exception as error:` |
| after | 4:33-57 | inline | `# noqa: F401, F821, F841` | `except Exception as error:` |

### Warning identities and visibility

The identities below are review-only, not original automated matcher identities. V = visible; S = suppressed; ranges are 1-based with exclusive end columns.

| Identity / source role | Warning and source slice | Before range | After range | A / B / C / D | Judgment |
|---|---|---|---|---|---|
| `review:F841@$.body[0].body[0].handlers[0].name`; exception-handler binding string field | F841: `error`; Local variable `error` is assigned to but never used | 4:25-4:30 | 4:25-4:30 | S / V / S / V | suppressed in both |
| `review:F841@$.body[0].body[1].targets[0]`; assignment Store Name | F841: `leftover`; Local variable `leftover` is assigned to but never used | 6:5-6:13 | 6:5-6:13 | V / V / V / V | visible in both |

### Evidence-based judgment and human review

The source changes only assignment spacing; executable AST and non-comment code tokens are equal. Exact diagnostic source slices identify the same `as error` handler binding and `leftover` assignment, with unchanged warning messages and roles. F841 `error` is suppressed in both; F841 `leftover` is visible in both. All four saved outputs replay exactly after ignoring only temporary filenames. Neutralizing directive comments makes ordinary lint reproduce the underlying warnings in both snapshots. Proposed resolution: Preserved; no corresponding warning changes its visible/suppressed state.

Human interpretation: Independent human adjudication is pending; this is an AI-assisted proposal. A human should confirm the same exception binding is referenced by F841 and approve any future extension beyond Store Name anchors; no matcher change is proposed as validated here.

Saved replays and comment-neutralized sources: `reports/ambiguous-audit/exports/exception_binding_boundary--multicode_first/ruff/rechecks`. All four replay stdout/stderr and command records are saved there; both neutralized ordinary-lint passes reproduce their respective underlying outputs.

### All four original raw Ruff diagnostic outputs

Privacy-derived JSON is preserved below with execution filenames anonymized and fix metadata retained. Empty arrays are actual empty outputs. Each stdout file also has a `.command.json`, `.stderr.txt` and `.diagnostics.json` sibling in both the original and export directories.

<details>
<summary>A_original_visible</summary>

Original: [A_original_visible.stdout.txt](../../datasets/results/phase3/trials/exception_binding_boundary--multicode_first/ruff/A_original_visible.stdout.txt). Export: [A_original_visible.stdout.txt](exports/exception_binding_boundary--multicode_first/ruff/A_original_visible.stdout.txt). Replay: [A_original_visible.stdout.txt](exports/exception_binding_boundary--multicode_first/ruff/rechecks/A_original_visible.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 13,
      "row": 6
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-kwlawvtg\\study_input.py",
    "fix": {
      "applicability": "unsafe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 1,
            "row": 7
          },
          "location": {
            "column": 1,
            "row": 6
          }
        }
      ],
      "message": "Remove assignment to unused variable `leftover`"
    },
    "location": {
      "column": 5,
      "row": 6
    },
    "message": "Local variable `leftover` is assigned to but never used",
    "noqa_row": 6,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  }
]
```

</details>

<details>
<summary>B_original_underlying</summary>

Original: [B_original_underlying.stdout.txt](../../datasets/results/phase3/trials/exception_binding_boundary--multicode_first/ruff/B_original_underlying.stdout.txt). Export: [B_original_underlying.stdout.txt](exports/exception_binding_boundary--multicode_first/ruff/B_original_underlying.stdout.txt). Replay: [B_original_underlying.stdout.txt](exports/exception_binding_boundary--multicode_first/ruff/rechecks/B_original_underlying.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 30,
      "row": 4
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-dcr9gywv\\study_input.py",
    "fix": {
      "applicability": "safe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 30,
            "row": 4
          },
          "location": {
            "column": 21,
            "row": 4
          }
        }
      ],
      "message": "Remove assignment to unused variable `error`"
    },
    "location": {
      "column": 25,
      "row": 4
    },
    "message": "Local variable `error` is assigned to but never used",
    "noqa_row": 4,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  },
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 13,
      "row": 6
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-dcr9gywv\\study_input.py",
    "fix": {
      "applicability": "unsafe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 1,
            "row": 7
          },
          "location": {
            "column": 1,
            "row": 6
          }
        }
      ],
      "message": "Remove assignment to unused variable `leftover`"
    },
    "location": {
      "column": 5,
      "row": 6
    },
    "message": "Local variable `leftover` is assigned to but never used",
    "noqa_row": 6,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  }
]
```

</details>

<details>
<summary>C_formatted_visible</summary>

Original: [C_formatted_visible.stdout.txt](../../datasets/results/phase3/trials/exception_binding_boundary--multicode_first/ruff/C_formatted_visible.stdout.txt). Export: [C_formatted_visible.stdout.txt](exports/exception_binding_boundary--multicode_first/ruff/C_formatted_visible.stdout.txt). Replay: [C_formatted_visible.stdout.txt](exports/exception_binding_boundary--multicode_first/ruff/rechecks/C_formatted_visible.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 13,
      "row": 6
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-jcgza5_s\\study_input.py",
    "fix": {
      "applicability": "unsafe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 1,
            "row": 7
          },
          "location": {
            "column": 1,
            "row": 6
          }
        }
      ],
      "message": "Remove assignment to unused variable `leftover`"
    },
    "location": {
      "column": 5,
      "row": 6
    },
    "message": "Local variable `leftover` is assigned to but never used",
    "noqa_row": 6,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  }
]
```

</details>

<details>
<summary>D_formatted_underlying</summary>

Original: [D_formatted_underlying.stdout.txt](../../datasets/results/phase3/trials/exception_binding_boundary--multicode_first/ruff/D_formatted_underlying.stdout.txt). Export: [D_formatted_underlying.stdout.txt](exports/exception_binding_boundary--multicode_first/ruff/D_formatted_underlying.stdout.txt). Replay: [D_formatted_underlying.stdout.txt](exports/exception_binding_boundary--multicode_first/ruff/rechecks/D_formatted_underlying.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 30,
      "row": 4
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-ew1bdl7m\\study_input.py",
    "fix": {
      "applicability": "safe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 30,
            "row": 4
          },
          "location": {
            "column": 21,
            "row": 4
          }
        }
      ],
      "message": "Remove assignment to unused variable `error`"
    },
    "location": {
      "column": 25,
      "row": 4
    },
    "message": "Local variable `error` is assigned to but never used",
    "noqa_row": 4,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  },
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 13,
      "row": 6
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-ew1bdl7m\\study_input.py",
    "fix": {
      "applicability": "unsafe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 1,
            "row": 7
          },
          "location": {
            "column": 1,
            "row": 6
          }
        }
      ],
      "message": "Remove assignment to unused variable `leftover`"
    },
    "location": {
      "column": 5,
      "row": 6
    },
    "message": "Local variable `leftover` is assigned to but never used",
    "noqa_row": 6,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  }
]
```

</details>

<a id="comparison-09"></a>

## 09. exception_binding_boundary--none / black

**Original label:** Ambiguous. **Proposed review resolution:** Preserved.

Original evidence directory: `datasets/results/phase3/trials/exception_binding_boundary--none/black`

Review export directory: `reports/ambiguous-audit/exports/exception_binding_boundary--none/black`

### Sources and exact evidence paths

Original source: [before.py](../../datasets/results/phase3/trials/exception_binding_boundary--none/black/before.py); byte-identical export: [before.py](exports/exception_binding_boundary--none/black/before.py). SHA-256: `9c6a952541236eaed573ea199a3e730e37b8b3046e737254668340a9b3bab94b`.

```python
def compute():
    try:
        1 / 0
    except Exception as error:
        pass
    leftover=1
```

Formatted source: [after.py](../../datasets/results/phase3/trials/exception_binding_boundary--none/black/after.py); byte-identical export: [after.py](exports/exception_binding_boundary--none/black/after.py). SHA-256: `67ab64146d061f1b9e9d5c1db44d742724433b8c6c3caf67fcbff491c5bd90a5`.

```python
def compute():
    try:
        1 / 0
    except Exception as error:
        pass
    leftover = 1
```

Original decision: [result.json](../../datasets/results/phase3/trials/exception_binding_boundary--none/black/result.json); failure details: [matching.json](../../datasets/results/phase3/trials/exception_binding_boundary--none/black/matching.json); formatter invocation: [formatter.command.json](../../datasets/results/phase3/trials/exception_binding_boundary--none/black/formatter.command.json). Full byte-identical copies are in the export directory.

### Why the matcher abstained

Exact recorded error: `Expected one relevant AST anchor, found 0`.

F841 points to the exception-handler name `error`. Python represents it as ExceptHandler.name (a string), not an ast.Name with Store context. The primary F841 anchor policy therefore finds no candidate. The separate `leftover` assignment does have a Store Name, but the unsupported `error` prevents complete primary correspondence.

### Noqa placement

| Snapshot | Position (1-based) | Kind | Exact comment | Preceding code on line |
|---|---|---|---|---|
| before | - | no directive | - | - |
| after | - | no directive | - | - |

### Warning identities and visibility

The identities below are review-only, not original automated matcher identities. V = visible; S = suppressed; ranges are 1-based with exclusive end columns.

| Identity / source role | Warning and source slice | Before range | After range | A / B / C / D | Judgment |
|---|---|---|---|---|---|
| `review:F841@$.body[0].body[0].handlers[0].name`; exception-handler binding string field | F841: `error`; Local variable `error` is assigned to but never used | 4:25-4:30 | 4:25-4:30 | V / V / V / V | visible in both |
| `review:F841@$.body[0].body[1].targets[0]`; assignment Store Name | F841: `leftover`; Local variable `leftover` is assigned to but never used | 6:5-6:13 | 6:5-6:13 | V / V / V / V | visible in both |

### Evidence-based judgment and human review

The source changes only assignment spacing; executable AST and non-comment code tokens are equal. Exact diagnostic source slices identify the same `as error` handler binding and `leftover` assignment, with unchanged warning messages and roles. F841 `error` is visible in both; F841 `leftover` is visible in both. All four saved outputs replay exactly after ignoring only temporary filenames. Neutralizing directive comments makes ordinary lint reproduce the underlying warnings in both snapshots. Proposed resolution: Preserved; no corresponding warning changes its visible/suppressed state.

Human interpretation: Independent human adjudication is pending; this is an AI-assisted proposal. A human should confirm the same exception binding is referenced by F841 and approve any future extension beyond Store Name anchors; no matcher change is proposed as validated here.

Saved replays and comment-neutralized sources: `reports/ambiguous-audit/exports/exception_binding_boundary--none/black/rechecks`. All four replay stdout/stderr and command records are saved there; both neutralized ordinary-lint passes reproduce their respective underlying outputs.

### All four original raw Ruff diagnostic outputs

Privacy-derived JSON is preserved below with execution filenames anonymized and fix metadata retained. Empty arrays are actual empty outputs. Each stdout file also has a `.command.json`, `.stderr.txt` and `.diagnostics.json` sibling in both the original and export directories.

<details>
<summary>A_original_visible</summary>

Original: [A_original_visible.stdout.txt](../../datasets/results/phase3/trials/exception_binding_boundary--none/black/A_original_visible.stdout.txt). Export: [A_original_visible.stdout.txt](exports/exception_binding_boundary--none/black/A_original_visible.stdout.txt). Replay: [A_original_visible.stdout.txt](exports/exception_binding_boundary--none/black/rechecks/A_original_visible.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 30,
      "row": 4
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-wu25bss6\\study_input.py",
    "fix": {
      "applicability": "safe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 30,
            "row": 4
          },
          "location": {
            "column": 21,
            "row": 4
          }
        }
      ],
      "message": "Remove assignment to unused variable `error`"
    },
    "location": {
      "column": 25,
      "row": 4
    },
    "message": "Local variable `error` is assigned to but never used",
    "noqa_row": 4,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  },
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 13,
      "row": 6
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-wu25bss6\\study_input.py",
    "fix": {
      "applicability": "unsafe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 1,
            "row": 7
          },
          "location": {
            "column": 1,
            "row": 6
          }
        }
      ],
      "message": "Remove assignment to unused variable `leftover`"
    },
    "location": {
      "column": 5,
      "row": 6
    },
    "message": "Local variable `leftover` is assigned to but never used",
    "noqa_row": 6,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  }
]
```

</details>

<details>
<summary>B_original_underlying</summary>

Original: [B_original_underlying.stdout.txt](../../datasets/results/phase3/trials/exception_binding_boundary--none/black/B_original_underlying.stdout.txt). Export: [B_original_underlying.stdout.txt](exports/exception_binding_boundary--none/black/B_original_underlying.stdout.txt). Replay: [B_original_underlying.stdout.txt](exports/exception_binding_boundary--none/black/rechecks/B_original_underlying.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 30,
      "row": 4
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-y70ls746\\study_input.py",
    "fix": {
      "applicability": "safe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 30,
            "row": 4
          },
          "location": {
            "column": 21,
            "row": 4
          }
        }
      ],
      "message": "Remove assignment to unused variable `error`"
    },
    "location": {
      "column": 25,
      "row": 4
    },
    "message": "Local variable `error` is assigned to but never used",
    "noqa_row": 4,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  },
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 13,
      "row": 6
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-y70ls746\\study_input.py",
    "fix": {
      "applicability": "unsafe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 1,
            "row": 7
          },
          "location": {
            "column": 1,
            "row": 6
          }
        }
      ],
      "message": "Remove assignment to unused variable `leftover`"
    },
    "location": {
      "column": 5,
      "row": 6
    },
    "message": "Local variable `leftover` is assigned to but never used",
    "noqa_row": 6,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  }
]
```

</details>

<details>
<summary>C_formatted_visible</summary>

Original: [C_formatted_visible.stdout.txt](../../datasets/results/phase3/trials/exception_binding_boundary--none/black/C_formatted_visible.stdout.txt). Export: [C_formatted_visible.stdout.txt](exports/exception_binding_boundary--none/black/C_formatted_visible.stdout.txt). Replay: [C_formatted_visible.stdout.txt](exports/exception_binding_boundary--none/black/rechecks/C_formatted_visible.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 30,
      "row": 4
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-dggaecmc\\study_input.py",
    "fix": {
      "applicability": "safe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 30,
            "row": 4
          },
          "location": {
            "column": 21,
            "row": 4
          }
        }
      ],
      "message": "Remove assignment to unused variable `error`"
    },
    "location": {
      "column": 25,
      "row": 4
    },
    "message": "Local variable `error` is assigned to but never used",
    "noqa_row": 4,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  },
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 13,
      "row": 6
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-dggaecmc\\study_input.py",
    "fix": {
      "applicability": "unsafe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 1,
            "row": 7
          },
          "location": {
            "column": 1,
            "row": 6
          }
        }
      ],
      "message": "Remove assignment to unused variable `leftover`"
    },
    "location": {
      "column": 5,
      "row": 6
    },
    "message": "Local variable `leftover` is assigned to but never used",
    "noqa_row": 6,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  }
]
```

</details>

<details>
<summary>D_formatted_underlying</summary>

Original: [D_formatted_underlying.stdout.txt](../../datasets/results/phase3/trials/exception_binding_boundary--none/black/D_formatted_underlying.stdout.txt). Export: [D_formatted_underlying.stdout.txt](exports/exception_binding_boundary--none/black/D_formatted_underlying.stdout.txt). Replay: [D_formatted_underlying.stdout.txt](exports/exception_binding_boundary--none/black/rechecks/D_formatted_underlying.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 30,
      "row": 4
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-740ombii\\study_input.py",
    "fix": {
      "applicability": "safe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 30,
            "row": 4
          },
          "location": {
            "column": 21,
            "row": 4
          }
        }
      ],
      "message": "Remove assignment to unused variable `error`"
    },
    "location": {
      "column": 25,
      "row": 4
    },
    "message": "Local variable `error` is assigned to but never used",
    "noqa_row": 4,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  },
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 13,
      "row": 6
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-740ombii\\study_input.py",
    "fix": {
      "applicability": "unsafe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 1,
            "row": 7
          },
          "location": {
            "column": 1,
            "row": 6
          }
        }
      ],
      "message": "Remove assignment to unused variable `leftover`"
    },
    "location": {
      "column": 5,
      "row": 6
    },
    "message": "Local variable `leftover` is assigned to but never used",
    "noqa_row": 6,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  }
]
```

</details>

<a id="comparison-10"></a>

## 10. exception_binding_boundary--none / ruff

**Original label:** Ambiguous. **Proposed review resolution:** Preserved.

Original evidence directory: `datasets/results/phase3/trials/exception_binding_boundary--none/ruff`

Review export directory: `reports/ambiguous-audit/exports/exception_binding_boundary--none/ruff`

### Sources and exact evidence paths

Original source: [before.py](../../datasets/results/phase3/trials/exception_binding_boundary--none/ruff/before.py); byte-identical export: [before.py](exports/exception_binding_boundary--none/ruff/before.py). SHA-256: `9c6a952541236eaed573ea199a3e730e37b8b3046e737254668340a9b3bab94b`.

```python
def compute():
    try:
        1 / 0
    except Exception as error:
        pass
    leftover=1
```

Formatted source: [after.py](../../datasets/results/phase3/trials/exception_binding_boundary--none/ruff/after.py); byte-identical export: [after.py](exports/exception_binding_boundary--none/ruff/after.py). SHA-256: `67ab64146d061f1b9e9d5c1db44d742724433b8c6c3caf67fcbff491c5bd90a5`.

```python
def compute():
    try:
        1 / 0
    except Exception as error:
        pass
    leftover = 1
```

Original decision: [result.json](../../datasets/results/phase3/trials/exception_binding_boundary--none/ruff/result.json); failure details: [matching.json](../../datasets/results/phase3/trials/exception_binding_boundary--none/ruff/matching.json); formatter invocation: [formatter.command.json](../../datasets/results/phase3/trials/exception_binding_boundary--none/ruff/formatter.command.json). Full byte-identical copies are in the export directory.

### Why the matcher abstained

Exact recorded error: `Expected one relevant AST anchor, found 0`.

F841 points to the exception-handler name `error`. Python represents it as ExceptHandler.name (a string), not an ast.Name with Store context. The primary F841 anchor policy therefore finds no candidate. The separate `leftover` assignment does have a Store Name, but the unsupported `error` prevents complete primary correspondence.

### Noqa placement

| Snapshot | Position (1-based) | Kind | Exact comment | Preceding code on line |
|---|---|---|---|---|
| before | - | no directive | - | - |
| after | - | no directive | - | - |

### Warning identities and visibility

The identities below are review-only, not original automated matcher identities. V = visible; S = suppressed; ranges are 1-based with exclusive end columns.

| Identity / source role | Warning and source slice | Before range | After range | A / B / C / D | Judgment |
|---|---|---|---|---|---|
| `review:F841@$.body[0].body[0].handlers[0].name`; exception-handler binding string field | F841: `error`; Local variable `error` is assigned to but never used | 4:25-4:30 | 4:25-4:30 | V / V / V / V | visible in both |
| `review:F841@$.body[0].body[1].targets[0]`; assignment Store Name | F841: `leftover`; Local variable `leftover` is assigned to but never used | 6:5-6:13 | 6:5-6:13 | V / V / V / V | visible in both |

### Evidence-based judgment and human review

The source changes only assignment spacing; executable AST and non-comment code tokens are equal. Exact diagnostic source slices identify the same `as error` handler binding and `leftover` assignment, with unchanged warning messages and roles. F841 `error` is visible in both; F841 `leftover` is visible in both. All four saved outputs replay exactly after ignoring only temporary filenames. Neutralizing directive comments makes ordinary lint reproduce the underlying warnings in both snapshots. Proposed resolution: Preserved; no corresponding warning changes its visible/suppressed state.

Human interpretation: Independent human adjudication is pending; this is an AI-assisted proposal. A human should confirm the same exception binding is referenced by F841 and approve any future extension beyond Store Name anchors; no matcher change is proposed as validated here.

Saved replays and comment-neutralized sources: `reports/ambiguous-audit/exports/exception_binding_boundary--none/ruff/rechecks`. All four replay stdout/stderr and command records are saved there; both neutralized ordinary-lint passes reproduce their respective underlying outputs.

### All four original raw Ruff diagnostic outputs

Privacy-derived JSON is preserved below with execution filenames anonymized and fix metadata retained. Empty arrays are actual empty outputs. Each stdout file also has a `.command.json`, `.stderr.txt` and `.diagnostics.json` sibling in both the original and export directories.

<details>
<summary>A_original_visible</summary>

Original: [A_original_visible.stdout.txt](../../datasets/results/phase3/trials/exception_binding_boundary--none/ruff/A_original_visible.stdout.txt). Export: [A_original_visible.stdout.txt](exports/exception_binding_boundary--none/ruff/A_original_visible.stdout.txt). Replay: [A_original_visible.stdout.txt](exports/exception_binding_boundary--none/ruff/rechecks/A_original_visible.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 30,
      "row": 4
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-z91aoi9t\\study_input.py",
    "fix": {
      "applicability": "safe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 30,
            "row": 4
          },
          "location": {
            "column": 21,
            "row": 4
          }
        }
      ],
      "message": "Remove assignment to unused variable `error`"
    },
    "location": {
      "column": 25,
      "row": 4
    },
    "message": "Local variable `error` is assigned to but never used",
    "noqa_row": 4,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  },
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 13,
      "row": 6
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-z91aoi9t\\study_input.py",
    "fix": {
      "applicability": "unsafe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 1,
            "row": 7
          },
          "location": {
            "column": 1,
            "row": 6
          }
        }
      ],
      "message": "Remove assignment to unused variable `leftover`"
    },
    "location": {
      "column": 5,
      "row": 6
    },
    "message": "Local variable `leftover` is assigned to but never used",
    "noqa_row": 6,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  }
]
```

</details>

<details>
<summary>B_original_underlying</summary>

Original: [B_original_underlying.stdout.txt](../../datasets/results/phase3/trials/exception_binding_boundary--none/ruff/B_original_underlying.stdout.txt). Export: [B_original_underlying.stdout.txt](exports/exception_binding_boundary--none/ruff/B_original_underlying.stdout.txt). Replay: [B_original_underlying.stdout.txt](exports/exception_binding_boundary--none/ruff/rechecks/B_original_underlying.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 30,
      "row": 4
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-zm390zzm\\study_input.py",
    "fix": {
      "applicability": "safe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 30,
            "row": 4
          },
          "location": {
            "column": 21,
            "row": 4
          }
        }
      ],
      "message": "Remove assignment to unused variable `error`"
    },
    "location": {
      "column": 25,
      "row": 4
    },
    "message": "Local variable `error` is assigned to but never used",
    "noqa_row": 4,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  },
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 13,
      "row": 6
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-zm390zzm\\study_input.py",
    "fix": {
      "applicability": "unsafe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 1,
            "row": 7
          },
          "location": {
            "column": 1,
            "row": 6
          }
        }
      ],
      "message": "Remove assignment to unused variable `leftover`"
    },
    "location": {
      "column": 5,
      "row": 6
    },
    "message": "Local variable `leftover` is assigned to but never used",
    "noqa_row": 6,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  }
]
```

</details>

<details>
<summary>C_formatted_visible</summary>

Original: [C_formatted_visible.stdout.txt](../../datasets/results/phase3/trials/exception_binding_boundary--none/ruff/C_formatted_visible.stdout.txt). Export: [C_formatted_visible.stdout.txt](exports/exception_binding_boundary--none/ruff/C_formatted_visible.stdout.txt). Replay: [C_formatted_visible.stdout.txt](exports/exception_binding_boundary--none/ruff/rechecks/C_formatted_visible.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 30,
      "row": 4
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-5v16wm9u\\study_input.py",
    "fix": {
      "applicability": "safe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 30,
            "row": 4
          },
          "location": {
            "column": 21,
            "row": 4
          }
        }
      ],
      "message": "Remove assignment to unused variable `error`"
    },
    "location": {
      "column": 25,
      "row": 4
    },
    "message": "Local variable `error` is assigned to but never used",
    "noqa_row": 4,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  },
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 13,
      "row": 6
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-5v16wm9u\\study_input.py",
    "fix": {
      "applicability": "unsafe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 1,
            "row": 7
          },
          "location": {
            "column": 1,
            "row": 6
          }
        }
      ],
      "message": "Remove assignment to unused variable `leftover`"
    },
    "location": {
      "column": 5,
      "row": 6
    },
    "message": "Local variable `leftover` is assigned to but never used",
    "noqa_row": 6,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  }
]
```

</details>

<details>
<summary>D_formatted_underlying</summary>

Original: [D_formatted_underlying.stdout.txt](../../datasets/results/phase3/trials/exception_binding_boundary--none/ruff/D_formatted_underlying.stdout.txt). Export: [D_formatted_underlying.stdout.txt](exports/exception_binding_boundary--none/ruff/D_formatted_underlying.stdout.txt). Replay: [D_formatted_underlying.stdout.txt](exports/exception_binding_boundary--none/ruff/rechecks/D_formatted_underlying.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 30,
      "row": 4
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-nz_ub10r\\study_input.py",
    "fix": {
      "applicability": "safe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 30,
            "row": 4
          },
          "location": {
            "column": 21,
            "row": 4
          }
        }
      ],
      "message": "Remove assignment to unused variable `error`"
    },
    "location": {
      "column": 25,
      "row": 4
    },
    "message": "Local variable `error` is assigned to but never used",
    "noqa_row": 4,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  },
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 13,
      "row": 6
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-nz_ub10r\\study_input.py",
    "fix": {
      "applicability": "unsafe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 1,
            "row": 7
          },
          "location": {
            "column": 1,
            "row": 6
          }
        }
      ],
      "message": "Remove assignment to unused variable `leftover`"
    },
    "location": {
      "column": 5,
      "row": 6
    },
    "message": "Local variable `leftover` is assigned to but never used",
    "noqa_row": 6,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  }
]
```

</details>

<a id="comparison-11"></a>

## 11. exception_binding_boundary--specific_first / black

**Original label:** Ambiguous. **Proposed review resolution:** Preserved.

Original evidence directory: `datasets/results/phase3/trials/exception_binding_boundary--specific_first/black`

Review export directory: `reports/ambiguous-audit/exports/exception_binding_boundary--specific_first/black`

### Sources and exact evidence paths

Original source: [before.py](../../datasets/results/phase3/trials/exception_binding_boundary--specific_first/black/before.py); byte-identical export: [before.py](exports/exception_binding_boundary--specific_first/black/before.py). SHA-256: `28a0cdbd5397ad1e81ec4549cd26d89c8c5871c46120174b3926114a48d43282`.

```python
def compute():
    try:
        1 / 0
    except Exception as error:  # noqa: F841
        pass
    leftover=1
```

Formatted source: [after.py](../../datasets/results/phase3/trials/exception_binding_boundary--specific_first/black/after.py); byte-identical export: [after.py](exports/exception_binding_boundary--specific_first/black/after.py). SHA-256: `0666debfa4436d1ef5399d7fc56ddc8d15da2afffb8eff71ca266c4652fb2b5f`.

```python
def compute():
    try:
        1 / 0
    except Exception as error:  # noqa: F841
        pass
    leftover = 1
```

Original decision: [result.json](../../datasets/results/phase3/trials/exception_binding_boundary--specific_first/black/result.json); failure details: [matching.json](../../datasets/results/phase3/trials/exception_binding_boundary--specific_first/black/matching.json); formatter invocation: [formatter.command.json](../../datasets/results/phase3/trials/exception_binding_boundary--specific_first/black/formatter.command.json). Full byte-identical copies are in the export directory.

### Why the matcher abstained

Exact recorded error: `Expected one relevant AST anchor, found 0`.

F841 points to the exception-handler name `error`. Python represents it as ExceptHandler.name (a string), not an ast.Name with Store context. The primary F841 anchor policy therefore finds no candidate. The separate `leftover` assignment does have a Store Name, but the unsupported `error` prevents complete primary correspondence.

### Noqa placement

| Snapshot | Position (1-based) | Kind | Exact comment | Preceding code on line |
|---|---|---|---|---|
| before | 4:33-45 | inline | `# noqa: F841` | `except Exception as error:` |
| after | 4:33-45 | inline | `# noqa: F841` | `except Exception as error:` |

### Warning identities and visibility

The identities below are review-only, not original automated matcher identities. V = visible; S = suppressed; ranges are 1-based with exclusive end columns.

| Identity / source role | Warning and source slice | Before range | After range | A / B / C / D | Judgment |
|---|---|---|---|---|---|
| `review:F841@$.body[0].body[0].handlers[0].name`; exception-handler binding string field | F841: `error`; Local variable `error` is assigned to but never used | 4:25-4:30 | 4:25-4:30 | S / V / S / V | suppressed in both |
| `review:F841@$.body[0].body[1].targets[0]`; assignment Store Name | F841: `leftover`; Local variable `leftover` is assigned to but never used | 6:5-6:13 | 6:5-6:13 | V / V / V / V | visible in both |

### Evidence-based judgment and human review

The source changes only assignment spacing; executable AST and non-comment code tokens are equal. Exact diagnostic source slices identify the same `as error` handler binding and `leftover` assignment, with unchanged warning messages and roles. F841 `error` is suppressed in both; F841 `leftover` is visible in both. All four saved outputs replay exactly after ignoring only temporary filenames. Neutralizing directive comments makes ordinary lint reproduce the underlying warnings in both snapshots. Proposed resolution: Preserved; no corresponding warning changes its visible/suppressed state.

Human interpretation: Independent human adjudication is pending; this is an AI-assisted proposal. A human should confirm the same exception binding is referenced by F841 and approve any future extension beyond Store Name anchors; no matcher change is proposed as validated here.

Saved replays and comment-neutralized sources: `reports/ambiguous-audit/exports/exception_binding_boundary--specific_first/black/rechecks`. All four replay stdout/stderr and command records are saved there; both neutralized ordinary-lint passes reproduce their respective underlying outputs.

### All four original raw Ruff diagnostic outputs

Privacy-derived JSON is preserved below with execution filenames anonymized and fix metadata retained. Empty arrays are actual empty outputs. Each stdout file also has a `.command.json`, `.stderr.txt` and `.diagnostics.json` sibling in both the original and export directories.

<details>
<summary>A_original_visible</summary>

Original: [A_original_visible.stdout.txt](../../datasets/results/phase3/trials/exception_binding_boundary--specific_first/black/A_original_visible.stdout.txt). Export: [A_original_visible.stdout.txt](exports/exception_binding_boundary--specific_first/black/A_original_visible.stdout.txt). Replay: [A_original_visible.stdout.txt](exports/exception_binding_boundary--specific_first/black/rechecks/A_original_visible.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 13,
      "row": 6
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-dig3expv\\study_input.py",
    "fix": {
      "applicability": "unsafe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 1,
            "row": 7
          },
          "location": {
            "column": 1,
            "row": 6
          }
        }
      ],
      "message": "Remove assignment to unused variable `leftover`"
    },
    "location": {
      "column": 5,
      "row": 6
    },
    "message": "Local variable `leftover` is assigned to but never used",
    "noqa_row": 6,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  }
]
```

</details>

<details>
<summary>B_original_underlying</summary>

Original: [B_original_underlying.stdout.txt](../../datasets/results/phase3/trials/exception_binding_boundary--specific_first/black/B_original_underlying.stdout.txt). Export: [B_original_underlying.stdout.txt](exports/exception_binding_boundary--specific_first/black/B_original_underlying.stdout.txt). Replay: [B_original_underlying.stdout.txt](exports/exception_binding_boundary--specific_first/black/rechecks/B_original_underlying.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 30,
      "row": 4
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-tup33mu5\\study_input.py",
    "fix": {
      "applicability": "safe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 30,
            "row": 4
          },
          "location": {
            "column": 21,
            "row": 4
          }
        }
      ],
      "message": "Remove assignment to unused variable `error`"
    },
    "location": {
      "column": 25,
      "row": 4
    },
    "message": "Local variable `error` is assigned to but never used",
    "noqa_row": 4,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  },
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 13,
      "row": 6
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-tup33mu5\\study_input.py",
    "fix": {
      "applicability": "unsafe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 1,
            "row": 7
          },
          "location": {
            "column": 1,
            "row": 6
          }
        }
      ],
      "message": "Remove assignment to unused variable `leftover`"
    },
    "location": {
      "column": 5,
      "row": 6
    },
    "message": "Local variable `leftover` is assigned to but never used",
    "noqa_row": 6,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  }
]
```

</details>

<details>
<summary>C_formatted_visible</summary>

Original: [C_formatted_visible.stdout.txt](../../datasets/results/phase3/trials/exception_binding_boundary--specific_first/black/C_formatted_visible.stdout.txt). Export: [C_formatted_visible.stdout.txt](exports/exception_binding_boundary--specific_first/black/C_formatted_visible.stdout.txt). Replay: [C_formatted_visible.stdout.txt](exports/exception_binding_boundary--specific_first/black/rechecks/C_formatted_visible.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 13,
      "row": 6
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-7g62gvep\\study_input.py",
    "fix": {
      "applicability": "unsafe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 1,
            "row": 7
          },
          "location": {
            "column": 1,
            "row": 6
          }
        }
      ],
      "message": "Remove assignment to unused variable `leftover`"
    },
    "location": {
      "column": 5,
      "row": 6
    },
    "message": "Local variable `leftover` is assigned to but never used",
    "noqa_row": 6,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  }
]
```

</details>

<details>
<summary>D_formatted_underlying</summary>

Original: [D_formatted_underlying.stdout.txt](../../datasets/results/phase3/trials/exception_binding_boundary--specific_first/black/D_formatted_underlying.stdout.txt). Export: [D_formatted_underlying.stdout.txt](exports/exception_binding_boundary--specific_first/black/D_formatted_underlying.stdout.txt). Replay: [D_formatted_underlying.stdout.txt](exports/exception_binding_boundary--specific_first/black/rechecks/D_formatted_underlying.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 30,
      "row": 4
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-77lh1yj9\\study_input.py",
    "fix": {
      "applicability": "safe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 30,
            "row": 4
          },
          "location": {
            "column": 21,
            "row": 4
          }
        }
      ],
      "message": "Remove assignment to unused variable `error`"
    },
    "location": {
      "column": 25,
      "row": 4
    },
    "message": "Local variable `error` is assigned to but never used",
    "noqa_row": 4,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  },
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 13,
      "row": 6
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-77lh1yj9\\study_input.py",
    "fix": {
      "applicability": "unsafe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 1,
            "row": 7
          },
          "location": {
            "column": 1,
            "row": 6
          }
        }
      ],
      "message": "Remove assignment to unused variable `leftover`"
    },
    "location": {
      "column": 5,
      "row": 6
    },
    "message": "Local variable `leftover` is assigned to but never used",
    "noqa_row": 6,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  }
]
```

</details>

<a id="comparison-12"></a>

## 12. exception_binding_boundary--specific_first / ruff

**Original label:** Ambiguous. **Proposed review resolution:** Preserved.

Original evidence directory: `datasets/results/phase3/trials/exception_binding_boundary--specific_first/ruff`

Review export directory: `reports/ambiguous-audit/exports/exception_binding_boundary--specific_first/ruff`

### Sources and exact evidence paths

Original source: [before.py](../../datasets/results/phase3/trials/exception_binding_boundary--specific_first/ruff/before.py); byte-identical export: [before.py](exports/exception_binding_boundary--specific_first/ruff/before.py). SHA-256: `28a0cdbd5397ad1e81ec4549cd26d89c8c5871c46120174b3926114a48d43282`.

```python
def compute():
    try:
        1 / 0
    except Exception as error:  # noqa: F841
        pass
    leftover=1
```

Formatted source: [after.py](../../datasets/results/phase3/trials/exception_binding_boundary--specific_first/ruff/after.py); byte-identical export: [after.py](exports/exception_binding_boundary--specific_first/ruff/after.py). SHA-256: `0666debfa4436d1ef5399d7fc56ddc8d15da2afffb8eff71ca266c4652fb2b5f`.

```python
def compute():
    try:
        1 / 0
    except Exception as error:  # noqa: F841
        pass
    leftover = 1
```

Original decision: [result.json](../../datasets/results/phase3/trials/exception_binding_boundary--specific_first/ruff/result.json); failure details: [matching.json](../../datasets/results/phase3/trials/exception_binding_boundary--specific_first/ruff/matching.json); formatter invocation: [formatter.command.json](../../datasets/results/phase3/trials/exception_binding_boundary--specific_first/ruff/formatter.command.json). Full byte-identical copies are in the export directory.

### Why the matcher abstained

Exact recorded error: `Expected one relevant AST anchor, found 0`.

F841 points to the exception-handler name `error`. Python represents it as ExceptHandler.name (a string), not an ast.Name with Store context. The primary F841 anchor policy therefore finds no candidate. The separate `leftover` assignment does have a Store Name, but the unsupported `error` prevents complete primary correspondence.

### Noqa placement

| Snapshot | Position (1-based) | Kind | Exact comment | Preceding code on line |
|---|---|---|---|---|
| before | 4:33-45 | inline | `# noqa: F841` | `except Exception as error:` |
| after | 4:33-45 | inline | `# noqa: F841` | `except Exception as error:` |

### Warning identities and visibility

The identities below are review-only, not original automated matcher identities. V = visible; S = suppressed; ranges are 1-based with exclusive end columns.

| Identity / source role | Warning and source slice | Before range | After range | A / B / C / D | Judgment |
|---|---|---|---|---|---|
| `review:F841@$.body[0].body[0].handlers[0].name`; exception-handler binding string field | F841: `error`; Local variable `error` is assigned to but never used | 4:25-4:30 | 4:25-4:30 | S / V / S / V | suppressed in both |
| `review:F841@$.body[0].body[1].targets[0]`; assignment Store Name | F841: `leftover`; Local variable `leftover` is assigned to but never used | 6:5-6:13 | 6:5-6:13 | V / V / V / V | visible in both |

### Evidence-based judgment and human review

The source changes only assignment spacing; executable AST and non-comment code tokens are equal. Exact diagnostic source slices identify the same `as error` handler binding and `leftover` assignment, with unchanged warning messages and roles. F841 `error` is suppressed in both; F841 `leftover` is visible in both. All four saved outputs replay exactly after ignoring only temporary filenames. Neutralizing directive comments makes ordinary lint reproduce the underlying warnings in both snapshots. Proposed resolution: Preserved; no corresponding warning changes its visible/suppressed state.

Human interpretation: Independent human adjudication is pending; this is an AI-assisted proposal. A human should confirm the same exception binding is referenced by F841 and approve any future extension beyond Store Name anchors; no matcher change is proposed as validated here.

Saved replays and comment-neutralized sources: `reports/ambiguous-audit/exports/exception_binding_boundary--specific_first/ruff/rechecks`. All four replay stdout/stderr and command records are saved there; both neutralized ordinary-lint passes reproduce their respective underlying outputs.

### All four original raw Ruff diagnostic outputs

Privacy-derived JSON is preserved below with execution filenames anonymized and fix metadata retained. Empty arrays are actual empty outputs. Each stdout file also has a `.command.json`, `.stderr.txt` and `.diagnostics.json` sibling in both the original and export directories.

<details>
<summary>A_original_visible</summary>

Original: [A_original_visible.stdout.txt](../../datasets/results/phase3/trials/exception_binding_boundary--specific_first/ruff/A_original_visible.stdout.txt). Export: [A_original_visible.stdout.txt](exports/exception_binding_boundary--specific_first/ruff/A_original_visible.stdout.txt). Replay: [A_original_visible.stdout.txt](exports/exception_binding_boundary--specific_first/ruff/rechecks/A_original_visible.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 13,
      "row": 6
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-ovy1mwqm\\study_input.py",
    "fix": {
      "applicability": "unsafe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 1,
            "row": 7
          },
          "location": {
            "column": 1,
            "row": 6
          }
        }
      ],
      "message": "Remove assignment to unused variable `leftover`"
    },
    "location": {
      "column": 5,
      "row": 6
    },
    "message": "Local variable `leftover` is assigned to but never used",
    "noqa_row": 6,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  }
]
```

</details>

<details>
<summary>B_original_underlying</summary>

Original: [B_original_underlying.stdout.txt](../../datasets/results/phase3/trials/exception_binding_boundary--specific_first/ruff/B_original_underlying.stdout.txt). Export: [B_original_underlying.stdout.txt](exports/exception_binding_boundary--specific_first/ruff/B_original_underlying.stdout.txt). Replay: [B_original_underlying.stdout.txt](exports/exception_binding_boundary--specific_first/ruff/rechecks/B_original_underlying.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 30,
      "row": 4
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-sacnvr94\\study_input.py",
    "fix": {
      "applicability": "safe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 30,
            "row": 4
          },
          "location": {
            "column": 21,
            "row": 4
          }
        }
      ],
      "message": "Remove assignment to unused variable `error`"
    },
    "location": {
      "column": 25,
      "row": 4
    },
    "message": "Local variable `error` is assigned to but never used",
    "noqa_row": 4,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  },
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 13,
      "row": 6
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-sacnvr94\\study_input.py",
    "fix": {
      "applicability": "unsafe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 1,
            "row": 7
          },
          "location": {
            "column": 1,
            "row": 6
          }
        }
      ],
      "message": "Remove assignment to unused variable `leftover`"
    },
    "location": {
      "column": 5,
      "row": 6
    },
    "message": "Local variable `leftover` is assigned to but never used",
    "noqa_row": 6,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  }
]
```

</details>

<details>
<summary>C_formatted_visible</summary>

Original: [C_formatted_visible.stdout.txt](../../datasets/results/phase3/trials/exception_binding_boundary--specific_first/ruff/C_formatted_visible.stdout.txt). Export: [C_formatted_visible.stdout.txt](exports/exception_binding_boundary--specific_first/ruff/C_formatted_visible.stdout.txt). Replay: [C_formatted_visible.stdout.txt](exports/exception_binding_boundary--specific_first/ruff/rechecks/C_formatted_visible.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 13,
      "row": 6
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-v4as1gcr\\study_input.py",
    "fix": {
      "applicability": "unsafe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 1,
            "row": 7
          },
          "location": {
            "column": 1,
            "row": 6
          }
        }
      ],
      "message": "Remove assignment to unused variable `leftover`"
    },
    "location": {
      "column": 5,
      "row": 6
    },
    "message": "Local variable `leftover` is assigned to but never used",
    "noqa_row": 6,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  }
]
```

</details>

<details>
<summary>D_formatted_underlying</summary>

Original: [D_formatted_underlying.stdout.txt](../../datasets/results/phase3/trials/exception_binding_boundary--specific_first/ruff/D_formatted_underlying.stdout.txt). Export: [D_formatted_underlying.stdout.txt](exports/exception_binding_boundary--specific_first/ruff/D_formatted_underlying.stdout.txt). Replay: [D_formatted_underlying.stdout.txt](exports/exception_binding_boundary--specific_first/ruff/rechecks/D_formatted_underlying.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 30,
      "row": 4
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-hss8ch5i\\study_input.py",
    "fix": {
      "applicability": "safe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 30,
            "row": 4
          },
          "location": {
            "column": 21,
            "row": 4
          }
        }
      ],
      "message": "Remove assignment to unused variable `error`"
    },
    "location": {
      "column": 25,
      "row": 4
    },
    "message": "Local variable `error` is assigned to but never used",
    "noqa_row": 4,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  },
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 13,
      "row": 6
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-hss8ch5i\\study_input.py",
    "fix": {
      "applicability": "unsafe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 1,
            "row": 7
          },
          "location": {
            "column": 1,
            "row": 6
          }
        }
      ],
      "message": "Remove assignment to unused variable `leftover`"
    },
    "location": {
      "column": 5,
      "row": 6
    },
    "message": "Local variable `leftover` is assigned to but never used",
    "noqa_row": 6,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  }
]
```

</details>

<a id="comparison-13"></a>

## 13. exception_binding_boundary--specific_last / black

**Original label:** Ambiguous. **Proposed review resolution:** Preserved.

Original evidence directory: `datasets/results/phase3/trials/exception_binding_boundary--specific_last/black`

Review export directory: `reports/ambiguous-audit/exports/exception_binding_boundary--specific_last/black`

### Sources and exact evidence paths

Original source: [before.py](../../datasets/results/phase3/trials/exception_binding_boundary--specific_last/black/before.py); byte-identical export: [before.py](exports/exception_binding_boundary--specific_last/black/before.py). SHA-256: `996acdf3e25cb67c53be0ccede398ef1d2e0f6cd688a6bfc1aa7cc3885e60110`.

```python
def compute():
    try:
        1 / 0
    except Exception as error:
        pass
    leftover=1  # noqa: F841
```

Formatted source: [after.py](../../datasets/results/phase3/trials/exception_binding_boundary--specific_last/black/after.py); byte-identical export: [after.py](exports/exception_binding_boundary--specific_last/black/after.py). SHA-256: `b9335eaaaee3e69c02dfb12964e14794ef2d3c711efc75a1d87c6f2720820540`.

```python
def compute():
    try:
        1 / 0
    except Exception as error:
        pass
    leftover = 1  # noqa: F841
```

Original decision: [result.json](../../datasets/results/phase3/trials/exception_binding_boundary--specific_last/black/result.json); failure details: [matching.json](../../datasets/results/phase3/trials/exception_binding_boundary--specific_last/black/matching.json); formatter invocation: [formatter.command.json](../../datasets/results/phase3/trials/exception_binding_boundary--specific_last/black/formatter.command.json). Full byte-identical copies are in the export directory.

### Why the matcher abstained

Exact recorded error: `Expected one relevant AST anchor, found 0`.

F841 points to the exception-handler name `error`. Python represents it as ExceptHandler.name (a string), not an ast.Name with Store context. The primary F841 anchor policy therefore finds no candidate. The separate `leftover` assignment does have a Store Name, but the unsupported `error` prevents complete primary correspondence.

### Noqa placement

| Snapshot | Position (1-based) | Kind | Exact comment | Preceding code on line |
|---|---|---|---|---|
| before | 6:17-29 | inline | `# noqa: F841` | `leftover=1` |
| after | 6:19-31 | inline | `# noqa: F841` | `leftover = 1` |

### Warning identities and visibility

The identities below are review-only, not original automated matcher identities. V = visible; S = suppressed; ranges are 1-based with exclusive end columns.

| Identity / source role | Warning and source slice | Before range | After range | A / B / C / D | Judgment |
|---|---|---|---|---|---|
| `review:F841@$.body[0].body[0].handlers[0].name`; exception-handler binding string field | F841: `error`; Local variable `error` is assigned to but never used | 4:25-4:30 | 4:25-4:30 | V / V / V / V | visible in both |
| `review:F841@$.body[0].body[1].targets[0]`; assignment Store Name | F841: `leftover`; Local variable `leftover` is assigned to but never used | 6:5-6:13 | 6:5-6:13 | S / V / S / V | suppressed in both |

### Evidence-based judgment and human review

The source changes only assignment spacing; executable AST and non-comment code tokens are equal. Exact diagnostic source slices identify the same `as error` handler binding and `leftover` assignment, with unchanged warning messages and roles. F841 `error` is visible in both; F841 `leftover` is suppressed in both. All four saved outputs replay exactly after ignoring only temporary filenames. Neutralizing directive comments makes ordinary lint reproduce the underlying warnings in both snapshots. Proposed resolution: Preserved; no corresponding warning changes its visible/suppressed state.

Human interpretation: Independent human adjudication is pending; this is an AI-assisted proposal. A human should confirm the same exception binding is referenced by F841 and approve any future extension beyond Store Name anchors; no matcher change is proposed as validated here.

Saved replays and comment-neutralized sources: `reports/ambiguous-audit/exports/exception_binding_boundary--specific_last/black/rechecks`. All four replay stdout/stderr and command records are saved there; both neutralized ordinary-lint passes reproduce their respective underlying outputs.

### All four original raw Ruff diagnostic outputs

Privacy-derived JSON is preserved below with execution filenames anonymized and fix metadata retained. Empty arrays are actual empty outputs. Each stdout file also has a `.command.json`, `.stderr.txt` and `.diagnostics.json` sibling in both the original and export directories.

<details>
<summary>A_original_visible</summary>

Original: [A_original_visible.stdout.txt](../../datasets/results/phase3/trials/exception_binding_boundary--specific_last/black/A_original_visible.stdout.txt). Export: [A_original_visible.stdout.txt](exports/exception_binding_boundary--specific_last/black/A_original_visible.stdout.txt). Replay: [A_original_visible.stdout.txt](exports/exception_binding_boundary--specific_last/black/rechecks/A_original_visible.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 30,
      "row": 4
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-icuo4pwu\\study_input.py",
    "fix": {
      "applicability": "safe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 30,
            "row": 4
          },
          "location": {
            "column": 21,
            "row": 4
          }
        }
      ],
      "message": "Remove assignment to unused variable `error`"
    },
    "location": {
      "column": 25,
      "row": 4
    },
    "message": "Local variable `error` is assigned to but never used",
    "noqa_row": 4,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  }
]
```

</details>

<details>
<summary>B_original_underlying</summary>

Original: [B_original_underlying.stdout.txt](../../datasets/results/phase3/trials/exception_binding_boundary--specific_last/black/B_original_underlying.stdout.txt). Export: [B_original_underlying.stdout.txt](exports/exception_binding_boundary--specific_last/black/B_original_underlying.stdout.txt). Replay: [B_original_underlying.stdout.txt](exports/exception_binding_boundary--specific_last/black/rechecks/B_original_underlying.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 30,
      "row": 4
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-pr6heyqp\\study_input.py",
    "fix": {
      "applicability": "safe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 30,
            "row": 4
          },
          "location": {
            "column": 21,
            "row": 4
          }
        }
      ],
      "message": "Remove assignment to unused variable `error`"
    },
    "location": {
      "column": 25,
      "row": 4
    },
    "message": "Local variable `error` is assigned to but never used",
    "noqa_row": 4,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  },
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 13,
      "row": 6
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-pr6heyqp\\study_input.py",
    "fix": {
      "applicability": "unsafe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 1,
            "row": 7
          },
          "location": {
            "column": 1,
            "row": 6
          }
        }
      ],
      "message": "Remove assignment to unused variable `leftover`"
    },
    "location": {
      "column": 5,
      "row": 6
    },
    "message": "Local variable `leftover` is assigned to but never used",
    "noqa_row": 6,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  }
]
```

</details>

<details>
<summary>C_formatted_visible</summary>

Original: [C_formatted_visible.stdout.txt](../../datasets/results/phase3/trials/exception_binding_boundary--specific_last/black/C_formatted_visible.stdout.txt). Export: [C_formatted_visible.stdout.txt](exports/exception_binding_boundary--specific_last/black/C_formatted_visible.stdout.txt). Replay: [C_formatted_visible.stdout.txt](exports/exception_binding_boundary--specific_last/black/rechecks/C_formatted_visible.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 30,
      "row": 4
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-v4658r0c\\study_input.py",
    "fix": {
      "applicability": "safe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 30,
            "row": 4
          },
          "location": {
            "column": 21,
            "row": 4
          }
        }
      ],
      "message": "Remove assignment to unused variable `error`"
    },
    "location": {
      "column": 25,
      "row": 4
    },
    "message": "Local variable `error` is assigned to but never used",
    "noqa_row": 4,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  }
]
```

</details>

<details>
<summary>D_formatted_underlying</summary>

Original: [D_formatted_underlying.stdout.txt](../../datasets/results/phase3/trials/exception_binding_boundary--specific_last/black/D_formatted_underlying.stdout.txt). Export: [D_formatted_underlying.stdout.txt](exports/exception_binding_boundary--specific_last/black/D_formatted_underlying.stdout.txt). Replay: [D_formatted_underlying.stdout.txt](exports/exception_binding_boundary--specific_last/black/rechecks/D_formatted_underlying.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 30,
      "row": 4
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-yu2mk5p3\\study_input.py",
    "fix": {
      "applicability": "safe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 30,
            "row": 4
          },
          "location": {
            "column": 21,
            "row": 4
          }
        }
      ],
      "message": "Remove assignment to unused variable `error`"
    },
    "location": {
      "column": 25,
      "row": 4
    },
    "message": "Local variable `error` is assigned to but never used",
    "noqa_row": 4,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  },
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 13,
      "row": 6
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-yu2mk5p3\\study_input.py",
    "fix": {
      "applicability": "unsafe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 1,
            "row": 7
          },
          "location": {
            "column": 1,
            "row": 6
          }
        }
      ],
      "message": "Remove assignment to unused variable `leftover`"
    },
    "location": {
      "column": 5,
      "row": 6
    },
    "message": "Local variable `leftover` is assigned to but never used",
    "noqa_row": 6,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  }
]
```

</details>

<a id="comparison-14"></a>

## 14. exception_binding_boundary--specific_last / ruff

**Original label:** Ambiguous. **Proposed review resolution:** Preserved.

Original evidence directory: `datasets/results/phase3/trials/exception_binding_boundary--specific_last/ruff`

Review export directory: `reports/ambiguous-audit/exports/exception_binding_boundary--specific_last/ruff`

### Sources and exact evidence paths

Original source: [before.py](../../datasets/results/phase3/trials/exception_binding_boundary--specific_last/ruff/before.py); byte-identical export: [before.py](exports/exception_binding_boundary--specific_last/ruff/before.py). SHA-256: `996acdf3e25cb67c53be0ccede398ef1d2e0f6cd688a6bfc1aa7cc3885e60110`.

```python
def compute():
    try:
        1 / 0
    except Exception as error:
        pass
    leftover=1  # noqa: F841
```

Formatted source: [after.py](../../datasets/results/phase3/trials/exception_binding_boundary--specific_last/ruff/after.py); byte-identical export: [after.py](exports/exception_binding_boundary--specific_last/ruff/after.py). SHA-256: `b9335eaaaee3e69c02dfb12964e14794ef2d3c711efc75a1d87c6f2720820540`.

```python
def compute():
    try:
        1 / 0
    except Exception as error:
        pass
    leftover = 1  # noqa: F841
```

Original decision: [result.json](../../datasets/results/phase3/trials/exception_binding_boundary--specific_last/ruff/result.json); failure details: [matching.json](../../datasets/results/phase3/trials/exception_binding_boundary--specific_last/ruff/matching.json); formatter invocation: [formatter.command.json](../../datasets/results/phase3/trials/exception_binding_boundary--specific_last/ruff/formatter.command.json). Full byte-identical copies are in the export directory.

### Why the matcher abstained

Exact recorded error: `Expected one relevant AST anchor, found 0`.

F841 points to the exception-handler name `error`. Python represents it as ExceptHandler.name (a string), not an ast.Name with Store context. The primary F841 anchor policy therefore finds no candidate. The separate `leftover` assignment does have a Store Name, but the unsupported `error` prevents complete primary correspondence.

### Noqa placement

| Snapshot | Position (1-based) | Kind | Exact comment | Preceding code on line |
|---|---|---|---|---|
| before | 6:17-29 | inline | `# noqa: F841` | `leftover=1` |
| after | 6:19-31 | inline | `# noqa: F841` | `leftover = 1` |

### Warning identities and visibility

The identities below are review-only, not original automated matcher identities. V = visible; S = suppressed; ranges are 1-based with exclusive end columns.

| Identity / source role | Warning and source slice | Before range | After range | A / B / C / D | Judgment |
|---|---|---|---|---|---|
| `review:F841@$.body[0].body[0].handlers[0].name`; exception-handler binding string field | F841: `error`; Local variable `error` is assigned to but never used | 4:25-4:30 | 4:25-4:30 | V / V / V / V | visible in both |
| `review:F841@$.body[0].body[1].targets[0]`; assignment Store Name | F841: `leftover`; Local variable `leftover` is assigned to but never used | 6:5-6:13 | 6:5-6:13 | S / V / S / V | suppressed in both |

### Evidence-based judgment and human review

The source changes only assignment spacing; executable AST and non-comment code tokens are equal. Exact diagnostic source slices identify the same `as error` handler binding and `leftover` assignment, with unchanged warning messages and roles. F841 `error` is visible in both; F841 `leftover` is suppressed in both. All four saved outputs replay exactly after ignoring only temporary filenames. Neutralizing directive comments makes ordinary lint reproduce the underlying warnings in both snapshots. Proposed resolution: Preserved; no corresponding warning changes its visible/suppressed state.

Human interpretation: Independent human adjudication is pending; this is an AI-assisted proposal. A human should confirm the same exception binding is referenced by F841 and approve any future extension beyond Store Name anchors; no matcher change is proposed as validated here.

Saved replays and comment-neutralized sources: `reports/ambiguous-audit/exports/exception_binding_boundary--specific_last/ruff/rechecks`. All four replay stdout/stderr and command records are saved there; both neutralized ordinary-lint passes reproduce their respective underlying outputs.

### All four original raw Ruff diagnostic outputs

Privacy-derived JSON is preserved below with execution filenames anonymized and fix metadata retained. Empty arrays are actual empty outputs. Each stdout file also has a `.command.json`, `.stderr.txt` and `.diagnostics.json` sibling in both the original and export directories.

<details>
<summary>A_original_visible</summary>

Original: [A_original_visible.stdout.txt](../../datasets/results/phase3/trials/exception_binding_boundary--specific_last/ruff/A_original_visible.stdout.txt). Export: [A_original_visible.stdout.txt](exports/exception_binding_boundary--specific_last/ruff/A_original_visible.stdout.txt). Replay: [A_original_visible.stdout.txt](exports/exception_binding_boundary--specific_last/ruff/rechecks/A_original_visible.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 30,
      "row": 4
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-8_anitqa\\study_input.py",
    "fix": {
      "applicability": "safe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 30,
            "row": 4
          },
          "location": {
            "column": 21,
            "row": 4
          }
        }
      ],
      "message": "Remove assignment to unused variable `error`"
    },
    "location": {
      "column": 25,
      "row": 4
    },
    "message": "Local variable `error` is assigned to but never used",
    "noqa_row": 4,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  }
]
```

</details>

<details>
<summary>B_original_underlying</summary>

Original: [B_original_underlying.stdout.txt](../../datasets/results/phase3/trials/exception_binding_boundary--specific_last/ruff/B_original_underlying.stdout.txt). Export: [B_original_underlying.stdout.txt](exports/exception_binding_boundary--specific_last/ruff/B_original_underlying.stdout.txt). Replay: [B_original_underlying.stdout.txt](exports/exception_binding_boundary--specific_last/ruff/rechecks/B_original_underlying.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 30,
      "row": 4
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-fbtqqf11\\study_input.py",
    "fix": {
      "applicability": "safe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 30,
            "row": 4
          },
          "location": {
            "column": 21,
            "row": 4
          }
        }
      ],
      "message": "Remove assignment to unused variable `error`"
    },
    "location": {
      "column": 25,
      "row": 4
    },
    "message": "Local variable `error` is assigned to but never used",
    "noqa_row": 4,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  },
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 13,
      "row": 6
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-fbtqqf11\\study_input.py",
    "fix": {
      "applicability": "unsafe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 1,
            "row": 7
          },
          "location": {
            "column": 1,
            "row": 6
          }
        }
      ],
      "message": "Remove assignment to unused variable `leftover`"
    },
    "location": {
      "column": 5,
      "row": 6
    },
    "message": "Local variable `leftover` is assigned to but never used",
    "noqa_row": 6,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  }
]
```

</details>

<details>
<summary>C_formatted_visible</summary>

Original: [C_formatted_visible.stdout.txt](../../datasets/results/phase3/trials/exception_binding_boundary--specific_last/ruff/C_formatted_visible.stdout.txt). Export: [C_formatted_visible.stdout.txt](exports/exception_binding_boundary--specific_last/ruff/C_formatted_visible.stdout.txt). Replay: [C_formatted_visible.stdout.txt](exports/exception_binding_boundary--specific_last/ruff/rechecks/C_formatted_visible.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 30,
      "row": 4
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-mfejh5hx\\study_input.py",
    "fix": {
      "applicability": "safe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 30,
            "row": 4
          },
          "location": {
            "column": 21,
            "row": 4
          }
        }
      ],
      "message": "Remove assignment to unused variable `error`"
    },
    "location": {
      "column": 25,
      "row": 4
    },
    "message": "Local variable `error` is assigned to but never used",
    "noqa_row": 4,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  }
]
```

</details>

<details>
<summary>D_formatted_underlying</summary>

Original: [D_formatted_underlying.stdout.txt](../../datasets/results/phase3/trials/exception_binding_boundary--specific_last/ruff/D_formatted_underlying.stdout.txt). Export: [D_formatted_underlying.stdout.txt](exports/exception_binding_boundary--specific_last/ruff/D_formatted_underlying.stdout.txt). Replay: [D_formatted_underlying.stdout.txt](exports/exception_binding_boundary--specific_last/ruff/rechecks/D_formatted_underlying.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 30,
      "row": 4
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-fumu2pbh\\study_input.py",
    "fix": {
      "applicability": "safe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 30,
            "row": 4
          },
          "location": {
            "column": 21,
            "row": 4
          }
        }
      ],
      "message": "Remove assignment to unused variable `error`"
    },
    "location": {
      "column": 25,
      "row": 4
    },
    "message": "Local variable `error` is assigned to but never used",
    "noqa_row": 4,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  },
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 13,
      "row": 6
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-fumu2pbh\\study_input.py",
    "fix": {
      "applicability": "unsafe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 1,
            "row": 7
          },
          "location": {
            "column": 1,
            "row": 6
          }
        }
      ],
      "message": "Remove assignment to unused variable `leftover`"
    },
    "location": {
      "column": 5,
      "row": 6
    },
    "message": "Local variable `leftover` is assigned to but never used",
    "noqa_row": 6,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  }
]
```

</details>

<a id="comparison-15"></a>

## 15. exception_binding_boundary--standalone_first / black

**Original label:** Ambiguous. **Proposed review resolution:** Preserved.

Original evidence directory: `datasets/results/phase3/trials/exception_binding_boundary--standalone_first/black`

Review export directory: `reports/ambiguous-audit/exports/exception_binding_boundary--standalone_first/black`

### Sources and exact evidence paths

Original source: [before.py](../../datasets/results/phase3/trials/exception_binding_boundary--standalone_first/black/before.py); byte-identical export: [before.py](exports/exception_binding_boundary--standalone_first/black/before.py). SHA-256: `e2d3ece8de3af11feb2171c324b867f58a82e825c5fa1d77ab8388d1676e2033`.

```python
def compute():
    try:
        1 / 0
    # noqa: F841
    except Exception as error:
        pass
    leftover=1
```

Formatted source: [after.py](../../datasets/results/phase3/trials/exception_binding_boundary--standalone_first/black/after.py); byte-identical export: [after.py](exports/exception_binding_boundary--standalone_first/black/after.py). SHA-256: `922b53194ca03031d753bc95b3a22653af4568c854feb3f8ce9e012ecfbdc2df`.

```python
def compute():
    try:
        1 / 0
    # noqa: F841
    except Exception as error:
        pass
    leftover = 1
```

Original decision: [result.json](../../datasets/results/phase3/trials/exception_binding_boundary--standalone_first/black/result.json); failure details: [matching.json](../../datasets/results/phase3/trials/exception_binding_boundary--standalone_first/black/matching.json); formatter invocation: [formatter.command.json](../../datasets/results/phase3/trials/exception_binding_boundary--standalone_first/black/formatter.command.json). Full byte-identical copies are in the export directory.

### Why the matcher abstained

Exact recorded error: `Expected one relevant AST anchor, found 0`.

F841 points to the exception-handler name `error`. Python represents it as ExceptHandler.name (a string), not an ast.Name with Store context. The primary F841 anchor policy therefore finds no candidate. The separate `leftover` assignment does have a Store Name, but the unsupported `error` prevents complete primary correspondence.

### Noqa placement

| Snapshot | Position (1-based) | Kind | Exact comment | Preceding code on line |
|---|---|---|---|---|
| before | 4:5-17 | standalone | `# noqa: F841` | `` |
| after | 4:5-17 | standalone | `# noqa: F841` | `` |

### Warning identities and visibility

The identities below are review-only, not original automated matcher identities. V = visible; S = suppressed; ranges are 1-based with exclusive end columns.

| Identity / source role | Warning and source slice | Before range | After range | A / B / C / D | Judgment |
|---|---|---|---|---|---|
| `review:F841@$.body[0].body[0].handlers[0].name`; exception-handler binding string field | F841: `error`; Local variable `error` is assigned to but never used | 5:25-5:30 | 5:25-5:30 | V / V / V / V | visible in both |
| `review:F841@$.body[0].body[1].targets[0]`; assignment Store Name | F841: `leftover`; Local variable `leftover` is assigned to but never used | 7:5-7:13 | 7:5-7:13 | V / V / V / V | visible in both |

### Evidence-based judgment and human review

The source changes only assignment spacing; executable AST and non-comment code tokens are equal. Exact diagnostic source slices identify the same `as error` handler binding and `leftover` assignment, with unchanged warning messages and roles. F841 `error` is visible in both; F841 `leftover` is visible in both. All four saved outputs replay exactly after ignoring only temporary filenames. Neutralizing directive comments makes ordinary lint reproduce the underlying warnings in both snapshots. Proposed resolution: Preserved; no corresponding warning changes its visible/suppressed state.

Human interpretation: Independent human adjudication is pending; this is an AI-assisted proposal. A human should confirm the same exception binding is referenced by F841 and approve any future extension beyond Store Name anchors; no matcher change is proposed as validated here. The standalone directive suppresses neither selected warning in the measured passes. Intended next-line suppression cannot be inferred; this does not make observed visibility uncertain.

Saved replays and comment-neutralized sources: `reports/ambiguous-audit/exports/exception_binding_boundary--standalone_first/black/rechecks`. All four replay stdout/stderr and command records are saved there; both neutralized ordinary-lint passes reproduce their respective underlying outputs.

### All four original raw Ruff diagnostic outputs

Privacy-derived JSON is preserved below with execution filenames anonymized and fix metadata retained. Empty arrays are actual empty outputs. Each stdout file also has a `.command.json`, `.stderr.txt` and `.diagnostics.json` sibling in both the original and export directories.

<details>
<summary>A_original_visible</summary>

Original: [A_original_visible.stdout.txt](../../datasets/results/phase3/trials/exception_binding_boundary--standalone_first/black/A_original_visible.stdout.txt). Export: [A_original_visible.stdout.txt](exports/exception_binding_boundary--standalone_first/black/A_original_visible.stdout.txt). Replay: [A_original_visible.stdout.txt](exports/exception_binding_boundary--standalone_first/black/rechecks/A_original_visible.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 30,
      "row": 5
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-wxfy2apc\\study_input.py",
    "fix": {
      "applicability": "safe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 30,
            "row": 5
          },
          "location": {
            "column": 21,
            "row": 5
          }
        }
      ],
      "message": "Remove assignment to unused variable `error`"
    },
    "location": {
      "column": 25,
      "row": 5
    },
    "message": "Local variable `error` is assigned to but never used",
    "noqa_row": 5,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  },
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 13,
      "row": 7
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-wxfy2apc\\study_input.py",
    "fix": {
      "applicability": "unsafe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 1,
            "row": 8
          },
          "location": {
            "column": 1,
            "row": 7
          }
        }
      ],
      "message": "Remove assignment to unused variable `leftover`"
    },
    "location": {
      "column": 5,
      "row": 7
    },
    "message": "Local variable `leftover` is assigned to but never used",
    "noqa_row": 7,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  }
]
```

</details>

<details>
<summary>B_original_underlying</summary>

Original: [B_original_underlying.stdout.txt](../../datasets/results/phase3/trials/exception_binding_boundary--standalone_first/black/B_original_underlying.stdout.txt). Export: [B_original_underlying.stdout.txt](exports/exception_binding_boundary--standalone_first/black/B_original_underlying.stdout.txt). Replay: [B_original_underlying.stdout.txt](exports/exception_binding_boundary--standalone_first/black/rechecks/B_original_underlying.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 30,
      "row": 5
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-s9ed_6i1\\study_input.py",
    "fix": {
      "applicability": "safe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 30,
            "row": 5
          },
          "location": {
            "column": 21,
            "row": 5
          }
        }
      ],
      "message": "Remove assignment to unused variable `error`"
    },
    "location": {
      "column": 25,
      "row": 5
    },
    "message": "Local variable `error` is assigned to but never used",
    "noqa_row": 5,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  },
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 13,
      "row": 7
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-s9ed_6i1\\study_input.py",
    "fix": {
      "applicability": "unsafe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 1,
            "row": 8
          },
          "location": {
            "column": 1,
            "row": 7
          }
        }
      ],
      "message": "Remove assignment to unused variable `leftover`"
    },
    "location": {
      "column": 5,
      "row": 7
    },
    "message": "Local variable `leftover` is assigned to but never used",
    "noqa_row": 7,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  }
]
```

</details>

<details>
<summary>C_formatted_visible</summary>

Original: [C_formatted_visible.stdout.txt](../../datasets/results/phase3/trials/exception_binding_boundary--standalone_first/black/C_formatted_visible.stdout.txt). Export: [C_formatted_visible.stdout.txt](exports/exception_binding_boundary--standalone_first/black/C_formatted_visible.stdout.txt). Replay: [C_formatted_visible.stdout.txt](exports/exception_binding_boundary--standalone_first/black/rechecks/C_formatted_visible.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 30,
      "row": 5
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-it_pndtc\\study_input.py",
    "fix": {
      "applicability": "safe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 30,
            "row": 5
          },
          "location": {
            "column": 21,
            "row": 5
          }
        }
      ],
      "message": "Remove assignment to unused variable `error`"
    },
    "location": {
      "column": 25,
      "row": 5
    },
    "message": "Local variable `error` is assigned to but never used",
    "noqa_row": 5,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  },
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 13,
      "row": 7
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-it_pndtc\\study_input.py",
    "fix": {
      "applicability": "unsafe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 1,
            "row": 8
          },
          "location": {
            "column": 1,
            "row": 7
          }
        }
      ],
      "message": "Remove assignment to unused variable `leftover`"
    },
    "location": {
      "column": 5,
      "row": 7
    },
    "message": "Local variable `leftover` is assigned to but never used",
    "noqa_row": 7,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  }
]
```

</details>

<details>
<summary>D_formatted_underlying</summary>

Original: [D_formatted_underlying.stdout.txt](../../datasets/results/phase3/trials/exception_binding_boundary--standalone_first/black/D_formatted_underlying.stdout.txt). Export: [D_formatted_underlying.stdout.txt](exports/exception_binding_boundary--standalone_first/black/D_formatted_underlying.stdout.txt). Replay: [D_formatted_underlying.stdout.txt](exports/exception_binding_boundary--standalone_first/black/rechecks/D_formatted_underlying.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 30,
      "row": 5
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-mi10tqw_\\study_input.py",
    "fix": {
      "applicability": "safe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 30,
            "row": 5
          },
          "location": {
            "column": 21,
            "row": 5
          }
        }
      ],
      "message": "Remove assignment to unused variable `error`"
    },
    "location": {
      "column": 25,
      "row": 5
    },
    "message": "Local variable `error` is assigned to but never used",
    "noqa_row": 5,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  },
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 13,
      "row": 7
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-mi10tqw_\\study_input.py",
    "fix": {
      "applicability": "unsafe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 1,
            "row": 8
          },
          "location": {
            "column": 1,
            "row": 7
          }
        }
      ],
      "message": "Remove assignment to unused variable `leftover`"
    },
    "location": {
      "column": 5,
      "row": 7
    },
    "message": "Local variable `leftover` is assigned to but never used",
    "noqa_row": 7,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  }
]
```

</details>

<a id="comparison-16"></a>

## 16. exception_binding_boundary--standalone_first / ruff

**Original label:** Ambiguous. **Proposed review resolution:** Preserved.

Original evidence directory: `datasets/results/phase3/trials/exception_binding_boundary--standalone_first/ruff`

Review export directory: `reports/ambiguous-audit/exports/exception_binding_boundary--standalone_first/ruff`

### Sources and exact evidence paths

Original source: [before.py](../../datasets/results/phase3/trials/exception_binding_boundary--standalone_first/ruff/before.py); byte-identical export: [before.py](exports/exception_binding_boundary--standalone_first/ruff/before.py). SHA-256: `e2d3ece8de3af11feb2171c324b867f58a82e825c5fa1d77ab8388d1676e2033`.

```python
def compute():
    try:
        1 / 0
    # noqa: F841
    except Exception as error:
        pass
    leftover=1
```

Formatted source: [after.py](../../datasets/results/phase3/trials/exception_binding_boundary--standalone_first/ruff/after.py); byte-identical export: [after.py](exports/exception_binding_boundary--standalone_first/ruff/after.py). SHA-256: `922b53194ca03031d753bc95b3a22653af4568c854feb3f8ce9e012ecfbdc2df`.

```python
def compute():
    try:
        1 / 0
    # noqa: F841
    except Exception as error:
        pass
    leftover = 1
```

Original decision: [result.json](../../datasets/results/phase3/trials/exception_binding_boundary--standalone_first/ruff/result.json); failure details: [matching.json](../../datasets/results/phase3/trials/exception_binding_boundary--standalone_first/ruff/matching.json); formatter invocation: [formatter.command.json](../../datasets/results/phase3/trials/exception_binding_boundary--standalone_first/ruff/formatter.command.json). Full byte-identical copies are in the export directory.

### Why the matcher abstained

Exact recorded error: `Expected one relevant AST anchor, found 0`.

F841 points to the exception-handler name `error`. Python represents it as ExceptHandler.name (a string), not an ast.Name with Store context. The primary F841 anchor policy therefore finds no candidate. The separate `leftover` assignment does have a Store Name, but the unsupported `error` prevents complete primary correspondence.

### Noqa placement

| Snapshot | Position (1-based) | Kind | Exact comment | Preceding code on line |
|---|---|---|---|---|
| before | 4:5-17 | standalone | `# noqa: F841` | `` |
| after | 4:5-17 | standalone | `# noqa: F841` | `` |

### Warning identities and visibility

The identities below are review-only, not original automated matcher identities. V = visible; S = suppressed; ranges are 1-based with exclusive end columns.

| Identity / source role | Warning and source slice | Before range | After range | A / B / C / D | Judgment |
|---|---|---|---|---|---|
| `review:F841@$.body[0].body[0].handlers[0].name`; exception-handler binding string field | F841: `error`; Local variable `error` is assigned to but never used | 5:25-5:30 | 5:25-5:30 | V / V / V / V | visible in both |
| `review:F841@$.body[0].body[1].targets[0]`; assignment Store Name | F841: `leftover`; Local variable `leftover` is assigned to but never used | 7:5-7:13 | 7:5-7:13 | V / V / V / V | visible in both |

### Evidence-based judgment and human review

The source changes only assignment spacing; executable AST and non-comment code tokens are equal. Exact diagnostic source slices identify the same `as error` handler binding and `leftover` assignment, with unchanged warning messages and roles. F841 `error` is visible in both; F841 `leftover` is visible in both. All four saved outputs replay exactly after ignoring only temporary filenames. Neutralizing directive comments makes ordinary lint reproduce the underlying warnings in both snapshots. Proposed resolution: Preserved; no corresponding warning changes its visible/suppressed state.

Human interpretation: Independent human adjudication is pending; this is an AI-assisted proposal. A human should confirm the same exception binding is referenced by F841 and approve any future extension beyond Store Name anchors; no matcher change is proposed as validated here. The standalone directive suppresses neither selected warning in the measured passes. Intended next-line suppression cannot be inferred; this does not make observed visibility uncertain.

Saved replays and comment-neutralized sources: `reports/ambiguous-audit/exports/exception_binding_boundary--standalone_first/ruff/rechecks`. All four replay stdout/stderr and command records are saved there; both neutralized ordinary-lint passes reproduce their respective underlying outputs.

### All four original raw Ruff diagnostic outputs

Privacy-derived JSON is preserved below with execution filenames anonymized and fix metadata retained. Empty arrays are actual empty outputs. Each stdout file also has a `.command.json`, `.stderr.txt` and `.diagnostics.json` sibling in both the original and export directories.

<details>
<summary>A_original_visible</summary>

Original: [A_original_visible.stdout.txt](../../datasets/results/phase3/trials/exception_binding_boundary--standalone_first/ruff/A_original_visible.stdout.txt). Export: [A_original_visible.stdout.txt](exports/exception_binding_boundary--standalone_first/ruff/A_original_visible.stdout.txt). Replay: [A_original_visible.stdout.txt](exports/exception_binding_boundary--standalone_first/ruff/rechecks/A_original_visible.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 30,
      "row": 5
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-lfho_r17\\study_input.py",
    "fix": {
      "applicability": "safe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 30,
            "row": 5
          },
          "location": {
            "column": 21,
            "row": 5
          }
        }
      ],
      "message": "Remove assignment to unused variable `error`"
    },
    "location": {
      "column": 25,
      "row": 5
    },
    "message": "Local variable `error` is assigned to but never used",
    "noqa_row": 5,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  },
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 13,
      "row": 7
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-lfho_r17\\study_input.py",
    "fix": {
      "applicability": "unsafe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 1,
            "row": 8
          },
          "location": {
            "column": 1,
            "row": 7
          }
        }
      ],
      "message": "Remove assignment to unused variable `leftover`"
    },
    "location": {
      "column": 5,
      "row": 7
    },
    "message": "Local variable `leftover` is assigned to but never used",
    "noqa_row": 7,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  }
]
```

</details>

<details>
<summary>B_original_underlying</summary>

Original: [B_original_underlying.stdout.txt](../../datasets/results/phase3/trials/exception_binding_boundary--standalone_first/ruff/B_original_underlying.stdout.txt). Export: [B_original_underlying.stdout.txt](exports/exception_binding_boundary--standalone_first/ruff/B_original_underlying.stdout.txt). Replay: [B_original_underlying.stdout.txt](exports/exception_binding_boundary--standalone_first/ruff/rechecks/B_original_underlying.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 30,
      "row": 5
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-6iz5g_yb\\study_input.py",
    "fix": {
      "applicability": "safe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 30,
            "row": 5
          },
          "location": {
            "column": 21,
            "row": 5
          }
        }
      ],
      "message": "Remove assignment to unused variable `error`"
    },
    "location": {
      "column": 25,
      "row": 5
    },
    "message": "Local variable `error` is assigned to but never used",
    "noqa_row": 5,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  },
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 13,
      "row": 7
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-6iz5g_yb\\study_input.py",
    "fix": {
      "applicability": "unsafe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 1,
            "row": 8
          },
          "location": {
            "column": 1,
            "row": 7
          }
        }
      ],
      "message": "Remove assignment to unused variable `leftover`"
    },
    "location": {
      "column": 5,
      "row": 7
    },
    "message": "Local variable `leftover` is assigned to but never used",
    "noqa_row": 7,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  }
]
```

</details>

<details>
<summary>C_formatted_visible</summary>

Original: [C_formatted_visible.stdout.txt](../../datasets/results/phase3/trials/exception_binding_boundary--standalone_first/ruff/C_formatted_visible.stdout.txt). Export: [C_formatted_visible.stdout.txt](exports/exception_binding_boundary--standalone_first/ruff/C_formatted_visible.stdout.txt). Replay: [C_formatted_visible.stdout.txt](exports/exception_binding_boundary--standalone_first/ruff/rechecks/C_formatted_visible.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 30,
      "row": 5
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-ll1i6shi\\study_input.py",
    "fix": {
      "applicability": "safe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 30,
            "row": 5
          },
          "location": {
            "column": 21,
            "row": 5
          }
        }
      ],
      "message": "Remove assignment to unused variable `error`"
    },
    "location": {
      "column": 25,
      "row": 5
    },
    "message": "Local variable `error` is assigned to but never used",
    "noqa_row": 5,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  },
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 13,
      "row": 7
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-ll1i6shi\\study_input.py",
    "fix": {
      "applicability": "unsafe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 1,
            "row": 8
          },
          "location": {
            "column": 1,
            "row": 7
          }
        }
      ],
      "message": "Remove assignment to unused variable `leftover`"
    },
    "location": {
      "column": 5,
      "row": 7
    },
    "message": "Local variable `leftover` is assigned to but never used",
    "noqa_row": 7,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  }
]
```

</details>

<details>
<summary>D_formatted_underlying</summary>

Original: [D_formatted_underlying.stdout.txt](../../datasets/results/phase3/trials/exception_binding_boundary--standalone_first/ruff/D_formatted_underlying.stdout.txt). Export: [D_formatted_underlying.stdout.txt](exports/exception_binding_boundary--standalone_first/ruff/D_formatted_underlying.stdout.txt). Replay: [D_formatted_underlying.stdout.txt](exports/exception_binding_boundary--standalone_first/ruff/rechecks/D_formatted_underlying.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 30,
      "row": 5
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-qgvafb_y\\study_input.py",
    "fix": {
      "applicability": "safe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 30,
            "row": 5
          },
          "location": {
            "column": 21,
            "row": 5
          }
        }
      ],
      "message": "Remove assignment to unused variable `error`"
    },
    "location": {
      "column": 25,
      "row": 5
    },
    "message": "Local variable `error` is assigned to but never used",
    "noqa_row": 5,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  },
  {
    "cell": null,
    "code": "F841",
    "end_location": {
      "column": 13,
      "row": 7
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-qgvafb_y\\study_input.py",
    "fix": {
      "applicability": "unsafe",
      "edits": [
        {
          "content": "",
          "end_location": {
            "column": 1,
            "row": 8
          },
          "location": {
            "column": 1,
            "row": 7
          }
        }
      ],
      "message": "Remove assignment to unused variable `leftover`"
    },
    "location": {
      "column": 5,
      "row": 7
    },
    "message": "Local variable `leftover` is assigned to but never used",
    "noqa_row": 7,
    "url": "https://docs.astral.sh/ruff/rules/unused-variable"
  }
]
```

</details>

<a id="comparison-17"></a>

## 17. fstring_boundary--blanket_first / black

**Original label:** Ambiguous. **Proposed review resolution:** Preserved.

Original evidence directory: `datasets/results/phase3/trials/fstring_boundary--blanket_first/black`

Review export directory: `reports/ambiguous-audit/exports/fstring_boundary--blanket_first/black`

### Sources and exact evidence paths

Original source: [before.py](../../datasets/results/phase3/trials/fstring_boundary--blanket_first/black/before.py); byte-identical export: [before.py](exports/fstring_boundary--blanket_first/black/before.py). SHA-256: `f1b850843425b49f5e0dc87a14d533edf5831fed540d1dcd1de19df0aa147eda`.

```python
text = f"{missing_a}"  # noqa
other = missing_b
```

Formatted source: [after.py](../../datasets/results/phase3/trials/fstring_boundary--blanket_first/black/after.py); byte-identical export: [after.py](exports/fstring_boundary--blanket_first/black/after.py). SHA-256: `f1b850843425b49f5e0dc87a14d533edf5831fed540d1dcd1de19df0aa147eda`.

```python
text = f"{missing_a}"  # noqa
other = missing_b
```

Original decision: [result.json](../../datasets/results/phase3/trials/fstring_boundary--blanket_first/black/result.json); failure details: [matching.json](../../datasets/results/phase3/trials/fstring_boundary--blanket_first/black/matching.json); formatter invocation: [formatter.command.json](../../datasets/results/phase3/trials/fstring_boundary--blanket_first/black/formatter.command.json). Full byte-identical copies are in the export directory.

### Why the matcher abstained

Exact recorded error: `Diagnostic or construct does not align with complete code tokens`.

F821 points to `missing_a` inside a formatted-value expression. Python 3.11 tokenize emits the whole f-string as a STRING token, so the embedded identifier span is not a complete token span under the primary matcher. This is a tokenization/coverage boundary, not evidence of a changed suppression.

### Noqa placement

| Snapshot | Position (1-based) | Kind | Exact comment | Preceding code on line |
|---|---|---|---|---|
| before | 1:24-30 | inline | `# noqa` | `text = f"{missing_a}"` |
| after | 1:24-30 | inline | `# noqa` | `text = f"{missing_a}"` |

### Warning identities and visibility

The identities below are review-only, not original automated matcher identities. V = visible; S = suppressed; ranges are 1-based with exclusive end columns.

| Identity / source role | Warning and source slice | Before range | After range | A / B / C / D | Judgment |
|---|---|---|---|---|---|
| `review:F821@$.body[0].value.values[0].value`; load Name | F821: `missing_a`; Undefined name `missing_a` | 1:11-1:20 | 1:11-1:20 | S / V / S / V | suppressed in both |
| `review:F821@$.body[1].value`; load Name | F821: `missing_b`; Undefined name `missing_b` | 2:9-2:18 | 2:9-2:18 | V / V / V / V | visible in both |

### Evidence-based judgment and human review

Original and formatted source are byte-identical. Full underlying and visible warnings reproduce; corresponding occurrences cannot move in an identical snapshot. F821 `missing_a` is suppressed in both; F821 `missing_b` is visible in both. All four saved outputs replay exactly after ignoring only temporary filenames. Neutralizing directive comments makes ordinary lint reproduce the underlying warnings in both snapshots. Proposed resolution: Preserved; no corresponding warning changes its visible/suppressed state.

Human interpretation: Independent human adjudication is pending; this is an AI-assisted proposal.

Saved replays and comment-neutralized sources: `reports/ambiguous-audit/exports/fstring_boundary--blanket_first/black/rechecks`. All four replay stdout/stderr and command records are saved there; both neutralized ordinary-lint passes reproduce their respective underlying outputs.

### All four original raw Ruff diagnostic outputs

Privacy-derived JSON is preserved below with execution filenames anonymized and fix metadata retained. Empty arrays are actual empty outputs. Each stdout file also has a `.command.json`, `.stderr.txt` and `.diagnostics.json` sibling in both the original and export directories.

<details>
<summary>A_original_visible</summary>

Original: [A_original_visible.stdout.txt](../../datasets/results/phase3/trials/fstring_boundary--blanket_first/black/A_original_visible.stdout.txt). Export: [A_original_visible.stdout.txt](exports/fstring_boundary--blanket_first/black/A_original_visible.stdout.txt). Replay: [A_original_visible.stdout.txt](exports/fstring_boundary--blanket_first/black/rechecks/A_original_visible.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 18,
      "row": 2
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-n3nhvwpr\\study_input.py",
    "fix": null,
    "location": {
      "column": 9,
      "row": 2
    },
    "message": "Undefined name `missing_b`",
    "noqa_row": 2,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  }
]
```

</details>

<details>
<summary>B_original_underlying</summary>

Original: [B_original_underlying.stdout.txt](../../datasets/results/phase3/trials/fstring_boundary--blanket_first/black/B_original_underlying.stdout.txt). Export: [B_original_underlying.stdout.txt](exports/fstring_boundary--blanket_first/black/B_original_underlying.stdout.txt). Replay: [B_original_underlying.stdout.txt](exports/fstring_boundary--blanket_first/black/rechecks/B_original_underlying.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 20,
      "row": 1
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-c8oomavx\\study_input.py",
    "fix": null,
    "location": {
      "column": 11,
      "row": 1
    },
    "message": "Undefined name `missing_a`",
    "noqa_row": 1,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  },
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 18,
      "row": 2
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-c8oomavx\\study_input.py",
    "fix": null,
    "location": {
      "column": 9,
      "row": 2
    },
    "message": "Undefined name `missing_b`",
    "noqa_row": 2,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  }
]
```

</details>

<details>
<summary>C_formatted_visible</summary>

Original: [C_formatted_visible.stdout.txt](../../datasets/results/phase3/trials/fstring_boundary--blanket_first/black/C_formatted_visible.stdout.txt). Export: [C_formatted_visible.stdout.txt](exports/fstring_boundary--blanket_first/black/C_formatted_visible.stdout.txt). Replay: [C_formatted_visible.stdout.txt](exports/fstring_boundary--blanket_first/black/rechecks/C_formatted_visible.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 18,
      "row": 2
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-4p6yrc1o\\study_input.py",
    "fix": null,
    "location": {
      "column": 9,
      "row": 2
    },
    "message": "Undefined name `missing_b`",
    "noqa_row": 2,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  }
]
```

</details>

<details>
<summary>D_formatted_underlying</summary>

Original: [D_formatted_underlying.stdout.txt](../../datasets/results/phase3/trials/fstring_boundary--blanket_first/black/D_formatted_underlying.stdout.txt). Export: [D_formatted_underlying.stdout.txt](exports/fstring_boundary--blanket_first/black/D_formatted_underlying.stdout.txt). Replay: [D_formatted_underlying.stdout.txt](exports/fstring_boundary--blanket_first/black/rechecks/D_formatted_underlying.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 20,
      "row": 1
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-7e9lqlnx\\study_input.py",
    "fix": null,
    "location": {
      "column": 11,
      "row": 1
    },
    "message": "Undefined name `missing_a`",
    "noqa_row": 1,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  },
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 18,
      "row": 2
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-7e9lqlnx\\study_input.py",
    "fix": null,
    "location": {
      "column": 9,
      "row": 2
    },
    "message": "Undefined name `missing_b`",
    "noqa_row": 2,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  }
]
```

</details>

<a id="comparison-18"></a>

## 18. fstring_boundary--blanket_first / ruff

**Original label:** Ambiguous. **Proposed review resolution:** Preserved.

Original evidence directory: `datasets/results/phase3/trials/fstring_boundary--blanket_first/ruff`

Review export directory: `reports/ambiguous-audit/exports/fstring_boundary--blanket_first/ruff`

### Sources and exact evidence paths

Original source: [before.py](../../datasets/results/phase3/trials/fstring_boundary--blanket_first/ruff/before.py); byte-identical export: [before.py](exports/fstring_boundary--blanket_first/ruff/before.py). SHA-256: `f1b850843425b49f5e0dc87a14d533edf5831fed540d1dcd1de19df0aa147eda`.

```python
text = f"{missing_a}"  # noqa
other = missing_b
```

Formatted source: [after.py](../../datasets/results/phase3/trials/fstring_boundary--blanket_first/ruff/after.py); byte-identical export: [after.py](exports/fstring_boundary--blanket_first/ruff/after.py). SHA-256: `f1b850843425b49f5e0dc87a14d533edf5831fed540d1dcd1de19df0aa147eda`.

```python
text = f"{missing_a}"  # noqa
other = missing_b
```

Original decision: [result.json](../../datasets/results/phase3/trials/fstring_boundary--blanket_first/ruff/result.json); failure details: [matching.json](../../datasets/results/phase3/trials/fstring_boundary--blanket_first/ruff/matching.json); formatter invocation: [formatter.command.json](../../datasets/results/phase3/trials/fstring_boundary--blanket_first/ruff/formatter.command.json). Full byte-identical copies are in the export directory.

### Why the matcher abstained

Exact recorded error: `Diagnostic or construct does not align with complete code tokens`.

F821 points to `missing_a` inside a formatted-value expression. Python 3.11 tokenize emits the whole f-string as a STRING token, so the embedded identifier span is not a complete token span under the primary matcher. This is a tokenization/coverage boundary, not evidence of a changed suppression.

### Noqa placement

| Snapshot | Position (1-based) | Kind | Exact comment | Preceding code on line |
|---|---|---|---|---|
| before | 1:24-30 | inline | `# noqa` | `text = f"{missing_a}"` |
| after | 1:24-30 | inline | `# noqa` | `text = f"{missing_a}"` |

### Warning identities and visibility

The identities below are review-only, not original automated matcher identities. V = visible; S = suppressed; ranges are 1-based with exclusive end columns.

| Identity / source role | Warning and source slice | Before range | After range | A / B / C / D | Judgment |
|---|---|---|---|---|---|
| `review:F821@$.body[0].value.values[0].value`; load Name | F821: `missing_a`; Undefined name `missing_a` | 1:11-1:20 | 1:11-1:20 | S / V / S / V | suppressed in both |
| `review:F821@$.body[1].value`; load Name | F821: `missing_b`; Undefined name `missing_b` | 2:9-2:18 | 2:9-2:18 | V / V / V / V | visible in both |

### Evidence-based judgment and human review

Original and formatted source are byte-identical. Full underlying and visible warnings reproduce; corresponding occurrences cannot move in an identical snapshot. F821 `missing_a` is suppressed in both; F821 `missing_b` is visible in both. All four saved outputs replay exactly after ignoring only temporary filenames. Neutralizing directive comments makes ordinary lint reproduce the underlying warnings in both snapshots. Proposed resolution: Preserved; no corresponding warning changes its visible/suppressed state.

Human interpretation: Independent human adjudication is pending; this is an AI-assisted proposal.

Saved replays and comment-neutralized sources: `reports/ambiguous-audit/exports/fstring_boundary--blanket_first/ruff/rechecks`. All four replay stdout/stderr and command records are saved there; both neutralized ordinary-lint passes reproduce their respective underlying outputs.

### All four original raw Ruff diagnostic outputs

Privacy-derived JSON is preserved below with execution filenames anonymized and fix metadata retained. Empty arrays are actual empty outputs. Each stdout file also has a `.command.json`, `.stderr.txt` and `.diagnostics.json` sibling in both the original and export directories.

<details>
<summary>A_original_visible</summary>

Original: [A_original_visible.stdout.txt](../../datasets/results/phase3/trials/fstring_boundary--blanket_first/ruff/A_original_visible.stdout.txt). Export: [A_original_visible.stdout.txt](exports/fstring_boundary--blanket_first/ruff/A_original_visible.stdout.txt). Replay: [A_original_visible.stdout.txt](exports/fstring_boundary--blanket_first/ruff/rechecks/A_original_visible.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 18,
      "row": 2
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-k804rw6q\\study_input.py",
    "fix": null,
    "location": {
      "column": 9,
      "row": 2
    },
    "message": "Undefined name `missing_b`",
    "noqa_row": 2,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  }
]
```

</details>

<details>
<summary>B_original_underlying</summary>

Original: [B_original_underlying.stdout.txt](../../datasets/results/phase3/trials/fstring_boundary--blanket_first/ruff/B_original_underlying.stdout.txt). Export: [B_original_underlying.stdout.txt](exports/fstring_boundary--blanket_first/ruff/B_original_underlying.stdout.txt). Replay: [B_original_underlying.stdout.txt](exports/fstring_boundary--blanket_first/ruff/rechecks/B_original_underlying.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 20,
      "row": 1
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-6yvotaza\\study_input.py",
    "fix": null,
    "location": {
      "column": 11,
      "row": 1
    },
    "message": "Undefined name `missing_a`",
    "noqa_row": 1,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  },
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 18,
      "row": 2
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-6yvotaza\\study_input.py",
    "fix": null,
    "location": {
      "column": 9,
      "row": 2
    },
    "message": "Undefined name `missing_b`",
    "noqa_row": 2,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  }
]
```

</details>

<details>
<summary>C_formatted_visible</summary>

Original: [C_formatted_visible.stdout.txt](../../datasets/results/phase3/trials/fstring_boundary--blanket_first/ruff/C_formatted_visible.stdout.txt). Export: [C_formatted_visible.stdout.txt](exports/fstring_boundary--blanket_first/ruff/C_formatted_visible.stdout.txt). Replay: [C_formatted_visible.stdout.txt](exports/fstring_boundary--blanket_first/ruff/rechecks/C_formatted_visible.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 18,
      "row": 2
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-wmp6bw_e\\study_input.py",
    "fix": null,
    "location": {
      "column": 9,
      "row": 2
    },
    "message": "Undefined name `missing_b`",
    "noqa_row": 2,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  }
]
```

</details>

<details>
<summary>D_formatted_underlying</summary>

Original: [D_formatted_underlying.stdout.txt](../../datasets/results/phase3/trials/fstring_boundary--blanket_first/ruff/D_formatted_underlying.stdout.txt). Export: [D_formatted_underlying.stdout.txt](exports/fstring_boundary--blanket_first/ruff/D_formatted_underlying.stdout.txt). Replay: [D_formatted_underlying.stdout.txt](exports/fstring_boundary--blanket_first/ruff/rechecks/D_formatted_underlying.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 20,
      "row": 1
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-3m_itvax\\study_input.py",
    "fix": null,
    "location": {
      "column": 11,
      "row": 1
    },
    "message": "Undefined name `missing_a`",
    "noqa_row": 1,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  },
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 18,
      "row": 2
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-3m_itvax\\study_input.py",
    "fix": null,
    "location": {
      "column": 9,
      "row": 2
    },
    "message": "Undefined name `missing_b`",
    "noqa_row": 2,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  }
]
```

</details>

<a id="comparison-19"></a>

## 19. fstring_boundary--blanket_last / black

**Original label:** Ambiguous. **Proposed review resolution:** Preserved.

Original evidence directory: `datasets/results/phase3/trials/fstring_boundary--blanket_last/black`

Review export directory: `reports/ambiguous-audit/exports/fstring_boundary--blanket_last/black`

### Sources and exact evidence paths

Original source: [before.py](../../datasets/results/phase3/trials/fstring_boundary--blanket_last/black/before.py); byte-identical export: [before.py](exports/fstring_boundary--blanket_last/black/before.py). SHA-256: `40f62d6dc6ef7aa89a355e7fc8a5ee70537e764f131f22cb6d03e1681e243e28`.

```python
text = f"{missing_a}"
other = missing_b  # noqa
```

Formatted source: [after.py](../../datasets/results/phase3/trials/fstring_boundary--blanket_last/black/after.py); byte-identical export: [after.py](exports/fstring_boundary--blanket_last/black/after.py). SHA-256: `40f62d6dc6ef7aa89a355e7fc8a5ee70537e764f131f22cb6d03e1681e243e28`.

```python
text = f"{missing_a}"
other = missing_b  # noqa
```

Original decision: [result.json](../../datasets/results/phase3/trials/fstring_boundary--blanket_last/black/result.json); failure details: [matching.json](../../datasets/results/phase3/trials/fstring_boundary--blanket_last/black/matching.json); formatter invocation: [formatter.command.json](../../datasets/results/phase3/trials/fstring_boundary--blanket_last/black/formatter.command.json). Full byte-identical copies are in the export directory.

### Why the matcher abstained

Exact recorded error: `Diagnostic or construct does not align with complete code tokens`.

F821 points to `missing_a` inside a formatted-value expression. Python 3.11 tokenize emits the whole f-string as a STRING token, so the embedded identifier span is not a complete token span under the primary matcher. This is a tokenization/coverage boundary, not evidence of a changed suppression.

### Noqa placement

| Snapshot | Position (1-based) | Kind | Exact comment | Preceding code on line |
|---|---|---|---|---|
| before | 2:20-26 | inline | `# noqa` | `other = missing_b` |
| after | 2:20-26 | inline | `# noqa` | `other = missing_b` |

### Warning identities and visibility

The identities below are review-only, not original automated matcher identities. V = visible; S = suppressed; ranges are 1-based with exclusive end columns.

| Identity / source role | Warning and source slice | Before range | After range | A / B / C / D | Judgment |
|---|---|---|---|---|---|
| `review:F821@$.body[0].value.values[0].value`; load Name | F821: `missing_a`; Undefined name `missing_a` | 1:11-1:20 | 1:11-1:20 | V / V / V / V | visible in both |
| `review:F821@$.body[1].value`; load Name | F821: `missing_b`; Undefined name `missing_b` | 2:9-2:18 | 2:9-2:18 | S / V / S / V | suppressed in both |

### Evidence-based judgment and human review

Original and formatted source are byte-identical. Full underlying and visible warnings reproduce; corresponding occurrences cannot move in an identical snapshot. F821 `missing_a` is visible in both; F821 `missing_b` is suppressed in both. All four saved outputs replay exactly after ignoring only temporary filenames. Neutralizing directive comments makes ordinary lint reproduce the underlying warnings in both snapshots. Proposed resolution: Preserved; no corresponding warning changes its visible/suppressed state.

Human interpretation: Independent human adjudication is pending; this is an AI-assisted proposal.

Saved replays and comment-neutralized sources: `reports/ambiguous-audit/exports/fstring_boundary--blanket_last/black/rechecks`. All four replay stdout/stderr and command records are saved there; both neutralized ordinary-lint passes reproduce their respective underlying outputs.

### All four original raw Ruff diagnostic outputs

Privacy-derived JSON is preserved below with execution filenames anonymized and fix metadata retained. Empty arrays are actual empty outputs. Each stdout file also has a `.command.json`, `.stderr.txt` and `.diagnostics.json` sibling in both the original and export directories.

<details>
<summary>A_original_visible</summary>

Original: [A_original_visible.stdout.txt](../../datasets/results/phase3/trials/fstring_boundary--blanket_last/black/A_original_visible.stdout.txt). Export: [A_original_visible.stdout.txt](exports/fstring_boundary--blanket_last/black/A_original_visible.stdout.txt). Replay: [A_original_visible.stdout.txt](exports/fstring_boundary--blanket_last/black/rechecks/A_original_visible.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 20,
      "row": 1
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-g427ohei\\study_input.py",
    "fix": null,
    "location": {
      "column": 11,
      "row": 1
    },
    "message": "Undefined name `missing_a`",
    "noqa_row": 1,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  }
]
```

</details>

<details>
<summary>B_original_underlying</summary>

Original: [B_original_underlying.stdout.txt](../../datasets/results/phase3/trials/fstring_boundary--blanket_last/black/B_original_underlying.stdout.txt). Export: [B_original_underlying.stdout.txt](exports/fstring_boundary--blanket_last/black/B_original_underlying.stdout.txt). Replay: [B_original_underlying.stdout.txt](exports/fstring_boundary--blanket_last/black/rechecks/B_original_underlying.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 20,
      "row": 1
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-te1f26ym\\study_input.py",
    "fix": null,
    "location": {
      "column": 11,
      "row": 1
    },
    "message": "Undefined name `missing_a`",
    "noqa_row": 1,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  },
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 18,
      "row": 2
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-te1f26ym\\study_input.py",
    "fix": null,
    "location": {
      "column": 9,
      "row": 2
    },
    "message": "Undefined name `missing_b`",
    "noqa_row": 2,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  }
]
```

</details>

<details>
<summary>C_formatted_visible</summary>

Original: [C_formatted_visible.stdout.txt](../../datasets/results/phase3/trials/fstring_boundary--blanket_last/black/C_formatted_visible.stdout.txt). Export: [C_formatted_visible.stdout.txt](exports/fstring_boundary--blanket_last/black/C_formatted_visible.stdout.txt). Replay: [C_formatted_visible.stdout.txt](exports/fstring_boundary--blanket_last/black/rechecks/C_formatted_visible.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 20,
      "row": 1
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-0tpxyj8v\\study_input.py",
    "fix": null,
    "location": {
      "column": 11,
      "row": 1
    },
    "message": "Undefined name `missing_a`",
    "noqa_row": 1,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  }
]
```

</details>

<details>
<summary>D_formatted_underlying</summary>

Original: [D_formatted_underlying.stdout.txt](../../datasets/results/phase3/trials/fstring_boundary--blanket_last/black/D_formatted_underlying.stdout.txt). Export: [D_formatted_underlying.stdout.txt](exports/fstring_boundary--blanket_last/black/D_formatted_underlying.stdout.txt). Replay: [D_formatted_underlying.stdout.txt](exports/fstring_boundary--blanket_last/black/rechecks/D_formatted_underlying.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 20,
      "row": 1
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-3549q8b3\\study_input.py",
    "fix": null,
    "location": {
      "column": 11,
      "row": 1
    },
    "message": "Undefined name `missing_a`",
    "noqa_row": 1,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  },
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 18,
      "row": 2
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-3549q8b3\\study_input.py",
    "fix": null,
    "location": {
      "column": 9,
      "row": 2
    },
    "message": "Undefined name `missing_b`",
    "noqa_row": 2,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  }
]
```

</details>

<a id="comparison-20"></a>

## 20. fstring_boundary--blanket_last / ruff

**Original label:** Ambiguous. **Proposed review resolution:** Preserved.

Original evidence directory: `datasets/results/phase3/trials/fstring_boundary--blanket_last/ruff`

Review export directory: `reports/ambiguous-audit/exports/fstring_boundary--blanket_last/ruff`

### Sources and exact evidence paths

Original source: [before.py](../../datasets/results/phase3/trials/fstring_boundary--blanket_last/ruff/before.py); byte-identical export: [before.py](exports/fstring_boundary--blanket_last/ruff/before.py). SHA-256: `40f62d6dc6ef7aa89a355e7fc8a5ee70537e764f131f22cb6d03e1681e243e28`.

```python
text = f"{missing_a}"
other = missing_b  # noqa
```

Formatted source: [after.py](../../datasets/results/phase3/trials/fstring_boundary--blanket_last/ruff/after.py); byte-identical export: [after.py](exports/fstring_boundary--blanket_last/ruff/after.py). SHA-256: `40f62d6dc6ef7aa89a355e7fc8a5ee70537e764f131f22cb6d03e1681e243e28`.

```python
text = f"{missing_a}"
other = missing_b  # noqa
```

Original decision: [result.json](../../datasets/results/phase3/trials/fstring_boundary--blanket_last/ruff/result.json); failure details: [matching.json](../../datasets/results/phase3/trials/fstring_boundary--blanket_last/ruff/matching.json); formatter invocation: [formatter.command.json](../../datasets/results/phase3/trials/fstring_boundary--blanket_last/ruff/formatter.command.json). Full byte-identical copies are in the export directory.

### Why the matcher abstained

Exact recorded error: `Diagnostic or construct does not align with complete code tokens`.

F821 points to `missing_a` inside a formatted-value expression. Python 3.11 tokenize emits the whole f-string as a STRING token, so the embedded identifier span is not a complete token span under the primary matcher. This is a tokenization/coverage boundary, not evidence of a changed suppression.

### Noqa placement

| Snapshot | Position (1-based) | Kind | Exact comment | Preceding code on line |
|---|---|---|---|---|
| before | 2:20-26 | inline | `# noqa` | `other = missing_b` |
| after | 2:20-26 | inline | `# noqa` | `other = missing_b` |

### Warning identities and visibility

The identities below are review-only, not original automated matcher identities. V = visible; S = suppressed; ranges are 1-based with exclusive end columns.

| Identity / source role | Warning and source slice | Before range | After range | A / B / C / D | Judgment |
|---|---|---|---|---|---|
| `review:F821@$.body[0].value.values[0].value`; load Name | F821: `missing_a`; Undefined name `missing_a` | 1:11-1:20 | 1:11-1:20 | V / V / V / V | visible in both |
| `review:F821@$.body[1].value`; load Name | F821: `missing_b`; Undefined name `missing_b` | 2:9-2:18 | 2:9-2:18 | S / V / S / V | suppressed in both |

### Evidence-based judgment and human review

Original and formatted source are byte-identical. Full underlying and visible warnings reproduce; corresponding occurrences cannot move in an identical snapshot. F821 `missing_a` is visible in both; F821 `missing_b` is suppressed in both. All four saved outputs replay exactly after ignoring only temporary filenames. Neutralizing directive comments makes ordinary lint reproduce the underlying warnings in both snapshots. Proposed resolution: Preserved; no corresponding warning changes its visible/suppressed state.

Human interpretation: Independent human adjudication is pending; this is an AI-assisted proposal.

Saved replays and comment-neutralized sources: `reports/ambiguous-audit/exports/fstring_boundary--blanket_last/ruff/rechecks`. All four replay stdout/stderr and command records are saved there; both neutralized ordinary-lint passes reproduce their respective underlying outputs.

### All four original raw Ruff diagnostic outputs

Privacy-derived JSON is preserved below with execution filenames anonymized and fix metadata retained. Empty arrays are actual empty outputs. Each stdout file also has a `.command.json`, `.stderr.txt` and `.diagnostics.json` sibling in both the original and export directories.

<details>
<summary>A_original_visible</summary>

Original: [A_original_visible.stdout.txt](../../datasets/results/phase3/trials/fstring_boundary--blanket_last/ruff/A_original_visible.stdout.txt). Export: [A_original_visible.stdout.txt](exports/fstring_boundary--blanket_last/ruff/A_original_visible.stdout.txt). Replay: [A_original_visible.stdout.txt](exports/fstring_boundary--blanket_last/ruff/rechecks/A_original_visible.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 20,
      "row": 1
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-ew0mrntc\\study_input.py",
    "fix": null,
    "location": {
      "column": 11,
      "row": 1
    },
    "message": "Undefined name `missing_a`",
    "noqa_row": 1,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  }
]
```

</details>

<details>
<summary>B_original_underlying</summary>

Original: [B_original_underlying.stdout.txt](../../datasets/results/phase3/trials/fstring_boundary--blanket_last/ruff/B_original_underlying.stdout.txt). Export: [B_original_underlying.stdout.txt](exports/fstring_boundary--blanket_last/ruff/B_original_underlying.stdout.txt). Replay: [B_original_underlying.stdout.txt](exports/fstring_boundary--blanket_last/ruff/rechecks/B_original_underlying.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 20,
      "row": 1
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-cxaxz8b5\\study_input.py",
    "fix": null,
    "location": {
      "column": 11,
      "row": 1
    },
    "message": "Undefined name `missing_a`",
    "noqa_row": 1,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  },
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 18,
      "row": 2
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-cxaxz8b5\\study_input.py",
    "fix": null,
    "location": {
      "column": 9,
      "row": 2
    },
    "message": "Undefined name `missing_b`",
    "noqa_row": 2,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  }
]
```

</details>

<details>
<summary>C_formatted_visible</summary>

Original: [C_formatted_visible.stdout.txt](../../datasets/results/phase3/trials/fstring_boundary--blanket_last/ruff/C_formatted_visible.stdout.txt). Export: [C_formatted_visible.stdout.txt](exports/fstring_boundary--blanket_last/ruff/C_formatted_visible.stdout.txt). Replay: [C_formatted_visible.stdout.txt](exports/fstring_boundary--blanket_last/ruff/rechecks/C_formatted_visible.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 20,
      "row": 1
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-dqk6j_eq\\study_input.py",
    "fix": null,
    "location": {
      "column": 11,
      "row": 1
    },
    "message": "Undefined name `missing_a`",
    "noqa_row": 1,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  }
]
```

</details>

<details>
<summary>D_formatted_underlying</summary>

Original: [D_formatted_underlying.stdout.txt](../../datasets/results/phase3/trials/fstring_boundary--blanket_last/ruff/D_formatted_underlying.stdout.txt). Export: [D_formatted_underlying.stdout.txt](exports/fstring_boundary--blanket_last/ruff/D_formatted_underlying.stdout.txt). Replay: [D_formatted_underlying.stdout.txt](exports/fstring_boundary--blanket_last/ruff/rechecks/D_formatted_underlying.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 20,
      "row": 1
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-uuecetod\\study_input.py",
    "fix": null,
    "location": {
      "column": 11,
      "row": 1
    },
    "message": "Undefined name `missing_a`",
    "noqa_row": 1,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  },
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 18,
      "row": 2
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-uuecetod\\study_input.py",
    "fix": null,
    "location": {
      "column": 9,
      "row": 2
    },
    "message": "Undefined name `missing_b`",
    "noqa_row": 2,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  }
]
```

</details>

<a id="comparison-21"></a>

## 21. fstring_boundary--file_specific / black

**Original label:** Ambiguous. **Proposed review resolution:** Preserved.

Original evidence directory: `datasets/results/phase3/trials/fstring_boundary--file_specific/black`

Review export directory: `reports/ambiguous-audit/exports/fstring_boundary--file_specific/black`

### Sources and exact evidence paths

Original source: [before.py](../../datasets/results/phase3/trials/fstring_boundary--file_specific/black/before.py); byte-identical export: [before.py](exports/fstring_boundary--file_specific/black/before.py). SHA-256: `7b27472572d8fa6fb4e34fc46b2c944bf41e840537b5de87810fad6d1a155dab`.

```python
# ruff: noqa: F821
text = f"{missing_a}"
other = missing_b
```

Formatted source: [after.py](../../datasets/results/phase3/trials/fstring_boundary--file_specific/black/after.py); byte-identical export: [after.py](exports/fstring_boundary--file_specific/black/after.py). SHA-256: `7b27472572d8fa6fb4e34fc46b2c944bf41e840537b5de87810fad6d1a155dab`.

```python
# ruff: noqa: F821
text = f"{missing_a}"
other = missing_b
```

Original decision: [result.json](../../datasets/results/phase3/trials/fstring_boundary--file_specific/black/result.json); failure details: [matching.json](../../datasets/results/phase3/trials/fstring_boundary--file_specific/black/matching.json); formatter invocation: [formatter.command.json](../../datasets/results/phase3/trials/fstring_boundary--file_specific/black/formatter.command.json). Full byte-identical copies are in the export directory.

### Why the matcher abstained

Exact recorded error: `Diagnostic or construct does not align with complete code tokens`.

F821 points to `missing_a` inside a formatted-value expression. Python 3.11 tokenize emits the whole f-string as a STRING token, so the embedded identifier span is not a complete token span under the primary matcher. This is a tokenization/coverage boundary, not evidence of a changed suppression.

### Noqa placement

| Snapshot | Position (1-based) | Kind | Exact comment | Preceding code on line |
|---|---|---|---|---|
| before | 1:1-19 | file directive | `# ruff: noqa: F821` | `` |
| after | 1:1-19 | file directive | `# ruff: noqa: F821` | `` |

### Warning identities and visibility

The identities below are review-only, not original automated matcher identities. V = visible; S = suppressed; ranges are 1-based with exclusive end columns.

| Identity / source role | Warning and source slice | Before range | After range | A / B / C / D | Judgment |
|---|---|---|---|---|---|
| `review:F821@$.body[0].value.values[0].value`; load Name | F821: `missing_a`; Undefined name `missing_a` | 2:11-2:20 | 2:11-2:20 | S / V / S / V | suppressed in both |
| `review:F821@$.body[1].value`; load Name | F821: `missing_b`; Undefined name `missing_b` | 3:9-3:18 | 3:9-3:18 | S / V / S / V | suppressed in both |

### Evidence-based judgment and human review

Original and formatted source are byte-identical. Full underlying and visible warnings reproduce; corresponding occurrences cannot move in an identical snapshot. F821 `missing_a` is suppressed in both; F821 `missing_b` is suppressed in both. All four saved outputs replay exactly after ignoring only temporary filenames. Neutralizing directive comments makes ordinary lint reproduce the underlying warnings in both snapshots. Proposed resolution: Preserved; no corresponding warning changes its visible/suppressed state.

Human interpretation: Independent human adjudication is pending; this is an AI-assisted proposal.

Saved replays and comment-neutralized sources: `reports/ambiguous-audit/exports/fstring_boundary--file_specific/black/rechecks`. All four replay stdout/stderr and command records are saved there; both neutralized ordinary-lint passes reproduce their respective underlying outputs.

### All four original raw Ruff diagnostic outputs

Privacy-derived JSON is preserved below with execution filenames anonymized and fix metadata retained. Empty arrays are actual empty outputs. Each stdout file also has a `.command.json`, `.stderr.txt` and `.diagnostics.json` sibling in both the original and export directories.

<details>
<summary>A_original_visible</summary>

Original: [A_original_visible.stdout.txt](../../datasets/results/phase3/trials/fstring_boundary--file_specific/black/A_original_visible.stdout.txt). Export: [A_original_visible.stdout.txt](exports/fstring_boundary--file_specific/black/A_original_visible.stdout.txt). Replay: [A_original_visible.stdout.txt](exports/fstring_boundary--file_specific/black/rechecks/A_original_visible.stdout.txt).

```json
[]
```

</details>

<details>
<summary>B_original_underlying</summary>

Original: [B_original_underlying.stdout.txt](../../datasets/results/phase3/trials/fstring_boundary--file_specific/black/B_original_underlying.stdout.txt). Export: [B_original_underlying.stdout.txt](exports/fstring_boundary--file_specific/black/B_original_underlying.stdout.txt). Replay: [B_original_underlying.stdout.txt](exports/fstring_boundary--file_specific/black/rechecks/B_original_underlying.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 20,
      "row": 2
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-y8asn0_l\\study_input.py",
    "fix": null,
    "location": {
      "column": 11,
      "row": 2
    },
    "message": "Undefined name `missing_a`",
    "noqa_row": 2,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  },
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 18,
      "row": 3
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-y8asn0_l\\study_input.py",
    "fix": null,
    "location": {
      "column": 9,
      "row": 3
    },
    "message": "Undefined name `missing_b`",
    "noqa_row": 3,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  }
]
```

</details>

<details>
<summary>C_formatted_visible</summary>

Original: [C_formatted_visible.stdout.txt](../../datasets/results/phase3/trials/fstring_boundary--file_specific/black/C_formatted_visible.stdout.txt). Export: [C_formatted_visible.stdout.txt](exports/fstring_boundary--file_specific/black/C_formatted_visible.stdout.txt). Replay: [C_formatted_visible.stdout.txt](exports/fstring_boundary--file_specific/black/rechecks/C_formatted_visible.stdout.txt).

```json
[]
```

</details>

<details>
<summary>D_formatted_underlying</summary>

Original: [D_formatted_underlying.stdout.txt](../../datasets/results/phase3/trials/fstring_boundary--file_specific/black/D_formatted_underlying.stdout.txt). Export: [D_formatted_underlying.stdout.txt](exports/fstring_boundary--file_specific/black/D_formatted_underlying.stdout.txt). Replay: [D_formatted_underlying.stdout.txt](exports/fstring_boundary--file_specific/black/rechecks/D_formatted_underlying.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 20,
      "row": 2
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-yp_p4yv1\\study_input.py",
    "fix": null,
    "location": {
      "column": 11,
      "row": 2
    },
    "message": "Undefined name `missing_a`",
    "noqa_row": 2,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  },
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 18,
      "row": 3
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-yp_p4yv1\\study_input.py",
    "fix": null,
    "location": {
      "column": 9,
      "row": 3
    },
    "message": "Undefined name `missing_b`",
    "noqa_row": 3,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  }
]
```

</details>

<a id="comparison-22"></a>

## 22. fstring_boundary--file_specific / ruff

**Original label:** Ambiguous. **Proposed review resolution:** Preserved.

Original evidence directory: `datasets/results/phase3/trials/fstring_boundary--file_specific/ruff`

Review export directory: `reports/ambiguous-audit/exports/fstring_boundary--file_specific/ruff`

### Sources and exact evidence paths

Original source: [before.py](../../datasets/results/phase3/trials/fstring_boundary--file_specific/ruff/before.py); byte-identical export: [before.py](exports/fstring_boundary--file_specific/ruff/before.py). SHA-256: `7b27472572d8fa6fb4e34fc46b2c944bf41e840537b5de87810fad6d1a155dab`.

```python
# ruff: noqa: F821
text = f"{missing_a}"
other = missing_b
```

Formatted source: [after.py](../../datasets/results/phase3/trials/fstring_boundary--file_specific/ruff/after.py); byte-identical export: [after.py](exports/fstring_boundary--file_specific/ruff/after.py). SHA-256: `7b27472572d8fa6fb4e34fc46b2c944bf41e840537b5de87810fad6d1a155dab`.

```python
# ruff: noqa: F821
text = f"{missing_a}"
other = missing_b
```

Original decision: [result.json](../../datasets/results/phase3/trials/fstring_boundary--file_specific/ruff/result.json); failure details: [matching.json](../../datasets/results/phase3/trials/fstring_boundary--file_specific/ruff/matching.json); formatter invocation: [formatter.command.json](../../datasets/results/phase3/trials/fstring_boundary--file_specific/ruff/formatter.command.json). Full byte-identical copies are in the export directory.

### Why the matcher abstained

Exact recorded error: `Diagnostic or construct does not align with complete code tokens`.

F821 points to `missing_a` inside a formatted-value expression. Python 3.11 tokenize emits the whole f-string as a STRING token, so the embedded identifier span is not a complete token span under the primary matcher. This is a tokenization/coverage boundary, not evidence of a changed suppression.

### Noqa placement

| Snapshot | Position (1-based) | Kind | Exact comment | Preceding code on line |
|---|---|---|---|---|
| before | 1:1-19 | file directive | `# ruff: noqa: F821` | `` |
| after | 1:1-19 | file directive | `# ruff: noqa: F821` | `` |

### Warning identities and visibility

The identities below are review-only, not original automated matcher identities. V = visible; S = suppressed; ranges are 1-based with exclusive end columns.

| Identity / source role | Warning and source slice | Before range | After range | A / B / C / D | Judgment |
|---|---|---|---|---|---|
| `review:F821@$.body[0].value.values[0].value`; load Name | F821: `missing_a`; Undefined name `missing_a` | 2:11-2:20 | 2:11-2:20 | S / V / S / V | suppressed in both |
| `review:F821@$.body[1].value`; load Name | F821: `missing_b`; Undefined name `missing_b` | 3:9-3:18 | 3:9-3:18 | S / V / S / V | suppressed in both |

### Evidence-based judgment and human review

Original and formatted source are byte-identical. Full underlying and visible warnings reproduce; corresponding occurrences cannot move in an identical snapshot. F821 `missing_a` is suppressed in both; F821 `missing_b` is suppressed in both. All four saved outputs replay exactly after ignoring only temporary filenames. Neutralizing directive comments makes ordinary lint reproduce the underlying warnings in both snapshots. Proposed resolution: Preserved; no corresponding warning changes its visible/suppressed state.

Human interpretation: Independent human adjudication is pending; this is an AI-assisted proposal.

Saved replays and comment-neutralized sources: `reports/ambiguous-audit/exports/fstring_boundary--file_specific/ruff/rechecks`. All four replay stdout/stderr and command records are saved there; both neutralized ordinary-lint passes reproduce their respective underlying outputs.

### All four original raw Ruff diagnostic outputs

Privacy-derived JSON is preserved below with execution filenames anonymized and fix metadata retained. Empty arrays are actual empty outputs. Each stdout file also has a `.command.json`, `.stderr.txt` and `.diagnostics.json` sibling in both the original and export directories.

<details>
<summary>A_original_visible</summary>

Original: [A_original_visible.stdout.txt](../../datasets/results/phase3/trials/fstring_boundary--file_specific/ruff/A_original_visible.stdout.txt). Export: [A_original_visible.stdout.txt](exports/fstring_boundary--file_specific/ruff/A_original_visible.stdout.txt). Replay: [A_original_visible.stdout.txt](exports/fstring_boundary--file_specific/ruff/rechecks/A_original_visible.stdout.txt).

```json
[]
```

</details>

<details>
<summary>B_original_underlying</summary>

Original: [B_original_underlying.stdout.txt](../../datasets/results/phase3/trials/fstring_boundary--file_specific/ruff/B_original_underlying.stdout.txt). Export: [B_original_underlying.stdout.txt](exports/fstring_boundary--file_specific/ruff/B_original_underlying.stdout.txt). Replay: [B_original_underlying.stdout.txt](exports/fstring_boundary--file_specific/ruff/rechecks/B_original_underlying.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 20,
      "row": 2
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-7_z56fds\\study_input.py",
    "fix": null,
    "location": {
      "column": 11,
      "row": 2
    },
    "message": "Undefined name `missing_a`",
    "noqa_row": 2,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  },
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 18,
      "row": 3
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-7_z56fds\\study_input.py",
    "fix": null,
    "location": {
      "column": 9,
      "row": 3
    },
    "message": "Undefined name `missing_b`",
    "noqa_row": 3,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  }
]
```

</details>

<details>
<summary>C_formatted_visible</summary>

Original: [C_formatted_visible.stdout.txt](../../datasets/results/phase3/trials/fstring_boundary--file_specific/ruff/C_formatted_visible.stdout.txt). Export: [C_formatted_visible.stdout.txt](exports/fstring_boundary--file_specific/ruff/C_formatted_visible.stdout.txt). Replay: [C_formatted_visible.stdout.txt](exports/fstring_boundary--file_specific/ruff/rechecks/C_formatted_visible.stdout.txt).

```json
[]
```

</details>

<details>
<summary>D_formatted_underlying</summary>

Original: [D_formatted_underlying.stdout.txt](../../datasets/results/phase3/trials/fstring_boundary--file_specific/ruff/D_formatted_underlying.stdout.txt). Export: [D_formatted_underlying.stdout.txt](exports/fstring_boundary--file_specific/ruff/D_formatted_underlying.stdout.txt). Replay: [D_formatted_underlying.stdout.txt](exports/fstring_boundary--file_specific/ruff/rechecks/D_formatted_underlying.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 20,
      "row": 2
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-_kvjoqyl\\study_input.py",
    "fix": null,
    "location": {
      "column": 11,
      "row": 2
    },
    "message": "Undefined name `missing_a`",
    "noqa_row": 2,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  },
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 18,
      "row": 3
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-_kvjoqyl\\study_input.py",
    "fix": null,
    "location": {
      "column": 9,
      "row": 3
    },
    "message": "Undefined name `missing_b`",
    "noqa_row": 3,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  }
]
```

</details>

<a id="comparison-23"></a>

## 23. fstring_boundary--multicode_first / black

**Original label:** Ambiguous. **Proposed review resolution:** Preserved.

Original evidence directory: `datasets/results/phase3/trials/fstring_boundary--multicode_first/black`

Review export directory: `reports/ambiguous-audit/exports/fstring_boundary--multicode_first/black`

### Sources and exact evidence paths

Original source: [before.py](../../datasets/results/phase3/trials/fstring_boundary--multicode_first/black/before.py); byte-identical export: [before.py](exports/fstring_boundary--multicode_first/black/before.py). SHA-256: `2f1e27c8f3b4afcd465ac331ec08dc05e506d278b476fe35e111de424b4c10a8`.

```python
text = f"{missing_a}"  # noqa: F401, F821, F841
other = missing_b
```

Formatted source: [after.py](../../datasets/results/phase3/trials/fstring_boundary--multicode_first/black/after.py); byte-identical export: [after.py](exports/fstring_boundary--multicode_first/black/after.py). SHA-256: `2f1e27c8f3b4afcd465ac331ec08dc05e506d278b476fe35e111de424b4c10a8`.

```python
text = f"{missing_a}"  # noqa: F401, F821, F841
other = missing_b
```

Original decision: [result.json](../../datasets/results/phase3/trials/fstring_boundary--multicode_first/black/result.json); failure details: [matching.json](../../datasets/results/phase3/trials/fstring_boundary--multicode_first/black/matching.json); formatter invocation: [formatter.command.json](../../datasets/results/phase3/trials/fstring_boundary--multicode_first/black/formatter.command.json). Full byte-identical copies are in the export directory.

### Why the matcher abstained

Exact recorded error: `Diagnostic or construct does not align with complete code tokens`.

F821 points to `missing_a` inside a formatted-value expression. Python 3.11 tokenize emits the whole f-string as a STRING token, so the embedded identifier span is not a complete token span under the primary matcher. This is a tokenization/coverage boundary, not evidence of a changed suppression.

### Noqa placement

| Snapshot | Position (1-based) | Kind | Exact comment | Preceding code on line |
|---|---|---|---|---|
| before | 1:24-48 | inline | `# noqa: F401, F821, F841` | `text = f"{missing_a}"` |
| after | 1:24-48 | inline | `# noqa: F401, F821, F841` | `text = f"{missing_a}"` |

### Warning identities and visibility

The identities below are review-only, not original automated matcher identities. V = visible; S = suppressed; ranges are 1-based with exclusive end columns.

| Identity / source role | Warning and source slice | Before range | After range | A / B / C / D | Judgment |
|---|---|---|---|---|---|
| `review:F821@$.body[0].value.values[0].value`; load Name | F821: `missing_a`; Undefined name `missing_a` | 1:11-1:20 | 1:11-1:20 | S / V / S / V | suppressed in both |
| `review:F821@$.body[1].value`; load Name | F821: `missing_b`; Undefined name `missing_b` | 2:9-2:18 | 2:9-2:18 | V / V / V / V | visible in both |

### Evidence-based judgment and human review

Original and formatted source are byte-identical. Full underlying and visible warnings reproduce; corresponding occurrences cannot move in an identical snapshot. F821 `missing_a` is suppressed in both; F821 `missing_b` is visible in both. All four saved outputs replay exactly after ignoring only temporary filenames. Neutralizing directive comments makes ordinary lint reproduce the underlying warnings in both snapshots. Proposed resolution: Preserved; no corresponding warning changes its visible/suppressed state.

Human interpretation: Independent human adjudication is pending; this is an AI-assisted proposal.

Saved replays and comment-neutralized sources: `reports/ambiguous-audit/exports/fstring_boundary--multicode_first/black/rechecks`. All four replay stdout/stderr and command records are saved there; both neutralized ordinary-lint passes reproduce their respective underlying outputs.

### All four original raw Ruff diagnostic outputs

Privacy-derived JSON is preserved below with execution filenames anonymized and fix metadata retained. Empty arrays are actual empty outputs. Each stdout file also has a `.command.json`, `.stderr.txt` and `.diagnostics.json` sibling in both the original and export directories.

<details>
<summary>A_original_visible</summary>

Original: [A_original_visible.stdout.txt](../../datasets/results/phase3/trials/fstring_boundary--multicode_first/black/A_original_visible.stdout.txt). Export: [A_original_visible.stdout.txt](exports/fstring_boundary--multicode_first/black/A_original_visible.stdout.txt). Replay: [A_original_visible.stdout.txt](exports/fstring_boundary--multicode_first/black/rechecks/A_original_visible.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 18,
      "row": 2
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-ju_l2n6t\\study_input.py",
    "fix": null,
    "location": {
      "column": 9,
      "row": 2
    },
    "message": "Undefined name `missing_b`",
    "noqa_row": 2,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  }
]
```

</details>

<details>
<summary>B_original_underlying</summary>

Original: [B_original_underlying.stdout.txt](../../datasets/results/phase3/trials/fstring_boundary--multicode_first/black/B_original_underlying.stdout.txt). Export: [B_original_underlying.stdout.txt](exports/fstring_boundary--multicode_first/black/B_original_underlying.stdout.txt). Replay: [B_original_underlying.stdout.txt](exports/fstring_boundary--multicode_first/black/rechecks/B_original_underlying.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 20,
      "row": 1
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-w510rnyf\\study_input.py",
    "fix": null,
    "location": {
      "column": 11,
      "row": 1
    },
    "message": "Undefined name `missing_a`",
    "noqa_row": 1,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  },
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 18,
      "row": 2
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-w510rnyf\\study_input.py",
    "fix": null,
    "location": {
      "column": 9,
      "row": 2
    },
    "message": "Undefined name `missing_b`",
    "noqa_row": 2,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  }
]
```

</details>

<details>
<summary>C_formatted_visible</summary>

Original: [C_formatted_visible.stdout.txt](../../datasets/results/phase3/trials/fstring_boundary--multicode_first/black/C_formatted_visible.stdout.txt). Export: [C_formatted_visible.stdout.txt](exports/fstring_boundary--multicode_first/black/C_formatted_visible.stdout.txt). Replay: [C_formatted_visible.stdout.txt](exports/fstring_boundary--multicode_first/black/rechecks/C_formatted_visible.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 18,
      "row": 2
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-drnqmjhw\\study_input.py",
    "fix": null,
    "location": {
      "column": 9,
      "row": 2
    },
    "message": "Undefined name `missing_b`",
    "noqa_row": 2,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  }
]
```

</details>

<details>
<summary>D_formatted_underlying</summary>

Original: [D_formatted_underlying.stdout.txt](../../datasets/results/phase3/trials/fstring_boundary--multicode_first/black/D_formatted_underlying.stdout.txt). Export: [D_formatted_underlying.stdout.txt](exports/fstring_boundary--multicode_first/black/D_formatted_underlying.stdout.txt). Replay: [D_formatted_underlying.stdout.txt](exports/fstring_boundary--multicode_first/black/rechecks/D_formatted_underlying.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 20,
      "row": 1
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-jm7ael_h\\study_input.py",
    "fix": null,
    "location": {
      "column": 11,
      "row": 1
    },
    "message": "Undefined name `missing_a`",
    "noqa_row": 1,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  },
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 18,
      "row": 2
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-jm7ael_h\\study_input.py",
    "fix": null,
    "location": {
      "column": 9,
      "row": 2
    },
    "message": "Undefined name `missing_b`",
    "noqa_row": 2,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  }
]
```

</details>

<a id="comparison-24"></a>

## 24. fstring_boundary--multicode_first / ruff

**Original label:** Ambiguous. **Proposed review resolution:** Preserved.

Original evidence directory: `datasets/results/phase3/trials/fstring_boundary--multicode_first/ruff`

Review export directory: `reports/ambiguous-audit/exports/fstring_boundary--multicode_first/ruff`

### Sources and exact evidence paths

Original source: [before.py](../../datasets/results/phase3/trials/fstring_boundary--multicode_first/ruff/before.py); byte-identical export: [before.py](exports/fstring_boundary--multicode_first/ruff/before.py). SHA-256: `2f1e27c8f3b4afcd465ac331ec08dc05e506d278b476fe35e111de424b4c10a8`.

```python
text = f"{missing_a}"  # noqa: F401, F821, F841
other = missing_b
```

Formatted source: [after.py](../../datasets/results/phase3/trials/fstring_boundary--multicode_first/ruff/after.py); byte-identical export: [after.py](exports/fstring_boundary--multicode_first/ruff/after.py). SHA-256: `2f1e27c8f3b4afcd465ac331ec08dc05e506d278b476fe35e111de424b4c10a8`.

```python
text = f"{missing_a}"  # noqa: F401, F821, F841
other = missing_b
```

Original decision: [result.json](../../datasets/results/phase3/trials/fstring_boundary--multicode_first/ruff/result.json); failure details: [matching.json](../../datasets/results/phase3/trials/fstring_boundary--multicode_first/ruff/matching.json); formatter invocation: [formatter.command.json](../../datasets/results/phase3/trials/fstring_boundary--multicode_first/ruff/formatter.command.json). Full byte-identical copies are in the export directory.

### Why the matcher abstained

Exact recorded error: `Diagnostic or construct does not align with complete code tokens`.

F821 points to `missing_a` inside a formatted-value expression. Python 3.11 tokenize emits the whole f-string as a STRING token, so the embedded identifier span is not a complete token span under the primary matcher. This is a tokenization/coverage boundary, not evidence of a changed suppression.

### Noqa placement

| Snapshot | Position (1-based) | Kind | Exact comment | Preceding code on line |
|---|---|---|---|---|
| before | 1:24-48 | inline | `# noqa: F401, F821, F841` | `text = f"{missing_a}"` |
| after | 1:24-48 | inline | `# noqa: F401, F821, F841` | `text = f"{missing_a}"` |

### Warning identities and visibility

The identities below are review-only, not original automated matcher identities. V = visible; S = suppressed; ranges are 1-based with exclusive end columns.

| Identity / source role | Warning and source slice | Before range | After range | A / B / C / D | Judgment |
|---|---|---|---|---|---|
| `review:F821@$.body[0].value.values[0].value`; load Name | F821: `missing_a`; Undefined name `missing_a` | 1:11-1:20 | 1:11-1:20 | S / V / S / V | suppressed in both |
| `review:F821@$.body[1].value`; load Name | F821: `missing_b`; Undefined name `missing_b` | 2:9-2:18 | 2:9-2:18 | V / V / V / V | visible in both |

### Evidence-based judgment and human review

Original and formatted source are byte-identical. Full underlying and visible warnings reproduce; corresponding occurrences cannot move in an identical snapshot. F821 `missing_a` is suppressed in both; F821 `missing_b` is visible in both. All four saved outputs replay exactly after ignoring only temporary filenames. Neutralizing directive comments makes ordinary lint reproduce the underlying warnings in both snapshots. Proposed resolution: Preserved; no corresponding warning changes its visible/suppressed state.

Human interpretation: Independent human adjudication is pending; this is an AI-assisted proposal.

Saved replays and comment-neutralized sources: `reports/ambiguous-audit/exports/fstring_boundary--multicode_first/ruff/rechecks`. All four replay stdout/stderr and command records are saved there; both neutralized ordinary-lint passes reproduce their respective underlying outputs.

### All four original raw Ruff diagnostic outputs

Privacy-derived JSON is preserved below with execution filenames anonymized and fix metadata retained. Empty arrays are actual empty outputs. Each stdout file also has a `.command.json`, `.stderr.txt` and `.diagnostics.json` sibling in both the original and export directories.

<details>
<summary>A_original_visible</summary>

Original: [A_original_visible.stdout.txt](../../datasets/results/phase3/trials/fstring_boundary--multicode_first/ruff/A_original_visible.stdout.txt). Export: [A_original_visible.stdout.txt](exports/fstring_boundary--multicode_first/ruff/A_original_visible.stdout.txt). Replay: [A_original_visible.stdout.txt](exports/fstring_boundary--multicode_first/ruff/rechecks/A_original_visible.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 18,
      "row": 2
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-7yrxmd4a\\study_input.py",
    "fix": null,
    "location": {
      "column": 9,
      "row": 2
    },
    "message": "Undefined name `missing_b`",
    "noqa_row": 2,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  }
]
```

</details>

<details>
<summary>B_original_underlying</summary>

Original: [B_original_underlying.stdout.txt](../../datasets/results/phase3/trials/fstring_boundary--multicode_first/ruff/B_original_underlying.stdout.txt). Export: [B_original_underlying.stdout.txt](exports/fstring_boundary--multicode_first/ruff/B_original_underlying.stdout.txt). Replay: [B_original_underlying.stdout.txt](exports/fstring_boundary--multicode_first/ruff/rechecks/B_original_underlying.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 20,
      "row": 1
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-pks5fm6b\\study_input.py",
    "fix": null,
    "location": {
      "column": 11,
      "row": 1
    },
    "message": "Undefined name `missing_a`",
    "noqa_row": 1,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  },
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 18,
      "row": 2
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-pks5fm6b\\study_input.py",
    "fix": null,
    "location": {
      "column": 9,
      "row": 2
    },
    "message": "Undefined name `missing_b`",
    "noqa_row": 2,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  }
]
```

</details>

<details>
<summary>C_formatted_visible</summary>

Original: [C_formatted_visible.stdout.txt](../../datasets/results/phase3/trials/fstring_boundary--multicode_first/ruff/C_formatted_visible.stdout.txt). Export: [C_formatted_visible.stdout.txt](exports/fstring_boundary--multicode_first/ruff/C_formatted_visible.stdout.txt). Replay: [C_formatted_visible.stdout.txt](exports/fstring_boundary--multicode_first/ruff/rechecks/C_formatted_visible.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 18,
      "row": 2
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-icxdxctg\\study_input.py",
    "fix": null,
    "location": {
      "column": 9,
      "row": 2
    },
    "message": "Undefined name `missing_b`",
    "noqa_row": 2,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  }
]
```

</details>

<details>
<summary>D_formatted_underlying</summary>

Original: [D_formatted_underlying.stdout.txt](../../datasets/results/phase3/trials/fstring_boundary--multicode_first/ruff/D_formatted_underlying.stdout.txt). Export: [D_formatted_underlying.stdout.txt](exports/fstring_boundary--multicode_first/ruff/D_formatted_underlying.stdout.txt). Replay: [D_formatted_underlying.stdout.txt](exports/fstring_boundary--multicode_first/ruff/rechecks/D_formatted_underlying.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 20,
      "row": 1
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-5j7fn5we\\study_input.py",
    "fix": null,
    "location": {
      "column": 11,
      "row": 1
    },
    "message": "Undefined name `missing_a`",
    "noqa_row": 1,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  },
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 18,
      "row": 2
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-5j7fn5we\\study_input.py",
    "fix": null,
    "location": {
      "column": 9,
      "row": 2
    },
    "message": "Undefined name `missing_b`",
    "noqa_row": 2,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  }
]
```

</details>

<a id="comparison-25"></a>

## 25. fstring_boundary--none / black

**Original label:** Ambiguous. **Proposed review resolution:** Preserved.

Original evidence directory: `datasets/results/phase3/trials/fstring_boundary--none/black`

Review export directory: `reports/ambiguous-audit/exports/fstring_boundary--none/black`

### Sources and exact evidence paths

Original source: [before.py](../../datasets/results/phase3/trials/fstring_boundary--none/black/before.py); byte-identical export: [before.py](exports/fstring_boundary--none/black/before.py). SHA-256: `8d5f96f277c7ba8c0c77cb70f1ff650516441943906d8836910ad2f9e90a75f6`.

```python
text = f"{missing_a}"
other = missing_b
```

Formatted source: [after.py](../../datasets/results/phase3/trials/fstring_boundary--none/black/after.py); byte-identical export: [after.py](exports/fstring_boundary--none/black/after.py). SHA-256: `8d5f96f277c7ba8c0c77cb70f1ff650516441943906d8836910ad2f9e90a75f6`.

```python
text = f"{missing_a}"
other = missing_b
```

Original decision: [result.json](../../datasets/results/phase3/trials/fstring_boundary--none/black/result.json); failure details: [matching.json](../../datasets/results/phase3/trials/fstring_boundary--none/black/matching.json); formatter invocation: [formatter.command.json](../../datasets/results/phase3/trials/fstring_boundary--none/black/formatter.command.json). Full byte-identical copies are in the export directory.

### Why the matcher abstained

Exact recorded error: `Diagnostic or construct does not align with complete code tokens`.

F821 points to `missing_a` inside a formatted-value expression. Python 3.11 tokenize emits the whole f-string as a STRING token, so the embedded identifier span is not a complete token span under the primary matcher. This is a tokenization/coverage boundary, not evidence of a changed suppression.

### Noqa placement

| Snapshot | Position (1-based) | Kind | Exact comment | Preceding code on line |
|---|---|---|---|---|
| before | - | no directive | - | - |
| after | - | no directive | - | - |

### Warning identities and visibility

The identities below are review-only, not original automated matcher identities. V = visible; S = suppressed; ranges are 1-based with exclusive end columns.

| Identity / source role | Warning and source slice | Before range | After range | A / B / C / D | Judgment |
|---|---|---|---|---|---|
| `review:F821@$.body[0].value.values[0].value`; load Name | F821: `missing_a`; Undefined name `missing_a` | 1:11-1:20 | 1:11-1:20 | V / V / V / V | visible in both |
| `review:F821@$.body[1].value`; load Name | F821: `missing_b`; Undefined name `missing_b` | 2:9-2:18 | 2:9-2:18 | V / V / V / V | visible in both |

### Evidence-based judgment and human review

Original and formatted source are byte-identical. Full underlying and visible warnings reproduce; corresponding occurrences cannot move in an identical snapshot. F821 `missing_a` is visible in both; F821 `missing_b` is visible in both. All four saved outputs replay exactly after ignoring only temporary filenames. Neutralizing directive comments makes ordinary lint reproduce the underlying warnings in both snapshots. Proposed resolution: Preserved; no corresponding warning changes its visible/suppressed state.

Human interpretation: Independent human adjudication is pending; this is an AI-assisted proposal.

Saved replays and comment-neutralized sources: `reports/ambiguous-audit/exports/fstring_boundary--none/black/rechecks`. All four replay stdout/stderr and command records are saved there; both neutralized ordinary-lint passes reproduce their respective underlying outputs.

### All four original raw Ruff diagnostic outputs

Privacy-derived JSON is preserved below with execution filenames anonymized and fix metadata retained. Empty arrays are actual empty outputs. Each stdout file also has a `.command.json`, `.stderr.txt` and `.diagnostics.json` sibling in both the original and export directories.

<details>
<summary>A_original_visible</summary>

Original: [A_original_visible.stdout.txt](../../datasets/results/phase3/trials/fstring_boundary--none/black/A_original_visible.stdout.txt). Export: [A_original_visible.stdout.txt](exports/fstring_boundary--none/black/A_original_visible.stdout.txt). Replay: [A_original_visible.stdout.txt](exports/fstring_boundary--none/black/rechecks/A_original_visible.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 20,
      "row": 1
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-mz8tjthe\\study_input.py",
    "fix": null,
    "location": {
      "column": 11,
      "row": 1
    },
    "message": "Undefined name `missing_a`",
    "noqa_row": 1,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  },
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 18,
      "row": 2
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-mz8tjthe\\study_input.py",
    "fix": null,
    "location": {
      "column": 9,
      "row": 2
    },
    "message": "Undefined name `missing_b`",
    "noqa_row": 2,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  }
]
```

</details>

<details>
<summary>B_original_underlying</summary>

Original: [B_original_underlying.stdout.txt](../../datasets/results/phase3/trials/fstring_boundary--none/black/B_original_underlying.stdout.txt). Export: [B_original_underlying.stdout.txt](exports/fstring_boundary--none/black/B_original_underlying.stdout.txt). Replay: [B_original_underlying.stdout.txt](exports/fstring_boundary--none/black/rechecks/B_original_underlying.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 20,
      "row": 1
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-_2rk6l_v\\study_input.py",
    "fix": null,
    "location": {
      "column": 11,
      "row": 1
    },
    "message": "Undefined name `missing_a`",
    "noqa_row": 1,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  },
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 18,
      "row": 2
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-_2rk6l_v\\study_input.py",
    "fix": null,
    "location": {
      "column": 9,
      "row": 2
    },
    "message": "Undefined name `missing_b`",
    "noqa_row": 2,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  }
]
```

</details>

<details>
<summary>C_formatted_visible</summary>

Original: [C_formatted_visible.stdout.txt](../../datasets/results/phase3/trials/fstring_boundary--none/black/C_formatted_visible.stdout.txt). Export: [C_formatted_visible.stdout.txt](exports/fstring_boundary--none/black/C_formatted_visible.stdout.txt). Replay: [C_formatted_visible.stdout.txt](exports/fstring_boundary--none/black/rechecks/C_formatted_visible.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 20,
      "row": 1
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-rvu3r4yv\\study_input.py",
    "fix": null,
    "location": {
      "column": 11,
      "row": 1
    },
    "message": "Undefined name `missing_a`",
    "noqa_row": 1,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  },
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 18,
      "row": 2
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-rvu3r4yv\\study_input.py",
    "fix": null,
    "location": {
      "column": 9,
      "row": 2
    },
    "message": "Undefined name `missing_b`",
    "noqa_row": 2,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  }
]
```

</details>

<details>
<summary>D_formatted_underlying</summary>

Original: [D_formatted_underlying.stdout.txt](../../datasets/results/phase3/trials/fstring_boundary--none/black/D_formatted_underlying.stdout.txt). Export: [D_formatted_underlying.stdout.txt](exports/fstring_boundary--none/black/D_formatted_underlying.stdout.txt). Replay: [D_formatted_underlying.stdout.txt](exports/fstring_boundary--none/black/rechecks/D_formatted_underlying.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 20,
      "row": 1
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-p1mb68xt\\study_input.py",
    "fix": null,
    "location": {
      "column": 11,
      "row": 1
    },
    "message": "Undefined name `missing_a`",
    "noqa_row": 1,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  },
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 18,
      "row": 2
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-p1mb68xt\\study_input.py",
    "fix": null,
    "location": {
      "column": 9,
      "row": 2
    },
    "message": "Undefined name `missing_b`",
    "noqa_row": 2,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  }
]
```

</details>

<a id="comparison-26"></a>

## 26. fstring_boundary--none / ruff

**Original label:** Ambiguous. **Proposed review resolution:** Preserved.

Original evidence directory: `datasets/results/phase3/trials/fstring_boundary--none/ruff`

Review export directory: `reports/ambiguous-audit/exports/fstring_boundary--none/ruff`

### Sources and exact evidence paths

Original source: [before.py](../../datasets/results/phase3/trials/fstring_boundary--none/ruff/before.py); byte-identical export: [before.py](exports/fstring_boundary--none/ruff/before.py). SHA-256: `8d5f96f277c7ba8c0c77cb70f1ff650516441943906d8836910ad2f9e90a75f6`.

```python
text = f"{missing_a}"
other = missing_b
```

Formatted source: [after.py](../../datasets/results/phase3/trials/fstring_boundary--none/ruff/after.py); byte-identical export: [after.py](exports/fstring_boundary--none/ruff/after.py). SHA-256: `8d5f96f277c7ba8c0c77cb70f1ff650516441943906d8836910ad2f9e90a75f6`.

```python
text = f"{missing_a}"
other = missing_b
```

Original decision: [result.json](../../datasets/results/phase3/trials/fstring_boundary--none/ruff/result.json); failure details: [matching.json](../../datasets/results/phase3/trials/fstring_boundary--none/ruff/matching.json); formatter invocation: [formatter.command.json](../../datasets/results/phase3/trials/fstring_boundary--none/ruff/formatter.command.json). Full byte-identical copies are in the export directory.

### Why the matcher abstained

Exact recorded error: `Diagnostic or construct does not align with complete code tokens`.

F821 points to `missing_a` inside a formatted-value expression. Python 3.11 tokenize emits the whole f-string as a STRING token, so the embedded identifier span is not a complete token span under the primary matcher. This is a tokenization/coverage boundary, not evidence of a changed suppression.

### Noqa placement

| Snapshot | Position (1-based) | Kind | Exact comment | Preceding code on line |
|---|---|---|---|---|
| before | - | no directive | - | - |
| after | - | no directive | - | - |

### Warning identities and visibility

The identities below are review-only, not original automated matcher identities. V = visible; S = suppressed; ranges are 1-based with exclusive end columns.

| Identity / source role | Warning and source slice | Before range | After range | A / B / C / D | Judgment |
|---|---|---|---|---|---|
| `review:F821@$.body[0].value.values[0].value`; load Name | F821: `missing_a`; Undefined name `missing_a` | 1:11-1:20 | 1:11-1:20 | V / V / V / V | visible in both |
| `review:F821@$.body[1].value`; load Name | F821: `missing_b`; Undefined name `missing_b` | 2:9-2:18 | 2:9-2:18 | V / V / V / V | visible in both |

### Evidence-based judgment and human review

Original and formatted source are byte-identical. Full underlying and visible warnings reproduce; corresponding occurrences cannot move in an identical snapshot. F821 `missing_a` is visible in both; F821 `missing_b` is visible in both. All four saved outputs replay exactly after ignoring only temporary filenames. Neutralizing directive comments makes ordinary lint reproduce the underlying warnings in both snapshots. Proposed resolution: Preserved; no corresponding warning changes its visible/suppressed state.

Human interpretation: Independent human adjudication is pending; this is an AI-assisted proposal.

Saved replays and comment-neutralized sources: `reports/ambiguous-audit/exports/fstring_boundary--none/ruff/rechecks`. All four replay stdout/stderr and command records are saved there; both neutralized ordinary-lint passes reproduce their respective underlying outputs.

### All four original raw Ruff diagnostic outputs

Privacy-derived JSON is preserved below with execution filenames anonymized and fix metadata retained. Empty arrays are actual empty outputs. Each stdout file also has a `.command.json`, `.stderr.txt` and `.diagnostics.json` sibling in both the original and export directories.

<details>
<summary>A_original_visible</summary>

Original: [A_original_visible.stdout.txt](../../datasets/results/phase3/trials/fstring_boundary--none/ruff/A_original_visible.stdout.txt). Export: [A_original_visible.stdout.txt](exports/fstring_boundary--none/ruff/A_original_visible.stdout.txt). Replay: [A_original_visible.stdout.txt](exports/fstring_boundary--none/ruff/rechecks/A_original_visible.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 20,
      "row": 1
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-nq0ln1t_\\study_input.py",
    "fix": null,
    "location": {
      "column": 11,
      "row": 1
    },
    "message": "Undefined name `missing_a`",
    "noqa_row": 1,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  },
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 18,
      "row": 2
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-nq0ln1t_\\study_input.py",
    "fix": null,
    "location": {
      "column": 9,
      "row": 2
    },
    "message": "Undefined name `missing_b`",
    "noqa_row": 2,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  }
]
```

</details>

<details>
<summary>B_original_underlying</summary>

Original: [B_original_underlying.stdout.txt](../../datasets/results/phase3/trials/fstring_boundary--none/ruff/B_original_underlying.stdout.txt). Export: [B_original_underlying.stdout.txt](exports/fstring_boundary--none/ruff/B_original_underlying.stdout.txt). Replay: [B_original_underlying.stdout.txt](exports/fstring_boundary--none/ruff/rechecks/B_original_underlying.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 20,
      "row": 1
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-0822qmed\\study_input.py",
    "fix": null,
    "location": {
      "column": 11,
      "row": 1
    },
    "message": "Undefined name `missing_a`",
    "noqa_row": 1,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  },
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 18,
      "row": 2
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-0822qmed\\study_input.py",
    "fix": null,
    "location": {
      "column": 9,
      "row": 2
    },
    "message": "Undefined name `missing_b`",
    "noqa_row": 2,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  }
]
```

</details>

<details>
<summary>C_formatted_visible</summary>

Original: [C_formatted_visible.stdout.txt](../../datasets/results/phase3/trials/fstring_boundary--none/ruff/C_formatted_visible.stdout.txt). Export: [C_formatted_visible.stdout.txt](exports/fstring_boundary--none/ruff/C_formatted_visible.stdout.txt). Replay: [C_formatted_visible.stdout.txt](exports/fstring_boundary--none/ruff/rechecks/C_formatted_visible.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 20,
      "row": 1
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-w7r7jmg3\\study_input.py",
    "fix": null,
    "location": {
      "column": 11,
      "row": 1
    },
    "message": "Undefined name `missing_a`",
    "noqa_row": 1,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  },
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 18,
      "row": 2
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-w7r7jmg3\\study_input.py",
    "fix": null,
    "location": {
      "column": 9,
      "row": 2
    },
    "message": "Undefined name `missing_b`",
    "noqa_row": 2,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  }
]
```

</details>

<details>
<summary>D_formatted_underlying</summary>

Original: [D_formatted_underlying.stdout.txt](../../datasets/results/phase3/trials/fstring_boundary--none/ruff/D_formatted_underlying.stdout.txt). Export: [D_formatted_underlying.stdout.txt](exports/fstring_boundary--none/ruff/D_formatted_underlying.stdout.txt). Replay: [D_formatted_underlying.stdout.txt](exports/fstring_boundary--none/ruff/rechecks/D_formatted_underlying.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 20,
      "row": 1
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-texoeiut\\study_input.py",
    "fix": null,
    "location": {
      "column": 11,
      "row": 1
    },
    "message": "Undefined name `missing_a`",
    "noqa_row": 1,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  },
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 18,
      "row": 2
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-texoeiut\\study_input.py",
    "fix": null,
    "location": {
      "column": 9,
      "row": 2
    },
    "message": "Undefined name `missing_b`",
    "noqa_row": 2,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  }
]
```

</details>

<a id="comparison-27"></a>

## 27. fstring_boundary--specific_first / black

**Original label:** Ambiguous. **Proposed review resolution:** Preserved.

Original evidence directory: `datasets/results/phase3/trials/fstring_boundary--specific_first/black`

Review export directory: `reports/ambiguous-audit/exports/fstring_boundary--specific_first/black`

### Sources and exact evidence paths

Original source: [before.py](../../datasets/results/phase3/trials/fstring_boundary--specific_first/black/before.py); byte-identical export: [before.py](exports/fstring_boundary--specific_first/black/before.py). SHA-256: `24d8abe2e3ca9e4ff8756f4421b4270b9bcf696639e00803225b1dfedc662bf0`.

```python
text = f"{missing_a}"  # noqa: F821
other = missing_b
```

Formatted source: [after.py](../../datasets/results/phase3/trials/fstring_boundary--specific_first/black/after.py); byte-identical export: [after.py](exports/fstring_boundary--specific_first/black/after.py). SHA-256: `24d8abe2e3ca9e4ff8756f4421b4270b9bcf696639e00803225b1dfedc662bf0`.

```python
text = f"{missing_a}"  # noqa: F821
other = missing_b
```

Original decision: [result.json](../../datasets/results/phase3/trials/fstring_boundary--specific_first/black/result.json); failure details: [matching.json](../../datasets/results/phase3/trials/fstring_boundary--specific_first/black/matching.json); formatter invocation: [formatter.command.json](../../datasets/results/phase3/trials/fstring_boundary--specific_first/black/formatter.command.json). Full byte-identical copies are in the export directory.

### Why the matcher abstained

Exact recorded error: `Diagnostic or construct does not align with complete code tokens`.

F821 points to `missing_a` inside a formatted-value expression. Python 3.11 tokenize emits the whole f-string as a STRING token, so the embedded identifier span is not a complete token span under the primary matcher. This is a tokenization/coverage boundary, not evidence of a changed suppression.

### Noqa placement

| Snapshot | Position (1-based) | Kind | Exact comment | Preceding code on line |
|---|---|---|---|---|
| before | 1:24-36 | inline | `# noqa: F821` | `text = f"{missing_a}"` |
| after | 1:24-36 | inline | `# noqa: F821` | `text = f"{missing_a}"` |

### Warning identities and visibility

The identities below are review-only, not original automated matcher identities. V = visible; S = suppressed; ranges are 1-based with exclusive end columns.

| Identity / source role | Warning and source slice | Before range | After range | A / B / C / D | Judgment |
|---|---|---|---|---|---|
| `review:F821@$.body[0].value.values[0].value`; load Name | F821: `missing_a`; Undefined name `missing_a` | 1:11-1:20 | 1:11-1:20 | S / V / S / V | suppressed in both |
| `review:F821@$.body[1].value`; load Name | F821: `missing_b`; Undefined name `missing_b` | 2:9-2:18 | 2:9-2:18 | V / V / V / V | visible in both |

### Evidence-based judgment and human review

Original and formatted source are byte-identical. Full underlying and visible warnings reproduce; corresponding occurrences cannot move in an identical snapshot. F821 `missing_a` is suppressed in both; F821 `missing_b` is visible in both. All four saved outputs replay exactly after ignoring only temporary filenames. Neutralizing directive comments makes ordinary lint reproduce the underlying warnings in both snapshots. Proposed resolution: Preserved; no corresponding warning changes its visible/suppressed state.

Human interpretation: Independent human adjudication is pending; this is an AI-assisted proposal.

Saved replays and comment-neutralized sources: `reports/ambiguous-audit/exports/fstring_boundary--specific_first/black/rechecks`. All four replay stdout/stderr and command records are saved there; both neutralized ordinary-lint passes reproduce their respective underlying outputs.

### All four original raw Ruff diagnostic outputs

Privacy-derived JSON is preserved below with execution filenames anonymized and fix metadata retained. Empty arrays are actual empty outputs. Each stdout file also has a `.command.json`, `.stderr.txt` and `.diagnostics.json` sibling in both the original and export directories.

<details>
<summary>A_original_visible</summary>

Original: [A_original_visible.stdout.txt](../../datasets/results/phase3/trials/fstring_boundary--specific_first/black/A_original_visible.stdout.txt). Export: [A_original_visible.stdout.txt](exports/fstring_boundary--specific_first/black/A_original_visible.stdout.txt). Replay: [A_original_visible.stdout.txt](exports/fstring_boundary--specific_first/black/rechecks/A_original_visible.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 18,
      "row": 2
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-dp31g2pe\\study_input.py",
    "fix": null,
    "location": {
      "column": 9,
      "row": 2
    },
    "message": "Undefined name `missing_b`",
    "noqa_row": 2,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  }
]
```

</details>

<details>
<summary>B_original_underlying</summary>

Original: [B_original_underlying.stdout.txt](../../datasets/results/phase3/trials/fstring_boundary--specific_first/black/B_original_underlying.stdout.txt). Export: [B_original_underlying.stdout.txt](exports/fstring_boundary--specific_first/black/B_original_underlying.stdout.txt). Replay: [B_original_underlying.stdout.txt](exports/fstring_boundary--specific_first/black/rechecks/B_original_underlying.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 20,
      "row": 1
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-zn2m4cti\\study_input.py",
    "fix": null,
    "location": {
      "column": 11,
      "row": 1
    },
    "message": "Undefined name `missing_a`",
    "noqa_row": 1,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  },
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 18,
      "row": 2
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-zn2m4cti\\study_input.py",
    "fix": null,
    "location": {
      "column": 9,
      "row": 2
    },
    "message": "Undefined name `missing_b`",
    "noqa_row": 2,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  }
]
```

</details>

<details>
<summary>C_formatted_visible</summary>

Original: [C_formatted_visible.stdout.txt](../../datasets/results/phase3/trials/fstring_boundary--specific_first/black/C_formatted_visible.stdout.txt). Export: [C_formatted_visible.stdout.txt](exports/fstring_boundary--specific_first/black/C_formatted_visible.stdout.txt). Replay: [C_formatted_visible.stdout.txt](exports/fstring_boundary--specific_first/black/rechecks/C_formatted_visible.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 18,
      "row": 2
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-w6vvirae\\study_input.py",
    "fix": null,
    "location": {
      "column": 9,
      "row": 2
    },
    "message": "Undefined name `missing_b`",
    "noqa_row": 2,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  }
]
```

</details>

<details>
<summary>D_formatted_underlying</summary>

Original: [D_formatted_underlying.stdout.txt](../../datasets/results/phase3/trials/fstring_boundary--specific_first/black/D_formatted_underlying.stdout.txt). Export: [D_formatted_underlying.stdout.txt](exports/fstring_boundary--specific_first/black/D_formatted_underlying.stdout.txt). Replay: [D_formatted_underlying.stdout.txt](exports/fstring_boundary--specific_first/black/rechecks/D_formatted_underlying.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 20,
      "row": 1
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-bm15rori\\study_input.py",
    "fix": null,
    "location": {
      "column": 11,
      "row": 1
    },
    "message": "Undefined name `missing_a`",
    "noqa_row": 1,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  },
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 18,
      "row": 2
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-bm15rori\\study_input.py",
    "fix": null,
    "location": {
      "column": 9,
      "row": 2
    },
    "message": "Undefined name `missing_b`",
    "noqa_row": 2,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  }
]
```

</details>

<a id="comparison-28"></a>

## 28. fstring_boundary--specific_first / ruff

**Original label:** Ambiguous. **Proposed review resolution:** Preserved.

Original evidence directory: `datasets/results/phase3/trials/fstring_boundary--specific_first/ruff`

Review export directory: `reports/ambiguous-audit/exports/fstring_boundary--specific_first/ruff`

### Sources and exact evidence paths

Original source: [before.py](../../datasets/results/phase3/trials/fstring_boundary--specific_first/ruff/before.py); byte-identical export: [before.py](exports/fstring_boundary--specific_first/ruff/before.py). SHA-256: `24d8abe2e3ca9e4ff8756f4421b4270b9bcf696639e00803225b1dfedc662bf0`.

```python
text = f"{missing_a}"  # noqa: F821
other = missing_b
```

Formatted source: [after.py](../../datasets/results/phase3/trials/fstring_boundary--specific_first/ruff/after.py); byte-identical export: [after.py](exports/fstring_boundary--specific_first/ruff/after.py). SHA-256: `24d8abe2e3ca9e4ff8756f4421b4270b9bcf696639e00803225b1dfedc662bf0`.

```python
text = f"{missing_a}"  # noqa: F821
other = missing_b
```

Original decision: [result.json](../../datasets/results/phase3/trials/fstring_boundary--specific_first/ruff/result.json); failure details: [matching.json](../../datasets/results/phase3/trials/fstring_boundary--specific_first/ruff/matching.json); formatter invocation: [formatter.command.json](../../datasets/results/phase3/trials/fstring_boundary--specific_first/ruff/formatter.command.json). Full byte-identical copies are in the export directory.

### Why the matcher abstained

Exact recorded error: `Diagnostic or construct does not align with complete code tokens`.

F821 points to `missing_a` inside a formatted-value expression. Python 3.11 tokenize emits the whole f-string as a STRING token, so the embedded identifier span is not a complete token span under the primary matcher. This is a tokenization/coverage boundary, not evidence of a changed suppression.

### Noqa placement

| Snapshot | Position (1-based) | Kind | Exact comment | Preceding code on line |
|---|---|---|---|---|
| before | 1:24-36 | inline | `# noqa: F821` | `text = f"{missing_a}"` |
| after | 1:24-36 | inline | `# noqa: F821` | `text = f"{missing_a}"` |

### Warning identities and visibility

The identities below are review-only, not original automated matcher identities. V = visible; S = suppressed; ranges are 1-based with exclusive end columns.

| Identity / source role | Warning and source slice | Before range | After range | A / B / C / D | Judgment |
|---|---|---|---|---|---|
| `review:F821@$.body[0].value.values[0].value`; load Name | F821: `missing_a`; Undefined name `missing_a` | 1:11-1:20 | 1:11-1:20 | S / V / S / V | suppressed in both |
| `review:F821@$.body[1].value`; load Name | F821: `missing_b`; Undefined name `missing_b` | 2:9-2:18 | 2:9-2:18 | V / V / V / V | visible in both |

### Evidence-based judgment and human review

Original and formatted source are byte-identical. Full underlying and visible warnings reproduce; corresponding occurrences cannot move in an identical snapshot. F821 `missing_a` is suppressed in both; F821 `missing_b` is visible in both. All four saved outputs replay exactly after ignoring only temporary filenames. Neutralizing directive comments makes ordinary lint reproduce the underlying warnings in both snapshots. Proposed resolution: Preserved; no corresponding warning changes its visible/suppressed state.

Human interpretation: Independent human adjudication is pending; this is an AI-assisted proposal.

Saved replays and comment-neutralized sources: `reports/ambiguous-audit/exports/fstring_boundary--specific_first/ruff/rechecks`. All four replay stdout/stderr and command records are saved there; both neutralized ordinary-lint passes reproduce their respective underlying outputs.

### All four original raw Ruff diagnostic outputs

Privacy-derived JSON is preserved below with execution filenames anonymized and fix metadata retained. Empty arrays are actual empty outputs. Each stdout file also has a `.command.json`, `.stderr.txt` and `.diagnostics.json` sibling in both the original and export directories.

<details>
<summary>A_original_visible</summary>

Original: [A_original_visible.stdout.txt](../../datasets/results/phase3/trials/fstring_boundary--specific_first/ruff/A_original_visible.stdout.txt). Export: [A_original_visible.stdout.txt](exports/fstring_boundary--specific_first/ruff/A_original_visible.stdout.txt). Replay: [A_original_visible.stdout.txt](exports/fstring_boundary--specific_first/ruff/rechecks/A_original_visible.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 18,
      "row": 2
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-5ucaj63x\\study_input.py",
    "fix": null,
    "location": {
      "column": 9,
      "row": 2
    },
    "message": "Undefined name `missing_b`",
    "noqa_row": 2,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  }
]
```

</details>

<details>
<summary>B_original_underlying</summary>

Original: [B_original_underlying.stdout.txt](../../datasets/results/phase3/trials/fstring_boundary--specific_first/ruff/B_original_underlying.stdout.txt). Export: [B_original_underlying.stdout.txt](exports/fstring_boundary--specific_first/ruff/B_original_underlying.stdout.txt). Replay: [B_original_underlying.stdout.txt](exports/fstring_boundary--specific_first/ruff/rechecks/B_original_underlying.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 20,
      "row": 1
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-w8ojuno8\\study_input.py",
    "fix": null,
    "location": {
      "column": 11,
      "row": 1
    },
    "message": "Undefined name `missing_a`",
    "noqa_row": 1,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  },
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 18,
      "row": 2
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-w8ojuno8\\study_input.py",
    "fix": null,
    "location": {
      "column": 9,
      "row": 2
    },
    "message": "Undefined name `missing_b`",
    "noqa_row": 2,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  }
]
```

</details>

<details>
<summary>C_formatted_visible</summary>

Original: [C_formatted_visible.stdout.txt](../../datasets/results/phase3/trials/fstring_boundary--specific_first/ruff/C_formatted_visible.stdout.txt). Export: [C_formatted_visible.stdout.txt](exports/fstring_boundary--specific_first/ruff/C_formatted_visible.stdout.txt). Replay: [C_formatted_visible.stdout.txt](exports/fstring_boundary--specific_first/ruff/rechecks/C_formatted_visible.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 18,
      "row": 2
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-7uganzz8\\study_input.py",
    "fix": null,
    "location": {
      "column": 9,
      "row": 2
    },
    "message": "Undefined name `missing_b`",
    "noqa_row": 2,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  }
]
```

</details>

<details>
<summary>D_formatted_underlying</summary>

Original: [D_formatted_underlying.stdout.txt](../../datasets/results/phase3/trials/fstring_boundary--specific_first/ruff/D_formatted_underlying.stdout.txt). Export: [D_formatted_underlying.stdout.txt](exports/fstring_boundary--specific_first/ruff/D_formatted_underlying.stdout.txt). Replay: [D_formatted_underlying.stdout.txt](exports/fstring_boundary--specific_first/ruff/rechecks/D_formatted_underlying.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 20,
      "row": 1
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-mgx_9xeu\\study_input.py",
    "fix": null,
    "location": {
      "column": 11,
      "row": 1
    },
    "message": "Undefined name `missing_a`",
    "noqa_row": 1,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  },
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 18,
      "row": 2
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-mgx_9xeu\\study_input.py",
    "fix": null,
    "location": {
      "column": 9,
      "row": 2
    },
    "message": "Undefined name `missing_b`",
    "noqa_row": 2,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  }
]
```

</details>

<a id="comparison-29"></a>

## 29. fstring_boundary--specific_last / black

**Original label:** Ambiguous. **Proposed review resolution:** Preserved.

Original evidence directory: `datasets/results/phase3/trials/fstring_boundary--specific_last/black`

Review export directory: `reports/ambiguous-audit/exports/fstring_boundary--specific_last/black`

### Sources and exact evidence paths

Original source: [before.py](../../datasets/results/phase3/trials/fstring_boundary--specific_last/black/before.py); byte-identical export: [before.py](exports/fstring_boundary--specific_last/black/before.py). SHA-256: `055393e4672a6a5be832b3bf2c2e5f29c9a3f095cc812b24aa2f9f6ca633e49e`.

```python
text = f"{missing_a}"
other = missing_b  # noqa: F821
```

Formatted source: [after.py](../../datasets/results/phase3/trials/fstring_boundary--specific_last/black/after.py); byte-identical export: [after.py](exports/fstring_boundary--specific_last/black/after.py). SHA-256: `055393e4672a6a5be832b3bf2c2e5f29c9a3f095cc812b24aa2f9f6ca633e49e`.

```python
text = f"{missing_a}"
other = missing_b  # noqa: F821
```

Original decision: [result.json](../../datasets/results/phase3/trials/fstring_boundary--specific_last/black/result.json); failure details: [matching.json](../../datasets/results/phase3/trials/fstring_boundary--specific_last/black/matching.json); formatter invocation: [formatter.command.json](../../datasets/results/phase3/trials/fstring_boundary--specific_last/black/formatter.command.json). Full byte-identical copies are in the export directory.

### Why the matcher abstained

Exact recorded error: `Diagnostic or construct does not align with complete code tokens`.

F821 points to `missing_a` inside a formatted-value expression. Python 3.11 tokenize emits the whole f-string as a STRING token, so the embedded identifier span is not a complete token span under the primary matcher. This is a tokenization/coverage boundary, not evidence of a changed suppression.

### Noqa placement

| Snapshot | Position (1-based) | Kind | Exact comment | Preceding code on line |
|---|---|---|---|---|
| before | 2:20-32 | inline | `# noqa: F821` | `other = missing_b` |
| after | 2:20-32 | inline | `# noqa: F821` | `other = missing_b` |

### Warning identities and visibility

The identities below are review-only, not original automated matcher identities. V = visible; S = suppressed; ranges are 1-based with exclusive end columns.

| Identity / source role | Warning and source slice | Before range | After range | A / B / C / D | Judgment |
|---|---|---|---|---|---|
| `review:F821@$.body[0].value.values[0].value`; load Name | F821: `missing_a`; Undefined name `missing_a` | 1:11-1:20 | 1:11-1:20 | V / V / V / V | visible in both |
| `review:F821@$.body[1].value`; load Name | F821: `missing_b`; Undefined name `missing_b` | 2:9-2:18 | 2:9-2:18 | S / V / S / V | suppressed in both |

### Evidence-based judgment and human review

Original and formatted source are byte-identical. Full underlying and visible warnings reproduce; corresponding occurrences cannot move in an identical snapshot. F821 `missing_a` is visible in both; F821 `missing_b` is suppressed in both. All four saved outputs replay exactly after ignoring only temporary filenames. Neutralizing directive comments makes ordinary lint reproduce the underlying warnings in both snapshots. Proposed resolution: Preserved; no corresponding warning changes its visible/suppressed state.

Human interpretation: Independent human adjudication is pending; this is an AI-assisted proposal.

Saved replays and comment-neutralized sources: `reports/ambiguous-audit/exports/fstring_boundary--specific_last/black/rechecks`. All four replay stdout/stderr and command records are saved there; both neutralized ordinary-lint passes reproduce their respective underlying outputs.

### All four original raw Ruff diagnostic outputs

Privacy-derived JSON is preserved below with execution filenames anonymized and fix metadata retained. Empty arrays are actual empty outputs. Each stdout file also has a `.command.json`, `.stderr.txt` and `.diagnostics.json` sibling in both the original and export directories.

<details>
<summary>A_original_visible</summary>

Original: [A_original_visible.stdout.txt](../../datasets/results/phase3/trials/fstring_boundary--specific_last/black/A_original_visible.stdout.txt). Export: [A_original_visible.stdout.txt](exports/fstring_boundary--specific_last/black/A_original_visible.stdout.txt). Replay: [A_original_visible.stdout.txt](exports/fstring_boundary--specific_last/black/rechecks/A_original_visible.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 20,
      "row": 1
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-jhpv77wd\\study_input.py",
    "fix": null,
    "location": {
      "column": 11,
      "row": 1
    },
    "message": "Undefined name `missing_a`",
    "noqa_row": 1,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  }
]
```

</details>

<details>
<summary>B_original_underlying</summary>

Original: [B_original_underlying.stdout.txt](../../datasets/results/phase3/trials/fstring_boundary--specific_last/black/B_original_underlying.stdout.txt). Export: [B_original_underlying.stdout.txt](exports/fstring_boundary--specific_last/black/B_original_underlying.stdout.txt). Replay: [B_original_underlying.stdout.txt](exports/fstring_boundary--specific_last/black/rechecks/B_original_underlying.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 20,
      "row": 1
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-rmpux472\\study_input.py",
    "fix": null,
    "location": {
      "column": 11,
      "row": 1
    },
    "message": "Undefined name `missing_a`",
    "noqa_row": 1,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  },
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 18,
      "row": 2
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-rmpux472\\study_input.py",
    "fix": null,
    "location": {
      "column": 9,
      "row": 2
    },
    "message": "Undefined name `missing_b`",
    "noqa_row": 2,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  }
]
```

</details>

<details>
<summary>C_formatted_visible</summary>

Original: [C_formatted_visible.stdout.txt](../../datasets/results/phase3/trials/fstring_boundary--specific_last/black/C_formatted_visible.stdout.txt). Export: [C_formatted_visible.stdout.txt](exports/fstring_boundary--specific_last/black/C_formatted_visible.stdout.txt). Replay: [C_formatted_visible.stdout.txt](exports/fstring_boundary--specific_last/black/rechecks/C_formatted_visible.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 20,
      "row": 1
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-ayhu_6pt\\study_input.py",
    "fix": null,
    "location": {
      "column": 11,
      "row": 1
    },
    "message": "Undefined name `missing_a`",
    "noqa_row": 1,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  }
]
```

</details>

<details>
<summary>D_formatted_underlying</summary>

Original: [D_formatted_underlying.stdout.txt](../../datasets/results/phase3/trials/fstring_boundary--specific_last/black/D_formatted_underlying.stdout.txt). Export: [D_formatted_underlying.stdout.txt](exports/fstring_boundary--specific_last/black/D_formatted_underlying.stdout.txt). Replay: [D_formatted_underlying.stdout.txt](exports/fstring_boundary--specific_last/black/rechecks/D_formatted_underlying.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 20,
      "row": 1
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-dwvz4z_v\\study_input.py",
    "fix": null,
    "location": {
      "column": 11,
      "row": 1
    },
    "message": "Undefined name `missing_a`",
    "noqa_row": 1,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  },
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 18,
      "row": 2
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-dwvz4z_v\\study_input.py",
    "fix": null,
    "location": {
      "column": 9,
      "row": 2
    },
    "message": "Undefined name `missing_b`",
    "noqa_row": 2,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  }
]
```

</details>

<a id="comparison-30"></a>

## 30. fstring_boundary--specific_last / ruff

**Original label:** Ambiguous. **Proposed review resolution:** Preserved.

Original evidence directory: `datasets/results/phase3/trials/fstring_boundary--specific_last/ruff`

Review export directory: `reports/ambiguous-audit/exports/fstring_boundary--specific_last/ruff`

### Sources and exact evidence paths

Original source: [before.py](../../datasets/results/phase3/trials/fstring_boundary--specific_last/ruff/before.py); byte-identical export: [before.py](exports/fstring_boundary--specific_last/ruff/before.py). SHA-256: `055393e4672a6a5be832b3bf2c2e5f29c9a3f095cc812b24aa2f9f6ca633e49e`.

```python
text = f"{missing_a}"
other = missing_b  # noqa: F821
```

Formatted source: [after.py](../../datasets/results/phase3/trials/fstring_boundary--specific_last/ruff/after.py); byte-identical export: [after.py](exports/fstring_boundary--specific_last/ruff/after.py). SHA-256: `055393e4672a6a5be832b3bf2c2e5f29c9a3f095cc812b24aa2f9f6ca633e49e`.

```python
text = f"{missing_a}"
other = missing_b  # noqa: F821
```

Original decision: [result.json](../../datasets/results/phase3/trials/fstring_boundary--specific_last/ruff/result.json); failure details: [matching.json](../../datasets/results/phase3/trials/fstring_boundary--specific_last/ruff/matching.json); formatter invocation: [formatter.command.json](../../datasets/results/phase3/trials/fstring_boundary--specific_last/ruff/formatter.command.json). Full byte-identical copies are in the export directory.

### Why the matcher abstained

Exact recorded error: `Diagnostic or construct does not align with complete code tokens`.

F821 points to `missing_a` inside a formatted-value expression. Python 3.11 tokenize emits the whole f-string as a STRING token, so the embedded identifier span is not a complete token span under the primary matcher. This is a tokenization/coverage boundary, not evidence of a changed suppression.

### Noqa placement

| Snapshot | Position (1-based) | Kind | Exact comment | Preceding code on line |
|---|---|---|---|---|
| before | 2:20-32 | inline | `# noqa: F821` | `other = missing_b` |
| after | 2:20-32 | inline | `# noqa: F821` | `other = missing_b` |

### Warning identities and visibility

The identities below are review-only, not original automated matcher identities. V = visible; S = suppressed; ranges are 1-based with exclusive end columns.

| Identity / source role | Warning and source slice | Before range | After range | A / B / C / D | Judgment |
|---|---|---|---|---|---|
| `review:F821@$.body[0].value.values[0].value`; load Name | F821: `missing_a`; Undefined name `missing_a` | 1:11-1:20 | 1:11-1:20 | V / V / V / V | visible in both |
| `review:F821@$.body[1].value`; load Name | F821: `missing_b`; Undefined name `missing_b` | 2:9-2:18 | 2:9-2:18 | S / V / S / V | suppressed in both |

### Evidence-based judgment and human review

Original and formatted source are byte-identical. Full underlying and visible warnings reproduce; corresponding occurrences cannot move in an identical snapshot. F821 `missing_a` is visible in both; F821 `missing_b` is suppressed in both. All four saved outputs replay exactly after ignoring only temporary filenames. Neutralizing directive comments makes ordinary lint reproduce the underlying warnings in both snapshots. Proposed resolution: Preserved; no corresponding warning changes its visible/suppressed state.

Human interpretation: Independent human adjudication is pending; this is an AI-assisted proposal.

Saved replays and comment-neutralized sources: `reports/ambiguous-audit/exports/fstring_boundary--specific_last/ruff/rechecks`. All four replay stdout/stderr and command records are saved there; both neutralized ordinary-lint passes reproduce their respective underlying outputs.

### All four original raw Ruff diagnostic outputs

Privacy-derived JSON is preserved below with execution filenames anonymized and fix metadata retained. Empty arrays are actual empty outputs. Each stdout file also has a `.command.json`, `.stderr.txt` and `.diagnostics.json` sibling in both the original and export directories.

<details>
<summary>A_original_visible</summary>

Original: [A_original_visible.stdout.txt](../../datasets/results/phase3/trials/fstring_boundary--specific_last/ruff/A_original_visible.stdout.txt). Export: [A_original_visible.stdout.txt](exports/fstring_boundary--specific_last/ruff/A_original_visible.stdout.txt). Replay: [A_original_visible.stdout.txt](exports/fstring_boundary--specific_last/ruff/rechecks/A_original_visible.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 20,
      "row": 1
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-bx5tkky2\\study_input.py",
    "fix": null,
    "location": {
      "column": 11,
      "row": 1
    },
    "message": "Undefined name `missing_a`",
    "noqa_row": 1,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  }
]
```

</details>

<details>
<summary>B_original_underlying</summary>

Original: [B_original_underlying.stdout.txt](../../datasets/results/phase3/trials/fstring_boundary--specific_last/ruff/B_original_underlying.stdout.txt). Export: [B_original_underlying.stdout.txt](exports/fstring_boundary--specific_last/ruff/B_original_underlying.stdout.txt). Replay: [B_original_underlying.stdout.txt](exports/fstring_boundary--specific_last/ruff/rechecks/B_original_underlying.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 20,
      "row": 1
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-3kg3gp04\\study_input.py",
    "fix": null,
    "location": {
      "column": 11,
      "row": 1
    },
    "message": "Undefined name `missing_a`",
    "noqa_row": 1,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  },
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 18,
      "row": 2
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-3kg3gp04\\study_input.py",
    "fix": null,
    "location": {
      "column": 9,
      "row": 2
    },
    "message": "Undefined name `missing_b`",
    "noqa_row": 2,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  }
]
```

</details>

<details>
<summary>C_formatted_visible</summary>

Original: [C_formatted_visible.stdout.txt](../../datasets/results/phase3/trials/fstring_boundary--specific_last/ruff/C_formatted_visible.stdout.txt). Export: [C_formatted_visible.stdout.txt](exports/fstring_boundary--specific_last/ruff/C_formatted_visible.stdout.txt). Replay: [C_formatted_visible.stdout.txt](exports/fstring_boundary--specific_last/ruff/rechecks/C_formatted_visible.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 20,
      "row": 1
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-ookf6x66\\study_input.py",
    "fix": null,
    "location": {
      "column": 11,
      "row": 1
    },
    "message": "Undefined name `missing_a`",
    "noqa_row": 1,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  }
]
```

</details>

<details>
<summary>D_formatted_underlying</summary>

Original: [D_formatted_underlying.stdout.txt](../../datasets/results/phase3/trials/fstring_boundary--specific_last/ruff/D_formatted_underlying.stdout.txt). Export: [D_formatted_underlying.stdout.txt](exports/fstring_boundary--specific_last/ruff/D_formatted_underlying.stdout.txt). Replay: [D_formatted_underlying.stdout.txt](exports/fstring_boundary--specific_last/ruff/rechecks/D_formatted_underlying.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 20,
      "row": 1
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-o7faminj\\study_input.py",
    "fix": null,
    "location": {
      "column": 11,
      "row": 1
    },
    "message": "Undefined name `missing_a`",
    "noqa_row": 1,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  },
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 18,
      "row": 2
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-o7faminj\\study_input.py",
    "fix": null,
    "location": {
      "column": 9,
      "row": 2
    },
    "message": "Undefined name `missing_b`",
    "noqa_row": 2,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  }
]
```

</details>

<a id="comparison-31"></a>

## 31. fstring_boundary--standalone_first / black

**Original label:** Ambiguous. **Proposed review resolution:** Preserved.

Original evidence directory: `datasets/results/phase3/trials/fstring_boundary--standalone_first/black`

Review export directory: `reports/ambiguous-audit/exports/fstring_boundary--standalone_first/black`

### Sources and exact evidence paths

Original source: [before.py](../../datasets/results/phase3/trials/fstring_boundary--standalone_first/black/before.py); byte-identical export: [before.py](exports/fstring_boundary--standalone_first/black/before.py). SHA-256: `166efa941bdd975739eec5e9d6e4387bb5cefdfb7292f232b3082fb1ff3dedc2`.

```python
# noqa: F821
text = f"{missing_a}"
other = missing_b
```

Formatted source: [after.py](../../datasets/results/phase3/trials/fstring_boundary--standalone_first/black/after.py); byte-identical export: [after.py](exports/fstring_boundary--standalone_first/black/after.py). SHA-256: `166efa941bdd975739eec5e9d6e4387bb5cefdfb7292f232b3082fb1ff3dedc2`.

```python
# noqa: F821
text = f"{missing_a}"
other = missing_b
```

Original decision: [result.json](../../datasets/results/phase3/trials/fstring_boundary--standalone_first/black/result.json); failure details: [matching.json](../../datasets/results/phase3/trials/fstring_boundary--standalone_first/black/matching.json); formatter invocation: [formatter.command.json](../../datasets/results/phase3/trials/fstring_boundary--standalone_first/black/formatter.command.json). Full byte-identical copies are in the export directory.

### Why the matcher abstained

Exact recorded error: `Diagnostic or construct does not align with complete code tokens`.

F821 points to `missing_a` inside a formatted-value expression. Python 3.11 tokenize emits the whole f-string as a STRING token, so the embedded identifier span is not a complete token span under the primary matcher. This is a tokenization/coverage boundary, not evidence of a changed suppression.

### Noqa placement

| Snapshot | Position (1-based) | Kind | Exact comment | Preceding code on line |
|---|---|---|---|---|
| before | 1:1-13 | standalone | `# noqa: F821` | `` |
| after | 1:1-13 | standalone | `# noqa: F821` | `` |

### Warning identities and visibility

The identities below are review-only, not original automated matcher identities. V = visible; S = suppressed; ranges are 1-based with exclusive end columns.

| Identity / source role | Warning and source slice | Before range | After range | A / B / C / D | Judgment |
|---|---|---|---|---|---|
| `review:F821@$.body[0].value.values[0].value`; load Name | F821: `missing_a`; Undefined name `missing_a` | 2:11-2:20 | 2:11-2:20 | V / V / V / V | visible in both |
| `review:F821@$.body[1].value`; load Name | F821: `missing_b`; Undefined name `missing_b` | 3:9-3:18 | 3:9-3:18 | V / V / V / V | visible in both |

### Evidence-based judgment and human review

Original and formatted source are byte-identical. Full underlying and visible warnings reproduce; corresponding occurrences cannot move in an identical snapshot. F821 `missing_a` is visible in both; F821 `missing_b` is visible in both. All four saved outputs replay exactly after ignoring only temporary filenames. Neutralizing directive comments makes ordinary lint reproduce the underlying warnings in both snapshots. Proposed resolution: Preserved; no corresponding warning changes its visible/suppressed state.

Human interpretation: Independent human adjudication is pending; this is an AI-assisted proposal. The standalone directive suppresses neither selected warning in the measured passes. Intended next-line suppression cannot be inferred; this does not make observed visibility uncertain.

Saved replays and comment-neutralized sources: `reports/ambiguous-audit/exports/fstring_boundary--standalone_first/black/rechecks`. All four replay stdout/stderr and command records are saved there; both neutralized ordinary-lint passes reproduce their respective underlying outputs.

### All four original raw Ruff diagnostic outputs

Privacy-derived JSON is preserved below with execution filenames anonymized and fix metadata retained. Empty arrays are actual empty outputs. Each stdout file also has a `.command.json`, `.stderr.txt` and `.diagnostics.json` sibling in both the original and export directories.

<details>
<summary>A_original_visible</summary>

Original: [A_original_visible.stdout.txt](../../datasets/results/phase3/trials/fstring_boundary--standalone_first/black/A_original_visible.stdout.txt). Export: [A_original_visible.stdout.txt](exports/fstring_boundary--standalone_first/black/A_original_visible.stdout.txt). Replay: [A_original_visible.stdout.txt](exports/fstring_boundary--standalone_first/black/rechecks/A_original_visible.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 20,
      "row": 2
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-nhokwvyd\\study_input.py",
    "fix": null,
    "location": {
      "column": 11,
      "row": 2
    },
    "message": "Undefined name `missing_a`",
    "noqa_row": 2,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  },
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 18,
      "row": 3
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-nhokwvyd\\study_input.py",
    "fix": null,
    "location": {
      "column": 9,
      "row": 3
    },
    "message": "Undefined name `missing_b`",
    "noqa_row": 3,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  }
]
```

</details>

<details>
<summary>B_original_underlying</summary>

Original: [B_original_underlying.stdout.txt](../../datasets/results/phase3/trials/fstring_boundary--standalone_first/black/B_original_underlying.stdout.txt). Export: [B_original_underlying.stdout.txt](exports/fstring_boundary--standalone_first/black/B_original_underlying.stdout.txt). Replay: [B_original_underlying.stdout.txt](exports/fstring_boundary--standalone_first/black/rechecks/B_original_underlying.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 20,
      "row": 2
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-pn02gpwr\\study_input.py",
    "fix": null,
    "location": {
      "column": 11,
      "row": 2
    },
    "message": "Undefined name `missing_a`",
    "noqa_row": 2,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  },
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 18,
      "row": 3
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-pn02gpwr\\study_input.py",
    "fix": null,
    "location": {
      "column": 9,
      "row": 3
    },
    "message": "Undefined name `missing_b`",
    "noqa_row": 3,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  }
]
```

</details>

<details>
<summary>C_formatted_visible</summary>

Original: [C_formatted_visible.stdout.txt](../../datasets/results/phase3/trials/fstring_boundary--standalone_first/black/C_formatted_visible.stdout.txt). Export: [C_formatted_visible.stdout.txt](exports/fstring_boundary--standalone_first/black/C_formatted_visible.stdout.txt). Replay: [C_formatted_visible.stdout.txt](exports/fstring_boundary--standalone_first/black/rechecks/C_formatted_visible.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 20,
      "row": 2
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-4iyisbp9\\study_input.py",
    "fix": null,
    "location": {
      "column": 11,
      "row": 2
    },
    "message": "Undefined name `missing_a`",
    "noqa_row": 2,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  },
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 18,
      "row": 3
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-4iyisbp9\\study_input.py",
    "fix": null,
    "location": {
      "column": 9,
      "row": 3
    },
    "message": "Undefined name `missing_b`",
    "noqa_row": 3,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  }
]
```

</details>

<details>
<summary>D_formatted_underlying</summary>

Original: [D_formatted_underlying.stdout.txt](../../datasets/results/phase3/trials/fstring_boundary--standalone_first/black/D_formatted_underlying.stdout.txt). Export: [D_formatted_underlying.stdout.txt](exports/fstring_boundary--standalone_first/black/D_formatted_underlying.stdout.txt). Replay: [D_formatted_underlying.stdout.txt](exports/fstring_boundary--standalone_first/black/rechecks/D_formatted_underlying.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 20,
      "row": 2
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-4q8nvkgj\\study_input.py",
    "fix": null,
    "location": {
      "column": 11,
      "row": 2
    },
    "message": "Undefined name `missing_a`",
    "noqa_row": 2,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  },
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 18,
      "row": 3
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-4q8nvkgj\\study_input.py",
    "fix": null,
    "location": {
      "column": 9,
      "row": 3
    },
    "message": "Undefined name `missing_b`",
    "noqa_row": 3,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  }
]
```

</details>

<a id="comparison-32"></a>

## 32. fstring_boundary--standalone_first / ruff

**Original label:** Ambiguous. **Proposed review resolution:** Preserved.

Original evidence directory: `datasets/results/phase3/trials/fstring_boundary--standalone_first/ruff`

Review export directory: `reports/ambiguous-audit/exports/fstring_boundary--standalone_first/ruff`

### Sources and exact evidence paths

Original source: [before.py](../../datasets/results/phase3/trials/fstring_boundary--standalone_first/ruff/before.py); byte-identical export: [before.py](exports/fstring_boundary--standalone_first/ruff/before.py). SHA-256: `166efa941bdd975739eec5e9d6e4387bb5cefdfb7292f232b3082fb1ff3dedc2`.

```python
# noqa: F821
text = f"{missing_a}"
other = missing_b
```

Formatted source: [after.py](../../datasets/results/phase3/trials/fstring_boundary--standalone_first/ruff/after.py); byte-identical export: [after.py](exports/fstring_boundary--standalone_first/ruff/after.py). SHA-256: `166efa941bdd975739eec5e9d6e4387bb5cefdfb7292f232b3082fb1ff3dedc2`.

```python
# noqa: F821
text = f"{missing_a}"
other = missing_b
```

Original decision: [result.json](../../datasets/results/phase3/trials/fstring_boundary--standalone_first/ruff/result.json); failure details: [matching.json](../../datasets/results/phase3/trials/fstring_boundary--standalone_first/ruff/matching.json); formatter invocation: [formatter.command.json](../../datasets/results/phase3/trials/fstring_boundary--standalone_first/ruff/formatter.command.json). Full byte-identical copies are in the export directory.

### Why the matcher abstained

Exact recorded error: `Diagnostic or construct does not align with complete code tokens`.

F821 points to `missing_a` inside a formatted-value expression. Python 3.11 tokenize emits the whole f-string as a STRING token, so the embedded identifier span is not a complete token span under the primary matcher. This is a tokenization/coverage boundary, not evidence of a changed suppression.

### Noqa placement

| Snapshot | Position (1-based) | Kind | Exact comment | Preceding code on line |
|---|---|---|---|---|
| before | 1:1-13 | standalone | `# noqa: F821` | `` |
| after | 1:1-13 | standalone | `# noqa: F821` | `` |

### Warning identities and visibility

The identities below are review-only, not original automated matcher identities. V = visible; S = suppressed; ranges are 1-based with exclusive end columns.

| Identity / source role | Warning and source slice | Before range | After range | A / B / C / D | Judgment |
|---|---|---|---|---|---|
| `review:F821@$.body[0].value.values[0].value`; load Name | F821: `missing_a`; Undefined name `missing_a` | 2:11-2:20 | 2:11-2:20 | V / V / V / V | visible in both |
| `review:F821@$.body[1].value`; load Name | F821: `missing_b`; Undefined name `missing_b` | 3:9-3:18 | 3:9-3:18 | V / V / V / V | visible in both |

### Evidence-based judgment and human review

Original and formatted source are byte-identical. Full underlying and visible warnings reproduce; corresponding occurrences cannot move in an identical snapshot. F821 `missing_a` is visible in both; F821 `missing_b` is visible in both. All four saved outputs replay exactly after ignoring only temporary filenames. Neutralizing directive comments makes ordinary lint reproduce the underlying warnings in both snapshots. Proposed resolution: Preserved; no corresponding warning changes its visible/suppressed state.

Human interpretation: Independent human adjudication is pending; this is an AI-assisted proposal. The standalone directive suppresses neither selected warning in the measured passes. Intended next-line suppression cannot be inferred; this does not make observed visibility uncertain.

Saved replays and comment-neutralized sources: `reports/ambiguous-audit/exports/fstring_boundary--standalone_first/ruff/rechecks`. All four replay stdout/stderr and command records are saved there; both neutralized ordinary-lint passes reproduce their respective underlying outputs.

### All four original raw Ruff diagnostic outputs

Privacy-derived JSON is preserved below with execution filenames anonymized and fix metadata retained. Empty arrays are actual empty outputs. Each stdout file also has a `.command.json`, `.stderr.txt` and `.diagnostics.json` sibling in both the original and export directories.

<details>
<summary>A_original_visible</summary>

Original: [A_original_visible.stdout.txt](../../datasets/results/phase3/trials/fstring_boundary--standalone_first/ruff/A_original_visible.stdout.txt). Export: [A_original_visible.stdout.txt](exports/fstring_boundary--standalone_first/ruff/A_original_visible.stdout.txt). Replay: [A_original_visible.stdout.txt](exports/fstring_boundary--standalone_first/ruff/rechecks/A_original_visible.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 20,
      "row": 2
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-flgn7x_d\\study_input.py",
    "fix": null,
    "location": {
      "column": 11,
      "row": 2
    },
    "message": "Undefined name `missing_a`",
    "noqa_row": 2,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  },
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 18,
      "row": 3
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-flgn7x_d\\study_input.py",
    "fix": null,
    "location": {
      "column": 9,
      "row": 3
    },
    "message": "Undefined name `missing_b`",
    "noqa_row": 3,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  }
]
```

</details>

<details>
<summary>B_original_underlying</summary>

Original: [B_original_underlying.stdout.txt](../../datasets/results/phase3/trials/fstring_boundary--standalone_first/ruff/B_original_underlying.stdout.txt). Export: [B_original_underlying.stdout.txt](exports/fstring_boundary--standalone_first/ruff/B_original_underlying.stdout.txt). Replay: [B_original_underlying.stdout.txt](exports/fstring_boundary--standalone_first/ruff/rechecks/B_original_underlying.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 20,
      "row": 2
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-93673_eb\\study_input.py",
    "fix": null,
    "location": {
      "column": 11,
      "row": 2
    },
    "message": "Undefined name `missing_a`",
    "noqa_row": 2,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  },
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 18,
      "row": 3
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-93673_eb\\study_input.py",
    "fix": null,
    "location": {
      "column": 9,
      "row": 3
    },
    "message": "Undefined name `missing_b`",
    "noqa_row": 3,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  }
]
```

</details>

<details>
<summary>C_formatted_visible</summary>

Original: [C_formatted_visible.stdout.txt](../../datasets/results/phase3/trials/fstring_boundary--standalone_first/ruff/C_formatted_visible.stdout.txt). Export: [C_formatted_visible.stdout.txt](exports/fstring_boundary--standalone_first/ruff/C_formatted_visible.stdout.txt). Replay: [C_formatted_visible.stdout.txt](exports/fstring_boundary--standalone_first/ruff/rechecks/C_formatted_visible.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 20,
      "row": 2
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-fxw9o0ig\\study_input.py",
    "fix": null,
    "location": {
      "column": 11,
      "row": 2
    },
    "message": "Undefined name `missing_a`",
    "noqa_row": 2,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  },
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 18,
      "row": 3
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-fxw9o0ig\\study_input.py",
    "fix": null,
    "location": {
      "column": 9,
      "row": 3
    },
    "message": "Undefined name `missing_b`",
    "noqa_row": 3,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  }
]
```

</details>

<details>
<summary>D_formatted_underlying</summary>

Original: [D_formatted_underlying.stdout.txt](../../datasets/results/phase3/trials/fstring_boundary--standalone_first/ruff/D_formatted_underlying.stdout.txt). Export: [D_formatted_underlying.stdout.txt](exports/fstring_boundary--standalone_first/ruff/D_formatted_underlying.stdout.txt). Replay: [D_formatted_underlying.stdout.txt](exports/fstring_boundary--standalone_first/ruff/rechecks/D_formatted_underlying.stdout.txt).

```json
[
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 20,
      "row": 2
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-68s8f9zk\\study_input.py",
    "fix": null,
    "location": {
      "column": 11,
      "row": 2
    },
    "message": "Undefined name `missing_a`",
    "noqa_row": 2,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  },
  {
    "cell": null,
    "code": "F821",
    "end_location": {
      "column": 18,
      "row": 3
    },
    "filename": "<home>\\AppData\\Local\\Temp\\suppression-study-68s8f9zk\\study_input.py",
    "fix": null,
    "location": {
      "column": 9,
      "row": 3
    },
    "message": "Undefined name `missing_b`",
    "noqa_row": 3,
    "url": "https://docs.astral.sh/ruff/rules/undefined-name"
  }
]
```

</details>

## Reproduction and scope

Run `python scripts/audit_ambiguities.py --output reports/ambiguous-audit-NEW` using the pinned study environment. Outputs must be new directories under reports; existing audits cannot be overwritten. Run `python scripts/audit_ambiguities.py --verify reports/ambiguous-audit` to recheck the retained hashes, all selected comparison coverage and exact report regeneration without rerunning tools. This retrospective audit does not change the primary study or establish independent held-out accuracy.
