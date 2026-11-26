import math
from dataclasses import replace

import pytest

from river_model.economics import CostInputs, compute_costs
from river_model.inputs import Params


BASE_INPUTS = CostInputs(15, 225, 3, 1, 2, 20.0, 10_000.0, 5.0)
CAPEX_PARAMETERS = (
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
)
OPEX_PARAMETERS = (
    "opex_staff_year",
    "opex_sampling_year",
    "opex_maint_frac",
    "opex_trip",
    "opex_admin_year",
)
FRACTION_PARAMETERS = (
    "contingency_rate",
    "opex_maint_frac",
    "replacement_capex_frac",
)


def _assert_invalid_input(field, value):
    with pytest.raises(ValueError, match=rf"\b{field}\b"):
        compute_costs(Params(), replace(BASE_INPUTS, **{field: value}))


def _assert_invalid_parameter(field, value):
    with pytest.raises(ValueError, match=rf"\b{field}\b"):
        compute_costs(replace(Params(), **{field: value}), BASE_INPUTS)


def test_capex_line_items_match_hand_calculation():
    inputs = CostInputs(
        sheds=15,
        heads=225,
        modules=3,
        tankers=1,
        carts=2,
        trips_week=20.0,
        vs_diverted_year=10_000.0,
        annual_mpn_prevented_12=5.0,
    )
    result = compute_costs(Params(), inputs)
    expected_capex = (
        3 * 380_000
        + 1_450_000
        + 2 * 180_000
        + 980_000
        + 3 * 45_000
        + 420_000
        + 180_000
        + 320_000
        + 155_000
        + 700_000
        + 600_000
    )
    assert result.capex == pytest.approx(expected_capex)


def test_cash_includes_contingency():
    result = compute_costs(Params(), BASE_INPUTS)
    assert result.opex_12m == 2_730_000.0
    assert result.contingency == 917_000.0
    assert result.cash_12m == 10_087_000.0


def test_zero_discount_uses_straight_line_annualization():
    inputs = CostInputs(15, 225, 3, 1, 2, 20.0, 10_000.0, 5.0)
    result = compute_costs(replace(Params(), discount=0.0), inputs)
    assert result.eac == pytest.approx(result.npc / Params().asset_life)


def test_zero_load_prevented_returns_infinite_unit_cost():
    inputs = CostInputs(15, 225, 3, 1, 2, 20.0, 10_000.0, 0.0)
    result = compute_costs(Params(), inputs)
    assert result.php_per_mpn12 == float("inf")


def test_base_case_has_zero_revenue_credit():
    inputs = CostInputs(15, 225, 3, 1, 2, 20.0, 10_000.0, 5.0)
    result = compute_costs(Params(), inputs)
    assert result.revenue_credit == 0.0


def test_default_lifecycle_matches_literal_values():
    result = compute_costs(Params(), BASE_INPUTS)
    assert result.npc == pytest.approx(26_771_261.166334495, rel=1e-12)
    assert result.eac == pytest.approx(3_989_707.363394699, rel=1e-12)


def test_default_replacement_is_discounted_from_its_scheduled_year():
    params = Params()
    result = compute_costs(params, BASE_INPUTS)
    without_replacement = compute_costs(
        replace(params, replacement_capex_frac=0.0), BASE_INPUTS
    )
    assert result.npc - without_replacement.npc == pytest.approx(
        1_610_000 / 1.08**5, rel=1e-12
    )


def test_default_positive_unit_costs_match_literal_values():
    result = compute_costs(Params(), BASE_INPUTS)
    assert result.php_per_shed_month == pytest.approx(
        22_165.040907748327, rel=1e-12
    )
    assert result.php_per_mpn12 == pytest.approx(797_941.4726789398, rel=1e-12)
    assert result.php_per_vs_kg == pytest.approx(398.9707363394699, rel=1e-12)
    assert result.fee_per_head_month == pytest.approx(
        1_477.6693938498886, rel=1e-12
    )


def test_zero_vs_diversion_returns_infinite_unit_cost():
    inputs = replace(BASE_INPUTS, vs_diverted_year=0.0)
    result = compute_costs(Params(), inputs)
    assert result.php_per_vs_kg == float("inf")


def test_tiny_positive_discount_uses_stable_annualization():
    params = replace(Params(), discount=1e-16)
    result = compute_costs(params, BASE_INPUTS)
    assert math.isfinite(result.eac)
    assert result.eac == pytest.approx(
        result.npc / params.asset_life, rel=1e-12, abs=1e-9
    )


@pytest.mark.parametrize(
    ("tankers", "carts", "expected_capex"),
    ((1, 2, 6_440_000.0), (2, 2, 7_890_000.0), (1, 3, 6_620_000.0)),
)
def test_tanker_and_cart_counts_have_independent_capex_multipliers(
    tankers, carts, expected_capex
):
    inputs = replace(BASE_INPUTS, tankers=tankers, carts=carts)
    result = compute_costs(Params(), inputs)
    assert result.capex == expected_capex


@pytest.mark.parametrize("field", ("sheds", "heads"))
@pytest.mark.parametrize(
    "value",
    (0, -1, 1.5, math.inf, -math.inf, math.nan, True, False, "15", None),
)
def test_positive_integer_inputs_reject_invalid_boundaries(field, value):
    _assert_invalid_input(field, value)


@pytest.mark.parametrize("field", ("modules", "tankers", "carts"))
@pytest.mark.parametrize(
    "value",
    (-1, 1.5, math.inf, -math.inf, math.nan, True, False, "3", None),
)
def test_nonnegative_integer_inputs_reject_invalid_boundaries(field, value):
    _assert_invalid_input(field, value)


@pytest.mark.parametrize(
    "field", ("trips_week", "vs_diverted_year", "annual_mpn_prevented_12")
)
@pytest.mark.parametrize(
    "value", (-1.0, math.inf, -math.inf, math.nan, True, False, "1", None)
)
def test_nonnegative_numeric_inputs_reject_invalid_boundaries(field, value):
    _assert_invalid_input(field, value)


@pytest.mark.parametrize("field", CAPEX_PARAMETERS + OPEX_PARAMETERS)
@pytest.mark.parametrize(
    "value", (-1.0, math.inf, -math.inf, math.nan, True, False, "1", None)
)
def test_economic_cost_parameters_reject_invalid_values(field, value):
    _assert_invalid_parameter(field, value)


@pytest.mark.parametrize("field", FRACTION_PARAMETERS)
@pytest.mark.parametrize(
    "value",
    (-0.01, 1.01, math.inf, -math.inf, math.nan, True, False, "0.5", None),
)
def test_fraction_parameters_reject_values_outside_zero_to_one(field, value):
    _assert_invalid_parameter(field, value)


@pytest.mark.parametrize(
    "value", (-1.0, math.inf, -math.inf, math.nan, True, False, "0.08", None)
)
def test_discount_rejects_invalid_values(value):
    _assert_invalid_parameter("discount", value)


@pytest.mark.parametrize(
    "value", (0, -1, 1.5, math.inf, -math.inf, math.nan, True, False, "10", None)
)
def test_asset_life_rejects_invalid_values(value):
    _assert_invalid_parameter("asset_life", value)


@pytest.mark.parametrize(
    "value", (0, -1, 11, 1.5, math.inf, -math.inf, math.nan, True, False, "5", None)
)
def test_replacement_year_rejects_values_outside_asset_life(value):
    _assert_invalid_parameter("replacement_year", value)


@pytest.mark.parametrize(
    "value", (0, -1, 13, 1.5, math.inf, -math.inf, math.nan, True, False, "12", None)
)
def test_pilot_months_rejects_values_outside_one_through_twelve(value):
    _assert_invalid_parameter("pilot_months", value)


def test_zero_optional_counts_trips_and_benefits_are_valid():
    inputs = replace(
        BASE_INPUTS,
        modules=0,
        tankers=0,
        carts=0,
        trips_week=0.0,
        vs_diverted_year=0.0,
        annual_mpn_prevented_12=0.0,
    )
    result = compute_costs(Params(), inputs)
    assert result.capex == 3_355_000.0
    assert math.isfinite(result.npc)
    assert math.isfinite(result.eac)
    assert result.php_per_mpn12 == float("inf")
    assert result.php_per_vs_kg == float("inf")


@pytest.mark.parametrize("rate", (0.0, 1.0))
def test_fraction_parameter_endpoints_are_valid(rate):
    params = replace(
        Params(),
        contingency_rate=rate,
        opex_maint_frac=rate,
        replacement_capex_frac=rate,
    )
    result = compute_costs(params, BASE_INPUTS)
    assert math.isfinite(result.npc)
    assert math.isfinite(result.eac)


@pytest.mark.parametrize(
    ("asset_life", "replacement_year", "pilot_months"),
    ((1, 1, 1), (10, 1, 12), (10, 10, 12)),
)
def test_lifecycle_and_pilot_boundaries_are_valid(
    asset_life, replacement_year, pilot_months
):
    params = replace(
        Params(),
        asset_life=asset_life,
        replacement_year=replacement_year,
        pilot_months=pilot_months,
    )
    result = compute_costs(params, BASE_INPUTS)
    assert math.isfinite(result.npc)
    assert math.isfinite(result.eac)
