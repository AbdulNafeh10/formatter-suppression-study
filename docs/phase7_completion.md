# Phase 7 - final review and reproduction

Historical checkpoint from the original repository. Current packaging, license
and reproduction status is in [public_snapshot.md](public_snapshot.md).

Completed 2026-11-03. All seven phases in the original brief are complete. This
repository is an inspectable empirical pilot; independent scientific assessment
and detector-accuracy evaluation remain outside the completed work.

## Delivered

- Repository-wide test, formatting, lint, dependency and reporting checks.
- Full fresh controlled and natural-source measurements under the original pins,
  with old evidence retained and fresh outputs stored separately.
- Recomputed analysis, tables, bootstrap draws and standalone figures.
- An [evidence guide](evidence_guide.md), [resume description](resume_description.md),
  [future research agenda](future_research.md), and internal scientific review.
- A small style correction in `scripts/prepare_phase2_controls.py`: replacing a
  lambda assignment with a named function satisfies Ruff E731 without changing
  the comment-neutralization method. No oracle or study criteria changed.

The optional explorer was omitted. Direct source/diagnostic evidence and the
navigation guide keep the study usable without an application dependency.

## Executed results

| Check | Result | Evidence |
|---|---|---|
| Full pytest suite | 126 passed | `reports/phase7/pytest.xml`, pytest.log |
| Black check | 36 Python files unchanged | format.log |
| Ruff check | Passed | lint.log |
| Dependency consistency | pip check passed; all 25 analysis-lock distributions match | dependencies.log, repository-review.json |
| Report claims | 86 evidence-bound claims verified | claim-check.log |
| Helper regression check | Token/AST and length checks passed on 20 retained control snapshots | helper-check.json |
| Controlled reproduction | All 400 comparisons match originals; all 200 sources regenerate identically | controlled-reproduction.json |
| Natural reproduction | All 80 primary comparisons and native status records match; archived population and selection recreate identically | natural-reproduction.json |
| Analysis reproduction | All 19 numeric/table artifacts and four PNG/SVG pairs match byte-for-byte | analysis-reproduction.json |
| Original evidence and report | Source, original data, analysis inputs, original configurations and reviewed PDF remain unchanged | repository-review.json, navigation-check.json |

All evidence paths in the table are under `reports/phase7` unless specified.
Fresh trials are in `datasets/results/phase7-controlled` and
`datasets/results/phase7-natural`; derived analysis is in `reports/phase7/analysis`.
Commands and fresh-output instructions are in [reproducibility.md](reproducibility.md).
The original environment is Windows / CPython 3.11.9 with Black 25.1.0 and Ruff
0.11.13. Validation uses the existing environment, not a clean-machine install or
another platform. Archive reconstruction is offline, not a new network acquisition.

The complete natural rerun includes all 15 changed primary outputs. This extends
repeatability coverage beyond the original Phase 4 prospective subset, which had
only unchanged outputs. The Phase 6 report is retained as its frozen checkpoint;
its repeat-coverage limitation describes that earlier subset. Repeats and native
sensitivity are not additional independent observations. Missing Requests native
configuration remains a status, not an executed native measurement.

## Scientific scope and remaining issues

The original controlled findings and negative natural-source result are unchanged.
Scheduled/resolved denominators, paired input identity, explicit ambiguity and
AST exclusions remain separate. Bootstrap/Wilson outputs are exploratory conditional
models; finite-corpus bounds are different estimands. No ecosystem prevalence,
general formatter superiority, originality priority or independent precision/recall
is established. See `reports/phase7/scientific_review.md` for the consistency review.

The same AI-assisted process performed implementation and verification. No
independent human adjudication, external scientific endorsement, publication,
external submission or public hosted release occurred. Natural-source licenses
and provenance remain in the archived dataset. The resume text requires the user's
review of their actual contribution and disclosure obligations.

Future work prioritizes independent held-out labels, prospectively defined natural
sampling, broader configurations and careful matching/AST-gate extensions. These
are proposals, not completed features. No further phase is defined by the original
brief; extensions require a new scope.
