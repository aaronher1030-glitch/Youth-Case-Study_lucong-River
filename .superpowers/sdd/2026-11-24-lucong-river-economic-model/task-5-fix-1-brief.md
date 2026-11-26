# Task 5 Fix Round 1 Brief

Work from: `C:\Users\Ma Christine\Downloads\Youth Case Study - UP RESEARCH FAIR`

## Context

Independent review confirmed the enumeration and alternative constants but found unclear duration failure, missing alternative-input validation, and limited branch coverage. Preserve all public dataclasses and function signatures.

This workspace is not a Git repository. Do not initialize Git or create commits. Do not dispatch subagents.

## Required production changes

1. **Explicit duration fail-fast**
   - At the start of `enumerate_designs`, if `pilot_months > 12`, raise `ValueError("pilot exceeds 12 months")` before calling `compute_costs`.
   - Keep the existing defensive `duration` check/rejection for returned evaluations.
   - Add a test pinning this fail-fast contract.

2. **Validate alternative inputs**
   - Before alternative calculations, validate every parameter actually used:
     - finite numeric `c0_mpn_100ml > 0` and `q_m3_s > 0`;
     - finite `discount >= 0`;
     - positive integer `asset_life`;
     - integer `replacement_year` from 1 through `asset_life`;
     - finite `contingency_rate` and `replacement_capex_frac` in `[0, 1]`.
   - Reject booleans and nonnumeric values with parameter-specific `ValueError`.
   - Keep valid alternative results unchanged.

3. **Document fail-fast source-share behavior**
   - Add one short docstring to `enumerate_designs`: a physically invalid service subset raises immediately; it is never capped or silently dropped.
   - Add one short docstring to `evaluate_alternatives` explaining that `c_end_low`/`high` are concentration bounds, with high effectiveness mapped to low concentration.

## Required tests

Follow TDD: add/update tests first and capture expected failures before production edits.

- Consolidate imports at the top of `tests/test_design.py`; remove unused `pytest` only if still unused.
- Add exact enumeration count/range tests:
  - fixture: 18 evaluations;
  - three eligible sheds across Santiago/Alfonso: 54 evaluations and exactly the three service sets;
  - `max_extra_modules=1`, `max_extra_tankers=1`: each service set has 8 evaluations and both inclusive ranges are represented.
- Add a nine-shed single-barangay case proving `carts == 2`.
- Add eligibility exclusions for `False` and `None` drainage.
- Assert the exact eight check keys on every evaluation.
- Verify costing-input propagation through real outputs: `php_per_vs_kg == eac / expected_vs_diverted_year` and `php_per_mpn12 == eac / expected_annual_mpn12` for a controlled row.
- Add rejection tests for focus share below 70%, insufficient land, failed upstream reconciliation, and low budget.
- Assert rows are sorted by `(eac, cash_12m, -shed_count)`.
- Add zero-enrollment coverage proving finite EAC/cash and infinite MPN/VS unit costs.
- Add `constraint_feasible` tests showing any failed check or rejection reason makes a row infeasible; this protects defensive mass-balance/digester/tanker rejection semantics without forcing impossible enumerated candidates.
- Add duration fail-fast and invalid-subset source-share fail-fast tests.
- Add exact household alternative bounds: 8,800 / 12,640 / 15,200 MPN/100 mL; mode annual prevention 52.98048 trillion MPN/year under defaults; do-nothing costs zero with `cost_status="sourced"`.
- Add invalid physical/economic alternative-input tests covering zero, negative, NaN, infinity, booleans, and nonnumeric values for each validated parameter.

## Verification and report

- Run focused tests while iterating.
- Run the full current suite once before reporting.
- Self-review the actual diff and confirm design-space constants and valid outputs are unchanged.

Append `## Fix round 1` to:
`C:\Users\Ma Christine\Downloads\Youth Case Study - UP RESEARCH FAIR\.superpowers\sdd\2026-11-24-lucong-river-economic-model\task-5-report.md`

Include exact RED/GREEN commands and relevant output, files changed, full-suite result, and self-review. Return only status, one-line test summary, concerns, and report path.
