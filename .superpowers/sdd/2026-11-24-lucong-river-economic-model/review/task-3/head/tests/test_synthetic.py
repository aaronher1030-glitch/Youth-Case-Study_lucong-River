from dataclasses import replace
from pathlib import Path

import numpy as np
import pytest

from river_model import synthetic
from river_model.inputs import load_census
from river_model.synthetic import (
    SyntheticSpec,
    generate_synthetic_census,
    write_census,
)


class _RecordingRNG:
    def __init__(self, rng):
        self._rng = rng
        self.choice_calls = []

    def integers(self, *args, **kwargs):
        return self._rng.integers(*args, **kwargs)

    def triangular(self, *args, **kwargs):
        return self._rng.triangular(*args, **kwargs)

    def random(self, *args, **kwargs):
        return self._rng.random(*args, **kwargs)

    def choice(self, *args, **kwargs):
        candidates = args[0] if args else kwargs["a"]
        self.choice_calls.append((tuple(candidates), args[1:], kwargs))
        return self._rng.choice(*args, **kwargs)


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


def test_synthetic_prior_uses_equal_weights_deterministically(monkeypatch):
    spec = SyntheticSpec(sheds_low=1, sheds_high=1)
    recording_rng = _RecordingRNG(np.random.default_rng(2026))
    monkeypatch.setattr(synthetic.np.random, "default_rng", lambda _seed: recording_rng)

    sheds = generate_synthetic_census(spec, scenario_id=1, seed=2026)

    assert len(sheds) == 1
    assert len(recording_rng.choice_calls) == 2
    (connection_levels, connection_args, connection_kwargs), (
        barangays,
        barangay_args,
        barangay_kwargs,
    ) = recording_rng.choice_calls
    assert connection_levels == spec.connection_levels
    assert barangays == spec.barangays
    for positional_args, keyword_args in (
        (connection_args, connection_kwargs),
        (barangay_args, barangay_kwargs),
    ):
        # p is the fourth choice parameter, after a, size, and replace.
        assert len(positional_args) < 3
        assert "p" not in keyword_args


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
