from __future__ import annotations

import math
from dataclasses import dataclass

from river_model.inputs import Params


@dataclass(frozen=True)
class CostInputs:
    sheds: int
    heads: int
    modules: int
    tankers: int
    carts: int
    trips_week: float
    vs_diverted_year: float
    annual_mpn_prevented_12: float


@dataclass(frozen=True)
class CostResult:
    capex: float
    opex_12m: float
    contingency: float
    cash_12m: float
    npc: float
    eac: float
    revenue_credit: float
    php_per_shed_month: float
    php_per_mpn12: float
    php_per_vs_kg: float
    fee_per_head_month: float


def compute_costs(params: Params, inputs: CostInputs) -> CostResult:
    capex = (
        inputs.modules * params.cap_digester
        + inputs.tankers * params.cap_tanker
        + inputs.carts * params.cap_cart
        + params.cap_pad
        + inputs.modules * params.cap_gas_kit
        + params.cap_site
        + params.cap_meters
        + params.cap_training
        + params.cap_manifest
        + params.cap_shed_fund
        + params.cap_replication
    )

    opex_12m = (
        params.opex_staff_year * params.pilot_months / 12.0
        + params.opex_sampling_year * params.pilot_months / 12.0
        + params.opex_maint_frac * capex
        + inputs.trips_week * 52.0 * params.opex_trip * params.pilot_months / 12.0
        + params.opex_admin_year * params.pilot_months / 12.0
    )

    subtotal = capex + opex_12m
    contingency = params.contingency_rate * subtotal
    cash_12m = subtotal + contingency

    replacement = params.replacement_capex_frac * capex
    npc = capex + contingency
    for year in range(1, params.asset_life + 1):
        annual_opex = (
            params.opex_staff_year
            + params.opex_sampling_year
            + params.opex_maint_frac * capex
            + inputs.trips_week * 52.0 * params.opex_trip
            + params.opex_admin_year
        )
        cash_flow = annual_opex
        if year == params.replacement_year:
            cash_flow += replacement
        npc += cash_flow / (1.0 + params.discount) ** year

    if params.discount == 0.0:
        eac = npc / params.asset_life
    else:
        crf = (
            params.discount
            * (1.0 + params.discount) ** params.asset_life
            / ((1.0 + params.discount) ** params.asset_life - 1.0)
        )
        eac = npc * crf

    revenue_credit = 0.0
    return CostResult(
        capex=capex,
        opex_12m=opex_12m,
        contingency=contingency,
        cash_12m=cash_12m,
        npc=npc,
        eac=eac,
        revenue_credit=revenue_credit,
        php_per_shed_month=eac / (inputs.sheds * 12.0),
        php_per_mpn12=(
            eac / inputs.annual_mpn_prevented_12
            if inputs.annual_mpn_prevented_12 > 0
            else float("inf")
        ),
        php_per_vs_kg=(
            eac / inputs.vs_diverted_year
            if inputs.vs_diverted_year > 0
            else float("inf")
        ),
        fee_per_head_month=eac / (inputs.heads * 12.0),
    )
