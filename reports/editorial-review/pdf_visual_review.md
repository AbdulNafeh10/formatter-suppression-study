# Public report layout review

The existing renderer produced six pages. Poppler PNGs were inspected in a
contact sheet and individually at 110 dpi. No clipped text, table overlap,
unreadable glyphs or stray blank pages were observed.

| Page | Checked content |
|---|---|
| 1 | Title, introduction, related work, tool settings and four-pass table |
| 2 | Continuation of methods, AST/token correspondence, inputs, analysis and AI disclosure |
| 3 | Controlled counts, paired table, ambiguity explanation and interval table |
| 4 | Source mechanisms and natural results, including exclusions and repeat coverage |
| 5 | Discussion, limitations and conclusion on one page with readable spacing |
| 6 | All eight references and data/reproduction links |

All pages retain the report title footer and consecutive page numbers. Manual
page breaks keep tables together and start Discussion and References on their
own pages. Figures remain linked standalone artifacts, as in the existing
public-report workflow; none was redrawn or changed.

Poppler printed display-font lookup warnings for Symbol and ArialUnicode.
Rendered text was visually intact. The existing renderer uses its existing
Times/Courier styles; no renderer or dependency changes were made.
