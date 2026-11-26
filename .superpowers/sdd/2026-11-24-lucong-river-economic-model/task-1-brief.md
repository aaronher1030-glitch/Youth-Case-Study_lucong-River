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

