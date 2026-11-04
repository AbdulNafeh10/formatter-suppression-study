# Phase 2 — Diagnostic matching and validation

Completed 2026-11-03 UTC. Phase 3 has not been started.

## Implemented

`matching.py` builds structural paths to load/store Name and import-alias nodes.
Ruff Unicode-character coordinates locate each diagnostic in its own source;
Python AST byte columns are explicitly converted. Name ranges must cover an
entire identifier; import ranges must lie inside exactly one alias and align
with complete tokens. Cross-source correspondence additionally checks rule,
coordinate-free node content, construct tokens and diagnostic tokens. Source
positions are retained as evidence, never used alone across formatting.

`classifier.py` verifies complete underlying correspondence before comparing
visibility. It implements Preserved, Newly hidden, Newly exposed, Mixed,
Diagnostic changed, AST changed, and Ambiguous. Pipeline failures retain
Execution failure; invalid source is separately flagged. Newly hidden/exposed
counts are null when attribution is blocked. Matching evidence is saved alongside
raw four-pass measurements. Compilation checks source legality without execution.

The CLI reports affected identities and before/after positions. Exit statuses
are 0 Preserved, 1 suppression change, 2 invalid input/execution failure,
3 inconclusive (Ambiguous, AST changed or Diagnostic changed). Supplied pairs do
not establish formatter causation; the format command records actual tool output.

## Independent labels and real-tool controls

The prospective protocol and frozen labels were committed as `411f3a6` before
the matcher existed. The frozen manifest SHA-256 is:

`fe85727fb70422f1a043d7b06e81a8fab406622ce506b8644a82216e4295174b`

Eight hand-authored discovery inputs were measured with each pinned formatter,
and all sixteen results are retained in `datasets/results/phase2-probes`.
These records intentionally use the historical Phase 1 measurement-only schema;
their dataset_origin identifies the Phase 2 discovery purpose. They are not
Phase 3 data. No candidates, failures or negative results were discarded.

Ten development controls were selected to exercise known branches: eight actual
formatter outputs on six distinct inputs, plus two manual directive interventions.
The labels were specified literally and checked against raw rule/lexeme occurrences
and visibility in all four diagnostic passes. The repeated-name control labels
the first and second source occurrences separately. Same-length comment-only
neutralization restored the ignore-noqa diagnostics under ordinary linting while
preserving the code tokens and AST. No classifier prediction was used as a label.
See `phase2_control_labels.md` and per-control `independent_review.json` files.

## Executed results

The implementation baseline recorded by validation runs is commit `99763c9`.
Final automated verification: **76 tests passed**, implementation Ruff checks
passed, and Black reported all fifteen implementation/test/helper files unchanged.

All ten frozen controls agreed with expected classifications, individual warning
visibility states, affected-warning counts, and source/output checksums. Both
complete validation executions passed. The second run is a reproducibility check
on the same controls, not ten additional observations.

| Control origin | Preserved | Newly hidden | Newly exposed | Mixed |
|---|---:|---:|---:|---:|
| Actual formatter output | 2 | 1 | 5 | 0 |
| Manual directive intervention | 0 | 1 | 0 | 1 |

This is a description of deliberately selected development controls. It is not
a suppression-change prevalence estimate, formatter comparison rate, or held-out
detector-accuracy evaluation. All controls are synthetic and AI-assisted.

Two individually reproducible findings illustrate why line numbers and counts
alone are insufficient:

1. **Semicolon splitting, Black and Ruff:** `x=missing_a; y=missing_b  # noqa: F821`
   becomes two statements on separate lines with the directive attached to the
   second. Underlying diagnostics remain the same two AST occurrences; visible
   diagnostics change from zero to one. `missing_a` is newly exposed.
2. **Inline list, Black:** a two-line list with a directive after its first item
   collapses to `x = [missing_a, missing_b]  # noqa: F821`. Both underlying
   occurrences correspond; `missing_b` becomes newly hidden. Ruff's actual output
   for this same input retains its visible state. This example-specific difference
   does not justify a general superiority claim.

`scripts/verify_phase2.py` checked complete JSONL against individual records,
CSV labels/counts/output hashes, raw diagnostic stdout, source checksums, strict
AST equivalence and frozen-manifest provenance. It verified repeated diagnostic
content, matched identities, coverage transitions, underlying-change records and
counts after excluding only temporary filenames. All checks passed; the derived
summary is `reports/phase2/evidence_checks.json`.

Tests additionally cover unchanged sources, repeated identical names whose
coverage swaps with unchanged aggregate counts, F401 aliases, F841 targets,
comprehensions, Unicode including non-BMP characters, malformed diagnostics,
non-unique anchors, duplicate records, unsupported rules/spans, source illegality,
AST changes, partial-pass failure, real Ruff option failure, timeouts and CLI exits.
An actual f-string diagnostic is conservatively Ambiguous because its embedded
name lacks a complete code-token anchor. Underlying-diagnostic-change tests use
injected unit data and are not claimed as empirical formatter findings.

## Reproduction

Use the existing Python 3.11 environment or follow README installation steps.
From the repository root in PowerShell:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe scripts/validate_phase2.py --output datasets/results/local-validation
.\.venv\Scripts\python.exe scripts/validate_phase2.py --output datasets/results/local-validation-repeat
.\.venv\Scripts\python.exe scripts/verify_phase2.py datasets/results/local-validation datasets/results/local-validation-repeat --report reports/local-validation-checks.json
```

Choose new directory names for each run; evidence directories are never replaced.
Canonical retained runs are `datasets/results/phase2-validation` and
`datasets/results/phase2-validation-repeat`. Each includes full JSONL, summary CSV,
per-trial evidence and an expected-versus-observed `control_validation.json`.
The final JUnit result and console output are in `reports/phase2`.

## Issues, limitations and next gate

There are no known failing tests or blocking execution errors. The initial
Phase 2 suite passed sixty tests. Two unused test imports found by Ruff were
removed; additional failure/scope/Unicode checks brought the final suite to
seventy-six passing tests. No failed empirical trials are hidden behind this count.

Labels are independent of the detector logic, not independently adjudicated by a
human or second linter. Controls are a development set selected using discovery
results; no precision, recall or F1 is reported. AST preservation does not prove
universal runtime equivalence. See `limitations.md` for the conservative support
boundary and remaining validity threats.

Historical Phase 1 evidence and its provisional labels were not modified. Source
provenance, outcome definitions and scripts are persisted for the next session.
Phase 3 should preregister generation specifications, build and validate the main
controlled dataset, and execute paired formatter comparisons. It requires a new
explicit user instruction. No main generator, statistical analysis, full research
report, real-world study, or explorer was implemented in this phase.
