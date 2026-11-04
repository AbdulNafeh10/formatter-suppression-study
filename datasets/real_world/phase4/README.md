# Natural source sample — Phase 4

These bytes come from immutable public GitHub commit archives. The study did not
generate or modify repository inputs with AI; ai_assisted=false refers to this
study's input provenance, not upstream authors' unknown tool use. AI assisted the
collection/measurement implementation and documentation. No repository programs
were imported, installed or executed.

| Repository | Release tag | Commit | Archived .py population | Eligible natural-noqa files | Selected |
|---|---|---|---:|---:|---:|
| psf/requests | v2.32.3 | 0e322af87745eff34caffe4df68456ebc20d9068 | 36 | 7 | 7 |
| pallets/flask | 3.1.0 | ab8149664182b662453a563161aa89013c806dc9 | 83 | 13 | 13 |
| pytest-dev/pytest | 8.3.5 | b55ab2aabb68c0ce94c3903139b062d0c2790152 | 256 | 28 | 20 |

Selection is a historical convenience sample of three domains, not a
latest-release or representative ecosystem sample. Each population is enumerated
before lint/format outcomes. Rank is SHA-256 of
`20261103:phase4:repository_full_name:path`; take the first up to twenty eligible
files. Eligibility requires natural COMMENT-token noqa, UTF-8, valid Python 3.11,
the 200 KiB cap, and the documented generated/vendored exclusions. Do not replace
negative, empty-warning or inconclusive outcomes with other files.

The public snapshot excludes `archives/`; the original archive hashes and immutable
URLs remain in `manifest.json` for checked retrieval. See the snapshot reproduction
instructions in `docs/reproducibility.md` at the repository root. Unused Requests
artwork/theme context and certificate fixtures are not distributed. Per-repository `.population.json` files preserve
all Python paths, reasons for exclusion, complete eligibility/rank data and
selected status. `sources/` preserves selected bytes. `contexts/` retains
configuration/extend targets, gitignore and license texts, with checksums. Source
links in the manifest point to the full commit and original repository path.

The prospective protocol is `docs/phase4_protocol.md`. Input/sample metadata,
configuration context and code were frozen at commit `b70e42d`. The main source
manifest SHA-256 is
`007caa19c5913e34e5dd0cf363589a83a5bb84b19d7a046e8821a89c76144d89`.
This README was added afterward and does not alter the frozen manifest or inputs.

Project-config sensitivity is supplementary. The main standardized measurement
retains the study_input.py lint filename from the controlled experiment; the
supplementary run uses archived Ruff config and the real path in a safe context.
Neither constitutes the projects' CI, dependency environment or entire lint rule
set. Finding a Ruff config is evidence of configuration, not proof of tool use.
Requests has no discovered Ruff config at this snapshot. Licenses remain those
of each original repository; the copied license/notice texts and full archives
are retained alongside the study inputs.
