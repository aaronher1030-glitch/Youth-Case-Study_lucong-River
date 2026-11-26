import re
from pathlib import Path

t = Path("docs/drafts/2026-11-19-paper-v1.0-submittable.md").read_text(encoding="utf-8")
start = t.index("## 2. Introduction")
end = t.index("## 7. References")
body = t[start:end]

PAT = r"[A-Za-z0-9\u00c0-\u017f'\u2019]+(?:[-][A-Za-z0-9\u00c0-\u017f]+)*|\u20b1[\d,]+|[%\u00b0]|MPN/100|mg/L|m\u00b3|km"

words = re.findall(PAT, body)
print("Sections 2-6, headings and tables included:", len(words))

# per-section breakdown
sections = re.split(r"(?m)^#{1,3} (\d)\. ", body)
pairs = list(zip(sections[1::2], sections[2::2]))
for num, txt in pairs:
    print(f"  §{num}: {len(re.findall(PAT, txt))}")

# tables excluded
lines = body.splitlines()
no_table, in_table = [], False
for ln in lines:
    s = ln.strip()
    if s.startswith("|"):
        in_table = True
        continue
    if in_table and not s:
        in_table = False
        continue
    if not in_table:
        no_table.append(ln)
print("Excluding tables:", len(re.findall(PAT, "\n".join(no_table))))
print(f"Budget: 2200 - {len(words)} = {2200 - len(words)} remaining")
