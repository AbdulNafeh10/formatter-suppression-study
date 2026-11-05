# Code Formatting and Linter Suppressions

Can a Python formatter change which warnings a `noqa` comment hides while
leaving the program's syntax tree unchanged? Black and Ruff both did so in
controlled tests. This matters when a formatting-only change also changes
what a lint check reports.

```python
# Before Black: Ruff reports missing_b.
value = [missing_a,  # noqa: F821
    missing_b]

# After Black: the same comment covers both names.
value = [missing_a, missing_b]  # noqa: F821
```

Ruff checked each source before and after formatting, with and without
suppression. The four passes distinguish a warning that changed visibility
from a warning whose underlying occurrence changed. We tested eight directive
variants of 25 templates with both formatters and separately tested 40 files
from pinned Requests, Flask and pytest snapshots.

| Controlled comparisons | Black | Ruff |
|---|---:|---:|
| Confirmed changes | 68 / 200 | 35 / 200 |
| Automatically ambiguous | 16 | 16 |

The separate AI-assisted review proposed **Preserved** for the 32 ambiguous
comparisons. The automatic labels and confirmed counts stand. The 80 natural
comparisons showed no confirmed change and included four strict syntax-tree
exclusions. These counts describe the tested inputs.

[Full report (PDF)](report/research_report_public.pdf) · [Markdown](report/research_report_public.md)

## Reproduce

From a Git checkout on Windows with CPython 3.11.9:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt -e .
.\.venv\Scripts\python.exe reproduce.py
```

The command restores the [evidence bundle](evidence/study.zip), runs the tests,
repeats the 400 controlled and 80 natural comparisons, and checks classifications,
diagnostics, metrics and figures. Each run writes to a new folder under `local/`.
Use `--check` to verify saved trials and rerun the analysis without the full formatter run,
or `--unpack` to inspect the original files. Extracted paths retain the identifiers
used in the original records, including the input and result manifests.

The natural rerun uses the retained sampled files. To reconstruct sample
selection as well, fetch the checksum-pinned archives and pass their cache path:

```powershell
.\.venv\Scripts\python.exe scripts/fetch_pinned_archives.py
.\.venv\Scripts\python.exe reproduce.py --archives local/upstream-archives
```

Rebuild the PDF from its Markdown source with
`python scripts/render_report.py` in the installed environment.
Earlier repeats, protocols and releases remain available in the
[prior public snapshot](https://github.com/AbdulNafeh10/formatter-suppression-study/tree/8c8ed2eec2053293a339275502916a8276f8210f).
See the [MIT license](LICENSE) and [upstream notices](THIRD_PARTY_NOTICES.md).
