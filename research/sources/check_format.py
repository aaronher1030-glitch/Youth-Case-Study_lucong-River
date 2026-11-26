"""Format check for the RF2027 paper DOCX: page, margins, fonts, sizes, spacing."""
import sys
from collections import Counter
from docx import Document
from docx.shared import Pt

path = sys.argv[1] if len(sys.argv) > 1 else 'docs/PAPER_LUCONG_V1.0_FULL.docx'
doc = Document(path)

sec = doc.sections[0]
print('page  %.3f x %.3f in' % (sec.page_width.inches, sec.page_height.inches))
print('margin L %.2f R %.2f T %.2f B %.2f in' % (
    sec.left_margin.inches, sec.right_margin.inches,
    sec.top_margin.inches, sec.bottom_margin.inches))

fonts, sizes, spacing, missing_font = Counter(), Counter(), Counter(), []
body_missing_spacing = 0
for p in doc.paragraphs:
    text = p.text.strip()
    ls = p.paragraph_format.line_spacing
    spacing[str(ls)] += 1
    for r in p.runs:
        if not r.text.strip():
            continue
        fonts[r.font.name] += 1
        sizes[r.font.size.pt if r.font.size else None] += 1
        if r.font.name != 'Times New Roman':
            missing_font.append((r.font.name, r.text[:40]))
    if text and len(text) > 120 and ls is None:
        body_missing_spacing += 1

tfonts, tsizes = Counter(), Counter()
for t in doc.tables:
    for row in t.rows:
        for cell in row.cells:
            for p in cell.paragraphs:
                for r in p.runs:
                    if r.text.strip():
                        tfonts[r.font.name] += 1
                        tsizes[r.font.size.pt if r.font.size else None] += 1

print('body fonts ', dict(fonts))
print('body sizes ', dict(sizes))
print('body spacing', dict(spacing))
print('long paragraphs with no explicit spacing:', body_missing_spacing)
print('table fonts ', dict(tfonts))
print('table sizes ', dict(tsizes))
if missing_font:
    print('non-TNR runs:', missing_font[:8], '...' if len(missing_font) > 8 else '')
