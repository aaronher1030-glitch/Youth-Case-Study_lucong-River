import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

p = pathlib.Path(r"C:\Users\Ma Christine\Downloads\Youth Case Study - UP RESEARCH FAIR\research\sources\bamban_clup")
fname = sys.argv[1]
start = int(sys.argv[2])
end = int(sys.argv[3])
lines = (p / fname).read_text(encoding="utf-8").splitlines()
for i in range(max(0, start - 1), min(len(lines), end)):
    text = lines[i].replace("\u200b", "").replace("\ufffd", "'")
    print(f"{i + 1}: {text}")
