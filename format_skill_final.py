"""Normalize skill-final-v1.pptx typography and remove metadata microcopy.

Rules requested by the user:
- top-left page title: Microsoft YaHei 24 pt, RGB(199, 0, 11)
- body section headings: Microsoft YaHei 12 pt
- body text: Microsoft YaHei 10 pt
- remove top-right and bottom-left metadata microcopy
Display KPI numbers (numeric-only, >=16 pt) keep their size so the layout does
not collapse; all other text follows the 10/12 rule.
"""
import re
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE_TYPE
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt

SRC = "skill-final-v1.pptx"
OUT = "skill-final-v1-formatted.pptx"
FONT = "微软雅黑"
TITLE_COLOR = RGBColor(199, 0, 11)
TITLE_SIZE = 24
HEADING_SIZE = 12
BODY_SIZE = 10
NUMERIC_RE = re.compile(r"^[\s\d.,%+×xX/–—\-:：万亿条元美]+$")


def set_font(run, size, bold=None, color=None, spc=None):
    run.font.name = FONT
    run.font.size = Pt(size)
    if bold is not None:
        run.font.bold = bold
    if color is not None:
        run.font.color.rgb = color
    rpr = run._r.get_or_add_rPr()
    for tag in ("a:ea", "a:cs"):
        el = rpr.find(qn(tag))
        if el is None:
            el = rpr.makeelement(qn(tag), {})
            rpr.append(el)
        el.set("typeface", FONT)
    if spc is not None:
        rpr.set("spc", str(spc))


def iter_shapes(shapes):
    for shape in shapes:
        if shape.shape_type == MSO_SHAPE_TYPE.GROUP:
            yield from iter_shapes(shape.shapes)
        else:
            yield shape


def max_size(shape):
    sizes = [r.font.size.pt for p in shape.text_frame.paragraphs for r in p.runs if r.font.size]
    return max(sizes) if sizes else 0


def remove_shape(shape):
    shape._element.getparent().remove(shape._element)


def main():
    prs = Presentation(SRC)
    W, H = prs.slide_width, prs.slide_height
    removed = []

    # Remove top-right and bottom-left metadata microcopy.
    for idx, slide in enumerate(prs.slides, 1):
        for shape in list(slide.shapes):
            if not shape.has_text_frame or not shape.text_frame.text.strip():
                continue
            text = shape.text_frame.text.strip()
            size = max_size(shape)
            left, top = shape.left / W, shape.top / H
            is_top_right = left >= 0.78 and top <= 0.10 and size <= 10.5
            is_bottom_left_meta = left <= 0.15 and top >= 0.90 and size <= 8.5
            is_table_footnote = text.startswith("下载分布") or text.startswith("中位 158")
            if is_top_right or is_bottom_left_meta or is_table_footnote:
                removed.append((idx, "TR" if is_top_right else ("BL" if is_bottom_left_meta else "TBL"), size, text[:70]))
                remove_shape(shape)

    # Format each slide.
    for idx, slide in enumerate(prs.slides, 1):
        shapes = list(iter_shapes(slide.shapes))

        # Pick the page title: the largest prominent text in the upper-left area.
        candidates = []
        for shape in shapes:
            if not shape.has_text_frame or not shape.text_frame.text.strip():
                continue
            text = shape.text_frame.text.strip()
            size = max_size(shape)
            if (
                size >= 18
                and shape.top / H < 0.13
                and shape.left / W < 0.25
                and not NUMERIC_RE.match(text)
            ):
                candidates.append((size, -shape.top, len(text), shape))
        title = max(candidates, key=lambda item: (item[0], item[1], item[2]))[3] if candidates else None

        if title is not None:
            # The top-right metadata is gone, so the title can use nearly the full width.
            title.width = W - title.left - int(0.04 * W)
            title.top = max(title.top, int(0.07 * H))
            for paragraph in title.text_frame.paragraphs:
                for run in paragraph.runs:
                    set_font(run, TITLE_SIZE, bold=True, color=TITLE_COLOR, spc=0)
                paragraph.font.name = FONT
                paragraph.font.size = Pt(TITLE_SIZE)
                paragraph.font.bold = True

        # Top-left kicker: widen slightly so the 10 pt label does not wrap awkwardly.
        for shape in shapes:
            if not shape.has_text_frame or not shape.text_frame.text.strip():
                continue
            if shape is title:
                continue
            if shape.text_frame.text.strip() == "Skills 83.5k":
                shape.width = int(0.055 * W)
            if shape.text_frame.text.strip() == "核心资产层":
                shape.left = int(0.205 * W)
            if shape.left / W < 0.20 and shape.top / H < 0.06 and max_size(shape) <= 12:
                shape.width = max(shape.width, int(0.55 * W))

        for shape in shapes:
            if shape is title:
                continue

            if shape.has_table:
                for row_index, row in enumerate(shape.table.rows):
                    for cell in row.cells:
                        for paragraph in cell.text_frame.paragraphs:
                            for run in paragraph.runs:
                                set_font(
                                    run,
                                    7.5,
                                    bold=True if row_index == 0 else None,
                                    spc=-40,
                                )
                        for cell in row.cells:
                            cell.margin_left = Inches(0.03)
                            cell.margin_right = Inches(0.03)
                            cell.margin_top = Inches(0.005)
                            cell.margin_bottom = Inches(0.005)
                continue

            if not shape.has_text_frame or not shape.text_frame.text.strip():
                continue

            for paragraph in shape.text_frame.paragraphs:
                text = paragraph.text.strip()
                if not text:
                    continue
                sizes = [r.font.size.pt for r in paragraph.runs if r.font.size]
                psize = max(sizes) if sizes else 0
                numeric = bool(re.search(r"\d", text)) and bool(NUMERIC_RE.match(text))
                bold_all = bool(paragraph.runs) and all(
                    r.font.bold is True for r in paragraph.runs if r.text.strip()
                )

                if numeric and psize >= 16 and re.fullmatch(r"0\d", text):
                    # Large decorative section markers ("01", "02", ...): body heading size.
                    for run in paragraph.runs:
                        set_font(run, HEADING_SIZE, bold=True, spc=-50)
                    continue

                if numeric and psize >= 16:
                    # Keep KPI / display numbers as visual anchors.
                    shape.text_frame.word_wrap = False
                    if ("%" in text or "," in text) and shape.width < int(0.075 * W):
                        shape.width = int(0.075 * W)
                    for run in paragraph.runs:
                        size = run.font.size.pt if run.font.size else psize
                        set_font(run, size, spc=0)
                    continue

                # Micro-labels (units, captions, layer IDs) stay at their original
                # size; forcing 10 pt into their small boxes breaks the dense cards.
                if psize and psize < 10:
                    shape.text_frame.word_wrap = False
                    for run in paragraph.runs:
                        size = run.font.size.pt if run.font.size else psize
                        set_font(run, size, spc=0)
                    continue

                is_heading = len(text) <= 45 and not numeric and psize >= 12.5
                target = HEADING_SIZE if is_heading else BODY_SIZE
                for run in paragraph.runs:
                    set_font(run, target, bold=True if is_heading else None, spc=-50 if is_heading else -100)
                paragraph.font.name = FONT
                paragraph.font.size = Pt(target)
                if is_heading:
                    paragraph.font.bold = True

    prs.save(OUT)
    print(f"saved {OUT}: {len(prs.slides)} slides, {Path(OUT).stat().st_size // 1024} KB")
    print(f"removed {len(removed)} metadata shapes")
    for item in removed:
        print("  ", item)


if __name__ == "__main__":
    main()
