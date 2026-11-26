from dataclasses import replace

import pytest

from river_model.economics import CostInputs, compute_costs
from river_model.inputs import Params


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
    inputs = CostInputs(15, 225, 3, 1, 2, 20.0, 10_000.0, 5.0)
    result = compute_costs(Params(), inputs)
    assert result.cash_12m == pytest.approx(
        (result.capex + result.opex_12m) * 1.10
    )


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
