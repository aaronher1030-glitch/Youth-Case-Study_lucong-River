# Task 5 Fix Round 2 Brief

Work from: `C:\Users\Ma Christine\Downloads\Youth Case Study - UP RESEARCH FAIR`

## Context

Task 5 fix 1 passed independent review, but controller boundary checks found that `enumerate_designs` now compares `pilot_months` directly with 12. `None` and `"13"` therefore raise `TypeError`, regressing Task 4's parameter-specific `ValueError` contract.

This workspace is not a Git repository. Do not initialize Git, commit, or dispatch subagents.

## Required TDD change

1. Add failing tests to `tests/test_design.py` for invalid `pilot_months`: `0`, `-1`, `1.5`, NaN, infinity, `True`, `False`, `"12"`, and `None`. Assert `ValueError` whose message names `pilot_months`.
2. Keep the existing over-12 test asserting exact `ValueError("pilot exceeds 12 months")` before costing.
3. Add valid boundary tests for 1 and 12 months proving enumeration still returns rows.
4. Capture RED before production edits.

## Minimal production fix

At `enumerate_designs` entry, before the `> 12` comparison:

- reject booleans and non-`Integral` values with `ValueError("pilot_months must be a finite integer")`;
- reject values below 1 with `ValueError("pilot_months must be an integer from 1 through 12")`;
- retain exact `ValueError("pilot exceeds 12 months")` above 12.

Do not change enumeration, alternatives, or other validation.

## Verification and report

Run focused tests and the full suite once. Append `## Fix round 2` to the existing Task 5 report with exact RED/GREEN/full-suite evidence and self-review. Return only status, one-line test summary, concerns, and report path.
