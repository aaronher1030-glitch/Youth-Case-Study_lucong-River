# Lucong River Economic Model and Viewer Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build an auditable Python model that selects the least-lifecycle-cost feasible Lucong River shed-service design under explicit uncertainty, supports observed and explicitly synthetic censuses, and presents both through an intuitive Streamlit/Plotly viewer.

**Architecture:** Keep five headless-tested modules for inputs, river load, process capacity, economics, and design/uncertainty decisions. Add a seeded synthetic-census generator, a prior-predictive scenario runner, reporting, and a thin Streamlit viewer that never contains model formulas. Borrow the load/cost/target separation from EPA RBEROST and BayOTA, the tidy scenario outputs from swmmio, and the provenance-focused interface from AquaScope; do not integrate SWMM or external solvers.

**Tech Stack:** Python 3.13.6, NumPy 2.3.4, Matplotlib 3.11.2, pytest 9.0.3, Streamlit 1.67.0, Plotly 7.1.0, openpyxl 3.1.5.

**Spec:** `docs/superpowers/specs/2026-11-24-river-economic-model-design.md`

## Global Constraints

- Study reach: exactly 1.0 km downstream from Santiago Bridge.
- Pilot duration: no greater than 12 months.
- 12-month cash requirement: no greater than PHP 10,000,000.
- Focus-stream allocation: at least 70%; shed-service base case is 100%.
- Target: station fecal coliform no greater than 8,000 MPN/100 mL.
- Robustness threshold: target probability at least 80% under joint uncertainty.
- Base-case compost and biogas revenue: PHP 0.
- No silent cap when computed source share `r > 1`; flag physical inconsistency.
- If no design reaches 80%, report no feasible design and the binding constraints; never lower the threshold after seeing results.
- Missing inputs must be labeled `missing`; scenario values must be labeled `assumption`.
- Fixed Monte Carlo seed: 2026; default draws: 20,000.
- Mass-balance closure tolerance: 5%.
- All outputs must be reproducible from one documented command.
- Workspace is not a Git repository. Do not initialize Git or create commits unless the user explicitly requests it.
- The original webinar screenshots are absent; do not claim they were reviewed.
- Synthetic mode must label every output `SYNTHETIC — NOT FIELD-VERIFIED` and every generated row `source="synthetic"`.
- Synthetic prior: 12–20 sheds; heads/shed triangular(8, 15, 25); drainage-connection probability equal-weight discrete {0.00, 0.25, 0.50, 0.75, 1.00}; barangay Santiago/Alfonso with equal probability.
- Synthetic defaults: seed 2026; 200 scenario censuses; at least 20,000 within-scenario joint draws for production runs.
- Public PSA/Bamban statistics provide context only and must not be allocated to Concepcion sheds.
- Design service sets are non-empty combinations of confirmed eligible barangays, not arbitrary exponential shed subsets.

## File Structure

```text
river_model/
├── __init__.py
├── __main__.py
├── inputs.py
├── synthetic.py
├── load.py
├── process.py
├── economics.py
├── design.py
├── uncertainty.py
├── reporting.py
├── scenarios.py
├── workbook.py
├── cli.py
└── app.py
tests/
├── fixtures/
│   └── census.csv
├── test_inputs.py
├── test_synthetic.py
├── test_load.py
├── test_process.py
├── test_economics.py
├── test_design.py
├── test_uncertainty.py
├── test_reporting.py
├── test_scenarios.py
├── test_workbook.py
├── test_app.py
└── test_end_to_end.py
requirements-dev.txt
docs/river_model_methods.md
```

`inputs.py` owns dataclasses, census parsing, overrides, and provenance. `synthetic.py` owns only the declared synthetic prior and reproducible census generation. `load.py`, `process.py`, and `economics.py` own independent formulas. `design.py` owns barangay-cluster candidate enumeration and hard constraints. `uncertainty.py` owns seeded draws and robust selection. `reporting.py` owns files and figures. `scenarios.py` owns prior-predictive orchestration across synthetic censuses. `app.py` owns presentation only.

---

### Task 1: Input Contracts, Census Loader, and Provenance Register

**Files:**
- Create: `river_model/__init__.py`
- Create: `river_model/inputs.py`
- Create: `tests/fixtures/census.csv`
- Create: `tests/test_inputs.py`
- Create: `requirements-dev.txt`

**Interfaces:**
- Consumes: census CSV with columns `shed_id,barangay,heads,drains_to_reach,source`.
- Produces: `Shed`, `Params`, `load_census(path: Path) -> tuple[Shed, ...]`, `eligible_sheds(sheds: Sequence[Shed]) -> tuple[Shed, ...]`, `apply_overrides(params: Params, overrides: Mapping[str, str]) -> Params`, `parameter_register(params: Params) -> list[dict[str, object]]`.

- [ ] **Step 1: Create the dependency file**

Create `requirements-dev.txt`:

```text
-r sim/requirements.txt
pytest==9.0.3
streamlit==1.67.0
plotly==7.1.0
openpyxl==3.1.5
```

- [ ] **Step 2: Create the census fixture**

Create `tests/fixtures/census.csv`:

```csv
shed_id,barangay,heads,drains_to_reach,source
S01,Santiago,10,true,MENRO census 2026-11-24
S02,Santiago,12,true,Barangay census 2026-11-24
S03,Alfonso,8,unknown,Team estimate 2026-11-24
```

- [ ] **Step 3: Write failing input tests**

Create `tests/test_inputs.py`:

```python
from dataclasses import fields, replace
from pathlib import Path

import pytest

from river_model.inputs import (
    Params,
    apply_overrides,
    eligible_sheds,
    load_census,
    parameter_register,
)

FIXTURE = Path(__file__).parent / "fixtures" / "census.csv"


def test_census_loads_and_excludes_unknown_drainage_from_base_case():
    sheds = load_census(FIXTURE)
    assert [s.shed_id for s in sheds] == ["S01", "S02", "S03"]
    assert [s.shed_id for s in eligible_sheds(sheds)] == ["S01", "S02"]
    assert eligible_sheds(sheds)[0].heads == 10


def test_census_rejects_duplicate_ids(tmp_path: Path):
    path = tmp_path / "bad.csv"
    path.write_text(
        "shed_id,barangay,heads,drains_to_reach,source\n"
        "S01,Santiago,10,true,test\n"
        "S01,Santiago,12,true,test\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="duplicate shed_id"):
        load_census(path)


def test_census_rejects_nonpositive_heads(tmp_path: Path):
    path = tmp_path / "bad.csv"
    path.write_text(
        "shed_id,barangay,heads,drains_to_reach,source\n"
        "S01,Santiago,0,true,test\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="heads must be positive"):
        load_census(path)


def test_override_parses_numbers_and_preserves_base_object():
    base = Params()
    changed = apply_overrides(base, {"q_m3_s": "0.08", "land_available_ha": "12.5"})
    assert changed.q_m3_s == 0.08
    assert changed.land_available_ha == 12.5
    assert base.q_m3_s == 0.05
    assert base.land_available_ha is None


def test_override_rejects_unknown_parameter():
    with pytest.raises(ValueError, match="unknown parameter"):
        apply_overrides(Params(), {"not_a_parameter": "1"})


def test_register_covers_every_parameter_and_marks_missing_land():
    rows = parameter_register(Params())
    names = {row["name"] for row in rows}
    expected = {field.name for field in fields(Params)}
    assert names == expected
    land = next(row for row in rows if row["name"] == "land_available_ha")
    assert land["status"] == "missing"
    assert land["value"] is None
```

- [ ] **Step 4: Run tests and verify failure**

Run: `python -m pytest tests/test_inputs.py -v`

Expected: FAIL because `river_model.inputs` does not exist.

- [ ] **Step 5: Implement the input module**

Create `river_model/inputs.py` with these exact dataclasses and defaults:

```python
from __future__ import annotations

import csv
from dataclasses import dataclass, fields, replace
from pathlib import Path
from typing import Literal, Mapping, Sequence

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
```

Implement `load_census` with `csv.DictReader`. Parse `drains_to_reach` as `true`, `false`, or `unknown`; reject any other token. Reject blank IDs, duplicate IDs, non-integer heads, and heads less than 1. `eligible_sheds` returns only rows where `drains_to_reach is True`.

Implement `apply_overrides` by checking `field.name` against `fields(Params)`, parsing `None`, integers, and floats, then returning `replace(params, **changed)`.

Implement `parameter_register` so every field appears exactly once. Use a `PARAMETER_META` dictionary keyed by field name with `unit`, `status`, and `source`. The test must fail if metadata is missing or extra. Mark `land_available_ha` and `upstream_mpn_100ml` as `missing`; mark `q_m3_s`, `e_head_day`, and `eta` as `assumption` with source text stating that field measurement or literature verification is required; mark `c0_mpn_100ml`, `ch4_mj_m3`, and `lpg_mj_kg` as `sourced`; mark target, budget, duration, and focus share as `design`.

- [ ] **Step 6: Run tests and verify pass**

Run: `python -m pytest tests/test_inputs.py -v`

Expected: 6 tests PASS.

- [ ] **Step 7: Verify package import**

Run: `python -c "from river_model.inputs import Params; print(Params().target_mpn_100ml)"`

Expected: `8000.0`.

---

### Task 1A: Seeded Synthetic Census Generator

**Files:**
- Create: `river_model/synthetic.py`
- Create: `tests/test_synthetic.py`

**Interfaces:**
- Consumes: `Shed` from Task 1 and the declared synthetic prior.
- Produces: `SyntheticSpec`, `generate_synthetic_census(spec: SyntheticSpec, scenario_id: int, seed: int) -> tuple[Shed, ...]`, `write_census(path: Path, sheds: Sequence[Shed]) -> None`.

- [ ] **Step 1: Write failing synthetic-census tests**

Create `tests/test_synthetic.py`:

```python
from dataclasses import replace
from pathlib import Path

import pytest

from river_model.inputs import load_census
from river_model.synthetic import (
    SyntheticSpec,
    generate_synthetic_census,
    write_census,
)


def test_fixed_seed_is_reproducible():
    spec = SyntheticSpec()
    a = generate_synthetic_census(spec, scenario_id=1, seed=2026)
    b = generate_synthetic_census(spec, scenario_id=1, seed=2026)
    assert a == b
    assert a != generate_synthetic_census(spec, scenario_id=1, seed=2027)


def test_generated_rows_obey_declared_bounds():
    spec = SyntheticSpec()
    sheds = generate_synthetic_census(spec, scenario_id=2, seed=2026)
    assert 12 <= len(sheds) <= 20
    assert all(8 <= shed.heads <= 25 for shed in sheds)
    assert all(shed.barangay in {"Santiago", "Alfonso"} for shed in sheds)
    assert len({shed.shed_id for shed in sheds}) == len(sheds)


def test_every_generated_row_is_labelled_synthetic():
    sheds = generate_synthetic_census(SyntheticSpec(), scenario_id=3, seed=2026)
    assert all(shed.source.startswith("synthetic;") for shed in sheds)
    assert all("scenario=3" in shed.source for shed in sheds)


def test_write_and_load_round_trip(tmp_path: Path):
    sheds = generate_synthetic_census(SyntheticSpec(), scenario_id=4, seed=2026)
    path = tmp_path / "synthetic.csv"
    write_census(path, sheds)
    assert load_census(path) == sheds


def test_invalid_prior_is_rejected():
    with pytest.raises(ValueError, match="heads_low"):
        generate_synthetic_census(
            replace(SyntheticSpec(), heads_low=30.0),
            scenario_id=1,
            seed=2026,
        )
    with pytest.raises(ValueError, match="connection_levels"):
        generate_synthetic_census(
            replace(SyntheticSpec(), connection_levels=(0.0, 1.5)),
            scenario_id=1,
            seed=2026,
        )
```

- [ ] **Step 2: Run tests and verify failure**

Run: `python -m pytest tests/test_synthetic.py -v`

Expected: FAIL because `river_model.synthetic` does not exist.

- [ ] **Step 3: Implement the synthetic generator**

Create `river_model/synthetic.py`:

```python
from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

import numpy as np

from river_model.inputs import Shed


@dataclass(frozen=True)
class SyntheticSpec:
    sheds_low: int = 12
    sheds_high: int = 20
    heads_low: float = 8.0
    heads_mode: float = 15.0
    heads_high: float = 25.0
    connection_levels: tuple[float, ...] = (0.0, 0.25, 0.50, 0.75, 1.00)
    barangays: tuple[str, ...] = ("Santiago", "Alfonso")
    default_scenarios: int = 200


def _validate(spec: SyntheticSpec) -> None:
    if spec.sheds_low < 1 or spec.sheds_high < spec.sheds_low:
        raise ValueError("shed bounds must be positive and ordered")
    if not (0 < spec.heads_low <= spec.heads_mode <= spec.heads_high):
        raise ValueError("heads_low, heads_mode, and heads_high must be positive and ordered")
    if not spec.connection_levels or any(
        value < 0.0 or value > 1.0 for value in spec.connection_levels
    ):
        raise ValueError("connection_levels must lie between 0 and 1")
    if len(spec.barangays) < 2 or len(set(spec.barangays)) != len(spec.barangays):
        raise ValueError("barangays must contain at least two unique names")
    if spec.default_scenarios < 1:
        raise ValueError("default_scenarios must be positive")


def generate_synthetic_census(
    spec: SyntheticSpec,
    scenario_id: int,
    seed: int,
) -> tuple[Shed, ...]:
    _validate(spec)
    if scenario_id < 1:
        raise ValueError("scenario_id must be positive")

    rng = np.random.default_rng(seed)
    n_sheds = int(rng.integers(spec.sheds_low, spec.sheds_high + 1))
    connection_probability = float(rng.choice(spec.connection_levels))
    sheds: list[Shed] = []

    for index in range(1, n_sheds + 1):
        heads = max(
            1,
            int(round(rng.triangular(spec.heads_low, spec.heads_mode, spec.heads_high))),
        )
        connected = bool(rng.random() < connection_probability)
        barangay = str(rng.choice(spec.barangays))
        source = (
            f"synthetic; scenario={scenario_id}; seed={seed}; "
            f"prior=sheds {spec.sheds_low}-{spec.sheds_high}, "
            f"heads triangular({spec.heads_low:g},{spec.heads_mode:g},{spec.heads_high:g}), "
            f"connection={connection_probability:.2f}"
        )
        sheds.append(
            Shed(
                shed_id=f"SYN-{scenario_id:04d}-{index:02d}",
                barangay=barangay,
                heads=heads,
                drains_to_reach=connected,
                source=source,
            )
        )

    return tuple(sheds)


def write_census(path: Path, sheds: Sequence[Shed]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["shed_id", "barangay", "heads", "drains_to_reach", "source"],
        )
        writer.writeheader()
        for shed in sheds:
            writer.writerow(
                {
                    "shed_id": shed.shed_id,
                    "barangay": shed.barangay,
                    "heads": shed.heads,
                    "drains_to_reach": (
                        "unknown" if shed.drains_to_reach is None else str(shed.drains_to_reach).lower()
                    ),
                    "source": shed.source,
                }
            )
```

- [ ] **Step 4: Run tests and verify pass**

Run: `python -m pytest tests/test_synthetic.py -v`

Expected: 5 tests PASS.

- [ ] **Step 5: Verify synthetic provenance in a generated file**

Run: `python -c "from pathlib import Path; from river_model.synthetic import SyntheticSpec,generate_synthetic_census,write_census; s=generate_synthetic_census(SyntheticSpec(),1,2026); write_census(Path('sim/outputs/synthetic_census_smoke.csv'),s); print(len(s), s[0].source)"`

Expected: a shed count from 12 through 20 and a source string beginning with `synthetic;`.

---

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

### Task 6: Joint Uncertainty, Sensitivity, and Robust Selection

**Files:**
- Create: `river_model/uncertainty.py`
- Create: `tests/test_uncertainty.py`

**Interfaces:**
- Consumes: `Params`, `Sequence[Shed]`, `Sequence[DesignEvaluation]`.
- Produces: `UncertaintySpec`, `MonteCarloResult`, `make_draws(spec: UncertaintySpec, n: int, seed: int) -> dict[str, object]`, `evaluate_design_uncertainty(params: Params, sheds: Sequence[Shed], evaluation: DesignEvaluation, draws: Mapping[str, object]) -> MonteCarloResult`, `run_uncertainty(params: Params, sheds: Sequence[Shed], evaluations: Sequence[DesignEvaluation], spec: UncertaintySpec) -> dict[Design, MonteCarloResult]`, `select_robust_design(params: Params, evaluations: Sequence[DesignEvaluation], results: Mapping[Design, MonteCarloResult]) -> DesignEvaluation | None`, `one_at_a_time(params: Params, sheds: Sequence[Shed], evaluation: DesignEvaluation, spec: UncertaintySpec) -> list[dict[str, object]]`.

- [ ] **Step 1: Write failing uncertainty tests**

Create `tests/test_uncertainty.py`:

```python
from dataclasses import replace
from pathlib import Path

import numpy as np

from river_model.design import DesignEvaluation, enumerate_designs
from river_model.inputs import Params, load_census
from river_model.uncertainty import (
    UncertaintySpec,
    evaluate_design_uncertainty,
    make_draws,
    one_at_a_time,
    run_uncertainty,
    select_robust_design,
)

FIXTURE = Path(__file__).parent / "fixtures" / "census.csv"


def test_fixed_seed_is_reproducible():
    spec = UncertaintySpec()
    a = make_draws(spec, 100, 2026)
    b = make_draws(spec, 100, 2026)
    assert np.array_equal(a["q"], b["q"])
    assert np.array_equal(a["eta"], b["eta"])


def test_zero_enrollment_cannot_meet_target():
    params = replace(Params(), p_enroll=0.0, land_available_ha=20.0)
    sheds = load_census(FIXTURE)
    evaluation = enumerate_designs(params, sheds)[0]
    draws = make_draws(UncertaintySpec(), 500, 2026)
    result = evaluate_design_uncertainty(params, sheds, evaluation, draws)
    assert result.p_target == 0.0


def test_invalid_draws_withhold_probability():
    params = replace(Params(), land_available_ha=20.0)
    sheds = load_census(FIXTURE)
    evaluation = enumerate_designs(params, sheds)[0]
    spec = UncertaintySpec(e_low=1.0e12, e_high=1.0e13)
    draws = make_draws(spec, 500, 2026)
    result = evaluate_design_uncertainty(params, sheds, evaluation, draws)
    assert result.invalid_fraction > 0.0
    assert result.p_target is None


def test_robust_selection_rejects_below_threshold():
    params = replace(Params(), land_available_ha=20.0, target_probability=0.99)
    sheds = load_census(FIXTURE)
    evaluations = enumerate_designs(params, sheds)
    results = run_uncertainty(
        params,
        sheds,
        evaluations,
        UncertaintySpec(n_draws=500, seed=2026),
    )
    selected = select_robust_design(params, evaluations, results)
    if selected is not None:
        assert results[selected.design].p_target >= 0.99


def test_sensitivity_has_expected_parameters():
    params = replace(Params(), land_available_ha=20.0)
    sheds = load_census(FIXTURE)
    evaluation = enumerate_designs(params, sheds)[0]
    rows = one_at_a_time(params, sheds, evaluation, UncertaintySpec())
    assert {row["parameter"] for row in rows} == {
        "q_m3_s",
        "e_head_day",
        "eta",
        "p_enroll",
        "p_collect",
        "p_retain",
        "cost_multiplier",
    }
```

- [ ] **Step 2: Run tests and verify failure**

Run: `python -m pytest tests/test_uncertainty.py -v`

Expected: FAIL because `river_model.uncertainty` does not exist.

- [ ] **Step 3: Implement uncertainty structures and draw generation**

Create `river_model/uncertainty.py` with:

```python
from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True)
class UncertaintySpec:
    q_low: float = 0.02
    q_high: float = 0.20
    e_low: float = 1.0e8
    e_high: float = 1.0e10
    eta_low: float = 0.50
    eta_mode: float = 0.80
    eta_high: float = 1.00
    p_enroll_low: float = 0.80
    p_enroll_mode: float = 0.95
    p_enroll_high: float = 0.99
    p_collect_low: float = 0.80
    p_collect_mode: float = 0.95
    p_collect_high: float = 0.99
    p_retain_low: float = 0.80
    p_retain_mode: float = 0.95
    p_retain_high: float = 0.99
    cost_low: float = 0.80
    cost_mode: float = 1.00
    cost_high: float = 1.30
    n_draws: int = 20_000
    seed: int = 2026


@dataclass(frozen=True)
class MonteCarloResult:
    p_target: float | None
    c_end_p10: float | None
    c_end_p50: float | None
    c_end_p90: float | None
    eac_p10: float | None
    eac_p50: float | None
    eac_p90: float | None
    invalid_fraction: float
    valid_draws: int
    endpoints: object
```

Implement `make_draws` with `np.random.default_rng(seed)`. Draw `q` log-uniformly, `e` log-uniformly, and `eta`, enrollment, collection, retention, and cost multiplier as triangular distributions using the low/mode/high fields. Return a dictionary with keys `q`, `e`, `eta`, `p_enroll`, `p_collect`, `p_retain`, `cost_multiplier`.

- [ ] **Step 4: Implement design uncertainty and robust selection**

Implement the draw evaluation with NumPy arrays so 200 synthetic scenarios can each use 20,000 draws without a Python loop over draws:

1. Compute `l0 = c0 * q * 86400 * 10000` as an array.
2. Compute `l_target = eta * sum(heads) * e` as an array.
3. Compute `r = l_target / l0`.
4. Build `invalid = (r > 1 + 1e-9) | (r < 0) | (q <= 0) | (e < 0) | (eta < 0) | (p_enroll < 0) | (p_collect < 0) | (p_retain < 0) | (cost_multiplier < 0)`.
5. For valid draws, compute `c = p_enroll * p_collect * p_retain`, `c_end = c0 * (1 - r * c)`, and `eac = evaluation.costs.eac * cost_multiplier`.
6. If `invalid_fraction > 0`, set all probability and percentile fields to `None`, set `endpoints` to an empty NumPy array, and do not truncate invalid draws.
7. Otherwise compute `p_target = mean(c_end <= target_mpn_100ml)`, compute the 10th/50th/90th percentiles, and return the endpoint array in `endpoints` for histogram reporting.

`run_uncertainty` evaluates every `constraint_feasible` evaluation using the same `draws` object, ensuring common random numbers. It returns a dictionary keyed by `Design`.

`select_robust_design` filters for:

- `constraint_feasible(evaluation)`.
- `results[evaluation.design].p_target is not None`.
- `p_target >= params.target_probability`.

It returns the candidate with the lowest `costs.eac`, or `None`.

`one_at_a_time` varies `q`, `e`, `eta`, each capture component, and cost multiplier between the low and high values in `UncertaintySpec`. For each setting, create a scenario-specific `UncertaintySpec` with that parameter fixed to the tested value, regenerate draws with the same seed, rerun `evaluate_design_uncertainty`, and record `p_target`, median endpoint, median EAC, and whether the 80% feasibility decision changes. Cost multiplier is expected to change EAC but not target probability; report that explicitly rather than forcing a decision flip.

- [ ] **Step 5: Run tests and verify pass**

Run: `python -m pytest tests/test_uncertainty.py -v`

Expected: 5 tests PASS.

- [ ] **Step 6: Run a 20,000-draw smoke test**

Run: `python -c "from pathlib import Path; from dataclasses import replace; from river_model.inputs import Params,load_census; from river_model.design import enumerate_designs; from river_model.uncertainty import UncertaintySpec,run_uncertainty,select_robust_design; p=replace(Params(),land_available_ha=20.0); s=load_census(Path('tests/fixtures/census.csv')); e=enumerate_designs(p,s); r=run_uncertainty(p,s,e,UncertaintySpec()); x=select_robust_design(p,e,r); print('selected', x.design if x else None, 'probability', r[x.design].p_target if x else None)"`

Expected: either a selected design with probability at least 0.80 or `selected None`; no invalid probability may be used for selection.

---

### Task 7: Reporting, Figures, Static HTML, and CLI

**Files:**
- Create: `river_model/reporting.py`
- Create: `river_model/cli.py`
- Create: `river_model/__main__.py`
- Create: `tests/test_reporting.py`

**Interfaces:**
- Consumes: parameter register, evaluations, uncertainty results, selected design.
- Produces: `write_outputs(output_dir: Path, params: Params, register: list[dict[str, object]], evaluations: Sequence[DesignEvaluation], results: Mapping[Design, MonteCarloResult], selected: DesignEvaluation | None, alternatives: Sequence[AlternativeEvaluation], mode: str) -> dict[str, Path]`, `run_model(census_path: Path, output_dir: Path, overrides: Mapping[str, str], n_draws: int, seed: int, mode: str = "observed") -> dict[str, object]`.

- [ ] **Step 1: Write failing reporting tests**

Create `tests/test_reporting.py`:

```python
import csv
import json
from pathlib import Path

from river_model.cli import run_model

FIXTURE = Path(__file__).parent / "fixtures" / "census.csv"


def test_run_model_writes_required_outputs(tmp_path: Path):
    result = run_model(
        FIXTURE,
        tmp_path,
        {"land_available_ha": "20"},
        n_draws=200,
        seed=2026,
    )
    expected = {
        "parameter_register.csv",
        "candidate_designs.csv",
        "alternatives.csv",
        "monte_carlo_summary.csv",
        "selected_design.json",
        "decision_brief.md",
        "cost_reduction_frontier.html",
        "uncertainty.html",
        "fig2_lucong_model.png",
    }
    assert expected <= set(result["files"])
    for name in expected:
        assert (tmp_path / name).exists()


def test_selected_design_json_is_valid_and_has_probability(tmp_path: Path):
    result = run_model(
        FIXTURE,
        tmp_path,
        {"land_available_ha": "20"},
        n_draws=200,
        seed=2026,
    )
    payload = json.loads((tmp_path / "selected_design.json").read_text(encoding="utf-8"))
    assert payload["mode"] == "observed"
    assert payload["evidence_label"] == "OBSERVED CENSUS"
    assert payload["selected"] in (True, False)
    if payload["selected"]:
        assert payload["target_probability"] >= 0.80


def test_candidate_csv_has_rejection_reasons(tmp_path: Path):
    run_model(
        FIXTURE,
        tmp_path,
        {"land_available_ha": "20"},
        n_draws=50,
        seed=2026,
    )
    with (tmp_path / "candidate_designs.csv").open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    assert rows
    assert "rejection_reasons" in rows[0]
```

- [ ] **Step 2: Run tests and verify failure**

Run: `python -m pytest tests/test_reporting.py -v`

Expected: FAIL because `river_model.cli` does not exist.

- [ ] **Step 3: Implement reporting**

Create `river_model/reporting.py` with CSV writers using `csv.DictWriter`, JSON output using `json.dump(payload, handle, indent=2)`, and Markdown output using plain strings.

`candidate_designs.csv` must contain one row per evaluation with columns:

```text
shed_ids,modules,tankers,carts,collection_days_week,capex,cash_12m,eac,
c_end_mpn_100ml,reduction_fraction,annual_mpn_prevented_12,land_ha_required,
digester_hrt_days,trips_week,feasible,rejection_reasons
```

`alternatives.csv` must contain one row per alternative with columns:

```text
name,c_end_low_mpn_100ml,c_end_mode_mpn_100ml,c_end_high_mpn_100ml,
annual_mpn_prevented_12_mode,cash_12m_mode,eac_mode,cost_status,
legal_status,measurable_12m,note
```

`monte_carlo_summary.csv` must contain one row per uncertainty result with columns:

```text
shed_ids,modules,tankers,carts,p_target,c_end_p10,c_end_p50,c_end_p90,
eac_p10,eac_p50,eac_p90,invalid_fraction,valid_draws
```

`selected_design.json` must contain:

```python
{
    "mode": mode,
    "evidence_label": "SYNTHETIC — NOT FIELD-VERIFIED" if mode == "synthetic" else "OBSERVED CENSUS",
    "selected": selected is not None,
    "target_probability": params.target_probability,
    "design": asdict(selected.design) if selected else None,
    "reason": "least-lifecycle-cost feasible design" if selected else "no feasible design",
}
```

Create two Plotly HTML figures:

- `cost_reduction_frontier.html`: x = annual MPN prevented, y = annualized cost, color = feasible/infeasible, hover text = shed IDs and rejection reasons.
- `uncertainty.html`: histogram of `MonteCarloResult.endpoints` for the selected design with a vertical line at 8,000. If no design is selected but a constraint-feasible uncertainty result exists, show the result with the highest valid target probability and label it “not selected.” If no constraint-feasible result exists, write an HTML page stating that no design could be evaluated because hard constraints failed.

Create `fig2_lucong_model.png` with Matplotlib: left panel cost–reduction frontier; right panel endpoint histogram or tornado for the selected design. Use the Agg backend.

`decision_brief.md` must begin with `OBSERVED CENSUS` or `SYNTHETIC — NOT FIELD-VERIFIED`, state the selected design or explicitly state that none is feasible, list cash, annualized cost, endpoint interval, target probability, binding constraints, and the three most decision-sensitive inputs. In synthetic mode it must state that probabilities are conditional on the declared synthetic-census prior.

- [ ] **Step 4: Implement the CLI orchestrator**

Create `river_model/cli.py`:

```python
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Mapping

from river_model.design import enumerate_designs, evaluate_alternatives
from river_model.inputs import Params, apply_overrides, load_census, parameter_register
from river_model.reporting import write_outputs
from river_model.uncertainty import (
    UncertaintySpec,
    run_uncertainty,
    select_robust_design,
)


def run_model(
    census_path: Path,
    output_dir: Path,
    overrides: Mapping[str, str],
    n_draws: int,
    seed: int,
    mode: str = "observed",
) -> dict[str, object]:
    if mode not in {"observed", "synthetic"}:
        raise ValueError("mode must be observed or synthetic")
    params = apply_overrides(Params(), overrides)
    sheds = load_census(census_path)
    evaluations = enumerate_designs(params, sheds)
    spec = UncertaintySpec(n_draws=n_draws, seed=seed)
    results = run_uncertainty(params, sheds, evaluations, spec)
    selected = select_robust_design(params, evaluations, results)
    files = write_outputs(
        output_dir,
        params,
        parameter_register(params),
        evaluations,
        results,
        selected,
        evaluate_alternatives(params),
        mode,
    )
    return {
        "mode": mode,
        "params": params,
        "selected": selected,
        "results": results,
        "files": files,
    }
```

Create `river_model/__main__.py` with argparse options:

```text
--census PATH              required
--output PATH              default sim/outputs/river_model
--draws INT                default 20000
--seed INT                 default 2026
--set NAME=VALUE           repeatable
```

Print a concise summary: number of candidates, number constraint-feasible, selected design or “no feasible design,” cash, annualized cost, endpoint interval, and target probability.

- [ ] **Step 5: Run reporting tests and verify pass**

Run: `python -m pytest tests/test_reporting.py -v`

Expected: 3 tests PASS.

- [ ] **Step 6: Run the CLI**

Run: `python -m river_model --census tests/fixtures/census.csv --output sim/outputs/river_model_smoke --draws 500 --seed 2026 --set land_available_ha=20`

Expected: all required files are written and the terminal summary matches `selected_design.json`.

---

### Task 7A: Prior-Predictive Scenario Runner and Synthetic CLI

**Files:**
- Create: `river_model/scenarios.py`
- Create: `tests/test_scenarios.py`
- Modify: `river_model/cli.py`
- Modify: `river_model/__main__.py`

**Interfaces:**
- Consumes: `SyntheticSpec`, `generate_synthetic_census`, `write_census`, `enumerate_designs`, `run_uncertainty`, `select_robust_design`, and `run_model`.
- Produces: `ScenarioSummary`, `run_synthetic_model(output_dir: Path, overrides: Mapping[str, str], n_scenarios: int, n_draws: int, seed: int) -> dict[str, object]`.

- [ ] **Step 1: Write failing scenario-runner tests**

Create `tests/test_scenarios.py`:

```python
import csv
import json
import subprocess
import sys
from pathlib import Path

from river_model.scenarios import run_synthetic_model

ROOT = Path(__file__).resolve().parents[1]


def test_synthetic_run_writes_prior_predictive_outputs(tmp_path: Path):
    result = run_synthetic_model(
        tmp_path,
        {"land_available_ha": "20"},
        n_scenarios=5,
        n_draws=100,
        seed=2026,
    )
    expected = {
        "synthetic_census_example.csv",
        "synthetic_scenarios.csv",
        "prior_predictive_summary.json",
        "selected_design.json",
        "decision_brief.md",
    }
    assert expected <= set(result["files"])
    for name in expected:
        assert (tmp_path / name).exists()

    payload = json.loads((tmp_path / "prior_predictive_summary.json").read_text(encoding="utf-8"))
    assert payload["mode"] == "synthetic"
    assert payload["evidence_label"] == "SYNTHETIC — NOT FIELD-VERIFIED"
    assert payload["n_scenarios"] == 5
    assert payload["n_draws"] == 100

    with (tmp_path / "synthetic_scenarios.csv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 5

    with (tmp_path / "synthetic_census_example.csv").open(encoding="utf-8", newline="") as handle:
        census_rows = list(csv.DictReader(handle))
    assert census_rows
    assert all(row["source"].startswith("synthetic;") for row in census_rows)


def test_synthetic_run_is_reproducible(tmp_path: Path):
    a = tmp_path / "a"
    b = tmp_path / "b"
    run_synthetic_model(a, {"land_available_ha": "20"}, 4, 80, 2026)
    run_synthetic_model(b, {"land_available_ha": "20"}, 4, 80, 2026)
    assert (a / "synthetic_scenarios.csv").read_bytes() == (b / "synthetic_scenarios.csv").read_bytes()
    assert (a / "prior_predictive_summary.json").read_bytes() == (b / "prior_predictive_summary.json").read_bytes()


def test_synthetic_cli_runs_without_census(tmp_path: Path):
    output = tmp_path / "output"
    command = [
        sys.executable,
        "-m",
        "river_model",
        "--synthetic",
        "--output",
        str(output),
        "--scenarios",
        "3",
        "--draws",
        "50",
        "--seed",
        "2026",
        "--set",
        "land_available_ha=20",
    ]
    completed = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    assert completed.returncode == 0, completed.stderr
    payload = json.loads((output / "prior_predictive_summary.json").read_text(encoding="utf-8"))
    assert payload["n_scenarios"] == 3
```

- [ ] **Step 2: Run tests and verify failure**

Run: `python -m pytest tests/test_scenarios.py -v`

Expected: FAIL because `river_model.scenarios` does not exist and the CLI has no `--synthetic` option.

- [ ] **Step 3: Implement scenario structures and orchestration**

Create `river_model/scenarios.py` with:

```python
from __future__ import annotations

import csv
import json
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from statistics import median
from typing import Mapping

import numpy as np

from river_model.cli import run_model
from river_model.design import enumerate_designs
from river_model.inputs import Params, apply_overrides, eligible_sheds
from river_model.synthetic import SyntheticSpec, generate_synthetic_census, write_census
from river_model.uncertainty import UncertaintySpec, run_uncertainty, select_robust_design


@dataclass(frozen=True)
class ScenarioSummary:
    scenario_id: int
    n_sheds: int
    connected_sheds: int
    connected_heads: int
    source_share_r: float | None
    selected: bool
    design_key: str | None
    best_p_target: float | None
    selected_p_target: float | None
    cash_12m: float | None
    eac: float | None
    c_end_p50: float | None
    invalid_fraction: float | None
    dominant_constraint: str | None
```

Implement `run_synthetic_model` with this exact logic:

1. Reject `n_scenarios < 1`, `n_draws < 1`, or `seed < 0`.
2. Create `output_dir` and set `params = apply_overrides(Params(), overrides)`.
3. For each `scenario_id` from 1 through `n_scenarios`, set `scenario_seed = seed + scenario_id - 1`.
4. Generate the census with `SyntheticSpec()`, enumerate designs, run uncertainty with `UncertaintySpec(n_draws=n_draws, seed=scenario_seed)`, and select the robust design.
5. Record total sheds, confirmed connected sheds, connected heads, deterministic source share `r` for the selected design or the highest-`r` constraint-feasible design, selection, a configuration-only design key, best valid target probability among constraint-feasible designs, selected probability, selected cash/EAC/median endpoint, maximum invalid fraction, and the most frequent rejection reason.
6. Choose the representative scenario with connected heads closest to the median connected-head count; break ties by lower scenario ID.
7. Write `synthetic_census_example.csv` for the representative scenario, then call `run_model(representative_path, output_dir, overrides, n_draws=n_draws, seed=representative_seed, mode="synthetic")` to produce the standard artifacts for that scenario. Append the synthetic prior, scenario count, and representative scenario ID to `verification_report.txt`.
8. Write `synthetic_scenarios.csv` with columns exactly:

```text
scenario_id,n_sheds,connected_sheds,connected_heads,source_share_r,selected,
design_key,best_p_target,selected_p_target,cash_12m,eac,c_end_p50,
invalid_fraction,dominant_constraint
```

9. Write `prior_predictive_summary.json` containing:

```python
valid_p = [row.best_p_target for row in summaries if row.best_p_target is not None]
heads = [row.connected_heads for row in summaries]
source_shares = [row.source_share_r for row in summaries if row.source_share_r is not None]
{
    "mode": "synthetic",
    "evidence_label": "SYNTHETIC — NOT FIELD-VERIFIED",
    "prior": asdict(SyntheticSpec()),
    "seed": seed,
    "n_scenarios": n_scenarios,
    "n_draws": n_draws,
    "selected_count": sum(row.selected for row in summaries),
    "no_feasible_count": sum(not row.selected for row in summaries),
    "invalid_scenario_count": sum((row.invalid_fraction or 0.0) > 0.0 for row in summaries),
    "selected_design_frequencies": dict(
        Counter(row.design_key for row in summaries if row.design_key is not None)
    ),
    "connected_heads_p10": float(np.percentile(heads, 10)),
    "connected_heads_p50": float(np.percentile(heads, 50)),
    "connected_heads_p90": float(np.percentile(heads, 90)),
    "source_share_r_p10": float(np.percentile(source_shares, 10)) if source_shares else None,
    "source_share_r_p50": float(np.percentile(source_shares, 50)) if source_shares else None,
    "source_share_r_p90": float(np.percentile(source_shares, 90)) if source_shares else None,
    "best_p_target_p10": float(np.percentile(valid_p, 10)) if valid_p else None,
    "best_p_target_p50": float(np.percentile(valid_p, 50)) if valid_p else None,
    "best_p_target_p90": float(np.percentile(valid_p, 90)) if valid_p else None,
    "dominant_constraints": dict(
        Counter(row.dominant_constraint for row in summaries if row.dominant_constraint is not None)
    ),
}
```

Use `None` for percentile fields when no valid values exist. Count an invalid scenario when any evaluated uncertainty result has `invalid_fraction > 0`.

- [ ] **Step 4: Implement the synthetic CLI branch**

Replace the Task 7 argparse body in `river_model/__main__.py` with:

```python
from __future__ import annotations

import argparse
from pathlib import Path

from river_model.cli import run_model
from river_model.scenarios import run_synthetic_model


def main() -> None:
    parser = argparse.ArgumentParser(description="Lucong River intervention model")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--census", type=Path)
    source.add_argument("--synthetic", action="store_true")
    parser.add_argument("--output", type=Path, default=Path("sim/outputs/river_model"))
    parser.add_argument("--draws", type=int, default=20_000)
    parser.add_argument("--seed", type=int, default=2026)
    parser.add_argument("--scenarios", type=int, default=200)
    parser.add_argument("--set", action="append", default=[])

    args = parser.parse_args()
    overrides = dict(item.split("=", 1) for item in args.set)

    if args.synthetic:
        result = run_synthetic_model(
            args.output,
            overrides,
            n_scenarios=args.scenarios,
            n_draws=args.draws,
            seed=args.seed,
        )
        summary = result["summary"]
        print("SYNTHETIC — NOT FIELD-VERIFIED")
        print(
            f"scenarios={summary['n_scenarios']} "
            f"selected={summary['selected_count']} "
            f"no_feasible={summary['no_feasible_count']}"
        )
        print(f"wrote {args.output / 'prior_predictive_summary.json'}")
        return

    result = run_model(
        args.census,
        args.output,
        overrides,
        n_draws=args.draws,
        seed=args.seed,
    )
    selected = result["selected"]
    print("OBSERVED CENSUS")
    print(selected.design if selected else "no feasible design")
    print(f"wrote {args.output / 'selected_design.json'}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 5: Run scenario tests and verify pass**

Run: `python -m pytest tests/test_scenarios.py -v`

Expected: 3 tests PASS.

- [ ] **Step 6: Run a reproducible synthetic smoke test**

Run: `python -m river_model --synthetic --output sim/outputs/river_model_synthetic_smoke --scenarios 10 --draws 500 --seed 2026 --set land_available_ha=20`

Expected: all standard outputs plus `synthetic_census_example.csv`, `synthetic_scenarios.csv`, and `prior_predictive_summary.json`; every synthetic artifact carries the evidence label.

---

### Task 8: Intuitive Streamlit/Plotly Viewer

**Files:**
- Create: `river_model/app.py`
- Create: `tests/test_app.py`

**Interfaces:**
- Consumes: `run_model`, `run_synthetic_model`, parameter register, evaluations, uncertainty results.
- Produces: `build_app(census_path: Path | None, synthetic: bool = False, n_scenarios: int = 200, n_draws: int = 20_000, seed: int = 2026) -> None`, `main() -> None`.

- [ ] **Step 1: Write failing viewer tests**

Create `tests/test_app.py`:

```python
from pathlib import Path

from streamlit.testing.v1 import AppTest

FIXTURE = Path(__file__).parent / "fixtures" / "census.csv"


def test_app_renders_all_tabs_without_exception():
    app = AppTest.from_function(build_app, args=(FIXTURE, False, 200, 500, 2026)).run()
    assert not app.exception
    labels = [tab.label for tab in app.tabs]
    assert labels == [
        "Overview",
        "Assumptions",
        "Designs",
        "Compare",
        "Uncertainty and methods",
    ]


def test_app_shows_missing_land_message():
    app = AppTest.from_function(build_app, args=(FIXTURE, False, 200, 500, 2026)).run()
    assert not app.exception
    assert any("land evidence missing" in str(item.value) for item in app.error)


def test_synthetic_app_shows_evidence_warning():
    app = AppTest.from_function(build_app, args=(None, True, 3, 50, 2026)).run()
    assert not app.exception
    assert any("SYNTHETIC — NOT FIELD-VERIFIED" in str(item.value) for item in app.warning)


def test_app_has_download_buttons():
    app = AppTest.from_function(build_app, args=(FIXTURE, False, 200, 500, 2026)).run()
    assert not app.exception
    assert len(app.download_button) >= 3
```

Add the import inside the test file:

```python
from river_model.app import build_app
```

- [ ] **Step 2: Run tests and verify failure**

Run: `python -m pytest tests/test_app.py -v`

Expected: FAIL because `river_model.app` does not exist.

- [ ] **Step 3: Implement the viewer shell and shared state**

Create `river_model/app.py` with `st.set_page_config(page_title="Lucong River Model", layout="wide")`.

Use `st.session_state` for:

```python
{
    "overrides": {},
    "comparison_ids": [],
    "census_path": str(census_path) if census_path else None,
    "synthetic": synthetic,
    "n_scenarios": n_scenarios,
    "n_draws": n_draws,
    "seed": seed,
}
```

Cache model execution with `@st.cache_data` around separate observed and synthetic helpers. The observed key must include census file bytes, sorted override items, draw count, and seed. The synthetic key must include sorted override items, scenario count, draw count, and seed. The synthetic helper must run in a temporary directory and return the result plus output-file bytes so downloads remain available after the directory is removed. Do not cache on a mutable dictionary alone.

- [ ] **Step 4: Implement the five tabs**

Before the tabs, render `st.warning("SYNTHETIC — NOT FIELD-VERIFIED")` in synthetic mode and show the declared prior, scenario count, draw count, and seed. In observed mode render `st.caption("OBSERVED CENSUS")`. Repeat a short mode caption inside every tab.

**Overview tab:**

- Render a plain Plotly reach schematic with four labeled nodes: Santiago Bridge, shed cluster, 1-km reach, EMB station.
- Render KPI cards using `st.metric`: selected design, 12-month cash, annualized cost, endpoint median, target probability, annual MPN prevented.
- In synthetic mode, render a Plotly histogram of connected heads and a bar chart of selected-design frequencies from `prior_predictive_summary.json`; label both as prior-predictive.
- If no design is selected, render `st.error("No feasible design meets the 80% target-probability rule.")` and list binding constraints.

**Assumptions tab:**

- Group controls under Load, Process, Capacity, Cost, and Decision headings.
- Use `st.number_input` for numeric values and `st.selectbox` for evidence status display.
- Show unit, source, and base/scenario label beside every control.
- Sourced or design values changed by the user must display a visible “Scenario override” warning.
- Add a `Reset to base case` button that clears `st.session_state["overrides"]`.

**Designs tab:**

- Build a pandas-free list of dictionaries from evaluations.
- Use `st.dataframe` with column configuration for currency, percentages, and MPN/100 mL.
- Add a feasibility filter with options All, Feasible, Infeasible.
- Render the Plotly cost–reduction frontier.
- Render a separate alternatives table from `alternatives.csv`; show `Missing` rather than 0 when an alternative has no cost quote.
- Add text rejection reasons; never rely on red/green color alone.

**Compare tab:**

- Allow up to three candidate IDs with `st.multiselect`.
- Render side-by-side `st.metric` blocks for cash, annualized cost, endpoint, reduction, land, HRT, and trips.
- Render a cost-breakdown bar chart and a constraint table with Pass/Fail/Missing text.

**Uncertainty and methods tab:**

- Render the endpoint histogram with the 8,000 threshold.
- Render a tornado chart from `one_at_a_time`.
- Display equations in `st.latex`.
- Display validation status and the parameter register.
- Add download buttons for candidate CSV, parameter register CSV, selected-design JSON, decision brief, and static HTML.

- [ ] **Step 5: Implement the real entry point**

`main()` must offer a mode selector with `Observed census` and `Synthetic prior-predictive`. Observed mode reads `RIVER_MODEL_CENSUS` when set, otherwise shows a file uploader and requires a CSV before running. Synthetic mode requires no upload and exposes scenario count, draw count, and seed controls. `build_app(census_path, synthetic)` is the testable entry point and must not depend on an uploader.

Add a static export button that writes the already-generated Plotly HTML files to a user-selected directory through `st.download_button` with file bytes. Synthetic mode must also offer downloads for `synthetic_scenarios.csv` and `prior_predictive_summary.json`.

- [ ] **Step 6: Run viewer tests and verify pass**

Run: `python -m pytest tests/test_app.py -v`

Expected: 4 tests PASS.

- [ ] **Step 7: Run the headed browser golden path**

Start: `streamlit run river_model/app.py --server.port 8501`

Use the installed Playwright MCP to verify:

1. Upload `tests/fixtures/census.csv`.
2. Overview renders and either selects a design or clearly reports infeasibility.
3. Change `q_m3_s` in Assumptions; a “Scenario override” warning appears and results rerun.
4. Reset to base case; the warning disappears.
5. Designs filter toggles between feasible and infeasible rows.
6. Compare shows two designs side by side.
7. Uncertainty tab shows the 8,000 threshold line.
8. At least one CSV download succeeds.
9. Switch to Synthetic prior-predictive; the warning, declared prior, connected-head histogram, and selected-design frequency chart render without an upload.
10. Download `prior_predictive_summary.json` and confirm its evidence label is `SYNTHETIC — NOT FIELD-VERIFIED`.
11. Browser console shows no uncaught exceptions.

Record the checked items in `docs/river_model_methods.md`; do not claim browser verification if the server cannot be started.

---

### Task 9: Independent Workbook, End-to-End Verification, and Methods Note

**Files:**
- Create: `river_model/workbook.py`
- Create: `tests/test_workbook.py`
- Create: `tests/test_end_to_end.py`
- Create: `docs/river_model_methods.md`

**Interfaces:**
- Consumes: selected `DesignEvaluation`, `Params`.
- Produces: `write_verification_workbook(path: Path, params: Params, evaluation: DesignEvaluation) -> None`.

- [ ] **Step 1: Write failing workbook tests**

Create `tests/test_workbook.py`:

```python
from pathlib import Path

from openpyxl import load_workbook

from river_model.design import enumerate_designs
from river_model.inputs import Params, load_census
from river_model.workbook import write_verification_workbook

FIXTURE = Path(__file__).parent / "fixtures" / "census.csv"


def test_workbook_contains_independent_formulas(tmp_path: Path):
    params = Params()
    sheds = load_census(FIXTURE)
    evaluation = enumerate_designs(params, sheds)[0]
    path = tmp_path / "check.xlsx"
    write_verification_workbook(path, params, evaluation)
    wb = load_workbook(path, data_only=False)
    assert wb.sheetnames == ["Inputs", "Load", "Process", "Cost", "Comparison"]
    assert wb["Load"]["B5"].value == "=B2*B3*86400*10000"
    assert wb["Comparison"]["B2"].value is not None
```

- [ ] **Step 2: Run test and verify failure**

Run: `python -m pytest tests/test_workbook.py -v`

Expected: FAIL because `river_model.workbook` does not exist.

- [ ] **Step 3: Implement the verification workbook**

Create `river_model/workbook.py` using openpyxl. The workbook must contain:

- `Inputs`: parameter name, value, unit, status, source.
- `Load`: cells `B2=C0`, `B3=Q`, `B4=L_gen`, `B5=L0`, `B6=r`, `B7=c`, `B8=C_end`; formulas in `B5`, `B6`, `B7`, `B8`.
- `Process`: manure, washwater, slurry, VS in, VS destroyed, methane, biogas, LPG equivalent, nutrient N, land, trips.
- `Cost`: CAPEX, OPEX, contingency, 12-month cash, NPC, EAC, unit costs.
- `Comparison`: Python model value, spreadsheet formula, absolute difference, pass/fail with tolerance `0.01` for costs and `1e-6` for physical quantities.

Write formulas as strings and also write the Python-computed values in adjacent cells. Do not claim the formulas were recalculated by Excel unless a spreadsheet engine actually opens and recalculates the file. The methods note must state that the workbook is an independent formula audit and that cached formula values require Excel/LibreOffice recalculation.

- [ ] **Step 4: Run workbook test and verify pass**

Run: `python -m pytest tests/test_workbook.py -v`

Expected: 1 test PASS.

- [ ] **Step 5: Write the end-to-end test**

Create `tests/test_end_to_end.py`:

```python
import json
import subprocess
import sys
from pathlib import Path


def test_cli_end_to_end(tmp_path: Path):
    root = Path(__file__).resolve().parents[1]
    output = tmp_path / "output"
    command = [
        sys.executable,
        "-m",
        "river_model",
        "--census",
        str(root / "tests" / "fixtures" / "census.csv"),
        "--output",
        str(output),
        "--draws",
        "1000",
        "--seed",
        "2026",
        "--set",
        "land_available_ha=20",
    ]
    completed = subprocess.run(command, cwd=root, capture_output=True, text=True)
    assert completed.returncode == 0, completed.stderr
    payload = json.loads((output / "selected_design.json").read_text(encoding="utf-8"))
    assert payload["selected"] in (True, False)
    assert (output / "verification_report.txt").exists()
    assert (output / "verification_workbook.xlsx").exists()


def test_synthetic_cli_end_to_end(tmp_path: Path):
    root = Path(__file__).resolve().parents[1]
    output = tmp_path / "synthetic_output"
    command = [
        sys.executable,
        "-m",
        "river_model",
        "--synthetic",
        "--output",
        str(output),
        "--scenarios",
        "3",
        "--draws",
        "100",
        "--seed",
        "2026",
        "--set",
        "land_available_ha=20",
    ]
    completed = subprocess.run(command, cwd=root, capture_output=True, text=True)
    assert completed.returncode == 0, completed.stderr
    payload = json.loads((output / "prior_predictive_summary.json").read_text(encoding="utf-8"))
    assert payload["mode"] == "synthetic"
    assert payload["n_scenarios"] == 3
    assert (output / "synthetic_census_example.csv").exists()
    assert (output / "synthetic_scenarios.csv").exists()
```

- [ ] **Step 6: Add final verification report generation**

Update `write_outputs` to write `verification_report.txt` containing:

- Python version.
- NumPy version.
- Mode and evidence label (`OBSERVED CENSUS` or `SYNTHETIC — NOT FIELD-VERIFIED`).
- Seed and draw count; scenario count and synthetic prior in synthetic mode.
- Candidate count.
- Constraint-feasible count.
- Invalid-draw fraction for the selected or best near-feasible design.
- Selected design or explicit infeasibility.
- Each acceptance check as PASS or FAIL.
- A statement if the workbook formulas were not recalculated by a spreadsheet engine.

When a selected design exists, call `write_verification_workbook` and write `verification_workbook.xlsx`. When no design exists but a constraint-feasible uncertainty result exists, write the workbook for the result with the highest valid target probability and label it “not selected.” When no constraint-feasible result exists, write the workbook for the lowest-EAC evaluated design, label it “not selected—hard constraints failed,” and leave probability fields blank.

- [ ] **Step 7: Run the complete test suite**

Run: `python -m pytest -q`

Expected: all tests PASS. If any test fails, fix the implementation before proceeding; do not mark the task complete.

- [ ] **Step 8: Run the reproducible production commands**

Synthetic prior-predictive run:

```bash
python -m river_model --synthetic --output sim/outputs/river_model_synthetic --scenarios 200 --draws 20000 --seed 2026 --set land_available_ha=20
```

Observed run when a verified census is available:

```bash
python -m river_model --census <verified-census.csv> --output sim/outputs/river_model --draws 20000 --seed 2026
```

If the verified census has not been supplied, use the fixture only for a smoke test and label the output as test data. Do not present fixture or synthetic results as observed Lucong findings.

- [ ] **Step 9: Write the methods note**

Create `docs/river_model_methods.md` with:

- Purpose and decision rule.
- Exact equations from the specification.
- Input schema and provenance rules.
- Census, flow, source-share, cost, and land data requirements.
- Observed-versus-synthetic mode, exact synthetic prior, seed, scenario count, and prior-predictive interpretation.
- How to run the CLI and viewer in both modes.
- How to interpret feasibility, target probability, and invalid draws.
- GitHub comparators and the specific patterns borrowed.
- Validation commands and results.
- Browser checks actually performed.
- Explicit limitations: parameterized not calibrated; no health benefit claim; no 200 MPN compliance claim; original screenshots absent; workbook formula recalculation status.

- [ ] **Step 10: Final review against the specification**

Confirm each specification section maps to a completed artifact:

- Sections 1–3: scope and constraints in CLI, tests, and methods note.
- Sections 4–6: five model modules and equations.
- Section 5.1: observed census loader, seeded synthetic generator, explicit priors, and provenance labels.
- Section 7: barangay-cluster enumeration, rejection reasons, robust selection, and same-functional-unit alternative comparison.
- Section 8: joint draws, invalid-draw handling, tornado/decision-flip output, and prior-predictive scenario summaries.
- Section 9: pytest suite, independent workbook, reproducibility report.
- Section 10: five-tab Streamlit viewer, static HTML, AppTest, headed browser check.
- Sections 11–13: outputs, claim boundaries, completion criteria.

Any uncovered requirement blocks completion.

---

## Research References

- [USEPA RBEROST](https://github.com/USEPA/RBEROST) — minimum-lifecycle-cost BMP decision structure.
- [BayOTA](https://github.com/dkauf42/bayota) — reproducible scenario and constraint-sweep framework.
- [USEPA SWMM](https://github.com/USEPA/Stormwater-Management-Model) and [PySWMM](https://github.com/pyswmm/pyswmm) — dynamic drainage scenarios; not integrated into the core.
- [swmmio](https://github.com/pyswmm/swmmio) — tidy input/output tables.
- [WaterModels.jl](https://github.com/lanl-ansi/WaterModels.jl) — explicit problem specification separated from solver execution.
- [AquaScope](https://github.com/Rekin226/aquascope) — provenance-focused exploratory interface; interface inspiration only.
- [Streamlit caching documentation](https://docs.streamlit.io/develop/concepts/architecture/caching) — cache-key and session-state design.

## Execution Handoff

The user selected subagent-driven development and authorized the synthetic prior-predictive implementation on 24 November 2026. Execute Tasks 1, 1A, 2, and 3 first; then Tasks 4, 5, and 6; then Tasks 7, 7A, 8, and 9. Use a fresh implementer per task and review between tasks.

Fixture data are authorized for automated smoke tests only. Synthetic outputs must remain labelled `SYNTHETIC — NOT FIELD-VERIFIED`; observed Lucong findings still require the verified census and drainage links.
