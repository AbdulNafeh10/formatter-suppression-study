# Phase 2 prospective oracle protocol

Established 2026-11-03 UTC before Phase 2 control probing or classifier execution.
This phase validates an oracle; it does not launch the controlled dataset study.
Pinned tools and the four-pass settings remain those of Phase 1.

## Correspondence policy

Require strict AST equality before attribution. For the selected rules only,
associate each underlying diagnostic span with a unique relevant AST construct:
F821 with a load Name, F841 with a store Name, F401 with an import alias.
Use the AST field/index path, rule, coordinate-free node dump and normalized
token context as identity across formatting. Coordinates locate constructs within
each source, never identify a diagnostic across sources. Convert AST UTF-8 byte
columns to Python string columns; verify Ruff's installed coordinate convention
using actual Unicode inputs. Preserve anchor evidence and both raw diagnostics.

Reject unsupported rules, invalid/out-of-bounds spans, non-unique anchors,
duplicate diagnostic identities and mismatched context as Ambiguous. Never match
by message alone, diagnostic order, aggregate counts, or nearest line. Repeated
names are distinguishable only through their verified structural paths. A name
or alias span must contain the diagnostic; details will be tightened to the
installed tool's observed ranges, with any changes documented.

Verify visible diagnostics are a multiset subset of underlying diagnostics on
each identical source. Only after complete unique anchoring compare underlying
identity sets. Unequal underlying sets are Diagnostic changed, with unmatched
records retained. If anchor construction is uncertain, prefer Ambiguous over a
claim about underlying changes. A complete equal set permits comparing each
identity's visible/suppressed state. Changes to diagnostic messages for an
otherwise equal anchor are conservatively Diagnostic changed, not drift.

## Outcome precedence and records

Tool/parse failures: Execution failure or invalid_source/Ambiguous as in Phase 1.
Valid unequal ASTs: AST changed. Unreliable correspondence: Ambiguous.
Verified unequal underlying diagnostics: Diagnostic changed. Otherwise compare
coverage: Preserved, Newly hidden, Newly exposed, or Mixed. Drift counts remain
null when attribution is blocked; stable empty diagnostic sets count as Preserved.
Unchanged text remains separately flagged. Do not modify Phase 1 evidence.

## Independent validation policy

Before using classifier predictions as validation, probe a small saved, explicitly
AI-assisted set of hand-written examples with real pinned tools, recording every
candidate (including failures and negative results). This is targeted feasibility
probing, not the Phase 3 dataset. If a formatter-induced change is found, preserve
the actual formatter output and all four raw Ruff passes. Establish expected
labels separately by reviewing exact name/alias occurrences, raw A/B/C/D results,
and a comment-only intervention with noqa comments neutralized using tokenize.
The intervention must preserve all non-comment tokens and the AST, then ordinary
linting must reproduce the ignore-noqa results. This intervention supports
attribution to directive effects rather than diagnostic movement.

Freeze a versioned control manifest before executing the classifier on controls.
Labels must not come from matcher/classifier output. Authored before/after pairs
may test hidden/exposed/mixed branches but must be labeled manual directive
interventions, never formatter-produced positive controls. If probing finds no
formatter positive, document that gap rather than manufacture one. Independently
verified refers to a separate procedure, not a separate human reviewer; human
review remains outstanding. No detector precision/recall or empirical prevalence
will be claimed from this small development validation set.

## Required validation scope

Test real formatter integrations, repeated diagnostics, rule-specific anchors,
Unicode, same-count identity swaps, empty inputs, underlying changes, invalid
source, ambiguous/unsupported spans, duplicate identities, malformed JSON,
subprocess failure/timeout, evidence export and deterministic repeat execution.
Unit-test injected diagnostics exercise error branches, not empirical findings.
Stop after this validation; dataset generation and main experiments need Phase 3.
