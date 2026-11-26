import math
from dataclasses import replace
from pathlib import Path

import pytest

from river_model import design as design_module
from river_model.design import (
    constraint_feasible,
    enumerate_designs,
    evaluate_alternatives,
)
from river_model.inputs import Params, Shed, load_census

FIXTURE = Path(__file__).parent / "fixtures" / "census.csv"
EXPECTED_CHECK_KEYS = (
    "duration",
    "budget",
    "focus_stream",
    "digester",
    "tanker",
    "land",
    "load_reconciliation",
    "mass_balance",
)
THREE_SHEDS = (
    Shed("S01", "Santiago", 10, True, "test"),
    Shed("S02", "Santiago", 12, True, "test"),
    Shed("S03", "Alfonso", 8, True, "test"),
)


def test_fixture_enumeration_has_exact_count_and_check_keys():
    params = replace(Params(), land_available_ha=20.0)
    rows = enumerate_designs(params, load_census(FIXTURE))
    assert len(rows) == 18
    assert all(row.design.shed_ids for row in rows)
    assert all(set(row.checks) == set(EXPECTED_CHECK_KEYS) for row in rows)


def test_three_sheds_use_exact_barangay_service_sets_and_default_count():
    rows = enumerate_designs(replace(Params(), land_available_ha=20.0), THREE_SHEDS)
    assert len(rows) == 54
    service_sets = {frozenset(row.design.shed_ids) for row in rows}
    assert service_sets == {
        frozenset({"S01", "S02"}),
        frozenset({"S03"}),
        frozenset({"S01", "S02", "S03"}),
    }


def test_single_extra_module_and_tanker_cover_each_inclusive_range():
    params = replace(
        Params(),
        land_available_ha=20.0,
        max_extra_modules=1,
        max_extra_tankers=1,
    )
    rows = enumerate_designs(params, THREE_SHEDS)
    assert len(rows) == 24
    service_sets = {frozenset(row.design.shed_ids) for row in rows}
    for service_set in service_sets:
        service_rows = [
            row for row in rows if frozenset(row.design.shed_ids) == service_set
        ]
        assert len(service_rows) == 8
        for collection_days in (1, 2):
            day_rows = [
                row
                for row in service_rows
                if row.design.collection_days_week == collection_days
            ]
            assert len(day_rows) == 4
            modules = sorted({row.design.modules for row in day_rows})
            tankers = sorted({row.design.tankers for row in day_rows})
            assert modules == list(range(modules[0], modules[0] + 2))
            assert tankers == list(range(tankers[0], tankers[0] + 2))
            assert len(
                {(row.design.modules, row.design.tankers) for row in day_rows}
            ) == 4


def test_nine_sheds_in_one_barangay_require_two_carts():
    sheds = tuple(
        Shed(f"S{index:02d}", "Santiago", 1, True, "test")
        for index in range(1, 10)
    )
    rows = enumerate_designs(replace(Params(), land_available_ha=20.0), sheds)
    assert rows
    assert all(row.design.carts == 2 for row in rows)
    assert all(len(row.design.shed_ids) == 9 for row in rows)


def test_false_and_unknown_drainage_are_excluded_from_service_sets():
    sheds = (
        Shed("S01", "Santiago", 10, True, "test"),
        Shed("S02", "Santiago", 100, False, "test"),
        Shed("S03", "Alfonso", 100, None, "test"),
    )
    rows = enumerate_designs(replace(Params(), land_available_ha=20.0), sheds)
    assert rows
    assert {row.design.shed_ids for row in rows} == {("S01",)}


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


def test_costing_receives_diverted_vs_and_annual_mpn_inputs():
    params = replace(
        Params(),
        land_available_ha=20.0,
        max_extra_modules=0,
        max_extra_tankers=0,
    )
    row = enumerate_designs(params, load_census(FIXTURE))[0]
    assert row.design.shed_ids == ("S01", "S02")
    expected_vs_diverted_year = 7.04 * 0.95 * 0.95 * 0.95 * 365
    expected_annual_mpn12 = 22 * 1.0e9 * 0.95 * 0.95 * 0.95 * 365 / 1.0e12
    assert row.costs.php_per_vs_kg == pytest.approx(
        row.costs.eac / expected_vs_diverted_year
    )
    assert row.costs.php_per_mpn12 == pytest.approx(
        row.costs.eac / expected_annual_mpn12
    )


@pytest.mark.parametrize(
    ("field", "value", "failed_check", "reason"),
    (
        (
            "focus_stream_share",
            0.69,
            "focus_stream",
            "focus-stream share below 70%",
        ),
        (
            "land_available_ha",
            0.0,
            "land",
            "land requirement exceeds available area",
        ),
        (
            "upstream_mpn_100ml",
            8_000.0,
            "load_reconciliation",
            "source loads do not reconcile",
        ),
        ("budget", 0.0, "budget", "cash requirement exceeds budget"),
    ),
)
def test_failed_constraints_record_rejection_reasons(
    field, value, failed_check, reason
):
    overrides = {"land_available_ha": 20.0, field: value}
    params = replace(Params(), **overrides)
    rows = enumerate_designs(params, load_census(FIXTURE))
    assert rows
    assert all(not row.checks[failed_check] for row in rows)
    assert all(reason in row.rejection_reasons for row in rows)


def test_rows_are_sorted_by_eac_cash_and_descending_shed_count():
    rows = enumerate_designs(
        replace(Params(), land_available_ha=20.0), THREE_SHEDS
    )
    keys = [
        (row.costs.eac, row.costs.cash_12m, -len(row.design.shed_ids))
        for row in rows
    ]
    assert keys == sorted(keys)


def test_zero_enrollment_keeps_costs_finite_and_unit_costs_infinite():
    params = replace(Params(), land_available_ha=20.0, p_enroll=0.0)
    rows = enumerate_designs(params, load_census(FIXTURE))
    assert rows
    for row in rows:
        assert math.isfinite(row.costs.eac)
        assert math.isfinite(row.costs.cash_12m)
        assert row.costs.php_per_mpn12 == float("inf")
        assert row.costs.php_per_vs_kg == float("inf")


@pytest.mark.parametrize("failed_check", EXPECTED_CHECK_KEYS)
def test_any_failed_check_makes_an_evaluation_infeasible(failed_check):
    row = enumerate_designs(
        replace(Params(), land_available_ha=20.0), load_census(FIXTURE)
    )[0]
    checks = {**row.checks, failed_check: False}
    assert not constraint_feasible(replace(row, checks=checks))


def test_rejection_reason_alone_makes_an_evaluation_infeasible():
    row = enumerate_designs(
        replace(Params(), land_available_ha=20.0), load_census(FIXTURE)
    )[0]
    checks = {key: True for key in EXPECTED_CHECK_KEYS}
    assert not constraint_feasible(
        replace(row, checks=checks, rejection_reasons=("defensive rejection",))
    )


def test_passing_checks_without_rejections_make_an_evaluation_feasible():
    row = enumerate_designs(
        replace(Params(), land_available_ha=20.0), load_census(FIXTURE)
    )[0]
    checks = {key: True for key in EXPECTED_CHECK_KEYS}
    assert constraint_feasible(replace(row, checks=checks, rejection_reasons=()))


@pytest.mark.parametrize(
    ("value", "message"),
    (
        (0, "pilot_months must be an integer from 1 through 12"),
        (-1, "pilot_months must be an integer from 1 through 12"),
        (1.5, "pilot_months must be a finite integer"),
        (math.nan, "pilot_months must be a finite integer"),
        (math.inf, "pilot_months must be a finite integer"),
        (True, "pilot_months must be a finite integer"),
        (False, "pilot_months must be a finite integer"),
        ("12", "pilot_months must be a finite integer"),
        (None, "pilot_months must be a finite integer"),
    ),
)
def test_invalid_pilot_months_fail_before_costing(monkeypatch, value, message):
    def unexpected_costing(*args, **kwargs):
        pytest.fail("compute_costs must not run for an invalid pilot duration")

    monkeypatch.setattr(design_module, "compute_costs", unexpected_costing)
    params = replace(Params(), pilot_months=value)
    with pytest.raises(ValueError, match=f"^{message}$"):
        enumerate_designs(params, load_census(FIXTURE))


@pytest.mark.parametrize("pilot_months", (1, 12))
def test_pilot_month_boundaries_return_evaluations(pilot_months):
    params = replace(
        Params(), land_available_ha=20.0, pilot_months=pilot_months
    )
    rows = enumerate_designs(params, load_census(FIXTURE))
    assert rows
    assert all(row.checks["duration"] for row in rows)


def test_pilot_over_twelve_months_fails_before_costing(monkeypatch):
    def unexpected_costing(*args, **kwargs):
        pytest.fail("compute_costs must not run for an overlong pilot")

    monkeypatch.setattr(design_module, "compute_costs", unexpected_costing)
    params = replace(Params(), pilot_months=13)
    with pytest.raises(ValueError, match="^pilot exceeds 12 months$"):
        enumerate_designs(params, load_census(FIXTURE))


def test_physically_invalid_service_subset_raises_instead_of_being_dropped():
    sheds = (
        Shed("S01", "Santiago", 10, True, "test"),
        Shed("S99", "Zulu", 1_000_000, True, "test"),
    )
    with pytest.raises(ValueError, match="source share exceeds 1"):
        enumerate_designs(replace(Params(), land_available_ha=20.0), sheds)


def test_target_is_not_a_deterministic_constraint():
    params = replace(Params(), land_available_ha=20.0, target_mpn_100ml=1.0)
    rows = enumerate_designs(params, load_census(FIXTURE))
    assert any(constraint_feasible(row) for row in rows)
    assert all("target" not in row.checks for row in rows)


def test_alternatives_use_same_station_functional_unit():
    rows = evaluate_alternatives(Params())
    assert [row.name for row in rows] == [
        "Do nothing / enforcement only",
        "Household septage service",
        "In-stream screen and dredge",
    ]
    assert rows[0].c_end_mode_mpn_100ml == 16_000.0
    assert rows[0].annual_mpn_prevented_12_mode == 0.0
    assert rows[0].cash_12m_mode == 0.0
    assert rows[0].eac_mode == 0.0
    assert rows[0].cost_status == "sourced"
    assert rows[1].c_end_mode_mpn_100ml < 16_000.0


def test_household_alternative_has_exact_concentration_and_prevention_bounds():
    household = evaluate_alternatives(Params())[1]
    assert (
        household.c_end_low_mpn_100ml,
        household.c_end_mode_mpn_100ml,
        household.c_end_high_mpn_100ml,
    ) == (8_800.0, 12_640.0, 15_200.0)
    assert household.annual_mpn_prevented_12_mode == 52.98048


def test_unquoted_alternative_costs_remain_missing():
    rows = evaluate_alternatives(Params())
    assert rows[1].cash_12m_mode is None
    assert rows[1].eac_mode is None
    assert rows[1].cost_status == "missing"
    assert rows[2].cost_status == "missing"


def _assert_invalid_alternative_parameter(field, value):
    with pytest.raises(ValueError, match=rf"\b{field}\b"):
        evaluate_alternatives(replace(Params(), **{field: value}))


@pytest.mark.parametrize("field", ("c0_mpn_100ml", "q_m3_s"))
@pytest.mark.parametrize(
    "value",
    (0.0, -1.0, math.nan, math.inf, -math.inf, True, False, "invalid", None),
)
def test_positive_alternative_physical_inputs_reject_invalid_values(field, value):
    _assert_invalid_alternative_parameter(field, value)


@pytest.mark.parametrize(
    "value", (-1.0, math.nan, math.inf, -math.inf, True, False, "invalid", None)
)
def test_alternative_discount_rejects_invalid_values(value):
    _assert_invalid_alternative_parameter("discount", value)


@pytest.mark.parametrize(
    "value",
    (0, -1, 1.5, math.nan, math.inf, -math.inf, True, False, "invalid", None),
)
def test_alternative_asset_life_rejects_invalid_values(value):
    _assert_invalid_alternative_parameter("asset_life", value)


@pytest.mark.parametrize(
    "value",
    (0, -1, 11, 1.5, math.nan, math.inf, -math.inf, True, False, "invalid", None),
)
def test_alternative_replacement_year_rejects_invalid_values(value):
    _assert_invalid_alternative_parameter("replacement_year", value)


@pytest.mark.parametrize("field", ("contingency_rate", "replacement_capex_frac"))
@pytest.mark.parametrize(
    "value",
    (-0.01, 1.01, math.nan, math.inf, -math.inf, True, False, "invalid", None),
)
def test_alternative_fractions_reject_invalid_values(field, value):
    _assert_invalid_alternative_parameter(field, value)
