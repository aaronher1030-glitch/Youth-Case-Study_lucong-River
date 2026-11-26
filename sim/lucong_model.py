"""
Lucong shed-service model: load balance, process balance, cost, design search.

Three blocks, in the order the paper argues them:
  1. load_balance()   what share of the river's coliform load the sheds carry,
                      and what capture does to the station concentration.
  2. process()        whether the slurry fits the digesters and the tanker,
                      and what the gas and compost balances say.
  3. design_search()  every design inside P10M / 12 months, and the least-cost
                      feasible one at a given census.

Every parameter carries its status:  SOURCED | ASSUMPTION | TO MEASURE.
The paper may quote sourced values as facts, assumptions as assumptions, and
must name the TO MEASURE ones as quantities the pilot exists to observe.

Run:  python sim/lucong_model.py
Writes: sim/outputs/lucong_designs.csv
        sim/outputs/lucong_load.csv
        sim/outputs/lucong_montecarlo.csv
        docs/figures/fig2_lucong_model.png
"""

from __future__ import annotations

import csv
import math
from dataclasses import dataclass, replace
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "sim" / "outputs"
FIG = ROOT / "docs" / "figures"


# --------------------------------------------------------------------------
# Parameters
# --------------------------------------------------------------------------

@dataclass(frozen=True)
class Params:
    # --- census -----------------------------------------------------------
    n_sheds: int = 15                 # design; MENRO census replaces it
    heads_per_shed: float = 15.0      # ASSUMPTION; census
    manure_kg_head_day: float = 2.0   # ASSUMPTION; literature range 1.5-3.0
    washwater_l_head_day: float = 22.0  # ASSUMPTION; 5 m3/day at 225 heads

    # --- load balance -----------------------------------------------------
    c0_mpn_100ml: float = 16_000.0    # SOURCED: EMB Region III, 2024
    q_m3_s: float = 0.05              # TO MEASURE: dry-season discharge
    e_head_day: float = 1.0e9         # ASSUMPTION: MPN per head-day, 1e8-1e10
    capture: float = 0.85             # design; manifest coverage target 0.95

    # --- process ----------------------------------------------------------
    dm_frac: float = 0.20             # ASSUMPTION: manure dry matter
    vs_frac_dm: float = 0.80          # ASSUMPTION: volatile solids of DM
    vs_destroyed: float = 0.50        # ASSUMPTION: anaerobic, 10-15 d HRT
    ch4_yield: float = 0.35           # ASSUMPTION: m3 CH4 / kg VS destroyed
    ch4_frac: float = 0.60            # ASSUMPTION: biogas methane fraction
    lpg_mj_kg: float = 46.0           # SOURCED: LPG lower heating value
    ch4_mj_m3: float = 35.8           # SOURCED: methane LHV
    n_frac_dm: float = 0.04           # ASSUMPTION: N share of manure DM
    rice_n_kg_ha: float = 120.0       # ASSUMPTION: lowland rice N rate
    husk_ratio: float = 0.713         # computed from C:N balance, see process()

    # --- cost (2026 planning prices, unquoted) ----------------------------
    cap_digester: float = 380_000     # per 25 m3 module, with gas train
    cap_tanker: float = 1_450_000     # 2,000 L vacuum tanker
    cap_cart: float = 180_000         # motorised cart with drums
    cap_pad: float = 980_000          # roofed composting pad, 300 m2
    cap_gas_kit: float = 45_000
    cap_site: float = 420_000
    opex_staff_year: float = 1_140_000  # coordinator + 2 operators, 95k/month
    opex_sampling_year: float = 240_000  # 6 stations x 4 rounds x 10k
    opex_maint_frac: float = 0.05
    opex_trip: float = 700            # fuel + consumables per tanker trip
    opex_admin_year: float = 60_000
    workdays_week: int = 6
    trips_day_cap: int = 5
    tanker_m3: float = 2.0
    module_m3: float = 25.0
    hrt_min_days: float = 10.0
    budget: float = 10_000_000
    discount: float = 0.08            # ASSUMPTION: capital recovery rate
    asset_life: int = 10              # years


# --------------------------------------------------------------------------
# 1. Load balance
# --------------------------------------------------------------------------

def load_balance(p: Params) -> dict:
    """Shed load, total station load, shed share s, and predicted endpoint."""
    heads = p.n_sheds * p.heads_per_shed
    l_sheds = heads * p.e_head_day                       # MPN/day
    l_total = p.c0_mpn_100ml * 10_000 * p.q_m3_s * 86_400  # MPN/day
    s = min(l_sheds / l_total, 0.95)                     # upstream load exists
    reduction = s * p.capture
    c_end = p.c0_mpn_100ml * (1 - reduction)
    return {
        "heads": heads,
        "l_sheds": l_sheds,
        "l_total": l_total,
        "s": s,
        "reduction": reduction,
        "c_end": c_end,
    }


# --------------------------------------------------------------------------
# 2. Process balance
# --------------------------------------------------------------------------

def process(p: Params) -> dict:
    heads = p.n_sheds * p.heads_per_shed
    manure_kg = heads * p.manure_kg_head_day
    wash_m3 = heads * p.washwater_l_head_day / 1000
    slurry_m3 = manure_kg / 1000.0 + wash_m3          # manure ~ water density

    vs_in = manure_kg * p.dm_frac * p.vs_frac_dm
    vs_dest = vs_in * p.vs_destroyed
    ch4_m3 = vs_dest * p.ch4_yield
    biogas_m3 = ch4_m3 / p.ch4_frac
    lpg_kg = ch4_m3 * p.ch4_mj_m3 / p.lpg_mj_kg

    nutrient_n = (manure_kg * p.dm_frac - vs_dest) * p.n_frac_dm
    land_ha = (nutrient_n * 365) / p.rice_n_kg_ha

    trips_week = slurry_m3 * 7 / p.tanker_m3
    return {
        "manure_kg_day": manure_kg,
        "wash_m3_day": wash_m3,
        "slurry_m3_day": slurry_m3,
        "vs_in": vs_in,
        "vs_dest": vs_dest,
        "biogas_m3_day": biogas_m3,
        "lpg_kg_day": lpg_kg,
        "compost_n_kg_day": nutrient_n,
        "land_ha": land_ha,
        "trips_week": trips_week,
    }


def design_costs(p: Params, modules: int, tankers: int, carts: int) -> dict:
    capex = (
        modules * p.cap_digester
        + tankers * p.cap_tanker
        + carts * p.cap_cart
        + p.cap_pad
        + modules * p.cap_gas_kit
        + p.cap_site
    )
    trips = process(p)["trips_week"]
    opex = (
        p.opex_staff_year
        + p.opex_sampling_year
        + p.opex_maint_frac * capex
        + trips * 52 * p.opex_trip
        + p.opex_admin_year
    )
    twelve_month = capex + opex
    crf = p.discount * (1 + p.discount) ** p.asset_life / (
        (1 + p.discount) ** p.asset_life - 1
    )
    levelised_year = capex * crf + opex
    return {
        "modules": modules,
        "tankers": tankers,
        "carts": carts,
        "capex": capex,
        "opex_year": opex,
        "twelve_month": twelve_month,
        "levelised_year": levelised_year,
        "per_shed_month_pilot": twelve_month / (p.n_sheds * 12),
        "per_shed_month_level": levelised_year / (p.n_sheds * 12),
    }


# --------------------------------------------------------------------------
# 3. Design search
# --------------------------------------------------------------------------

def design_search(p: Params) -> list[dict]:
    """Enumerate feasible designs; return them sorted by levelised unit cost."""
    pr = process(p)
    feasible = []
    for modules in range(1, 16):
        if modules * p.module_m3 / pr["slurry_m3_day"] < p.hrt_min_days:
            continue
        for tankers in range(1, 8):
            if pr["trips_week"] > tankers * p.workdays_week * p.trips_day_cap:
                continue
            carts = math.ceil(p.n_sheds / 8)
            c = design_costs(p, modules, tankers, carts)
            if c["twelve_month"] > p.budget:
                continue
            feasible.append({**c, "trips_week": pr["trips_week"],
                             "hrt_days": modules * p.module_m3 / pr["slurry_m3_day"]})
    if not feasible:
        return []
    # prefer the cheapest levelised service; tie-break on pilot cost
    feasible.sort(key=lambda r: (r["per_shed_month_level"], r["twelve_month"]))
    return feasible


# --------------------------------------------------------------------------
# Experiments
# --------------------------------------------------------------------------

def load_table() -> list[dict]:
    """s and endpoint concentration across flow and census."""
    rows = []
    base = Params()
    for q in (0.02, 0.05, 0.10, 0.20):
        for heads in (10, 15, 25):
            p = replace(base, q_m3_s=q, heads_per_shed=heads)
            lb = load_balance(p)
            rows.append({
                "q_m3_s": q,
                "heads_per_shed": heads,
                "s": round(lb["s"], 3),
                "c_end_at_85_capture": round(lb["c_end"]),
                "c_end_at_95_capture": round(
                    p.c0_mpn_100ml * (1 - lb["s"] * 0.95)),
            })
    return rows


def monte_carlo(n: int = 20_000, seed: int = 2026) -> dict:
    rng = np.random.default_rng(seed)
    base = Params()
    q = np.exp(rng.uniform(math.log(0.02), math.log(0.20), n))
    e = np.exp(rng.uniform(math.log(1e8), math.log(1e10), n))
    heads = rng.triangular(8, 15, 25, n)
    c = rng.triangular(0.70, 0.85, 0.95, n)
    shed_n = rng.integers(12, 21, n)

    l_sheds = shed_n * heads * e
    l_total = base.c0_mpn_100ml * 10_000 * q * 86_400
    s = np.clip(l_sheds / l_total, 0, 0.95)
    c_end = base.c0_mpn_100ml * (1 - s * c)

    return {
        "s_p10": float(np.percentile(s, 10)),
        "s_p50": float(np.percentile(s, 50)),
        "s_p90": float(np.percentile(s, 90)),
        "c_end_p10": float(np.percentile(c_end, 10)),
        "c_end_p50": float(np.percentile(c_end, 50)),
        "c_end_p90": float(np.percentile(c_end, 90)),
        "p_meet_8000": float((c_end <= 8_000).mean()),
        "p_meet_2000": float((c_end <= 2_000).mean()),
    }


def figure(layout: str = "stack") -> None:
    """Two-panel figure. 'stack' for a 3.25-inch journal column,
    'wide' for a 6.3-inch single-column manuscript page."""
    if layout == "wide":
        fig, axes = plt.subplots(1, 2, figsize=(6.8, 3.0), dpi=300)
        k = 1.25
        name = "fig2_lucong_model_wide.png"
        pad = (3.0, 1.4)
    else:
        fig, axes = plt.subplots(2, 1, figsize=(3.4, 5.0), dpi=300)
        k = 1.0
        name = "fig2_lucong_model.png"
        pad = (1.0, 1.0)
    ax1, ax2 = axes

    # a: endpoint concentration vs capture, one line per flow
    capture = np.linspace(0, 0.95, 100)
    for q, style in ((0.02, "-"), (0.05, "--"), (0.20, ":")):
        p = replace(Params(), q_m3_s=q)
        s = load_balance(replace(p, capture=0.0))["s"]
        ax1.plot(capture * 100, p.c0_mpn_100ml * (1 - s * capture), style,
                 lw=1.2, label=f"Q = {q:.2f} m$^3$/s")
    ax1.axhline(8000, color="0.35", lw=0.8, ls="-.")
    ax1.text(2, 8800, "conditional target 8,000", fontsize=5.5 * k, color="0.35",
             ha="left", bbox=dict(fc="white", ec="none", pad=0.6))
    ax1.axhline(200, color="0.15", lw=0.8, ls=":")
    ax1.text(2, 235, "DAO limit 200", fontsize=5.5 * k, color="0.15", ha="left",
             bbox=dict(fc="white", ec="none", pad=0.6))
    ax1.set_xlabel("shed load captured (%)", fontsize=6.5 * k)
    ax1.set_ylabel("station fecal coliform (MPN/100 mL)", fontsize=6.5 * k)
    ax1.set_yscale("log")
    ax1.set_xlim(0, 95)
    ax1.set_ylim(120, 22000)
    ax1.tick_params(labelsize=5.5 * k)
    ax1.legend(fontsize=5.5 * k, frameon=False, loc="center left")
    ax1.set_title("a. capture buys less at higher flow", fontsize=7 * k, loc="left")

    # b: levelised cost per shed-month against census
    xs, ys = [], []
    for n in (12, 15, 18, 21, 24, 27, 30):
        p = replace(Params(), n_sheds=n, washwater_l_head_day=10.0)
        rows = design_search(p)
        if rows:
            xs.append(n)
            ys.append(rows[0]["per_shed_month_level"])
    ax2.plot(xs, ys, "o-", lw=1.2, ms=3 * k)
    ax2.set_xlabel("sheds served", fontsize=6.5 * k)
    ax2.set_ylabel("levelised \u20b1 per shed-month", fontsize=6.5 * k)
    ax2.tick_params(labelsize=5.5 * k)
    ax2.set_xticks(xs)
    ax2.set_title("b. cost falls with census, then stops", fontsize=7 * k, loc="left")
    ax2.text(0.03, 0.06, "at 10 L/head-day washwater", transform=ax2.transAxes,
             fontsize=5.5 * k, color="0.35")

    fig.tight_layout(h_pad=pad[0], w_pad=pad[1])
    FIG.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG / name, bbox_inches="tight")
    plt.close(fig)


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    base = Params()

    print("== load balance ==")
    for row in load_table():
        print(row)
    write_csv(OUT / "lucong_load.csv", load_table())

    print("\n== process at 15 sheds ==")
    pr = process(base)
    for k, v in pr.items():
        print(f"  {k:18s} {v:12.2f}")

    print("\n== design search ==")
    design_rows = []
    for n, wash in ((15, 22.0), (15, 10.0), (20, 22.0), (20, 10.0),
                    (30, 10.0), (30, 22.0), (60, 10.0)):
        p = replace(base, n_sheds=n, washwater_l_head_day=wash)
        rows = design_search(p)
        best = rows[0] if rows else None
        design_rows.append({
            "sheds": n,
            "washwater_l_head_day": wash,
            "feasible_designs": len(rows),
            "modules": best["modules"] if best else None,
            "tankers": best["tankers"] if best else None,
            "trips_week": round(process(p)["trips_week"], 1),
            "capex": round(best["capex"]) if best else None,
            "twelve_month": round(best["twelve_month"]) if best else None,
            "per_shed_month_pilot": round(best["per_shed_month_pilot"]) if best else None,
            "per_shed_month_level": round(best["per_shed_month_level"]) if best else None,
        })
    for r in design_rows:
        print(r)
    write_csv(OUT / "lucong_designs.csv", design_rows)

    print("\n== monte carlo ==")
    mc = monte_carlo()
    for k, v in mc.items():
        print(f"  {k:14s} {v:.4f}" if v < 1 else f"  {k:14s} {v:,.0f}")
    write_csv(OUT / "lucong_montecarlo.csv", [mc])

    figure("stack")
    figure("wide")
    print("\nwrote", FIG / "fig2_lucong_model.png")
    print("wrote", FIG / "fig2_lucong_model_wide.png")


if __name__ == "__main__":
    main()
