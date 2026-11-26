# Task 5 fix round 2 — independent scoped review

Reviewer: fresh read-only general-purpose agent `task5-fix2-review` (`add78be12a96be0f9`).

## Spec verdict: APPROVED

- All nine invalid inputs raise exact parameter-specific `ValueError` before costing.
- `pilot_months=13` retains exact `ValueError("pilot exceeds 12 months")`.
- Boundaries `1` and `12` enumerate successfully.
- No public interface or other production behavior changed in the delta.

## Quality verdict: APPROVED

The fix is minimal, uses the existing `Integral` import, validates before numeric comparisons or enumeration, and follows established costing-validation conventions. Tests assert exact anchored messages and explicitly fail if costing is reached.

## Findings

None. No fixes required.

## Verification evidence

Python 3.13.6.

```text
python -m pytest tests/test_design.py -q
107 passed in 0.61s

python -m pytest -q
559 passed in 4.59s
```

Direct probes confirmed:

- `0`, `-1` → `pilot_months must be an integer from 1 through 12`
- `1.5`, NaN, infinity, `True`, `False`, `"12"`, `None` → `pilot_months must be a finite integer`
- `13` → `pilot exceeds 12 months`
- Every invalid/over-12 case made zero costing calls.
- Both `1` and `12` returned 18 rows, all with passing duration checks.
- Additional `-infinity` and a very large integer probes behaved correctly.

Mutation testing used only in-memory module replacement; workspace files were not modified.

```text
Remove both new guards: 9 failed in 2.81s
Remove type guard only: 7 failed, 2 passed in 2.62s
Remove lower guard only: 2 failed, 7 passed in 2.66s
```

Thus, the new tests detect removal of the complete fix and each guard independently.

## Scope statement

Reviewed only the fix-round-2 delta. Current `river_model/design.py` and `tests/test_design.py` exactly match the supplied fix-2-head snapshots, and an independently reconstructed diff matches the package. All 12 other production/test/fixture files match the available original Task-5 head snapshots. Because this is not a Git repository, unchanged status outside those available baselines cannot be proven globally. No workspace files were edited, no Git repository was initialized, and no subagents were dispatched.

## Controller confirmation

The controller reconstructed the six-line production and eleven-test-case snapshot diff, inspected current guard placement at `river_model/design.py:38-47`, and reran verification:

```text
python -m pytest tests/test_design.py -q
107 passed in 0.82s

python -m pytest -q
559 passed in 3.22s
```

Verdict stands: APPROVED for progression to Task 6.
