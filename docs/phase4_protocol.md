# Phase 4 prospective real-world validation protocol

Established 2026-11-03 UTC before inspecting repository source or lint/format
outcomes. Phase 4 remains separate from the controlled suite and prior controls.
No inference/statistical analysis, figures, full report or explorer is authorized.

## Repository selection and immutable acquisition

Use a convenience sample of three public Python projects from distinct domains:
psf/requests at v2.32.3 (HTTP client), pallets/flask at 3.1.0 (web framework),
pytest-dev/pytest at 8.3.5 (testing tool). These historical release tags are chosen
for availability and compatibility with the already pinned Python/tool era,
not because of known suppression changes. Resolve each tag to a full commit ID
using the GitHub connector and freeze it before acquiring sources. They are not
a representative or latest-release sample. If access fails, retain failure
evidence and try pallets/click at 8.1.8 as a predetermined fallback; otherwise
report incomplete access rather than substitute fabricated files.

The connector cannot download binary archives. Download the immutable full-commit
GitHub source tarball as a read-only acquisition fallback; preserve archive URL,
SHA-256, full commit/tag, metadata and licensing files. Never import, install or
execute repository programs, project build tools or Git hooks. Inspect archives
without unrestricted extraction. Reject unsafe/symlink/nonregular members.

## Eligible population and deterministic sampling

Enumerate every regular tracked .py file represented in each commit archive.
Record a row for every Python member and every exclusion. Exclude paths containing
vendor, vendored, _vendor, third_party, third-party or generated components;
protobuf-generated *_pb2.py/*_pb2_grpc.py; and files with an auto-generated,
generated-by or do-not-edit marker in the first 4096 bytes. These are conservative
heuristics, not a claim to perfectly identify every generated file.

Apply a 200 KiB source-size cap. Require UTF-8 source valid for the pinned Python
3.11 parser/compiler. Require a natural COMMENT token matching noqa syntax,
including file-level variants; directive-looking strings do not qualify. Do not
filter by selected warning rule, lint outcome, formatter compatibility or drift.
Tests and package initializers are eligible; preserve original path and file role.
Keep UTF-8/grammar/generated/no-directive/unsafe exclusions explicitly.

Within each repository, rank eligible paths by SHA-256 of
`20261103:phase4:repository_full_name:path`. Select the first **up to 20** files.
If fewer qualify, use all; do not search for replacement positives. Save complete
eligible/excluded populations, ranks, selected paths and original source bytes.
Naturally occurring source is flagged ai_assisted=false; AI assists collection
code/documentation, not the repository input bytes. Preserve repo license texts.

## Standardized primary measurement

Freeze the population/sample manifest, code and configuration in Git before
running measurements. Gate execution on the existing oracle and collection tests.
Run both formatters on the identical unmodified selected files, with the same
pins and isolated four-pass F401/F821/F841 conditions used in Phase 3. Do not
exclude files with zero underlying selected warnings: record their diagnostic
and suppression counts so vacuous preservation remains visible. Preserve tool
failure, invalid/AST-changed output, underlying change, ambiguity and unchanged text.

The primary lint filename remains study_input.py to preserve the standardized
condition from the controlled study. In particular, this is not a claim about
native __init__.py lint behavior. Record original paths separately. Never imply
a project uses Ruff merely because our study runs Ruff against its sources.

## Project-configuration sensitivity, where possible

Inspect archived ruff.toml, .ruff.toml and pyproject.toml with tool.ruff, including
ancestor configs. Save relevant configuration files/extend targets in a safe
context, without running project code. If a discoverable project Ruff config is
present, run a supplementary four-pass lint comparison on the SAME preserved
source pair using that config and the actual original file path. Respect native
rule selection/ignores; keep full raw diagnostics but classify only the study's
three supported rules. Do not call this full project CI or native environment
reproduction. Missing config, incompatible config and native lint failures are
recorded separately and do not invalidate the primary standardized trial.

Config sensitivity uses a restored archive context for configuration discovery,
not the project's installed dependencies/Git checkout. Any ignored-file or
path-dependent behavior must be documented. No formatter is rerun with native
formatter settings; this isolates lint-configuration sensitivity on the same pair.

## Reproduction, investigation and reporting

Repeat the lexicographically first selected path per repository with both
formatters (up to six comparisons), chosen without looking at outcomes. Check
all retained source/archive hashes, complete CSV/JSONL records and paired coverage.
Compare repeat hashes, raw diagnostics, identities and classifications, excluding
only execution-specific filenames/paths and timestamps.

Investigate every Ambiguous/AST changed/Diagnostic changed/Execution failure trial
through saved errors, AST and anchor evidence, without altering the frozen oracle
or relabeling uncertainty as preservation. Summarize reasons per repository.
For every observed primary drift trial, perform a comment-only noqa-neutralization
intervention and check code-token/AST preservation plus restored underlying Ruff
diagnostics. Retain failed or inconclusive interventions; do not discard them.

Report per-repository populations, exclusions, sampling, standardized outcomes,
nonvacuous diagnostic/suppression counts, native-config sensitivity and repeat
checks separately. Compare observed mechanisms descriptively with Phase 3;
never combine synthetic and natural prevalence denominators. A negative result
is valid and does not refute the controlled mechanisms. No population prevalence,
formatter superiority, detector accuracy or unseen-repository generalization is
justified by this small convenience sample. Stop after Phase 4 and await approval
to proceed to Phase 5.
