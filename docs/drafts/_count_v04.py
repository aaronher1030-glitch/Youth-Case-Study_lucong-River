import re
from pathlib import Path

t = Path("docs/drafts/2026-11-18-paper-v0.4-submittable.md").read_text(encoding="utf-8")
start = t.index("## 2.")
end = t.index("## 4. References")
body = t[start:end]

# word = runs of word characters (letters, digits, underscore, apostrophe),
# plus currency/percent/degree tokens; hyphens inside words kept via \w-
words = re.findall(r"[A-Za-z0-9\u00c0-\u017f'\u2019]+(?:[-][A-Za-z0-9\u00c0-\u017f]+)*|\u20b1|\u20b1[\d,]+|[%\u00b0]|MPN/100|mg/L|m\u00b3|km|km\u00b2", body)
print("Sections 2-6, headings and tables included:", len(words))

# tables excluded variant
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
body2 = "\n".join(no_table)
words2 = re.findall(r"[A-Za-z0-9\u00c0-\u017f'\u2019]+(?:[-][A-Za-z0-9\u00c0-\u017f]+)*|\u20b1[\d,]+", body2)
print("Excluding tables:", len(words2))
