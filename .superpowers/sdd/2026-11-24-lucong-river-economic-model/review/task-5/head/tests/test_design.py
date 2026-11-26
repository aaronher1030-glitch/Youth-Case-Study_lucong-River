from dataclasses import replace
from pathlib import Path

import pytest

from river_model.design import constraint_feasible, enumerate_designs
from river_model.inputs import Params, load_census

FIXTURE = Path(__file__).parent / "fixtures" / "census.csv"


def test_enumeration_returns_evaluations_and_counts_shed_subsets():
    params = replace(Params(), land_available_ha=20.0)
    sheds = load_census(FIXTURE)
    rows = enumerate_designs(params, sheds)
    assert rows
    assert all(row.design.shed_ids for row in rows)
    assert all(len(row.design.shed_ids) <= 2 for row in rows)


def test_enumeration_uses_barangay_service_sets():
    from river_model.inputs import Shed

    sheds = (
        Shed("S01", "Santiago", 10, True, "test"),
        Shed("S02", "Santiago", 12, True, "test"),
        Shed("S03", "Alfonso", 8, True, "test"),
    )
    rows = enumerate_designs(replace(Params(), land_available_ha=20.0), sheds)
    service_sets = {frozenset(row.design.shed_ids) for row in rows}
    assert service_sets == {
        frozenset({"S01", "S02"}),
        frozenset({"S03"}),
        frozenset({"S01", "S02", "S03"}),
    }


def test_missing_land_rejects_every_design():
    sheds = load_census(FIXTURE)
    rows = enumerate_designs(Params(), sheds)
    assert rows
    assert not any(constraint_feasible(row) for row in rows)
    assert all("land evidence missing" in row.rejection_reasons for row in rows)


def test_budget_constraint_is_never_violated_by_feasible_design():
    params = replace(Params(), land_available_ha=20.0)
    rows = enumerate_designs(params, load_census(FIXTURE))
    for row in rows:
        if constraint_feasible(row):
            assert row.costs.cash_12m <= params.budget
            assert row.checks["budget"]


def test_digester_and_tanker_constraints_match_formulas():
    params = replace(Params(), land_available_ha=20.0)
    rows = enumerate_designs(params, load_census(FIXTURE))
    for row in rows:
        expected_hrt_ok = (
            row.design.modules * params.module_m3
            >= row.process.slurry_m3_day * params.hrt_min_days
        )
        expected_trips_ok = (
            row.process.trips_week
            <= row.design.tankers
            * row.design.collection_days_week
            * params.trips_day_cap
            * params.utilization
        )
        assert row.checks["digester"] == expected_hrt_ok
        assert row.checks["tanker"] == expected_trips_ok


def test_target_is_not_a_deterministic_constraint():
    params = replace(Params(), land_available_ha=20.0, target_mpn_100ml=1.0)
    rows = enumerate_designs(params, load_census(FIXTURE))
    assert any(constraint_feasible(row) for row in rows)
    assert all("target" not in row.checks for row in rows)


from river_model.design import evaluate_alternatives


def test_alternatives_use_same_station_functional_unit():
    rows = evaluate_alternatives(Params())
    assert [row.name for row in rows] == [
        "Do nothing / enforcement only",
        "Household septage service",
        "In-stream screen and dredge",
    ]
    assert rows[0].c_end_mode_mpn_100ml == 16_000.0
    assert rows[0].annual_mpn_prevented_12_mode == 0.0
    assert rows[1].c_end_mode_mpn_100ml < 16_000.0


def test_unquoted_alternative_costs_remain_missing():
    rows = evaluate_alternatives(Params())
    assert rows[1].cash_12m_mode is None
    assert rows[1].eac_mode is None
    assert rows[1].cost_status == "missing"
    assert rows[2].cost_status == "missing"
