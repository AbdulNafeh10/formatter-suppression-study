# Phase A: Scientific integration

Historical checkpoint from the original repository. Current packaging, license
and reproduction status is in [public_snapshot.md](public_snapshot.md).

## 1. Evidence checked

I checked the original report, methods, limitations, related work, AI disclosure,
experiment settings, source templates, test configuration and four figures. The
`START_HERE_FOR_CHATGPT.md` guide is an entry in the earlier project ZIP, not a
file in the repository. It describes commit `0d6b2ab1` and predates the review.

The existing evidence checker passed on all 400 controlled comparisons, 80 natural
comparisons and 66 completed native-configuration checks. It checked source hashes,
formatter output, lint settings, warning records, pairing and outcome arithmetic.
The original controlled and natural metrics were recalculated and matched Phase 5.

The supplementary audit's hashes passed for 840 original files and 1,498 review
artifacts. Its 32 entries cover exactly the originally ambiguous comparisons.
I checked all 128 saved lint replays and 64 comment-intervention results against
their original diagnostic records. No new formatting or lint experiment was run
in Phase A. The separate analysis and its safeguards passed 33 relevant tests.
The full test suite remains a Phase B check; the earlier 126-test result belongs
to Phase 7 and is not a new test count for this revision.

## 2. Supplementary resolutions

All 32 proposed Preserved resolutions are supported by the saved evidence for the
selected Ruff rules. The 16 f-string comparisons have identical source bytes and
unchanged warning visibility. The other 16 change only assignment spacing. Their
F841 warnings still refer to the same exception binding and local assignment.
The original matcher could not handle an identifier inside a Python 3.11 f-string
token or the string-valued `ExceptHandler.name` field.

This is an AI-assisted review using a separate procedure, not independent human
adjudication. Exception-binding judgments still carry the audit's human-review
flag. Standalone comments suppress neither warning in these examples; their
authors' intended scope cannot be inferred from the measured behavior.

I would present these as supplementary results alongside the automatic results.
The detector's original labels should remain unchanged.

| Outcome | Original Black | Original Ruff | Reviewed Black | Reviewed Ruff |
|---|---:|---:|---:|---:|
| Preserved | 116 | 149 | 132 | 165 |
| Newly hidden | 50 | 14 | 50 | 14 |
| Newly exposed | 18 | 21 | 18 | 21 |
| Ambiguous | 16 | 16 | 0 | 0 |

Each column contains 200 comparisons. The reviewed columns depend on accepting
the supplementary proposals. They do not show that the unchanged matcher now
resolves every input or that its accuracy has been independently measured.
The formatter difference describes this fixed suite, not general superiority.

## 3. Supplementary calculations

Confirmed changes remain 68/200 for Black and 35/200 for Ruff, or 34.0% and 17.5%.
The original complete-pair comparison used 184 inputs and gave a difference of
17.93 percentage points. With the review applied to all 200 pairs, the difference
is 33/200 = 16.50 points. Its paired table is [[132, 0], [33, 35]], with Black on
rows, Ruff on columns and no-drift/drift as the two states. Hiding and exposure
differences are 18.00 and -1.50 points, respectively.

The intervals were recalculated rather than copied. Whole-family resampling now
uses 25 families and gives a 95% model interval of 8.00 to 25.50 points for the
difference. Category resampling uses 13 categories and gives 4.89 to 30.29 points.
Both use 20,000 paired cluster draws and the original seed conventions. The two
boundary families share one category, so the category count rises from 12 to 13.

Family-incidence Wilson calculations now use 15/25 families for Black and 12/25
for Ruff. Their model intervals are 40.74%-76.60% and 30.03%-66.50%. These concern
whether a family has any drift, not the rate across individual inputs. All these
intervals are exploratory and conditional on the review and cluster assumptions.
Related, deliberately constructed templates are not random Python projects.

The original unresolved-outcome bounds remain valid for the automatic results.
Assigning the reviewed cases to Preserved makes those completion ranges single
values in the supplementary calculation. This does not remove review error or
make them confidence intervals. The original bounds should remain available.

The overlay, paired rows, group tables, draws, metrics, input hashes and verification
records are in `reports/publication-phase-a/analysis`. The overlay keeps the original
classification in a separate column. In these supplementary tables, resolved or
attributable means resolved conditional on the review, not by the original matcher.
Other affected summaries were recalculated too: changed outputs classified as
Preserved become 65 for Black and 83 for Ruff, compared with the original 57 and
75. These must not be mixed with the old resolved-case summaries in the new draft.

## 4. Natural-source findings and remaining concerns

Natural-source results are unchanged: no confirmed drift in 80 comparisons.
There were 65 unchanged outputs and 15 changed outputs. Twenty-two of the 40
original files had no underlying warnings from the selected rules, corresponding
to 44 comparisons. Four comparisons still fail the strict AST gate because of
`TypeIgnore.lineno` changes. The ambiguity audit does not resolve those exclusions.
These facts limit what the negative result can establish.
Only F401/F821/F841 and the saved Windows/Python 3.11 environment were tested;
the archived native configurations do not reproduce full project CI.

The report says the natural repeat sample contained only unchanged outputs. That
describes Phase 4, but Phase 7 later repeated all 80 comparisons, including all 15
changed outputs. The revised report should distinguish those checkpoints. The
limitations document has the same historical qualification to add. Reproduction
does not supply independent warning labels or additional independent samples.

The related-work claims remain narrow: suppression evolution, warning tracking and
differential testing provide context; formatter/comment interaction was already
documented. The source recheck is in `reports/publication-phase-a/literature_check.md`.
No original paper's performance numbers should be used as this detector's accuracy.

## 5. Figure plan

1. Keep Figure 1 unchanged. Add a supplementary outcome plot showing original and
   reviewed controlled counts on the same 200-input denominators. Natural panels
   do not change. This is a possible single README figure.
2. Add a supplementary Figure 2 with 25 family profiles, the 200-pair table and
   newly calculated intervals. Keep the original 184-pair figure and caption.
3. Add a supplementary Figure 3. The boundary-category cells become reviewed 0/2
   instead of unresolved U2; other counts stay the same. Label the review clearly.
4. Reuse Figure 4 without changing its natural-file counts or interpretation.

New figure files should go under `reports/figures-reviewed`, with both PNG and SVG
exports. No figures were created or replaced in Phase A.

## 6. Repository and writing plan

After approval for Phase B, prepare a 400-650 word README with one figure. Write
a new `report/research_report_public.md` and corresponding PDF, keeping the original
report, template, claim ledger and PDF at their existing paths. Use the requested
eight numbered sections, ordinary language and first-person singular where it
describes actual work. Keep one short AI-use note. Add claim bindings for the new
draft and perform a separate paragraph-by-paragraph writing audit.
The public template, claim specification and ledger should be separate files.
The report builder and renderer will need explicit input/output options or separate
entry points; their existing defaults must still reproduce the original report.

Before Phase A, the repository had 33,737 tracked files totaling 139,885,480 bytes.
The largest file is 4,689,873 bytes; repeated evidence contributes to the file count.
Do not delete canonical evidence or rewrite historical commits to reduce size.
Public documentation can link to the main sources, review and reproduction records
without reproducing every phase handoff on the landing page.

There is no root project LICENSE. A license choice and third-party notice review
are still needed before publication. Upstream license files are retained, including
separate notices inside the Requests archive; the top-level license should not be
assumed to cover every archived component. Raw records contain local Windows paths.
Keep their bytes intact, use relative links in new prose, and review publication
of those paths in Phase C. This is an inventory, not a completed release audit.

Phase B should run the existing suite and relevant integrity checks after drafting.
Phase C still needs explicit approval, a license/provenance review, private-file
and size checks, and verification of the approved GitHub upload. Nothing has been
published. Phase A stops here.
