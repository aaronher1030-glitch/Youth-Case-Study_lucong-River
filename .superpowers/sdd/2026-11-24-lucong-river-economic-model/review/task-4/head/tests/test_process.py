from dataclasses import replace

import pytest

from river_model.inputs import Params, Shed
from river_model.process import ProcessResult, compute_process


_PROCESS_PARAMETERS = (
    "manure_kg_head_day",
    "washwater_l_head_day",
    "dm_frac",
    "vs_frac_dm",
    "vs_destroyed",
    "ch4_yield",
    "ch4_frac",
    "ch4_mj_m3",
    "lpg_mj_kg",
    "n_frac_dm",
    "rice_n_kg_ha",
    "tanker_m3",
)


def test_independent_hand_calculation_for_all_outputs():
    sheds = (Shed("S01", "Santiago", 3, True, "test"),)
    params = Params(
        manure_kg_head_day=4.0,
        washwater_l_head_day=10.0,
        dm_frac=0.25,
        vs_frac_dm=0.80,
        vs_destroyed=0.50,
        ch4_yield=0.40,
        ch4_frac=0.60,
        ch4_mj_m3=30.0,
        lpg_mj_kg=45.0,
        n_frac_dm=0.05,
        rice_n_kg_ha=100.0,
        tanker_m3=3.0,
    )

    result = compute_process(params, sheds)

    assert result.heads == 3
    assert result.manure_kg_day == pytest.approx(12.0)
    assert result.wash_m3_day == pytest.approx(0.03)
    assert result.slurry_m3_day == pytest.approx(0.042)
    assert result.dm_in_kg_day == pytest.approx(3.0)
    assert result.vs_in_kg_day == pytest.approx(2.4)
    assert result.vs_destroyed_kg_day == pytest.approx(1.2)
    assert result.vs_remaining_kg_day == pytest.approx(1.2)
    assert result.dm_remaining_kg_day == pytest.approx(1.8)
    assert result.ch4_m3_day == pytest.approx(0.48)
    assert result.biogas_m3_day == pytest.approx(0.8)
    assert result.lpg_kg_day == pytest.approx(0.32)
    assert result.nutrient_n_kg_day == pytest.approx(0.09)
    assert result.land_ha_required == pytest.approx(0.3285)
    assert result.trips_week == pytest.approx(0.098)
    assert result.vs_balance_error_pct == pytest.approx(0.0)


def test_empty_eligible_set_has_all_zero_outputs():
    result = compute_process(Params(), ())

    assert result == ProcessResult(
        heads=0,
        manure_kg_day=0.0,
        wash_m3_day=0.0,
        slurry_m3_day=0.0,
        dm_in_kg_day=0.0,
        vs_in_kg_day=0.0,
        vs_destroyed_kg_day=0.0,
        vs_remaining_kg_day=0.0,
        dm_remaining_kg_day=0.0,
        vs_balance_error_pct=0.0,
        ch4_m3_day=0.0,
        biogas_m3_day=0.0,
        lpg_kg_day=0.0,
        nutrient_n_kg_day=0.0,
        land_ha_required=0.0,
        trips_week=0.0,
    )


def test_zero_quantity_fraction_and_head_boundaries_are_valid():
    params = Params(
        manure_kg_head_day=0.0,
        washwater_l_head_day=0.0,
        dm_frac=0.0,
        vs_frac_dm=0.0,
        vs_destroyed=0.0,
        ch4_yield=0.0,
        n_frac_dm=0.0,
    )
    sheds = (Shed("S01", "Santiago", 0, True, "test"),)

    assert compute_process(params, sheds) == ProcessResult(
        heads=0,
        manure_kg_day=0.0,
        wash_m3_day=0.0,
        slurry_m3_day=0.0,
        dm_in_kg_day=0.0,
        vs_in_kg_day=0.0,
        vs_destroyed_kg_day=0.0,
        vs_remaining_kg_day=0.0,
        dm_remaining_kg_day=0.0,
        vs_balance_error_pct=0.0,
        ch4_m3_day=0.0,
        biogas_m3_day=0.0,
        lpg_kg_day=0.0,
        nutrient_n_kg_day=0.0,
        land_ha_required=0.0,
        trips_week=0.0,
    )


def test_unit_fraction_boundaries_are_valid():
    params = Params(
        dm_frac=1.0,
        vs_frac_dm=1.0,
        vs_destroyed=1.0,
        ch4_frac=1.0,
        n_frac_dm=1.0,
    )
    sheds = (Shed("S01", "Santiago", 3, True, "test"),)

    result = compute_process(params, sheds)

    assert result.vs_destroyed_kg_day == result.vs_in_kg_day
    assert result.biogas_m3_day == result.ch4_m3_day


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


@pytest.mark.parametrize(
    ("parameter", "value"),
    [
        ("manure_kg_head_day", -1.0),
        ("washwater_l_head_day", -1.0),
        ("ch4_yield", -1.0),
    ],
)
def test_rejects_negative_process_quantities(parameter, value):
    sheds = (Shed("S01", "Santiago", 1, True, "test"),)
    with pytest.raises(ValueError, match=parameter):
        compute_process(replace(Params(), **{parameter: value}), sheds)


@pytest.mark.parametrize("parameter", _PROCESS_PARAMETERS)
@pytest.mark.parametrize("value", [float("nan"), float("inf")])
def test_rejects_non_finite_process_parameters(parameter, value):
    sheds = (Shed("S01", "Santiago", 1, True, "test"),)
    with pytest.raises(ValueError, match=parameter):
        compute_process(replace(Params(), **{parameter: value}), sheds)


@pytest.mark.parametrize(
    ("parameter", "value"),
    [
        ("dm_frac", -0.01),
        ("dm_frac", 1.01),
        ("vs_frac_dm", -0.01),
        ("vs_frac_dm", 1.01),
        ("vs_destroyed", -0.01),
        ("vs_destroyed", 1.01),
        ("n_frac_dm", -0.01),
        ("n_frac_dm", 1.01),
        ("ch4_frac", -0.01),
        ("ch4_frac", 0.0),
        ("ch4_frac", 1.01),
    ],
)
def test_rejects_out_of_range_fractions(parameter, value):
    sheds = (Shed("S01", "Santiago", 1, True, "test"),)
    with pytest.raises(ValueError, match=parameter):
        compute_process(replace(Params(), **{parameter: value}), sheds)


@pytest.mark.parametrize(
    ("parameter", "value"),
    [
        ("ch4_mj_m3", 0.0),
        ("ch4_mj_m3", -1.0),
        ("lpg_mj_kg", 0.0),
        ("lpg_mj_kg", -1.0),
        ("rice_n_kg_ha", 0.0),
        ("rice_n_kg_ha", -1.0),
        ("tanker_m3", 0.0),
        ("tanker_m3", -1.0),
    ],
)
def test_rejects_nonpositive_energy_uptake_and_transport_parameters(parameter, value):
    sheds = (Shed("S01", "Santiago", 1, True, "test"),)
    with pytest.raises(ValueError, match=parameter):
        compute_process(replace(Params(), **{parameter: value}), sheds)


@pytest.mark.parametrize("parameter", _PROCESS_PARAMETERS)
def test_rejects_nonnumeric_process_parameters(parameter):
    sheds = (Shed("S01", "Santiago", 1, True, "test"),)
    with pytest.raises(ValueError, match=parameter):
        compute_process(replace(Params(), **{parameter: "invalid"}), sheds)


@pytest.mark.parametrize("heads", [-1, float("nan"), float("inf"), "3", None, True])
def test_rejects_invalid_eligible_shed_heads(heads):
    sheds = (Shed("S01", "Santiago", heads, True, "test"),)
    with pytest.raises(ValueError, match="heads") as error:
        compute_process(Params(), sheds)
    assert "S01" in str(error.value)


@pytest.mark.parametrize(
    ("parameter", "value"),
    [
        ("ch4_frac", 0.0),
        ("lpg_mj_kg", 0.0),
        ("rice_n_kg_ha", 0.0),
        ("tanker_m3", 0.0),
    ],
)
def test_rejects_invalid_denominators_without_eligible_heads(parameter, value):
    with pytest.raises(ValueError, match=parameter):
        compute_process(replace(Params(), **{parameter: value}), ())
