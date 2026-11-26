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
