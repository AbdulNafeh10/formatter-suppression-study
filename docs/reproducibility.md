# Reproducibility in the public snapshot

Use Windows and CPython 3.11 with the retained historical tool pins. Run from the
snapshot root in PowerShell. Programs being analyzed are never executed.

Git must be on PATH, and this must be a Git checkout with a committed HEAD.
Provenance scripts use Git; a source ZIP without Git metadata is not supported
by the supplementary provenance step. The checked Git version is recorded in
the release dependency record.

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-analysis-lock.txt
.\.venv\Scripts\python.exe -m pip install --no-deps --no-build-isolation -e .
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe -m black --check --config configs/black.toml src tests scripts
.\.venv\Scripts\python.exe -m ruff check src tests scripts
```

New local outputs may contain machine-specific paths. Keep them under ignored
`local` or `reports/local-*` paths and do not include those folders in a release.
The privacy-derived records already tracked here are historical observations,
not commands to execute verbatim. Their placeholders intentionally hide private
execution paths. See [public_snapshot.md](public_snapshot.md).

## Check retained measurements and claims

```powershell
.\.venv\Scripts\python.exe scripts/build_public_docs.py --check
.\.venv\Scripts\python.exe scripts/build_report.py --check
.\.venv\Scripts\python.exe scripts/audit_ambiguities.py --verify reports/ambiguous-audit
.\.venv\Scripts\python.exe scripts/verify_phase3.py --repeat datasets/results/phase7-controlled --report local/controlled-check.json
.\.venv\Scripts\python.exe scripts/verify_phase4.py --repeat datasets/results/phase7-natural --allow-missing-archives --report local/natural-retained-check.json
```

The last command explicitly skips archive population reconstruction while checking
retained sources, four-pass diagnostics, CSV/JSONL agreement and saved repeat
comparisons. Its output records the skipped checks as false. Natural code in
`*.evidence.json` is decoded and checksum-checked by the verifier; the decoded
bytes and diagnostic coordinates are unchanged. No proposed review label replaces
an original automatic label.

## Reconstruct the full upstream sample

```powershell
.\.venv\Scripts\python.exe scripts/fetch_pinned_archives.py --output local/upstream-archives
.\.venv\Scripts\python.exe scripts/verify_phase4.py --repeat datasets/results/phase7-natural --archive-cache local/upstream-archives --report local/natural-full-check.json
```

The fetcher uses pinned HTTPS URLs, size bounds and the original SHA-256 values.
An existing wrong archive is rejected. Full reconstruction reads archives as data
and recreates the original population and selection without executing upstream
code. Downloaded artwork, certificates and other unrelated files stay in the
ignored local cache; do not redistribute that cache. Upstream hosting may change.
The retained sampled sources and necessary configuration also support offline
natural reruns without full archives; that mode checks their own hashes and
explicitly discloses the absent archive validation.

## Fresh measurements and analysis

Choose unused output directories. Existing observations must not be overwritten.
For the full controlled run, copy `configs/phase7-reproduction.toml` to an ignored
local config and change only its output path to `local/controlled-fresh`; then run:

```powershell
.\.venv\Scripts\python.exe -m suppression_study experiment --config local/controlled-reproduction.toml
.\.venv\Scripts\python.exe scripts/run_phase4.py --output local/natural-fresh
.\.venv\Scripts\python.exe -m suppression_study analyze --output reports/local-original-analysis --figures reports/local-original-analysis/figures
.\.venv\Scripts\python.exe scripts/analyze_reviewed_results.py --output reports/local-reviewed-analysis
.\.venv\Scripts\python.exe scripts/make_reviewed_figures.py --output reports/local-reviewed-figures
```

Analysis commands use the retained primary observations, not automatically the
fresh local runs. Their integrity gates still verify source bytes, underlying
warning correspondence and within-source arithmetic. Compare fresh measurement
outputs with the saved runs using the verifiers' `--repeat` option. Repeats are
not additional independent samples. For uncertainty assumptions, see the
[analysis specification](phase5_analysis_spec.md) and
[supplementary methods](../reports/publication-phase-a/methods.md).

## PDF and figure exports

Report rendering uses a separate Python 3.12 environment with
`requirements-report.txt`; it is not part of the study dependency lock. Run
`python scripts/render_report.py --public` in that environment to render the
six-page public PDF. The default renderer targets the historical original report.
Generated PDFs require visual review. Relative PDF links depend on viewer support;
use Markdown for reliable navigation. Standalone PNG/SVG pairs retain the original
figure values. [Release verification](../reports/public-release/verification.json)
records what was actually tested; untested platforms are not implied.
