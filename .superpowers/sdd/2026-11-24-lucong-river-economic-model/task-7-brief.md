# Task 7 Brief: Reporting, Figures, Static HTML, and CLI

Work from: `C:\Users\Ma Christine\Downloads\Youth Case Study - UP RESEARCH FAIR`

## Context and authority

Implement Task 7 of the approved plan using completed Tasks 1–6. The binding spec requires auditable files, same-functional-unit alternatives, explicit missing data, no fabricated claims, and exact evidence labels.

No Git initialization/commits and no subagents.

## Interfaces

Create:

- `river_model/reporting.py`
- `river_model/cli.py`
- `river_model/__main__.py`
- `tests/test_reporting.py`

Produce exactly:

```python
def write_outputs(
    output_dir: Path,
    params: Params,
    register: list[dict[str, object]],
    evaluations: Sequence[DesignEvaluation],
    results: Mapping[Design, MonteCarloResult],
    selected: DesignEvaluation | None,
    alternatives: Sequence[AlternativeEvaluation],
    mode: str,
    *,
    sensitivity_rows: Sequence[Mapping[str, object]] | None = None,
) -> dict[str, Path]

def run_model(
    census_path: Path,
    output_dir: Path,
    overrides: Mapping[str, str],
    n_draws: int,
    seed: int,
    mode: str = "observed",
) -> dict[str, object]
```

## Required files and columns

Create output directory and return all paths in a `dict[str, Path]` under `files`.

- `parameter_register.csv`: every register field.
- `candidate_designs.csv`, exactly:
  `shed_ids,modules,tankers,carts,collection_days_week,capex,cash_12m,eac,c_end_mpn_100ml,reduction_fraction,annual_mpn_prevented_12,land_ha_required,digester_hrt_days,trips_week,feasible,rejection_reasons`
  - `shed_ids` is semicolon-joined; rejection reasons are semicolon-joined;
  - `feasible` means deterministic `constraint_feasible`, not probabilistic success.
- `alternatives.csv`, exactly:
  `name,c_end_low_mpn_100ml,c_end_mode_mpn_100ml,c_end_high_mpn_100ml,annual_mpn_prevented_12_mode,cash_12m_mode,eac_mode,cost_status,legal_status,measurable_12m,note`
  - unquoted costs remain blank, never zero.
- `monte_carlo_summary.csv`, exactly:
  `shed_ids,modules,tankers,carts,p_target,c_end_p10,c_end_p50,c_end_p90,eac_p10,eac_p50,eac_p90,invalid_fraction,valid_draws`
  - `None` values become blank cells.
- `sensitivity.csv`, exactly:
  `parameter,setting,value,p_target,c_end_p50,eac_p50,decision_changes`
  - write the supplied rows; when none are available, write the header and no fabricated rows.
- `sensitivity.html`: tornado/decision-flip chart when valid sensitivity exists; otherwise an explicit unavailable/withheld statement.
- `selected_design.json`.
- `decision_brief.md`.
- `cost_reduction_frontier.html`.
- `uncertainty.html`.
- `fig2_lucong_model.png`.

## JSON and claim rules

`selected_design.json` must include:

- `mode` and exact `evidence_label`: `SYNTHETIC — NOT FIELD-VERIFIED` or `OBSERVED CENSUS`;
- `selected` boolean;
- `target_probability_required` from `Params`;
- `target_probability` achieved for the selected design, or `None` if not selected/withheld;
- `design` as `asdict(selected.design)` or `None`;
- selected `cash_12m`, `eac`, `c_end_p10/p50/p90`, `invalid_fraction`, and `rejection_reasons` (empty when selected), all `None`/empty when absent;
- `reason`: `least-lifecycle-cost feasible design` when selected, otherwise `no feasible design`.

Do not call fixture smoke output a verified Lucong finding. The methods/report artifacts must retain the evidence label.

## Figures and brief

- Use Plotly HTML with no external CDN dependency for core rendering (`include_plotlyjs=True` is acceptable).
- Cost frontier: annual MPN prevented vs EAC; deterministic feasibility colors plus text labels; hover has shed IDs and rejections.
- Uncertainty:
  - selected valid result: endpoint histogram with vertical target line;
  - no selection but valid feasible result: highest valid probability, labeled `not selected`;
  - feasible results all withheld: explicit probability-withheld page with invalid fraction, no probability claim;
  - no feasible result: explicit hard-constraints-failed page.
- Matplotlib PNG uses Agg, has cost frontier left and endpoint histogram right when valid data exist, and is closed after saving. If no valid endpoints, state that endpoints are unavailable.
- `run_model` computes `one_at_a_time` for the selected design; if no design is selected but a deterministic-feasible result exists, compute it for the highest-valid-probability near-feasible design; otherwise pass no rows. This preserves `write_outputs`' existing positional interface while adding the optional keyword-only sensitivity input.
- Decision brief begins with exact evidence label; states selected design or no feasible design; includes cash, EAC, endpoint interval, probability, binding constraints, and three most decision-sensitive inputs.
- Sensitivity ranking: decision flips first, then absolute probability change, then absolute median endpoint change; unavailable/withheld values never fabricate a rank. If no valid sensitivity exists, say so.
- Synthetic brief explicitly states probabilities are conditional on the declared synthetic-census prior.

## CLI

- Validate `mode` is exactly `observed` or `synthetic`.
- Apply overrides, load census, enumerate, run uncertainty, select robust design, evaluate alternatives, and write outputs.
- `__main__.py` supports:
  `--census PATH`, `--output PATH` default `sim/outputs/river_model`, `--draws INT` default 20000, `--seed INT` default 2026, repeatable `--set NAME=VALUE`.
- Print exact evidence label, candidate and deterministic-feasible counts, selected design or `no feasible design`, cash, EAC, endpoint interval, and achieved probability. Summary must agree with JSON.
- Malformed `--set` entries fail clearly.

## Required tests

TDD first; observe missing CLI/module failures.

- all required outputs exist and are nonempty;
- exact CSV headers and row counts;
- rejection reasons survive CSV round-trip;
- blank alternative costs remain blank;
- selected JSON achieved probability is not confused with required threshold;
- synthetic label and conditional-prior wording;
- no-selection JSON/brief/uncertainty page behavior;
- withheld uncertainty produces no probability claim and empty endpoints handling;
- no deterministic-feasible evaluation produces clear hard-constraint failure;
- figure target line at 8,000 and correct selected/not-selected labeling;
- CLI stdout agrees with selected JSON;
- invalid mode, malformed override, invalid draw count/seed fail;
- required 500-draw CLI smoke command succeeds.

## Verification and report

Run focused tests and the plan's observed smoke command:

`python -m river_model --census tests/fixtures/census.csv --output sim/outputs/river_model_smoke --draws 500 --seed 2026 --set land_available_ha=20`

Run full suite once before reporting.

Create:
`C:\Users\Ma Christine\Downloads\Youth Case Study - UP RESEARCH FAIR\.superpowers\sdd\2026-11-24-lucong-river-economic-model\task-7-report.md`

Include RED/GREEN and smoke commands/results, files changed, full-suite result, and self-review. Return only status, one-line test summary, concerns, and report path.
