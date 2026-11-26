# Task 4 Report: Twelve-Month Cash, Lifecycle Cost, and Unit Economics

**Date:** 2026-11-25
**Status:** DONE_WITH_CONCERNS
**Workspace:** `C:\Users\Ma Christine\Downloads\Youth Case Study - UP RESEARCH FAIR`
**Repository:** Not a Git repository; no Git initialization or commits were performed.

## Summary

Implemented the prescribed economic interface in `river_model/economics.py` and added the five required tests in `tests/test_economics.py`. The module computes capital expenditure, prorated 12-month operating expenditure, contingency, 12-month cash requirement, discounted lifecycle cost (NPC), equivalent annual cost (EAC), zero revenue credit, and per-shed, per-MPN12, per-kg-VS, and per-head unit costs. The frozen `CostInputs` and `CostResult` dataclasses and `compute_costs(params: Params, inputs: CostInputs) -> CostResult` signature match the brief verbatim.

## Files Changed

Created:

- `C:\Users\Ma Christine\Downloads\Youth Case Study - UP RESEARCH FAIR\river_model\economics.py`
- `C:\Users\Ma Christine\Downloads\Youth Case Study - UP RESEARCH FAIR\tests\test_economics.py`

Report:

- `C:\Users\Ma Christine\Downloads\Youth Case Study - UP RESEARCH FAIR\.superpowers\sdd\2026-11-24-lucong-river-economic-model\task-4-report.md`

No existing source, test, configuration, or documentation files were modified.

## TDD Evidence

### RED — required failing test run

The tests were written before the production module. From the workspace root, the exact required command was run:

```text
python -m pytest tests/test_economics.py -v
```

Observed result: exit code 2; pytest collected 0 items and stopped with 1 collection error. The relevant error was:

```text
tests\test_economics.py:5: in <module>
    from river_model.economics import CostInputs, compute_costs
E   ModuleNotFoundError: No module named 'river_model.economics'
```

This is the expected RED failure: the tested module did not exist. No production implementation was written until this failure was observed.

### GREEN — focused tests

After implementing `river_model/economics.py`, the exact required focused command was run:

```text
python -m pytest tests/test_economics.py -v
```

Observed result: exit code 0; all five tests passed in 0.38 seconds:

```text
tests/test_economics.py::test_capex_line_items_match_hand_calculation PASSED [ 20%]
tests/test_economics.py::test_cash_includes_contingency PASSED           [ 40%]
tests/test_economics.py::test_zero_discount_uses_straight_line_annualization PASSED [ 60%]
tests/test_economics.py::test_zero_load_prevented_returns_infinite_unit_cost PASSED [ 80%]
tests/test_economics.py::test_base_case_has_zero_revenue_credit PASSED    [100%]

5 passed in 0.38s
```

### Full-suite verification

After focused GREEN and before writing this report, the full current suite was run exactly once:

```text
python -m pytest -v
```

Observed result: exit code 0; 172 tests collected and all 172 passed in 7.10 seconds, with no failures, errors, or warnings reported.

```text
collected 172 items
...
172 passed in 7.10s
```

## Requirements Checklist

- [x] Created `tests/test_economics.py` with the five tests specified in the brief.
- [x] Wrote the tests before implementation and captured the expected missing-module RED failure.
- [x] Created `river_model/economics.py` using the specified `CostInputs` fields, `CostResult` fields, and `compute_costs` interface.
- [x] Included all eleven capital line items with the specified module, tanker, and cart multipliers.
- [x] Prorated annual staff, sampling, transport, and administration costs by `pilot_months / 12.0`; maintenance is based on CAPEX.
- [x] Applied contingency to the sum of CAPEX and 12-month OPEX for `cash_12m`.
- [x] Calculated NPC using discounted annual OPEX and the specified replacement in `replacement_year`.
- [x] Used straight-line annualization at zero discount and the specified capital-recovery factor otherwise.
- [x] Returned infinite unit cost for nonpositive annual MPN prevention or VS diversion, and zero revenue credit.
- [x] Passed all five focused tests.
- [x] Ran the full current suite once before reporting.
- [x] Performed self-review and wrote this report.

## Hand-Check Reference

For the brief's base-case input (`15` sheds, `225` heads, `3` modules, `1` tanker, `2` carts, `20` trips/week):

- CAPEX = PHP 6,440,000.
- 12-month OPEX = PHP 2,730,000: PHP 1,140,000 staff + PHP 480,000 sampling + PHP 322,000 maintenance + PHP 728,000 transport + PHP 60,000 administration.
- Contingency = PHP 917,000 at 10% of PHP 9,170,000.
- 12-month cash = PHP 10,087,000.
- Scheduled replacement = PHP 1,610,000, which is 25% of CAPEX.

These checks agree with the formulas exercised by the focused tests.

## Self-Review

- The production code follows the brief's implementation and consumes only the tested `Params` interface from `river_model.inputs.py`; no changes to Tasks 1/1A–3 were needed.
- Dataclass field order, names, types, and frozen behavior match the specified public interface.
- The CAPEX hand-calculation test protects all capital multipliers and fixed line items. The contingency test protects application of contingency to both CAPEX and OPEX. The zero-discount test protects the straight-line EAC branch. The zero-prevention test protects the required infinite MPN12 unit cost. The revenue test protects the base-case zero credit.
- No revenue adjustment is subtracted from EAC or the unit costs, consistent with the prescribed zero-credit implementation.
- No subagents were dispatched, no Git commands creating a repository or commit were used, and no unrelated files were changed.

### Concerns / Limitations

1. The brief prescribes only five tests. They do not independently assert numeric values for 12-month OPEX, discounted NPC, replacement timing, the nonzero-discount CRF, positive per-shed/per-MPN12/per-kg-VS/per-head unit costs, or the zero-VS branch. These paths are implemented as specified but have limited direct regression coverage.
2. Per the prescribed implementation, `sheds` and `heads` are used as unguarded denominators. Zero values raise `ZeroDivisionError` rather than returning infinity or raising a domain-specific error; the brief specifies neither validation nor alternate behavior for these inputs.
3. The brief's `import math` is unused. It was retained to keep the implementation faithful to the provided source and has no runtime effect.

These concerns do not prevent the required Task 4 interface or test criteria from being satisfied.

## Fix round 1

**Date:** 2026-11-25  
**Status:** DONE

### Summary

Added pre-arithmetic validation for every `CostInputs` field and every CAPEX, OPEX, discount, lifecycle, replacement, and pilot-duration parameter used by `compute_costs`. Invalid counts, rates, fractions, durations, booleans, nonnumeric values, negative values, and non-finite values now raise field- or parameter-specific `ValueError` instances. Valid zero optional counts, zero trips, zero prevention, and zero VS diversion remain accepted; zero prevention and zero diversion still return infinite unit costs.

Replaced the cancellation-prone nonzero-discount CRF with the required `math.log1p`/`math.expm1` expression. The zero-discount straight-line branch, frozen dataclasses, field order, and `compute_costs(params: Params, inputs: CostInputs) -> CostResult` public interface are unchanged.

Retained the five original tests, strengthened the cash test with literal values, and expanded `tests/test_economics.py` from 5 to 285 collected cases. Added independent literal lifecycle and unit-cost assertions, replacement-timing coverage, zero-VS coverage, tiny-positive-discount coverage, independent tanker/cart CAPEX cases, invalid-boundary matrices, and valid-boundary cases.

### Files Changed

Modified:

- `C:\Users\Ma Christine\Downloads\Youth Case Study - UP RESEARCH FAIR\river_model\economics.py`
- `C:\Users\Ma Christine\Downloads\Youth Case Study - UP RESEARCH FAIR\tests\test_economics.py`

Appended:

- `C:\Users\Ma Christine\Downloads\Youth Case Study - UP RESEARCH FAIR\.superpowers\sdd\2026-11-24-lucong-river-economic-model\task-4-report.md`

No other source, test, configuration, or documentation files were changed.

### TDD Evidence

#### RED — tests written before production edits

From the workspace root, the exact focused command was run before editing `river_model/economics.py`:

```text
python -m pytest tests/test_economics.py -q --tb=short
```

Observed result: exit code 1; 267 failed and 18 passed in 7.85 seconds. Relevant failures were:

```text
test_tiny_positive_discount_uses_stable_annualization
E   ZeroDivisionError: float division by zero

test_positive_integer_inputs_reject_invalid_boundaries[0-sheds]
E   ZeroDivisionError: float division by zero

test_positive_integer_inputs_reject_invalid_boundaries[-1-sheds]
E   Failed: DID NOT RAISE <class 'ValueError'>

267 failed, 18 passed in 7.85s
```

The literal default-value, replacement-timing, positive unit-cost, zero-VS, and independent CAPEX-multiplier cases already passed, confirming that the new tests preserved the valid-default behavior. The validation matrices and tiny-discount case failed for the expected missing-validation and CRF-cancellation reasons. No production edits were made before this RED result was captured.

#### GREEN — focused economics tests

After the minimal production changes, the exact focused command was run again:

```text
python -m pytest tests/test_economics.py -q --tb=short
```

Observed result: exit code 0:

```text
........................................................................ [ 25%]
........................................................................ [ 50%]
........................................................................ [ 75%]
.....................................................................    [100%]
285 passed in 0.91s
```

After diff review and a formatting-only adjustment, the same focused command was rerun for fresh verification:

```text
285 passed in 2.93s
```

### Full-Suite Verification

After focused GREEN and self-review, the full current suite was run exactly once:

```text
python -m pytest -v
```

Observed result: exit code 0; 452 items collected and all 452 passed in 2.62 seconds. No failures, errors, or warnings were reported.

```text
collected 452 items
...
452 passed in 2.62s
```

### Self-Review

- Reviewed the actual changes against the preserved pre-fix snapshots with `diff -u` for both `river_model/economics.py` and `tests/test_economics.py`. The diff contains only the requested validation, stable CRF, test strengthening, and regression coverage.
- Confirmed validation executes before CAPEX, OPEX, contingency, NPC, EAC, or unit-cost arithmetic. All eleven CAPEX parameters, all OPEX parameters, the three bounded fractions, discount, asset life, replacement year, and pilot months used by the model are covered.
- Confirmed booleans and nonnumeric values are rejected with the offending field or parameter name in each `ValueError`. Zero sheds/heads now raise `ValueError` instead of `ZeroDivisionError`.
- Compared current defaults with the original snapshot loaded independently. CAPEX (`6_440_000.0`), 12-month OPEX (`2_730_000.0`), contingency (`917_000.0`), 12-month cash (`10_087_000.0`), NPC (`26_771_261.16633448`), and revenue credit (`0.0`) are exactly unchanged.
- The mandated stable CRF changes default EAC only from `3_989_707.3633946963` to `3_989_707.363394698` (delta `1.862645149230957e-09`). Derived default unit costs likewise differ only at machine precision, and all literal assertions pass at `rel=1e-12`.
- Confirmed `discount=1e-16` returns finite EAC `3_626_700.0000000014`, approximately NPC divided by the 10-year asset life (`3_626_700.0`).
- Confirmed the zero-discount branch is unchanged and zero prevention/zero VS diversion still return `float("inf")` unit costs.
- Confirmed independent tanker and cart changes produce literal CAPEX values `7_890_000.0` and `6_620_000.0`, respectively, while the other count remains at its default.
- All three concerns recorded in the original report are addressed: lifecycle/unit economics now have direct literal coverage, zero shed/head denominators are validated, and `math` is used by the stable CRF.
- No subagents were dispatched, no Git repository was initialized, and no commits were created.

### Concerns / Limitations

No blocking concerns remain. The only observed valid-default differences are machine-precision rounding changes caused by the required numerically stable CRF; they are far below the literal regression tolerances and do not change the economic results.
