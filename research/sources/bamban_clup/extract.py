"""Extract text from the Bamban CLUP PDF set downloaded from the LGU site.

Usage:  python extract.py
Writes one .txt per PDF in this folder and prints a summary table.
"""
import pathlib
import sys

import fitz  # PyMuPDF

HERE = pathlib.Path(__file__).parent


def extract(pdf_path: pathlib.Path) -> tuple[int, int, str]:
    doc = fitz.open(pdf_path)
    pages = []
    chars = 0
    for page in doc:
        text = page.get_text("text")
        chars += len(text.strip())
        pages.append(f"\n\n===== PAGE {page.number + 1} =====\n{text}")
    doc.close()
    return len(pages), chars, "".join(pages)


def main() -> int:
    rows = []
    for pdf in sorted(HERE.glob("*.pdf")):
        n_pages, chars, text = extract(pdf)
        out = pdf.with_suffix(".txt")
        out.write_text(text, encoding="utf-8")
        rows.append((pdf.name, n_pages, chars, out.name))

    print(f"{'file':<42}{'pages':>7}{'chars':>10}  text?")
    for name, n_pages, chars, _ in rows:
        flag = "yes" if chars > 200 * n_pages else "SCANNED/EMPTY"
        print(f"{name:<42}{n_pages:>7}{chars:>10}  {flag}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
