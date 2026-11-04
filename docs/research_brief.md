# CODEX RESEARCH BRIEF
## Code Formatting and Linter Suppressions

You are my research engineering partner for an independent empirical software engineering project.

I want you to build, execute, test, analyze, and document a complete, reproducible research study.

**IMPORTANT: Read this entire brief, but DO NOT attempt to implement the entire project in one run.**

Work in clearly separated, independently testable phases. Execute only the currently authorized phase, complete and validate it, summarize the results, and STOP. Wait for my explicit instruction to continue before starting the next phase.

The objective is to produce a scientifically defensible research project while minimizing unnecessary computation, model usage, repeated work, and context consumption.

Do not create speculative features or elaborate architecture beyond what is required.

Never fabricate experimental results, measurements, citations, source repositories, or successful tests.

---

# 1. PROJECT IDENTITY

**Research title:** Code Formatting and Linter Suppressions

**Repository:** `formatter-suppression-study`

**Language:** Python

**Primary tools:** Black, Ruff, pytest, Python AST, tokenize, Git

**Analysis:** pandas, NumPy, SciPy where justified, matplotlib

**Research area:** Software engineering, static analysis, developer tools, automated testing.

Avoid artificial product branding, promotional language, unnecessary AI features, or exaggerated claims.

The goal is a clean research repository, a reproducible experimental framework, real measurements, and a concise academic report suitable for showcasing in a graduate Computer Science application.

# 2. CENTRAL RESEARCH QUESTION

**Can automated Python code formatting change which static-analysis warnings are suppressed, even when the program's executable syntax remains unchanged?**

Automated formatters rearrange code and associated comments.

Python linters support suppression directives such as:

`# noqa: F821`

These directives influence which diagnostics are reported.

If formatting changes the position or effective scope of such directives, a linter may suppress additional warnings or expose previously ignored warnings.

We want to determine whether this happens, under what conditions, and whether such changes can be detected reliably.

We are not claiming to have discovered this general possibility.

Our contribution should be the controlled empirical investigation, reproducible evidence, careful measurement, and independently validated detection method.

# 3. RESEARCH QUESTIONS

Define these questions before collecting results.

**RQ1 — Suppression preservation**

Under what tested conditions does automatic Python formatting preserve or change the effective suppression of static-analysis diagnostics?

**RQ2 — Failure characteristics**

When suppression behavior changes, does formatting:

- Hide additional warnings?
- Expose previously suppressed warnings?
- Relocate directives without changing effective suppression?
- Change underlying diagnostics independently of suppression behavior?

**RQ3 — Formatter comparison**

How do Black and Ruff's formatter behave on identical controlled inputs under the same linting conditions?

Do not assume either formatter performs better.

**RQ4 — Real-world relevance**

Do changes observed in controlled examples also appear in naturally occurring Python source files from public repositories?

**RQ5 — Detection feasibility**

Can an automated comparison identify verified suppression changes with sufficiently low false-positive and false-negative rates to be useful as a developer check?

Treat RQ5 as an extension if there are insufficient independently verified examples.

# 4. SCIENTIFIC PRINCIPLES

These requirements override implementation convenience.

1. Establish hypotheses, definitions, inclusion criteria, and analysis rules before the main experiment.
2. Separate actual observations from expectations.
3. Preserve raw inputs, outputs, and tool configurations.
4. Record failed, invalid, excluded, and inconclusive trials.
5. Never cherry-pick successful examples.
6. Never substitute synthetic data for real-world evidence.
7. AST equivalence is a syntactic-preservation check, not proof of universal runtime semantic equivalence.
8. Never classify warnings as newly hidden merely because their line numbers changed.
9. Never attribute an underlying diagnostic change to suppression movement without independent evidence.
10. Never claim unprecedented originality without supporting literature.
11. Do not change experimental criteria after seeing the results unless clearly documented as exploratory analysis.
12. A negative result is a valid scientific outcome.

If no formatter-induced suppression changes are found, report that accurately.

# 5. RELATED WORK

Inspect and document relevant prior work.

Start with:

**Black code style:**
https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html

**Black FAQ:**
https://black.readthedocs.io/en/latest/faq.html

**Ruff linter documentation:**
https://docs.astral.sh/ruff/linter/

**Ruff formatter documentation:**
https://docs.astral.sh/ruff/formatter/

**Empirical study of suppressed static-analysis warnings:**
https://people.ece.ubc.ca/mjulia/publications/Suppressed_Static_Analysis_Warnings_FSE2025.pdf

Look for additional studies concerning formatter-induced directive movement, suppression changes, static-analysis interactions, and differential testing.

Verify bibliographic information from accessible sources.

Create `docs/related_work.md`, documenting:

- Established knowledge
- Existing research
- Our narrower research question
- Potential contribution
- Limitations on originality claims

Do not present inaccessible papers as though they were reviewed.

# 6. EXPERIMENTAL FRAMEWORK

Implement the following pipeline:

Original Python file
→ baseline diagnostics
→ automated formatting
→ formatted diagnostics
→ independent suppression-effect analysis
→ classification
→ reproducible evidence record.

Preserve both original and transformed source files.

## 6.1 Reproducible environment

Create an isolated Python environment.

Pin exact compatible versions of required dependencies.

Record:

- Operating system
- Python version
- Black version
- Ruff version
- Commands and configurations
- Formatter exit status
- Random seeds
- Repository commit identifiers

Use a controlled baseline lint configuration.

Verify command-line options and tool compatibility before relying on them.

## 6.2 Controlled input generation

Generate valid Python source examples covering:

- Function calls
- Lists, tuples, and dictionaries
- Multiline expressions
- Nested expressions
- Function definitions
- Imports
- Comprehensions
- Long expressions triggering wrapping
- Conditional expressions
- Multiple statements
- Trailing and standalone comments

Cover suppression types including:

- `# noqa: CODE`
- Multiple rule codes
- Blanket `# noqa`
- Different valid directive placements
- Multiple potential diagnostics

Use a small, well-understood subset of stable Ruff diagnostic rules.

Create positive and negative controls.

**Positive controls** must be based on independently reproducible, real tool behavior. Do not invent positive examples to satisfy a target.

**Negative controls** should verify that valid transformations preserving suppression behavior are correctly classified.

## 6.3 AI-assisted test generation

AI coding tools may assist in generating candidate stress-test inputs.

This is an intentional part of the methodology.

However, test generation and validation must be separate.

Every generated candidate must pass appropriate checks for:

- Python syntax validity
- Experimental relevance
- Duplicates
- Formatter compatibility
- AST preservation where required
- Reproducibility

Record generation methods and random seeds.

Save generation specifications.

Explicitly distinguish AI-assisted controlled examples from naturally occurring source code.

# 7. VALIDATION ORACLE — CRITICAL

The study must distinguish real suppression changes from line-number changes and unrelated diagnostic differences.

Implement four diagnostic passes for each source transformation.

**A. Original code, normal linting**

Run Ruff with `noqa` directives respected.

**B. Original code, suppression disabled**

Run Ruff with `--ignore-noqa`.

**C. Formatted code, normal linting**

Run Ruff with `noqa` directives respected.

**D. Formatted code, suppression disabled**

Run Ruff with `--ignore-noqa`.

Use structured JSON diagnostic output.

Conceptually:

- Underlying diagnostics = diagnostics with `noqa` ignored.
- Visible diagnostics = diagnostics with `noqa` respected.
- Suppressed diagnostics = matched underlying diagnostics absent from visible diagnostics.

**Diagnostic identity must not depend solely on line numbers.**

Implement matching based on:

- Diagnostic rule identifier
- Relevant AST node or source construct
- Normalized code context
- Stable structural location when possible
- Unambiguous occurrence identity

Use AST, tokenization, and contextual matching where appropriate.

If the correspondence cannot be established reliably, classify the result as ambiguous.

Before attributing changes to suppression movement, confirm that relevant underlying diagnostics match across the formatting transformation.

Record underlying diagnostic changes separately.

## 7.1 Classification

Each trial must receive one of these classifications:

- **Preserved:** underlying diagnostics and effective suppression coverage unchanged.
- **Newly hidden:** a matched previously visible diagnostic becomes suppressed.
- **Newly exposed:** a matched previously suppressed diagnostic becomes visible.
- **Mixed:** both newly hidden and newly exposed diagnostics occur.
- **Diagnostic changed:** underlying unsuppressed diagnostics differ.
- **AST changed:** required AST equivalence fails.
- **Ambiguous:** correspondence cannot be established reliably.
- **Execution failure:** required tool execution fails.

Record unchanged formatting outputs separately so they do not distort statistics about transformed files.

Preserve every exclusion.

# 8. EXPERIMENTAL DATASETS

## Dataset A — Controlled stress tests

Target at least 200 distinct, valid controlled input cases.

Test the same cases using Black and Ruff where supported.

This produces a target of approximately 400 formatter comparisons.

These numbers are targets, not results.

Cover meaningful syntactic diversity rather than generating hundreds of superficial variations.

Use reproducible seeds and save inputs.

Validate the diagnostic comparison system before launching the main experiment.

## Dataset B — Real-world repository validation

Select at least three public Python repositories if accessible.

Document:

- Selection criteria
- Repository URLs
- Commit hashes
- Eligible source-file population
- Sampling procedure
- Exclusions
- Formatter and linter configurations

Prioritize repositories naturally containing `# noqa` directives.

Exclude generated and vendored files.

Run transformations in temporary copies.

Where possible, distinguish standardized lint-configuration results from project-native configuration results.

Do not imply a repository uses Ruff simply because our study analyzed it with Ruff.

If repository access is unavailable, complete the controlled study and document real-world validation as incomplete.

Never merge synthetic and real-world prevalence estimates.

# 9. METRICS

Report:

**Primary outcomes**

- Valid comparisons
- Changed suppression coverage
- Newly hidden diagnostics
- Newly exposed diagnostics
- Proportions for each outcome

**Secondary outcomes**

- Number of affected diagnostics
- Outcome rates by formatter
- Outcome rates by syntax category
- Outcome rates by suppression type
- Ambiguous classification rate
- AST-equivalence failures
- Formatting changes without suppression changes

**Detector evaluation**

Only with independently labeled ground truth:

- True positives
- False positives
- False negatives
- True negatives
- Precision
- Recall
- F1 score

Never evaluate the detector using labels produced solely by the same logic being evaluated.

Use Wilson 95% confidence intervals where appropriate.

Account for paired formatter comparisons.

Do not assume correlated generated inputs or files from the same repository are independent observations.

Report per-repository findings separately where appropriate.

Avoid unsupported causal or superiority claims.

# 10. DATA RECORDING

Each trial record should include:

- Trial ID
- Dataset origin
- AI-assisted generation flag
- Input family
- Repository and commit
- Formatter and version
- Linter and version
- Configuration
- Input checksum
- Output checksum
- Formatting-change status
- AST equivalence
- Original underlying diagnostics
- Formatted underlying diagnostics
- Original visible diagnostics
- Formatted visible diagnostics
- Matched diagnostic identities
- Newly hidden count
- Newly exposed count
- Classification
- Validation status
- Error details
- Evidence paths

Export CSV and JSONL.

Preserve source files, diagnostics, configurations, and transformation outputs.

Every claimed finding must be individually reproducible.

# 11. COMMAND-LINE TOOL

Implement a lightweight Python CLI.

Primary commands:

`python -m suppression_study compare before.py after.py`

`python -m suppression_study experiment --config configs/pilot.toml`

Optionally support analyzing a file using a selected formatter.

Report:

- AST-preservation status
- Suppression-behavior status
- Matched affected diagnostics
- Classification explanation
- Evidence location

Use meaningful exit codes.

Keep analysis errors distinct from confirmed suppression drift.

Never execute arbitrary analyzed Python programs simply to collect lint results.

Use bounded subprocess execution and temporary directories.

# 12. AUTOMATED TESTS

Build a proper pytest suite covering:

- Input validation
- Directive handling
- Formatter integration
- Ruff JSON parsing
- Diagnostic matching
- AST comparison
- Outcome classification
- Ambiguous findings
- Subprocess failures
- Unicode input
- Repeated diagnostics
- Dataset generation
- Result export
- Reproducibility

Include end-to-end integration tests using actual pinned formatter and linter versions.

Synthetic unit-test results must not be presented as empirical research findings.

# 13. ANALYSIS AND VISUALIZATION

Generate academic-quality figures from actual data.

Target:

**Figure 1 — Outcome distribution**

Suppression outcomes, ambiguity, and exclusions.

**Figure 2 — Formatter comparison**

Paired comparison of Black and Ruff.

**Figure 3 — Structural patterns**

Outcomes by syntax category or suppression pattern.

If a planned figure is unsupported by observed data, substitute a more informative analysis.

Use descriptive captions, clearly labeled axes, denominators, and appropriate uncertainty.

Export PNG and SVG.

Do not generate fake or decorative data.

# 14. OPTIONAL RESULTS EXPLORER

Only implement after experimental work is complete.

Create a lightweight static HTML explorer or simple Streamlit interface.

Allow users to:

- Filter by outcome
- Compare before/after code
- Inspect affected diagnostics
- Examine evidence
- Open preserved experimental files

The research must remain usable without the interface.

# 15. RESEARCH REPORT

Create:

`report/research_report.md`

Target approximately 4–6 pages of substantive content when rendered.

Sections:

1. Abstract
2. Introduction
3. Related work
4. Research questions
5. Methodology
6. Results
7. Discussion
8. Threats to validity
9. Future work
10. Conclusion
11. References

Write naturally, precisely, and academically.

Avoid promotional claims.

Every quantitative statement must be supported by executed experiments.

Do not invent literature citations or experimental observations.

Include an honest AI-use disclosure:

- AI coding tools assisted implementation.
- AI-assisted generation was used for controlled stress-test inputs.
- Inputs were validated using deterministic tools.
- Synthetic and real-world datasets were analyzed separately.
- Reported measurements came from executed experiments.

Treat the research report as a factual draft for student review and revision.

# 16. REPOSITORY STRUCTURE

Use approximately:

    formatter-suppression-study/
    ├── README.md
    ├── pyproject.toml
    ├── src/
    │   └── suppression_study/
    │       ├── __init__.py
    │       ├── cli.py
    │       ├── formatters.py
    │       ├── diagnostics.py
    │       ├── matching.py
    │       ├── classifier.py
    │       ├── generator.py
    │       ├── experiment.py
    │       └── analysis.py
    ├── tests/
    ├── configs/
    ├── datasets/
    │   ├── controlled/
    │   ├── real_world/
    │   └── results/
    ├── reports/
    │   └── figures/
    ├── report/
    │   └── research_report.md
    └── docs/
        ├── methodology.md
        ├── related_work.md
        ├── limitations.md
        └── reproducibility.md

Create directories and modules incrementally as needed.

Do not build empty scaffolding for later phases merely to make the project appear complete.

Prefer readable, maintainable Python over unnecessary abstractions.

# 17. PHASE-GATED EXECUTION — MANDATORY

**This section controls how you execute the entire research brief.**

The complete project is divided into seven phases.

You must work on **ONE PHASE PER USER REQUEST**.

You must not automatically proceed to the next phase even if the current phase finishes successfully.

Do not run the entire brief in a single autonomous session.

This is intended to reduce credit consumption, prevent cascading errors, and allow scientific review between stages.

## PHASE 1 — Environment and feasibility

Tasks:

1. Create the repository.
2. Establish a minimal Python environment.
3. Install and verify Black, Ruff, and pytest.
4. Write the initial research methodology.
5. Implement the basic four-pass diagnostic comparison.
6. Implement AST equivalence checks.
7. Build a minimal end-to-end example.
8. Run real integration tests.
9. Document initial feasibility observations.

**Deliverable:** A working minimal experiment demonstrating that the measurement pipeline operates correctly.

Do not claim suppression drift unless independently verified.

**STOP after Phase 1.**

## PHASE 2 — Diagnostic matching and validation

Tasks:

1. Build structural diagnostic matching.
2. Implement outcome classification.
3. Create positive controls where independently justified.
4. Implement negative controls.
5. Develop comprehensive unit tests.
6. Handle ambiguous and invalid comparisons.
7. Verify classifier correctness using real tool executions.

**Deliverable:** A tested and validated experimental oracle.

**STOP after Phase 2.**

## PHASE 3 — Controlled experiments

Tasks:

1. Implement controlled test generation.
2. Establish input categories and generation rules.
3. Generate and validate the controlled dataset.
4. Execute the Black and Ruff comparisons.
5. Save complete evidence and results.
6. Check reproducibility.
7. Report preliminary numerical findings without overstating them.

**Deliverable:** Completed controlled dataset with actual measurements.

**STOP after Phase 3.**

## PHASE 4 — Real-world validation

Tasks:

1. Find suitable public repositories.
2. Document selection criteria.
3. Collect a reproducible sample.
4. Run the experiment on real source code.
5. Preserve evidence.
6. Investigate ambiguous findings.
7. Compare observed patterns with the controlled dataset.

**Deliverable:** A separately documented real-world validation dataset.

**STOP after Phase 4.**

## PHASE 5 — Statistical analysis

Tasks:

1. Validate result integrity.
2. Calculate primary and secondary metrics.
3. Compute appropriate confidence intervals.
4. Analyze formatter differences.
5. Generate evidence-based figures.
6. Document important patterns and limitations.

**Deliverable:** Reproducible analysis and publication-quality figures.

**STOP after Phase 5.**

## PHASE 6 — Research report and documentation

Tasks:

1. Verify relevant literature.
2. Complete the research report.
3. Document methodology.
4. Add AI-use disclosure.
5. Document limitations and future research.
6. Write reproduction instructions.
7. Audit quantitative claims against actual result files.

**Deliverable:** Complete research report and documentation.

**STOP after Phase 6.**

## PHASE 7 — Final polish and optional explorer

Tasks:

1. Review repository quality.
2. Run the entire test suite.
3. Verify experiment reproduction.
4. Build a minimal evidence explorer if useful.
5. Review scientific consistency.
6. Prepare a concise, accurate résumé description.
7. Document future research opportunities.

**Deliverable:** A polished research repository ready for independent review.

**STOP after Phase 7.**

# 18. CREDIT AND CONTEXT EFFICIENCY

Minimize unnecessary model usage while preserving research quality.

Follow these rules:

1. Do not repeatedly rewrite functioning code.
2. Do not rebuild completed phases unless a specific issue requires it.
3. Do not repeatedly explain the full research background.
4. Use concise terminal output when possible.
5. Use automated tests instead of verbose speculative reasoning.
6. Do not create unnecessary dashboards or features.
7. Do not generate hundreds of near-identical cases merely to inflate the dataset.
8. Prefer targeted debugging over full-project rewrites.
9. Use existing reliable Python libraries instead of reinventing infrastructure.
10. Do not launch later phases while earlier validation remains incomplete.
11. Persist key decisions, methodology, and reproducibility details in repository files so future sessions can resume efficiently.
12. At the start of each new phase, read the relevant repository documentation and current code rather than asking me to paste the entire project brief again.

Spend computational effort on actual experimental execution and verification, not unnecessarily elaborate planning or presentation.

**Never sacrifice scientific validity merely to save tokens or credits.**

# 19. END-OF-PHASE HANDOFF

At the end of each phase, provide a short, factual summary in this format:

**Completed phase:** [number and title]

**Implemented:** What was actually built.

**Executed:** What commands, tests, and experiments actually ran.

**Results:** Measured findings, if applicable.

**Issues:** Bugs, limitations, blockers, or unresolved questions.

**Files:** Main files created or modified.

**Next phase:** Brief description of the next authorized stage.

Do not repeat the entire research brief.

Do not describe planned features as completed features.

End with:

**"Phase [N] complete. Ready for Phase [N+1]."**

Then STOP.

If the current phase is blocked, summarize the blocker and stop without claiming completion.

Wait for my explicit instruction, such as:

`Continue to Phase 2.`

Do not automatically continue.

# 20. PROJECT COMPLETION CRITERIA

A successful completed research pilot requires:

- A functioning experimental pipeline
- Passing automated tests
- Successful integration tests
- Actual executed comparisons
- Preserved before/after source
- Reproducible datasets
- Reliable classification logic
- Statistical summaries
- Explicit limitations
- Evidence-grounded conclusions

A complete two-dataset study additionally requires real-world repository validation.

If only the controlled study is finished, describe the project as a controlled pilot.

Never claim publication readiness without independent assessment.

# 21. START NOW — PHASE 1 ONLY

Read and understand the complete research brief.

**Execute only PHASE 1: Environment and feasibility.**

Create the repository, verify the tooling, implement the minimal four-pass comparison, validate AST equivalence, and run the first genuine end-to-end experiments.

Do not implement the full dataset generator, statistical analysis, research report, or results explorer yet.

Do not stop at producing a plan. Actually implement and test Phase 1.

Once Phase 1 is complete, provide the required phase summary and STOP.

**Wait for my instruction before beginning Phase 2.**

The ultimate objective is a rigorous, independent empirical research study—not an impressive-looking collection of unverified code.