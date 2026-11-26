from __future__ import annotations

import math
from dataclasses import dataclass, replace
from numbers import Integral, Real
from typing import Mapping, Sequence

import numpy as np

from river_model.design import Design, DesignEvaluation, constraint_feasible
from river_model.inputs import Params, Shed, eligible_sheds


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


_DRAW_KEYS = (
    "q",
    "e",
    "eta",
    "p_enroll",
    "p_collect",
    "p_retain",
    "cost_multiplier",
)
_TRIANGULAR_PARAMETERS = (
    ("eta", True),
    ("p_enroll", True),
    ("p_collect", True),
    ("p_retain", True),
    ("cost_multiplier", False),
)
_SENSITIVITY_FIELDS = {
    "q_m3_s": "q",
    "e_head_day": "e",
    "eta": "eta",
    "p_enroll": "p_enroll",
    "p_collect": "p_collect",
    "p_retain": "p_retain",
    "cost_multiplier": "cost_multiplier",
}


def _validate_integer(name: str, value: object, minimum: int) -> None:
    if isinstance(value, bool) or not isinstance(value, Integral):
        raise ValueError(f"{name} must be an integer")
    if value < minimum:
        if minimum == 0:
            raise ValueError(f"{name} must be a nonnegative integer")
        raise ValueError(f"{name} must be a positive integer")


def _validate_finite_number(name: str, value: object) -> float:
    if isinstance(value, bool) or not isinstance(value, Real):
        raise ValueError(f"{name} must be a finite number")
    try:
        number = float(value)
    except (OverflowError, TypeError, ValueError) as exc:
        raise ValueError(f"{name} must be a finite number") from exc
    if not math.isfinite(number):
        raise ValueError(f"{name} must be a finite number")
    return number


def _validate_spec(spec: UncertaintySpec) -> None:
    _validate_integer("n_draws", spec.n_draws, 1)
    _validate_integer("seed", spec.seed, 0)

    for prefix in ("q", "e"):
        low = _validate_finite_number(f"{prefix}_low", getattr(spec, f"{prefix}_low"))
        high = _validate_finite_number(
            f"{prefix}_high", getattr(spec, f"{prefix}_high")
        )
        if low <= 0.0 or high <= 0.0:
            raise ValueError(f"{prefix}_low and {prefix}_high must be strictly positive")
        if low > high:
            raise ValueError(f"{prefix}_low must be less than or equal to {prefix}_high")

    for parameter, is_fraction in _TRIANGULAR_PARAMETERS:
        field_prefix = "cost" if parameter == "cost_multiplier" else parameter
        low = _validate_finite_number(
            f"{field_prefix}_low", getattr(spec, f"{field_prefix}_low")
        )
        mode = _validate_finite_number(
            f"{field_prefix}_mode", getattr(spec, f"{field_prefix}_mode")
        )
        high = _validate_finite_number(
            f"{field_prefix}_high", getattr(spec, f"{field_prefix}_high")
        )
        if not low <= mode <= high:
            raise ValueError(
                f"{field_prefix}_low must be <= {field_prefix}_mode <= {field_prefix}_high"
            )
        if is_fraction:
            if not 0.0 <= low <= high <= 1.0:
                raise ValueError(f"{parameter} bounds must lie in [0, 1]")
        elif low < 0.0:
            raise ValueError(f"{parameter} bounds must be nonnegative")


def make_draws(spec: UncertaintySpec, n: int, seed: int) -> dict[str, object]:
    _validate_integer("n", n, 1)
    _validate_integer("seed", seed, 0)
    _validate_spec(spec)

    rng = np.random.default_rng(seed)
    draws: dict[str, object] = {
        "q": np.exp(rng.uniform(math.log(spec.q_low), math.log(spec.q_high), n)),
        "e": np.exp(rng.uniform(math.log(spec.e_low), math.log(spec.e_high), n)),
    }
    for parameter, _ in _TRIANGULAR_PARAMETERS:
        field_prefix = "cost" if parameter == "cost_multiplier" else parameter
        low = getattr(spec, f"{field_prefix}_low")
        mode = getattr(spec, f"{field_prefix}_mode")
        high = getattr(spec, f"{field_prefix}_high")
        if low == high:
            # NumPy rejects a zero-width triangular distribution. Consume the
            # same random stream width, then represent its degenerate limit.
            rng.random(n)
            draws[parameter] = np.full(n, low, dtype=float)
        else:
            draws[parameter] = rng.triangular(low, mode, high, n)
    return draws


def _validate_concentration_params(params: Params) -> None:
    c0 = _validate_finite_number("c0_mpn_100ml", params.c0_mpn_100ml)
    target = _validate_finite_number("target_mpn_100ml", params.target_mpn_100ml)
    if c0 <= 0.0:
        raise ValueError("c0_mpn_100ml must be positive")
    if target < 0.0:
        raise ValueError("target_mpn_100ml must be nonnegative")


def _validate_draws(draws: Mapping[str, object]) -> dict[str, np.ndarray]:
    if set(draws) != set(_DRAW_KEYS):
        missing = sorted(set(_DRAW_KEYS) - set(draws))
        extra = sorted(set(draws) - set(_DRAW_KEYS))
        raise ValueError(f"draw mapping keys mismatch: missing={missing}, extra={extra}")

    arrays: dict[str, np.ndarray] = {}
    length: int | None = None
    for key in _DRAW_KEYS:
        try:
            raw = np.asarray(draws[key])
        except (TypeError, ValueError) as exc:
            raise ValueError(f"draw {key} must be a numeric one-dimensional array") from exc
        if raw.ndim != 1:
            raise ValueError(f"draw {key} must be one-dimensional")
        if length is None:
            length = raw.size
            if length == 0:
                raise ValueError("draw arrays must be nonempty")
        elif raw.size != length:
            raise ValueError("draw arrays must have equal lengths")
        if raw.dtype.kind not in {"i", "u", "f"}:
            raise ValueError(f"draw {key} must contain numeric values")
        try:
            arrays[key] = raw.astype(float, copy=False)
        except (TypeError, ValueError, OverflowError) as exc:
            raise ValueError(f"draw {key} must contain numeric values") from exc
    return arrays


def _served_heads(sheds: Sequence[Shed], evaluation: DesignEvaluation) -> int:
    by_id: dict[str, Shed] = {}
    for shed in sheds:
        if shed.shed_id in by_id:
            raise ValueError(f"duplicate shed_id: {shed.shed_id}")
        by_id[shed.shed_id] = shed
    confirmed = {shed.shed_id: shed for shed in eligible_sheds(sheds)}

    selected: set[str] = set()
    heads = 0
    for shed_id in evaluation.design.shed_ids:
        if shed_id in selected:
            raise ValueError(f"duplicate design shed_id: {shed_id}")
        selected.add(shed_id)
        if shed_id not in by_id:
            raise ValueError(f"design shed_id is missing from census: {shed_id}")
        if shed_id not in confirmed:
            raise ValueError(f"design shed_id is not confirmed eligible: {shed_id}")
        shed = confirmed[shed_id]
        if isinstance(shed.heads, bool) or not isinstance(shed.heads, Real):
            raise ValueError(f"heads for shed {shed_id} must be a finite number")
        try:
            shed_heads = float(shed.heads)
        except (TypeError, ValueError, OverflowError) as exc:
            raise ValueError(f"heads for shed {shed_id} must be a finite number") from exc
        if not math.isfinite(shed_heads) or shed_heads < 0.0:
            raise ValueError(f"heads for shed {shed_id} must be finite and nonnegative")
        heads += shed.heads
    return heads


def _withheld_result(invalid_fraction: float) -> MonteCarloResult:
    return MonteCarloResult(
        p_target=None,
        c_end_p10=None,
        c_end_p50=None,
        c_end_p90=None,
        eac_p10=None,
        eac_p50=None,
        eac_p90=None,
        invalid_fraction=invalid_fraction,
        valid_draws=0,
        endpoints=np.empty(0, dtype=float),
    )


def evaluate_design_uncertainty(
    params: Params,
    sheds: Sequence[Shed],
    evaluation: DesignEvaluation,
    draws: Mapping[str, object],
) -> MonteCarloResult:
    _validate_concentration_params(params)
    arrays = _validate_draws(draws)
    served_heads = _served_heads(sheds, evaluation)
    base_eac = _validate_finite_number("costs.eac", evaluation.costs.eac)
    if base_eac < 0.0:
        raise ValueError("costs.eac must be nonnegative")

    finite = np.ones_like(arrays["q"], dtype=bool)
    for array in arrays.values():
        finite &= np.isfinite(array)

    with np.errstate(over="ignore", under="ignore", divide="ignore", invalid="ignore"):
        l0 = params.c0_mpn_100ml * arrays["q"] * 86_400.0 * 10_000.0
        l_target = arrays["eta"] * served_heads * arrays["e"]
        r = l_target / l0
        eac = base_eac * arrays["cost_multiplier"]

    invalid = (
        ~finite
        | ~np.isfinite(l0)
        | ~np.isfinite(l_target)
        | ~np.isfinite(r)
        | ~np.isfinite(eac)
        | (arrays["q"] <= 0.0)
        | (arrays["e"] < 0.0)
        | (arrays["eta"] < 0.0)
        | (arrays["eta"] > 1.0)
        | (arrays["p_enroll"] < 0.0)
        | (arrays["p_enroll"] > 1.0)
        | (arrays["p_collect"] < 0.0)
        | (arrays["p_collect"] > 1.0)
        | (arrays["p_retain"] < 0.0)
        | (arrays["p_retain"] > 1.0)
        | (arrays["cost_multiplier"] < 0.0)
        | (r > 1.0)
        | (r < 0.0)
    )
    invalid_fraction = float(np.mean(invalid))
    if invalid_fraction > 0.0:
        return _withheld_result(invalid_fraction)

    capture = arrays["p_enroll"] * arrays["p_collect"] * arrays["p_retain"]
    c_end = params.c0_mpn_100ml * (1.0 - r * capture)
    c_percentiles = np.percentile(c_end, (10.0, 50.0, 90.0))
    eac_percentiles = np.percentile(eac, (10.0, 50.0, 90.0))
    return MonteCarloResult(
        p_target=float(np.mean(c_end <= params.target_mpn_100ml)),
        c_end_p10=float(c_percentiles[0]),
        c_end_p50=float(c_percentiles[1]),
        c_end_p90=float(c_percentiles[2]),
        eac_p10=float(eac_percentiles[0]),
        eac_p50=float(eac_percentiles[1]),
        eac_p90=float(eac_percentiles[2]),
        invalid_fraction=0.0,
        valid_draws=int(arrays["q"].size),
        endpoints=c_end,
    )


def run_uncertainty(
    params: Params,
    sheds: Sequence[Shed],
    evaluations: Sequence[DesignEvaluation],
    spec: UncertaintySpec,
) -> dict[Design, MonteCarloResult]:
    draws = make_draws(spec, spec.n_draws, spec.seed)
    return {
        evaluation.design: evaluate_design_uncertainty(
            params, sheds, evaluation, draws
        )
        for evaluation in evaluations
        if constraint_feasible(evaluation)
    }


def _validate_target_probability(params: Params) -> float:
    target = _validate_finite_number("target_probability", params.target_probability)
    if not 0.0 <= target <= 1.0:
        raise ValueError("target_probability must lie in [0, 1]")
    return target


def _meets_threshold(probability: float | None, threshold: float) -> bool:
    return (
        probability is not None
        and math.isfinite(probability)
        and 0.0 <= probability <= 1.0
        and probability >= threshold
    )


def select_robust_design(
    params: Params,
    evaluations: Sequence[DesignEvaluation],
    results: Mapping[Design, MonteCarloResult],
) -> DesignEvaluation | None:
    threshold = _validate_target_probability(params)
    candidates = [
        evaluation
        for evaluation in evaluations
        if constraint_feasible(evaluation)
        and evaluation.design in results
        and _meets_threshold(
            results[evaluation.design].p_target,
            threshold,
        )
    ]
    if not candidates:
        return None
    return min(
        candidates,
        key=lambda evaluation: (
            evaluation.costs.eac,
            evaluation.costs.cash_12m,
            -len(evaluation.design.shed_ids),
        ),
    )


def _fixed_spec(
    spec: UncertaintySpec, parameter: str, setting: str
) -> tuple[UncertaintySpec, float]:
    if parameter in ("q_m3_s", "e_head_day"):
        draw_name = _SENSITIVITY_FIELDS[parameter]
        value = getattr(spec, f"{draw_name}_{setting}")
        return replace(spec, **{f"{draw_name}_low": value, f"{draw_name}_high": value}), value

    field_prefix = "cost" if parameter == "cost_multiplier" else parameter
    value = getattr(spec, f"{field_prefix}_{setting}")
    return (
        replace(
            spec,
            **{
                f"{field_prefix}_low": value,
                f"{field_prefix}_mode": value,
                f"{field_prefix}_high": value,
            },
        ),
        value,
    )


def one_at_a_time(
    params: Params,
    sheds: Sequence[Shed],
    evaluation: DesignEvaluation,
    spec: UncertaintySpec,
) -> list[dict[str, object]]:
    threshold = _validate_target_probability(params)
    baseline_draws = make_draws(spec, spec.n_draws, spec.seed)
    baseline = evaluate_design_uncertainty(
        params, sheds, evaluation, baseline_draws
    )
    baseline_decision = _meets_threshold(baseline.p_target, threshold)

    rows: list[dict[str, object]] = []
    for parameter in _SENSITIVITY_FIELDS:
        for setting in ("low", "high"):
            scenario, value = _fixed_spec(spec, parameter, setting)
            scenario_draws = make_draws(scenario, scenario.n_draws, scenario.seed)
            result = evaluate_design_uncertainty(
                params, sheds, evaluation, scenario_draws
            )
            decision = _meets_threshold(result.p_target, threshold)
            rows.append(
                {
                    "parameter": parameter,
                    "setting": setting,
                    "value": value,
                    "p_target": result.p_target,
                    "c_end_p50": result.c_end_p50,
                    "eac_p50": result.eac_p50,
                    "decision_changes": decision != baseline_decision,
                }
            )
    return rows
