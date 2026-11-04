# Methodology

The measurement unit is one source formatted by one tool. Each original source
is paired across Black and Ruff. The controlled corpus tests specific layouts;
the natural sample checks the same procedure on unedited upstream source.
They answer different questions and are analyzed separately.

## Tool settings and execution

The measured environment was CPython 3.11.9 on Windows, Black 25.1.0 and Ruff
0.11.13. Both formatters used line length 88, target `py311` and no preview.
Ruff selected F401 (unused import), F821 (undefined name) and F841 (unused local),
without fixes. Primary lint calls used isolated configuration and the filename
`study_input.py`, including for files originally named `__init__.py`. Black used
an explicit study TOML file. These conditions make the primary comparison
consistent across inputs; they do not reproduce each project's normal CI.

Subprocesses received argument arrays, a temporary working directory and a
30-second timeout. No shell was used. Python compilation checked source legality;
the programs under analysis were never executed.

## Separating warnings from suppression

Each comparison has four Ruff passes:

| Pass | Source | `noqa` handling | Meaning |
|---|---|---|---|
| A | Original | Respected | Warnings ordinarily visible before formatting |
| B | Original | Ignored | Underlying warnings before formatting |
| C | Formatted | Respected | Warnings ordinarily visible after formatting |
| D | Formatted | Ignored | Underlying warnings after formatting |

Within a snapshot, visible diagnostics must be a multiset subset of underlying
diagnostics. This check uses the rule, message and exact start/end coordinates.
The difference identifies suppressed warning occurrences. A change in the visible
count alone cannot distinguish changed suppression from changed underlying warnings.

Across snapshots, line numbers are unreliable because formatting moves code.
The matcher keys a warning by rule and AST field/index path, then checks its
coordinate-free node representation, construct tokens and diagnostic tokens.
F401 anchors to an import alias, F821 to a loaded `Name` and F841 to a stored
`Name`. Ruff character columns are converted when compared with AST UTF-8 byte
offsets. Anchors must be unique and cover complete, aligned token spans.
Unsupported anchors remain unresolved rather than being matched by counts or
similar messages. The implementation is in `src/suppression_study/matching.py`.

The AST gate parses with Python 3.11 grammar and `type_comments=True`, then
compares dumps without node attributes. `TypeIgnore.lineno` is an AST field,
so it still participates. Equality checks this representation, not runtime
equivalence. The four natural-source exclusions caused by shifted type-ignore
lines retain their original labels.

Only an accepted AST gate and stable underlying correspondence permit a
visibility judgment. A formerly visible warning becoming suppressed is Newly
hidden; the reverse is Newly exposed. Both transitions give Mixed. Preserved
means no transition under these checks, including when selected warning sets
are empty. Ambiguous, Diagnostic changed, AST changed and Execution failure
remain separate outcomes, with unresolved drift counts left null.

## Inputs and analysis

The controlled design crosses 25 templates with eight directive modes: 200
sources and 400 comparisons. Seed 20261103 ranks execution by SHA-256; it does
not generate random programs. Template construction used AI assistance and
development controls. The main suite was frozen before its run, but was not
held out for evaluating matcher accuracy. Treatments of the same template are
related observations.

The natural sample uses pinned historical commits of Requests, Flask and pytest.
Eligible files contain a genuine COMMENT-token `noqa`, are UTF-8, compile under
Python 3.11 and are at most 200 KiB, with documented generated/vendored exclusions.
Seeded hash ranking selected up to 20 eligible files per project without looking
at formatter outcomes: 7 Requests, 13 Flask and 20 pytest files. The
[sampling protocol](phase4_protocol.md) records the frame and pins. The separate
native-configuration check reran linting on primary source pairs, not formatting
under each project's settings. It executed 66 comparisons; 14 Requests entries
record missing configuration rather than completed native checks.

The [analysis specification](phase5_analysis_spec.md) distinguishes corpus
proportions, paired contrasts, unresolved-outcome bounds and exploratory
cluster-model intervals. Detailed statistical choices followed the initial
counts. Cluster assumptions are not established by the authored templates, and
the intervals do not estimate ecosystem prevalence.

The [supplementary review](../reports/ambiguous-audit/ambiguous_comparisons_review.md)
proposes resolutions for 32 ambiguous comparisons. It uses saved diagnostics and
comment-only interventions, with separate reviewed metrics. It neither replaces
the automatic labels nor supplies independent human ground truth. See
[limitations](limitations.md) and the [AI disclosure](ai_use.md).

<details>
<summary>Historical Phase 1 protocol and dated amendments (unchanged)</summary>

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

</details>
