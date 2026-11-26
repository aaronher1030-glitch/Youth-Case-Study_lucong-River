from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
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


def _require_finite(name: str, value: object) -> None:
    try:
        finite = isfinite(value)
    except TypeError as exc:
        raise ValueError(f"{name} must be finite") from exc
    if not finite:
        raise ValueError(f"{name} must be finite")


def compute_load(params: Params, sheds: Sequence[Shed]) -> LoadResult:
    for name in (
        "c0_mpn_100ml",
        "q_m3_s",
        "e_head_day",
        "eta",
        "p_enroll",
        "p_collect",
        "p_retain",
        "source_share_tolerance",
    ):
        _require_finite(name, getattr(params, name))
    if params.upstream_mpn_100ml is not None:
        _require_finite("upstream_mpn_100ml", params.upstream_mpn_100ml)

    if params.c0_mpn_100ml <= 0:
        raise ValueError("c0_mpn_100ml must be positive")
    if params.q_m3_s <= 0:
        raise ValueError("q_m3_s must be positive")
    if params.e_head_day < 0:
        raise ValueError("e_head_day must be nonnegative")
    for name in ("eta", "p_enroll", "p_collect", "p_retain", "source_share_tolerance"):
        if not 0 <= getattr(params, name) <= 1:
            raise ValueError(f"{name} must be between 0 and 1")
    if params.upstream_mpn_100ml is not None and params.upstream_mpn_100ml < 0:
        raise ValueError("upstream_mpn_100ml must be nonnegative")

    active = eligible_sheds(sheds)
    for shed in active:
        _require_finite("eligible shed heads", shed.heads)
        if shed.heads < 0:
            raise ValueError("eligible shed heads must be nonnegative")
    heads = sum(s.heads for s in active)
    l_gen = heads * params.e_head_day
    l0 = params.c0_mpn_100ml * params.q_m3_s * 86_400 * 10_000
    l_target = params.eta * l_gen
    r = l_target / l0

    if r > 1.0:
        raise ValueError(
            f"source share exceeds 1: r={r:.6f}; revise source or flow inputs"
        )
    if r < 0.0:
        raise ValueError(f"source share must be nonnegative: r={r:.6f}")

    c = params.p_enroll * params.p_collect * params.p_retain
    reduction = r * c
    c_end = params.c0_mpn_100ml * (1 - reduction)

    top_down_r = None
    reconciliation_ok = True
    if params.upstream_mpn_100ml is not None:
        top_down_r = (
            params.c0_mpn_100ml - params.upstream_mpn_100ml
        ) / params.c0_mpn_100ml
        if top_down_r < 0:
            reconciliation_ok = False
        else:
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
