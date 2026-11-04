# Phase 4 — Real-world validation

Completed 2026-11-03 UTC. Natural-source evidence is separate from controlled
examples, development controls and repeat runs. Phase 5 has not been started.

## Selection and provenance

The prospective protocol is `phase4_protocol.md`. Repository selection used a
small historical convenience sample across HTTP, web-framework and testing-tool
domains, chosen before source outcomes. These are not latest-release snapshots
or a representative ecosystem sample. GitHub connector metadata resolved tags to
full commits. Its binary-download limitation required read-only commit archive
downloads; no project code/build scripts, hooks or dependency installers were run.

| Repository | Tag | Commit | Archive .py population | Eligible | Selected |
|---|---|---|---:|---:|---:|
| [Requests](https://github.com/psf/requests/commit/0e322af87745eff34caffe4df68456ebc20d9068) | v2.32.3 | 0e322af87745eff34caffe4df68456ebc20d9068 | 36 | 7 | 7 |
| [Flask](https://github.com/pallets/flask/commit/ab8149664182b662453a563161aa89013c806dc9) | 3.1.0 | ab8149664182b662453a563161aa89013c806dc9 | 83 | 13 | 13 |
| [pytest](https://github.com/pytest-dev/pytest/commit/b55ab2aabb68c0ce94c3903139b062d0c2790152) | 8.3.5 | b55ab2aabb68c0ce94c3903139b062d0c2790152 | 256 | 28 | 20 |

Eligibility required natural COMMENT-token noqa, UTF-8, Python 3.11 validity,
the 200 KiB cap and predefined generated/vendored filters. Requests excluded
twenty-eight no-directive files and one generated-header match; Flask excluded
seventy no-directive files; pytest excluded 226 no-directive files and two
generated-header matches. Every Python population member/exclusion is retained.
Generated/vendored detection remains heuristic, with that limitation disclosed.

Rank paths within each repository by SHA-256 of
`20261103:phase4:repository_full_name:path`; take the first up to twenty. All
seven Requests and thirteen Flask eligible files were used; twenty of twenty-eight
pytest files were selected. No replacement or outcome-based relevance filter was
applied. Tests and examples remained eligible, and source file roles are recorded.
There were no access failures and the predetermined fallback was not used.

Full archives, archive hashes, selected original bytes, complete populations,
natural comment text/positions, licenses and configuration checksums are in
`datasets/real_world/phase4`. ai_assisted=false means the study did not generate
or modify these inputs with AI; upstream authoring practices are unknown.
AI assisted the collection/measurement code and documentation.

Code, protocol, sample and provenance were frozen at **b70e42d** before main
measurement. The frozen source manifest SHA-256 is
`007caa19c5913e34e5dd0cf363589a83a5bb84b19d7a046e8821a89c76144d89`.
The oracle modules and all earlier phase evidence remained unchanged.

## Executed primary comparisons

Ran each of forty files through both pinned formatters: **80 standardized
comparisons**, with all four real Ruff passes per pair. Pins/settings match
Phase 3: Python 3.11.9, Black 25.1.0, Ruff 0.11.13, F401/F821/F841, target py311,
line length 88, preview disabled, no fixes, isolated linting. The primary lint
filename remains **study_input.py**; real repository paths are metadata, not a
claim that these diagnostics match project-native __init__.py handling or CI.

| Repository / formatter | Comparisons | Preserved | Strict AST excluded | Text changed |
|---|---:|---:|---:|---:|
| Requests / Black | 7 | 7 | 0 | 3 |
| Requests / Ruff format | 7 | 7 | 0 | 2 |
| Flask / Black | 13 | 12 | 1 | 1 |
| Flask / Ruff format | 13 | 13 | 0 | 1 |
| pytest / Black | 20 | 18 | 2 | 2 |
| pytest / Ruff format | 20 | 19 | 1 | 6 |

**No newly hidden, newly exposed or Mixed result was observed.** There were no
Ambiguous, Diagnostic changed or Execution failure outcomes. Seventy-six pairs
were Preserved; four retained the required **AST changed** label under the strict
oracle. Those four are exclusions from suppression attribution, not confirmations
of preservation. Fifteen formatter/file comparisons changed text; eleven of them
were AST-accepted and suppression-preserved. Sixty-five outputs were unchanged.

The same repository file tested by two formatters contributes two dependent
comparisons. No natural-source denominator is pooled with synthetic data.

## Diagnostic relevance and negative-result limits

Natural noqa comments do not necessarily target the three rules selected here.
Zero underlying warnings were retained rather than replaced with more promising
inputs. Before formatting, these per-formatter counts were the same for both
formatters because the original sources/settings were identical:

| Repository | Selected files | With underlying selected warnings | With original selected-rule suppression | With zero selected warnings |
|---|---:|---:|---:|---:|
| Requests | 7 | 6 | 5 | 1 |
| Flask | 13 | 4 | 4 | 9 |
| pytest | 20 | 8 | 8 | 12 |

Thus forty-four of eighty comparisons had empty underlying diagnostic sets.
Only seven comparisons both changed text, passed the strict AST gate and began
with selected-rule suppression (five Requests, zero Flask, two pytest). This
is an important limit on the opportunity to observe suppression movement.
The zero-drift result is not evidence that formatting preserves all real-world
suppressions, that other rules cannot drift, or that the controlled mechanisms
are absent elsewhere.

## Project-config sensitivity

Archived Ruff config was discovered for thirteen Flask and twenty pytest files.
Ran **66 supplementary four-pass comparisons** on the same preserved source
pairs, with those configs and their original paths. Native rule selection and
ignores were respected; full raw native diagnostics are retained, while only
F401/F821/F841 were classified by the supported oracle. This is configuration
sensitivity in a restored safe archive context, not project CI, a complete native
environment or a verdict on the rest of the native rule set. No formatter was
rerun using project-native formatter settings.

The study-rule outcomes matched the primary outcomes on these files:
Flask Black 12 Preserved/1 AST changed, Flask Ruff 13 Preserved, pytest Black
18 Preserved/2 AST changed, pytest Ruff 19 Preserved/1 AST changed. No native-config
drift or configuration execution failure was observed. Forty-two of these
sixty-six comparisons had no underlying selected-rule diagnostics (eighteen Flask,
twenty-four pytest), which further limits interpretation.

Requests had no discovered Ruff configuration at this commit; its fourteen
supplementary records explicitly say no_project_ruff_config rather than inventing
native results. A configuration's presence does not establish actual project
tool use. All eighty supplementary status records are retained separately from
the eighty primary observations in their own JSONL and CSV.

## Investigation of every uncertainty

The four primary strict AST exclusions were:

| Formatter | Original file | Differing AST fields |
|---|---|---:|
| Black | Flask src/flask/app.py | 18 TypeIgnore.lineno fields |
| Black | pytest src/_pytest/_code/code.py | 2 TypeIgnore.lineno fields |
| Black | pytest src/_pytest/logging.py | 2 TypeIgnore.lineno fields |
| Ruff | pytest src/_pytest/logging.py | 2 TypeIgnore.lineno fields |

Python's TypeIgnore line numbers are AST fields even when ordinary positional
attributes are omitted from ast.dump. An investigative copy that zeroes only
those fields makes each before/after AST equal. **Original classifications were
retained**: this secondary explanation did not relax the frozen oracle or claim
drift/preservation for excluded pairs. The four supplementary exclusions had
the same cause. Field paths and old/new values are preserved per trial in
`datasets/results/phase4-investigation`.

No primary drift existed to intervene on, so **zero comment-neutralization
interventions were performed**. The summary's all_interventions_passed=true is
vacuous with an empty list and is not positive validation evidence. A future
prospectively specified AST sensitivity could distinguish TypeIgnore position
metadata from executable-syntax changes; it was not applied to primary labels.

## Tests and reproducibility

**103 tests passed**, including collection safety, token-vs-string detection,
eligibility, deterministic ranks, exact bytes/licenses, config lookup, real native
scope/ignore behavior, incompatible config retention, natural provenance and
tamper detection, in addition to the earlier frozen oracle controls. Implementation
lint checks passed. An unused implementation import was removed before the gate.

The prospectively selected first path per repository was repeated with both
formatters: **six primary comparisons**, plus four applicable native sensitivity
comparisons and two missing-config status records. Hashes, diagnostic content,
identities and classifications agreed with their main records. All six selected
repeat transformations happened to be text-unchanged, which limits this repeat
check's coverage of changed natural outputs; no replacements were chosen afterward.

The verifier recreated every repository's full eligibility population and exact
sample from the preserved archive, verified archive/configuration/license hashes
and all forty source bytes, checked every primary/native CSV and JSONL record,
and checked raw diagnostic evidence. All checks passed. No network access or
repository program execution is needed to verify retained evidence.

See `reproducibility.md` for commands. Main results are in `datasets/results/phase4`,
repeats in `datasets/results/phase4-repeat`, investigations in
`datasets/results/phase4-investigation`, and test/log/verification artifacts in
`reports/phase4`.

## Relationship to controlled findings and next gate

Phase 3 found 103 oracle-classified drift comparisons on its deliberately
constructed stress suite. No corresponding natural-source drift was found under
the present standardized conditions. These findings are compatible: the natural
convenience sample has a different selection frame, mostly unchanged text, many
empty selected-rule diagnostic sets and four conservative exclusions. Do not
combine their proportions or interpret them as a detector accuracy estimate.

Two datasets have now been collected and documented; statistical analysis,
uncertainty treatment, the full research report and final polish remain pending.
Phase 5 should audit result integrity and perform the planned analysis with
paired formatter/file observations and within-repository dependence accounted
for. It requires explicit authorization. No intervals, significance tests,
figures, full report or explorer were created in Phase 4.
