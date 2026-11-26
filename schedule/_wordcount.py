import re, os

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BASE)


def body(path, start_pat, end_pat):
    t = open(path, encoding="utf-8").read()
    return t[t.index(start_pat):t.index(end_pat)]


def w(lines):
    s = "\n".join(lines)
    s = re.sub(r"[#*`>|]", " ", s)
    return len([x for x in s.split() if re.search(r"[A-Za-z0-9]", x)])


def counts(txt):
    lines = txt.splitlines()
    prose = [l for l in lines if not l.strip().startswith("|")]
    return w(prose), w(lines)


for lbl, path in [
    ("v0.2", os.path.join(ROOT, "docs", "drafts", "2026-11-13-paper-draft-v0.2.md")),
    ("v0.3", os.path.join(ROOT, "docs", "drafts", "2026-11-14-paper-draft-v0.3.md")),
]:
    t = body(path, "## The Last Meter", "## Revision log")
    a, b = counts(t)
    print(f"{lbl}: prose-only {a}   incl-tables {b}")
