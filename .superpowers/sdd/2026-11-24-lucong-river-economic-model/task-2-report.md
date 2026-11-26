# Task 2 Report: River Load, Capture Chain, and Source Reconciliation

## Status

DONE

## Requirements and implementation

Implemented the Task 2 brief verbatim for its public interfaces, parameter values, formulas, and seven required tests.

- Added `LoadResult` as a frozen dataclass with all 12 specified fields.
- Added `compute_load(params: Params, sheds: Sequence[Shed]) -> LoadResult`.
- Reused `eligible_sheds` from `river_model.inputs`, so only sheds with `drains_to_reach is True` contribute heads.
- Calculated daily generated load, ambient river load, captured target load, bottom-up source share, and capture-chain reduction.
- Preserved the specified `1e-9` source-share tolerance and raised `ValueError` rather than capping a source share above one.
- Calculated final concentration and annual MPN prevented in trillions.
- Added optional top-down source-share reconciliation against `upstream_mpn_100ml` using `source_share_tolerance`.
- Omitted the brief implementation's unused `math` import; no interface or behavior changed.

## Files changed

- Created `C:\Users\Ma Christine\Downloads\Youth Case Study - UP RESEARCH FAIR\river_model\load.py`
- Created `C:\Users\Ma Christine\Downloads\Youth Case Study - UP RESEARCH FAIR\tests\test_load.py`
- Created this report at `C:\Users\Ma Christine\Downloads\Youth Case Study - UP RESEARCH FAIR\.superpowers\sdd\2026-11-24-lucong-river-economic-model\task-2-report.md`

Existing Task 1/1A files were not modified. The workspace is not a Git repository; no Git repository or commits were created.

## TDD evidence

### RED

Created the seven tests from Step 1 before creating the production module, then ran:

```text
python -m pytest tests/test_load.py -v
```

Result: exit code 2; pytest collected 0 tests and stopped during collection with the expected missing-module error:

```text
E   ModuleNotFoundError: No module named 'river_model.load'
ERROR tests/test_load.py
1 error in 3.60s
```

This matches the brief's expected RED condition that `river_model.load` does not exist.

### GREEN

After adding the production module, reran the same command:

```text
python -m pytest tests/test_load.py -v
```

Result: exit code 0; all 7 tests passed in 0.47s:

```text
test_unit_conversion_matches_hand_calculation PASSED
test_zero_enrollment_returns_baseline PASSED
test_no_confirmed_sheds_means_no_reduction PASSED
test_capture_monotonicity PASSED
test_source_share_above_one_raises_instead_of_capping PASSED
test_threshold_identity_for_8000 PASSED
test_unknown_drainage_is_excluded PASSED
7 passed in 0.47s
```

## Threshold verification

Ran the brief's low-flow numerical check, augmented with its two required assertions:

```text
python -c "from river_model.inputs import Params; from river_model.load import compute_load; from dataclasses import replace; from river_model.inputs import Shed; r=compute_load(replace(Params(), q_m3_s=0.02), [Shed('S','S',225,True,'test')]); print(r.r, r.c, r.c_end_mpn_100ml); assert r.r * r.c >= 0.5; assert r.c_end_mpn_100ml <= 8000"
```

Output and result:

```text
0.8138020833333334 0.8573749999999999 4836.263020833334
```

Exit code 0. The reduction fraction is approximately 0.697748566, which is at least 0.5, and final concentration is below 8,000 MPN/100 mL.

## Supplemental reconciliation verification

The required seven tests do not directly exercise the optional upstream reconciliation branch, so a supplemental command checked both matching and mismatching estimates using the 22-head census fixture:

```text
bottom_up_r 0.031828703703703706
matching 0.03182870370370369 True
mismatch 0.5 False
```

Exit code 0. A matching upstream concentration of 15,490.74074074074 MPN/100 mL reconciles with the bottom-up source share; an upstream concentration of 8,000 MPN/100 mL produces a top-down share of 0.5 and correctly fails the default 0.10 tolerance.

An initial supplemental check used an incorrect hand-entered matching concentration and an alleged mismatch still inside tolerance. It failed its assertion, not the implementation. Correcting those independent input values produced the passing evidence above; no production code was changed in response.

## Full test suite

Ran the full current suite after implementation:

```text
python -m pytest -v
```

Result: exit code 0; 26 passed in 6.02s, with no failures, errors, or warnings.

- 13 existing input tests passed.
- 7 new load tests passed.
- 6 existing synthetic-data tests passed.

## Self-review

- **Interface:** `LoadResult` field names, order, and types match the brief; `compute_load` accepts `Params` and `Sequence[Shed]` and returns `LoadResult`.
- **Eligibility:** Unknown and false drainage values are excluded through the existing `eligible_sheds` helper. The census fixture confirms 10 + 12 = 22 eligible heads while excluding the unknown 8-head shed.
- **Units:** Ambient load converts m3/s to m3/day with 86,400 and to 100 mL volumes with 10,000. The hand-calculated test confirms 691.2 billion MPN/day ambient load and 225 billion MPN/day generated load for 225 heads.
- **Capture chain:** Capture is the product of enrollment, collection, and retention probabilities; reduction is bottom-up source share times capture; final concentration preserves the specified threshold identity.
- **Bounds:** Zero enrollment returns baseline concentration; no eligible sheds yields zero source share and zero annual prevention; higher collection monotonically lowers final concentration; source shares above one raise rather than cap.
- **Reconciliation:** Without an upstream measurement, `top_down_r` is `None` and `reconciliation_ok` is `True`. With a measurement, top-down share is clamped at zero and compared with the bottom-up share using the configured tolerance. Supplemental checks covered both true and false outcomes.
- **Mutation check:** Realistic regressions in conversion factors, eligibility, capture multiplication, source-share validation, or concentration identity are caught by the required tests. The optional reconciliation branch was checked separately by command because the prescribed test file has no dedicated reconciliation cases.
- **Scope:** No unrelated source files, dependencies, documentation, or Git state were changed.

## Concerns

No blocking implementation concerns. The model has no supplied upstream water-quality measurement by default, so empirical source reconciliation remains pending field data; this is an existing input-data limitation, not a Task 2 implementation defect. Optional reconciliation also lacks a dedicated automated regression test because the brief prescribes exactly seven tests; both outcomes were verified by the supplemental command above.

## Fix round 1

Status: DONE. This section supersedes the earlier statements about the `1e-9` acceptance band, top-down clamping, and supplemental-only reconciliation coverage.

### Production changes

- `C:\Users\Ma Christine\Downloads\Youth Case Study - UP RESEARCH FAIR\river_model\load.py`
  - Enforced finite numeric inputs before load arithmetic, including nonnumeric values raising parameter-specific `ValueError` rather than being coerced or leaking `TypeError`.
  - Enforced positive `c0_mpn_100ml` and `q_m3_s`, nonnegative `e_head_day`, optional upstream evidence and eligible shed heads, and `[0, 1]` bounds for `eta`, all capture probabilities, and `source_share_tolerance`.
  - Changed bottom-up validation to strict `r > 1.0` and added the required negative-source-share error; removed the former acceptance band and `max(0.0, r)` clamp.
  - Preserved raw top-down share, including negative values, and forced `reconciliation_ok=False` for a negative raw share even when the configured tolerance would otherwise cover the difference.

### Test changes

- `C:\Users\Ma Christine\Downloads\Youth Case Study - UP RESEARCH FAIR\tests\test_load.py`
  - Removed the unused `eligible_sheds` import.
  - Added independent target-load, threshold endpoint, reduction, and nonzero annual-prevention expectations.
  - Added a source share `5e-10` above one inside the former acceptance band.
  - Added parameterized invalid physical, factor, probability, tolerance, upstream, and eligible-head cases, including non-finite and nonnumeric values.
  - Added automated reconciliation coverage for missing, matching, mismatching, exact-boundary, and upstream-greater-than-C0 evidence.

### TDD evidence

RED for the required behavior changes was captured before production edits with:

```text
python -m pytest tests/test_load.py -q --tb=short
```

Exit code 1: `46 failed, 12 passed in 2.79s`. Relevant failures included the within-former-band source share not raising, `ZeroDivisionError` for zero concentration/flow, missing validation for negative/non-finite inputs, an infinity reaching the source-share error instead of the parameter-specific error, and the negative raw top-down share being returned as `0.0`.

Additional RED checks captured the finite/nonnumeric eligible-head boundary and nonnumeric parameter handling:

```text
python -m pytest tests/test_load.py -q --tb=short -k nonfinite_eligible_shed_heads
python -m pytest tests/test_load.py -q --tb=short -k nonnumeric
```

Relevant output:

```text
3 failed, 58 deselected in 0.77s
10 failed, 61 deselected in 1.51s
TypeError: must be real number, not str
```

After the minimal production changes, the final focused GREEN command was:

```text
python -m pytest tests/test_load.py -q --tb=short
```

Exit code 0: `71 passed in 0.95s`, with no failures, errors, or warnings.

### Full suite

Ran the full current suite once after the final focused verification:

```text
python -m pytest -q
```

Exit code 0: `90 passed in 3.64s`, with no failures, errors, or warnings.

### Self-review

- Reviewed the actual `diff -u` output for both changed source/test files against the Task 2 review snapshots; only the intended validation, source-share, reconciliation, and regression-test changes are present.
- Searched `river_model/load.py` for `max(0.0)`, `1e-9`, and other clamp patterns; no matches remain.
- Confirmed strict above-one handling, the explicit negative bottom-up error, raw negative top-down diagnostics, inclusive tolerance comparison, and unchanged missing-upstream interface behavior.
- Confirmed the negative top-down regression uses tolerance `1.0`, so it protects the mandatory negative-share rejection branch rather than merely failing the numerical difference.
- Confirmed hand-derived arithmetic assertions and all requested reconciliation cases are automated.
- No Git repository was initialized and no commits were created.

### Concerns

No blocking concerns. Upstream field evidence remains unavailable by default, so empirical reconciliation still depends on future measurements. Downstream consumers must also be prepared to display a negative `top_down_r` as incompatible evidence rather than interpreting it as a physical source fraction.
