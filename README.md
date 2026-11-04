# Code Formatting and Linter Suppressions

Can formatting Python code change which lint warnings are suppressed, even when
its executable syntax stays the same? I compared Black and Ruff formatting using
Ruff's diagnostics before and after each transformation. This is an independent
research pilot with a controlled test suite and a separate sample of public
repository files.

## Method

For each comparison, I ran Ruff on the original and formatted source, with `noqa`
comments respected and ignored. These four checks separate a change in underlying
warnings from a change in which warnings are visible. An abstract syntax tree
(AST) comparison checks parsed program structure. A matcher then uses rule, AST occurrence and token
context to establish warning identity rather than relying on line numbers.

The controlled suite contains 25 templates crossed with 8 directive modes:
200 inputs tested with each formatter. The natural sample contains 40 files
from pinned historical versions of Requests, Flask and pytest. Only F401, F821
and F841 were selected. The tools were Black 25.1.0, Ruff 0.11.13 and Python 3.11.9.
There were 400 controlled comparisons in total. Analyzed programs were
never executed, and lint fixes were disabled.

## Results

Black produced 68 confirmed suppression changes in 200 controlled comparisons
(34.0%); Ruff produced 35 (17.5%). Both hiding and exposure occurred. These
proportions describe deliberately constructed examples, not Python-wide frequency.

The original matcher marked 16 comparisons per formatter as Ambiguous. A separate
AI-assisted review proposed Preserved for all 32, giving reviewed Preserved
counts of 132 for Black and 165 for Ruff. The original labels remain intact.
The review is not independently human-validated ground truth.

![Original automatic classifications and supplementary reviewed counts](reports/figures-reviewed/figure1_reviewed_outcomes.png)

Each bar contains 200 comparisons. Reviewed bars depend on the supplementary
proposals; confirmed-change counts are unchanged.

No confirmed drift appeared in 80 natural-source comparisons. However, 65 outputs
were unchanged by formatting, and 22 of the 40 original files had no underlying
warnings from the selected rules. There were also 4 strict AST exclusions. The
zero result does not establish that either formatter is safe on other code.

## Limitations

Template variants are related, the repositories were chosen for feasibility,
and only the pinned Windows environment was tested. AST equality does not prove
runtime equivalence. Statistical intervals are exploratory cluster-model checks,
not ecosystem estimates. Independent detector accuracy remains unmeasured.

AI tools assisted implementation, debugging, controlled input generation, analysis
scripts and writing. Measurements came from executed tools, and inputs were
checked programmatically. The [AI-use note](docs/ai_use.md) explains the scope.

## Running the Experiments

From the repository root in PowerShell:

Git must be available on PATH. Use a committed Git checkout for provenance.

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-analysis-lock.txt
.\.venv\Scripts\python.exe -m pip install --no-deps --no-build-isolation -e .
.\.venv\Scripts\python.exe -m pytest -q
```

Use the [reproduction instructions](docs/reproducibility.md) for fresh experiment,
analysis and reviewed-result outputs. Existing evidence directories cannot be
overwritten. Dependencies require network access on first installation. All primary comparisons were also repeated in a freshly installed pinned
environment on the same Windows host. A clean-machine installation and other
platforms remain untested.

## Project Files

Start with the [public report](report/research_report_public.md) or its
[PDF](report/research_report_public.pdf). The [evidence guide](docs/evidence_guide.md)
links source snapshots and diagnostics. [Original metrics](reports/phase5/analysis/metrics.json),
[reviewed metrics](reports/publication-phase-a/analysis/metrics.json) and the
[ambiguity audit](reports/ambiguous-audit/ambiguous_comparisons_review.md) remain separate.

This is a privacy-derived public snapshot with fresh history. Source bytes and
scientific findings are preserved; execution metadata is anonymized. Full upstream
archives and unrelated assets are excluded. See the [snapshot notes](docs/public_snapshot.md),
[third-party notices](THIRD_PARTY_NOTICES.md) and [release status](docs/release_review.md).
MIT is approved for author-owned material, pending the exact copyright-holder line.
No publication has been performed.
