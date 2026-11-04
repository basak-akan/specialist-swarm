"""Text + structural extraction from docx / pptx deliverables."""
from __future__ import annotations

import re
from pathlib import Path

PLACEHOLDER_RE = re.compile(r"TODO|lorem|placeholder|\[insert|TBD|XXX", re.IGNORECASE)


def _iter_block_items(doc):
    """Yield Paragraph and Table objects of the document body in document order."""
    from docx.table import Table
    from docx.text.paragraph import Paragraph

    body = doc.element.body
    for child in body.iterchildren():
        tag = child.tag.rsplit("}", 1)[-1]
        if tag == "p":
            yield Paragraph(child, doc)
        elif tag == "tbl":
            yield Table(child, doc)


def _table_lines(table) -> list[str]:
    lines = []
    for row in table.rows:
        cells = []
        prev = None
        for cell in row.cells:
            # merged cells repeat the same _tc; dedupe adjacent repeats
            if prev is not None and cell._tc is prev:
                continue
            prev = cell._tc
            cells.append(" ".join(cell.text.split()))
        lines.append(" | ".join(cells))
    return lines


def _is_heading(par) -> bool:
    try:
        name = (par.style.name or "").lower()
    except Exception:
        return False
    return name.startswith("heading") or name == "title"


def extract_docx(path) -> dict:
    from docx import Document
    from docx.table import Table

    doc = Document(str(path))
    lines: list[str] = []
    headings: list[str] = []
    title = ""
    table_count = 0
    for block in _iter_block_items(doc):
        if isinstance(block, Table):
            table_count += 1
            lines.extend(_table_lines(block))
        else:
            txt = block.text.strip()
            if not txt:
                continue
            lines.append(txt)
            if _is_heading(block):
                headings.append(txt)
                if not title and ((block.style.name or "").lower() in ("title", "heading 1")):
                    title = txt
    if not title:
        try:
            title = (doc.core_properties.title or "").strip()
        except Exception:
            title = ""
    # header/footer text is not part of "text" but placeholders there still count
    extra = []
    for section in doc.sections:
        for part in (section.header, section.footer):
            try:
                extra.extend(p.text for p in part.paragraphs if p.text.strip())
            except Exception:
                pass
    text = "\n".join(lines)
    hits = PLACEHOLDER_RE.findall(text + "\n" + "\n".join(extra))
    return {
        "text": text,
        "title": title,
        "headings": headings,
        "table_count": table_count,
        "word_count": len(text.split()),
        "placeholder_hits": hits,
    }


def extract_pptx(path) -> dict:
    from pptx import Presentation

    prs = Presentation(str(path))
    lines: list[str] = []
    titles: list[str] = []
    for slide in prs.slides:
        title = ""
        try:
            if slide.shapes.title is not None:
                title = slide.shapes.title.text_frame.text.strip()
        except Exception:
            title = ""
        titles.append(title)
        for shape in slide.shapes:
            if getattr(shape, "has_text_frame", False) and shape.has_text_frame:
                t = shape.text_frame.text.strip()
                if t:
                    lines.append(t)
            if getattr(shape, "has_table", False) and shape.has_table:
                for row in shape.table.rows:
                    lines.append(" | ".join(" ".join(c.text.split()) for c in row.cells))
        try:
            if slide.has_notes_slide:
                n = slide.notes_slide.notes_text_frame.text.strip()
                if n:
                    lines.append(n)
        except Exception:
            pass
    return {"text": "\n".join(lines), "slide_count": len(prs.slides), "slide_titles": titles}


if __name__ == "__main__":
    import json
    import sys

    p = Path(sys.argv[1])
    out = extract_pptx(p) if p.suffix.lower() == ".pptx" else extract_docx(p)
    print(json.dumps(out, indent=2, ensure_ascii=False))
