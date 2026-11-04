# Public snapshot and evidence boundaries

This repository is a separate export with fresh Git history. The original
repository, commits and evidence remain private and unchanged. Historical phase
commit IDs identify that earlier provenance; they are not ancestors of this
public history.

## Measured bytes and public derivatives

Public execution records replace private home/workspace paths and personal
contacts with explicit placeholders. JUnit derivatives omit machine names.
These are privacy derivatives, not byte-identical command captures or new
measurements. The export manifest records original and public hashes separately.

Measured source bytes, rule identities, warning messages and coordinates,
visibility, classifications, exclusions and review judgments are preserved.
Natural trial source, AST dumps and formatter stdout use `*.evidence.json`
containers with upstream and modification notices. Decoding returns the original
UTF-8 bytes, including line endings, and checks their checksum. A logical
`after.py` is stored as `after.py.evidence.json`. Keeping notices outside the
measured source avoids shifting the warning coordinates. Controlled source
remains in its original form.

Original automatic results and supplementary AI-assisted review remain separate.
The public report incorporates both with their different qualifications. The
historical report stays frozen; its old packaging or phase-authorization wording
describes its checkpoint, not the current public repository.

## Omitted archives

The full Requests, Flask and pytest archives are excluded, along with unrelated
artwork, theme assets and certificate/key fixtures. Private inventories and
superseded release-decision documents are also omitted. The
[exclusion manifest](../reports/public-release/exclusions.json) records the paths.
Nothing was removed from the private original.

All 40 sampled source files and required native configuration are retained.
Offline reruns check their hashes and can reproduce the measured comparisons,
but cannot independently rebuild the archive populations. Full selection
reconstruction requires downloads matching the original three archive checksums.
An incorrect supplied archive is rejected. See [reproducibility](reproducibility.md)
for both modes. Downloaded archives and new machine-specific outputs belong in
ignored local folders, outside the distributable tree.

## Publication and later revisions

The public baseline is commit `7c77a230`, published at
[AbdulNafeh10/formatter-suppression-study](https://github.com/AbdulNafeh10/formatter-suppression-study).
The original [release checks](../reports/public-release/verification.json) are
records of preparing that snapshot. Later documentation revisions have a
[separate review](editorial_revision.md); they do not retrospectively change
the earlier release manifests or experimental provenance.

[MIT](../LICENSE) covers author-owned code and documentation with the approved
copyright name Abdul Nafeh. Upstream terms remain in
[third-party notices](../THIRD_PARTY_NOTICES.md). No redistribution permission
is assumed for excluded assets.
