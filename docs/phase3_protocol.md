# Phase 3 prospective controlled-experiment protocol

Established 2026-11-03 UTC before Phase 3 generation or tool measurements.
Phases 1–2 informed the stress-test design. This is not a held-out detector
evaluation and is not a sample of natural code. Do not change generation or
classification rules after seeing results without a dated exploratory amendment.

## Fixed factorial design

Generate **25 structural templates × 8 directive treatments = 200 candidates**.
The 25 templates cover positional/keyword/nested calls; short/long lists;
plain/starred tuples; dictionaries with pairs/unpacking; short/long binary and
boolean expressions; conditional expressions; list/dict comprehensions;
generator expressions; function defaults and local assignments; multi-import
and from-import; module/function semicolons; nested containers; f-strings; and
exception bindings. The last two deliberately exercise known oracle boundaries.

Each template has two distinct physical directive sites, marked first and last.
Some templates have more than two underlying warning occurrences. Treatments:
no directive; standalone specific noqa immediately above the first site;
first-site specific noqa; first-site blanket noqa; first-site multiple selected
codes; last-site specific noqa; last-site blanket noqa; file-level specific
`# ruff: noqa: CODE`. Multicode uses F401,F821,F841. The primary template rule is
F821, F401 or F841 as appropriate. File-level directives are a documented extra
scope control. Indentation is retained for standalone comments.

These are 200 distinct sources, **not 200 independent code structures**. Within
each template, executable ASTs are intentionally identical so that suppression
treatment is the manipulated factor. Do not inflate the design by renaming
identifiers or changing seeds to create more observations. Templates contain
actual syntax/construct differences and potential diagnostics, not just whitespace
variants. Save the complete template specification and every candidate source.

Seed **20261103** determines a stable SHA-256-ranked execution order. Source
generation is deterministic and does not use random sampling. Reproduction uses
the same specification/seed. No AI model is called by the generator: AI assists
in authoring the saved templates and this protocol; deterministic Python renders
and validates the candidates.

## Validation and retention

Before measurement, compile and parse every source without executing it. Reject
exact byte duplicates and invalid sources, retaining each candidate and reason.
Record structural fingerprints to disclose template dependence; AST duplicates
across directive treatments are intentional and are not byte duplicates.
Run original-source Ruff with ignore-noqa once per candidate to verify selected
diagnostic relevance before main formatter comparisons; save raw outputs and
include all preflight failures/exclusions. Require at least one underlying selected
diagnostic for eligibility. No outcome-based replacement or resampling is allowed.

Use the frozen Phase 2 oracle and unchanged exact tool/configuration pins. Run
every eligible source through both Black and Ruff, with four real lint passes per
comparison. Preserve failures, invalid/AST-changed outputs, ambiguity, underlying
diagnostic changes and unchanged text. Formatter compatibility and output AST
preservation are checked per comparison, not assumed from input validity. Never
drop ambiguous boundary cases to improve rates. Keep prior-phase evidence intact.

## Execution and reproduction

Freeze protocol, generator, configuration and source manifest in Git before the
main experiment. Run the existing independently labeled Phase 2 control tests
before starting. Main runs are sequential, use bounded subprocesses and temporary
working directories, and never execute analyzed programs. Save source/configuration
hashes, run/code commit IDs, generation metadata, all diagnostics, matching evidence,
and complete JSONL plus CSV records. Trial IDs must distinguish dataset runs.

Regenerate all sources independently and verify byte/hash/manifest equality.
Prospectively repeat one treatment per template: treatment index = template index
modulo eight in the saved specification order. This yields **25 cases / 50 paired
formatter comparisons**, covering every template and all treatments. This selection
does not depend on outcomes. Compare hashes, AST status, diagnostics, identities,
coverage transitions and classifications, excluding only documented execution paths
and timestamps. Repetitions are not additional independent observations.

## Preliminary reporting only

Report all planned/eligible/excluded comparisons, each outcome by formatter,
attributed affected-warning counts, changed/unchanged outputs, and ambiguity/AST/
execution failures with denominators. Descriptive proportions apply only to this
fixed synthetic stress suite. Do not pool controlled data with earlier development
controls or real-world data. No Wilson intervals, significance tests, independence
assumptions, superiority claims, held-out detector metrics, figures or prevalence
inferences are part of Phase 3; statistical analysis belongs to Phase 5.

Independently intervene on a deterministic representative of each observed drift
classification per formatter (lexicographically first case ID): neutralize noqa
only inside comment tokens, require the same code tokens/AST, and verify ordinary
Ruff reproduces the corresponding ignore-noqa diagnostics. Preserve checks and
failures; this supports selected-case attribution, not a detector accuracy estimate.
All other new labels remain oracle outputs, not independent ground truth.

Stop after the controlled experiment and handoff. Public repository sampling is
Phase 4 and requires explicit authorization.
