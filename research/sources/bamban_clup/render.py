import pathlib
import sys

import pymupdf

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

p = pathlib.Path(r"C:\Users\Ma Christine\Downloads\Youth Case Study - UP RESEARCH FAIR\research\sources\bamban_clup")
pdf = p / sys.argv[1]
out_dir = p / "pages_png"
out_dir.mkdir(exist_ok=True)

doc = pymupdf.open(pdf)
for spec in sys.argv[2:]:
    if "-" in spec:
        a, b = spec.split("-")
        nums = range(int(a), int(b) + 1)
    else:
        nums = [int(spec)]
    for n in nums:
        page = doc[n - 1]
        pix = page.get_pixmap(dpi=160)
        out = out_dir / f"{pdf.stem}_p{n:03d}.png"
        pix.save(out)
        print(f"{out.name}  {pix.width}x{pix.height}")
doc.close()
