# Task 5 Report: Barangay-Cluster Design Enumeration and Alternatives

**Date:** 2026-11-25  
**Status:** DONE_WITH_CONCERNS  
**Workspace:** `C:\Users\Ma Christine\Downloads\Youth Case Study - UP RESEARCH FAIR`  
**Repository:** Not a Git repository; no Git initialization or commits were performed.

## Summary

Implemented the Task 5 public interfaces in `river_model/design.py` and added the eight required tests in `tests/test_design.py`. Design enumeration uses confirmed eligible sheds grouped into non-empty barangay combinations, applies the prescribed module/tanker/day search bounds, computes Task 2–4 load/process/economic results, records all eight deterministic checks and exact rejection messages, omits the probabilistic target from feasibility, and sorts by EAC, cash requirement, then shed coverage. Alternative comparison provides the three prescribed alternatives on the same station-level functional unit while leaving unquoted costs missing.

## Files Changed

Created:

- `C:\Users\Ma Christine\Downloads\Youth Case Study - UP RESEARCH FAIR\river_model\design.py`
- `C:\Users\Ma Christine\Downloads\Youth Case Study - UP RESEARCH FAIR\tests\test_design.py`

Report:

- `C:\Users\Ma Christine\Downloads\Youth Case Study - UP RESEARCH FAIR\.superpowers\sdd\2026-11-24-lucong-river-economic-model\task-5-report.md`

No existing source, test, configuration, or model-input files were modified.

## TDD Evidence

### Cycle 1 RED — enumeration tests before implementation

The six Step 1 tests were written before `river_model/design.py` existed. From the workspace root, the exact required command was run:

```text
python -m pytest tests/test_design.py -v
```

Observed result: exit code 2; pytest collected 0 items and stopped with the expected collection error:

```text
tests\test_design.py:6: in <module>
    from river_model.design import constraint_feasible, enumerate_designs
E   ModuleNotFoundError: No module named 'river_model.design'
```

This is the brief's expected RED condition. No production implementation was written before this failure was observed.

### Cycle 1 GREEN — enumeration implementation

After implementing the enumeration dataclasses and function, the same focused command was run:

```text
python -m pytest tests/test_design.py -v
```

Observed result: exit code 0; all six enumeration tests passed in 0.16 seconds:

```text
test_enumeration_returns_evaluations_and_counts_shed_subsets PASSED
test_enumeration_uses_barangay_service_sets PASSED
test_missing_land_rejects_every_design PASSED
test_budget_constraint_is_never_violated_by_feasible_design PASSED
test_digester_and_tanker_constraints_match_formulas PASSED
test_target_is_not_a_deterministic_constraint PASSED

6 passed in 0.16s
```

### Required candidate inspection

The brief's inspection command was run after enumeration GREEN:

```text
python -c "from pathlib import Path; from dataclasses import replace; from river_model.inputs import Params,load_census; from river_model.design import enumerate_designs,constraint_feasible; p=replace(Params(),land_available_ha=20.0); rows=enumerate_designs(p,load_census(Path('tests/fixtures/census.csv'))); print(len(rows), sum(constraint_feasible(r) for r in rows)); print(rows[0].design, rows[0].costs.eac)"
```

Observed output:

```text
18 8
Design(shed_ids=('S01', 'S02'), modules=1, tankers=1, carts=1, collection_days_week=1) 3071892.3399877204
```

This confirms a positive evaluation count, a non-negative feasible count, and a finite first-row EAC.

### Cycle 2 RED — alternative tests before implementation

The two Step 6 tests were appended while `evaluate_alternatives` was still absent. The exact required focused command was run before adding the alternative implementation:

```text
python -m pytest tests/test_design.py -v
```

Observed result: exit code 2; pytest collected 0 items and stopped with the expected import error:

```text
tests\test_design.py:81: in <module>
    from river_model.design import evaluate_alternatives
E   ImportError: cannot import name 'evaluate_alternatives' from 'river_model.design'
```

No alternative production code was written before this failure was observed.

### Cycle 2 GREEN — complete design suite

After implementing the prescribed alternatives and calculations, the exact required focused command was run again:

```text
python -m pytest tests/test_design.py -v
```

Observed result: exit code 0; all eight tests passed in 0.23 seconds:

```text
test_enumeration_returns_evaluations_and_counts_shed_subsets PASSED
test_enumeration_uses_barangay_service_sets PASSED
test_missing_land_rejects_every_design PASSED
test_budget_constraint_is_never_violated_by_feasible_design PASSED
test_digester_and_tanker_constraints_match_formulas PASSED
test_target_is_not_a_deterministic_constraint PASSED
test_alternatives_use_same_station_functional_unit PASSED
test_unquoted_alternative_costs_remain_missing PASSED

8 passed in 0.23s
```

### Full current suite

After focused GREEN and self-review, the full current suite was run exactly once before reporting:

```text
python -m pytest -v
```

Observed result: exit code 0; 460 items collected and all 460 passed in 2.54 seconds. No failures, errors, or warnings were reported.

```text
collected 460 items
...
460 passed in 2.54s
```

## Requirements Checklist

- [x] Added the six prescribed enumeration tests before production code and captured missing-module RED.
- [x] Added the two prescribed alternative tests before alternative production code and captured missing-function RED.
- [x] Added frozen `Design`, `DesignEvaluation`, `Alternative`, and `AlternativeEvaluation` dataclasses with the specified fields and order.
- [x] Added `constraint_feasible`, `enumerate_designs`, and `evaluate_alternatives` with the specified signatures.
- [x] Sorted confirmed eligible sheds by `shed_id` and enumerated every non-empty combination of sorted unique barangays.
- [x] Included every confirmed eligible shed in each selected barangay cluster and excluded unknown/false drainage through `eligible_sheds`.
- [x] Used `ceil(len(subset) / 8)` carts and collection-day values `(1, 2)`.
- [x] Used the prescribed inclusive module and tanker ranges from each minimum through the configured extra-count bound.
- [x] Passed the prescribed VS diversion and annual MPN12 values into Task 4 `compute_costs`.
- [x] Populated exactly the eight required check keys and used the nine exact rejection messages.
- [x] Kept target concentration and target probability out of deterministic checks.
- [x] Sorted evaluations by `(costs.eac, costs.cash_12m, -len(design.shed_ids))`.
- [x] Added exactly the three prescribed alternatives with exact scenario values, legal text, measurability flags, and notes.
- [x] Calculated station-level concentration bounds, mode annual MPN12 prevention, and mode cash/EAC when costs are present.
- [x] Returned `None` costs and `cost_status="missing"` for unquoted alternatives; returned zero costs and `"sourced"` for the defined counterfactual.
- [x] Ran the required candidate inspection and obtained a finite EAC.
- [x] Ran focused tests after each implementation cycle and the full suite once.
- [x] Dispatched no subagents and performed no Git initialization or commits.

## Self-Review

- **Interfaces and dependencies:** The module consumes the tested `Params`, `Shed`, `eligible_sheds`, `compute_load`, `compute_process`, `CostInputs`, and `compute_costs` interfaces without changing Tasks 1/1A–4.
- **Enumeration scope:** Service sets are barangay combinations rather than synthetic-shed power sets. For Santiago/Alfonso this yields at most three service sets, and all member sheds are retained in ID order.
- **Search boundaries:** Both loops are inclusive of `max_extra_modules` and `max_extra_tankers`; collection days are exactly 1 and 2; minimum counts are at least one.
- **Constraint fidelity:** Digester and tanker checks reproduce the formulas asserted by the focused tests. Budget compares 12-month cash, land distinguishes missing evidence from insufficient area, reconciliation delegates to `LoadResult`, and mass balance uses the 5% limit. Focus-stream allocation is checked against the 70% minimum using `Params.focus_stream_share`.
- **Rejection traceability:** Each failed check adds its corresponding prescribed rejection text; land failure adds exactly one of the missing-evidence or insufficient-area messages.
- **Decision-rule separation:** `constraint_feasible` considers only deterministic checks and rejection reasons. The target concentration is deliberately absent, leaving Task 6 to apply its probability threshold.
- **Alternative functional unit:** Every alternative uses `C0` and the Task 2 `L0 = C0 × Q × 86,400 × 10,000` conversion. Low/high concentration bounds are ordered from lowest to highest concentration, so high source-share/capture produces `c_end_low`, and low source-share/capture produces `c_end_high`.
- **Alternative economics:** Present mode CAPEX/OPEX use the Task 4 contingency base, replacement timing, discounting, and stable capital-recovery formula. Missing quotes are never replaced with fabricated values.
- **Test quality:** The required tests exercise real load, process, cost, and enumeration code with no mocks. The service-set test catches accidental shed-level power-set enumeration; missing-land coverage protects evidence handling; formula checks protect capacity constraints; the strict-target test protects deterministic/probabilistic separation; and the alternative tests protect station-level baseline behavior and missing-cost handling.
- **Scope:** Only the two requested implementation/test files and this requested report were created.

## Concerns / Limitations

1. **Duration check is redundant for valid Task 4 parameters and unreachable as a returned rejection for invalid durations.** `enumerate_designs` records `duration = pilot_months <= 12` and the exact rejection text, but Task 4's tested `compute_costs` raises `ValueError` when `pilot_months > 12` before a `DesignEvaluation` can be returned. Thus valid model inputs always pass duration, while an over-12-month input is rejected upstream rather than retained as a rejected candidate. Resolving this would require changing the Task 4 interface/validation contract or adding a separately specified costing path, neither of which Task 5 authorizes.
2. **The eight prescribed tests do not directly cover every branch.** In particular, they do not independently assert exact evaluation counts/ranges, EAC sorting and tie-breaks, focus-stream failure, duration failure, insufficient-area land failure, upstream reconciliation failure, mass-balance failure, alternative low/high concentration ordering, or the nonzero quoted-cost EAC branch. These paths follow the brief but have limited direct regression coverage.
3. **Alternative low/high outcome ordering is an interpretation of the scenario labels.** The implementation orders reported concentrations from low to high, pairing high effectiveness with low concentration and low effectiveness with high concentration. The required tests assert only the mode and counterfactual values, so this convention is not independently pinned by the prescribed test suite.

These concerns do not prevent the required Task 5 interface or its eight focused tests from passing, but they should be considered in downstream review.

## Fix round 1

**Status:** DONE  
**Date:** 2026-11-25  
**Workspace:** `C:\Users\Ma Christine\Downloads\Youth Case Study - UP RESEARCH FAIR`

### Summary

Added the review-requested duration fail-fast and alternative-input validation without changing any public dataclass or function signature. Expanded `tests/test_design.py` from 8 to 96 focused cases covering exact enumeration geometry, eligibility, check/rejection branches, costing-input propagation, sorting, zero enrollment, defensive feasibility, fail-fast behavior, exact alternative outcomes, and invalid physical/economic inputs. Added the two requested behavior docstrings.

### Files changed

- `C:\Users\Ma Christine\Downloads\Youth Case Study - UP RESEARCH FAIR\river_model\design.py`
- `C:\Users\Ma Christine\Downloads\Youth Case Study - UP RESEARCH FAIR\tests\test_design.py`
- `C:\Users\Ma Christine\Downloads\Youth Case Study - UP RESEARCH FAIR\.superpowers\sdd\2026-11-24-lucong-river-economic-model\task-5-report.md`

No other source, test, configuration, or model-input files were changed. The workspace remains outside Git; no repository was initialized and no commits were created. No subagents were dispatched.

### TDD evidence

All regression tests were written before the production edits. An initial diagnostic run also exposed one test-only duplicate keyword in the insufficient-land fixture; that setup error was corrected before implementation. The definitive pre-implementation RED command was:

```text
python -m pytest tests/test_design.py -q --tb=no
```

Observed result: exit code 1, with exactly the 66 missing-contract cases failing and 30 existing/characterization cases passing:

```text
.........................F.....FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF [ 75%]
FFFFFFFFFFFFFFFFFFFFFFFF                                                 [100%]
...
66 failed, 30 passed in 1.05s
```

The preceding diagnostic command was:

```text
python -m pytest tests/test_design.py -q --tb=short
```

Its relevant failure evidence showed that an overlong pilot reached the patched costing boundary and that invalid alternative physical inputs returned instead of raising:

```text
E   Failed: compute_costs must not run for an overlong pilot
E   Failed: DID NOT RAISE <class 'ValueError'>
```

After adding only the duration guard, the focused duration regression command was:

```text
python -m pytest tests/test_design.py::test_pilot_over_twelve_months_fails_before_costing -q
```

Observed result: exit code 0:

```text
.                                                                        [100%]
1 passed in 0.17s
```

After adding alternative validation, the complete focused GREEN command was:

```text
python -m pytest tests/test_design.py -q
```

Observed result: exit code 0:

```text
........................................................................ [ 75%]
........................                                                 [100%]
96 passed in 0.48s
```

### Full current suite

The full current suite was run once after focused GREEN and self-review:

```text
python -m pytest -q
```

Observed result: exit code 0; 548 items collected and all passed, with no failures, errors, or warnings:

```text
........................................................................ [ 13%]
........................................................................ [ 26%]
........................................................................ [ 39%]
........................................................................ [ 52%]
........................................................................ [ 65%]
........................................................................ [ 78%]
........................................................................ [ 91%]
............................................                            [100%]
548 passed in 4.38s
```

### Self-review

- Reviewed the actual source and test changes against saved pre-fix copies using `git diff --no-index`; this did not initialize or modify a Git repository.
- **Public interfaces:** `Design`, `DesignEvaluation`, `Alternative`, `AlternativeEvaluation`, `constraint_feasible`, `enumerate_designs`, and `evaluate_alternatives` retain their existing fields and signatures.
- **Duration:** `pilot_months > 12` now raises `ValueError("pilot exceeds 12 months")` at the start of enumeration, before costing. The existing returned-evaluation `duration` check and rejection text remain intact.
- **Source-share behavior:** The new docstring states that a physically invalid service subset raises immediately and is never capped or dropped. The regression case has a valid first service subset followed by an impossible second subset and pins the existing `source share exceeds 1` failure.
- **Alternative validation:** Validation runs before alternative calculations and covers exactly the parameters used there: positive finite `c0_mpn_100ml`/`q_m3_s`, nonnegative finite `discount`, positive integral `asset_life`, integral `replacement_year` in `1..asset_life`, and finite `contingency_rate`/`replacement_capex_frac` in `[0, 1]`. Booleans and nonnumeric values are rejected with parameter-specific `ValueError` messages.
- **Alternative convention:** The new docstring identifies `c_end_low`/`c_end_high` as concentration bounds and states that high effectiveness maps to low concentration.
- **Design-space constants and formulas:** No enumeration bounds, service-set logic, cart rule, check formulas, rejection strings, sort key, alternative constants, concentration formulas, or economic formulas changed.
- **Valid-output preservation:** Loaded the saved pre-fix module beside the current module and compared `dataclasses.asdict` results exactly across 27 valid cases: nine parameter sets, each evaluated for alternatives plus fixture and three-shed enumeration. Every enumeration row, check, rejection tuple, cost, and alternative result matched exactly.
- **Branch coverage:** Tests now pin 18 fixture evaluations; 54 evaluations and exactly three Santiago/Alfonso service sets; 8 evaluations per service set with both one-extra inclusive ranges; two carts for nine sheds; `False`/`None` drainage exclusion; all eight check keys; real unit-cost propagation; focus, land, reconciliation, and budget rejections; sort order; zero-enrollment infinite unit costs; every failed-check and rejection-reason feasibility path; exact household bounds `8,800 / 12,640 / 15,200`; mode prevention `52.98048` trillion MPN/year; and sourced zero-cost do-nothing economics.
- **Concerns:** None identified for this fix round. The earlier duration, branch-coverage, and alternative-ordering concerns are addressed by the production changes and regression tests above.

## Fix round 2

**Status:** DONE  
**Date:** 2026-11-25  
**Workspace:** `C:\Users\Ma Christine\Downloads\Youth Case Study - UP RESEARCH FAIR`

### Summary

Restored the `enumerate_designs` controller-boundary contract for invalid `pilot_months` without changing any public interface, enumeration logic, alternatives, or valid-output behavior. The entry guard now rejects booleans and non-`Integral` values before any numeric comparison, rejects integers below 1, and retains the exact over-12 error before costing. Added regression coverage for all nine required invalid values and valid boundaries at 1 and 12 months.

### Files changed

- `C:\Users\Ma Christine\Downloads\Youth Case Study - UP RESEARCH FAIR\river_model\design.py`
- `C:\Users\Ma Christine\Downloads\Youth Case Study - UP RESEARCH FAIR\tests\test_design.py`
- `C:\Users\Ma Christine\Downloads\Youth Case Study - UP RESEARCH FAIR\.superpowers\sdd\2026-11-24-lucong-river-economic-model\task-5-report.md`

No other source, test, configuration, or model-input files were intentionally changed. The workspace remains outside Git; no repository was initialized and no commits were created. No subagents were dispatched.

### TDD evidence

All nine invalid-value cases and both valid-boundary cases were added before the production edit. The definitive pre-implementation RED command was:

```text
python -m pytest tests/test_design.py -q --tb=short
```

Observed result: exit code 1; exactly the nine new invalid-value cases failed and the 98 existing/valid-boundary cases passed:

```text
.........................FFFFFFFFF...................................... [ 67%]
...................................                              [100%]
...
9 failed, 98 passed in 6.17s
```

The failures demonstrated the regression at the intended boundary: `0`, `-1`, `1.5`, NaN, `True`, and `False` reached costing instead of being rejected at entry; infinity received the over-12 message instead of the finite-integer message; and `"12"` and `None` raised `TypeError` at the direct `> 12` comparison. No production code was edited before this RED result was observed.

After adding only the prescribed entry validation, the focused GREEN command was:

```text
python -m pytest tests/test_design.py -q
```

Observed result: exit code 0:

```text
........................................................................ [ 67%]
...................................                                      [100%]
107 passed in 1.13s
```

### Full current suite

After focused GREEN and self-review, the full current suite was run exactly once:

```text
python -m pytest -q
```

Observed result: exit code 0; 559 items collected and all passed, with no failures, errors, or warnings:

```text
........................................................................ [ 12%]
........................................................................ [ 25%]
........................................................................ [ 38%]
........................................................................ [ 51%]
........................................................................ [ 64%]
........................................................................ [ 77%]
........................................................................ [ 90%]
.......................................................               [100%]
559 passed in 6.69s
```

### Self-review

- **Public interfaces:** All existing dataclasses, function signatures, return types, and valid enumeration/alternative outputs remain unchanged. The only production change is the new validation at the start of `enumerate_designs`.
- **Validation order:** Booleans and non-`Integral` values raise `ValueError("pilot_months must be a finite integer")` before the `> 12` comparison; values below 1 raise `ValueError("pilot_months must be an integer from 1 through 12")`; values above 12 retain exact `ValueError("pilot exceeds 12 months")`.
- **Fail-fast behavior:** Every invalid regression case patches `compute_costs` to fail if called, proving rejection occurs at the controller boundary rather than downstream. The existing over-12 test and its exact-message assertion were retained unchanged.
- **Boundary preservation:** Both 1 and 12 months still return evaluations, and every returned row retains a passing duration check.
- **Regression coverage:** The nine required invalid inputs are `0`, `-1`, `1.5`, NaN, infinity, `True`, `False`, `"12"`, and `None`; each asserts the prescribed parameter-specific `ValueError` message.
- **Scope:** Enumeration, alternatives, other validation, and costing were not modified. No Git operations or subagents were used.
- **Concerns:** None identified for this fix round.
