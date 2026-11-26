"""Build the RF2027 3:4 portrait poster for the Lucong River entry.

Output: docs/POSTER_LUCONG_V1.png (2700 x 3600 px, exactly 3:4).
Run: python research/sources/make_poster.py
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
W, H = 2700, 3600
M = 130  # margin

INK = (26, 32, 38)
TEAL = (15, 76, 92)
RED = (176, 58, 30)
SAND = (247, 243, 236)
MIST = (238, 242, 243)
GRAY = (108, 116, 124)
RULE = (214, 214, 210)
WHITE = (255, 255, 255)

FONT_DIR = Path("C:/Windows/Fonts")
REG = str(FONT_DIR / "times.ttf")
BOLD = str(FONT_DIR / "timesbd.ttf")
ITAL = str(FONT_DIR / "timesi.ttf")


def f(size, bold=False, italic=False):
    path = BOLD if bold else (ITAL if italic else REG)
    return ImageFont.truetype(path, size)


def wrap(draw, text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_par(draw, xy, text, font, max_w, fill=INK, leading=1.42, align="left"):
    x, y = xy
    lines = wrap(draw, text, font, max_w)
    step = int(font.size * leading)
    for ln in lines:
        if align == "center":
            tw = draw.textlength(ln, font=font)
            draw.text((x + (max_w - tw) / 2, y), ln, font=font, fill=fill)
        else:
            draw.text((x, y), ln, font=font, fill=fill)
        y += step
    return y


def eyebrow(draw, x, y, text, size=30):
    draw.text((x, y), " ".join(text.upper()), font=f(size, bold=True), fill=GRAY)


def section(draw, x, y, num, label, width):
    """Numbered section head with a rule beneath."""
    head = f(58, bold=True)
    draw.text((x, y), f"{num}", font=f(58, bold=True), fill=RED)
    nw = draw.textlength(num, font=head)
    draw.text((x + nw + 26, y), label, font=head, fill=TEAL)
    draw.line([(x, y + 84), (x + width, y + 84)], fill=TEAL, width=5)
    return y + 116


def main():
    img = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(img)

    # ---------------- header ----------------
    y = M
    eyebrow(d, M, y, "RF2027 Case Study Competition  ·  Concepcion, Tarlac")
    y += 62

    d.text((M, y), "Eighty Times the Limit", font=f(132, bold=True), fill=INK)
    y += 168

    d.text(
        (M, y),
        "A shed-level waste service for the Lucong River",
        font=f(58),
        fill=TEAL,
    )
    y += 82

    d.text(
        (M, y),
        "[School Name]  ·  Team [Number]  ·  [Participant Names]  ·  December 2026",
        font=f(34),
        fill=GRAY,
    )
    y += 74

    # ---------------- stat band ----------------
    band_top = y
    band_h = 300
    d.rectangle([M, band_top, W - M, band_top + band_h], fill=MIST)
    d.rectangle([M, band_top, M + 14, band_top + band_h], fill=TEAL)

    stats = [
        ("16,000", "fecal coliform, MPN/100 mL", INK),
        ("80\u00d7", "the 200 standard", RED),
        ("164 t", "manure diverted a year", TEAL),
    ]
    col_w = (W - 2 * M) / 3
    for i, (big, cap, col) in enumerate(stats):
        cx = M + i * col_w
        if i:
            d.line([(cx, band_top + 60), (cx, band_top + band_h - 60)], fill=RULE, width=3)
        bw = d.textlength(big, font=f(126, bold=True))
        d.text((cx + (col_w - bw) / 2, band_top + 52), big, font=f(126, bold=True), fill=col)
        cw = d.textlength(cap, font=f(32))
        d.text((cx + (col_w - cw) / 2, band_top + 196), cap, font=f(32), fill=GRAY)

    y = band_top + band_h + 78

    # ---------------- map + why ----------------
    map_x, map_w = M, 1300
    src = Image.open(ROOT / "docs/figures/fig1_lucong_site_map.png").convert("RGBA")
    map_h = int(map_w * src.height / src.width)
    scaled = src.resize((map_w, map_h), Image.LANCZOS)
    bg = Image.new("RGB", (map_w, map_h), WHITE)
    bg.paste(scaled, (0, 0), scaled)
    img.paste(bg, (map_x, y))
    d.rectangle([map_x, y, map_x + map_w, y + map_h], outline=RULE, width=3)

    cap_y = y + map_h + 18
    cap_end = draw_par(
        d,
        (map_x, cap_y),
        "Monitored 1-km reach, Santiago Bridge downstream. Zones A and B are built-up banks; "
        "zone C is farmland behind the levees.",
        f(30, italic=True),
        map_w,
        fill=GRAY,
        leading=1.34,
    )

    rx = M + map_w + 96
    rw = W - M - rx
    ry = y
    ry = section(d, rx, ry, "01", "Why the river fails", rw)

    draw_par(
        d,
        (rx, ry),
        "BOD, DO, pH and temperature all pass. Fecal coliform fails alone, at 80 times the "
        "standard. Industrial effluent would raise oxygen demand; nothing here does.",
        f(37),
        rw,
        leading=1.5,
    )
    ry += 236

    draw_par(
        d,
        (rx, ry),
        "EMB reports livestock farms discharging sewage into the Lucong. Piggeries stand on "
        "both banks, untreated and unmonitored.",
        f(37),
        rw,
        leading=1.5,
    )
    ry += 226

    d.line([(rx, ry), (rx + 90, ry)], fill=RED, width=6)
    ry += 34
    draw_par(
        d,
        (rx, ry),
        "The rival account: every house drains to a septic tank, which can produce the same "
        "signal. Month 1 sampling separates the two.",
        f(34, italic=True),
        rw,
        fill=TEAL,
        leading=1.48,
    )

    # ---------------- the service ----------------
    y = max(cap_end, ry) + 74
    y = section(d, M, y, "02", "What we propose", W - 2 * M)

    d.text(
        (M, y),
        "Collect at the shed, not at the river. No sewer network required.",
        font=f(44, bold=True),
        fill=INK,
    )
    y += 100

    steps = [
        ("1", "Seal", "A sump and drum at every shed, so manure and washwater never reach the bank."),
        ("2", "Collect", "A 2,000 L vacuum tanker on a fixed weekly route. Every load weighed and manifested."),
        ("3", "Digest", "Three 25 m\u00b3 covered digesters, 10 to 15 days. Gas fires the sheds' scalding tanks."),
        ("4", "Return", "Digestate composted with rice husk, then given to the rice farms behind the levees."),
    ]
    gap = 34
    chip_w = (W - 2 * M - 3 * gap) / 4
    chip_top = y
    chip_h = 470
    for i, (num, title, body) in enumerate(steps):
        cx = M + i * (chip_w + gap)
        d.rectangle([cx, chip_top, cx + chip_w, chip_top + chip_h], fill=SAND)
        d.rectangle([cx, chip_top, cx + chip_w, chip_top + 10], fill=TEAL)
        d.text((cx + 34, chip_top + 40), num, font=f(58, bold=True), fill=RED)
        d.text((cx + 34, chip_top + 122), title, font=f(48, bold=True), fill=TEAL)
        draw_par(
            d,
            (cx + 34, chip_top + 196),
            body,
            f(31),
            chip_w - 68,
            leading=1.44,
        )

    y = chip_top + chip_h + 88

    # ---------------- cost + outcomes ----------------
    y = section(d, M, y, "03", "What it costs and what it buys", W - 2 * M)

    lw = 1180
    rxx = M + lw + 110
    rww = W - M - rxx
    top = y

    rows = [
        ("Total, 24 months", "\u20b110,000,000"),
        ("Works and equipment", "44.9%"),
        ("Per shed-month, 15 sheds", "\u20b125,600"),
        ("At 60 sheds", "\u20b16,400"),
    ]
    ry2 = top
    for label, val in rows:
        d.text((M, ry2 + 8), label, font=f(36), fill=INK)
        vw = d.textlength(val, font=f(40, bold=True))
        d.text((M + lw - vw, ry2), val, font=f(40, bold=True), fill=TEAL)
        ry2 += 76
        d.line([(M, ry2 - 12), (M + lw, ry2 - 12)], fill=RULE, width=2)

    d.text((rxx, top), "Targets", font=f(40, bold=True), fill=TEAL)
    ty = top + 66
    for line in [
        "2,000 MPN/100 mL by Month 24",
        "95% manifest coverage",
        "164 t manure diverted yearly",
        "Every load traceable to a field",
    ]:
        d.ellipse([rxx, ty + 14, rxx + 14, ty + 28], fill=RED)
        ty = draw_par(d, (rxx + 34, ty), line, f(34), rww - 34, leading=1.42) + 16

    # ---------------- footer ----------------
    fy = H - M - 118
    d.line([(M, fy - 30), (W - M, fy - 30)], fill=RULE, width=3)
    draw_par(
        d,
        (M, fy),
        "Sources: EMB Region III, Regional state of the brown environment report 2022; DENR DAO 2016-08; "
        "Municipal Government of Concepcion, Citizen's Charter 2024; PhilAtlas 2026; Municipality of Bamban, "
        "Integrated Zoning Ordinance 2026. Base map \u00a9 OpenStreetMap contributors (ODbL).",
        f(25),
        W - 2 * M,
        fill=GRAY,
        leading=1.36,
    )

    out = ROOT / "docs/POSTER_LUCONG_V1.png"
    img.save(out, optimize=True)
    print(f"saved {out}  {img.size[0]}x{img.size[1]}  ratio {img.size[0]/img.size[1]:.4f}")


if __name__ == "__main__":
    main()
