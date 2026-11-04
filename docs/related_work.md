# Related work

This is a targeted review of suppression behavior, warning correspondence and
differential testing, not a systematic search or a claim of priority.

Hu, Wang, Rubin and Pradel's *An Empirical Study of Suppressed Static Analysis
Warnings* studies suppression mapping and evolution, including line-splitting
effects ([2025, DOI](https://doi.org/10.1145/3715729),
[published author text](https://software-lab.org/publications/fse2025_suppressions.pdf)).
Its longitudinal setting differs from the isolated formatter intervention here.
The final author text and retained metadata govern the citation; the supplied
draft contains publication placeholders.

Li and Yang's *Tracking the Evolution of Static Code Warnings: The State-of-the-Art
and a Better Approach* shows why warning identity across revisions needs more
than location matching ([TSE 50(3), 534-550, 2024](https://doi.org/10.1109/TSE.2024.3358283),
[author text](https://jinqiuyang.github.io/papers/staticdiff-tse24.pdf)). This study's
AST-stable, three-rule matcher addresses a restricted case. It is not a new
general warning tracker, and that paper's accuracy figures do not validate it.

McKeeman's *Differential Testing for Software* provides the comparison principle
([Digital Technical Journal 10(1), 100-107, 1998](https://vmssoftware.com/docs/dtj-v10-01-1998.pdf)).
Here, formatter disagreement helps locate cases to inspect. Agreement alone
does not show that suppression or warning identity is correct.

## Tool documentation and scope

Black's [25.1.0 FAQ](https://github.com/psf/black/blob/25.1.0/docs/faq.md)
discusses moved lint directives. Ruff's
[0.11.13 deviations from Black](https://github.com/astral-sh/ruff/blob/0.11.13/docs/formatter/black.md)
documents suppression broadening when a list collapses. The general interaction
was already known. Ruff's [pragma-comment discussion](https://github.com/astral-sh/ruff/discussions/6670)
is useful design history, not an empirical evaluation.

The retained contribution is a paired, inspectable experiment with explicit
unresolved cases and a separate negative natural-source sample. Neither the
literature search nor the sample establishes novelty priority or ecosystem rates.
Independent detector accuracy remains unmeasured.

[NIST's Wilson guidance](https://www.itl.nist.gov/div898/handbook/prc/section2/prc241.htm)
and [Stata's bootstrap manual](https://www.stata.com/manuals/rbootstrap.pdf)
support the statistical formulas and resampling principles. They do not justify
exchangeability of the authored templates. Calculations used NumPy, not Stata.

## Access records

The 2026-11-03 checks are recorded in
`reports/phase6/literature_access.json` and
`reports/phase6/documentation_sources.json`, with retained Crossref payloads.
They distinguish retrieved sources from blocked publisher access. Relevant
passages were reviewed; independent replication and an exhaustive full-text
review are not claimed. Current web documentation is background; pinned help
and executed commands determine the experimental options.

<details>
<summary>Historical Phase 1 documentation review (unchanged)</summary>

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

</details>
