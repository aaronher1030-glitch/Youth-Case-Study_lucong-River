import re
import sys
from pathlib import Path

from docx import Document
from docx.enum.section import WD_ORIENT
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

ROOT = Path(__file__).resolve().parents[2]
INK = RGBColor(0x00, 0x00, 0x00)
GREY = RGBColor(0x00, 0x00, 0x00)
TOKEN = re.compile(r"(\*\*.+?\*\*|\*[^*]+?\*)")


def set_run_font(run, name="Times New Roman", size=None, bold=None, italic=None, color=None):
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
    if color is not None:
        run.font.color.rgb = color


def add_runs(par, text, size=12, bold=False, italic=False, color=None):
    for tok in TOKEN.split(text):
        if not tok:
            continue
        b, i = bold, italic
        if tok.startswith("**") and tok.endswith("**") and len(tok) > 4:
            tok, b = tok[2:-2], True
        elif tok.startswith("*") and tok.endswith("*") and len(tok) > 2:
            tok, i = tok[1:-1], True
        run = par.add_run(tok)
        set_run_font(run, size=size, bold=b, italic=i, color=color)


def shade(cell, fill):
    tcpr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill)
    tcpr.append(shd)


def cell_margins(table, top=50, bottom=50, left=80, right=80):
    tblpr = table._tbl.tblPr
    mar = OxmlElement("w:tblCellMar")
    for side, val in (("top", top), ("left", left), ("bottom", bottom), ("right", right)):
        el = OxmlElement(f"w:{side}")
        el.set(qn("w:w"), str(val))
        el.set(qn("w:type"), "dxa")
        mar.append(el)
    tblpr.append(mar)


def fixed_layout(table, widths):
    table.autofit = False
    tblpr = table._tbl.tblPr
    layout = OxmlElement("w:tblLayout")
    layout.set(qn("w:type"), "fixed")
    tblpr.append(layout)
    for i, w in enumerate(widths):
        table.columns[i].width = Inches(w)
    grid = table._tbl.tblGrid
    for i, gc in enumerate(grid.gridCol_lst):
        gc.w = Inches(widths[i])


def repeat_header(row):
    trpr = row._tr.get_or_add_trPr()
    el = OxmlElement("w:tblHeader")
    el.set(qn("w:val"), "true")
    trpr.append(el)
    cant = OxmlElement("w:cantSplit")
    trpr.append(cant)


def add_table(doc, rows):
    header, body = rows[0], rows[1:]
    ncols = len(header)
    size = 9.6
    longest = [max(len(r[i]) if i < len(r) else 0 for r in rows) for i in range(ncols)]
    if max(longest) <= 18:
        widths = [6.5 / ncols] * ncols
    else:
        weights = []
        for i in range(ncols):
            vals = [len(r[i]) for r in rows if i < len(r)]
            weights.append(max(0.5, 0.6 * max(vals) + 0.4 * (sum(vals) / len(vals))))
        total = sum(weights)
        widths = [6.5 * w / total for w in weights]
        # no column narrower than its longest word, or words break mid-word
        for i in range(ncols):
            words = re.findall(r"[A-Za-z0-9]+", " ".join(r[i] for r in rows if i < len(r)))
            longest_word = max(len(w) for w in words) if words else 4
            wmin = 0.16 + 0.070 * longest_word * (8.6 / size)
            if widths[i] < wmin:
                excess = wmin - widths[i]
                widths[i] = wmin
                donors = [j for j in range(ncols) if widths[j] > wmin + 0.05 and j != i]
                pool = sum(widths[j] for j in donors)
                for j in donors:
                    widths[j] -= excess * widths[j] / pool
        scale = 6.5 / sum(widths)
        widths = [w * scale for w in widths]

    table = doc.add_table(rows=0, cols=ncols)
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    fixed_layout(table, widths)
    cell_margins(table)

    hr = table.add_row()
    repeat_header(hr)
    for i, text in enumerate(header):
        cell = hr.cells[i]
        cell.width = Inches(widths[i])
        par = cell.paragraphs[0]
        par.paragraph_format.space_before = Pt(0)
        par.paragraph_format.space_after = Pt(0)
        par.paragraph_format.line_spacing = 1.0
        par.paragraph_format.keep_with_next = True
        add_runs(par, text, size=size, bold=True)
    for r_idx, row in enumerate(body):
        tr = table.add_row()
        trpr = tr._tr.get_or_add_trPr()
        trpr.append(OxmlElement("w:cantSplit"))
        is_last = r_idx == len(body) - 1
        for i in range(ncols):
            cell = tr.cells[i]
            cell.width = Inches(widths[i])
            par = cell.paragraphs[0]
            par.paragraph_format.space_before = Pt(0)
            par.paragraph_format.space_after = Pt(0)
            par.paragraph_format.line_spacing = 1.0
            if not is_last:
                par.paragraph_format.keep_with_next = True
            text = row[i] if i < len(row) else ""
            add_runs(par, text, size=size)

    spacer = doc.add_paragraph()
    spacer.paragraph_format.space_after = Pt(0)
    spacer.paragraph_format.line_spacing = 1.0
    for r in spacer.runs:
        r.font.size = Pt(4)


def add_page_number_footer(section):
    par = section.footer.paragraphs[0]
    par.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = par.add_run("Page ")
    set_run_font(run, size=9, color=GREY)
    for instr in ("PAGE", "NUMPAGES"):
        fld = OxmlElement("w:fldSimple")
        fld.set(qn("w:instr"), instr)
        r = OxmlElement("w:r")
        t = OxmlElement("w:t")
        t.text = "1"
        r.append(t)
        fld.append(r)
        par._p.append(fld)
        if instr == "PAGE":
            sep = par.add_run(" of ")
            set_run_font(sep, size=9, color=GREY)


def add_header(section, text="RF2027 Case Study  |  Section 2  |  Lucong River, Concepcion, Tarlac"):
    par = section.header.paragraphs[0]
    par.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = par.add_run(text)
    set_run_font(run, size=8, color=GREY)


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
        m = re.match(r"^\d+\.\s+(.*)$", line)
        if m:
            blocks.append(("num", m.group(1).strip()))
            i += 1
            continue
        para = [line.strip()]
        i += 1
        while (
            i < len(lines)
            and lines[i].strip()
            and not lines[i].startswith(("|", "#", "!["))
            and not re.match(r"^\d+\.\s", lines[i])
            and not lines[i].startswith("- ")
        ):
            para.append(lines[i].strip())
            i += 1
        blocks.append(("p", " ".join(para)))
    return blocks


def build(md_path, out_path, header_text=None, title=None):
    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Inches(8.5), Inches(11)
    sec.left_margin = sec.right_margin = Inches(1.0)
    sec.top_margin = sec.bottom_margin = Inches(1.0)
    if header_text:
        add_header(sec, header_text)
    else:
        add_header(sec)
    add_page_number_footer(sec)

    normal = doc.styles["Normal"]
    normal.font.name = "Times New Roman"
    normal.font.size = Pt(12)
    normal.element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
    normal.paragraph_format.line_spacing = 1.5
    normal.paragraph_format.space_after = Pt(6)

    refs = False
    for kind, data in parse(md_path):
        if kind == "h1":
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(10)
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.keep_with_next = True
            add_runs(p, data, size=18, bold=True, color=INK)
            refs = False
            pPr = p._p.get_or_add_pPr()
            bdr = OxmlElement("w:pBdr")
            bottom = OxmlElement("w:bottom")
            bottom.set(qn("w:val"), "single")
            bottom.set(qn("w:sz"), "10")
            bottom.set(qn("w:space"), "4")
            bottom.set(qn("w:color"), "auto")
            bdr.append(bottom)
            pPr.append(bdr)
        elif kind == "h2":
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(16)
            p.paragraph_format.space_after = Pt(6)
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.keep_with_next = True
            add_runs(p, data, size=13.5, bold=True, color=INK)
            refs = bool(re.fullmatch(r"\d+\.\s*References", data.strip(), re.I))
        elif kind == "h3":
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(10)
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.keep_with_next = True
            add_runs(p, data, size=12, bold=True)
        elif kind == "p":
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            if re.match(r"\*\*[^*]+:\*\*", data):
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                p.paragraph_format.space_after = Pt(3)
                p.paragraph_format.line_spacing = 1.15
                add_runs(p, data, size=12)
            elif refs:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                p.paragraph_format.left_indent = Inches(0.5)
                p.paragraph_format.first_line_indent = Inches(-0.5)
                p.paragraph_format.line_spacing = 1.5
                p.paragraph_format.space_after = Pt(2)
                add_runs(p, data, size=12)
            else:
                add_runs(p, data, size=12)
                if re.match(r"^\*\*Table\s+\d", data):
                    p.paragraph_format.keep_with_next = True
        elif kind == "bullet":
            p = doc.add_paragraph(style="List Bullet")
            add_runs(p, data, size=12)
        elif kind == "num":
            p = doc.add_paragraph(style="List Number")
            add_runs(p, data, size=12)
        elif kind == "table":
            add_table(doc, data)
        elif kind == "image":
            alt, rel = data
            img = ROOT / rel
            wide = img.with_name(img.stem + "_wide" + img.suffix)
            if wide.exists():
                img = wide
            if not img.exists():
                raise FileNotFoundError(img)
            holder = doc.add_paragraph()
            holder.alignment = WD_ALIGN_PARAGRAPH.CENTER
            holder.paragraph_format.space_before = Pt(6)
            holder.paragraph_format.space_after = Pt(4)
            holder.paragraph_format.keep_with_next = True
            holder.add_run().add_picture(str(img), width=Inches(5.6))
            cap = doc.add_paragraph()
            cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            cap.paragraph_format.space_after = Pt(12)
            cap.paragraph_format.line_spacing = 1.0
            add_runs(cap, alt, size=9, italic=True, color=GREY)

    doc.core_properties.title = title or "Target Site Profile and Root-Cause Diagnosis: Lucong River"
    doc.core_properties.subject = "RF2027 Case Study Competition, Section 2"
    doc.save(out_path)
    print("saved", out_path)


if __name__ == "__main__":
    extra = sys.argv[3:]
    build(
        sys.argv[1],
        sys.argv[2],
        header_text=extra[0] if len(extra) > 0 else None,
        title=extra[1] if len(extra) > 1 else None,
    )

