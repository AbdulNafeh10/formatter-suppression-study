# Supplementary analysis method

The original automatic classifications are the primary record. The new analysis
answers a separate question: what changes if the saved AI-assisted review's 32
Preserved proposals are accepted? It does not provide independent human labels.

`scripts/analyze_reviewed_results.py` verifies the existing audit's hashes and
checks the canonical primary evidence. It requires exact coverage of the ambiguity
cohort and matching source hashes. Missing, duplicate, uncertain or visibility-
changing proposals are rejected. Original rows remain unchanged; a separate deep
copy supplies the reviewed calculations. `review_overlay.csv` retains both labels
and identifies which rows use a proposal. Natural results are not reclassified.

Counts, paired differences and group summaries use all 200 reviewed input pairs.
The existing tested numerical helpers resample whole paired clusters with
replacement. Every treatment and both formatters stay together. The family model
uses 25 clusters, seed 20261103; the category model uses 13, seed 20261104. Each
has 20,000 PCG64 draws with linear 2.5/97.5 percentile endpoints. Draw CSVs are
retained. The Wilson event is any drift among a family's eight treatments, with
25 family units per formatter. Neither model is an IID analysis of 200 inputs
or a population estimate. Review errors are not represented by these intervals.

The original metrics were reproduced before calculating the reviewed versions.
Both sets remain separate in metrics.json, and the original primary metrics file
was not replaced. Revised completion ranges are conditional on all proposals;
they do not supersede the original unresolved-outcome bounds.

The execution used the retained Python 3.11 study environment and exact analysis
pins. No formatter/linter reruns or new figures were needed. Phase A instead
checked saved raw replay/intervention outputs and all 64 reviewed warning
transitions. Both new draw sets and interval summaries were regenerated exactly
from their saved cluster counts. Validation records are in the parent directory.

To reproduce into a fresh directory from the repository root:

```powershell
.\.venv\Scripts\python.exe scripts/analyze_reviewed_results.py --output reports/publication-phase-a/local-reproduction
```

Use another unused path for later executions. Numeric outputs should agree;
the provenance commit can differ after a new local commit. No output directory
is overwritten. Tests in `tests/test_reviewed_analysis.py` check that proposals
cannot silently replace the primary labels or supply missing evidence.
