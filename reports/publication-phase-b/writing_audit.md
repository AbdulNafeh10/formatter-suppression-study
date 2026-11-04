# Separate writing review

The editing pass covered the README and public report after the first draft was
generated. Each prose paragraph was checked sentence by sentence for a clear
purpose, evidence, ordinary wording, unnecessary repetition and accurate use of
first-person singular. The original report was not edited.

## Changes made in the editing pass

- Replaced "all-scheduled proportions" with "Across all scheduled comparisons,
  the rates were". The denominator stays explicit without introducing a label
  the reader has to decode.
- Changed the template description to "I used ... source templates, each with ...
  directive modes". This describes the actual construction without a generic
  introduction to experimental design.
- Removed a vague claim about a "more complete description" and named the two
  matcher gaps instead.
- Made the proposed natural-source follow-up concrete: define a separate sample
  with selected warnings and changed formatter output, then limit conclusions to
  that sample. No history of prior project formatting was invented.
- Replaced an indirect statement about human-adjudication uncertainty with the
  specific limitation that intervals do not account for errors in the AI-assisted
  review.
- Avoided starting the natural-relevance sentence with a bare digit. Count and
  denominator remain bound to the evidence.
- Added the total controlled comparison count so the reader need not infer it
  from the input count and formatter pairing.
- Expanded AST at its first README mention so the method does not assume that
  every reader already knows the abbreviation.

## Paragraph purposes

The introduction starts with the actual question, explains a directive's effect
and distinguishes the two datasets. Related work states the different settings
of suppression research, warning tracking and differential testing; the existing
formatter documentation prevents a novelty claim. Methods explain why four lint
passes, AST comparison and occurrence matching were needed, then describe input
selection and the later review.

Results begin with measurements. The automatic and reviewed columns are separate,
as are scheduled and resolved denominators. The short-list and semicolon examples
describe retained source transformations. Natural-source exclusions, empty warning
sets and unchanged outputs remain visible. The Phase 4 repeat limitation is put
in its historical context, followed by the completed Phase 7 reproduction.

Discussion separates observations from possible explanations and identifies what
would change in another repository study. Limitations concern this experiment's
templates, sampling, rules, AST gate, review process and environment. The conclusion
states the controlled finding and natural negative result, then gives a short list
of extensions. It does not claim a breakthrough, validated developer tool or
publication status.

The README gives navigation and a short explanation rather than duplicating the
report. Its one figure labels supplementary counts. AI assistance is disclosed
briefly; the report has one methods paragraph for that disclosure. Repeated
references to the AI-assisted review identify a result's provenance rather than
repeat a general authorship statement.

## Historical comparison and checks

For organization, the comparison used the contents and methods/results separation
in Faisal Irfan Yar Khan's 2017 University of Washington student thesis,
[*Effects of Peer Feedback on Password Strength*](https://digital.lib.washington.edu/researchworks/bitstreams/f3d9f0b3-aee4-4392-bb96-9c9cec2e1386/download).
That is a master's thesis, not a small undergraduate report. Its length, topic,
claims and wording were not adopted. The public draft uses conventional numbered
sections at the shorter length requested here. No text was copied from it.

Automated checks enforce ASCII punctuation, no team "we", resolved claim markers
and README length. Manual review covers meaning, paragraph usefulness, protocol
constants and citations. There was no AI-detector scoring or attempt to disguise
assistance. Human author review is still needed; these checks do not certify
personal authorship or independent scientific validity.
