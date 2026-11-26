# Task 3 Fix Round 1 Brief

Work from: `C:\Users\Ma Christine\Downloads\Youth Case Study - UP RESEARCH FAIR`

## Context

Independent review confirmed the valid-input formulas but found missing physical-input validation, uncontrolled division by zero, and weak independent test coverage. This round must close those findings without changing the public `ProcessResult` or `compute_process` interface.

This workspace is not a Git repository. Do not initialize Git or create commits. Do not dispatch subagents.

## Required production changes

Add validation at the start of `compute_process`, before any arithmetic or division:

- Require finite numeric values for every process parameter used and for eligible-shed heads.
- Require eligible-shed heads, `manure_kg_head_day`, `washwater_l_head_day`, and `ch4_yield` to be nonnegative.
- Require `dm_frac`, `vs_frac_dm`, `vs_destroyed`, and `n_frac_dm` to lie in `[0, 1]`.
- Require `ch4_frac` to lie in `(0, 1]`.
- Require `ch4_mj_m3`, `lpg_mj_kg`, `rice_n_kg_ha`, and `tanker_m3` to be strictly positive.
- Raise parameter-specific `ValueError` for invalid values. Nonnumeric values must also become `ValueError`, not leaked `TypeError`.
- Validate denominators even when there are zero eligible heads, so invalid parameters never depend on data volume to be detected.
- Preserve all valid-input formulas and zero-input results.

## Required tests

Follow TDD: add/update tests first, run them to capture expected failures, then change production code.

1. Remove the unused `replace` import only if still unused after tests are added.
2. Add a non-default hand-calculation test with independently derived expected values for all 16 `ProcessResult` fields. Use this exact case:
   - 3 eligible heads
   - `manure_kg_head_day=4.0`
   - `washwater_l_head_day=10.0`
   - `dm_frac=0.25`
   - `vs_frac_dm=0.80`
   - `vs_destroyed=0.50`
   - `ch4_yield=0.40`
   - `ch4_frac=0.60`
   - `ch4_mj_m3=30.0`
   - `lpg_mj_kg=45.0`
   - `n_frac_dm=0.05`
   - `rice_n_kg_ha=100.0`
   - `tanker_m3=3.0`
   Expected values include: manure 12 kg/day; wash 0.03 m3/day; slurry 0.042 m3/day; DM in 3; VS in 2.4; VS destroyed 1.2; VS remaining 1.2; DM remaining 1.8; methane 0.48 m3/day; biogas 0.8 m3/day; LPG 0.32 kg/day; N 0.09 kg/day; land 0.3285 ha; trips 0.098/week; balance error 0.
3. Add an all-output zero test for an empty eligible set using valid parameters.
4. Add focused parameterized tests for:
   - negative/non-finite process quantities and heads;
   - out-of-range fractions and destruction;
   - zero/negative methane fraction, energy contents, rice uptake, and tanker volume;
   - nonnumeric process parameters.
   Keep the suite focused; do not duplicate every Cartesian combination unless each case protects a distinct validation branch.
5. Retain eligibility, monotonicity, and valid balance tests, but ensure the exact hand calculation independently protects the formulas.

## Verification and report

- Run focused tests while iterating.
- Run the full current suite once before reporting.
- Self-review the actual diff and confirm no invalid input is clamped or silently converted to zero.

Append `## Fix round 1` to:
`C:\Users\Ma Christine\Downloads\Youth Case Study - UP RESEARCH FAIR\.superpowers\sdd\2026-11-24-lucong-river-economic-model\task-3-report.md`

Include exact RED/GREEN commands and relevant output, files changed, full-suite result, and self-review. Return only status, one-line test summary, concerns, and report path.
