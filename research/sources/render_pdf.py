import pathlib
import sys

import pymupdf

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

src = pathlib.Path(sys.argv[1])
out_dir = src.parent / (src.stem + "_pages")
out_dir.mkdir(exist_ok=True)
doc = pymupdf.open(src)
print(f"{len(doc)} pages")
for i, page in enumerate(doc, 1):
    pix = page.get_pixmap(dpi=110)
    out = out_dir / f"p{i}.png"
    pix.save(out)
    print(out.name, f"{pix.width}x{pix.height}")
doc.close()
