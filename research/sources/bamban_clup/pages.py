import pathlib
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

p = pathlib.Path(r"C:\Users\Ma Christine\Downloads\Youth Case Study - UP RESEARCH FAIR\research\sources\bamban_clup")
fname = sys.argv[1]
text = (p / fname).read_text(encoding="utf-8")
pages = text.split("===== PAGE ")
print(f"{'page':>5} {'chars':>7}  first line")
for chunk in pages[1:]:
    num, _, body = chunk.partition("=====")
    body = body.strip()
    first = body.splitlines()[0][:80] if body else ""
    print(f"{num.strip():>5} {len(body):>7}  {first}")
