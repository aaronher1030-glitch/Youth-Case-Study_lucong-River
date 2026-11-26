import re
from pathlib import Path

t = Path("docs/drafts/2026-11-18-paper-v0.4-journal.md").read_text(encoding="utf-8")

word_re = r"[A-Za-z0-9\u00c0-\u017f'\u2019]+(?:[-][A-Za-z0-9\u00c0-\u017f]+)*|\u20b1[\d,]+|\u20b1"

def count(text):
    return len(re.findall(word_re, text))

abstract_start = t.index("## Abstract")
abstract_end = t.index("## Keywords")
keywords_end = t.index("## 1. Introduction")
body_start = t.index("## 1. Introduction")
body_end = t.index("## References")

abstract = t[abstract_start + len("## Abstract"):abstract_end]
body = t[body_start:body_end]
print("Abstract:", count(abstract))
print("Body sections 1-6 (headings, captions, tables included):", count(body))
print("Abstract + body:", count(abstract) + count(body))

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
print("Body excluding tables:", count("\n".join(no_table)))
