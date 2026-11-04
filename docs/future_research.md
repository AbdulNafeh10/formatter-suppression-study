# Future research opportunities

These are proposals, not completed experiments. They require new protocols and
separate evidence; none changes this pilot's primary labels or denominators.

| Priority | Question | Proposed design | Evidence needed before a stronger claim |
|---|---|---|---|
| Independent accuracy | Does correspondence recover the intended warning identity? | Held-out changed/unchanged pairs labeled by independent reviewers, with disagreements adjudicated without oracle output | False positives/negatives, precision/recall with uncertainty, clear treatment of abstention |
| Natural relevance | Does drift occur where selected warnings are present? | Prospectively define a warning-relevant natural stratum separately from an unfiltered sample; retain all eligibility and exclusion counts | Rates within the defined frame; no extrapolation from a selected positive corpus |
| Versions and configurations | Which observations persist across releases and settings? | Pin a prospective version/configuration matrix; pair identical inputs and separate linter from formatter changes | Raw outputs and version-specific correspondence, not an assumption that newer is better |
| AST representation | Can type-ignore position metadata be handled more informatively? | Specify a secondary gate prospectively; compare strict and narrowly normalized representations | Independent review of executable syntax, type-checker effects and changes to exclusion rates |
| Matching coverage | Can f-string and exception-binding ambiguity be reduced safely? | Add new anchors against independent examples, then evaluate on held-out inputs | Coverage gains plus error/abstention analysis; no automatic conversion of unknowns to negatives |
| Broader inference | How frequent are changes in a defined population? | Establish a repository/file sampling frame and dependence-aware analysis before collection | Design-based or justified model-based inference with diagnostic relevance and nonresponse accounted for |

Prioritize independent adjudication before presenting the oracle as a developer
check with useful accuracy. The negative natural result warrants stronger sampling
and relevance analysis, not replacement of sampled files with favorable examples.
More variants of the same authored templates do not establish independent support.
Generalization to other languages, linters or runtime semantics remains untested.
