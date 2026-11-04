# Next research questions

These are proposed studies. None changes this pilot's observations or labels.

The first need is an independent check of warning correspondence. Reviewers could
label held-out source pairs without seeing the oracle output, then adjudicate
disagreements. The evaluation should report incorrect matches, missed matches
and abstentions separately. More variants of the existing templates would not
provide that independence.

The natural sample needs more opportunities to test suppression. A prospective
study could keep an unfiltered sample and add a separately defined stratum with
selected suppressed warnings and formatting changes. Eligibility and exclusion
counts would need to be retained for both. Selecting only cases that exhibit
drift would answer a different question and could not support a prevalence rate.

F-string and exception-binding anchors are concrete candidates for extending
coverage. Any extension should be checked against independent examples before
evaluation on held-out inputs. Likewise, a revised AST gate could distinguish
type-ignore position metadata from executable structure, but type-checker effects
would need separate review. The four existing AST exclusions and 32 automatic
ambiguities should remain unchanged as records of the original procedure.

A pinned version/configuration matrix could test which observed changes persist.
Keeping linter versions fixed while varying the formatter, then varying the
linter separately, would help distinguish transformation effects from diagnostic
changes. Raw outputs and version-specific correspondence would still be required.

Estimating frequency beyond a selected corpus requires a defined repository/file
sampling frame and a dependence-aware analysis specified before collection.
Projects, template treatments and paired formatter runs are not interchangeable
independent observations. Broader rules, languages and runtime properties would
each require new measurement criteria rather than a stronger interpretation of
the present results.
