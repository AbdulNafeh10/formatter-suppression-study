# Phase 5 analysis specification — exploratory

Established 2026-11-03 UTC after Phase 3/4 outcome counts were already known,
before executing new Phase 5 statistics or figures. Earlier protocols fixed
outcome definitions, input selection, paired measurements and dataset separation.
They did not fix all statistical details below before measurement. Accordingly,
this phase is descriptive/exploratory, not a confirmatory preregistered test.
Do not change classification or exclusion rules, normalize away AST exclusions,
collect extra examples, or select a favorable interval after inspecting results.

## Integrity gate and analysis units

Recheck raw source/diagnostic/CSV/JSONL evidence using existing verifiers, writing
new reports under reports/phase5 (never replacing prior reports). Additionally
audit counts, visible-subset invariants, matched-occurrence visibility/transitions,
classification arithmetic, paired input checksums, tool/configuration provenance,
and record coverage. These are integrity checks, not independent detector labels.

Primary data: 400 Phase 3 controlled records and 80 Phase 4 standardized records.
Keep them separate. Development probes/controls and repeat runs are excluded
from primary denominators. Keep the 66 actual project-config comparisons separate
from primary conditions and from fourteen missing-config status records.

Report all eight outcomes, scheduled/measurement-complete/attributable counts,
text changed/unchanged, original warning/suppression relevance, affected diagnostic
transition counts, and outcome proportions. All-scheduled proportions include
unresolved outcomes explicitly; conditional resolved proportions have their own
denominator. Do not convert null drift counts into confirmed zero outcomes.

## Paired and structural analysis

Pair formatters by dataset and case ID, verifying identical input checksums.
Build a 2x2 table only on pairs where BOTH outcomes are attributable (Preserved,
Newly hidden, Newly exposed, Mixed). Record jointly/singly unresolved pairs.
Compute Black-minus-Ruff differences in any-drift proportion and in hidden/exposed
event proportions on those SAME pairs. Keep direction-specific warning counts
separate; neither fewer total changes nor fewer hidden warnings implies superiority.

Controlled structural summaries: syntax category, template family, directive
treatment/placement and suppression type. These are exact descriptions of a fixed
factorial suite, not independent observations or an ecosystem prevalence sample.
No multiple-testing claims or p-values; do not use an unclustered McNemar test.

## Uncertainty and confidence intervals

1. **Finite-corpus identification bounds:** for each formatter, the lower bound
   is confirmed drift / scheduled and the upper bound assigns every unresolved
   outcome to drift. Also bound the paired all-scheduled contrast by assigning
   each formatter's unresolved binary outcome conservatively. Bounds describe
   unadjudicated outcomes, not probabilities or confidence coverage.
2. **Controlled cluster-bootstrap model intervals:** use only common-resolved
   pairs. Resample entire template families with replacement, retaining every
   directive treatment and formatter pairing within each sampled family. Use
   20,000 replicates, seed 20261103, NumPy PCG64, 2.5/97.5 percentile endpoints
   with linear quantile interpolation. Calculate both formatter rates and their
   paired difference using ratios of summed counts/denominators. Save all draws.
   Repeat the same calculation with syntax categories as larger clusters,
   seed 20261104, as a predeclared cross-family dependence sensitivity. Report
   both schemes, not whichever is narrower or excludes zero.
3. **Wilson 95% model sensitivity:** calculate family-level ANY confirmed drift
   across the eight treatments only for wholly resolved families (separately
   by formatter). The binomial unit is the family, never each source or each
   formatter trial. Label these as conditional independent/exchangeable-family
   model intervals. Fixed, related templates were not sampled randomly, so the
   model's coverage is unverified; this is not an ecosystem confidence claim.
4. **Natural-source data:** report each repository separately. Do not calculate
   pooled binomial Wilson intervals, an IID file bootstrap, or bootstrap three
   repositories into an apparently precise confidence interval. For the finite
   eligible archive population N, show assumption-free bounds
   [confirmed/N, (confirmed + sampled-unresolved + unsampled)/N]. The two censuses
   still retain unresolved-measurement uncertainty. The pytest sample is not a
   census. No stochastic confidence interpretation is attached to these bounds.

The cluster model assumes the chosen cluster units are exchangeable and mutually
independent. It preserves known within-cluster dependence but cannot establish
that assumption for hand-authored related templates. Category sensitivity exposes
one coarser grouping; neither interval justifies generalization. Natural and
controlled corpora have different selection frames and must never share a rate.

## Figures and artifacts

Generate standalone PNG (300 dpi) and SVG with embedded/editable vector text,
consistent accessible colors, labeled counts/denominators and factual captions:

1. Outcome distribution: controlled and per-repository natural conditions kept
   in separate panels; uncertainty/exclusions are visible, zero outcomes documented.
2. Paired controlled comparison: family-level paired pattern, common-resolved
   2x2 counts, and family/category cluster model intervals with explicit caveats.
3. Structural patterns: matched category/treatment heatmaps for both formatters,
   with counts and unresolved cells distinct from zeros. Small cells get no
   unsupported confidence intervals.
4. If useful, original natural-file diagnostic relevance (unique files, not two
   formatter copies), to contextualize the negative natural finding.

Export aggregate metrics, per-trial normalized analysis rows, pairing tables,
group tables, interval draws, integrity/provenance manifests and a concise Phase 5
findings document. Render and visually inspect every figure, then check artifact
and numerical reproduction in fresh output directories.

## Scope and methods sources

Wilson formula: [NIST confidence-interval guidance](https://www.itl.nist.gov/div898/handbook/prc/section2/prc241.htm).
Cluster-level resampling principle: [Stata bootstrap reference manual](https://www.stata.com/manuals/rbootstrap.pdf).
Deterministic resampling API: [NumPy 2.2 Generator.choice documentation](https://numpy.org/doc/2.2/reference/random/generated/numpy.random.Generator.choice.html).
These sources support methods/API details, not the empirical findings. This is
not the complete Phase 6 literature review.

No detector precision/recall/F1: there is no independent held-out ground truth
for the main datasets. No full research report, explorer, new corpus or Phase 6
work is part of this phase. Stop after Phase 5 and await explicit authorization.
