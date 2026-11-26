# Task 2 Fix Round 1 Brief

Work from: `C:\Users\Ma Christine\Downloads\Youth Case Study - UP RESEARCH FAIR`

## Context

Independent review found that the core arithmetic is correct but physical-inconsistency handling and regression protection are insufficient. The binding specification overrides two brief details: any bottom-up `r > 1` must raise (no `1e-9` acceptance band), and incompatible upstream evidence must remain visible rather than being clamped.

This workspace is not a Git repository. Do not initialize Git or create commits. Do not dispatch subagents.

## Required production changes

1. **Strict source-share consistency**
   - Raise `ValueError` for any computed `r > 1.0`, including `1 < r <= 1.0 + 1e-9`.
   - Remove the `max(0.0, r)` sanitization. Negative computed source share must raise as physically invalid.
   - Keep the existing error text prefix `source share exceeds 1` for the above-one case; use a clear `source share must be nonnegative` error for negative values.

2. **Input validation at the model boundary**
   - Before division or load calculation, require finite values.
   - Require `c0_mpn_100ml > 0`, `q_m3_s > 0`, and `e_head_day >= 0`.
   - Require `eta`, `p_enroll`, `p_collect`, `p_retain`, and `source_share_tolerance` to lie in `[0, 1]`.
   - If supplied, require `upstream_mpn_100ml >= 0` and finite.
   - Reject negative eligible-shed head counts.
   - Raise `ValueError` with parameter-specific messages. Do not add defaults or silently coerce invalid values.

3. **Honest top-down reconciliation**
   - Compute raw `top_down_r = (C0 - upstream) / C0` without clamping.
   - If raw top-down share is negative, keep it in `LoadResult.top_down_r` and set `reconciliation_ok=False`.
   - Otherwise compare absolute difference to `source_share_tolerance` using `<=` as before.
   - When upstream is missing, preserve `top_down_r=None`; `reconciliation_ok=True` retains the existing interface meaning "no contradiction detected," not "field-reconciled."

## Required test changes

Follow TDD: add/update tests first and capture expected failures before production edits.

- Remove the unused `eligible_sheds` import from `tests/test_load.py`.
- Strengthen `test_unit_conversion_matches_hand_calculation` to assert `l_target_mpn_day` independently.
- Strengthen `test_threshold_identity_for_8000` with independent expected values: `c_end` approximately `4836.263020833334`, reduction at least `0.5`, and endpoint at most `8000`.
- Add an independent nonzero annual-prevention assertion using the `365 / 1e12` conversion and a hand-computed expected value.
- Extend the above-one test to cover a source share just above one within the former `1e-9` band.
- Add invalid-input tests covering zero/negative/non-finite physical inputs, out-of-range probabilities/factors/tolerance, negative upstream, and negative eligible heads.
- Add automated reconciliation tests for: missing upstream evidence, matching estimate, mismatching estimate, exact tolerance boundary, and upstream greater than C0 producing a negative raw top-down share with `reconciliation_ok=False`.

## Verification and report

- Run focused tests while iterating.
- Run the full current suite once before reporting.
- Self-review the actual diff and confirm no silent clamps remain.

Append `## Fix round 1` to:
`C:\Users\Ma Christine\Downloads\Youth Case Study - UP RESEARCH FAIR\.superpowers\sdd\2026-11-24-lucong-river-economic-model\task-2-report.md`

Include exact RED/GREEN commands and relevant output, files changed, full-suite result, and self-review. Return only status, one-line test summary, concerns, and report path.
