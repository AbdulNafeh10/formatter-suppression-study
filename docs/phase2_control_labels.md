# Frozen Phase 2 control labels

Labels were established before implementing or running the structural matcher.
The literal expectations in `scripts/prepare_phase2_controls.py` were checked
against raw A/B/C/D diagnostic spans and lexemes, then saved in
`datasets/controls/phase2/manifest.json`. Per-source `independent_review.json`
records give the reviewed warning occurrences, positions and visibility.

All ten controls passed a separate intervention: tokenize identifies COMMENT
tokens and replaces the word noqa with same-length note inside comments only.
The non-comment token sequence and strict AST must stay identical. Ordinary
Ruff on this source must reproduce the original ignore-noqa diagnostics with
the same code, message and coordinates. This evidence is independent of the
structural correspondence algorithm, but is not an independent human review.

## Expectations fixed before classifier execution

| Control | Origin | Expected outcome | Specific evidence |
|---|---|---|---|
| semicolon-black | actual Black output | Newly exposed | missing_a becomes visible when the statements are split |
| semicolon-ruff | actual Ruff format output | Newly exposed | missing_a becomes visible when the statements are split |
| list_inline-black | actual Black output | Newly hidden | missing_b loses visibility when the list collapses |
| list_inline-ruff | actual Ruff format output | Preserved | missing_a stays suppressed and missing_b stays visible |
| import_inline-black | actual Black output | Preserved | path stays suppressed and getcwd stays visible |
| local_semicolon-ruff | actual Ruff format output | Newly exposed | unused local a becomes visible after splitting |
| repeated_name-black | actual Black output | Newly exposed | first missing occurrence becomes visible; second stays suppressed |
| unicode-black | actual Black output | Newly exposed | absent becomes visible; missing stays suppressed |
| manual-hidden | authored directive intervention | Newly hidden | a directive is added to suppress missing_a |
| manual-mixed | authored directive intervention | Mixed | directive coverage switches from missing_a to missing_b |

Manual interventions are not formatter positives. Eight actual formatter controls
come from the saved eight-input/two-formatter discovery probe; all 16 probe
outcomes remain retained, including those not selected as controls. Selection
here exercises validation branches and does not provide a population estimate.
The Unicode probe confirms Ruff 0.11.13 JSON columns count Unicode characters,
whereas Python AST columns count UTF-8 bytes. Exact lexeme extraction was checked
separately against the raw diagnostics before implementing the conversion.

All examples are AI-assisted, synthetic development controls. Labels are never
loaded from classifier predictions. Ground truth is a small development set,
not a held-out accuracy benchmark. No precision, recall or general accuracy claim
is justified. Further independent human and repository validation remain future work.
