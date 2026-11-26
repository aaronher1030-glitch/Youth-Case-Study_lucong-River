# Task 4 Fix Round 1 Brief

Work from: `C:\Users\Ma Christine\Downloads\Youth Case Study - UP RESEARCH FAIR`

## Context

Independent review confirmed the valid-default formulas but found missing input validation and weak lifecycle/unit-cost regression coverage. This round must preserve the public interfaces and valid-default results while preventing invalid scenarios from appearing artificially cheap or crashing.

This workspace is not a Git repository. Do not initialize Git or create commits. Do not dispatch subagents.

## Required production changes

1. **Validate `CostInputs` before arithmetic**
   - `sheds` and `heads`: finite integers strictly greater than zero.
   - `modules`, `tankers`, `carts`: finite integers greater than or equal to zero.
   - `trips_week`, `vs_diverted_year`, `annual_mpn_prevented_12`: finite and nonnegative.
   - Reject booleans and nonnumeric values with field-specific `ValueError`.
   - Keep zero prevention and zero VS diversion valid; their unit costs remain `float("inf")`.

2. **Validate economic parameters**
   - All CAPEX and OPEX parameter values used must be finite and nonnegative.
   - `contingency_rate`, `opex_maint_frac`, and `replacement_capex_frac` must lie in `[0, 1]`.
   - `discount` must be finite and nonnegative.
   - `asset_life` must be a positive integer.
   - `replacement_year` must be an integer from 1 through `asset_life`, inclusive.
   - `pilot_months` must be an integer from 1 through 12, inclusive.
   - Reject booleans/nonnumeric values with parameter-specific `ValueError`.

3. **Numerically stable EAC**
   - Remove the unused-import concern by using `math.log1p` and `math.expm1` for the nonzero-discount CRF:
     `crf = discount / (-expm1(-asset_life * log1p(discount)))`.
   - Preserve the zero-discount `npc / asset_life` branch and valid-default results.

## Required tests

Follow TDD: add/update tests first and capture expected failures before production edits.

- Keep the five existing tests, but strengthen the cash test with literal OPEX and cash values:
  - `opex_12m = 2_730_000.0`
  - `contingency = 917_000.0`
  - `cash_12m = 10_087_000.0`
- Add literal default lifecycle assertions:
  - `npc ≈ 26_771_261.166334495`
  - `eac ≈ 3_989_707.363394699`
- Add a replacement-timing assertion: default NPC minus NPC with `replacement_capex_frac=0` equals `1_610_000 / 1.08**5`.
- Add literal positive unit-cost assertions for the default case:
  - `php_per_shed_month ≈ 22_165.040907748327`
  - `php_per_mpn12 ≈ 797_941.4726789398`
  - `php_per_vs_kg ≈ 398.9707363394699`
  - `fee_per_head_month ≈ 1_477.6693938498886`
- Add zero-VS diversion returning infinite unit cost.
- Add a tiny-positive-discount test (`discount=1e-16`) confirming EAC is approximately `npc / asset_life` without division failure.
- Add focused validation tests for invalid counts, negative/non-finite trips and benefits, invalid rates/fractions, zero/negative asset life, out-of-life replacement year, pilot months outside 1–12, nonnumeric values, and zero sheds/heads.
- Vary tanker and cart counts independently in a CAPEX test or parameterized case so each multiplier is protected.

## Verification and report

- Run focused tests while iterating.
- Run the full current suite once before reporting.
- Self-review the actual diff and confirm valid-default values are unchanged.

Append `## Fix round 1` to:
`C:\Users\Ma Christine\Downloads\Youth Case Study - UP RESEARCH FAIR\.superpowers\sdd\2026-11-24-lucong-river-economic-model\task-4-report.md`

Include exact RED/GREEN commands and relevant output, files changed, full-suite result, and self-review. Return only status, one-line test summary, concerns, and report path.
