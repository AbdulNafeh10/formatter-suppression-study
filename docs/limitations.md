# Limitations through Phase 6

The [research report](../report/research_report.md) consolidates these limitations
by construct, internal, external and conclusion validity. The [AI disclosure](ai_use.md)
explains correlated validation risks. The targeted [literature review](related_work.md)
establishes prior awareness but cannot establish novelty. No independent scientific
review or publication-readiness assessment has occurred.

Priority future work is independently adjudicated held-out matching evaluation,
prospective warning-relevant natural sampling, broader versions/rules/projects,
and a separately specified evaluation of any AST-gate revision. No data have been
reclassified to implement those extensions in Phase 6.

- The completed main experiment is a controlled pilot with 200 AI-assisted
  synthetic sources from 25 AST structures and eight directive treatments.
  A separate historical convenience sample now contains forty natural-noqa files
  from three pinned repositories. Main controlled results, natural results, prior
  development controls, discovery probes and repeat runs are separate. No
  stress-suite proportion estimates natural prevalence.
- Each source is paired across formatters; each template is reused across
  treatments. These observations are dependent. The design was informed by
  Phase 2 discoveries, not held out for detector evaluation.
  Phase 5 provides exact corpus proportions/bounds and conditional cluster-model
  sensitivity, not design-based population inference or significance testing.
- Detailed interval choices were made after earlier outcome counts were known.
  The analysis is exploratory rather than confirmatory. Template/category
  bootstrap and family-level Wilson intervals assume exchangeable independent
  clusters; hand-selected, related templates do not verify that assumption.
  No natural-source IID/Wilson or three-repository bootstrap interval is reported.
  Finite archive completion bounds describe unobserved/unresolved outcomes and
  are not confidence intervals or ecosystem prevalence bounds.
- Natural-source selection uses fixed generated/vendored heuristics, UTF-8 and
  Python 3.11 validity, a 200 KiB cap, and at most twenty eligible files per repo.
  It includes tests/examples and is not a representative source-population sample.
  Noqas for rules outside F401/F821/F841 often yield empty selected warning sets:
  forty-four of eighty primary comparisons were empty. Most text was unchanged.
- The oracle is limited to pinned Ruff F401, F821 and F841. Load/store Name and
  import-alias spans are supported. Warnings inside f-string expressions or
  string-based annotations may lack a complete token-aligned anchor and are
  conservatively Ambiguous. F841 bindings without an ast.Name (such as exception
  handler names) are also outside the current anchor policy.
- AST equality is strict, includes type comments, and is not proof of runtime
  equivalence. TypeIgnore line metadata, docstring changes, or type-comment
  changes can cause AST changed classifications. Compilation verifies source
  legality but analyzed programs are never executed.
  Four natural-source comparisons were excluded solely because TypeIgnore.lineno
  fields shifted. Investigative normalization explains the exclusions but does
  not reclassify them or change the prospectively specified strict gate.
- Complete underlying correspondence is required before attributing drift.
  There is no fuzzy recovery for changed diagnostic spans, tokens, or messages.
  Invalid spans, unsupported rules and duplicate identities remain inconclusive.
  This favors conservative attribution over broad coverage.
- Labels were fixed before the matcher existed and checked using raw warning
  occurrences plus a comment-only intervention. The separate procedure uses the
  same pinned Ruff engine as measurement. It is not a second linter or a separate
  human adjudication. A held-out set and independent human review are outstanding.
  This describes the Phase 2 controls. New Phase 3 labels come from the oracle;
  four representative comment-only interventions support selected-case attribution,
  not independent labeling of the full main dataset.
- Diagnostic changed branches are exercised with injected unit diagnostics.
  These are software-validation tests, not observed formatter-induced underlying
  diagnostic changes. Manual directive intervention positives are not formatter
  positives. No detector precision, recall, F1 or general accuracy claim is made.
- Python 3.11 / Windows x64 and the saved exact dependency environment are the
  only tested environment. Only UTF-8 source is accepted. Primary formatting/linting
  uses isolated standardized settings and study_input.py, including for initializers.
  Supplementary native-config sensitivity uses actual paths and restored archive
  configs for Flask/pytest, but is not full project CI/dependency/Git-environment
  reproduction. Only the three study rules are classified; Requests has no
  discovered Ruff config at its selected commit.
- Text unchanged is recorded separately. Repeated executions are reproducibility
  checks on the same cases, not additional independent observations.
  Phase 3 repeated fifty comparisons chosen before results and regenerated all
  200 sources; it did not execute a second full 400-comparison main run.
  Phase 4 repeated six prospectively chosen primary comparisons; all happened to
  be text-unchanged. Whole archive/population/sample reconstruction and all source
  checksums were verified, but changed natural outputs were not rerun in that sample.
