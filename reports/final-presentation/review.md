# Final report presentation review

Baseline: local documentation commit `4d64e72b`. The published evidence snapshot
remains `7c77a230`. This revision is local and does not authorize publication.

## Substantive changes

| File | Change and reason |
|---|---|
| `report/research_report_public.template.md` | Add Abdul Nafeh as visible author; embed four existing figure references with explanatory captions; copy an actual before/after source pair; clarify sections 3.2, 3.4, 4.2 and 6; explain reproduction terminology. Preserve the introduction, related work, discussion and conclusions apart from the necessary figure navigation. |
| `report/research_report_public.md` | Regenerate from that template with the unchanged public-document builder. |
| `report/research_report_public.pdf` | Regenerate as nine pages, including two landscape figure pages. Correct author metadata, retain AI disclosure, and use published snapshot URLs for file links so the document works outside the checkout. |
| `scripts/render_report.py` | With explicit approval, add presentation-only support for Markdown images/captions, fenced code, landscape pages, correct public author metadata and flexible public-report length. Add `--validation` so new validation can be saved separately. Keep the historical rendering behavior and page limit. |
| `reports/publication-phase-b/public_claim_audit.json` | Refresh current-document hashes and claim locations. All 78 claim values, formatted numbers, evidence pointers and source hashes are unchanged. |
| `reports/final-presentation/*` | Add this explanation, PDF/page review, verification results and artifact hashes. Earlier release and editorial manifests remain unchanged records of their own snapshots. |

The renderer still uses the existing ReportLab workflow and pinned report
dependencies. No experimental module, test, configuration, dataset, source
observation, statistical calculation, figure export or legal notice changed.

## Figures and example

Figures 1-3 are the existing supplementary reviewed plots. Their captions retain
the condition that the AI-assisted proposals are accepted. Figure 4 is the
original natural-source relevance plot. The four original PNGs are embedded
without redrawing, cropping, stretching or changing their pixels. Dense Figures
2 and 3 occupy landscape pages; captions remain attached to their images.

The code example comes from:

`datasets/results/phase3/trials/list_short--specific_first/black/`

Both code blocks match `before.py` and `after.py` exactly, including indentation.
The retained result is Newly hidden with an accepted strict AST gate. Ruff's
visible output contains `missing_b` before formatting and no warning afterward;
ignoring `noqa` reports `missing_a` and `missing_b` in both snapshots. All four
saved lint commands were replayed with the pinned environment and matched the
retained diagnostics after excluding execution filenames. No analyzed program
was executed. This explains one observed mechanism, not its population frequency.

## Targeted prose clarifications

Section 3.2 defines the AST, its field/index paths and warning anchors, then
separates correspondence from visibility classification. It explains why a
type-ignore line field remains in the strict comparison.

Section 3.4 explains whole-group resampling and family incidence, identifies the
purpose of comment-only interventions, and keeps the reviewed results conditional.
Section 4.2 explains the two unsupported constructs without treating ambiguity as
preservation. Section 6 explains exchangeability, completion bounds and the
missing independent labels in ordinary technical language. None of these edits
changes the statistical procedure or resolves an outstanding scientific question.

The final section explains primary observations, bootstrap draws, the numerical
claim ledger and lossless source containers. It names the public repository and
distinguishes offline retained-source checks from full archive reconstruction.
PDF file links are pinned to the published `7c77a230` snapshot; Markdown keeps
portable relative links. All eight reference entries and the AI-assistance
paragraph are unchanged from the baseline.

## Build and checks

In the separate Python 3.12 report environment, with `requirements-report.txt`:

```powershell
python scripts/build_public_docs.py
python scripts/render_report.py --public --validation reports/final-presentation/pdf_validation.json
```

For a later local rebuild, choose an ignored validation destination such as
`local/public-pdf-validation.json` to preserve this review record.

The final report has nine pages. Every page was rendered with Poppler and inspected
individually at 110 dpi, including all tables, chart labels, code indentation,
captions, references and footers. No clipping or overlapping elements were found.
An additional character-bound check found no text outside the body/footer safety
bounds. Four embedded image objects match the original RGB pixels and dimensions.
The author is Abdul Nafeh both visibly and in `/Author` metadata.

All 146 tests passed after the renderer changes. The 78-public/86-historical claim
checks passed. The ambiguity verifier checked 32 comparisons, 1,498 review artifacts
and 840 unchanged original files. Controlled regeneration and saved repeat checks
covered 400 comparisons; the natural checks covered 80 primary/repeat comparisons
and their native-status records. Natural archive-population reconstruction was
explicitly skipped because the archives are absent. This review did not rerun the
full experiment, rebuild archives or generate new statistical estimates.

`pip check`, Black's check on 47 files and Ruff's source check passed. Rendering
the historical report to an ignored temporary destination produced a byte-identical
copy of the frozen PDF. The original PDF was never rewritten.
Rebuilding the public report again also produced a byte-identical copy of the
visually reviewed final PDF.

`verification.json` records the protected-file, link, privacy, claim and image
checks; `artifact_hashes.json` identifies this revision's files. The private
original remains clean at `60d9471e`. Findings, uncertainty, licensing and ownership
are unchanged. No push, publication or history rewrite was performed.
