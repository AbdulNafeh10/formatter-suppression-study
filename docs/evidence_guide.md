# Inspecting the evidence

Start with the [report](../report/research_report.md), [methodology](methodology.md)
and [limitations](limitations.md). The study remains fully usable without a UI.
No optional explorer was added in Phase 7: source snapshots, JSON/CSV exports and
the examples below provide direct access without another application dependency.

## Find a comparison

`datasets/results/phase3/results.jsonl` contains the controlled primary records;
`datasets/results/phase4/results.jsonl` contains the natural primary records.
Native configuration sensitivity has its own `native_results.jsonl`. CSV files
are convenient indexes; nested fields are JSON-encoded and raw evidence is the
authority. Reproduction outputs are separate measurements, not additional
independent research observations.

From the repository root in PowerShell, list controlled changes:

```powershell
Get-Content datasets/results/phase3/results.jsonl |
    ForEach-Object { $_ | ConvertFrom-Json } |
    Where-Object { $_.classification -in @('Newly hidden', 'Newly exposed', 'Mixed') } |
    Select-Object case_id, formatter, classification, newly_hidden_count, newly_exposed_count
```

To inspect a trial, use its case_id and formatter under the dataset's `trials`
directory. Recorded `evidence_path` values reflect the original machine and are
not portable path identifiers; relative repository paths below are portable.

| Example | Primary evidence directory |
|---|---|
| Controlled newly hidden | [generator expression / Black](../datasets/results/phase3/trials/generator_expression--blanket_first/black/result.json) |
| Controlled newly exposed | [long list / Black](../datasets/results/phase3/trials/list_long--blanket_first/black/result.json) |
| Controlled preserved | [no-directive semicolon function / Black](../datasets/results/phase3/trials/semicolon_function--none/black/result.json) |
| Controlled ambiguity | [exception binding / Black](../datasets/results/phase3/trials/exception_binding_boundary--specific_first/black/result.json) |
| Natural AST exclusion | [Flask app / Black](../datasets/results/phase4/trials/pallets--flask--d3e0349504081bb5/black/result.json) |

These examples illustrate retained labels, not a representative sample or a
separate accuracy evaluation. Match case IDs against the manifests to recover
the controlled family or natural repository path and immutable source URL.

## Read a trial in this order

1. Compare `before.py` and `after.py`; treat source files as data, not programs to run.
2. Read `result.json` for status, AST gate, selected rules and classification.
3. Inspect A/C visible passes and B/D underlying passes. Each has raw stdout,
   parsed diagnostics and a command record containing return code and stderr.
4. Inspect `matching.json` for diagnostic identity, anchors and visibility transitions.
   An absent or partial match may be an explicit limitation rather than preservation.
5. Check formatter command evidence, source hashes and both AST dumps. Line shifts
   alone do not establish warning identity or changed suppression.

Mixed, Diagnostic changed, AST changed, Ambiguous and Execution failure are
distinct states. Do not merge exclusions or unknown correspondence into Preserved.
For natural TypeIgnore exclusions, read the separate Phase 4 investigation and
retain the primary classifications. Missing native configuration is a status,
not an executed native comparison.

## Aggregate evidence and verification

- [Machine-readable metrics](../reports/phase5/analysis/metrics.json) and companion
  CSVs distinguish scheduled, resolved and paired denominators.
- [Figure captions](../reports/phase5/analysis/figure_captions.json) state units,
  uncertainty models and scope. Original PNG/SVG figures are in `reports/figures`.
- [Report claim audit](../reports/phase6/claim_audit.json) binds report values to
  source fields; [manual claim review](../reports/phase6/manual_claim_review.md)
  covers interpretation and protocol constants.
- [Reproduction instructions](reproducibility.md) keep old evidence immutable and
  describe exclusions, version pins, environment limits and fresh output paths.

The final Phase 7 handoff records actual test and reproduction outcomes. Automated
consistency and repeatability checks do not establish independent detector accuracy.
