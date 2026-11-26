### Task 3: Process, Hydraulic, Transport, and Land Balances

**Files:**
- Create: `river_model/process.py`
- Create: `tests/test_process.py`

**Interfaces:**
- Consumes: `Params`, `Sequence[Shed]`.
- Produces: `ProcessResult`, `compute_process(params: Params, sheds: Sequence[Shed]) -> ProcessResult`.

- [ ] **Step 1: Write failing process tests**

Create `tests/test_process.py`:

```python
from dataclasses import replace

import pytest

from river_model.inputs import Params, Shed
from river_model.process import compute_process


def test_two_shed_hand_calculation():
    sheds = (
        Shed("S01", "Santiago", 10, True, "test"),
        Shed("S02", "Santiago", 12, True, "test"),
    )
    result = compute_process(Params(), sheds)
    assert result.heads == 22
    assert result.manure_kg_day == pytest.approx(44.0)
    assert result.wash_m3_day == pytest.approx(0.484)
    assert result.vs_in_kg_day == pytest.approx(7.04)
    assert result.vs_destroyed_kg_day == pytest.approx(3.52)
    assert result.biogas_m3_day > 0
    assert result.lpg_kg_day > 0


def test_vs_balance_closes():
    sheds = (Shed("S01", "Santiago", 20, True, "test"),)
    result = compute_process(Params(), sheds)
    assert result.vs_balance_error_pct <= 5.0


def test_trips_increase_with_slurry():
    small = (Shed("S01", "Santiago", 10, True, "test"),)
    large = (Shed("S01", "Santiago", 100, True, "test"),)
    assert compute_process(Params(), large).trips_week > compute_process(Params(), small).trips_week


def test_land_requirement_increases_with_heads():
    small = (Shed("S01", "Santiago", 10, True, "test"),)
    large = (Shed("S01", "Santiago", 100, True, "test"),)
    assert compute_process(Params(), large).land_ha_required > compute_process(Params(), small).land_ha_required


def test_unknown_drainage_is_excluded():
    sheds = (Shed("S01", "Santiago", 100, None, "test"),)
    result = compute_process(Params(), sheds)
    assert result.manure_kg_day == 0.0
    assert result.trips_week == 0.0
```

- [ ] **Step 2: Run tests and verify failure**

Run: `python -m pytest tests/test_process.py -v`

Expected: FAIL because `river_model.process` does not exist.

- [ ] **Step 3: Implement the process module**

Create `river_model/process.py`:

```python
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from river_model.inputs import Params, Shed, eligible_sheds


@dataclass(frozen=True)
class ProcessResult:
    heads: int
    manure_kg_day: float
    wash_m3_day: float
    slurry_m3_day: float
    dm_in_kg_day: float
    vs_in_kg_day: float
    vs_destroyed_kg_day: float
    vs_remaining_kg_day: float
    dm_remaining_kg_day: float
    vs_balance_error_pct: float
    ch4_m3_day: float
    biogas_m3_day: float
    lpg_kg_day: float
    nutrient_n_kg_day: float
    land_ha_required: float
    trips_week: float


def compute_process(params: Params, sheds: Sequence[Shed]) -> ProcessResult:
    active = eligible_sheds(sheds)
    heads = sum(s.heads for s in active)
    manure = heads * params.manure_kg_head_day
    wash = heads * params.washwater_l_head_day / 1000.0
    slurry = manure / 1000.0 + wash

    dm_in = manure * params.dm_frac
    vs_in = dm_in * params.vs_frac_dm
    vs_destroyed = vs_in * params.vs_destroyed
    vs_remaining = vs_in - vs_destroyed
    dm_remaining = dm_in - vs_destroyed

    balance_error = (
        abs(dm_in - (vs_destroyed + dm_remaining)) / dm_in * 100.0
        if dm_in > 0
        else 0.0
    )

    ch4 = vs_destroyed * params.ch4_yield
    biogas = ch4 / params.ch4_frac
    lpg = ch4 * params.ch4_mj_m3 / params.lpg_mj_kg

    nutrient_n = dm_remaining * params.n_frac_dm
    land_ha = nutrient_n * 365.0 / params.rice_n_kg_ha
    trips_week = slurry * 7.0 / params.tanker_m3

    return ProcessResult(
        heads=heads,
        manure_kg_day=manure,
        wash_m3_day=wash,
        slurry_m3_day=slurry,
        dm_in_kg_day=dm_in,
        vs_in_kg_day=vs_in,
        vs_destroyed_kg_day=vs_destroyed,
        vs_remaining_kg_day=vs_remaining,
        dm_remaining_kg_day=dm_remaining,
        vs_balance_error_pct=balance_error,
        ch4_m3_day=ch4,
        biogas_m3_day=biogas,
        lpg_kg_day=lpg,
        nutrient_n_kg_day=nutrient_n,
        land_ha_required=land_ha,
        trips_week=trips_week,
    )
```

- [ ] **Step 4: Run tests and verify pass**

Run: `python -m pytest tests/test_process.py -v`

Expected: 5 tests PASS.

---

