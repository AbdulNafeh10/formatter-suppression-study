# Phase 3 — Controlled experiments

Completed 2026-11-03 UTC. This is a **controlled pilot**, with real-world
repository validation still pending. Phase 4 has not been started.

## Design and implementation

The prospective protocol, exact configurations, generator, experiment runner,
tests, source specification and all 200 inputs were frozen at commit `dbefde5`
before main tool measurement. The main manifest SHA-256 is
`e00a86abf2beb934188e8e255c77722105cac72f4cac4bebc87818920d7de4b8`.

The design crosses 25 structural templates with eight directive treatments,
yielding 200 byte-distinct, valid UTF-8 sources with 25 distinct AST structures.
The treatments deliberately share executable syntax within each template;
**200 sources are not 200 independent code structures**. They cover thirteen
syntax-category labels and the rule-specific, multicode, blanket, standalone,
file-specific and absent-directive conditions described in `phase3_protocol.md`.

AI assisted authoring the saved templates and methodology. The generator makes
no model calls: deterministic Python renders, parses, compiles and checks them.
Seed 20261103 determines a SHA-256-ranked execution order, not random code
generation or population sampling. No input was replaced after observing outcomes.

Added `generator.py`, `experiment.py`, executable TOML configurations and CLI
generate/experiment commands. The Phase 2 matching and classification modules
were unchanged. Pipeline changes add source-generation metadata and an explicit
experiment-start environment snapshot to avoid repeatedly scanning accumulated
evidence with Git. No numerical-analysis dependencies were added.

## Executed validation

- All **85 tests passed**, including the frozen Phase 2 independent controls and
  new generation, duplicate/invalid-candidate retention, tamper detection,
  metadata safety, real paired-run, exclusion and export tests.
- All **200 candidates passed syntax/compilation and byte-uniqueness checks**.
  Original-source Ruff preflight found selected underlying diagnostics in every
  candidate. No candidates or planned comparisons were excluded.
- Ran **400 main comparisons**: the same 200 sources with Black 25.1.0 and
  Ruff 0.11.13, using the unchanged four-pass lint settings and Python 3.11.9.
- Repeated the prospectively selected one-treatment-per-template sample:
  **25 sources / 50 comparisons**, covering every template and all treatments.
- Independently regenerated every source and manifest byte-for-byte, checked
  all CSV fields against full JSONL/individual records, verified raw diagnostics,
  source/output hashes and matching evidence, and compared repeat measurements.
- Neutralized directives in comment tokens for four prospectively selected
  representative drift comparisons. All eight before/after interventions kept
  the code tokens/AST and reproduced the corresponding ignore-noqa diagnostics
  under ordinary Ruff linting. These are selected-case attribution checks,
  not independent labels for all 400 outputs or detector-accuracy measurements.

The implementation lint checks also passed. Existing phase evidence was retained.

## Preliminary main results

The table describes the **main run only**. Repetitions, unit tests, Phase 2
controls and discovery probes are not additional observations in these counts.
Each formatter column has a denominator of **200 scheduled/executed comparisons**.

| Outcome | Black | Ruff format |
|---|---:|---:|
| Preserved | 116 | 149 |
| Newly hidden | 50 | 14 |
| Newly exposed | 18 | 21 |
| Mixed | 0 | 0 |
| Diagnostic changed | 0 | 0 |
| AST changed | 0 | 0 |
| Ambiguous | 16 | 16 |
| Execution failure | 0 | 0 |
| **Total** | **200** | **200** |

Underlying correspondence was established for **184 comparisons per formatter**;
the remaining sixteen per formatter were ambiguous. Thus 368 of 400 comparisons
have attributable suppression classifications. All 400 completed the four passes
and preserved the strict AST. An AST-equal measurement is not automatically a
reliable suppression comparison.

The oracle classified **68 Black comparisons** and **35 Ruff comparisons** as
suppression changes: 103 formatter/input comparisons in total. A source tested
by two formatters contributes two comparisons, not two independent inputs.
Every changed comparison affected one matched diagnostic: Black had 50 newly
hidden and 18 newly exposed transitions; Ruff had fourteen and twenty-one.
These are diagnostic transitions per comparison, not counts of unique natural
warnings or warnings across public repositories.

| Text-change bookkeeping | Black | Ruff format |
|---|---:|---:|
| Formatted text changed | 133 | 118 |
| Formatted text unchanged | 67 | 82 |
| Text changed and suppression Preserved | 57 | 75 |

Unchanged outputs remain in the main denominator and are explicitly marked.
Among changed outputs, some comparisons remain Ambiguous; they must not be
silently treated as suppression-preserved transformations.

All thirty-two ambiguous comparisons arise from the two predeclared support
boundaries: f-string inner names and exception-handler bindings, eight treatments
of each per formatter. The oracle does not invent token/Name anchors for them.
No unexpected ambiguity family, AST failure or underlying-diagnostic change was
observed in this suite. This is not evidence that such outcomes cannot occur.

Results support the narrower observation that the pinned formatters can change
effective noqa coverage on controlled AST-preserved examples under these lint
settings. The raw results and selected interventions support both newly hidden
and newly exposed cases. The intentionally constructed, correlated stress suite
does not estimate natural prevalence, establish general formatter superiority,
or evaluate detector error rates. Statistical analysis and uncertainty treatment
are deferred to Phase 5; no intervals, significance tests or figures were created.

## Repeatability and representative checks

All fifty preselected repeat comparisons agreed with the corresponding main
measurements on source/output hashes, AST/text-change flags, raw diagnostic
content, structural identities, coverage transitions, underlying-change records
and classifications. Temporary diagnostic filenames were the only diagnostic
fields disregarded. All 200 regenerated input sources and both manifest and
specification files were identical to the frozen versions.

The prospectively defined representatives were:

| Formatter | Oracle outcome | Case |
|---|---|---|
| Black | Newly exposed | binary_long--blanket_first |
| Black | Newly hidden | binary_short--blanket_first |
| Ruff | Newly exposed | binary_long--blanket_first |
| Ruff | Newly hidden | binary_short--blanket_last |

All four comment-only intervention checks passed. No Mixed result was observed,
so no Mixed representative was available. The Phase 2 manual Mixed control
remains a software-validation case, not a main-experiment observation.

## Evidence and reproduction

- Sources, full generation specifications and manifest:
  `datasets/controlled/phase3/`.
- Main complete JSONL, CSV, preflight evidence, all trial source pairs/raw passes,
  matching records and preliminary counts: `datasets/results/phase3/`.
- Repeat measurements: `datasets/results/phase3-repeat/`.
- Selected interventions: `datasets/results/phase3-interventions/`.
- Test output/JUnit, execution logs and derived verification summary:
  `reports/phase3/`.

Read `docs/reproducibility.md` for full commands. Existing evidence is never
overwritten. With fresh paths in copied configs, run generate, experiment, and
the repeat experiment. `scripts/verify_phase3.py` regenerates sources in a temporary
directory and checks retained main/repeat records. The individual format command
can reproduce any candidate with the saved formatter and a new evidence path.

## Issues and handoff

No failing tests, tool failures, invalid generated inputs or preflight exclusions
remain in the executed main experiment. Oracle scope limitations remain explicit:
sixteen comparisons per formatter are inconclusive, and all new main labels are
oracle outputs rather than independently adjudicated ground truth. The repeat
sample covers every template but is not a rerun of all 400 comparisons. Full
source regeneration covers all 200 inputs.

The study is limited to the pinned standardized settings, synthetic templates
and Windows/Python environment. Shared templates and paired formatter trials are
dependent. The selection was informed by Phase 2 discovery, not blinded or held
out. Human review, natural repository evidence and inferential analysis remain
outstanding. See `limitations.md`.

Phase 4 should specify public-repository selection and sampling, then perform
separate real-world validation. It requires an explicit new user instruction.
