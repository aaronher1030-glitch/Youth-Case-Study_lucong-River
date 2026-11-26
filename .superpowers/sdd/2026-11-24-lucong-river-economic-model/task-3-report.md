# Task 3 Report: Process, Hydraulic, Transport, and Land Balances

Date: 2026-11-25
Status: DONE

## Requirements implemented

- Added `river_model/process.py` with the frozen `ProcessResult` dataclass and `compute_process(params: Params, sheds: Sequence[Shed]) -> ProcessResult` interface from the task brief.
- Consumed `Params`, `Shed`, and `eligible_sheds` from `river_model.inputs`.
- Included only sheds whose `drains_to_reach` value is `True`; unknown and false drainage are excluded.
- Implemented the specified manure, washwater, slurry, dry matter, volatile solids, digestion, methane, biogas, LPG-equivalent, nitrogen, land, and weekly tanker-trip calculations.
- Used the brief's zero-input behavior: the dry-matter balance error is `0.0` when dry-matter input is zero, and all flow-derived outputs are zero when there are no eligible heads.
- Added the five required tests verbatim in `tests/test_process.py`.

## TDD evidence

### RED

After writing `tests/test_process.py` and before creating `river_model/process.py`, ran:

```text
python -m pytest tests/test_process.py -v
```

Observed exit code: `2`.

Relevant output:

```text
collecting ... collected 0 items / 1 error
tests\test_process.py:6: in <module>
    from river_model.process import compute_process
E   ModuleNotFoundError: No module named 'river_model.process'
============================== short test summary info ============================
ERROR tests/test_process.py
!!!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
```

This is the expected RED state: the required production module did not exist.

### GREEN

After implementing `river_model/process.py`, ran:

```text
python -m pytest tests/test_process.py -v
```

Observed exit code: `0`.

```text
collecting ... collected 5 items

tests/test_process.py::test_two_shed_hand_calculation PASSED             [ 20%]
tests/test_process.py::test_vs_balance_closes PASSED                     [ 40%]
tests/test_process.py::test_trips_increase_with_slurry PASSED             [ 60%]
tests/test_process.py::test_land_requirement_increases_with_heads PASSED [ 80%]
tests/test_process.py::test_unknown_drainage_is_excluded PASSED          [100%]

============================== 5 passed in 0.25s ===============================
```

## Full-suite verification

Ran the full current suite after focused GREEN:

```text
python -m pytest -v
```

Observed exit code: `0`.

```text
collecting ... collected 95 items
...
tests/test_process.py::test_two_shed_hand_calculation PASSED             [ 89%]
tests/test_process.py::test_vs_balance_closes PASSED                     [ 90%]
tests/test_process.py::test_trips_increase_with_slurry PASSED             [ 91%]
tests/test_process.py::test_land_requirement_increases_with_heads PASSED [ 92%]
tests/test_process.py::test_unknown_drainage_is_excluded PASSED          [ 93%]
tests/test_synthetic.py::test_fixed_seed_is_reproducible PASSED           [ 94%]
tests/test_synthetic.py::test_generated_rows_obey_declared_bounds PASSED [ 95%]
tests/test_synthetic.py::test_every_generated_row_is_labelled_synthetic PASSED [ 96%]
tests/test_synthetic.py::test_synthetic_prior_uses_equal_weights_deterministically PASSED [ 97%]
tests/test_synthetic.py::test_write_and_load_round_trip PASSED           [ 98%]
tests/test_synthetic.py::test_invalid_prior_is_rejected PASSED            [100%]

============================== 95 passed in 3.56s ===============================
```

## Files changed

- Created `C:\Users\Ma Christine\Downloads\Youth Case Study - UP RESEARCH FAIR\river_model\process.py`
- Created `C:\Users\Ma Christine\Downloads\Youth Case Study - UP RESEARCH FAIR\tests\test_process.py`
- Created this report at `C:\Users\Ma Christine\Downloads\Youth Case Study - UP RESEARCH FAIR\.superpowers\sdd\2026-11-24-lucong-river-economic-model\task-3-report.md`

No Git repository was initialized and no commit was created.

## Self-review

- Confirmed all 16 required `ProcessResult` fields, their order, and their types match the brief.
- Confirmed `compute_process` uses `eligible_sheds`, preserving the shared drainage eligibility rule.
- Rechecked the 22-head hand calculation: 44 kg/day manure, 0.484 m3/day washwater, 8.8 kg/day dry matter, 7.04 kg/day volatile solids, and 3.52 kg/day volatile solids destroyed.
- Rechecked the balance identity: `dm_remaining = dm_in - vs_destroyed`, so `vs_destroyed + dm_remaining = dm_in`; the specified balance-error calculation therefore returns zero for positive dry matter and has an explicit zero-input branch.
- Rechecked methane/biogas/LPG conversion units, annual nitrogen-to-land conversion, and seven-day slurry-to-tanker-trip conversion.
- Confirmed empty or entirely ineligible input produces zero heads and zero flow-derived requirements without division by zero.
- Retained the brief's `from dataclasses import replace` test import verbatim even though it is unused; this has no functional effect.
- No implementation deviations, unresolved test failures, or functional concerns were found.

## Concerns

None.

## Fix round 1

Date: 2026-11-25
Status: DONE

### Changes

- Added independent literal expectations for all 16 `ProcessResult` fields using the exact three-head case in the fix brief.
- Added all-output zero tests for an empty eligible set and for valid zero quantity, fraction, and head boundaries, plus a unit-fraction boundary test.
- Added parameterized rejection tests for negative quantities, non-finite values in every process parameter used, out-of-range fractions, nonpositive denominators and energy/uptake values, nonnumeric process parameters, and invalid eligible-shed heads. Errors identify the parameter; shed-head errors also identify the shed.
- Added explicit zero-eligible-head tests for all four denominators so validation cannot depend on data volume.
- Added start-of-`compute_process` validation for every process parameter used and every eligible shed's heads. Nonnumeric and boolean values are rejected as `ValueError`; valid zero and unit boundaries remain accepted.
- Preserved the `ProcessResult` and `compute_process` interfaces and every valid-input formula. The `replace` import is now used by the tests and was retained.

### TDD evidence

Tests were added before production changes.

#### RED

Command:

```text
python -m pytest tests/test_process.py -q
```

Observed exit code: `1`.

Relevant output:

```text
.........FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF [ 93%]
FFFFF                                                                    [100%]
E       Failed: DID NOT RAISE <class 'ValueError'>
E       ZeroDivisionError: float division by zero
E       TypeError: unsupported operand type(s) for /: 'str' and 'float'
E       TypeError: can't multiply sequence by non-int of type 'float'
E       TypeError: unsupported operand type(s) for +: 'int' and 'str'
============================== 68 failed, 9 passed in 6.89s ==============================
```

The nine passing tests were the independent hand calculation, zero/boundary acceptance, and retained behavior tests. The 68 failures demonstrated missing validation, leaked arithmetic exceptions, and denominator validation absent when no heads were eligible.

#### GREEN

After adding validation without changing the formulas, command:

```text
python -m pytest tests/test_process.py -q
```

Observed exit code: `0`.

Relevant output:

```text
........................................................................ [ 93%]
.....                                                                    [100%]
77 passed in 0.54s
```

### Full-suite verification

Ran the full current suite once after focused GREEN:

```text
python -m pytest -v
```

Observed exit code: `0`.

Relevant output:

```text
collecting ... collected 167 items
tests/test_process.py::test_independent_hand_calculation_for_all_outputs PASSED [ 50%]
tests/test_process.py::test_empty_eligible_set_has_all_zero_outputs PASSED     [ 51%]
...
tests/test_process.py::test_rejects_invalid_denominators_without_eligible_heads[tanker_m3-0.0] PASSED [ 95%]
tests/test_synthetic.py::test_write_and_load_round_trip PASSED           [ 99%]
tests/test_synthetic.py::test_invalid_prior_is_rejected PASSED          [100%]

============================== 167 passed in 2.76s ===============================
```

### Files changed

- `C:\Users\Ma Christine\Downloads\Youth Case Study - UP RESEARCH FAIR\river_model\process.py`
- `C:\Users\Ma Christine\Downloads\Youth Case Study - UP RESEARCH FAIR\tests\test_process.py`
- `C:\Users\Ma Christine\Downloads\Youth Case Study - UP RESEARCH FAIR\.superpowers\sdd\2026-11-24-lucong-river-economic-model\task-3-report.md`

### Self-review

- Reviewed both production and test diffs against the Task 3 review snapshots.
- Confirmed validation runs before head summation, arithmetic, and division, and covers all 12 process parameters used by the calculation.
- Confirmed the four denominators are validated even for an empty eligible set.
- Confirmed eligible-shed heads must be finite numeric values and nonnegative; nonnumeric and boolean heads raise shed-specific `ValueError`.
- Confirmed no invalid input is clamped, coerced to zero, or silently accepted.
- Confirmed all formula lines after validation are unchanged, including the zero-dry-matter balance branch.
- Rechecked the exact hand case independently: 12 kg/day manure, 0.03 m3/day wash, 0.042 m3/day slurry, 3 kg/day DM, 2.4 kg/day VS, 1.2 kg/day VS destroyed and remaining, 1.8 kg/day DM remaining, 0.48 m3/day methane, 0.8 m3/day biogas, 0.32 kg/day LPG, 0.09 kg/day N, 0.3285 ha land, 0.098 trips/week, and zero balance error.
- No Git repository was initialized, no subagents were dispatched, and no commit was created.

### Concerns

None.
