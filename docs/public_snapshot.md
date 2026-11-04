# Public snapshot and evidence boundaries

This is a separate export of the completed research, with fresh Git history.
The original repository, historical commits and original evidence remain private
and unchanged. Historical phase notes describe their original checkpoints; their
commit IDs are provenance identifiers, not ancestors of this snapshot.

## What changed

Private home/workspace paths and personal contact metadata were replaced with
explicit placeholders in public execution records. These records are privacy
derivatives, not byte-identical original captures and not new measurements.
Machine names were also removed from JUnit derivatives.
Source bytes, rule identities, messages, diagnostic coordinates, visibility,
automatic classifications, exclusion reasons, counts and supplementary review
judgments were not changed. Replacement hashes describe the public derivative;
the export manifest records original and public hashes separately.

Natural trial code, AST dumps and formatter stdout use `*.evidence.json` files
with same-file upstream and modification notices. The UTF-8 content decodes to
the original measured bytes, including line endings. The reader in
`suppression_study.evidence` checks that checksum before returning source.
For example, a logical `after.py` is stored as `after.py.evidence.json`.
This packaging keeps license notices beside the modified source without adding
comments that would shift diagnostic coordinates. Controlled source is unchanged.

The public README and six-page report retain the scientific findings and
limitations. Packaging/licensing wording differs from the original report's
historical statements. Original automatic labels and the later AI-assisted review
remain separate; the latter is not independent human ground truth.

## Exclusions and reproducibility

The full Requests, Flask and pytest source archives are not redistributed.
Requests artwork/theme context and certificate/key fixtures are absent. Historical
private-path inventories and superseded release-decision documents are omitted.
The exclusion manifest records the precise paths. No excluded asset was deleted
from the original repository.

The retained 40 sampled source files and required native configuration allow
fresh natural comparisons offline. That mode verifies retained source/context
hashes but does not independently recreate the archive population. The manifest
explicitly records the permitted non-measured context omissions. A supplied
archive is always checksum-checked; an absent archive is tolerated only for this
declared public export. Required measured source/configuration checks remain.

The archive-fetch command and a full reconstruction check are documented in
[reproducibility](reproducibility.md). Fresh downloads must match the three original
SHA-256 values. Archives are processed as data, without running upstream programs.
Network availability and future upstream hosting are outside this repository's
control. Do not add downloaded archives or new machine-specific execution outputs
to the public history.

## Release status

Scientific, reproduction and release checks passed as recorded in the
[readiness report](public_release_readiness.md). The author confirmed the public
copyright-holder name Abdul Nafeh, and [MIT](../LICENSE) now covers author-owned
code and documentation. Upstream terms remain separate. No identity was inferred
from an email address. Nothing has been pushed, published or connected to a remote;
publication still requires separate explicit approval.
