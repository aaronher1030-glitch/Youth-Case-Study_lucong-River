from __future__ import annotations

import math
from dataclasses import dataclass
from numbers import Integral, Real

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


def _validate_integer(
    name: str, value: object, minimum: int, maximum: int | None = None
) -> None:
    if isinstance(value, bool) or not isinstance(value, Integral):
        raise ValueError(f"{name} must be a finite integer")
    if value < minimum or (maximum is not None and value > maximum):
        if maximum is None:
            raise ValueError(
                f"{name} must be an integer greater than or equal to {minimum}"
            )
        raise ValueError(f"{name} must be an integer from {minimum} through {maximum}")


def _validate_number(
    name: str, value: object, minimum: float = 0.0, maximum: float | None = None
) -> None:
    if isinstance(value, bool) or not isinstance(value, Real):
        raise ValueError(f"{name} must be a finite number")
    try:
        finite = math.isfinite(value)
    except (OverflowError, TypeError, ValueError):
        finite = False
    if not finite:
        raise ValueError(f"{name} must be finite")
    if value < minimum or (maximum is not None and value > maximum):
        if maximum is None:
            raise ValueError(f"{name} must be greater than or equal to {minimum}")
        raise ValueError(f"{name} must be from {minimum} through {maximum}")


def _validate_cost_inputs(inputs: CostInputs) -> None:
    for name in ("sheds", "heads"):
        _validate_integer(name, getattr(inputs, name), minimum=1)
    for name in ("modules", "tankers", "carts"):
        _validate_integer(name, getattr(inputs, name), minimum=0)
    for name in ("trips_week", "vs_diverted_year", "annual_mpn_prevented_12"):
        _validate_number(name, getattr(inputs, name))


def _validate_params(params: Params) -> None:
    for name in (
        "cap_digester",
        "cap_tanker",
        "cap_cart",
        "cap_pad",
        "cap_gas_kit",
        "cap_site",
        "cap_meters",
        "cap_training",
        "cap_manifest",
        "cap_shed_fund",
        "cap_replication",
        "opex_staff_year",
        "opex_sampling_year",
        "opex_trip",
        "opex_admin_year",
    ):
        _validate_number(name, getattr(params, name))
    for name in ("contingency_rate", "opex_maint_frac", "replacement_capex_frac"):
        _validate_number(name, getattr(params, name), maximum=1.0)
    _validate_number("discount", params.discount)
    _validate_integer("asset_life", params.asset_life, minimum=1)
    _validate_integer(
        "replacement_year",
        params.replacement_year,
        minimum=1,
        maximum=params.asset_life,
    )
    _validate_integer("pilot_months", params.pilot_months, minimum=1, maximum=12)


def compute_costs(params: Params, inputs: CostInputs) -> CostResult:
    _validate_cost_inputs(inputs)
    _validate_params(params)

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
        crf = params.discount / (
            -math.expm1(-params.asset_life * math.log1p(params.discount))
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
