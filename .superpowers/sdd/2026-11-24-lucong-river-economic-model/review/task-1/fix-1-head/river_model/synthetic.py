from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

import numpy as np

from river_model.inputs import Shed


@dataclass(frozen=True)
class SyntheticSpec:
    sheds_low: int = 12
    sheds_high: int = 20
    heads_low: float = 8.0
    heads_mode: float = 15.0
    heads_high: float = 25.0
    connection_levels: tuple[float, ...] = (0.0, 0.25, 0.50, 0.75, 1.00)
    barangays: tuple[str, ...] = ("Santiago", "Alfonso")
    default_scenarios: int = 200


def _validate(spec: SyntheticSpec) -> None:
    if spec.sheds_low < 1 or spec.sheds_high < spec.sheds_low:
        raise ValueError("shed bounds must be positive and ordered")
    if not (0 < spec.heads_low <= spec.heads_mode <= spec.heads_high):
        raise ValueError("heads_low, heads_mode, and heads_high must be positive and ordered")
    if not spec.connection_levels or any(
        value < 0.0 or value > 1.0 for value in spec.connection_levels
    ):
        raise ValueError("connection_levels must lie between 0 and 1")
    if len(spec.barangays) < 2 or len(set(spec.barangays)) != len(spec.barangays):
        raise ValueError("barangays must contain at least two unique names")
    if spec.default_scenarios < 1:
        raise ValueError("default_scenarios must be positive")


def generate_synthetic_census(
    spec: SyntheticSpec,
    scenario_id: int,
    seed: int,
) -> tuple[Shed, ...]:
    _validate(spec)
    if scenario_id < 1:
        raise ValueError("scenario_id must be positive")

    rng = np.random.default_rng(seed)
    n_sheds = int(rng.integers(spec.sheds_low, spec.sheds_high + 1))
    connection_probability = float(rng.choice(spec.connection_levels))
    sheds: list[Shed] = []

    for index in range(1, n_sheds + 1):
        heads = max(
            1,
            int(round(rng.triangular(spec.heads_low, spec.heads_mode, spec.heads_high))),
        )
        connected = bool(rng.random() < connection_probability)
        barangay = str(rng.choice(spec.barangays))
        sheds.append(
            Shed(
                shed_id=f"SYN-{scenario_id:04d}-{index:02d}",
                barangay=barangay,
                heads=heads,
                drains_to_reach=connected,
                source="synthetic",
            )
        )

    return tuple(sheds)


def write_census(path: Path, sheds: Sequence[Shed]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["shed_id", "barangay", "heads", "drains_to_reach", "source"],
        )
        writer.writeheader()
        for shed in sheds:
            writer.writerow(
                {
                    "shed_id": shed.shed_id,
                    "barangay": shed.barangay,
                    "heads": shed.heads,
                    "drains_to_reach": (
                        "unknown" if shed.drains_to_reach is None else str(shed.drains_to_reach).lower()
                    ),
                    "source": shed.source,
                }
            )
