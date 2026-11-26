import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

p = pathlib.Path(r"C:\Users\Ma Christine\Downloads\Youth Case Study - UP RESEARCH FAIR\research\sources\bamban_clup")
fname = sys.argv[1]
target = int(sys.argv[2])

text = (p / fname).read_text(encoding="utf-8")
pages = text.split("===== PAGE ")
for chunk in pages[1:]:
    num, _, body = chunk.partition("=====")
    body = body.split("\n===== PAGE")[0]
    # count lines to locate absolute line
    pass

lines = text.splitlines()
# map line index -> page
page_of = {}
cur = 0
for i, ln in enumerate(lines):
    if ln.startswith("===== PAGE "):
        cur = int(ln.replace("===== PAGE ", "").replace(" =====", "").strip())
    page_of[i + 1] = cur

pdf_page = page_of.get(target)
print(f"line {target} -> PDF page {pdf_page}")
# printed footer number on that page
block = []
for i, ln in enumerate(lines):
    if page_of[i + 1] == pdf_page:
        block.append(ln.strip())
nums = [b for b in block if re.fullmatch(r"\d{1,4}", b)]
print("printed page candidates:", nums[-3:] if nums else "none")
