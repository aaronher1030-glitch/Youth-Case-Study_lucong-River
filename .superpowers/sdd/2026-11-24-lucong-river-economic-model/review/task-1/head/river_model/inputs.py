from __future__ import annotations

import csv
from dataclasses import dataclass, fields, replace
from pathlib import Path
from typing import Literal, Mapping, Sequence, get_args, get_type_hints

Status = Literal["measured", "sourced", "derived", "assumption", "missing", "design"]


@dataclass(frozen=True)
class Shed:
    shed_id: str
    barangay: str
    heads: int
    drains_to_reach: bool | None
    source: str


@dataclass(frozen=True)
class Params:
    c0_mpn_100ml: float = 16_000.0
    q_m3_s: float = 0.05
    e_head_day: float = 1.0e9
    eta: float = 1.0
    p_enroll: float = 0.95
    p_collect: float = 0.95
    p_retain: float = 0.95
    upstream_mpn_100ml: float | None = None
    source_share_tolerance: float = 0.10

    manure_kg_head_day: float = 2.0
    washwater_l_head_day: float = 22.0
    dm_frac: float = 0.20
    vs_frac_dm: float = 0.80
    vs_destroyed: float = 0.50
    ch4_yield: float = 0.35
    ch4_frac: float = 0.60
    lpg_mj_kg: float = 46.0
    ch4_mj_m3: float = 35.8
    n_frac_dm: float = 0.04
    rice_n_kg_ha: float = 120.0
    land_available_ha: float | None = None

    cap_digester: float = 380_000.0
    cap_tanker: float = 1_450_000.0
    cap_cart: float = 180_000.0
    cap_pad: float = 980_000.0
    cap_gas_kit: float = 45_000.0
    cap_site: float = 420_000.0
    cap_meters: float = 180_000.0
    cap_training: float = 320_000.0
    cap_manifest: float = 155_000.0
    cap_shed_fund: float = 700_000.0
    cap_replication: float = 600_000.0
    opex_staff_year: float = 1_140_000.0
    opex_sampling_year: float = 480_000.0
    opex_maint_frac: float = 0.05
    opex_trip: float = 700.0
    opex_admin_year: float = 60_000.0
    contingency_rate: float = 0.10

    workdays_week: int = 6
    trips_day_cap: int = 5
    tanker_m3: float = 2.0
    module_m3: float = 25.0
    hrt_min_days: float = 10.0
    utilization: float = 0.80

    budget: float = 10_000_000.0
    discount: float = 0.08
    asset_life: int = 10
    replacement_year: int = 5
    replacement_capex_frac: float = 0.25

    pilot_months: int = 12
    target_mpn_100ml: float = 8_000.0
    target_probability: float = 0.80
    focus_stream_share: float = 1.0
    max_extra_modules: int = 2
    max_extra_tankers: int = 2


PARAMETER_META: dict[str, dict[str, str]] = {
    "c0_mpn_100ml": {
        "unit": "MPN/100 mL",
        "status": "sourced",
        "source": "MODEL_SPEC_LUCONG.md baseline; retain the cited source for research use.",
    },
    "q_m3_s": {
        "unit": "m3/s",
        "status": "assumption",
        "source": "Field measurement or literature verification is required.",
    },
    "e_head_day": {
        "unit": "MPN/head/day",
        "status": "assumption",
        "source": "Field measurement or literature verification is required.",
    },
    "eta": {
        "unit": "fraction",
        "status": "assumption",
        "source": "Field measurement or literature verification is required.",
    },
    "p_enroll": {
        "unit": "fraction",
        "status": "assumption",
        "source": "Planning assumption; verify with enrollment records.",
    },
    "p_collect": {
        "unit": "fraction",
        "status": "assumption",
        "source": "Planning assumption; verify with collection monitoring.",
    },
    "p_retain": {
        "unit": "fraction",
        "status": "assumption",
        "source": "Planning assumption; verify with service-use monitoring.",
    },
    "upstream_mpn_100ml": {
        "unit": "MPN/100 mL",
        "status": "missing",
        "source": "No upstream river water-quality measurement supplied.",
    },
    "source_share_tolerance": {
        "unit": "fraction",
        "status": "design",
        "source": "Research design choice for acceptable source-share error.",
    },
    "manure_kg_head_day": {
        "unit": "kg/head/day",
        "status": "assumption",
        "source": "MODEL_SPEC_LUCONG.md baseline; verify with field measurement or literature.",
    },
    "washwater_l_head_day": {
        "unit": "L/head/day",
        "status": "assumption",
        "source": "MODEL_SPEC_LUCONG.md baseline; verify with field measurement or literature.",
    },
    "dm_frac": {
        "unit": "fraction",
        "status": "assumption",
        "source": "MODEL_SPEC_LUCONG.md baseline; verify with field measurement or literature.",
    },
    "vs_frac_dm": {
        "unit": "fraction",
        "status": "assumption",
        "source": "MODEL_SPEC_LUCONG.md baseline; verify with field measurement or literature.",
    },
    "vs_destroyed": {
        "unit": "fraction",
        "status": "assumption",
        "source": "MODEL_SPEC_LUCONG.md baseline; verify with digester operating data or literature.",
    },
    "ch4_yield": {
        "unit": "m3 CH4/kg VS",
        "status": "assumption",
        "source": "MODEL_SPEC_LUCONG.md baseline; verify with substrate-specific literature.",
    },
    "ch4_frac": {
        "unit": "fraction",
        "status": "assumption",
        "source": "MODEL_SPEC_LUCONG.md baseline; verify with biogas composition data.",
    },
    "lpg_mj_kg": {
        "unit": "MJ/kg",
        "status": "sourced",
        "source": "MODEL_SPEC_LUCONG.md LPG energy-content baseline.",
    },
    "ch4_mj_m3": {
        "unit": "MJ/m3",
        "status": "sourced",
        "source": "MODEL_SPEC_LUCONG.md methane energy-content baseline.",
    },
    "n_frac_dm": {
        "unit": "kg N/kg DM",
        "status": "assumption",
        "source": "MODEL_SPEC_LUCONG.md baseline; verify with manure analysis or literature.",
    },
    "rice_n_kg_ha": {
        "unit": "kg N/ha",
        "status": "assumption",
        "source": "MODEL_SPEC_LUCONG.md baseline; verify with agronomic recommendations.",
    },
    "land_available_ha": {
        "unit": "ha",
        "status": "missing",
        "source": "No verified land availability supplied.",
    },
    "cap_digester": {
        "unit": "PHP",
        "status": "design",
        "source": "MODEL_SPEC_LUCONG.md planning capital cap; validate with local quotations.",
    },
    "cap_tanker": {
        "unit": "PHP",
        "status": "design",
        "source": "MODEL_SPEC_LUCONG.md planning capital cap; validate with local quotations.",
    },
    "cap_cart": {
        "unit": "PHP",
        "status": "design",
        "source": "MODEL_SPEC_LUCONG.md planning capital cap; validate with local quotations.",
    },
    "cap_pad": {
        "unit": "PHP",
        "status": "design",
        "source": "MODEL_SPEC_LUCONG.md planning capital cap; validate with local quotations.",
    },
    "cap_gas_kit": {
        "unit": "PHP",
        "status": "design",
        "source": "MODEL_SPEC_LUCONG.md planning capital cap; validate with local quotations.",
    },
    "cap_site": {
        "unit": "PHP",
        "status": "design",
        "source": "MODEL_SPEC_LUCONG.md planning capital cap; validate with local quotations.",
    },
    "cap_meters": {
        "unit": "PHP",
        "status": "design",
        "source": "MODEL_SPEC_LUCONG.md planning capital cap; validate with local quotations.",
    },
    "cap_training": {
        "unit": "PHP",
        "status": "design",
        "source": "MODEL_SPEC_LUCONG.md planning capital cap; validate with local quotations.",
    },
    "cap_manifest": {
        "unit": "PHP",
        "status": "design",
        "source": "MODEL_SPEC_LUCONG.md planning capital cap; validate with local quotations.",
    },
    "cap_shed_fund": {
        "unit": "PHP",
        "status": "design",
        "source": "MODEL_SPEC_LUCONG.md planning capital cap; validate with local quotations.",
    },
    "cap_replication": {
        "unit": "PHP",
        "status": "design",
        "source": "MODEL_SPEC_LUCONG.md planning capital cap; validate with local quotations.",
    },
    "opex_staff_year": {
        "unit": "PHP/year",
        "status": "assumption",
        "source": "MODEL_SPEC_LUCONG.md planning estimate; verify with local staffing costs.",
    },
    "opex_sampling_year": {
        "unit": "PHP/year",
        "status": "assumption",
        "source": "MODEL_SPEC_LUCONG.md planning estimate; verify with laboratory quotations.",
    },
    "opex_maint_frac": {
        "unit": "fraction/year",
        "status": "assumption",
        "source": "MODEL_SPEC_LUCONG.md planning estimate; verify with maintenance records.",
    },
    "opex_trip": {
        "unit": "PHP/trip",
        "status": "assumption",
        "source": "MODEL_SPEC_LUCONG.md planning estimate; verify with local hauling rates.",
    },
    "opex_admin_year": {
        "unit": "PHP/year",
        "status": "assumption",
        "source": "MODEL_SPEC_LUCONG.md planning estimate; verify with administrative costs.",
    },
    "contingency_rate": {
        "unit": "fraction",
        "status": "design",
        "source": "Research design choice for capital-cost contingency.",
    },
    "workdays_week": {
        "unit": "days/week",
        "status": "assumption",
        "source": "MODEL_SPEC_LUCONG.md operating assumption; verify with service schedule.",
    },
    "trips_day_cap": {
        "unit": "trips/day",
        "status": "design",
        "source": "Research design choice for daily collection capacity.",
    },
    "tanker_m3": {
        "unit": "m3",
        "status": "design",
        "source": "MODEL_SPEC_LUCONG.md vehicle sizing assumption; verify supplier specifications.",
    },
    "module_m3": {
        "unit": "m3",
        "status": "design",
        "source": "MODEL_SPEC_LUCONG.md modular sizing assumption; verify supplier specifications.",
    },
    "hrt_min_days": {
        "unit": "days",
        "status": "assumption",
        "source": "MODEL_SPEC_LUCONG.md operating assumption; verify design literature and climate.",
    },
    "utilization": {
        "unit": "fraction",
        "status": "design",
        "source": "Research design choice for effective capacity utilization.",
    },
    "budget": {
        "unit": "PHP",
        "status": "design",
        "source": "Research design budget constraint from MODEL_SPEC_LUCONG.md.",
    },
    "discount": {
        "unit": "fraction/year",
        "status": "assumption",
        "source": "Financial-analysis assumption; verify against the study's chosen rate.",
    },
    "asset_life": {
        "unit": "years",
        "status": "design",
        "source": "Research design duration for economic appraisal.",
    },
    "replacement_year": {
        "unit": "year",
        "status": "design",
        "source": "Research design duration for scheduled replacement.",
    },
    "replacement_capex_frac": {
        "unit": "fraction",
        "status": "assumption",
        "source": "Financial-analysis assumption; verify with equipment replacement quotations.",
    },
    "pilot_months": {
        "unit": "months",
        "status": "design",
        "source": "Research design duration for the pilot.",
    },
    "target_mpn_100ml": {
        "unit": "MPN/100 mL",
        "status": "design",
        "source": "Research design target for treated effluent quality.",
    },
    "target_probability": {
        "unit": "fraction",
        "status": "design",
        "source": "Research design target for scenario success probability.",
    },
    "focus_stream_share": {
        "unit": "fraction",
        "status": "design",
        "source": "Research design choice for the focus stream share.",
    },
    "max_extra_modules": {
        "unit": "modules",
        "status": "design",
        "source": "Research design limit on additional digester modules.",
    },
    "max_extra_tankers": {
        "unit": "tankers",
        "status": "design",
        "source": "Research design limit on additional tankers.",
    },
}


_CENSUS_COLUMNS = {"shed_id", "barangay", "heads", "drains_to_reach", "source"}


def load_census(path: Path) -> tuple[Shed, ...]:
    sheds: list[Shed] = []
    seen_ids: set[str] = set()
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None or not _CENSUS_COLUMNS.issubset(reader.fieldnames):
            raise ValueError("census CSV is missing required columns")
        for row in reader:
            raw_shed_id = row["shed_id"]
            shed_id = raw_shed_id.strip() if raw_shed_id is not None else ""
            if not shed_id:
                raise ValueError("shed_id must not be blank")
            if shed_id in seen_ids:
                raise ValueError(f"duplicate shed_id: {shed_id}")
            seen_ids.add(shed_id)

            try:
                heads = int(row["heads"])
            except (TypeError, ValueError) as exc:
                raise ValueError(f"heads must be an integer for shed_id {shed_id}") from exc
            if heads < 1:
                raise ValueError(f"heads must be positive for shed_id {shed_id}")

            drainage = (row["drains_to_reach"] or "").strip().lower()
            if drainage not in {"true", "false", "unknown"}:
                raise ValueError(
                    f"drains_to_reach must be true, false, or unknown for shed_id {shed_id}"
                )
            drains_to_reach = {"true": True, "false": False, "unknown": None}[drainage]
            sheds.append(
                Shed(
                    shed_id=shed_id,
                    barangay=row["barangay"],
                    heads=heads,
                    drains_to_reach=drains_to_reach,
                    source=row["source"],
                )
            )
    return tuple(sheds)


def eligible_sheds(sheds: Sequence[Shed]) -> tuple[Shed, ...]:
    return tuple(shed for shed in sheds if shed.drains_to_reach is True)


def apply_overrides(params: Params, overrides: Mapping[str, str]) -> Params:
    params_by_name = {field.name: field for field in fields(Params)}
    parameter_types = get_type_hints(Params)
    changed: dict[str, float | int | None] = {}
    for name, raw_value in overrides.items():
        if name not in params_by_name:
            raise ValueError(f"unknown parameter: {name}")
        current = getattr(params, name)
        text = raw_value.strip()
        if text.lower() == "none":
            if type(None) not in get_args(parameter_types[name]):
                raise ValueError(f"parameter {name} cannot be None")
            changed[name] = None
        elif isinstance(current, int) and not isinstance(current, bool):
            try:
                changed[name] = int(text)
            except ValueError as exc:
                raise ValueError(f"parameter {name} must be an integer") from exc
        else:
            try:
                changed[name] = float(text)
            except ValueError as exc:
                raise ValueError(f"parameter {name} must be a number or None") from exc
    return replace(params, **changed)


def parameter_register(params: Params) -> list[dict[str, object]]:
    parameter_names = {field.name for field in fields(Params)}
    metadata_names = set(PARAMETER_META)
    if parameter_names != metadata_names:
        missing = sorted(parameter_names - metadata_names)
        extra = sorted(metadata_names - parameter_names)
        raise ValueError(f"parameter metadata mismatch: missing={missing}, extra={extra}")

    rows: list[dict[str, object]] = []
    for field in fields(Params):
        metadata = PARAMETER_META[field.name]
        if set(metadata) != {"unit", "status", "source"}:
            raise ValueError(f"parameter metadata mismatch for {field.name}")
        rows.append(
            {
                "name": field.name,
                "value": getattr(params, field.name),
                "unit": metadata["unit"],
                "status": metadata["status"],
                "source": metadata["source"],
            }
        )
    return rows
