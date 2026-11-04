# Report claim review - 2026-11-03

Scope: the Phase 6 report, its template and current documentation. This is an
AI-assisted evidence review, not independent human validation. The generated
ledger covers 86 distinct numeric or provenance bindings (some repeated in prose).
It records JSON fields, transformations, actual values and source hashes. No
external study's quantitative findings are reused as our results.

## Evidence checks beyond templated values

| Claim | Retained evidence / review |
|---|---|
| Controlled zero Mixed, Diagnostic changed, AST changed and Execution failure | `reports/phase5/analysis/metrics.json`, `controlled.{black,ruff}.outcomes`: all four values are zero for each formatter. |
| Natural zero Ambiguous, Diagnostic changed and Execution failure | Same file, all six `natural` repository/formatter outcome maps: zero. Confirmed-drift zero is also bound per row. |
| Every Ruff controlled drift also has Black drift | `controlled_pairs.matrix_rows_black_columns_ruff_0_1[0][1]` is zero. This says nothing about drift direction. |
| Same unresolved controlled inputs | `controlled_pairs.one_sided_unresolved=0`, `both_unresolved=16`; boundary grouping documented in Phase 3 results and family tables. |
| Natural type-ignore exclusions and normalization | `docs/phase4_results.md` and `datasets/results/phase4-investigation`; excludes Black Flask app, Black pytest code and both formatter pytest logging pairs. These retain primary AST-changed labels. |
| Native outcomes agree | `metrics.json`, `native` completed and same_primary_classification counts agree for Flask and pytest. Requests completed is zero; its 14 records are absence statuses. |
| Most natural text unchanged; many selected-empty | Six natural metrics rows sum to 15 changed / 80 comparisons and 44 zero-underlying / 80. No relevance-filtered positive subset is substituted. |
| Controlled design and dependence | `datasets/controlled/phase3/manifest.json`: unique input_family and directive_placement counts bind the template. Eight directive modes include distinct placement variants; suppression_type alone has six values and is not the mode count. |
| Natural historical frames and tags | `datasets/real_world/phase4/manifest.json`, repositories and cases; exact tags, frame counts and sample counts bind the template. Commits and hashes remain in that manifest. |
| Pins, grammar, settings and rules | `requirements-analysis-lock.txt`, `configs/controlled.toml`, Phase 1 installed help and trial environment/command records. Python 3.11.9 is the experiment runtime, not the PDF runtime. |
| Four-pass matching and semantic limitations | `docs/phase2_protocol.md`, `src/suppression_study`; four passes separate suppression from underlying diagnostics and AST/ambiguity failures. AST equality is not runtime equivalence. |
| Post-count exploratory statistics | `docs/phase5_analysis_spec.md`, dated methods commit and Phase 5 findings. No confirmatory preregistration, population coverage or significance claim. |
| Bootstrap level, whole-cluster treatment and bounds | `metrics.json`, `cluster_model_intervals` level 0.95; both methods are paired whole-cluster percentile bootstrap, 20,000 draws each. `finite_all_scheduled_contrast_bounds` is a distinct all-scheduled estimand. |
| No measured detector accuracy | `metrics.json`, detector_accuracy_evaluated=false; controls and interventions do not provide independent held-out human labels. |
| Source and AI provenance | Controlled manifest ai_assisted=true; natural manifest ai_assisted_source_generation=false refers only to study-side generation. No assertion about upstream AI use. |
| Literature authors, titles, year, journal/pages | Primary PDF relevant passages plus selected Crossref metadata in `hu_crossref.json` and `statictracker_crossref.json`; source access hashes in literature_access.json. McKeeman printed page 100 verifies name/title/journal/year; journal article is pages 100-107. |
| Report length and layout | `pdf_validation.json` and `pdf_visual_review.md`: six pages, section checks and rendered-page review. |

## Interpretation audit

The report keeps scheduled and resolved denominators separate, reports exclusions
without imputing them as preservation, and treats conditional cluster intervals
separately from finite completion bounds. Natural repositories are not pooled for
IID inference. Hiding and exposure are visibility events, not judgments of warning
truth or formatter quality. The natural result remains negative. We state no
precision/recall/F1, ecosystem frequency, general superiority, priority, independent
review, public release or publication readiness.

The audit verifies reporting consistency with the retained analysis and protocols.
It cannot discover all matching errors already encoded in those inputs, certify
causality beyond the experimental assumptions, or substitute for expert review.
