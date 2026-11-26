from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from river_model.inputs import Params, Shed, eligible_sheds


@dataclass(frozen=True)
class ProcessResult:
    heads: int
    manure_kg_day: float
    wash_m3_day: float
    slurry_m3_day: float
    dm_in_kg_day: float
    vs_in_kg_day: float
    vs_destroyed_kg_day: float
    vs_remaining_kg_day: float
    dm_remaining_kg_day: float
    vs_balance_error_pct: float
    ch4_m3_day: float
    biogas_m3_day: float
    lpg_kg_day: float
    nutrient_n_kg_day: float
    land_ha_required: float
    trips_week: float


def compute_process(params: Params, sheds: Sequence[Shed]) -> ProcessResult:
    active = eligible_sheds(sheds)
    heads = sum(s.heads for s in active)
    manure = heads * params.manure_kg_head_day
    wash = heads * params.washwater_l_head_day / 1000.0
    slurry = manure / 1000.0 + wash

    dm_in = manure * params.dm_frac
    vs_in = dm_in * params.vs_frac_dm
    vs_destroyed = vs_in * params.vs_destroyed
    vs_remaining = vs_in - vs_destroyed
    dm_remaining = dm_in - vs_destroyed

    balance_error = (
        abs(dm_in - (vs_destroyed + dm_remaining)) / dm_in * 100.0
        if dm_in > 0
        else 0.0
    )

    ch4 = vs_destroyed * params.ch4_yield
    biogas = ch4 / params.ch4_frac
    lpg = ch4 * params.ch4_mj_m3 / params.lpg_mj_kg

    nutrient_n = dm_remaining * params.n_frac_dm
    land_ha = nutrient_n * 365.0 / params.rice_n_kg_ha
    trips_week = slurry * 7.0 / params.tanker_m3

    return ProcessResult(
        heads=heads,
        manure_kg_day=manure,
        wash_m3_day=wash,
        slurry_m3_day=slurry,
        dm_in_kg_day=dm_in,
        vs_in_kg_day=vs_in,
        vs_destroyed_kg_day=vs_destroyed,
        vs_remaining_kg_day=vs_remaining,
        dm_remaining_kg_day=dm_remaining,
        vs_balance_error_pct=balance_error,
        ch4_m3_day=ch4,
        biogas_m3_day=biogas,
        lpg_kg_day=lpg,
        nutrient_n_kg_day=nutrient_n,
        land_ha_required=land_ha,
        trips_week=trips_week,
    )
