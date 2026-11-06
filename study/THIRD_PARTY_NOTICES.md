# Third-party material

The [project MIT license](LICENSE), Copyright (c) 2026 Abdul Nafeh, covers
author-owned code and documentation. It does not relicense upstream source,
excerpts or derived formatter evidence.

| Source | Pinned commit | License and attribution |
|---|---|---|
| Requests v2.32.3 | `0e322af87745eff34caffe4df68456ebc20d9068` | [Apache-2.0](third_party/requests/LICENSE), Copyright 2019 Kenneth Reitz; [NOTICE](third_party/requests/NOTICE) |
| Flask 3.1.0 | `ab8149664182b662453a563161aa89013c806dc9` | [BSD-3-Clause](third_party/flask/LICENSE), Copyright 2010 Pallets |
| pytest 8.3.5 | `b55ab2aabb68c0ce94c3903139b062d0c2790152` | [MIT](third_party/pytest/LICENSE), Copyright 2004 Holger Krekel and others |
| Flask-CLI material in Flask's `tests/test_cli.py` | Inherited through the pinned Flask source above | [Revised BSD text and supplementary notices](third_party/flask-cli/LICENSE), Copyright 2015 CERN |

Full license and applicable NOTICE texts are retained, including the root
[NOTICE](NOTICE). Unmodified sampled Python source remains under
`datasets/real_world/phase4/sources`; its original hashes are unchanged.
Flask's sampled `tests/test_cli.py` explicitly retains the earlier Flask-CLI/CERN
notice. Its full upstream [license text](https://github.com/inveniosoftware/flask-cli/blob/master/LICENSE)
was additionally retrieved for this export; the local copy includes CERN's
privileges-and-immunities clause and the upstream file-specific notices. This
supplementary license retrieval is not a new experimental source selection.

Natural trial source, AST dumps and formatter stdout are losslessly packaged as
`*.evidence.json`. Each container carries a prominent upstream attribution and
modification notice with the source content, its original checksum and logical
filename. The notice distinguishes upstream before-source, formatter-modified
after-source and the public container representation. Existing command JSON files
that contain natural source also carry the notice. Decoding does not add headers
or change measured lines. These are attributed evidence representations under
the corresponding upstream license, not newly authored study programs.

The full upstream archives, Requests `ext` artwork and `docs/_themes` material,
and all archived certificate/private-key fixtures are excluded. The separate
all-rights-reserved artwork notice therefore grants no assumed permission in
this snapshot. No redistribution of that uncertain artwork is proposed.
Reconstruction can download the original archives into an ignored local cache;
that cache must not be included in any public package.

Dependencies are installed separately and are not vendored. Referenced papers
are linked rather than redistributed. Retain all notices when sharing the public
snapshot. No endorsement or rights in upstream logos are asserted.
