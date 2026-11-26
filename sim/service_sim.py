"""
service_sim.py — Discrete-event simulation of a household desludging campaign.

WHAT THIS MODELS
----------------
400 households in one contiguous kilometre, served by a crew with a small
vacuum unit, under two notification arms:

    Arm 1  standard schedule card through barangay channels
    Arm 2  the same card, plus a household visit and access remediation
           (floor works or an external access port) done before the window

The question is not whether the trucks can keep up. It is which barrier
decides who actually gets served, and what that costs.

WHAT THIS DOES NOT MODEL
------------------------
Hydraulics, septage treatment, water quality, disease. This is a queueing
and scheduling model. It says nothing about the river.

TIME
----
Model time is WORKING MINUTES. There are no nights, weekends or holidays
inside the clock; a "day" is 480 working minutes. Day counts are therefore
crew-days, not calendar days. This keeps the model readable and is stated
in the paper.

USAGE
-----
    python service_sim.py                 # default scenario, 1 replicate
    python service_sim.py --uplift 0.25   # change one parameter
    python service_sim.py --reps 200      # distribution rather than a run
"""

from __future__ import annotations

import argparse
import math
import statistics
from dataclasses import dataclass, field, asdict

import numpy as np
import simpy

# --------------------------------------------------------------------------
# Parameters. Every value carries its provenance; see README.md.
# --------------------------------------------------------------------------


@dataclass
class Params:
    # cohort
    n_households: int = 400
    n_blocks: int = 10
    arm_split: float = 0.5

    # behaviour — the quantities under test
    base_accept: float = 0.55          # MWSS acceptance, 2025
    uplift: float = 0.15               # arm 2 effect: THE parameter of interest
    f3_refusal_arm1: float = 0.25      # share refusing floor works, arm 1 only

    # access tiering, from IFC 2018 marginals
    p_under_house: float = 0.70        # tank beneath the house
    p_narrow_path: float = 0.71        # path fits only a person or motorbike

    # response timing
    mean_lag_arm1_days: float = 5.0
    mean_lag_arm2_days: float = 2.0

    # service schedule
    window_days: float = 12.0          # each block's service window
    day_minutes: float = 480.0         # 8-hour working day
    run_days: float = 234.0            # 9 collection months of 26 days

    # crew and equipment
    n_crews: int = 2
    staff_per_crew: int = 4
    pump_lpm: float = 250.0            # small vacuum unit
    tank_m3_lo: float = 0.5
    tank_m3_hi: float = 1.5
    transfer_min: float = 5.0          # unit -> mother tanker
    travel_min: float = 3.0            # mean inter-household movement

    # access setup, minutes
    setup_f1: float = 10.0             # direct truck access
    setup_f2: float = 30.0             # narrow path, long hose run
    setup_f3: float = 75.0             # tank under house, floor opened
    setup_f3_remediated: float = 30.0  # arm 2: port installed in advance

    # failure
    no_show: float = 0.12              # household not present
    retry_days: float = 3.0
    no_show_visit_min: float = 15.0    # wasted travel + setup

    # money, PHP
    wage_day: float = 755.0 * 1.25     # NCR-28 minimum wage + 25% on-cost
    haul_cost_per_load: float = 4700.0 # Maynilad published rate
    load_m3: float = 10.0
    gate_fee_per_m3: float = 580.0     # Ormoc City ordinance benchmark


# --------------------------------------------------------------------------
# Household construction
# --------------------------------------------------------------------------


@dataclass
class Household:
    hh_id: int
    block: int
    arm: int
    tier: str
    accepts: bool
    booking_day: float
    volume_m3: float


def build_cohort(p: Params, rng: np.random.Generator) -> list[Household]:
    """Assign block, arm, access tier, acceptance and response lag."""
    households: list[Household] = []
    per_block = p.n_households // p.n_blocks

    # Arms are assigned by block, because a notification campaign is a
    # barangay-level act, not a household-level one.
    n_arm2_blocks = round(p.n_blocks * p.arm_split)
    arm2_blocks = set(rng.choice(p.n_blocks, size=n_arm2_blocks, replace=False).tolist())

    for block in range(p.n_blocks):
        arm = 2 if block in arm2_blocks else 1
        open_day = block * p.window_days

        for _ in range(per_block):
            # Access tier from the two IFC marginals. Independence is an
            # assumption, stated in the paper; it is the least informative
            # joint distribution available.
            under_house = rng.random() < p.p_under_house
            narrow = rng.random() < p.p_narrow_path
            if under_house:
                tier = "F3"
            elif narrow:
                tier = "F2"
            else:
                tier = "F1"

            if arm == 2:
                p_accept = min(0.98, p.base_accept + p.uplift)
            else:
                p_accept = p.base_accept
                if tier == "F3":
                    # In arm 1 nobody has prepared the floor, so a share of
                    # these households refuse once the crew arrives.
                    p_accept *= 1.0 - p.f3_refusal_arm1

            accepts = bool(rng.random() < p_accept)

            mean_lag = p.mean_lag_arm1_days if arm == 1 else p.mean_lag_arm2_days
            booking_day = open_day + float(rng.exponential(mean_lag))

            households.append(
                Household(
                    hh_id=len(households),
                    block=block,
                    arm=arm,
                    tier=tier,
                    accepts=accepts,
                    booking_day=booking_day,
                    volume_m3=float(rng.uniform(p.tank_m3_lo, p.tank_m3_hi)),
                )
            )
    return households


# --------------------------------------------------------------------------
# Service duration
# --------------------------------------------------------------------------


def job_minutes(hh: Household, p: Params) -> float:
    """Crew time on site, including transfer to the mother tanker."""
    if hh.tier == "F1":
        setup = p.setup_f1
    elif hh.tier == "F2":
        setup = p.setup_f2
    else:
        setup = p.setup_f3_remediated if hh.arm == 2 else p.setup_f3
    pump = hh.volume_m3 * 1000.0 / p.pump_lpm
    return setup + pump + p.transfer_min + p.travel_min


# --------------------------------------------------------------------------
# Simulation
# --------------------------------------------------------------------------


def simulate(p: Params, seed: int = 0) -> dict:
    rng = np.random.default_rng(seed)
    cohort = build_cohort(p, rng)

    env = simpy.Environment()
    crews = simpy.Resource(env, capacity=p.n_crews)

    run_minutes = p.run_days * p.day_minutes
    stats = {
        "served": 0,
        "served_arm1": 0,
        "served_arm2": 0,
        "no_booking": 0,
        "late_booking": 0,
        "no_show_final": 0,
        "cutoff": 0,
        "crew_minutes": 0.0,
        "volume_m3": 0.0,
        "waits": [],
        "completed_on_day": [],
    }

    def visit(hh: Household, attempt: int = 1):
        """One crew visit. May be wasted by a no-show, then retried once."""
        if env.now >= run_minutes:
            stats["cutoff"] += 1
            return

        cancelled = attempt == 1 and rng.random() < p.no_show

        requested_at = env.now
        with crews.request() as req:
            yield req
            start = env.now
            stats["waits"].append(start - requested_at)

            if cancelled:
                yield env.timeout(p.no_show_visit_min)
                stats["crew_minutes"] += p.no_show_visit_min
                # Retry inside the same block window if there is time.
                close = (hh.block + 1) * p.window_days * p.day_minutes
                retry_at = start + p.retry_days * p.day_minutes
                if retry_at < close and retry_at < run_minutes:
                    env.process(visit(hh, attempt=2))
                else:
                    stats["no_show_final"] += 1
                return

            duration = job_minutes(hh, p)
            yield env.timeout(duration)

            stats["crew_minutes"] += duration
            stats["served"] += 1
            stats["volume_m3"] += hh.volume_m3
            stats["completed_on_day"].append(math.floor(start / p.day_minutes))
            if hh.arm == 1:
                stats["served_arm1"] += 1
            else:
                stats["served_arm2"] += 1

    def household_process(hh: Household):
        if not hh.accepts:
            stats["no_booking"] += 1
            return

        close = (hh.block + 1) * p.window_days * p.day_minutes
        arrive_at = hh.booking_day * p.day_minutes

        # Booking after the block's window closes is a miss, whatever the
        # reason. This is what makes a slow response cost a household.
        if arrive_at >= close:
            stats["late_booking"] += 1
            return

        yield env.timeout(max(0.0, arrive_at - env.now))
        yield from visit(hh)

    for hh in cohort:
        env.process(household_process(hh))

    env.run(until=run_minutes)

    # ---------------------------------------------------------------- outputs
    total = p.n_households
    served = stats["served"]
    days_used = (
        max(stats["completed_on_day"]) + 1 if stats["completed_on_day"] else 0
    )
    capacity_minutes = p.n_crews * days_used * p.day_minutes if days_used else 0.0

    loads = math.ceil(stats["volume_m3"] / p.load_m3) if stats["volume_m3"] else 0
    labour_actual = (
        p.n_crews * p.staff_per_crew * p.wage_day * days_used
    )
    labour_staffed = (
        p.n_crews * p.staff_per_crew * p.wage_day * p.run_days
    )
    hauling = loads * p.haul_cost_per_load
    gate = stats["volume_m3"] * p.gate_fee_per_m3
    cost_actual = labour_actual + hauling + gate
    cost_staffed = labour_staffed + hauling + gate

    arm1_total = sum(1 for h in cohort if h.arm == 1)
    arm2_total = total - arm1_total

    return {
        "seed": seed,
        "n_households": total,
        "served": served,
        "served_arm1": stats["served_arm1"],
        "served_arm2": stats["served_arm2"],
        "arm1_rate": stats["served_arm1"] / arm1_total if arm1_total else 0.0,
        "arm2_rate": stats["served_arm2"] / arm2_total if arm2_total else 0.0,
        "arm_diff": (
            stats["served_arm2"] / arm2_total - stats["served_arm1"] / arm1_total
            if arm1_total and arm2_total
            else 0.0
        ),
        "completion_rate": served / total,
        "no_booking": stats["no_booking"],
        "late_booking": stats["late_booking"],
        "no_show_final": stats["no_show_final"],
        "cutoff": stats["cutoff"],
        "volume_m3": round(stats["volume_m3"], 2),
        "days_used": days_used,
        "crew_utilisation": (
            stats["crew_minutes"] / capacity_minutes if capacity_minutes else 0.0
        ),
        "loads": loads,
        "cost_actual_php": round(cost_actual, 0),
        "cost_staffed_php": round(cost_staffed, 0),
        "cost_per_hh_actual": round(cost_actual / served, 0) if served else 0.0,
        "cost_per_hh_staffed": round(cost_staffed / served, 0) if served else 0.0,
        "crew_minutes_per_hh": round(stats["crew_minutes"] / served, 1) if served else 0.0,
        "wait_median_min": round(statistics.median(stats["waits"]), 0) if stats["waits"] else 0.0,
        "wait_p90_min": round(
            float(np.percentile(stats["waits"], 90)), 0
        ) if stats["waits"] else 0.0,
    }


# --------------------------------------------------------------------------
# Replicates
# --------------------------------------------------------------------------


def summarise(p: Params, reps: int = 100, seed0: int = 0) -> dict:
    runs = [simulate(p, seed=seed0 + i) for i in range(reps)]

    def ci(key: str) -> tuple[float, float, float]:
        vals = [r[key] for r in runs]
        m = statistics.fmean(vals)
        if reps < 2:
            return m, m, m
        half = 1.96 * statistics.stdev(vals) / math.sqrt(reps)
        return m, m - half, m + half

    keys = [
        "completion_rate",
        "arm1_rate",
        "arm2_rate",
        "arm_diff",
        "days_used",
        "cost_per_hh_actual",
        "cost_per_hh_staffed",
        "crew_utilisation",
        "crew_minutes_per_hh",
        "wait_median_min",
        "wait_p90_min",
        "no_booking",
        "late_booking",
        "no_show_final",
    ]
    out = {"params": asdict(p), "reps": reps}
    for k in keys:
        m, lo, hi = ci(k)
        out[k] = round(m, 3 if isinstance(m, float) and abs(m) < 100 else 0)
        out[k + "_lo"] = round(lo, 3 if abs(lo) < 100 else 0)
        out[k + "_hi"] = round(hi, 3 if abs(hi) < 100 else 0)
    return out


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------


def main() -> None:
    ap = argparse.ArgumentParser(description="Desludging campaign simulation")
    ap.add_argument("--uplift", type=float, default=None, help="arm 2 effect, 0-0.4")
    ap.add_argument("--base", type=float, default=None, help="baseline acceptance")
    ap.add_argument("--crews", type=int, default=None)
    ap.add_argument("--reps", type=int, default=1)
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()

    p = Params()
    if args.uplift is not None:
        p.uplift = args.uplift
    if args.base is not None:
        p.base_accept = args.base
    if args.crews is not None:
        p.n_crews = args.crews

    if args.reps > 1:
        s = summarise(p, reps=args.reps, seed0=args.seed)
        for k, v in s.items():
            if k != "params":
                print(f"{k:<28} {v}")
        return

    r = simulate(p, seed=args.seed)
    width = max(len(k) for k in r)
    for k, v in r.items():
        print(f"{k:<{width}}  {v}")


if __name__ == "__main__":
    main()
