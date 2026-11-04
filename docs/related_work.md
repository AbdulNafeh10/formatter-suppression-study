# Verified related work - Phase 6

Accessed 2026-11-03 UTC. This targeted review follows the supplied references,
warning correspondence, and differential testing. It is not a systematic search
or evidence of priority. The historical Phase 1 review below is retained; its
pending-review statements are superseded by this section. Searches used the
supplied title, suppression/formatter interactions, warning tracking and
differential testing. Primary sources support the report.

## Research literature reviewed

- Huimin Hu, Yingying Wang, Julia Rubin and Michael Pradel,
  *An Empirical Study of Suppressed Static Analysis Warnings*, PACMSE 2(FSE),
  290-311 (2025), [DOI](https://doi.org/10.1145/3715729).
  The [supplied draft](https://people.ece.ubc.ca/mjulia/publications/Suppressed_Static_Analysis_Warnings_FSE2025.pdf)
  and [published author PDF](https://software-lab.org/publications/fse2025_suppressions.pdf)
  were retrieved. Relevant passages on suppression mapping, evolution and line
  splitting were reviewed. Their longitudinal setting differs from our isolated
  formatter intervention. Draft footer placeholders differ from final metadata;
  the author PDF and retained Crossref record govern the citation. ACM landing
  access was blocked; publisher-fulltext access and replication are not claimed.
- Junjie Li and Jinqiu Yang, *Tracking the Evolution of Static Code Warnings:
  The State-of-the-Art and a Better Approach*, IEEE TSE 50(3), 534-550 (2024),
  [DOI](https://doi.org/10.1109/TSE.2024.3358283).
  [Author PDF](https://jinqiuyang.github.io/papers/staticdiff-tse24.pdf) abstract,
  motivating examples and tracking discussion were reviewed; metadata was checked
  against Crossref. Matching warnings across revisions is an established problem.
  Our AST-stable, rule-restricted oracle is not a new general warning tracker.
  Published performance figures are not transferred to this detector.
- William M. McKeeman, *Differential Testing for Software*, Digital Technical
  Journal 10(1), 100-107 (1998).
  [Original journal PDF](https://vmssoftware.com/docs/dtj-v10-01-1998.pdf), PDF page
  103 / printed page 100, was reviewed for the comparison principle and metadata.
  Disagreement identifies candidates requiring interpretation. Our visibility
  property differs from formatter output equality; agreement is not correctness.

## Versioned documentation and originality limits

Black's [25.1.0 FAQ source](https://github.com/psf/black/blob/25.1.0/docs/faq.md)
was fetched to verify relevance to the pin. Ruff's [0.11.13 deviations source](https://github.com/astral-sh/ruff/blob/0.11.13/docs/formatter/black.md)
documents suppression broadening when a list collapses; the
[current page](https://docs.astral.sh/ruff/formatter/black/) was also consulted.
These references establish prior awareness, not measured prevalence.
MichaReiser's [Pragma comment handling discussion #6670](https://github.com/astral-sh/ruff/discussions/6670),
dated 18 August 2023, was read as design history, not a peer-reviewed evaluation.

The contribution is the retained paired experiment and separate negative natural
validation with explicit exclusions. Independent detector accuracy and broad
population estimates remain open. Related-work coverage cannot establish
originality priority. Search leads such as ViolationTracker were not used for
technical conclusions because their full methods were not reviewed here.

`reports/phase6/literature_access.json` records PDF/metadata URLs, lengths and
hashes. Crossref payloads are retained. `reports/phase6/documentation_sources.json`
records pinned-document hashes and review scope. Temporary copies are excluded
from Git; primary-source links remain available. Access, relevant-passage reading
and independent replication are distinct. This was not an exhaustive full-text
review of every cited paper.

Statistical method references remain [NIST's Wilson guidance](https://www.itl.nist.gov/div898/handbook/prc/section2/prc241.htm)
and [Stata's bootstrap manual](https://www.stata.com/manuals/rbootstrap.pdf).
They support formulas and resampling principles, not exchangeability of our data.

## Historical Phase 1 documentation review

Accessed 2026-11-03 UTC. This is a tool-documentation review; systematic literature
verification and the research report belong to Phase 6.

## Established knowledge

[Black current style](https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html)
describes wrapping and comment relocation, including limitations of AST checks.
[Black FAQ](https://black.readthedocs.io/en/latest/faq.html) explicitly discusses
lint directives being moved and the possibility of needing to reposition them.
These pages already establish the general interaction; we claim no discovery of it.

[Ruff linter documentation](https://docs.astral.sh/ruff/linter/) describes rule
selection, noqa suppression, and diagnostic exit statuses.
[Ruff formatter documentation](https://docs.astral.sh/ruff/formatter/) describes
formatting and interaction with lint rules. Current web documentation can describe
features newer than our pins; installed tool help and actual integration tests
are the authority for the options used here. No newer suppression syntax is tested.

## Narrower question and potential contribution

The prospective contribution is a controlled, paired measurement of suppression
coverage using underlying-diagnostic checks and independently validated matching,
followed by separate real-world validation if available. No empirical contribution
or detector accuracy is established by the Phase 1 smoke experiment.

## Literature still to review

The brief supplied
[a suppressed-warning study PDF](https://people.ece.ubc.ca/mjulia/publications/Suppressed_Static_Analysis_Warnings_FSE2025.pdf).
It has **not** been reviewed in Phase 1; author names, title, venue and findings
are not asserted here. Verify bibliographic details and review accessible content
in the literature phase, together with formatter/directive interactions and
differential-testing research. No originality conclusion follows from this
limited documentation review.
