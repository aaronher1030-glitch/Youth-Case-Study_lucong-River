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
