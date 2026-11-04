# Literature recheck for Phase A

The existing citations were checked against the retained bibliographic records,
accessible primary papers and documentation pinned to the tested tool versions.
This was a targeted recheck, not a new systematic literature review.

- Hu, Wang, Rubin and Pradel's 2025 suppression study addresses warning suppression
  and evolution. Section 3.4 excludes line-splitting cases that change warning
  counts without introducing a new warning. It is not the Black/Ruff benchmark
  conducted here. The published author text identifies PACMSE 2(FSE), article
  FSE014; retained Crossref metadata gives pages 290-311 and an online date.
  These are different metadata conventions, not different papers. Use the DOI and
  one consistent final citation style in the new report. [Published author text](https://software-lab.org/publications/fse2025_suppressions.pdf),
  [DOI](https://doi.org/10.1145/3715729).
- Li and Yang's warning-tracking paper supports the need to establish warning
  correspondence. Its reported tracking performance does not measure this
  project's detector. Author names/title were rechecked in the primary text;
  the retained Crossref record supplies TSE 50(3), 534-550 (2024).
  [Author text](https://jinqiuyang.github.io/papers/staticdiff-tse24.pdf),
  [DOI](https://doi.org/10.1109/TSE.2024.3358283).
- McKeeman's *Differential Testing for Software*, Digital Technical Journal 10(1),
  100-107 (1998), remains methodological context. The retained original-journal
  extraction was checked. Disagreement suggests a case to investigate; it does
  not by itself prove a formatter defect. [Original journal](https://vmssoftware.com/docs/dtj-v10-01-1998.pdf).
- Black's pinned FAQ states that comments affecting linters may move. Ruff's
  pinned deviations document gives an example where moving `noqa` broadens its
  coverage after a list collapses. Both versioned sources were fetched again
  through the connected GitHub reader. The direct web fetch failed for these
  raw URLs, so that failure is not treated as successful access.
  [Black 25.1.0 FAQ](https://github.com/psf/black/blob/25.1.0/docs/faq.md),
  [Ruff 0.11.13 deviations](https://github.com/astral-sh/ruff/blob/0.11.13/docs/formatter/black.md).

No source checked here establishes novelty priority for this project. The concise
public related-work section should explain the different settings rather than
claim that earlier work studied this specific experiment. NIST's Wilson guidance
and the Stata bootstrap manual remain method references in the original analysis;
they do not establish independence or population coverage for these templates.
