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


@pytest.mark.parametrize(
    ("row", "message"),
    [
        ("S01,,10,true,test\n", "barangay must not be blank"),
        ("S01,   ,10,true,test\n", "barangay must not be blank"),
        ("S01\n", "barangay must not be blank"),
        ("S01,Santiago,10,true,\n", "source must not be blank"),
        ("S01,Santiago,10,true,   \n", "source must not be blank"),
        ("S01,Santiago,10,true\n", "source must not be blank"),
    ],
    ids=[
        "blank-barangay",
        "whitespace-barangay",
        "truncated-barangay",
        "blank-source",
        "whitespace-source",
        "truncated-source",
    ],
)
def test_census_rejects_blank_or_missing_provenance(tmp_path: Path, row: str, message: str):
    path = tmp_path / "bad.csv"
    path.write_text(
        "shed_id,barangay,heads,drains_to_reach,source\n" + row,
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match=message):
        load_census(path)


def test_override_parses_numbers_and_preserves_base_object():
    base = Params()
    changed = apply_overrides(base, {"q_m3_s": "0.08", "land_available_ha": "12.5"})
    assert changed.q_m3_s == 0.08
    assert changed.land_available_ha == 12.5
    assert base.q_m3_s == 0.05
    assert base.land_available_ha is None


def test_override_can_clear_a_populated_optional_parameter():
    base = apply_overrides(Params(), {"upstream_mpn_100ml": "120.0"})
    changed = apply_overrides(base, {"upstream_mpn_100ml": "None"})
    assert changed.upstream_mpn_100ml is None
    assert base.upstream_mpn_100ml == 120.0


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
