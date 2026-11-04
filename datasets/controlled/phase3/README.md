# Controlled factorial sources

These are synthetic, AI-assisted source templates rendered by deterministic
Python code, not naturally occurring repository files or model-generated samples
at experiment runtime. No analyzed source is executed.

- 25 distinct AST structures, each crossed with eight directive treatments.
- 200 byte-distinct, parseable and compile-valid UTF-8 candidates.
- AST repetition within a template is intentional: directive placement/type is
  the treatment. Byte duplicate detection is separate from structural fingerprints.
- Seed 20261103 ranks execution order using SHA-256; it does not randomize code.
- One preselected treatment per template is marked reproduction_selected, using
  treatment index = template index modulo eight. This is independent of outcomes.

`specification.json` contains every complete template, rule, syntax category and
treatment name. `manifest.json` contains every case's source/checksum, structural
fingerprint, validation/exclusion status, provenance, repeat selection, and the
execution order. `cases/` preserves all 200 inputs. `generator.py` is the rendering
and validation implementation; `docs/phase3_protocol.md` is the prospective protocol.

Known f-string and exception-binding anchor boundaries are included and flagged.
Do not remove cases based on their formatter or oracle outcomes. Syntax validity
does not imply compatible formatter output or successful diagnostic matching;
those are per-comparison measurements in the result evidence.

The frozen manifest SHA-256 is
`e00a86abf2beb934188e8e255c77722105cac72f4cac4bebc87818920d7de4b8`.
Its source/specification baseline is commit `dbefde5`. Previous development
controls are stored separately and are not included in the main dataset.
