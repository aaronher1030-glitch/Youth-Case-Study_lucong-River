### Task 2: River Load, Capture Chain, and Source Reconciliation

**Files:**
- Create: `river_model/load.py`
- Create: `tests/test_load.py`

**Interfaces:**
- Consumes: `Params`, `Sequence[Shed]`.
- Produces: `LoadResult`, `compute_load(params: Params, sheds: Sequence[Shed]) -> LoadResult`.

- [ ] **Step 1: Write failing load tests**

Create `tests/test_load.py`:

```python
from dataclasses import replace
from pathlib import Path

import pytest

from river_model.inputs import Params, Shed, eligible_sheds, load_census
from river_model.load import compute_load

FIXTURE = Path(__file__).parent / "fixtures" / "census.csv"


def test_unit_conversion_matches_hand_calculation():
    sheds = (Shed("S01", "Santiago", 225, True, "test"),)
    result = compute_load(replace(Params(), eta=1.0), sheds)
    assert result.l0_mpn_day == pytest.approx(691_200_000_000.0)
    assert result.l_gen_mpn_day == pytest.approx(225_000_000_000.0)


def test_zero_enrollment_returns_baseline():
    sheds = (Shed("S01", "Santiago", 10, True, "test"),)
    result = compute_load(replace(Params(), p_enroll=0.0), sheds)
    assert result.c == 0.0
    assert result.c_end_mpn_100ml == result.c0_mpn_100ml


def test_no_confirmed_sheds_means_no_reduction():
    sheds = (Shed("S01", "Santiago", 10, None, "test"),)
    result = compute_load(Params(), sheds)
    assert result.r == 0.0
    assert result.annual_mpn_prevented_12 == 0.0


def test_capture_monotonicity():
    sheds = (Shed("S01", "Santiago", 225, True, "test"),)
    low = compute_load(replace(Params(), p_collect=0.80), sheds)
    high = compute_load(replace(Params(), p_collect=0.95), sheds)
    assert high.c_end_mpn_100ml < low.c_end_mpn_100ml


def test_source_share_above_one_raises_instead_of_capping():
    sheds = (Shed("S01", "Santiago", 1000, True, "test"),)
    with pytest.raises(ValueError, match="source share exceeds 1"):
        compute_load(Params(), sheds)


def test_threshold_identity_for_8000():
    sheds = (Shed("S01", "Santiago", 225, True, "test"),)
    result = compute_load(replace(Params(), q_m3_s=0.02), sheds)
    assert result.c_end_mpn_100ml == pytest.approx(
        result.c0_mpn_100ml * (1 - result.r * result.c)
    )
    assert result.reduction_fraction == pytest.approx(result.r * result.c)


def test_unknown_drainage_is_excluded():
    sheds = load_census(FIXTURE)
    result = compute_load(Params(), sheds)
    assert result.heads == 22
```

- [ ] **Step 2: Run tests and verify failure**

Run: `python -m pytest tests/test_load.py -v`

Expected: FAIL because `river_model.load` does not exist.

- [ ] **Step 3: Implement the load module**

Create `river_model/load.py`:

```python
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence

from river_model.inputs import Params, Shed, eligible_sheds


@dataclass(frozen=True)
class LoadResult:
    heads: int
    l_gen_mpn_day: float
    l0_mpn_day: float
    l_target_mpn_day: float
    r: float
    c: float
    c0_mpn_100ml: float
    c_end_mpn_100ml: float
    reduction_fraction: float
    annual_mpn_prevented_12: float
    reconciliation_ok: bool
    top_down_r: float | None


def compute_load(params: Params, sheds: Sequence[Shed]) -> LoadResult:
    active = eligible_sheds(sheds)
    heads = sum(s.heads for s in active)
    l_gen = heads * params.e_head_day
    l0 = params.c0_mpn_100ml * params.q_m3_s * 86_400 * 10_000
    l_target = params.eta * l_gen
    r = l_target / l0

    if r > 1.0 + 1e-9:
        raise ValueError(
            f"source share exceeds 1: r={r:.6f}; revise source or flow inputs"
        )
    r = max(0.0, r)

    c = params.p_enroll * params.p_collect * params.p_retain
    reduction = r * c
    c_end = params.c0_mpn_100ml * (1 - reduction)

    top_down_r = None
    reconciliation_ok = True
    if params.upstream_mpn_100ml is not None:
        top_down_r = max(
            0.0,
            (params.c0_mpn_100ml - params.upstream_mpn_100ml)
            / params.c0_mpn_100ml,
        )
        reconciliation_ok = abs(r - top_down_r) <= params.source_share_tolerance

    annual_mpn_prevented_12 = reduction * l0 * 365 / 1.0e12
    return LoadResult(
        heads=heads,
        l_gen_mpn_day=l_gen,
        l0_mpn_day=l0,
        l_target_mpn_day=l_target,
        r=r,
        c=c,
        c0_mpn_100ml=params.c0_mpn_100ml,
        c_end_mpn_100ml=c_end,
        reduction_fraction=reduction,
        annual_mpn_prevented_12=annual_mpn_prevented_12,
        reconciliation_ok=reconciliation_ok,
        top_down_r=top_down_r,
    )
```

- [ ] **Step 4: Run tests and verify pass**

Run: `python -m pytest tests/test_load.py -v`

Expected: 7 tests PASS.

- [ ] **Step 5: Verify the key threshold numerically**

Run: `python -c "from river_model.inputs import Params; from river_model.load import compute_load; from dataclasses import replace; from river_model.inputs import Shed; r=compute_load(replace(Params(), q_m3_s=0.02), [Shed('S','S',225,True,'test')]); print(r.r, r.c, r.c_end_mpn_100ml)"`

Expected: `r * c >= 0.5` and `c_end <= 8000` for the low-flow test case.

---

