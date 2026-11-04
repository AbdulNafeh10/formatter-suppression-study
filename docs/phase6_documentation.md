# Phase 6 - research report and documentation

Completed 2026-11-03 UTC. Scope is Phase 6 only. No new experimental observations,
oracle changes, reclassification, explorer, application statement or Phase 7 full
test run were introduced.

## Delivered artifacts

- `report/research_report.md` and six-page `report/research_report.pdf` include the
  requested sections, separate dataset findings, exploratory uncertainty, limitations,
  future research, references and AI disclosure. They are factual drafts for review.
- `report/research_report.template.md`, `report/claim_spec.json` and
  `scripts/build_report.py` bind 86 distinct claims to retained JSON fields. The
  generated audit records source hashes and template locations. `--check` detects
  stale evidence bindings, hand-edits and inconsistent derived output.
- `scripts/render_report.py` and separate `requirements-report.txt` reproduce the
  PDF from the generated Markdown without changing the experimental environment.
- `docs/related_work.md` records verified primary literature, relevant-passage
  review scope, metadata corrections and originality limits. Source retrieval
  evidence and selected Crossref metadata are in `reports/phase6`.
- `docs/methodology.md`, `docs/limitations.md`, `docs/ai_use.md`, README and
  `docs/reproducibility.md` give the consolidated method, caveats and instructions.
  Earlier protocols remain historical records rather than being silently rewritten.

## Executed validation

Commands ran from the repository root using the pinned study Python unless stated:

```powershell
.\.venv\Scripts\python.exe scripts/build_report.py
.\.venv\Scripts\python.exe -m black --config configs/black.toml scripts/build_report.py scripts/render_report.py tests/test_report.py
.\.venv\Scripts\python.exe -m ruff check scripts/build_report.py scripts/render_report.py tests/test_report.py
.\.venv\Scripts\python.exe scripts/build_report.py --check
.\.venv\Scripts\python.exe -m pytest -q tests/test_report.py --junitxml=reports/phase6/pytest.xml
.\.venv\Scripts\python.exe scripts/verify_phase5.py --report reports/phase6/analysis_integrity.json
```

Three targeted tests passed: stale measurements/hand-edits, missing bindings, and
source path escape. Lint passed; Black formatted only the three new Python files.
The prior full-suite checkpoint remains Phase 5's 123 tests, not a new full-suite
run. Phase 7 will own full-repository final validation if authorized.

The optional renderer ran twice with bundled CPython 3.12.14, ReportLab 4.4.9 and
pypdf 6.10.0. Both PDF digests were identical. Poppler produced six page PNGs and
each was inspected; no layout defect was found. The final PDF hash and content
checks are in `reports/phase6/pdf_validation.json`; visual review is documented
in `pdf_visual_review.md`. Temporary reading/rendering copies are ignored.

The Phase 5 verifier confirmed matching numeric artifacts, bootstrap draws and
all four PNG/SVG figure pairs. An additional direct check verified all twelve
Phase 5 input digests and no changes from baseline `d876051` in raw data,
implementation, experiment configuration, prior phase evidence, figures or study
dependency locks. `scope_integrity.json` retains this result. No scientific
measurement or statistical calculation was rerun for the report.

## Findings and unresolved limitations

The report retains the original controlled findings and the separate negative
natural-source result. Black has 68 confirmed changes and Ruff 35 among 200
controlled comparisons each; both have 16 ambiguous cases. The common-resolved
paired difference is 17.93 percentage points. Natural files show no confirmed
changes; conservative AST exclusions and limited warning relevance remain explicit.
These are the Phase 3-5 measurements, not Phase 6 observations.

Independent detector accuracy is unmeasured. Cluster intervals remain conditional
exploratory models; natural convenience sampling cannot establish prevalence.
No novelty priority, formatter superiority or publication readiness is asserted.
The supplied paper's provisional footer was resolved against final author text and
Crossref metadata; inaccessible publisher full text was not claimed as reviewed.
The claim audit checks reporting consistency, not oracle correctness or independent
scientific validity. Future human review and held-out adjudication remain necessary.

## Handoff

Phase 6 is complete. Phase 7 would review repository quality, run the entire suite,
verify full reproduction, consider an optional minimal explorer, and prepare a
careful application description. It requires explicit user authorization.

PDF artifacts are explicitly marked binary in Git to preserve their exact bytes.
New derived Phase 6 JSON records use LF line endings; prior raw evidence is untouched.
