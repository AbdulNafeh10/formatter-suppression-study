# Methodology through Phase 6

## Current consolidated method (2026-11-03)

This is a two-dataset empirical pilot: a controlled stress corpus and a separate
historical convenience sample. The source-formatter comparison is the measurement
unit; formatter contrasts are paired by original source. Template treatments and
files within projects are dependent. No ecosystem sampling frame or independent
detector-accuracy benchmark is claimed.

CPython 3.11.9, Black 25.1.0 and Ruff 0.11.13 are fixed historical baselines on
Windows. Formatting uses line length 88, target py311 and no preview. Ruff checks
F401/F821/F841 without fixes. Primary settings isolate user/project configuration.
Four passes observe original/formatted source with directives respected/ignored.
Within-snapshot subset checks use exact diagnostic identity; cross-snapshot
matching uses unique rule/AST-occurrence/token correspondence. Visibility changes
require stable underlying diagnostics and an accepted AST gate. Unsupported
anchors, changed diagnostics, AST changes and failures remain separate outcomes.

The 25-template by eight-directive controlled design produces 200 original sources
and 400 formatter comparisons. Natural selection uses three pinned archives,
genuine noqa comments, UTF-8, Python 3.11 parsing, a 200 KiB cap and documented
vendored/generated exclusions. Seeded hash ranking selects up to twenty eligible
files per project without outcomes. Forty natural inputs yield eighty primary
comparisons. Native configuration sensitivity is separate from the artificial-
filename standardized primary; neither recreates full project CI.

Raw source, AST dumps, diagnostic arrays, commands, stdout/stderr, environment and
hashes are retained. The strict AST representation includes type-ignore line
fields; secondary normalization does not replace primary labels. Repeats and
representative directive interventions check narrower claims than independent
oracle accuracy. Analyzed programs are never executed.

Detailed statistical choices were fixed after earlier counts were known and are
exploratory. Descriptive proportions, paired contrasts, unresolved-outcome bounds
and conditional cluster-model sensitivity have distinct estimands. There is no
IID per-variant inference or pooled natural-source confidence interval. See the
[report](../report/research_report.md), [AI disclosure](ai_use.md) and
[limitations](limitations.md) for interpretive scope.

## Protocol chronology (retained below)

The following Phase 1 text and dated amendments are historical records. Their
authorization statements describe those stages, not current permissions. The
Phase 2 oracle, Phase 3 controlled protocol, Phase 4 natural protocol and Phase 5
exploratory analysis specification govern their respective retained artifacts.

### Methodology, version 0.1 - Phase 1 protocol

**Phase 5 analysis amendment (2026-11-03, exploratory):**
[Phase 5 specification](phase5_analysis_spec.md) fixes detailed descriptive and
conditional-model procedures before new statistical calculation. Earlier outcome
counts were already known; the new interval choices are not claimed to have been
specified before measurement. Input/label rules and the oracle remain unchanged.

**Phase 4 prospective amendment (2026-11-03):**
[Phase 4 protocol](phase4_protocol.md) governs separate natural-source sampling
from three pinned public repositories. Standardized primary lint conditions,
separate project-config sensitivity and uncertainty investigation are specified
before source outcomes. It supersedes historical authorization statements below;
the Phase 2 oracle remains unchanged.

**Phase 3 prospective amendment (2026-11-03):**
[Phase 3 protocol](phase3_protocol.md) authorizes a fixed 25 × 8 controlled design,
its relevance preflight, paired formatter runs and deterministic repeat sample.
It supersedes the historical authorization statements below. Oracle matching
and classification rules remain those validated in Phase 2.

**Phase 2 prospective amendment (2026-11-03):** The historical protocol below
is retained. [Phase 2 protocol](phase2_protocol.md) now governs correspondence,
classification and validation. Phase 1 evidence keeps its original provisional
labels. New measurements use schema version 2 and the Phase 2 oracle. Main dataset
generation is still unauthorized.

Protocol established before the first feasibility measurement on 2026-11-03 UTC.
The main experiment has not begun. Changes to this protocol must be dated and
identified as prospective or exploratory.

## Research questions

- RQ1: Under what tested conditions does formatting preserve or change effective
  suppression coverage?
- RQ2: Do changes hide warnings, expose warnings, merely relocate directives, or
  accompany changes in underlying diagnostics?
- RQ3: How do Black and Ruff formatting behave on paired identical inputs under
  identical lint settings? No superiority is presumed.
- RQ4: Do controlled observations occur in naturally occurring repository files?
- RQ5 (extension): Can a detector identify independently verified suppression
  changes with useful error rates?

## Hypotheses and definitions

The null hypothesis is unchanged suppression coverage for corresponding underlying
diagnostics after formatting. The alternative is at least one corresponding
diagnostic changing visibility. This is a question to test, not an assumed result.
Phase 1 is a functional feasibility check, not a statistical hypothesis test.

A diagnostic is *underlying* when reported with `--ignore-noqa`, and *visible*
when reported with directives respected. For each identical source snapshot,
suppressed diagnostics are the multiset difference between underlying and visible
diagnostics. A subset check must succeed. This within-source operation uses code,
message, and exact start/end coordinates; it never compares positions across files.

An AST-preserved pair has identical `ast.dump(ast.parse(..., type_comments=True,
feature_version=(3, 11)), include_attributes=False)` output. This strict check
includes type comments and string content, excludes coordinates, and is not proof
of universal runtime semantic equivalence. Docstring or type-comment differences
may fail this check even when a formatter considers the change acceptable.

## Phase 1 scope and inclusion

Use one explicitly AI-authored UTF-8 example, with unused-import (F401) and
undefined-name (F821) diagnostics and both visible and suppressed findings. Run
the same source through each pinned formatter. F841 is selected for later
experiments but is not exercised by this initial example. There is no random
generation or real-world sample. Seed 0 is recorded as an unused placeholder.

Inputs must parse under the installed Python 3.11 grammar. Parse-invalid files
are retained with invalid_source status. Tool failures and timeouts are retained
with Execution failure classification. Unchanged formatted outputs are explicitly
flagged; no denominator based only on changed files is calculated in this phase.
Repeated trial IDs/directories cannot overwrite evidence.

## Execution controls

Use Black 25.1.0, Ruff 0.11.13, pytest 8.3.5, Python 3.11; these are fixed
compatibility baselines, not claims about the latest releases. Record the actual
runtime and full dependency snapshot. Black receives an explicit copied TOML;
Ruff receives `--isolated` and explicit flags. Line length is 88, target py311,
preview disabled, no lint fixes, selected rules F401,F821,F841. These three rules
avoid intentional line-length/style effects, though this does not guarantee
underlying diagnostic stability.

For each pair run A original/normal, B original/ignore-noqa,
C formatted/normal, D formatted/ignore-noqa. JSON stdout, stderr, command,
exit code, timeout and source snapshots are preserved. Ruff check status 1 means
diagnostics and is accepted; other unexpected statuses are execution failures.
All subprocesses have a 30-second bound, use argument arrays without a shell,
and run in fresh temporary working directories. Analyzed programs are never run.

## Interpretation and next validation gate

Phase 1 labels complete AST-equal measurements **Ambiguous** because structural
cross-transformation matching is deliberately deferred to Phase 2. This is not
an empirical ambiguity rate for the future detector. Equal aggregate counts do
not establish equal diagnostic identity or suppression coverage. Newly hidden
and exposed counts remain null, never inferred from counts or line shifts.
AST differences are separately labeled **AST changed** and block attribution.

Phase 2 must implement correspondence by rule, AST/source construct, normalized
context and unambiguous occurrence identity. It must validate underlying
diagnostic stability before assigning Preserved, Newly hidden, Newly exposed or
Mixed; unmatched underlying changes receive Diagnostic changed, uncertain
correspondence Ambiguous. No positive control or drift finding is currently claimed.
All outcomes and exclusions must be retained. Main dataset generation requires
another explicit phase authorization after oracle validation.

## Planned analysis rules (not implemented or executed)

Keep controlled and repository datasets separate. Report denominators and
unchanged outputs; retain failures, ambiguity, AST failures and underlying
diagnostic changes. Compare formatters on paired inputs, account for input-family
and repository dependence, and use Wilson 95% intervals only with an appropriate
interpretation of the sampling unit. Detector metrics require ground truth
independently labeled from the detector. Sampling and detailed analysis must be
specified before the main experiments. No prevalence inference from this example.
