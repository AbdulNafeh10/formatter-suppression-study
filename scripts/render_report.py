"""Render the generated research Markdown; PDF dependencies stay separate."""

import argparse
import hashlib
import html
import json
import re
from pathlib import Path

import reportlab
from pypdf import PdfReader
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parents[1]


def inline(text):
    text = html.escape(text)
    text = re.sub(
        r"\[([^\]]+)\]\(([^)]+)\)",
        lambda m: f'<a href="{m[2]}" color="#174e73">{m[1]}</a>',
        text,
    )
    return re.sub(r"`([^`]+)`", r'<font name="Courier" size="8.1">\1</font>', text)


def render(source=None, output=None, validation_path=None, required=None):
    source = source or ROOT / "report/research_report.md"
    output = output or ROOT / "report/research_report.pdf"
    validation_path = validation_path or ROOT / "reports/phase6/pdf_validation.json"
    body = ParagraphStyle(
        "body",
        fontName="Times-Roman",
        fontSize=10.4,
        leading=13,
        spaceAfter=7,
        alignment=TA_LEFT,
    )
    styles = {
        1: ParagraphStyle(
            "title",
            parent=body,
            fontName="Times-Bold",
            fontSize=21,
            leading=24,
            spaceAfter=12,
        ),
        2: ParagraphStyle(
            "section",
            parent=body,
            fontName="Times-Bold",
            fontSize=13,
            leading=16,
            spaceBefore=7,
            spaceAfter=7,
            keepWithNext=True,
        ),
        3: ParagraphStyle(
            "subsection",
            parent=body,
            fontName="Times-Bold",
            fontSize=11,
            leading=14,
            spaceBefore=4,
            spaceAfter=5,
            keepWithNext=True,
        ),
    }
    cell = ParagraphStyle("cell", parent=body, fontSize=9.1, leading=11, spaceAfter=0)
    story = []
    lines = source.read_text(encoding="utf-8").splitlines()
    index = 0
    while index < len(lines):
        line = lines[index].strip()
        if not line:
            index += 1
            continue
        if line == "<!-- pagebreak -->":
            story.append(PageBreak())
        elif line.startswith("#"):
            level = len(line) - len(line.lstrip("#"))
            story.append(Paragraph(inline(line[level:].strip()), styles[level]))
        elif line.startswith("|"):
            rows = []
            while index < len(lines) and lines[index].strip().startswith("|"):
                cells = [s.strip() for s in lines[index].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-+:?", s) for s in cells):
                    rows.append([Paragraph(inline(s), cell) for s in cells])
                index += 1
            columns = len(rows[0])
            widths = {
                3: [241, 130, 130],
                4: [195, 87, 87, 132],
                5: [99, 73, 96, 105, 128],
            }[columns]
            table = Table(rows, colWidths=widths, repeatRows=1, hAlign="LEFT")
            table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#eaf0f4")),
                        ("VALIGN", (0, 0), (-1, -1), "TOP"),
                        ("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.HexColor("#758895")),
                        (
                            "LINEBELOW",
                            (0, -1),
                            (-1, -1),
                            0.35,
                            colors.HexColor("#a2adb5"),
                        ),
                        ("LEFTPADDING", (0, 0), (-1, -1), 6),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                        ("TOPPADDING", (0, 0), (-1, -1), 5),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                    ]
                )
            )
            story.extend([table, Spacer(1, 9)])
            continue
        elif line.startswith("- "):
            story.append(Paragraph(inline(line[2:]), body, bulletText="-"))
        else:
            paragraph = [line]
            while index + 1 < len(lines) and lines[index + 1].strip():
                index += 1
                paragraph.append(lines[index].strip())
            story.append(Paragraph(inline(" ".join(paragraph)), body))
        index += 1

    def footer(canvas, document):
        canvas.setStrokeColor(colors.HexColor("#a2adb5"))
        canvas.line(47, 39, A4[0] - 47, 39)
        canvas.setFont("Times-Roman", 8)
        canvas.drawString(
            47, 27, "Code Formatting and Linter Suppressions | Research pilot"
        )
        canvas.drawRightString(A4[0] - 47, 27, str(document.page))

    doc = SimpleDocTemplate(
        str(output),
        pagesize=A4,
        leftMargin=47,
        rightMargin=47,
        topMargin=41,
        bottomMargin=50,
        title="Code Formatting and Linter Suppressions",
        author="AI-assisted research pilot",
        pageCompression=1,
        invariant=1,
    )
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    reader = PdfReader(output)
    text = "\n".join(page.extract_text() for page in reader.pages)
    if not 4 <= len(reader.pages) <= 6:
        raise ValueError(f"report length outside target: {len(reader.pages)} pages")
    required = required or [
        "Abstract",
        "Methodology",
        "Results: controlled inputs",
        "Results: natural-source validation",
        "Threats to validity",
        "References",
        "AI-use disclosure",
    ]
    if any(part not in text for part in required) or "{{" in text or "\u25a0" in text:
        raise ValueError("PDF content verification failed")
    result = {
        "pages": len(reader.pages),
        "reportlab": reportlab.Version,
        "markdown_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "pdf_sha256": hashlib.sha256(output.read_bytes()).hexdigest(),
        "required_sections_present": True,
        "page_text_characters": [len(page.extract_text()) for page in reader.pages],
        "visual_review": "Separate rendered-page inspection required; see pdf_visual_review.md.",
    }
    validation_path.parent.mkdir(parents=True, exist_ok=True)
    validation_path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--public", action="store_true")
    args = parser.parse_args()
    if args.public:
        render(
            ROOT / "report/research_report_public.md",
            ROOT / "report/research_report_public.pdf",
            ROOT / "reports/publication-phase-b/pdf_validation.json",
            [
                f"{number}. {name}"
                for number, name in enumerate(
                    [
                        "Introduction",
                        "Related Work",
                        "Methodology",
                        "Results",
                        "Discussion",
                        "Limitations",
                        "Conclusion",
                        "References",
                    ],
                    1,
                )
            ],
        )
    else:
        render()
