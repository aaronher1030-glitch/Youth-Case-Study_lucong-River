# Task 1/1A Fix Round 1 Brief

Work from: `C:\Users\Ma Christine\Downloads\Youth Case Study - UP RESEARCH FAIR`

## Context

The independent review approved the core contracts but found two Important issues and one Minor test gap. The binding spec says every generated row must carry exact `source="synthetic"` plus a scenario identifier. The existing `shed_id` already carries the scenario identifier. Missing census `barangay` or `source` values must not bypass validation because the model refuses undocumented missing values.

This workspace is not a Git repository. Do not initialize Git or create commits. Do not dispatch subagents.

## Required changes

### 1. Exact synthetic provenance

- Change every generated `Shed.source` to exactly `"synthetic"`.
- Keep the scenario identifier in `shed_id` (`SYN-####-##`) and keep the declared prior/seed visible in later scenario/report outputs.
- Update `test_every_generated_row_is_labelled_synthetic` to assert exact equality with `"synthetic"` and retain the scenario-ID check.
- Update the Task 1 report/smoke expectation by appending a fix-round section; do not rewrite prior evidence.

### 2. Census required-field validation

- Reject blank or missing `barangay` with `ValueError` matching `barangay must not be blank`.
- Reject blank or missing `source` with `ValueError` matching `source must not be blank`.
- This must also reject truncated CSV rows where those cells are absent.
- Add focused regression tests for both fields, including at least one truncated-row case.

### 3. Uniform-prior test

- Add a deterministic test proving both connection-level selection and barangay assignment use equal weighting under the declared RNG sequence. Use enough scenarios to make a weighted implementation fail reliably, without mocking NumPy or asserting incidental exact counts from a tiny sample.
- Keep the test focused on the public `generate_synthetic_census` behavior.

## TDD sequence

1. Add/update the failing tests first.
2. Run the focused tests and capture the expected failures.
3. Make the minimal production changes.
4. Run the focused tests and confirm all pass with pristine output.
5. Run the full current test suite once.
6. Self-review the actual edits.

## Report

Append a `## Fix round 1` section to:
`C:\Users\Ma Christine\Downloads\Youth Case Study - UP RESEARCH FAIR\.superpowers\sdd\2026-11-24-lucong-river-economic-model\task-1-report.md`

Include exact RED and GREEN commands/output, files changed, test results, and self-review findings. Return a short status only: DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT, test summary, concerns, and report path.
