# Documentation revision

This local revision starts from the published public snapshot `7c77a230`.
It changes explanations and navigation, not the experiment. No push or publication
is part of this work. AI assisted the revision; no detector score was used as a
target, and no personal motivation or development history was invented.

## What needed work

The main problem was repetition rather than ornate vocabulary. Scope warnings
appeared in the overview, results, discussion, limitations and release notes,
often in the same short-list structure. Meanwhile, the purpose of diagnostic
correspondence was compressed into terms such as "unique rule/AST-occurrence/token
correspondence". That is accurate shorthand, but it leaves readers to work out
why warning counts and line numbers are insufficient.

Other problems were practical. The evidence guide assumed natural trial source
was stored as an ordinary `.py` file. The reproduction guide required an
undocumented manual configuration edit. Current limitation notes stopped at the
early repeat sample, although Phase 7 had subsequently repeated every comparison.
Several release pages still said the repository had no remote or publication.
Those statements described earlier checkpoints, not the published snapshot.

## Files revised

| Files | Substantive change |
|---|---|
| `report/README_public.template.md`, generated `README.md` | Lead with how joining/splitting lines changes suppression; reduce repeated scope and release administration. The generated README has 524 prose words. |
| `report/research_report_public.template.md`, generated Markdown and PDF | Explain occurrence matching and paired denominators; separate observations from interpretation; give Discussion its own page; retain all tables, numeric bindings and references. |
| `docs/methodology.md` | Expand the four-pass rationale, exact identity checks, Unicode coordinates, strict AST gate, tool settings and outcome definitions. Retain the historical protocol tail unchanged in a collapsible section. |
| `docs/limitations.md` | Group actual limitations by sample, oracle, analysis and environment; distinguish completed full repeats from outstanding independent validation. |
| `docs/evidence_guide.md` | Start with the current report, explain lossless natural-source containers, provide a checked decoding example and distinguish automatic/reviewed result layers. |
| `docs/ai_use.md` | Disclose this editorial assistance and explain shared-error risks without implying independent human validation. |
| `docs/related_work.md` | Put each source's relevance before access logistics; keep pinned-document and novelty limits. Retain the historical review tail unchanged. |
| `docs/future_research.md` | Replace a uniform wide table with reasoned priorities: independent correspondence checks, relevant natural cases and separately evaluated coverage extensions. |
| `docs/reproducibility.md` | Separate saved checks, fresh measurement and analysis of retained observations; provide the exact configuration-copy transformation. |
| `docs/public_snapshot.md`, `docs/release_review.md`, `docs/public_release_readiness.md` | Correct the current publication context while retaining earlier verification totals and linking later editorial checks separately. |
| `reports/publication-phase-b/public_claim_audit.json` | Regenerate current-document hashes, claim locations and README word count with the existing builder. All 78 source pointers, source hashes, formats, values and rendered numbers are unchanged. |

The new files under `reports/editorial-review` record document scope, checks,
PDF validation and hashes for this revision. This page records the editorial
decisions. The [review-output directory](../reports/editorial-review) contains
the machine-readable detail.

All 44 baseline Markdown files were inventoried and reviewed. Frozen phase
protocols, result notes, claim reviews, dataset documentation and the original
report were retained as historical/evidentiary records. Legal notices were
reviewed without editing. The resume description already states the supplied
August-November 2026 period and its limits; it needed no substantive rewrite.
The per-file decisions are in `documentation_scope.json`.

## Representative passages

### Explain what a check does

Before, the methodology summary said:

> Within-snapshot subset checks use exact diagnostic identity; cross-snapshot
> matching uses unique rule/AST-occurrence/token correspondence.

After:

> Within a snapshot, visible diagnostics must be a multiset subset of underlying
> diagnostics. This check uses the rule, message and exact start/end coordinates.
> The difference identifies suppressed warning occurrences. A change in the visible
> count alone cannot distinguish changed suppression from changed underlying warnings.

The revised text distinguishes the two identity problems and explains the
purpose of the subset check. The following paragraph describes the cross-source
key and its validation rather than using the shorthand as an explanation.

### Describe the correspondence key precisely

Before, the public report said:

> The automatic matcher identifies warnings by rule, AST occurrence and token
> context. It does not match across formatting by line number or message alone.
> Correspondence must be unique, and the underlying warning identities must agree.

After:

> Across snapshots, the identity key is the rule plus an AST field/index path.
> The matcher also requires the coordinate-free node content and
> construct/diagnostic tokens to agree. It supports import aliases, load Names
> and store Names for the selected rules.

The revised explanation separates the identity key from the checks applied to
it and names the supported constructs. This makes the later exception-binding
limitation easier to understand without claiming that correspondence is solved
for other syntax.

### Make an evidence-reading instruction usable

Before:

> Compare `before.py` and `after.py`; treat source files as data, not programs to run.

After:

> Controlled trials store ordinary `before.py` and `after.py` files. Natural trials
> use `before.py.evidence.json` and `after.py.evidence.json`: lossless containers
> holding the measured source and required notices.

The guide now follows this with a working `evidence_bytes` example. It explains
why the packaging preserves coordinates instead of asking readers to find files
that do not exist under those physical names.

### Separate historical repeat coverage from current limits

Before, the limitations ended with the early natural repeat sample:

> Phase 4 repeated six prospectively chosen primary comparisons; all happened to
> be text-unchanged. Whole archive/population/sample reconstruction and all source
> checksums were verified, but changed natural outputs were not rerun in that sample.

The current guide now states:

> Phase 7 later repeated all 400 controlled and 80 natural comparisons, including
> the 15 changed natural outputs. Public-release preparation repeated them in a
> fresh pinned environment on the same host. These runs extend the earlier limited
> repeat checks, but add no independent inputs or clean-machine validation.

This reconciles completed stages without changing the earlier record or making
repeatability stand in for independent accuracy.

## Repetition removed

The README now introduces the mechanism, method, main observations and entry
points without a separate list repeating the report's limitations. Access
logistics no longer interrupt each related-work explanation. Current release
pages link to one snapshot boundary instead of repeating the approval history.
The future-work table's repeated "evidence needed" framing is replaced by the
specific question each proposed study would answer. Caveats remain where needed
for independent reading, especially around reviewed labels and natural results.

## Questions left unresolved

The 32 proposed Preserved judgments remain AI-assisted and conditional. Exception
binding identity and the intended scope of standalone directives still require
human interpretation. No prose revision can establish independent matcher
accuracy, review-error rates or whether cluster exchangeability is reasonable.
The natural zero result cannot settle prevalence: many outputs did not change
and selected warning sets were often empty. Four strict type-ignore AST
exclusions remain exclusions. These are research limits, not editorial defects.

Historical dataset notes still describe archives retained in the original study.
They were not rewritten because dataset contents and provenance are protected.
Current snapshot and reproduction guides explicitly explain the public omission
and the offline/full-reconstruction distinction.

## Verification and preservation

All 146 existing tests passed in the pinned environment on the same Windows
host. `pip check`, Black's read-only check (47 files) and Ruff's check passed.
The existing builders verified 78 current-public and 86 historical claim bindings.
The ambiguity verifier checked 32 comparisons, 1,498 review artifacts and 840
unchanged original files. Controlled source regeneration and saved full-repeat
checks covered 400 comparisons; natural retained-source/repeat checks covered 80.
The latter explicitly skipped archive hashes and eligible-population reconstruction.
No fresh measurements, archive reconstruction or statistical reruns are claimed
for this prose-only revision.

The report was regenerated with the existing `scripts/render_report.py` workflow,
calling `render` with the public source/output paths and a separate
`reports/editorial-review/pdf_validation.json` destination. Its eight required
section titles were checked. All six rendered pages were inspected at reading
size; tables, references, footer numbering and page transitions were checked.
Standalone figures were not regenerated; all seven PNG/SVG pairs are unchanged.

Relative Markdown file/image targets were checked outside code fences; fragment
anchors were not part of that check. Public references remain byte-identical.
Primary sources were rechecked for relevant passages, including the pinned
Black/Ruff documentation, two author-hosted research papers, McKeeman's original
journal and the statistical method references. Browser access to the journal
exceeded the tool's size limit; the completed original PDF download was inspected
locally instead. GitHub's connector supplied the pinned documentation when web
fetches failed. No access failure was treated as successful verification.

Protected tracked files were compared directly with baseline Git blobs, including
source, tests, configurations, measurements, both analyses, figures, original
report, licenses, notices and earlier provenance. No experimental or legal file
changed. The only regenerated earlier-path JSON is the current-document claim
ledger, whose evidence fields are unchanged. Old release hash manifests are
verified against commit `7c77a230`, not rebound to edited documents. New editorial
hashes describe this revision separately.

Changed/new distributable files and extracted PDF text were scanned with the
existing credential, home-path and email patterns. Pattern checks cannot prove
the absence of every possible secret. Local logs, downloaded references and page
images remain ignored and are not included in the commit. The private original
was checked read-only: clean at `60d9471e`. Findings, numerical results, statistical
calculations, upstream terms and the MIT ownership wording are unchanged.

The final diff and verification counts are reported with the local commit.
Publishing this revision still requires a separate instruction.
