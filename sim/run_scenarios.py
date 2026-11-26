"""
run_scenarios.py — the experiment the paper reports.

Three outputs, all written to sim/outputs/:

  arm_sweep.csv        arm 1 vs arm 2 completion across a sweep of the
                       unknown quantity (the effect of the household visit)
  decomposition.csv    splits the arm difference into its two channels:
                       physical access work vs faster response
  sensitivity.csv      one-at-a-time sensitivity of the headline result
                       to every assumption a judge might challenge
  fig_arm_sweep.png    the figure that goes on the poster

Run:  python sim/run_scenarios.py --reps 200
"""

from __future__ import annotations

import argparse
import csv
import os
import sys
from dataclasses import replace

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from service_sim import Params, summarise  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "outputs")


def write_csv(path: str, rows: list[dict]) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not rows:
        return
    keys = list(rows[0].keys())
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=keys)
        w.writeheader()
        for r in rows:
            w.writerow(r)


def arm_sweep(reps: int, seed0: int) -> list[dict]:
    rows = []
    for uplift in [0.0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30]:
        p = replace(Params(), uplift=uplift)
        s = summarise(p, reps=reps, seed0=seed0)
        rows.append(
            {
                "uplift": uplift,
                "arm1_rate": s["arm1_rate"],
                "arm1_rate_lo": s["arm1_rate_lo"],
                "arm1_rate_hi": s["arm1_rate_hi"],
                "arm2_rate": s["arm2_rate"],
                "arm2_rate_lo": s["arm2_rate_lo"],
                "arm2_rate_hi": s["arm2_rate_hi"],
                "arm_diff": s["arm_diff"],
                "arm_diff_lo": s["arm_diff_lo"],
                "arm_diff_hi": s["arm_diff_hi"],
                "completion_rate": s["completion_rate"],
                "days_used": s["days_used"],
                "crew_utilisation": s["crew_utilisation"],
                "cost_per_hh_actual": s["cost_per_hh_actual"],
                "cost_per_hh_staffed": s["cost_per_hh_staffed"],
            }
        )
        print(
            f"uplift {uplift:>4.2f}   arm1 {s['arm1_rate']:.3f}   "
            f"arm2 {s['arm2_rate']:.3f}   diff {s['arm_diff']:+.3f} "
            f"[{s['arm_diff_lo']:+.3f}, {s['arm_diff_hi']:+.3f}]   "
            f"PHP/hh {s['cost_per_hh_actual']:.0f}"
        )
    return rows


def sensitivity(reps: int, seed0: int) -> list[dict]:
    """One-at-a-time. Answers 'what if a judge disputes this assumption?'"""
    base = Params()
    rows: list[dict] = []

    variations: list[tuple[str, str, float, Params]] = []
    for v in (0.45, 0.55, 0.65):
        variations.append(("base_accept", f"baseline uptake {v:.2f}", v,
                           replace(base, base_accept=v)))
    for v in (0.0, 0.25, 0.50):
        variations.append(("f3_refusal_arm1", f"floor-work refusal {v:.2f}", v,
                           replace(base, f3_refusal_arm1=v)))
    for v in (0.0, 0.12, 0.25):
        variations.append(("no_show", f"no-show {v:.2f}", v,
                           replace(base, no_show=v)))
    for v in (1, 2, 3):
        variations.append(("n_crews", f"{v} crew(s)", float(v),
                           replace(base, n_crews=v)))
    for v in (0.60, 0.70, 0.80):
        variations.append(("p_under_house", f"under house {v:.0%}", v,
                           replace(base, p_under_house=v)))
    for v in (5.0, 12.0):
        variations.append(("window_days", f"block window {v:.0f} days", v,
                           replace(base, window_days=v)))
    for lo, hi in ((0.5, 1.5), (0.5, 2.5), (0.5, 3.5)):
        variations.append(("tank_m3", f"tank {lo}-{hi} m3", (lo + hi) / 2,
                           replace(base, tank_m3_lo=lo, tank_m3_hi=hi)))

    for param, label, value, p in variations:
        s = summarise(p, reps=reps, seed0=seed0)
        rows.append(
            {
                "parameter": param,
                "setting": label,
                "value": value,
                "completion_rate": s["completion_rate"],
                "arm_diff": s["arm_diff"],
                "days_used": s["days_used"],
                "crew_utilisation": s["crew_utilisation"],
                "cost_per_hh_actual": s["cost_per_hh_actual"],
            }
        )
        print(f"  {param:<18} {label:<24} completion {s['completion_rate']:.3f}  "
              f"PHP/hh {s['cost_per_hh_actual']:.0f}")
    return rows


def decompose(reps: int, seed0: int) -> list[dict]:
    """Split the arm difference into its two channels.

    Arm 2 differs from arm 1 in two ways at once:

      (a) physical access work — an external port is installed before the
          window, so an F3 household is no longer a 75-minute floor job and
          no longer refuses on arrival;
      (b) a faster response — the household visit shortens the lag from
          booking to crew arrival, so fewer bookings fall outside the block
          window.

    Running arm 2 with arm 1's response lag isolates the arrival-side channel.
    At uplift = 0 that channel is purely the physical access work, because
    nothing else differs. At uplift > 0 it bundles access work with the
    awareness gain, so it must be labelled as both. The remainder — total
    minus arrival-side — is the response-speed contribution.
    """
    base = Params()
    rows: list[dict] = []
    for uplift in (0.0, 0.15):
        full = replace(base, uplift=uplift)
        lag_matched = replace(
            base, uplift=uplift, mean_lag_arm2_days=base.mean_lag_arm1_days
        )
        s_full = summarise(full, reps=reps, seed0=seed0)
        s_lag = summarise(lag_matched, reps=reps, seed0=seed0)
        arrival = s_lag["arm_diff"]
        speed = s_full["arm_diff"] - arrival
        rows.append(
            {
                "uplift": uplift,
                "arm_diff_total": s_full["arm_diff"],
                "arm_diff_arrival_channel": round(arrival, 3),
                "arm_diff_speed_channel": round(speed, 3),
                "arrival_share": round(arrival / s_full["arm_diff"], 3)
                if s_full["arm_diff"]
                else 0.0,
                "arm2_rate_lag_matched": s_lag["arm2_rate"],
                "arrival_channel_means": (
                    "access work only" if uplift == 0.0
                    else "access work + awareness"
                ),
            }
        )
        kind = "access only" if uplift == 0.0 else "access + awareness"
        print(
            f"uplift {uplift:>4.2f}   total {s_full['arm_diff']:+.3f}   "
            f"arrival[{kind}] {arrival:+.3f}   "
            f"response speed {speed:+.3f}"
        )
    return rows


def figure(rows: list[dict]) -> str:
    x = [r["uplift"] * 100 for r in rows]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2))

    ax1.plot(x, [r["arm1_rate"] * 100 for r in rows], "o-", label="Arm 1 — standard notice",
             color="#2563eb", lw=2)
    ax1.plot(x, [r["arm2_rate"] * 100 for r in rows], "s-", label="Arm 2 — visit + access work",
             color="#16a34a", lw=2)
    ax1.fill_between(
        x,
        [r["arm1_rate_lo"] * 100 for r in rows],
        [r["arm1_rate_hi"] * 100 for r in rows],
        color="#2563eb", alpha=0.12,
    )
    ax1.fill_between(
        x,
        [r["arm2_rate_lo"] * 100 for r in rows],
        [r["arm2_rate_hi"] * 100 for r in rows],
        color="#16a34a", alpha=0.12,
    )
    ax1.axhline(55, color="#6b7280", lw=1, ls=":",
                label="55% — citywide acceptance, 2025")
    ax1.set_xlabel("Effect of the household visit (percentage points)")
    ax1.set_ylabel("Households served (%)")
    ax1.set_title("Who gets served")
    ax1.grid(alpha=0.25)
    ax1.set_ylim(0, 100)
    ax1.legend(frameon=False, fontsize=9, loc="lower right")

    ax2.plot(x, [r["cost_per_hh_actual"] for r in rows], "o-", color="#d97706", lw=2,
             label="Actual campaign cost")
    ax2.plot(x, [r["cost_per_hh_staffed"] for r in rows], "s--", color="#7c3aed", lw=2,
             label="Cost if staffed for 234 days")
    ax2.axhline(1000, color="#b91c1c", lw=1, ls=":",
                label="Environmental charge yield (~PHP 500–1,000)")
    ax2.set_xlabel("Effect of the household visit (percentage points)")
    ax2.set_ylabel("Cost per household served (PHP)")
    ax2.set_title("What it costs — and the gap is idle labour")
    ax2.grid(alpha=0.25)
    ax2.legend(frameon=True, facecolor="white", edgecolor="none",
               framealpha=1.0, fontsize=9, loc="lower right")

    fig.tight_layout()
    path = os.path.join(OUT, "fig_arm_sweep.png")
    fig.savefig(path, dpi=180)
    plt.close(fig)
    return path


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--reps", type=int, default=200)
    ap.add_argument("--seed", type=int, default=2026)
    args = ap.parse_args()

    os.makedirs(OUT, exist_ok=True)
    print(f"Arm sweep — {args.reps} replicates per point\n")
    rows = arm_sweep(args.reps, args.seed)
    write_csv(os.path.join(OUT, "arm_sweep.csv"), rows)

    print("\nOne-at-a-time sensitivity at uplift = 0.15\n")
    sens = sensitivity(args.reps, args.seed)
    write_csv(os.path.join(OUT, "sensitivity.csv"), sens)

    print("\nDecomposing the arm difference\n")
    dec = decompose(args.reps, args.seed)
    write_csv(os.path.join(OUT, "decomposition.csv"), dec)

    fig = figure(rows)
    print(
        f"\nWrote {OUT}\\arm_sweep.csv, sensitivity.csv, decomposition.csv, "
        f"{os.path.basename(fig)}"
    )


if __name__ == "__main__":
    main()
