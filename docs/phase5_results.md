# Phase 5 — Statistical analysis and figures

Completed 2026-11-03 UTC. This phase analyzes retained observations; it does not
collect new empirical data or change the oracle. The full research report and
literature audit remain Phase 6 work.

## Analysis status and integrity

The detailed specification, tested code and pinned environment were committed
at **ca6084a** before new statistical calculations. Earlier Phase 3/4 outcome
counts were already known: these analyses are **descriptive and exploratory**,
not a confirmatory analysis preregistered before measurement. The earlier rules
for selection, labels, unresolved outcomes, pairing and dataset separation remain.

Existing verifiers passed again on the controlled and natural archives/source,
diagnostic JSON, CSV/JSONL, source hashes and saved repeats. An additional audit
checked all **400 controlled primary records, 80 natural primary records and
66 completed native-config comparisons** for within-source subset arithmetic,
matching identity/visibility/transition consistency, warning counts and outcome
arithmetic. Paired inputs, frozen manifests, formatter stdout and lint flags/tool
versions were verified. Fourteen missing-native-config status records stayed
separate. This is an integrity audit, not independent detector ground truth.

Only the main primary observations enter primary summaries. The fifty controlled
and six natural repeat comparisons, development controls and discovery probes
are excluded from those denominators. Input files and empirical labels were
unchanged. Analysis uses NumPy 2.2.6, pandas 2.2.3 and matplotlib 3.10.3; the
complete separate environment lock is requirements-analysis-lock.txt. No SciPy
dependency or experimental tool upgrade was needed.

## Controlled primary metrics

Each formatter column below has **200 scheduled comparisons**: 25 templates
crossed with eight directive treatments. The 200 inputs are not independent
structures; the formatter columns are paired on identical source.

| Outcome | Black | Ruff format |
|---|---:|---:|
| Preserved | 116 (58.0%) | 149 (74.5%) |
| Newly hidden | 50 (25.0%) | 14 (7.0%) |
| Newly exposed | 18 (9.0%) | 21 (10.5%) |
| Mixed | 0 | 0 |
| Diagnostic changed | 0 | 0 |
| AST changed | 0 | 0 |
| Ambiguous | 16 (8.0%) | 16 (8.0%) |
| Execution failure | 0 | 0 |

There are **184 attributable comparisons per formatter**. Conditional on that
resolved denominator, any confirmed suppression change is 68/184 = **36.96%**
for Black and 35/184 = **19.02%** for Ruff. On the all-scheduled denominator,
confirmed-change fractions are 68/200 = **34.0%** and 35/200 = **17.5%**. The latter
are observed confirmed fractions, not claims that ambiguous outcomes are negative.

Affected-warning counts are fifty newly hidden and eighteen newly exposed for
Black, fourteen and twenty-one for Ruff. They are transitions per formatter/input
comparison, not unique warnings across a population. Text changed in 133 Black
and 118 Ruff comparisons; 67 and 82 were unchanged. Text changed while suppression
was Preserved in 57 and 75 comparisons respectively. All outcomes, including the
two wholly ambiguous boundary templates, remain in the scheduled denominator.

## Paired formatter comparison

The common-resolved subset contains **184 input pairs**, with no one-sided
uncertainty. Sixteen additional pairs are unresolved for both formatters.

| Black outcome / Ruff outcome | No drift | Drift |
|---|---:|---:|
| No drift | 116 | 0 |
| Drift | 33 | 35 |

The Black-minus-Ruff paired difference in any-drift fraction on those same inputs
is 33/184 = **17.93 percentage points**. Hiding-event difference is
(50−14)/184 = **19.57 points**; exposing-event difference is
(18−21)/184 = **−1.63 points**. Fewer total changes does not mean fewer exposed
warnings: three inputs were Newly hidden under Black but Newly exposed under
Ruff. The other shared-drift pairs are fourteen hidden/hidden and eighteen
exposed/exposed. These are fixed-suite descriptions, not superiority claims.

No unclustered McNemar test, independent-samples comparison or p-value was used.
The exact input pairing table is controlled_pairs.csv.

## Uncertainty: three different questions

### Fixed-corpus unresolved-outcome bounds

Without assigning outcomes to the ambiguous comparisons, possible completion
bounds on all 200 inputs are **34.0–42.0%** for Black and **17.5–25.5%** for Ruff.
The paired all-scheduled difference is bounded by **8.5–24.5 percentage points**.
These are worst-case assignments of unadjudicated binary outcomes, not measured
extra drift, confidence intervals or an excuse to reclassify uncertain records.

### Conditional cluster-bootstrap model intervals

For common-resolved inputs only, resample entire clusters with all their paired
formatter outcomes and treatments retained. Each grouping uses **20,000** draws,
NumPy PCG64, and 2.5/97.5 percentile endpoints with linear interpolation.

| Cluster grouping | Units | Seed | Black−Ruff point difference | Exploratory 95% model interval |
|---|---:|---:|---:|---:|
| Template families | 23 | 20261103 | 17.93 pp | 8.70–28.26 pp |
| Syntax categories | 12 | 20261104 | 17.93 pp | 5.92–32.14 pp |

Both groupings are reported; neither was selected for a favorable endpoint.
The family model's formatter fractions have intervals **25.00–48.37%** (Black)
and **10.87–28.26%** (Ruff). Category-model intervals are **22.02–52.27%** and
**9.13–31.58%**. The saved cluster-count and bootstrap-draw CSVs reproduce them.

These intervals are conditional sensitivity to hypothetical independent,
exchangeable cluster sampling. The templates were hand-authored and related;
that assumption and nominal population coverage are unverified. Coarser category
resampling addresses one additional dependence grouping, not all possible shared
design effects. Neither interval estimates Python ecosystem prevalence or proves
general formatter superiority, and no significance claim is made.

These intervals and the preceding finite bounds answer different questions:
bootstrap varies cluster composition within a conditional model; finite bounds
hold the all-scheduled corpus fixed and vary unresolved outcomes. Their endpoints
need not be nested.

### Wilson family-incidence sensitivity

Wilson 95% intervals use **whole, fully resolved families as units**, never the
200 related sources. The event is at least one confirmed drift among a family's
eight fixed treatments. Two incomplete families are excluded from this conditional
model, not counted as negative.

| Formatter | Families affected / fully resolved | Fraction | Wilson 95% model interval |
|---|---:|---:|---:|
| Black | 15/23 | 65.22% | 44.89–81.19% |
| Ruff | 12/23 | 52.17% | 32.96–70.76% |

These are hypothetical independent/exchangeable-family Bernoulli-model intervals
for a different event than per-comparison drift. They are sensitivity outputs,
not empirical evidence that the families are independent. Marginal interval
overlap/non-overlap is not used as a paired test.

The Wilson formula follows [NIST guidance](https://www.itl.nist.gov/div898/handbook/prc/section2/prc241.htm).
The cluster-level resampling principle is described in the
[Stata bootstrap manual](https://www.stata.com/manuals/rbootstrap.pdf); actual
implementation uses NumPy, not Stata. These sources support methods, not the
study's empirical conclusions or a complete related-work review.

## Structural and suppression patterns

Each treatment has twenty-five scheduled cases and twenty-three attributable
cases per formatter. Confirmed-drift counts on the twenty-three resolved cases:

| Treatment | Black | Ruff |
|---|---:|---:|
| No directive | 0 | 0 |
| Standalone above first site | 0 | 0 |
| First-site specific | 14 | 5 |
| First-site blanket | 14 | 5 |
| First-site multicode | 14 | 5 |
| Last-site specific | 13 | 10 |
| Last-site blanket | 13 | 10 |
| File-specific | 0 | 0 |

This suite exhibits placement/construct dependence, not a universal rule that
standalone or file directives are safe. Comprehension templates have drift under
Black for all five inline treatments but none under Ruff in the tested examples;
the two semicolon templates have drift under both formatters for the three
first-site inline treatments. Many call/function/import templates have no drift.
These small, correlated cells receive no inferential per-cell intervals/tests.
Detailed category, family, treatment and suppression-type tables are exported.

## Natural-source results and finite-frame uncertainty

Natural observations remain per repository. No natural-source binomial Wilson
interval, IID file bootstrap or pooled three-repository confidence interval is
reported: files are related within repositories and the repositories form a
small convenience sample.

| Repository / formatter | Scheduled | Attributable | Confirmed drift | Strict AST excluded |
|---|---:|---:|---:|---:|
| Requests / Black | 7 | 7 | 0 | 0 |
| Requests / Ruff | 7 | 7 | 0 | 0 |
| Flask / Black | 13 | 12 | 0 | 1 |
| Flask / Ruff | 13 | 13 | 0 | 0 |
| pytest / Black | 20 | 18 | 0 | 2 |
| pytest / Ruff | 20 | 19 | 0 | 1 |

The natural paired subsets have seven, twelve and eighteen common-resolved input
pairs respectively. There are two one-sided unresolved pairs and one jointly
unresolved pair across these separate frames. Every retained AST exclusion remains
excluded: Phase 4's TypeIgnore.lineno explanation is not an analysis relabeling.

For the finite **eligible archive** frame only, retain unobserved/uncertain files
as unknown. Lower = confirmed/N; upper =
(confirmed + sampled-unresolved + unsampled)/N. These are completion bounds,
not stochastic confidence intervals or bounds on all repository Python files.

| Repository / formatter | Eligible N | Sampled | Sampled unresolved | Unsampled | Finite-frame bounds |
|---|---:|---:|---:|---:|---:|
| Requests / Black | 7 | 7 | 0 | 0 | 0–0% |
| Requests / Ruff | 7 | 7 | 0 | 0 | 0–0% |
| Flask / Black | 13 | 13 | 1 | 0 | 0–7.69% |
| Flask / Ruff | 13 | 13 | 0 | 0 | 0–0% |
| pytest / Black | 28 | 20 | 2 | 8 | 0–35.71% |
| pytest / Ruff | 28 | 20 | 1 | 8 | 0–32.14% |

Zero-width bounds for completed censuses describe only their pinned, filtered,
measured frame. They do not establish future or ecosystem-wide safety. A sample
zero for pytest does not adjudicate the eight unsampled eligible files.

Only fifteen of eighty natural formatter/file comparisons changed text; eleven
of those were attributable and seven began with selected-rule suppression.
Twenty-two of forty original files have no selected underlying warnings, so
forty-four paired formatter observations have empty diagnostic sets. Sixty-five
outputs were unchanged. These constraints limit the negative result's opportunity
to reveal the controlled mechanisms. They are shown rather than filtered away.

Native-config sensitivity remains separate: sixty-six completed comparisons,
sixty-six matching primary classifications, and forty-two with empty selected
diagnostic sets. Fourteen Requests records indicate missing Ruff config. These
are not sixty-six new independent files and not complete project-CI results.

## Figures, artifacts and reproduction

All figures use actual retained observations, consistent colors, explicit
denominators and explanatory captions. PNG files are 300 dpi; SVGs retain
editable vector text. All four were visually inspected for legibility, clipping,
labels and legends.

1. **[figure1_outcomes](../reports/figures/figure1_outcomes.png)**
   ([SVG](../reports/figures/figure1_outcomes.svg)): controlled and per-repository natural outcome distribution,
   including ambiguity and strict AST exclusions.
2. **[figure2_paired_comparison](../reports/figures/figure2_paired_comparison.png)**
   ([SVG](../reports/figures/figure2_paired_comparison.svg)): template profiles, the paired 2x2 table and both
   conditional cluster-model intervals.
3. **[figure3_structural_patterns](../reports/figures/figure3_structural_patterns.png)**
   ([SVG](../reports/figures/figure3_structural_patterns.svg)): matched category/treatment count heatmaps;
   unresolved cells remain distinct from zero.
4. **[figure4_natural_relevance](../reports/figures/figure4_natural_relevance.png)**
   ([SVG](../reports/figures/figure4_natural_relevance.svg)): mutually exclusive original-file diagnostic
   relevance groups, counting each natural file once.

Canonical figures are in `reports/figures`. Data, metric JSON, nineteen derived
artifacts (tables, normalized observations, pairs, both 20,000-draw files and
captions), integrity results and provenance are in `reports/phase5/analysis`.
The provenance input digests identify every primary source/result file used.
Bootstrap seeds in metrics.json and the saved draw files are authoritative;
environment.seed=0 is the inherited tool-environment placeholder, not a bootstrap
seed. It is not used by the statistical functions.

A complete fresh analysis run under `reports/phase5/reproduction` reproduced
all nineteen derived artifacts and all eight PNG/SVG files **byte-for-byte**.
PNG integrity/dimensions and SVG editable text were verified. No source programs
or formatter experiments were rerun for this analysis reproduction.

**123 tests passed**, including twenty new numerical/integrity tests. The first
new test run passed nineteen and failed one because an older Phase 2 fixture
lacked a case_id; the fixture was corrected without changing empirical inputs,
classifications or analysis criteria. Wilson reference/boundary values,
whole-cluster resampling, pair preservation, weighted denominators, missing-value
handling, conservative bounds and tampered arithmetic are covered. Implementation
lint checks passed. Retained source/label evidence remains unchanged.

See `reproducibility.md` for full commands and fresh-path verification. The full
research report, complete literature audit and final polish remain unfinished.
Phase 6 requires explicit authorization. No detector precision, recall, F1,
novelty claim, general superiority claim or publication-readiness claim is made.
