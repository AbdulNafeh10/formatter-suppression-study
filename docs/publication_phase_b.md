# Phase B: Public drafts prepared

Historical checkpoint from the original repository. Current packaging, license
and reproduction status is in [public_snapshot.md](public_snapshot.md).

Phase B is complete for author review. Nothing was published or pushed, and Phase C
has not started.

## Files

- [README](../README.md): 504 words excluding its code block, with one figure.
- [Public report](../report/research_report_public.md) and
  [PDF](../report/research_report_public.pdf): eight numbered sections, six rendered
  pages, and separate original and supplementary results.
- [Supplementary figures](../reports/figures-reviewed/captions.json): three PNG/SVG
  pairs with captions, plotted values and provenance. Original figures remain intact.
- [Reproduction instructions](reproducibility.md), [AI-use note](ai_use.md), and
  [release review](release_review.md).

The original report, template, claim ledger, figures, data, labels, experiment
configuration and analysis were not replaced. The earlier README and AI disclosure
are retained in docs/history. Detailed protocols and phase records remain available;
the landing page no longer lists the full development chronology.

## Writing and measurements

The new prose starts with the research question and uses first-person singular
where it describes actual work. The report explains the four passes, AST gate and
warning matching without a general introduction to software development. Results
state measurements before interpretation. Discussion names the observed layout
patterns and the limits of the natural sample. AI assistance is disclosed briefly.

A separate sentence-level editing pass removed jargon and vague statements,
clarified the proposed follow-up sample and retained the denominators. Its record
is in `reports/publication-phase-b/writing_audit.md`; paragraph hashes are in
paragraph_review.json. No text was copied from the historical student thesis used
for an organizational comparison. No AI-detector scoring was used.

The public documents have 78 evidence-bound claims. Unbound protocol constants,
zero-outcome statements, examples and references were reviewed separately in
manual_claim_review.md. The original report still passes its own 86-claim check.
The controlled counts remain 68 Black changes and 35 Ruff changes among 200 inputs
per formatter. Reviewed Preserved counts are labeled as AI-assisted proposals.
The natural negative result retains unchanged-output counts, warning relevance and
the strict AST exclusions. No precision/recall or ecosystem prevalence is claimed.

## Executed checks

The full suite passed: 139 tests, no failures or errors. Ruff and Black checks pass
for the implementation. The supplementary analysis was reproduced into a fresh
directory; all eleven numeric/evidence/CSV artifacts matched Phase A exactly.
Both bootstrap draw sets and their metrics remain separate from the original
184-pair analysis. All three supplementary PNG/SVG pairs, captions and plotted
values reproduced byte-for-byte.

All final PDF pages and all three figures were visually inspected. No clipping,
overlap or unreadable glyphs were found. The renderer gained a `--public` option;
its existing defaults were retained. Rendering the original report to a temporary
file produced the exact preserved original PDF bytes. No canonical PDF was
overwritten by that check. Public links and figure/table denominators were checked.

Records are under `reports/publication-phase-b`, including pytest.xml,
verification.json, public_claim_audit.json and pdf_validation.json. Canonical raw
evidence was audited through the reviewed-analysis reproduction, not recollected.
The earlier full experiment reruns remain the Phase 7 evidence. A clean-machine
installation and another operating system remain untested.

## Remaining release decisions

There is still no project license. MIT, BSD-3-Clause and Apache-2.0 are listed as
options for original material the author can license; no terms were invented or
applied to third-party material. Separate upstream notices, particularly the
Requests archive's ext and theme material, need review before publication.

The file scan found four private-key headers in Requests' archived certificate
test fixtures. Their test provenance was checked without copying key values into
the report. Raw evidence also contains local Windows paths. These findings are
documented, not silently deleted or marked as approved for publication. The exact
approved public file set and full Git history still require a Phase C check.
Ignored environments/caches were not added, and canonical evidence was not removed
to reduce size.

The author should review the actual drafts and choose how to handle those release
issues before approving Phase C. No remote repository was created or changed.
