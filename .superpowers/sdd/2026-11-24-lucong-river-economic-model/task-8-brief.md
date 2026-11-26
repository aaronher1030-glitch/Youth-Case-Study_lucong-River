# Task 8 Brief: Intuitive Streamlit/Plotly Viewer

Work from: `C:\Users\Ma Christine\Downloads\Youth Case Study - UP RESEARCH FAIR`

## Context and authority

Implement Task 8 of the approved plan on top of completed model, reporting, and synthetic scenario modules. The viewer is presentation only: no model formulas or duplicated calculations. Binding requirements include five tabs, mode labels on every tab, explicit synthetic-prior warnings, scenario overrides, reset, filters/comparison, downloads, cache keys based on immutable inputs, and honest no-selection/withheld-probability states.

Do not dispatch subagents. Do not initialize Git or commit.

## Interfaces

Create:

- `river_model/app.py`
- `tests/test_app.py`

Produce:

```python
def build_app(
    census_path: Path | None,
    synthetic: bool = False,
    n_scenarios: int = 200,
    n_draws: int = 20_000,
    seed: int = 2026,
) -> None

def main() -> None
```

## Shared execution and cache contract

- `build_app` must work headlessly through Streamlit `AppTest` and must not require an uploader.
- Observed mode requires a non-`None` census path and renders a clear error otherwise.
- Synthetic mode requires no census and runs `run_synthetic_model`.
- Use `st.session_state` for overrides, comparison IDs, census path, synthetic flag, scenario count, draw count, and seed.
- Cache observed execution by census bytes/hash, sorted override items, draw count, and seed.
- Cache synthetic execution by sorted override items, scenario count, draw count, and seed.
- Synthetic helper runs in a temporary directory and returns result plus output-file bytes; downloads survive cleanup.
- Never cache on mutable dictionaries/lists alone.
- Model errors are caught at the UI boundary and displayed as `st.error`; no silent fallback to defaults.

## Required interface content

Before tabs:

- synthetic: `st.warning("SYNTHETIC — NOT FIELD-VERIFIED")`, declared prior, scenario count, draws, seed;
- observed: `st.caption("OBSERVED CENSUS")`.

Five tabs with exact labels:

1. `Overview`
2. `Assumptions`
3. `Designs`
4. `Compare`
5. `Uncertainty and methods`

Repeat a short exact mode caption in every tab.

### Overview

- Plotly reach schematic: Santiago Bridge → shed cluster → 1-km reach → EMB station.
- KPI metrics: selected design, cash, EAC, median endpoint, achieved probability, annual MPN prevented.
- No selection: explicit error using the required 80% rule and binding constraints; no fabricated KPI zero.
- Withheld selected/near-feasible probability: show `withheld`/invalid fraction, never 0%.
- Synthetic: connected-head histogram and selected-design frequencies labeled prior-predictive.

### Assumptions

- Group controls under Load, Process, Capacity, Cost, Decision.
- Numeric controls show unit, provenance status, source, and base/scenario label.
- User changes produce visible `Scenario override` warning.
- `Reset to base case` clears overrides and comparison state as appropriate.
- Missing land is visibly missing and must not be silently defaulted to a number.

### Designs

- Candidate table built without importing pandas; include feasibility text and rejection reasons.
- Filter All/Feasible/Infeasible.
- Cost–reduction frontier.
- Alternatives table shows `Missing`, not zero, for unquoted costs.
- Never rely on color alone.

### Compare

- Multiselect up to three candidates; default comparison state must not crash when empty.
- Side-by-side cash, EAC, endpoint, reduction, land, HRT, trips.
- Cost-breakdown chart and Pass/Fail/Missing constraint table.

### Uncertainty and methods

- Endpoint histogram with 8,000 threshold when valid; explicit withheld/unavailable state otherwise.
- Tornado/decision-flip chart from `one_at_a_time`.
- Exact core equations via `st.latex`.
- Validation status and parameter register.
- Download buttons for candidate CSV, parameter register CSV, selected-design JSON, decision brief, and both static HTML files.
- Synthetic mode additionally downloads `synthetic_scenarios.csv` and `prior_predictive_summary.json`.

### Entry point

`main()` offers `Observed census` and `Synthetic prior-predictive`. Observed reads `RIVER_MODEL_CENSUS` when set, otherwise file uploader. Synthetic needs no upload and exposes scenario/draw/seed controls. `build_app` remains the testable entry point.

## Required tests

TDD first; observe missing-module failure.

- five exact tab labels and no exceptions;
- missing-land error and all rows retain rejection text;
- synthetic warning, prior, scenario/draw/seed display;
- at least required download buttons;
- observed no-census error;
- no-selection and withheld-probability UI states never show fabricated probabilities;
- scenario override warning appears after changing a control and disappears after reset;
- Designs filter changes visible rows;
- Compare supports zero, one, two, and three candidates without exceptions;
- synthetic prior-predictive charts/downloads are present;
- cache tests prove changed census/overrides/draws/seed produce distinct executions;
- AppTest default timeout is increased where needed rather than hiding slow failures.

## Browser verification

After focused/full tests, start:

`streamlit run river_model/app.py --server.port 8501`

Use the installed headed Playwright MCP to check the plan's 11 golden-path items, including upload, land override, override warning/reset, filters, compare, threshold line, CSV download, synthetic mode, prior-predictive charts, summary download/evidence label, and console errors. Record only checks actually performed in `docs/river_model_methods.md` if it exists; otherwise include them in the Task 8 report for Task 9 propagation.

## Verification and report

Run focused tests, full suite once, and browser checks. Create:

`C:\Users\Ma Christine\Downloads\Youth Case Study - UP RESEARCH FAIR\.superpowers\sdd\2026-11-24-lucong-river-economic-model\task-8-report.md`

Include RED/GREEN, test results, exact browser checks/results or explicit inability, files changed, and self-review. Return only status, one-line test summary, concerns, and report path.
