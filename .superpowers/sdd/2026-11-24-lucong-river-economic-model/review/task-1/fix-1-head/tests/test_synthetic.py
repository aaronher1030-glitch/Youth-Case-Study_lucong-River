from collections import Counter
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
    assert all(shed.source == "synthetic" for shed in sheds)
    assert all(shed.shed_id.startswith("SYN-0003-") for shed in sheds)


def test_synthetic_prior_uses_equal_weights_deterministically():
    n_scenarios = 200
    sheds_per_scenario = 200
    spec = SyntheticSpec(sheds_low=sheds_per_scenario, sheds_high=sheds_per_scenario)
    scenarios = [
        generate_synthetic_census(spec, scenario_id, seed=2025 + scenario_id)
        for scenario_id in range(1, n_scenarios + 1)
    ]

    selected_levels = Counter(
        min(
            spec.connection_levels,
            key=lambda level: abs(sum(shed.drains_to_reach for shed in sheds) / len(sheds) - level),
        )
        for sheds in scenarios
    )
    expected_scenarios = n_scenarios / len(spec.connection_levels)
    connection_chi_square = sum(
        (selected_levels[level] - expected_scenarios) ** 2 / expected_scenarios
        for level in spec.connection_levels
    )
    # 200 fixed-seed draws give ample power; chi-square(df=4) < 20 has p < 0.001.
    assert set(selected_levels) == set(spec.connection_levels)
    assert connection_chi_square < 20.0

    barangay_counts = Counter(shed.barangay for sheds in scenarios for shed in sheds)
    total_sheds = n_scenarios * sheds_per_scenario
    expected_barangays = total_sheds / len(spec.barangays)
    barangay_chi_square = sum(
        (barangay_counts[barangay] - expected_barangays) ** 2 / expected_barangays
        for barangay in spec.barangays
    )
    # 40,000 fixed-seed assignments give ample power; chi-square(df=1) < 20 has p < 0.001.
    assert set(barangay_counts) == set(spec.barangays)
    assert barangay_chi_square < 20.0


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
