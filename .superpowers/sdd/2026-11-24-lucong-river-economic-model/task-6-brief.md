# Task 6 Brief: Joint Uncertainty, Sensitivity, and Robust Selection

Work from: `C:\Users\Ma Christine\Downloads\Youth Case Study - UP RESEARCH FAIR`

## Context and authority

The binding spec is `docs/superpowers/specs/2026-11-24-river-economic-model-design.md`; the implementation plan is `docs/superpowers/plans/2026-11-24-lucong-river-economic-model.md`, Task 6. Global constraints apply, especially seed 2026, production default 20,000 draws, target probability at least 80%, and no lowering the threshold.

The workspace is not a Git repository. Do not initialize Git, commit, or dispatch subagents.

## Interfaces

Create `river_model/uncertainty.py` and `tests/test_uncertainty.py`.

Produce exactly these public signatures:

```python
@dataclass(frozen=True)
class UncertaintySpec:
    q_low: float = 0.02
    q_high: float = 0.20
    e_low: float = 1.0e8
    e_high: float = 1.0e10
    eta_low: float = 0.50
    eta_mode: float = 0.80
    eta_high: float = 1.00
    p_enroll_low: float = 0.80
    p_enroll_mode: float = 0.95
    p_enroll_high: float = 0.99
    p_collect_low: float = 0.80
    p_collect_mode: float = 0.95
    p_collect_high: float = 0.99
    p_retain_low: float = 0.80
    p_retain_mode: float = 0.95
    p_retain_high: float = 0.99
    cost_low: float = 0.80
    cost_mode: float = 1.00
    cost_high: float = 1.30
    n_draws: int = 20_000
    seed: int = 2026

@dataclass(frozen=True)
class MonteCarloResult:
    p_target: float | None
    c_end_p10: float | None
    c_end_p50: float | None
    c_end_p90: float | None
    eac_p10: float | None
    eac_p50: float | None
    eac_p90: float | None
    invalid_fraction: float
    valid_draws: int
    endpoints: object

def make_draws(spec: UncertaintySpec, n: int, seed: int) -> dict[str, object]
def evaluate_design_uncertainty(
    params: Params,
    sheds: Sequence[Shed],
    evaluation: DesignEvaluation,
    draws: Mapping[str, object],
) -> MonteCarloResult
def run_uncertainty(
    params: Params,
    sheds: Sequence[Shed],
    evaluations: Sequence[DesignEvaluation],
    spec: UncertaintySpec,
) -> dict[Design, MonteCarloResult]
def select_robust_design(
    params: Params,
    evaluations: Sequence[DesignEvaluation],
    results: Mapping[Design, MonteCarloResult],
) -> DesignEvaluation | None
def one_at_a_time(
    params: Params,
    sheds: Sequence[Shed],
    evaluation: DesignEvaluation,
    spec: UncertaintySpec,
) -> list[dict[str, object]]
```

## Rulings that override plan details

1. **Strict physical validity:** The plan's `r > 1 + 1e-9` allowance conflicts with the spec. Any draw with `r > 1.0` is invalid. There is no tolerance and no silent cap.
2. **Fractions are bounded:** `eta`, enrollment, collection, and retention values outside `[0, 1]` are invalid physical draws. Cost multiplier may exceed one but must be finite and nonnegative.
3. **Nonfinite values are invalid:** NaN/infinity in any supplied draw array invalidates that draw and withholds probability claims.
4. **Design-specific heads:** Use only confirmed eligible sheds whose IDs appear in `evaluation.design.shed_ids`; do not sum the whole census when evaluating a subset. Raise if a design ID is absent or not confirmed eligible.
5. **Tie-breaking:** Robust selection orders valid candidates by `(costs.eac, costs.cash_12m, -len(shed_ids))`, matching deterministic ranking.

## Implementation requirements

### Draw generation and validation

- Use `np.random.default_rng(seed)`.
- `q` and `e` are log-uniform: `exp(uniform(log(low), log(high)))`.
- `eta`, `p_enroll`, `p_collect`, `p_retain`, and `cost_multiplier` use NumPy triangular distributions with the exact low/mode/high fields.
- Return arrays under exactly: `q`, `e`, `eta`, `p_enroll`, `p_collect`, `p_retain`, `cost_multiplier`.
- Validate before drawing:
  - `n` is a positive integer, not bool;
  - `seed` is a nonnegative integer, not bool;
  - `q_low`, `q_high`, `e_low`, `e_high` are finite and strictly positive, with low <= high;
  - triangular low/mode/high are finite with low <= mode <= high;
  - eta/capture bounds lie in `[0,1]`;
  - cost bounds are finite and nonnegative;
  - `spec.n_draws` is a positive integer and `spec.seed` is a nonnegative integer.
- Raise parameter-specific `ValueError`; no default replacement.

### Vectorized evaluation

Use NumPy arrays; never loop over Monte Carlo draws.

1. Validate `params.c0_mpn_100ml` is finite and positive, `target_mpn_100ml` is finite and nonnegative.
2. Validate draw mappings contain exactly the seven required keys, one-dimensional equal-length nonempty arrays, with numeric contents.
3. Compute `l0 = c0 * q * 86400 * 10000`, `l_target = eta * served_heads * e`, and `r = l_target / l0`.
4. Mark invalid any draw with nonfinite values, `q <= 0`, `e < 0`, `eta` or capture outside `[0,1]`, `cost_multiplier < 0`, or `r > 1.0` or `r < 0`.
5. For valid draws only compute endpoint/EAC arrays for summary math, but never discard invalid draws to form a claim.
6. If `invalid_fraction > 0`: all six percentile fields and `p_target` are `None`, `valid_draws=0`, `endpoints` is an empty float NumPy array.
7. Otherwise: `p_target = mean(c_end <= target)`, percentiles are 10th/50th/90th, `valid_draws=n`, and `endpoints` contains all endpoints.
8. `c_end = c0 * (1 - r * p_enroll * p_collect * p_retain)` and `eac = evaluation.costs.eac * cost_multiplier`.

### Run and selection

- `run_uncertainty` makes one draw object and reuses it for every deterministically feasible evaluation, ensuring common random numbers. Return only feasible evaluations keyed by `Design`.
- `select_robust_design` considers only deterministic-feasible evaluations with a present result, non-`None` probability, and `p_target >= params.target_probability`.
- Validate `target_probability` is finite in `[0,1]`.
- Return the lowest-EAC candidate with the specified tie-breaks, or `None`; never lower the threshold.

### One-at-a-time sensitivity

- Baseline result uses the original spec.
- For each of `q_m3_s`, `e_head_day`, `eta`, `p_enroll`, `p_collect`, `p_retain`, and `cost_multiplier`, test its low and high values: 14 rows total.
- Fix all three low/mode/high fields of the tested parameter to the tested value, retain the same seed, regenerate draws, and rerun evaluation.
- Return each row with exactly these keys:
  - `parameter`, `setting` (`"low"` or `"high"`), `value`, `p_target`, `c_end_p50`, `eac_p50`, `decision_changes`.
- `decision_changes` compares meeting `params.target_probability` against the baseline. A `None` probability does not meet the threshold.
- Cost multiplier must change median EAC but leave `p_target` and `decision_changes` unchanged; do not force a decision flip.

## Required tests

Follow TDD: write tests first, run the focused suite to observe expected import failure, then implement.

Minimum coverage:

- fixed-seed reproducibility and different-seed difference;
- exact seven draw keys and array lengths;
- log-uniform and triangular parameters with hand-computed/statistical checks strong enough to detect swapped distributions;
- invalid specs: bounds, mode ordering, fractions, zero/negative log-uniform bounds, NaN/infinity, booleans, nonpositive draw counts, and negative/noninteger seeds;
- zero enrollment gives `p_target=0`;
- any `r > 1` draw withholds probability even if `r=1+1e-12`;
- nonfinite draw values and out-of-range fractions withhold probability;
- invalid fraction and `valid_draws=0` are retained; endpoints are empty on withheld results;
- valid percentiles and endpoints independently recalculate from a small controlled draw mapping;
- design-specific head count excludes nonselected and unconfirmed sheds;
- missing/unknown design shed IDs raise;
- `run_uncertainty` excludes deterministic-infeasible candidates and uses common random numbers;
- selection rejects missing/withheld/below-threshold results and applies EAC/cash/coverage tie-breaks;
- no candidate meets threshold returns `None`;
- sensitivity has the seven parameters and 14 low/high rows;
- cost sensitivity leaves probability/decision unchanged while median EAC changes;
- sensitivity decision flip is correctly detected in a controlled case;
- 20,000-draw smoke run completes and selection never uses a withheld probability.

## Verification and report

- Run focused tests while iterating.
- Run the required 20,000-draw smoke command from the plan after GREEN.
- Run the full current suite once before reporting.
- Append `## Task 6 implementation` to a new report:
  `C:\Users\Ma Christine\Downloads\Youth Case Study - UP RESEARCH FAIR\.superpowers\sdd\2026-11-24-lucong-river-economic-model\task-6-report.md`

Include exact RED/GREEN commands and output, smoke output, files changed, full-suite result, and self-review. Return only status, one-line test summary, concerns, and report path.
