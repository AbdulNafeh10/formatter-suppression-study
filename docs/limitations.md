# Limitations

The controlled results show that formatting can change suppression under the
tested conditions. They do not estimate how often it happens in Python projects.
The natural sample found no confirmed changes, but offered few opportunities to
observe them. These limits affect different parts of the argument.

## What the samples cover

The 200 controlled sources come from 25 AI-assisted AST structures, each reused
across eight directive treatments. They deliberately exercise layouts near
suppression boundaries. The design benefited from development discoveries and
is not a held-out accuracy benchmark. A formatter difference on these cases is
evidence about the corpus, not a general ranking of the tools.

Requests, Flask and pytest were a convenience selection at historical commits.
Eligibility rules exclude non-UTF-8, oversized, generated and vendored files;
only 20 of pytest's 28 eligible files were selected. Tests and examples remain
eligible. This is not a representative repository or file sampling frame.
Of 80 primary natural comparisons, 65 had unchanged text and 44 began with no
underlying warning from the three selected rules. Only seven combined changed
text, an accepted AST gate and a selected warning originally suppressed. The
negative result is therefore narrow.

## What the oracle can establish

The oracle tracks Ruff F401, F821 and F841 using specific AST and token anchors.
Python 3.11 f-string expressions do not expose the required complete token span,
and exception binding names are strings in `ExceptHandler.name`, not stored
`Name` nodes. These boundaries produced all 32 automatic ambiguities. The
supplementary AI-assisted review proposes Preserved in each case, with evidence
and human-interpretation flags. Those proposals remain conditional. Intended
scope of a standalone directive cannot be inferred from its placement alone.

Strict AST equality includes type comments and type-ignore line fields. Four
natural comparisons failed solely because `TypeIgnore.lineno` moved. A secondary
normalization explains those failures without changing the primary gate or
labels. AST equality and successful compilation do not prove runtime equivalence;
none of the analyzed programs was executed.

Stable underlying diagnostics and complete correspondence are required before
attributing a visibility change. This limits coverage when an anchor is missing
or diagnostics change. Tests with injected diagnostics exercise software branches;
they are not observed formatter-induced changes or an independent accuracy study.
No precision, recall or F1 has been measured.

The implementation, templates, tests, interpretation and supplementary review all
used AI assistance. Shared assumptions can survive deterministic checks and
repeated tool runs. Independent adjudication of held-out examples is still needed.

## Analysis and environment

Formatter observations are paired, and directive variants share templates.
Interval choices were made after initial counts were available. The reported
bootstrap and Wilson calculations are exploratory model checks, conditional on
independent, exchangeable clusters. The corpus does not verify those assumptions.
Unresolved-outcome bounds are finite-corpus bounds, not confidence intervals.
No natural-source population interval or significance test is reported.

The measured tools and environment are pinned: CPython 3.11.9, Black 25.1.0 and
Ruff 0.11.13 on Windows. Primary calls isolate project configuration and use an
artificial filename. Native sensitivity restores the available Flask/pytest
lint context, but does not reproduce dependencies, the full Git environment or
project CI. Requests had no discovered Ruff configuration at its selected commit.
Behavior on newer versions, other rules and other platforms remains untested.

Phase 7 later repeated all 400 controlled and 80 natural comparisons, including
the 15 changed natural outputs. Public-release preparation repeated them in a
fresh pinned environment on the same host. These runs extend the earlier limited
repeat checks, but add no independent inputs or clean-machine validation.

The public snapshot omits full upstream archives. Offline checks validate retained
sources and context; rebuilding the original eligible populations requires the
checksum-verified archive downloads described in [reproducibility](reproducibility.md).
Publication checks address packaging and repeatability, not independent scientific
endorsement. The [future-work note](future_research.md) describes concrete ways to
test the remaining questions.
