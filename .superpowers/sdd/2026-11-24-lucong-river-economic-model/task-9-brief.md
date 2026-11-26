# Task 9 Brief: Workbook, End-to-End Verification, Methods Note, and Final Artifacts

Work from: `C:\Users\Ma Christine\Downloads\Youth Case Study - UP RESEARCH FAIR`

## Context and authority

Complete Task 9 of the approved plan after Tasks 1–8 are review-clean. This task produces the independent formula audit, verification report/workbook, end-to-end tests, methods note, and reproducible production artifacts. It must not convert fixture or synthetic results into observed Lucong findings.

No Git initialization/commits and no subagents.

## Interfaces and files

Create:

- `river_model/workbook.py`
- `tests/test_workbook.py`
- `tests/test_end_to_end.py`
- `docs/river_model_methods.md`

Modify `river_model/reporting.py` as needed to generate verification artifacts.

Produce:

```python
def write_verification_workbook(path: Path, params: Params, evaluation: DesignEvaluation) -> None
```

## Workbook requirements

Use openpyxl. Sheets exactly:

- `Inputs`
- `Load`
- `Process`
- `Cost`
- `Comparison`

Load cells:

- `B2=C0`
- `B3=Q`
- `B4=L_gen`
- `B5=L0` formula `=B2*B3*86400*10000`
- `B6=r`
- `B7=c`
- `B8=C_end`

Write real spreadsheet formulas for `B5:B8`, not Python values. Process/Cost sheets contain all relevant quantities and formulas. Comparison contains Python value, spreadsheet formula, absolute difference, and PASS/FAIL with tolerance `0.01` for cost and `1e-6` for physical quantities.

Write Python-computed values in adjacent cells. Do not claim formulas were recalculated by Excel/LibreOffice unless a spreadsheet engine actually recalculated them. State that cached formula values require recalculation.

## Verification artifacts

Update `write_outputs` to write:

- `verification_report.txt`:
  Python/NumPy versions; mode/evidence label; seed/draws; synthetic prior/scenario count where applicable; candidate and deterministic-feasible counts; selected or explicit infeasibility; selected/best invalid fraction; acceptance checks as PASS/FAIL; workbook recalculation statement.
- `verification_workbook.xlsx`:
  selected evaluation when present; otherwise highest valid target probability among deterministic-feasible results labeled `not selected`; otherwise lowest-EAC evaluated design labeled `not selected—hard constraints failed` with probability fields blank.

Acceptance report must distinguish deterministic constraints, probabilistic threshold, reproducibility, invalid draws, and missing field evidence. A withheld probability is not a pass.

## End-to-end tests

Create observed and synthetic CLI tests using subprocess, temporary output directories, and the exact plan commands at reduced test sizes. Verify required artifacts, valid JSON, exact evidence labels, and that synthetic census rows use exact `source="synthetic"`.

The fixture is authorized only as smoke-test input. Tests and outputs must not call it a verified Concepcion census.

## Reproducible production commands

Run and record actual results:

```bash
python -m river_model --synthetic --output sim/outputs/river_model_synthetic --scenarios 200 --draws 20000 --seed 2026 --set land_available_ha=20
```

If no verified census has been supplied, run the fixture only as an explicitly labeled smoke test; do not claim observed Lucong findings.

Do not mark completion if a required production command fails. If it exceeds a single command timeout, run it as a monitored background process and wait for completion rather than substituting a smaller run.

## Methods note

`docs/river_model_methods.md` must include:

- purpose, exact decision rule, and constraints;
- exact equations and units from the specification;
- input schema/provenance and missing-data rules;
- observed versus synthetic mode, exact prior, seed/scenario/draw defaults, and conditional prior-predictive interpretation;
- CLI and viewer commands for both modes;
- interpretation of deterministic feasibility, target probability, invalid draws, and no-selection states;
- GitHub comparators and specific borrowed patterns, with verified URLs only;
- actual validation commands/results and Task 8 browser checks actually performed;
- explicit limitations: parameterized not calibrated; no health benefit; no 200 MPN compliance claim; original screenshots absent; workbook recalculation status; public swine statistics are context only;
- artifact inventory and claim boundaries.

## Required tests

TDD first; observe missing workbook/end-to-end failures.

- workbook sheet names and formula strings;
- Python values adjacent to formulas;
- cost/physical comparison tolerances;
- selected/not-selected/hard-constraint-failed workbook selection;
- verification report contains evidence label and recalculation disclaimer;
- observed CLI end-to-end artifacts;
- synthetic CLI end-to-end artifacts and exact row provenance;
- no fabricated probability in no-selection/withheld cases;
- full suite passes.

## Verification and report

Run focused tests, full suite once, and production command(s). Create:

`C:\Users\Ma Christine\Downloads\Youth Case Study - UP RESEARCH FAIR\.superpowers\sdd\2026-11-24-lucong-river-economic-model\task-9-report.md`

Include exact commands/results, production runtime, artifact paths, files changed, full-suite result, citation-verification status, browser-check propagation, and self-review. Return only status, one-line test summary, concerns, and report path.
