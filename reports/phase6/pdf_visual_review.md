# PDF review - 2026-11-03

Input: `report/research_report.pdf`; final digest is in `pdf_validation.json`.
Built from generated Markdown with ReportLab 4.4.9 and extracted with pypdf 6.10.0.
Poppler rendered all six pages at 105 dpi into ignored temporary PNGs. Each page
was visually inspected individually, not just text-extracted.

- Page 1: title, abstract, introduction, literature context and questions readable.
- Page 2: four-pass table, correspondence and sampling methods fit without spill.
- Page 3: outcome, paired and interval tables align; denominator caveats remain visible.
- Page 4: natural population and outcome tables readable; no exclusion row omitted.
- Page 5: discussion, validity threats, future work and AI disclosure fit cleanly.
- Page 6: references, data availability and reproduction content readable; links styled.

No clipped text, overlapping content, broken table cells, missing-glyph boxes,
or footer collisions were observed. Required section and page-count checks passed.
Poppler printed missing display-font notices for Symbol/ArialUnicode; the six
rendered pages were nevertheless complete and showed no visual glyph defect.
Relative file links depend on the PDF viewer and distribution layout; repository
Markdown is the preferred navigable source. Original analysis figures remain
separate full-resolution artifacts rather than reduced images inside the report.
