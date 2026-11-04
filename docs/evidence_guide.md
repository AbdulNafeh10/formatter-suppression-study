# Inspecting the evidence

Start with the [public report](../report/research_report_public.md) for the
argument and [methodology](methodology.md) for diagnostic definitions. The files
below let a reader inspect a comparison without installing an explorer or
executing the analyzed code.

## Locate a comparison

`datasets/results/phase3/results.jsonl` indexes the controlled primary runs;
`datasets/results/phase4/results.jsonl` indexes the natural runs. CSV exports
provide a flat index with nested fields encoded as JSON. Native sensitivity is
separate in `native_results.jsonl`. Repeat runs check the same cases and do not
increase the primary sample.

From the root in PowerShell:

```powershell
Get-Content datasets/results/phase3/results.jsonl |
    ForEach-Object { $_ | ConvertFrom-Json } |
    Where-Object { $_.classification -in @('Newly hidden', 'Newly exposed', 'Mixed') } |
    Select-Object case_id, formatter, classification, newly_hidden_count, newly_exposed_count
```

Use `case_id` and `formatter` under the dataset's `trials` directory. Recorded
`evidence_path` values contain privacy placeholders and are not portable commands.
The relative paths below are usable in this checkout.

| Retained outcome | Example |
|---|---|
| Newly hidden | [Generator expression / Black](../datasets/results/phase3/trials/generator_expression--blanket_first/black/result.json) |
| Newly exposed | [Long list / Black](../datasets/results/phase3/trials/list_long--blanket_first/black/result.json) |
| Preserved | [Semicolon function, no directive / Black](../datasets/results/phase3/trials/semicolon_function--none/black/result.json) |
| Ambiguous | [Exception binding / Black](../datasets/results/phase3/trials/exception_binding_boundary--specific_first/black/result.json) |
| AST changed | [Flask app / Black](../datasets/results/phase4/trials/pallets--flask--d3e0349504081bb5/black/result.json) |

These are illustrations, not a representative subset or independent accuracy
test. Manifests connect case IDs to template families or upstream paths and
immutable source URLs.

## Read the source and four passes together

First compare the original and formatted source, then read `result.json` for
the AST gate and classification. Controlled trials store ordinary `before.py`
and `after.py` files. Natural trials use `before.py.evidence.json` and
`after.py.evidence.json`: lossless containers holding the measured source and
required notices. Their decoded bytes preserve line endings and diagnostic
coordinates. The existing reader validates the stored source checksum:

```python
from suppression_study.evidence import evidence_bytes

source = evidence_bytes(
    "datasets/results/phase4/trials/pallets--flask--d3e0349504081bb5/black/before.py"
)
print(source.decode("utf-8"))
```

Read A/C for visible warnings and B/D for underlying warnings. Each pass retains
parsed diagnostics, raw output and a command record with return code and stderr.
`matching.json` explains identities, anchors and visibility transitions. Check
source hashes, AST dumps and formatter output if the match is unclear. A moved
line or equal warning count cannot establish correspondence.

Ambiguous means the automatic matcher could not settle correspondence. Diagnostic
changed, AST changed and Execution failure have different reasons for withholding
a suppression judgment. None should be read as Preserved. Requests' missing
native configuration entries are statuses, not completed native comparisons.

## Keep the result layers separate

The [original metrics](../reports/phase5/analysis/metrics.json) retain automatic
labels and distinguish scheduled, resolved and paired denominators. The
[ambiguity review](../reports/ambiguous-audit/ambiguous_comparisons_review.md)
provides exact evidence paths and proposed judgments for all 32 unresolved
controlled comparisons. The [reviewed metrics](../reports/publication-phase-a/analysis/metrics.json)
are conditional on those proposals; they do not overwrite the original records.

The [public claim ledger](../reports/publication-phase-b/public_claim_audit.json)
binds numeric observations in the current README and public report to source
fields. The [original report ledger](../reports/phase6/claim_audit.json) belongs
to the frozen historical report. Protocol constants and interpretation require
separate reading; a claim binding is not an accuracy assessment.

For fresh outputs, archive reconstruction and checks, use
[reproducibility](reproducibility.md). The [snapshot notes](public_snapshot.md)
explain which hashes describe original measured bytes and which describe public
privacy derivatives.
