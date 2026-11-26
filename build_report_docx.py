# Build DEEP_RESEARCH_STREAM3_TECH_STACK_CLEANING.docx from the markdown report.
import re
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

BASE = r"C:\Users\Ma Christine\Downloads\Youth Case Study - UP RESEARCH FAIR"
MD = BASE + r"\DEEP_RESEARCH_STREAM3_TECH_STACK_CLEANING.md"
OUT = BASE + r"\DEEP_RESEARCH_STREAM3_TECH_STACK_CLEANING.docx"

ACCENT = RGBColor(0x1F, 0x4E, 0x79)
GRAY = RGBColor(0x59, 0x59, 0x59)
HDR_FILL = "D9E2F3"

TOK = re.compile(r"(\*\*[^*]+\*\*|\*[^*\s][^*]*\*|`[^`]+`)")

def set_eastasia(style, name="Calibri"):
    rpr = style.element.get_or_add_rPr()
    rf = rpr.find(qn("w:rFonts"))
    if rf is None:
        rf = OxmlElement("w:rFonts")
        rpr.append(rf)
    rf.set(qn("w:ascii"), name)
    rf.set(qn("w:hAnsi"), name)
    rf.set(qn("w:eastAsia"), name)

def add_runs(par, text, size=None):
    for part in TOK.split(text):
        if not part:
            continue
        if part.startswith("**") and part.endswith("**"):
            r = par.add_run(part[2:-2]); r.bold = True
        elif part.startswith("`") and part.endswith("`"):
            r = par.add_run(part[1:-1]); r.font.name = "Consolas"
            r._element.rPr.rFonts.set(qn("w:eastAsia"), "Consolas")
        elif part.startswith("*") and part.endswith("*") and len(part) > 2:
            r = par.add_run(part[1:-1]); r.italic = True
        else:
            r = par.add_run(part)
        if size is not None:
            r.font.size = Pt(size)

def fix_widths(table, widths):
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    tbl = table._tbl
    tblPr = tbl.tblPr
    layout = tblPr.find(qn("w:tblLayout"))
    if layout is None:
        layout = OxmlElement("w:tblLayout")
        tblPr.append(layout)
    layout.set(qn("w:type"), "fixed")
    for row in table.rows:
        for i, cell in enumerate(row.cells):
            cell.width = Inches(widths[min(i, len(widths) - 1)])

def shade(cell, fill):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:fill"), fill)
    tcPr.append(shd)

def repeat_header(table):
    trPr = table.rows[0]._tr.get_or_add_trPr()
    th = OxmlElement("w:tblHeader")
    trPr.append(th)

def style_table(table):
    try:
        table.style = "Table Grid"
    except KeyError:
        pass
    for i, cell in enumerate(table.rows[0].cells):
        shade(cell, HDR_FILL)
        for p in cell.paragraphs:
            for r in p.runs:
                r.bold = True
    repeat_header(table)
    for row in table.rows:
        for cell in row.cells:
            for p in cell.paragraphs:
                p.paragraph_format.space_before = Pt(1)
                p.paragraph_format.space_after = Pt(1)
                for r in p.runs:
                    r.font.size = Pt(9)

WIDTHS = {
    5: [0.7, 1.5, 1.6, 1.2, 1.5],
    4: [1.4, 2.2, 1.6, 1.3],
    3: [1.0, 3.9, 1.6],
    2: [5.3, 1.2],
}

doc = Document()
sec = doc.sections[0]
sec.page_width, sec.page_height = Inches(8.5), Inches(11)
for a in ("left_margin", "right_margin", "top_margin", "bottom_margin"):
    setattr(sec, a, Inches(1))

n = doc.styles["Normal"]
n.font.name = "Calibri"; n.font.size = Pt(11)
n.paragraph_format.space_after = Pt(6)
set_eastasia(n)
for name, size in (("Title", 22), ("Heading 1", 15), ("Heading 2", 12.5), ("Heading 3", 11.5)):
    st = doc.styles[name]
    st.font.name = "Calibri"; st.font.size = Pt(size); st.font.bold = True
    st.font.color.rgb = ACCENT if name != "Title" else RGBColor(0x11, 0x2A, 0x46)
    st.paragraph_format.space_before = Pt(14 if name != "Title" else 0)
    st.paragraph_format.space_after = Pt(6)
    set_eastasia(st)
lb = doc.styles["List Bullet"]
lb.font.name = "Calibri"; lb.font.size = Pt(11); set_eastasia(lb)
ln = doc.styles["List Number"]
ln.font.name = "Calibri"; ln.font.size = Pt(11); set_eastasia(ln)

with open(MD, encoding="utf-8") as f:
    lines = f.read().splitlines()

i = 0
title_done = False
in_extract = False
while i < len(lines):
    line = lines[i]
    stripped = line.strip()

    if not stripped or stripped == "---":
        i += 1
        continue

    # tables
    if stripped.startswith("|"):
        rows = []
        while i < len(lines) and lines[i].strip().startswith("|"):
            cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
            if not all(re.fullmatch(r":?-{3,}:?", c) for c in cells):
                rows.append(cells)
            i += 1
        if rows:
            ncols = max(len(r) for r in rows)
            t = doc.add_table(rows=len(rows), cols=ncols)
            for ri, r in enumerate(rows):
                for ci in range(ncols):
                    txt = r[ci] if ci < len(r) else ""
                    p = t.rows[ri].cells[ci].paragraphs[0]
                    add_runs(p, txt)
            style_table(t)
            fix_widths(t, WIDTHS.get(ncols, [6.5 / ncols] * ncols))
            doc.add_paragraph()
        continue

    # headings
    if stripped.startswith("#### "):
        doc.add_heading(re.sub(r"\*\*", "", stripped[5:]), level=3)
        i += 1
        continue
    if stripped.startswith("### "):
        txt = stripped[4:]
        in_extract = txt.startswith("[")
        doc.add_heading(re.sub(r"\*\*", "", txt), level=3)
        i += 1
        continue
    if stripped.startswith("## "):
        txt = stripped[3:]
        in_extract = txt.startswith("Source Extracts")
        doc.add_heading(re.sub(r"\*\*", "", txt), level=2)
        i += 1
        continue
    if stripped.startswith("# ") and not title_done:
        p = doc.add_paragraph(style="Title")
        add_runs(p, stripped[2:])
        title_done = True
        i += 1
        continue
    if stripped.startswith("# "):
        doc.add_heading(stripped[2:], level=1)
        i += 1
        continue

    # blockquote subtitle
    if stripped.startswith("> "):
        p = doc.add_paragraph()
        r = p.add_run(stripped[2:])
        r.italic = True; r.font.size = Pt(10); r.font.color.rgb = GRAY
        i += 1
        continue

    # checkbox items
    m = re.match(r"- \[ \] (.*)", stripped)
    if m:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.25)
        p.paragraph_format.space_after = Pt(3)
        r = p.add_run("\u2610  ")
        r.font.size = Pt(11)
        add_runs(p, m.group(1))
        i += 1
        continue

    # numbered list
    m = re.match(r"(\d+)\. (.*)", stripped)
    if m and len(m.group(1)) <= 1:
        p = doc.add_paragraph(style="List Number")
        add_runs(p, m.group(2))
        i += 1
        continue

    # bullets
    if stripped.startswith("- "):
        p = doc.add_paragraph(style="List Bullet")
        p.paragraph_format.space_after = Pt(3)
        add_runs(p, stripped[2:])
        i += 1
        continue

    # bibliography entries
    if re.match(r"\[\d+\]", stripped):
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.3)
        p.paragraph_format.first_line_indent = Inches(-0.3)
        p.paragraph_format.space_after = Pt(2)
        add_runs(p, stripped, size=9)
        i += 1
        continue

    p = doc.add_paragraph()
    add_runs(p, stripped)
    i += 1

doc.save(OUT)
print("saved", OUT)

# verify: no markdown artifacts remain
d2 = Document(OUT)
bad = [p.text for p in d2.paragraphs if "**" in p.text or p.text.strip().startswith("|")]
print("paragraphs:", len(d2.paragraphs), "tables:", len(d2.tables), "artifacts:", len(bad))
for t in d2.tables:
    print("table", len(t.rows), "x", len(t.columns))
