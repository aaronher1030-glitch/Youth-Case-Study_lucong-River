### Task 4: Twelve-Month Cash, Lifecycle Cost, and Unit Economics

**Files:**
- Create: `river_model/economics.py`
- Create: `tests/test_economics.py`

**Interfaces:**
- Consumes: `Params`, `CostInputs`.
- Produces: `CostInputs`, `CostResult`, `compute_costs(params: Params, inputs: CostInputs) -> CostResult`.

- [ ] **Step 1: Write failing economic tests**

Create `tests/test_economics.py`:

```python
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
```

- [ ] **Step 2: Run tests and verify failure**

Run: `python -m pytest tests/test_economics.py -v`

Expected: FAIL because `river_model.economics` does not exist.

- [ ] **Step 3: Implement the economic module**

Create `river_model/economics.py`:

```python
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
```

- [ ] **Step 4: Run tests and verify pass**

Run: `python -m pytest tests/test_economics.py -v`

Expected: 5 tests PASS.

---

