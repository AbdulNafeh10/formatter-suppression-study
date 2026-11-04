# Public report visual review

The final public PDF was rendered to six page PNGs using Poppler at 105 dpi.
All six were inspected individually after the separate editing pass. Title and
section hierarchy, tables, paragraph spacing, links and page numbering were
readable. No clipping, overlapping text, missing-glyph boxes or footer collision
was observed. References and data links fit on the last page.

The three supplementary figures were also inspected individually. Original and
reviewed bars use the same denominators and retain the original ambiguity counts.
The paired figure shows the reviewed boundary families, pair table and new model
intervals. The pattern figure outlines the reviewed boundary row. Labels, counts,
legends and footnotes remain readable; axes include the relevant zero reference.

Poppler reported missing display-font notices for Symbol/ArialUnicode. The rendered
pages nevertheless showed no missing glyphs. The report uses ASCII prose. The
PDF's final hash and section checks are recorded in pdf_validation.json.

As a renderer compatibility check, the original report was rendered to a temporary
path and matched the preserved original PDF byte-for-byte. Its canonical source,
PDF and validation file were not overwritten. Relative file links depend on the
PDF viewer; repository Markdown is the preferred navigable version.
