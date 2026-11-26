import re
import sys
from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION_START
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Emu, Inches, Pt

ROOT = Path(__file__).resolve().parents[2]
TOKEN = re.compile(r"(\*\*.+?\*\*|\*[^*]+?\*)")
CAPTION_RE = re.compile(r"^\*\*(Table|Figure)\s+\d+\.\*\*")
COLUMN_WIDTH = 3.25  # usable column width at 0.75-inch margins, 0.5-inch gutter
FULL_WIDTH = 7.0


def set_run_font(run, name="Times New Roman", size=None, bold=None, italic=None):
    run.font.name = name
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.append(rfonts)
    for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rfonts.set(qn(attr), name)
    if size is not None:
        run.font.size = Pt(size)
    if bold is not None:
        run.bold = bold
    if italic is not None:
        run.italic = italic
    # no color is ever set: all text inherits plain black


def add_runs(par, text, size=10, bold=False, italic=False):
    for tok in TOKEN.split(text):
        if not tok:
            continue
        b, i = bold, italic
        if tok.startswith("**") and tok.endswith("**") and len(tok) > 4:
            tok, b = tok[2:-2], True
        elif tok.startswith("*") and tok.endswith("*") and len(tok) > 2:
            tok, i = tok[1:-1], True
        run = par.add_run(tok)
        set_run_font(run, size=size, bold=b, italic=i)


def set_cols(section, num, space=720):
    sectpr = section._sectPr
    cols = sectpr.find(qn("w:cols"))
    if cols is None:
        cols = OxmlElement("w:cols")
        sectpr.append(cols)
    cols.set(qn("w:num"), str(num))
    cols.set(qn("w:space"), str(space))


def plain_borders(table):
    tblpr = table._tbl.tblPr
    borders = OxmlElement("w:tblBorders")
    for side in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = OxmlElement(f"w:{side}")
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), "4")
        el.set(qn("w:space"), "0")
        el.set(qn("w:color"), "auto")
        borders.append(el)
    tblpr.append(borders)
    layout = OxmlElement("w:tblLayout")
    layout.set(qn("w:type"), "fixed")
    tblpr.append(layout)
    mar = OxmlElement("w:tblCellMar")
    for side, val in (("top", 20), ("left", 60), ("bottom", 20), ("right", 60)):
        el = OxmlElement(f"w:{side}")
        el.set(qn("w:w"), str(val))
        el.set(qn("w:type"), "dxa")
        mar.append(el)
    tblpr.append(mar)


def repeat_header(row):
    trpr = row._tr.get_or_add_trPr()
    el = OxmlElement("w:tblHeader")
    el.set(qn("w:val"), "true")
    trpr.append(el)
    trpr.append(OxmlElement("w:cantSplit"))


def add_table(doc, rows, total_width=COLUMN_WIDTH):
    header, body = rows[0], rows[1:]
    ncols = len(header)
    weights = []
    for i in range(ncols):
        vals = [len(r[i]) for r in rows if i < len(r)]
        weights.append(max(0.5, 0.6 * max(vals) + 0.4 * (sum(vals) / len(vals))))
    total = sum(weights)
    widths = [max(0.4, total_width * w / total) for w in weights]
    widths = [w * total_width / sum(widths) for w in widths]

    size = 8.0 if ncols >= 4 else 8.5
    table = doc.add_table(rows=0, cols=ncols)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    plain_borders(table)
    for i, w in enumerate(widths):
        table.columns[i].width = Inches(w)
    grid = table._tbl.tblGrid
    for i, gc in enumerate(grid.gridCol_lst):
        gc.w = Inches(widths[i])

    hr = table.add_row()
    repeat_header(hr)
    for i, text in enumerate(header):
        cell = hr.cells[i]
        cell.width = Inches(widths[i])
        par = cell.paragraphs[0]
        par.paragraph_format.space_before = Pt(0)
        par.paragraph_format.space_after = Pt(0)
        par.paragraph_format.line_spacing = 1.0
        add_runs(par, text, size=size, bold=True)
    for row in body:
        tr = table.add_row()
        trpr = tr._tr.get_or_add_trPr()
        trpr.append(OxmlElement("w:cantSplit"))
        for i in range(ncols):
            cell = tr.cells[i]
            cell.width = Inches(widths[i])
            par = cell.paragraphs[0]
            par.paragraph_format.space_before = Pt(0)
            par.paragraph_format.space_after = Pt(0)
            par.paragraph_format.line_spacing = 1.0
            text = row[i] if i < len(row) else ""
            add_runs(par, text, size=size)

    # keep the table on one page: every row but the last sticks to the next
    for r in table.rows[:-1]:
        for c in r.cells:
            for par in c.paragraphs:
                par.paragraph_format.keep_with_next = True

    spacer = doc.add_paragraph()
    spacer.paragraph_format.space_before = Pt(0)
    spacer.paragraph_format.space_after = Pt(4)
    spacer.paragraph_format.line_spacing = 1.0
    if spacer.runs:
        spacer.runs[0].font.size = Pt(4)


def add_page_number_footer(section):
    par = section.footer.paragraphs[0]
    par.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = par.add_run("Page ")
    set_run_font(run, size=9)
    fld = OxmlElement("w:fldSimple")
    fld.set(qn("w:instr"), "PAGE")
    r = OxmlElement("w:r")
    t = OxmlElement("w:t")
    t.text = "1"
    r.append(t)
    fld.append(r)
    par._p.append(fld)


def add_figure(doc, alt, rel):
    """In-column figure, centered, 3.25 inches wide, caption below (V7 style)."""
    img = ROOT / rel
    if not img.exists():
        raise FileNotFoundError(img)
    holder = doc.add_paragraph()
    holder.alignment = WD_ALIGN_PARAGRAPH.CENTER
    holder.paragraph_format.space_before = Pt(6)
    holder.paragraph_format.space_after = Pt(2)
    holder.paragraph_format.line_spacing = 1.0
    holder.paragraph_format.keep_with_next = True
    holder.add_run().add_picture(str(img), width=Inches(COLUMN_WIDTH))
    cap = doc.add_paragraph()
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap.paragraph_format.space_before = Pt(0)
    cap.paragraph_format.space_after = Pt(6)
    cap.paragraph_format.line_spacing = 1.0
    add_runs(cap, alt, size=9, bold=True)


def parse(md_path):
    lines = Path(md_path).read_text(encoding="utf-8").splitlines()
    blocks, i = [], 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if line.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                raw = lines[i].strip()
                if not re.match(r"^\|[\s:\-|]+\|$", raw):
                    rows.append([c.strip() for c in raw.strip("|").split("|")])
                i += 1
            if rows:
                blocks.append(("table", rows))
            continue
        m = re.match(r"^!\[(.*?)\]\((.*?)\)\s*$", line)
        if m:
            blocks.append(("image", (m.group(1), m.group(2))))
            i += 1
            continue
        m = re.match(r"^(#{1,3})\s+(.*)$", line)
        if m:
            blocks.append(("h" + str(len(m.group(1))), m.group(2).strip()))
            i += 1
            continue
        if line.startswith("- "):
            blocks.append(("bullet", line[2:].strip()))
            i += 1
            continue
        para = [line.strip()]
        i += 1
        while i < len(lines) and lines[i].strip() and not lines[i].startswith(("|", "#", "![")):
            para.append(lines[i].strip())
            i += 1
        blocks.append(("p", " ".join(para)))
    return blocks


def ref_par(doc, text, size=9):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.0
    p.paragraph_format.keep_together = True
    p.paragraph_format.left_indent = Inches(0.18)
    p.paragraph_format.first_line_indent = Inches(-0.18)
    add_runs(p, text, size=size)


def body_par(doc, text, size=10, indent_hanging=False):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(5)
    p.paragraph_format.line_spacing = 1.0
    if indent_hanging:
        p.paragraph_format.left_indent = Inches(0.18)
        p.paragraph_format.first_line_indent = Inches(-0.18)
    add_runs(p, text, size=size)
    return p


def build(md_path, out_path):
    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Inches(8.5), Inches(11)
    sec.left_margin = sec.right_margin = Inches(0.75)
    sec.top_margin = sec.bottom_margin = Inches(1.0)
    set_cols(sec, 1)
    add_page_number_footer(sec)

    normal = doc.styles["Normal"]
    normal.font.name = "Times New Roman"
    normal.font.size = Pt(10)
    normal.element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
    normal.paragraph_format.line_spacing = 1.0

    state = "title"      # title -> abstract -> keywords -> body
    refs = False
    honor = False
    decl = False
    ref_no = 0
    for kind, data in parse(md_path):
        if kind == "h1":
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(10)
            p.paragraph_format.line_spacing = 1.0
            add_runs(p, data, size=18)
        elif kind == "h2":
            head = data.strip().lower()
            if head == "abstract":
                state = "abstract"
                p = doc.add_paragraph()
                p.paragraph_format.space_before = Pt(12)
                p.paragraph_format.space_after = Pt(2)
                p.paragraph_format.line_spacing = 1.0
                add_runs(p, "Abstract", size=9, bold=True)
                continue
            if head == "keywords":
                state = "keywords"
                continue
            if head.startswith("references") or "references" in head:
                refs = True
            else:
                refs = False
            if head.startswith("honor code"):
                honor = True
            if "declaration" in head:
                decl = True
            if state in ("abstract", "keywords"):
                # first numbered heading: switch to two columns before it
                new = doc.add_section(WD_SECTION_START.CONTINUOUS)
                set_cols(new, 2)
                state = "body"
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(10)
            p.paragraph_format.space_after = Pt(5)
            p.paragraph_format.line_spacing = 1.0
            p.paragraph_format.keep_with_next = True
            add_runs(p, data, size=11, bold=True)
        elif kind == "h3":
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.space_after = Pt(3)
            p.paragraph_format.line_spacing = 1.0
            p.paragraph_format.keep_with_next = True
            add_runs(p, data, size=10, bold=True)
        elif kind == "p":
            if state == "title":
                p = doc.add_paragraph()
                p.paragraph_format.space_before = Pt(0)
                p.paragraph_format.space_after = Pt(2)
                p.paragraph_format.line_spacing = 1.0
                add_runs(p, data, size=10)
                continue
            if refs:
                ref_no += 1
                ref_par(doc, f"{ref_no}. {data}")
                continue
            if state == "keywords":
                p = doc.add_paragraph()
                p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                p.paragraph_format.space_before = Pt(2)
                p.paragraph_format.space_after = Pt(6)
                p.paragraph_format.line_spacing = 1.0
                add_runs(p, "Keywords: ", size=9, bold=True)
                add_runs(p, data, size=9, italic=True)
                continue
            if CAPTION_RE.match(data):
                p = doc.add_paragraph()
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p.paragraph_format.space_before = Pt(0)
                p.paragraph_format.space_after = Pt(4)
                p.paragraph_format.line_spacing = 1.0
                p.paragraph_format.keep_with_next = True
                add_runs(p, data, size=9, bold=True)
                continue
            if honor:
                p = doc.add_paragraph()
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                p.paragraph_format.space_before = Pt(12) if (data.startswith("**") and data.endswith("**")) else Pt(0)
                p.paragraph_format.space_after = Pt(2)
                p.paragraph_format.line_spacing = 1.0
                add_runs(p, data, size=10)
                continue
            if decl:
                p = doc.add_paragraph()
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                p.paragraph_format.space_before = Pt(0)
                p.paragraph_format.space_after = Pt(3)
                p.paragraph_format.line_spacing = 1.0
                add_runs(p, data, size=9)
                continue
            body_par(doc, data)
        elif kind == "bullet":
            body_par(doc, "\u2013  " + data, indent_hanging=True)
        elif kind == "table":
            add_table(doc, data)
        elif kind == "image":
            alt, rel = data
            add_figure(doc, alt, rel)
            continue

    doc.core_properties.title = "Eighty Times the Limit: A Shed-Level Manure Service and Load-Balance Model for the Lucong River"
    doc.core_properties.subject = "RF2027 Case Study Competition (two-column journal format)"
    doc.save(out_path)
    print("saved", out_path)


if __name__ == "__main__":
    build(sys.argv[1], sys.argv[2])
