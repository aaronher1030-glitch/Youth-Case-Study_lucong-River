# Task 7A Brief: Prior-Predictive Scenario Runner and Synthetic CLI

Work from: `C:\Users\Ma Christine\Downloads\Youth Case Study - UP RESEARCH FAIR`

## Context and authority

Implement Task 7A of `docs/superpowers/plans/2026-11-24-lucong-river-economic-model.md` against the binding design specification. Task 7 reporting/CLI will already exist. Global constraints apply: exact synthetic prior, seed 2026, default 200 scenario censuses and 20,000 within-scenario draws, exact label `SYNTHETIC — NOT FIELD-VERIFIED`, and no Git initialization/commits.

Do not dispatch subagents.

## Interfaces

Create:

- `river_model/scenarios.py`
- `tests/test_scenarios.py`

Modify:

- `river_model/cli.py` only if the Task 7 interface needs integration
- `river_model/__main__.py`

Produce:

```python
@dataclass(frozen=True)
class ScenarioSummary:
    scenario_id: int
    n_sheds: int
    connected_sheds: int
    connected_heads: int
    source_share_r: float | None
    selected: bool
    design_key: str | None
    best_p_target: float | None
    selected_p_target: float | None
    cash_12m: float | None
    eac: float | None
    c_end_p50: float | None
    invalid_fraction: float | None
    dominant_constraint: str | None

def run_synthetic_model(
    output_dir: Path,
    overrides: Mapping[str, str],
    n_scenarios: int,
    n_draws: int,
    seed: int,
) -> dict[str, object]
```

## Binding rulings

1. **Exact row provenance:** Every generated census row has `source == "synthetic"` exactly. The plan test using `startswith("synthetic;")` is superseded. Scenario identity remains in `shed_id`.
2. **Configuration key:** Use `modules,tankers,carts,collection_days_week` only, joined by `|` (for example `1|1|1|1`). Do not include synthetic shed IDs, which change every scenario and would destroy frequency interpretation.
3. **Strict counts:** `n_scenarios` and `n_draws` are positive integers; `seed` is a nonnegative integer. Reject booleans and nonintegers with `ValueError`.
4. **Invalid scenarios remain visible:** Any evaluated feasible uncertainty result with `invalid_fraction > 0` makes that scenario count as invalid. Do not truncate draws or manufacture probabilities.
5. **Dominant rejection:** Count exact rejection reasons across infeasible evaluations; choose highest count, then lexicographically smallest reason for ties. Return `None` when there are no rejection reasons.
6. **Source share:** Use selected design's deterministic `load.r`; if none selected, use highest `r` among deterministically feasible evaluations. Return `None` if no feasible evaluation exists.
7. **Representative scenario:** Connected heads closest to the median connected-head count, tie lower scenario ID. Standard artifacts describe this representative scenario, not an aggregate selected design.

## Implementation requirements

For each scenario ID 1 through `n_scenarios`:

- derive `scenario_seed = seed + scenario_id - 1`;
- generate with `SyntheticSpec()` and `generate_synthetic_census`;
- apply overrides once to `Params()`;
- enumerate designs, run uncertainty with `UncertaintySpec(n_draws=n_draws, seed=scenario_seed)`, and select robust design;
- record exact `ScenarioSummary` fields;
- `best_p_target` is the maximum non-`None` probability among deterministically feasible results;
- `invalid_fraction` is the maximum invalid fraction among evaluated results, or `None` if none;
- selected cost/EAC/median endpoint come from the selected evaluation/result and remain `None` if no selection.

Choose the representative scenario, write `synthetic_census_example.csv`, then call `run_model(..., mode="synthetic")` for standard artifacts. Write:

- `synthetic_scenarios.csv` with exactly:
  `scenario_id,n_sheds,connected_sheds,connected_heads,source_share_r,selected,design_key,best_p_target,selected_p_target,cash_12m,eac,c_end_p50,invalid_fraction,dominant_constraint`
- `prior_predictive_summary.json` with exact plan fields: mode, evidence label, prior, seed, counts, selected/no-feasible/invalid counts, selected-design frequencies, connected-head percentiles, source-share percentiles, best-probability percentiles, dominant constraints.
- Missing percentile inputs produce `None`, never NaN or fabricated zero.
- Return `{"mode": "synthetic", "evidence_label": "SYNTHETIC — NOT FIELD-VERIFIED", "summary": summary_dict, "summaries": summaries, "files": files}`.

CLI:

- mutually exclusive required `--census` / `--synthetic`;
- `--output` default `sim/outputs/river_model`;
- `--draws` default 20000;
- `--seed` default 2026;
- `--scenarios` default 200;
- repeatable `--set NAME=VALUE`;
- synthetic branch prints the exact evidence label before any result;
- observed branch prints `OBSERVED CENSUS`;
- malformed overrides fail clearly rather than being silently ignored.

## Required tests

Follow TDD; first observe missing-module/CLI failures.

- synthetic artifacts and exact evidence label;
- exact `source == "synthetic"` on every example row;
- reproducibility of scenario CSV and summary JSON for identical inputs;
- CLI works without census and honors scenario/draw counts;
- invalid count/seed types and boundaries raise;
- configuration-only design-key frequencies;
- representative median-head selection with lower-ID tie-break;
- selected/no-selected field handling;
- best valid probability ignores withheld results;
- invalid scenario counting from any evaluated result;
- source-share fallback to highest-r feasible evaluation;
- dominant-rejection count/tie rule;
- empty percentile groups return `None`;
- synthetic outputs are never labeled observed;
- smoke run with 10 scenarios and 500 writes, seeded 2026, succeeds.

## Verification and report

- Run focused tests while iterating.
- Run the plan's 10-scenario/500-draw synthetic smoke command.
- Run the full suite once before reporting.
- Create:
  `C:\Users\Ma Christine\Downloads\Youth Case Study - UP RESEARCH FAIR\.superpowers\sdd\2026-11-24-lucong-river-economic-model\task-7a-report.md`

Include RED/GREEN and smoke commands/results, files changed, full-suite result, and self-review. Return only status, one-line test summary, concerns, and report path.
