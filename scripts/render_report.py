"""Render the generated research Markdown; PDF dependencies stay separate."""

import argparse
import hashlib
import html
import json
import re
from pathlib import Path
from urllib.parse import quote, urlsplit

import reportlab
from pypdf import PdfReader
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    Image,
    KeepTogether,
    NextPageTemplate,
    PageBreak,
    PageTemplate,
    Paragraph,
    Preformatted,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_EVIDENCE = (
    "https://github.com/AbdulNafeh10/formatter-suppression-study/blob/main/"
)
PUBLIC_SECTIONS = [
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
]


def inline(text, source=None):
    def link(match):
        target = html.unescape(match[2])
        parts = urlsplit(target)
        if source is not None and not parts.scheme and not parts.netloc:
            path = (source.parent / parts.path).resolve()
            target = PUBLIC_EVIDENCE + quote(path.relative_to(ROOT).as_posix())
            if parts.fragment:
                target += "#" + parts.fragment
        return f'<a href="{html.escape(target, quote=True)}" color="#174e73">{match[1]}</a>'

    text = html.escape(text)
    text = re.sub(
        r"\[([^\]]+)\]\(([^)]+)\)",
        link,
        text,
    )
    return re.sub(r"`([^`]+)`", r'<font name="Courier" size="8.1">\1</font>', text)


def render(source=None, output=None, validation_path=None, required=None):
    source = source or ROOT / "report/research_report_public.md"
    output = output or ROOT / "report/research_report_public.pdf"
    validation_path = validation_path or ROOT / "local/pdf-validation.json"

    def markup(text):
        return inline(text, source)

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
    caption = ParagraphStyle(
        "caption", parent=body, fontSize=9.2, leading=11.8, spaceBefore=6, spaceAfter=10
    )
    code = ParagraphStyle(
        "code",
        fontName="Courier",
        fontSize=9,
        leading=12,
        leftIndent=9,
        rightIndent=9,
        borderPadding=8,
        backColor=colors.HexColor("#f3f5f6"),
        spaceBefore=3,
        spaceAfter=10,
    )
    story = []
    figures = []
    wide_page = False
    lines = source.read_text(encoding="utf-8").splitlines()
    index = 0
    while index < len(lines):
        line = lines[index].strip()
        if not line:
            index += 1
            continue
        if line in ("<!-- landscape -->", "<!-- portrait -->"):
            wide_page = line == "<!-- landscape -->"
            story.extend(
                [
                    NextPageTemplate("landscape" if wide_page else "portrait"),
                    PageBreak(),
                ]
            )
        elif line.startswith("!["):
            match = re.fullmatch(r"!\[(.+)\]\(([^)]+)\)", line)
            if not match:
                raise ValueError("Unsupported figure syntax")
            label, target = match.groups()
            path = (source.parent / target).resolve()
            if not path.is_relative_to(ROOT) or not path.is_file():
                raise ValueError("Figure must be an existing repository file")
            image = Image(str(path))
            max_width = (landscape(A4)[0] if wide_page else A4[0]) - 94
            caption_text = Paragraph(markup(label), caption)
            _, caption_height = caption_text.wrap(max_width, 100)
            max_height = 470 - caption_height if wide_page else 290
            scale = min(max_width / image.imageWidth, max_height / image.imageHeight)
            image.drawWidth = image.imageWidth * scale
            image.drawHeight = image.imageHeight * scale
            image.hAlign = "CENTER"
            story.append(KeepTogether([image, caption_text]))
            figures.append(
                {
                    "path": path.relative_to(ROOT).as_posix(),
                    "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                    "width_points": image.drawWidth,
                    "height_points": image.drawHeight,
                }
            )
        elif line.startswith("```"):
            block = []
            index += 1
            while index < len(lines) and not lines[index].startswith("```"):
                block.append(lines[index])
                index += 1
            if index == len(lines):
                raise ValueError("Unclosed code block")
            story.append(Preformatted("\n".join(block), code))
        elif line == "<!-- pagebreak -->":
            story.append(PageBreak())
        elif line.startswith("#"):
            level = len(line) - len(line.lstrip("#"))
            story.append(Paragraph(markup(line[level:].strip()), styles[level]))
        elif line.startswith("|"):
            rows = []
            while index < len(lines) and lines[index].strip().startswith("|"):
                cells = [s.strip() for s in lines[index].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-+:?", s) for s in cells):
                    rows.append([Paragraph(markup(s), cell) for s in cells])
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
            story.append(Paragraph(markup(line[2:]), body, bulletText="-"))
        elif line in ("Before formatting:", "After formatting:"):
            label = ParagraphStyle("code_label", parent=body, keepWithNext=True)
            story.append(Paragraph(markup(line), label))
        else:
            paragraph = [line]
            while index + 1 < len(lines) and lines[index + 1].strip():
                index += 1
                paragraph.append(lines[index].strip())
            story.append(Paragraph(markup(" ".join(paragraph)), body))
        index += 1

    def footer(canvas, document):
        width = canvas._pagesize[0]
        canvas.setStrokeColor(colors.HexColor("#a2adb5"))
        canvas.line(47, 39, width - 47, 39)
        canvas.setFont("Times-Roman", 8)
        canvas.drawString(
            47, 27, "Code Formatting and Linter Suppressions | Research pilot"
        )
        canvas.drawRightString(width - 47, 27, str(document.page))

    doc = BaseDocTemplate(
        str(output),
        pagesize=A4,
        leftMargin=47,
        rightMargin=47,
        topMargin=41,
        bottomMargin=50,
        title="Code Formatting and Linter Suppressions",
        author="Abdul Nafeh",
        pageCompression=1,
        invariant=1,
    )
    templates = []
    for name, size in (("portrait", A4), ("landscape", landscape(A4))):
        frame = Frame(
            47,
            50,
            size[0] - 94,
            size[1] - 91,
            leftPadding=0,
            rightPadding=0,
            topPadding=0,
            bottomPadding=0,
        )
        templates.append(PageTemplate(name, [frame], onPage=footer, pagesize=size))
    doc.addPageTemplates(templates)
    doc.build(story)
    reader = PdfReader(output)
    text = "\n".join(page.extract_text() for page in reader.pages)
    required = required or PUBLIC_SECTIONS
    if any(part not in text for part in required) or "{{" in text or "\u25a0" in text:
        raise ValueError("PDF content verification failed")
    result = {
        "pages": len(reader.pages),
        "reportlab": reportlab.Version,
        "markdown_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "pdf_sha256": hashlib.sha256(output.read_bytes()).hexdigest(),
        "required_sections_present": True,
        "page_text_characters": [len(page.extract_text()) for page in reader.pages],
    }
    if len(figures) != 4 or reader.metadata.author != "Abdul Nafeh":
        raise ValueError("Public report requires four figures and the approved author")
    result.update(
        author=reader.metadata.author,
        embedded_figures=figures,
        repository_link_base=PUBLIC_EVIDENCE,
    )
    validation_path.parent.mkdir(parents=True, exist_ok=True)
    validation_path.write_bytes((json.dumps(result, indent=2) + "\n").encode())
    print(json.dumps(result))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--validation", type=Path)
    render(validation_path=parser.parse_args().validation)
