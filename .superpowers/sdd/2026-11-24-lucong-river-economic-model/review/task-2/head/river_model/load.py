from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from river_model.inputs import Params, Shed, eligible_sheds


@dataclass(frozen=True)
class LoadResult:
    heads: int
    l_gen_mpn_day: float
    l0_mpn_day: float
    l_target_mpn_day: float
    r: float
    c: float
    c0_mpn_100ml: float
    c_end_mpn_100ml: float
    reduction_fraction: float
    annual_mpn_prevented_12: float
    reconciliation_ok: bool
    top_down_r: float | None


def compute_load(params: Params, sheds: Sequence[Shed]) -> LoadResult:
    active = eligible_sheds(sheds)
    heads = sum(s.heads for s in active)
    l_gen = heads * params.e_head_day
    l0 = params.c0_mpn_100ml * params.q_m3_s * 86_400 * 10_000
    l_target = params.eta * l_gen
    r = l_target / l0

    if r > 1.0 + 1e-9:
        raise ValueError(
            f"source share exceeds 1: r={r:.6f}; revise source or flow inputs"
        )
    r = max(0.0, r)

    c = params.p_enroll * params.p_collect * params.p_retain
    reduction = r * c
    c_end = params.c0_mpn_100ml * (1 - reduction)

    top_down_r = None
    reconciliation_ok = True
    if params.upstream_mpn_100ml is not None:
        top_down_r = max(
            0.0,
            (params.c0_mpn_100ml - params.upstream_mpn_100ml)
            / params.c0_mpn_100ml,
        )
        reconciliation_ok = abs(r - top_down_r) <= params.source_share_tolerance

    annual_mpn_prevented_12 = reduction * l0 * 365 / 1.0e12
    return LoadResult(
        heads=heads,
        l_gen_mpn_day=l_gen,
        l0_mpn_day=l0,
        l_target_mpn_day=l_target,
        r=r,
        c=c,
        c0_mpn_100ml=params.c0_mpn_100ml,
        c_end_mpn_100ml=c_end,
        reduction_fraction=reduction,
        annual_mpn_prevented_12=annual_mpn_prevented_12,
        reconciliation_ok=reconciliation_ok,
        top_down_r=top_down_r,
    )
