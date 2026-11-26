### Task 5: Transparent Design Enumeration and Hard Constraints

**Files:**
- Create: `river_model/design.py`
- Create: `tests/test_design.py`

**Interfaces:**
- Consumes: `Params`, `Sequence[Shed]`, outputs from Tasks 2–4.
- Produces: `Design`, `DesignEvaluation`, `Alternative`, `AlternativeEvaluation`, `enumerate_designs(params: Params, sheds: Sequence[Shed]) -> list[DesignEvaluation]`, `constraint_feasible(evaluation: DesignEvaluation) -> bool`, `evaluate_alternatives(params: Params) -> list[AlternativeEvaluation]`.

- [ ] **Step 1: Write failing design tests**

Create `tests/test_design.py`:

```python
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
```

- [ ] **Step 2: Run tests and verify failure**

Run: `python -m pytest tests/test_design.py -v`

Expected: FAIL because `river_model.design` does not exist.

- [ ] **Step 3: Implement the design module**

Create `river_model/design.py` with these dataclasses:

```python
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
```

Implement `enumerate_designs` with this exact search logic:

1. Sort confirmed eligible sheds by `shed_id`.
2. Build the sorted unique list of barangays represented by confirmed eligible sheds.
3. For every non-empty combination of those barangays:
   - Select every confirmed eligible shed whose barangay is in the combination.
   - Compute load and process results.
   - Set `carts = ceil(len(subset) / 8)`.
   - For `collection_days_week` in `(1, 2)`:
     - `min_modules = max(1, ceil(slurry_m3_day * hrt_min_days / module_m3))`.
     - `min_tankers = max(1, ceil(trips_week / (collection_days_week * trips_day_cap * utilization)))`.
     - Enumerate modules from `min_modules` through `min_modules + max_extra_modules`.
     - Enumerate tankers from `min_tankers` through `min_tankers + max_extra_tankers`.
     - Compute costs with `vs_diverted_year = vs_in_kg_day * p_enroll * p_collect * p_retain * 365` and `annual_mpn_prevented_12 = load.annual_mpn_prevented_12`.
4. Populate checks with keys exactly: `duration`, `budget`, `focus_stream`, `digester`, `tanker`, `land`, `load_reconciliation`, `mass_balance`.
5. Add rejection text exactly: `pilot exceeds 12 months`, `cash requirement exceeds budget`, `focus-stream share below 70%`, `digester retention too short`, `tanker capacity insufficient`, `land evidence missing`, `land requirement exceeds available area`, `source loads do not reconcile`, `mass balance error exceeds 5%`.
6. Sort evaluations by `(costs.eac, costs.cash_12m, -len(design.shed_ids))`.

This yields at most three service sets for Santiago/Alfonso and avoids exponential enumeration over individual synthetic sheds.

The target concentration is deliberately absent from deterministic checks; Task 6 applies the probability threshold.

- [ ] **Step 4: Run tests and verify pass**

Run: `python -m pytest tests/test_design.py -v`

Expected: 6 tests PASS.

- [ ] **Step 5: Inspect one candidate by hand**

Run: `python -c "from pathlib import Path; from dataclasses import replace; from river_model.inputs import Params,load_census; from river_model.design import enumerate_designs,constraint_feasible; p=replace(Params(),land_available_ha=20.0); rows=enumerate_designs(p,load_census(Path('tests/fixtures/census.csv'))); print(len(rows), sum(constraint_feasible(r) for r in rows)); print(rows[0].design, rows[0].costs.eac)"`

Expected: a positive evaluation count, a non-negative feasible count, and a finite annualized cost.

- [ ] **Step 6: Add failing alternative-comparison tests**

Append to `tests/test_design.py`:

```python
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
```

- [ ] **Step 7: Run alternative tests and verify failure**

Run: `python -m pytest tests/test_design.py -v`

Expected: the two new tests FAIL because `evaluate_alternatives` does not exist.

- [ ] **Step 8: Implement alternative comparison**

Add these dataclasses to `river_model/design.py`:

```python
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
```

Implement `evaluate_alternatives(params)` with exactly three alternatives:

1. `Do nothing / enforcement only`: source share and capture are 0 in all scenarios; CAPEX and OPEX are 0; legal text is `No new permit; enforcement-only precedent failed`; measurable within 12 months is `True`; note is `Counterfactual: river condition remains at baseline unless external conditions change.`
2. `Household septage service`: source-share low/mode/high = 0.10/0.30/0.50; capture low/mode/high = 0.50/0.70/0.90; all cost fields are `None`; legal text is `Requires LGU septage program and disposal permits`; measurable is `True`; note is `Source share and costs are unresolved assumptions; do not rank this option as cheaper until quoted.`
3. `In-stream screen and dredge`: source-share low/mode/high = 0.00/0.00/0.10; capture low/mode/high = 0.00/0.00/0.10; all cost fields are `None`; legal text is `Easement and disposal permits unresolved`; measurable is `False`; note is `No evidence that screening reduces fecal coliform; dredging may resuspend solids.`

For each alternative calculate:

\[
C_{end}=C_0(1-r_jc_j)
\]

for low/mode/high and calculate mode annual station-equivalent MPN prevented with the same `L0` conversion as Task 2. When mode CAPEX and OPEX are present, calculate 12-month cash and lifecycle EAC with the same discount and contingency rules as Task 4; otherwise return `None` and `cost_status="missing"`. Do-nothing costs return 0 and `cost_status="sourced"` because they are the defined counterfactual.

- [ ] **Step 9: Run all design tests and verify pass**

Run: `python -m pytest tests/test_design.py -v`

Expected: 8 tests PASS.

---

