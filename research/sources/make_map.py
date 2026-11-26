import math, io, json, requests
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patheffects
from matplotlib.patches import Rectangle, FancyArrowPatch
from matplotlib.ticker import FuncFormatter
from PIL import Image

LAT0, LAT1 = 15.3205, 15.3405
LON0, LON1 = 120.6205, 120.6485
Z = 16
N = 2 ** Z

def lon2x(lon): return (lon + 180.0) / 360.0 * N
def lat2y(lat):
    r = math.radians(lat)
    return (1.0 - math.log(math.tan(r) + 1.0 / math.cos(r)) / math.pi) / 2.0 * N
def x2lon(x): return x / N * 360.0 - 180.0
def y2lat(y):
    n = math.pi - 2.0 * math.pi * y / N
    return math.degrees(math.atan(math.sinh(n)))

x0, x1 = int(math.floor(lon2x(LON0))), int(math.floor(lon2x(LON1)))
y0, y1 = int(math.floor(lat2y(LAT1))), int(math.floor(lat2y(LAT0)))
hdr = {"User-Agent": "YouthCaseStudy-RF2027/1.0 (educational research; Concepcion, Tarlac)"}
rows = []
for y in range(y0, y1 + 1):
    row = []
    for x in range(x0, x1 + 1):
        r = requests.get(f"https://tile.openstreetmap.org/{Z}/{x}/{y}.png", headers=hdr, timeout=30)
        r.raise_for_status()
        row.append(Image.open(io.BytesIO(r.content)).convert("RGB"))
    rows.append(row)
w, h = rows[0][0].size
mosaic = Image.new("RGB", (w * len(rows[0]), h * len(rows)), "white")
for j, row in enumerate(rows):
    for i, im in enumerate(row):
        mosaic.paste(im, (i * w, j * h))
mosaic.save("research/sources/osm_mosaic.png")
ext = (x2lon(x0), x2lon(x1 + 1), y2lat(y1 + 1), y2lat(y0))

# River geometry (OSM way 265729651), walked downstream from Santiago Bridge
# and cut at the measured distances so the lines end exactly at their stars.
d = json.load(open("research/sources/osm_river.json", encoding="utf-8"))
way = [e for e in d["elements"] if e["id"] == 265729651][0]
pts = [(p["lat"], p["lon"]) for p in way["geometry"]]

def hav(a, b):
    R = 6371000.0
    p1, p2 = math.radians(a[0]), math.radians(b[0])
    dp = p2 - p1
    dl = math.radians(b[1] - a[1])
    h = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * R * math.asin(math.sqrt(h))

i0 = min(range(len(pts)), key=lambda i: hav(pts[i], (15.32996, 120.62838)))
path = [(15.32996, 120.62838)] + pts[i0 + 1:]
cum = [0.0]
for p, q in zip(path, path[1:]):
    cum.append(cum[-1] + hav(p, q))

def point_at(dist):
    for i in range(1, len(cum)):
        if cum[i] >= dist:
            f = (dist - cum[i - 1]) / (cum[i] - cum[i - 1])
            return (path[i - 1][0] + f * (path[i][0] - path[i - 1][0]),
                    path[i - 1][1] + f * (path[i][1] - path[i - 1][1]))
    return path[-1]

S = (15.32996, 120.62838)
K = point_at(1000.0)
A = point_at(1516.0)
print("start vertex gap m:", round(hav(pts[i0], S), 1))
print("walk end distance:", round(cum[-1], 1))
print("K:", tuple(round(v, 5) for v in K))
print("A:", tuple(round(v, 5) for v in A))

reach = [path[i] for i in range(len(path)) if cum[i] <= 1516.0] + [A]
km = [path[i] for i in range(len(path)) if cum[i] <= 1000.0] + [K]
km_lons = [p[1] for p in km]; km_lats = [p[0] for p in km]
lons = [p[1] for p in reach]; lats = [p[0] for p in reach]

fig, ax = plt.subplots(figsize=(9.2, 7.1), dpi=240)
ax.imshow(mosaic, extent=ext, interpolation="lanczos", zorder=0)
ax.plot(lons, lats, color="#f2b100", lw=4.0, solid_capstyle="round", zorder=3)
ax.plot(km_lons, km_lats, color="#d7191c", lw=4.8, solid_capstyle="round", zorder=4)
ax.scatter([S[1], A[1]], [S[0], A[0]], marker="*", s=400, color="#1a9641",
           edgecolor="white", linewidth=0.8, zorder=6)
ax.scatter([K[1]], [K[0]], marker="o", s=95, facecolor="white", edgecolor="#d7191c",
           linewidth=2.0, zorder=6)

def lab(lon, lat, text, ha="left", color="black", size=9.0):
    ax.annotate(text, (lon, lat), ha=ha, va="center", fontsize=size, color=color,
                weight="bold", zorder=7,
                bbox=dict(boxstyle="round,pad=0.28", fc="white", ec="0.55", lw=0.6, alpha=0.93))

lab(120.6213, 15.3291, "Santiago Bridge\nEMB Station 2\n(15.330 N, 120.628 E)", ha="left")
lab(A[1] + 0.0006, A[0] + 0.0015, "Alfonso Bridge\nend of reach (15.334 N, 120.641 E)")
lab(K[1] + 0.0006, K[0] - 0.0016, "1-km mark\n15.333 N, 120.637 E", size=8.7)

lab(120.6258, 15.3382, "A. Built-up bank, Brgy. Santiago\nhousehold waste, septic effluent,\ncommercial drains (indirect + direct)", color="#b2182b", size=8.8)
ax.annotate("", xy=(120.6302, 15.3316), xytext=(120.6262, 15.3370),
            arrowprops=dict(arrowstyle="-|>", color="#b2182b", lw=1.2), zorder=5)

lab(120.6380, 15.3288, "B. Built-up bank, Brgy. Alfonso\nshops and drains along the road,\nbackyard piggeries (direct + indirect)", color="#b2182b", size=8.8)
ax.annotate("", xy=(120.6360, 15.3322), xytext=(120.6376, 15.3289),
            arrowprops=dict(arrowstyle="-|>", color="#b2182b", lw=1.2), zorder=5)

lab(120.6236, 15.3266, "C. Irrigated paddies and farm lots\nlivestock/agricultural runoff;\nbamboo and trees on the bank (indirect)", color="#006d2c", size=8.8)
ax.annotate("", xy=(120.6304, 15.3278), xytext=(120.6283, 15.3269),
            arrowprops=dict(arrowstyle="-|>", color="#006d2c", lw=1.2), zorder=5)


ax.annotate("N", xy=(120.6470, 15.3393), ha="center", va="center", fontsize=11, weight="bold", zorder=8)
ax.add_patch(FancyArrowPatch((120.6470, 15.3378), (120.6470, 15.3390),
             arrowstyle="-|>", mutation_scale=14, color="black", lw=1.4, zorder=8))

deg = 500.0 / (111320.0 * math.cos(math.radians(15.33)))
ax.add_patch(Rectangle((120.6222, 15.3229), deg, 0.00032, facecolor="black", edgecolor="black", zorder=8))
ax.add_patch(Rectangle((120.6222 + deg, 15.3229), deg, 0.00032, facecolor="white", edgecolor="black", zorder=8))
for xx, tt, ha in [(120.6222, "0", "center"), (120.6222 + deg, "500", "center"),
                   (120.6222 + 2 * deg, "1,000 m", "left")]:
    ax.text(xx, 15.3226, tt, fontsize=8.0, ha=ha, va="top", zorder=8)

handles = [
    plt.Line2D([], [], color="#d7191c", lw=4.5, label="Monitored 1-km stretch"),
    plt.Line2D([], [], color="#f2b100", lw=3.5, label="Full 1.52-km reach"),
    plt.Line2D([], [], marker="*", color="none", markerfacecolor="#1a9641",
               markeredgecolor="white", markersize=12, label="Bridge / EMB sampling point"),
]
leg = ax.legend(handles=handles, loc="lower right", fontsize=8.2, framealpha=0.95,
                borderpad=0.7, labelspacing=0.6)
leg.set_zorder(9)

ax.set_xlim(LON0, LON1); ax.set_ylim(LAT0, LAT1)
ax.set_xticks([120.6225, 120.6275, 120.6325, 120.6375, 120.6425, 120.6475])
ax.set_yticks([15.3225, 15.3275, 15.3325, 15.3375])
ax.xaxis.set_major_formatter(FuncFormatter(lambda v, p: f"{v:.3f}"))
ax.yaxis.set_major_formatter(FuncFormatter(lambda v, p: f"{v:.3f}"))
ax.set_xlabel("Longitude (decimal degrees)", fontsize=9)
ax.set_ylabel("Latitude (decimal degrees)", fontsize=9)
ax.tick_params(labelsize=8)
ax.set_title("Lucong River, Concepcion, Tarlac: monitored 1-km stretch,\nSantiago Bridge to Alfonso Bridge reach",
             fontsize=11.5, weight="bold", pad=6)
ax.text(120.6209, 15.3208,
        "Base map: OpenStreetMap contributors (ODbL). Channel traced from OSM way 265729651;\n"
        "reach measured in Google Earth: 1,516 m, heading 70.9 deg. Prepared 18 November 2026.",
        fontsize=6.5, color="0.25", ha="left", va="bottom")
fig.tight_layout(rect=(0, 0.045, 1, 1))
fig.savefig("docs/figures/fig1_lucong_site_map.png", dpi=220)
print("saved")
