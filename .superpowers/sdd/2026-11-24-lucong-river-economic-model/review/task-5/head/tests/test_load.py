from dataclasses import replace
from math import inf, nan
from pathlib import Path

import pytest

from river_model.inputs import Params, Shed, load_census
from river_model.load import compute_load

FIXTURE = Path(__file__).parent / "fixtures" / "census.csv"


def test_unit_conversion_matches_hand_calculation():
    sheds = (Shed("S01", "Santiago", 225, True, "test"),)
    result = compute_load(replace(Params(), eta=1.0), sheds)
    assert result.l0_mpn_day == pytest.approx(691_200_000_000.0)
    assert result.l_gen_mpn_day == pytest.approx(225_000_000_000.0)
    assert result.l_target_mpn_day == pytest.approx(225_000_000_000.0)


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


@pytest.mark.parametrize(
    ("heads", "c0_mpn_100ml", "e_head_day"),
    [
        pytest.param(1000, 16_000.0, 1.0e9, id="clearly-above-one"),
        pytest.param(
            1,
            1_000.0,
            43_200_000_000.0 * (1.0 + 5e-10),
            id="within-former-tolerance-band",
        ),
    ],
)
def test_source_share_above_one_raises_instead_of_capping(
    heads, c0_mpn_100ml, e_head_day
):
    sheds = (Shed("S01", "Santiago", heads, True, "test"),)
    params = replace(
        Params(), c0_mpn_100ml=c0_mpn_100ml, e_head_day=e_head_day
    )
    with pytest.raises(ValueError, match="source share exceeds 1"):
        compute_load(params, sheds)


def test_threshold_identity_for_8000():
    sheds = (Shed("S01", "Santiago", 225, True, "test"),)
    result = compute_load(replace(Params(), q_m3_s=0.02), sheds)
    assert result.c_end_mpn_100ml == pytest.approx(4836.263020833334)
    assert result.reduction_fraction >= 0.5
    assert result.c_end_mpn_100ml <= 8000
    assert result.c_end_mpn_100ml == pytest.approx(
        result.c0_mpn_100ml * (1 - result.r * result.c)
    )
    assert result.reduction_fraction == pytest.approx(result.r * result.c)


def test_annual_prevention_matches_independent_hand_calculation():
    sheds = (Shed("S01", "Santiago", 1, True, "test"),)
    params = replace(
        Params(),
        c0_mpn_100ml=1_000.0,
        q_m3_s=0.1,
        e_head_day=1.0e9,
        eta=1.0,
        p_enroll=1.0,
        p_collect=1.0,
        p_retain=1.0,
    )
    result = compute_load(params, sheds)
    # One billion MPN/day prevented for 365 days is 0.365 trillion MPN/year.
    assert result.annual_mpn_prevented_12 == pytest.approx(0.365)


def test_unknown_drainage_is_excluded():
    sheds = load_census(FIXTURE)
    result = compute_load(Params(), sheds)
    assert result.heads == 22


@pytest.mark.parametrize("field", ["c0_mpn_100ml", "q_m3_s"])
@pytest.mark.parametrize("value", [0.0, -1.0, nan, inf, -inf])
def test_invalid_physical_inputs_are_rejected(field, value):
    sheds = (Shed("S01", "Santiago", 1, True, "test"),)
    with pytest.raises(ValueError, match=field):
        compute_load(replace(Params(), **{field: value}), sheds)


@pytest.mark.parametrize("value", [-1.0, nan, inf, -inf])
def test_invalid_head_load_is_rejected(value):
    sheds = (Shed("S01", "Santiago", 1, True, "test"),)
    with pytest.raises(ValueError, match="e_head_day"):
        compute_load(replace(Params(), e_head_day=value), sheds)


@pytest.mark.parametrize(
    "field",
    ["eta", "p_enroll", "p_collect", "p_retain", "source_share_tolerance"],
)
@pytest.mark.parametrize("value", [-0.01, 1.01, nan, inf, -inf])
def test_invalid_factors_probabilities_and_tolerance_are_rejected(field, value):
    sheds = (Shed("S01", "Santiago", 1, True, "test"),)
    with pytest.raises(ValueError, match=field):
        compute_load(replace(Params(), **{field: value}), sheds)


@pytest.mark.parametrize("value", [-1.0, nan, inf, -inf])
def test_invalid_upstream_evidence_is_rejected(value):
    sheds = (Shed("S01", "Santiago", 1, True, "test"),)
    with pytest.raises(ValueError, match="upstream_mpn_100ml"):
        compute_load(replace(Params(), upstream_mpn_100ml=value), sheds)


@pytest.mark.parametrize(
    "field",
    [
        "c0_mpn_100ml",
        "q_m3_s",
        "e_head_day",
        "eta",
        "p_enroll",
        "p_collect",
        "p_retain",
        "source_share_tolerance",
        "upstream_mpn_100ml",
    ],
)
def test_nonnumeric_load_parameters_are_rejected(field):
    sheds = (Shed("S01", "Santiago", 1, True, "test"),)
    with pytest.raises(ValueError, match=field):
        compute_load(replace(Params(), **{field: "not-a-number"}), sheds)


def test_negative_eligible_shed_heads_are_rejected():
    sheds = (Shed("S01", "Santiago", -1, True, "test"),)
    with pytest.raises(ValueError, match="eligible shed heads"):
        compute_load(Params(), sheds)


@pytest.mark.parametrize("heads", [nan, inf, -inf])
def test_nonfinite_eligible_shed_heads_are_rejected(heads):
    sheds = (Shed("S01", "Santiago", heads, True, "test"),)
    with pytest.raises(ValueError, match="eligible shed heads"):
        compute_load(Params(), sheds)


def test_nonnumeric_eligible_shed_heads_are_rejected():
    sheds = (Shed("S01", "Santiago", "not-a-number", True, "test"),)
    with pytest.raises(ValueError, match="eligible shed heads"):
        compute_load(Params(), sheds)


def test_reconciliation_without_upstream_reports_no_contradiction():
    sheds = (Shed("S01", "Santiago", 1, True, "test"),)
    result = compute_load(Params(), sheds)
    assert result.top_down_r is None
    assert result.reconciliation_ok is True


def test_reconciliation_accepts_matching_estimate():
    sheds = (Shed("S01", "Santiago", 1, True, "test"),)
    params = replace(
        Params(),
        c0_mpn_100ml=1_000.0,
        q_m3_s=1.0,
        e_head_day=216_000_000_000.0,
        upstream_mpn_100ml=750.0,
    )
    result = compute_load(params, sheds)
    assert result.r == pytest.approx(0.25)
    assert result.top_down_r == pytest.approx(0.25)
    assert result.reconciliation_ok is True


def test_reconciliation_rejects_mismatching_estimate():
    sheds = (Shed("S01", "Santiago", 1, True, "test"),)
    params = replace(
        Params(),
        c0_mpn_100ml=1_000.0,
        q_m3_s=1.0,
        e_head_day=216_000_000_000.0,
        upstream_mpn_100ml=500.0,
    )
    result = compute_load(params, sheds)
    assert result.top_down_r == pytest.approx(0.5)
    assert result.reconciliation_ok is False


def test_reconciliation_accepts_exact_tolerance_boundary():
    sheds = (Shed("S01", "Santiago", 1, True, "test"),)
    params = replace(
        Params(),
        c0_mpn_100ml=1_000.0,
        q_m3_s=1.0,
        e_head_day=216_000_000_000.0,
        upstream_mpn_100ml=500.0,
        source_share_tolerance=0.25,
    )
    result = compute_load(params, sheds)
    assert result.top_down_r == pytest.approx(0.5)
    assert result.reconciliation_ok is True


def test_reconciliation_preserves_negative_raw_top_down_share():
    sheds = (Shed("S01", "Santiago", 1, True, "test"),)
    params = replace(
        Params(),
        c0_mpn_100ml=1_000.0,
        q_m3_s=1.0,
        e_head_day=216_000_000_000.0,
        upstream_mpn_100ml=1_200.0,
        source_share_tolerance=1.0,
    )
    result = compute_load(params, sheds)
    assert result.top_down_r == pytest.approx(-0.2)
    assert result.reconciliation_ok is False
