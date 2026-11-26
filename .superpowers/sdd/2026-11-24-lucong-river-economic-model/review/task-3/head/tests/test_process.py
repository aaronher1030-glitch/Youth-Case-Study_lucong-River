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
