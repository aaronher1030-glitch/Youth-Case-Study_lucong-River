from __future__ import annotations

import itertools
import math
from dataclasses import dataclass
from typing import Sequence

from river_model.economics import CostInputs, CostResult, compute_costs
from river_model.inputs import Params, Shed, eligible_sheds
from river_model.load import LoadResult, compute_load
from river_model.process import ProcessResult, compute_process


@dataclass(frozen=True)
class Design:
    shed_ids: tuple[str, ...]
    modules: int
    tankers: int
    carts: int
    collection_days_week: int


@dataclass(frozen=True)
class DesignEvaluation:
    design: Design
    load: LoadResult
    process: ProcessResult
    costs: CostResult
    checks: dict[str, bool]
    rejection_reasons: tuple[str, ...]


def constraint_feasible(evaluation: DesignEvaluation) -> bool:
    return all(evaluation.checks.values()) and not evaluation.rejection_reasons


def enumerate_designs(params: Params, sheds: Sequence[Shed]) -> list[DesignEvaluation]:
    confirmed = sorted(eligible_sheds(sheds), key=lambda shed: shed.shed_id)
    barangays = sorted({shed.barangay for shed in confirmed})
    evaluations: list[DesignEvaluation] = []

    for cluster_count in range(1, len(barangays) + 1):
        for cluster in itertools.combinations(barangays, cluster_count):
            subset = tuple(shed for shed in confirmed if shed.barangay in cluster)
            load = compute_load(params, subset)
            process = compute_process(params, subset)
            carts = math.ceil(len(subset) / 8)
            vs_diverted_year = (
                process.vs_in_kg_day
                * params.p_enroll
                * params.p_collect
                * params.p_retain
                * 365
            )

            for collection_days_week in (1, 2):
                min_modules = max(
                    1,
                    math.ceil(
                        process.slurry_m3_day * params.hrt_min_days / params.module_m3
                    ),
                )
                min_tankers = max(
                    1,
                    math.ceil(
                        process.trips_week
                        / (
                            collection_days_week
                            * params.trips_day_cap
                            * params.utilization
                        )
                    ),
                )
                for modules in range(
                    min_modules, min_modules + params.max_extra_modules + 1
                ):
                    for tankers in range(
                        min_tankers, min_tankers + params.max_extra_tankers + 1
                    ):
                        costs = compute_costs(
                            params,
                            CostInputs(
                                sheds=len(subset),
                                heads=load.heads,
                                modules=modules,
                                tankers=tankers,
                                carts=carts,
                                trips_week=process.trips_week,
                                vs_diverted_year=vs_diverted_year,
                                annual_mpn_prevented_12=load.annual_mpn_prevented_12,
                            ),
                        )
                        land_evidence_present = params.land_available_ha is not None
                        checks = {
                            "duration": params.pilot_months <= 12,
                            "budget": costs.cash_12m <= params.budget,
                            "focus_stream": params.focus_stream_share >= 0.70,
                            "digester": (
                                modules * params.module_m3
                                >= process.slurry_m3_day * params.hrt_min_days
                            ),
                            "tanker": (
                                process.trips_week
                                <= tankers
                                * collection_days_week
                                * params.trips_day_cap
                                * params.utilization
                            ),
                            "land": (
                                land_evidence_present
                                and process.land_ha_required <= params.land_available_ha
                            ),
                            "load_reconciliation": load.reconciliation_ok,
                            "mass_balance": process.vs_balance_error_pct <= 5.0,
                        }
                        rejection_reasons: list[str] = []
                        if not checks["duration"]:
                            rejection_reasons.append("pilot exceeds 12 months")
                        if not checks["budget"]:
                            rejection_reasons.append("cash requirement exceeds budget")
                        if not checks["focus_stream"]:
                            rejection_reasons.append("focus-stream share below 70%")
                        if not checks["digester"]:
                            rejection_reasons.append("digester retention too short")
                        if not checks["tanker"]:
                            rejection_reasons.append("tanker capacity insufficient")
                        if not checks["land"]:
                            if land_evidence_present:
                                rejection_reasons.append(
                                    "land requirement exceeds available area"
                                )
                            else:
                                rejection_reasons.append("land evidence missing")
                        if not checks["load_reconciliation"]:
                            rejection_reasons.append("source loads do not reconcile")
                        if not checks["mass_balance"]:
                            rejection_reasons.append(
                                "mass balance error exceeds 5%"
                            )

                        evaluations.append(
                            DesignEvaluation(
                                design=Design(
                                    shed_ids=tuple(shed.shed_id for shed in subset),
                                    modules=modules,
                                    tankers=tankers,
                                    carts=carts,
                                    collection_days_week=collection_days_week,
                                ),
                                load=load,
                                process=process,
                                costs=costs,
                                checks=checks,
                                rejection_reasons=tuple(rejection_reasons),
                            )
                        )

    evaluations.sort(
        key=lambda row: (
            row.costs.eac,
            row.costs.cash_12m,
            -len(row.design.shed_ids),
        )
    )
    return evaluations


@dataclass(frozen=True)
class Alternative:
    name: str
    source_share_low: float
    source_share_mode: float
    source_share_high: float
    capture_low: float
    capture_mode: float
    capture_high: float
    capex_low: float | None
    capex_mode: float | None
    capex_high: float | None
    opex_low: float | None
    opex_mode: float | None
    opex_high: float | None
    legal_status: str
    measurable_12m: bool
    note: str


@dataclass(frozen=True)
class AlternativeEvaluation:
    name: str
    c_end_low_mpn_100ml: float
    c_end_mode_mpn_100ml: float
    c_end_high_mpn_100ml: float
    annual_mpn_prevented_12_mode: float
    cash_12m_mode: float | None
    eac_mode: float | None
    cost_status: str
    legal_status: str
    measurable_12m: bool
    note: str


def evaluate_alternatives(params: Params) -> list[AlternativeEvaluation]:
    alternatives = (
        Alternative(
            name="Do nothing / enforcement only",
            source_share_low=0.0,
            source_share_mode=0.0,
            source_share_high=0.0,
            capture_low=0.0,
            capture_mode=0.0,
            capture_high=0.0,
            capex_low=0.0,
            capex_mode=0.0,
            capex_high=0.0,
            opex_low=0.0,
            opex_mode=0.0,
            opex_high=0.0,
            legal_status="No new permit; enforcement-only precedent failed",
            measurable_12m=True,
            note="Counterfactual: river condition remains at baseline unless external conditions change.",
        ),
        Alternative(
            name="Household septage service",
            source_share_low=0.10,
            source_share_mode=0.30,
            source_share_high=0.50,
            capture_low=0.50,
            capture_mode=0.70,
            capture_high=0.90,
            capex_low=None,
            capex_mode=None,
            capex_high=None,
            opex_low=None,
            opex_mode=None,
            opex_high=None,
            legal_status="Requires LGU septage program and disposal permits",
            measurable_12m=True,
            note="Source share and costs are unresolved assumptions; do not rank this option as cheaper until quoted.",
        ),
        Alternative(
            name="In-stream screen and dredge",
            source_share_low=0.00,
            source_share_mode=0.00,
            source_share_high=0.10,
            capture_low=0.00,
            capture_mode=0.00,
            capture_high=0.10,
            capex_low=None,
            capex_mode=None,
            capex_high=None,
            opex_low=None,
            opex_mode=None,
            opex_high=None,
            legal_status="Easement and disposal permits unresolved",
            measurable_12m=False,
            note="No evidence that screening reduces fecal coliform; dredging may resuspend solids.",
        ),
    )

    l0_mpn_day = params.c0_mpn_100ml * params.q_m3_s * 86_400 * 10_000
    evaluations: list[AlternativeEvaluation] = []
    for alternative in alternatives:
        c_end_low = params.c0_mpn_100ml * (
            1.0 - alternative.source_share_high * alternative.capture_high
        )
        c_end_mode = params.c0_mpn_100ml * (
            1.0 - alternative.source_share_mode * alternative.capture_mode
        )
        c_end_high = params.c0_mpn_100ml * (
            1.0 - alternative.source_share_low * alternative.capture_low
        )
        annual_mpn_prevented_12_mode = (
            alternative.source_share_mode
            * alternative.capture_mode
            * l0_mpn_day
            * 365
            / 1.0e12
        )

        cash_12m_mode: float | None = None
        eac_mode: float | None = None
        cost_status = "missing"
        if (
            alternative.capex_mode is not None
            and alternative.opex_mode is not None
        ):
            subtotal = alternative.capex_mode + alternative.opex_mode
            contingency = params.contingency_rate * subtotal
            cash_12m_mode = subtotal + contingency
            npc = alternative.capex_mode + contingency
            replacement = params.replacement_capex_frac * alternative.capex_mode
            for year in range(1, params.asset_life + 1):
                cash_flow = alternative.opex_mode
                if year == params.replacement_year:
                    cash_flow += replacement
                npc += cash_flow / (1.0 + params.discount) ** year
            if params.discount == 0.0:
                eac_mode = npc / params.asset_life
            else:
                crf = params.discount / (
                    -math.expm1(-params.asset_life * math.log1p(params.discount))
                )
                eac_mode = npc * crf
            cost_status = "sourced"

        evaluations.append(
            AlternativeEvaluation(
                name=alternative.name,
                c_end_low_mpn_100ml=c_end_low,
                c_end_mode_mpn_100ml=c_end_mode,
                c_end_high_mpn_100ml=c_end_high,
                annual_mpn_prevented_12_mode=annual_mpn_prevented_12_mode,
                cash_12m_mode=cash_12m_mode,
                eac_mode=eac_mode,
                cost_status=cost_status,
                legal_status=alternative.legal_status,
                measurable_12m=alternative.measurable_12m,
                note=alternative.note,
            )
        )
    return evaluations
