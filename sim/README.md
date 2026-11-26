# Desludging Campaign Simulation

**A discrete-event model of 400 households served under two notification arms, built to test which barrier binds — access or awareness.**

Run it in two commands. It needs no data files, no accounts, and no network.

```bash
python -m pip install -r sim/requirements.txt
python sim/run_scenarios.py --reps 200
```

Everything it writes lands in `sim/outputs/`.

---

## 1. What this model is for

The paper's primary endpoint is a difference between two arms:

- **Arm 1** — a standard schedule card delivered through barangay channels.
- **Arm 2** — the same card, plus a household visit and access remediation: an external access port or floor work, completed *before* the service window opens.

The barrier the paper argues about cannot be observed directly before a pilot runs. What *can* be done is ask: **under what assumptions does arm 2 beat arm 1, by how much, and which assumption carries the result?** That is what this model produces — a distribution over the arm difference, plus a one-at-a-time sensitivity table that says where the answer is fragile.

It is a queueing and scheduling model. Nothing more.

## 2. What this model does not do — read this before quoting it

| Not modelled | Consequence |
|---|---|
| Hydraulics, currents, tidal exchange | Says nothing about where septage goes once it leaves the tank |
| Treatment, BOD, fecal coliform | Says nothing about the river |
| Disease, exposure, health outcomes | Says nothing about health benefit |
| Calendar time | Model time is working minutes; see §5 |
| Anything geographic | The access-tier marginals are national figures applied to Paco |

**It also does not model trucks being unable to keep up.** Crew utilisation is about 10% (§7). No queue ever forms. Any claim that haulage capacity constrains the programme is *not* supported by this model and must not appear in the paper.

## 3. Files

```
sim/
├── service_sim.py       the model: Params, build_cohort, job_minutes, simulate, summarise
├── run_scenarios.py     the experiment: arm sweep, decomposition, sensitivity, figure
├── requirements.txt     pinned versions, tested 14 Nov 2026
├── README.md            this file
└── outputs/
    ├── arm_sweep.csv        arm 1 vs arm 2 across the sweep
    ├── decomposition.csv    the arm difference split into its two channels
    ├── sensitivity.csv      one-at-a-time sensitivity
    └── fig_arm_sweep.png    the poster figure
```

## 4. How to run it

```bash
# one replicate, every field printed
python sim/service_sim.py

# change one parameter
python sim/service_sim.py --uplift 0.25 --crews 1

# distribution over replicates, with 95% intervals
python sim/service_sim.py --reps 200

# the full experiment and the figure (2–3 minutes on a laptop)
python sim/run_scenarios.py --reps 200 --seed 2026
```

Seeds are explicit and integer, so a judge can reproduce any number exactly.

## 5. Time convention

**Model time is working minutes.** A "day" is 480 minutes of crew time. There are no nights, weekends, or holidays inside the clock, and `days_used` counts *crew-days*, not calendar days.

This matters when reading `days_used = 117`. That is not 117 calendar days of fieldwork — it is the span the block windows impose, since 10 blocks × 12 days = 120, and the last block finishes just inside it. Do not convert it to a calendar date.

## 6. Every parameter, and where it came from

Each value is either **sourced**, a **design choice**, or an **assumption**. The distinction is the point: an assumption is something the pilot would measure.

| Parameter | Value | Status | Basis |
|---|---|---|---|
| `n_households` | 400 | design | Pilot scale for one kilometre |
| `n_blocks` | 10 | design | Blocks served in sequence, 12-day windows |
| `arm_split` | 0.50 | design | 5 blocks per arm; arms assigned by block, not household |
| `base_accept` | 0.55 | sourced | MWSS acceptance, 2025 |
| `uplift` | **swept 0–0.30** | **the unknown** | Not asserted anywhere; the sweep is the result |
| `f3_refusal_arm1` | 0.25 | **assumption** | Share refusing floor work on arrival; arm 1 only |
| `p_under_house` | 0.70 | sourced | IFC 2018 marginal — tank beneath the house |
| `p_narrow_path` | 0.71 | sourced | IFC 2018 marginal — path fits one person |
| `mean_lag_arm1_days` | 5.0 | **assumption** | Booking lag from a schedule card |
| `mean_lag_arm2_days` | 2.0 | **assumption** | Shorter lag after a household visit |
| `window_days` | 12.0 | design | Service window per block |
| `day_minutes` | 480 | assumption | Eight-hour working day |
| `run_days` | 234 | sourced | Budget line: 9 months × 26 days |
| `n_crews` | 2 | design | Swept 1–3 |
| `staff_per_crew` | 4 | design | Driver, two technicians, coordinator |
| `pump_lpm` | 250 | sourced | Mid-range of commercial vacuum units, 200–400 L/min |
| `tank_m3_lo/hi` | 0.5–1.5 | **assumption — contested** | See the note below |
| `transfer_min` | 5.0 | assumption | Portable unit to mother tanker |
| `travel_min` | 3.0 | assumption | Mean inter-household movement |
| `setup_f1` | 10 | assumption | Direct truck access |
| `setup_f2` | 30 | assumption | Narrow path, long hose run |
| `setup_f3` | 75 | assumption | Floor opened, tank beneath house |
| `setup_f3_remediated` | 30 | assumption | Port installed in advance |
| `no_show` | 0.12 | assumption | Household not present; one retry |
| `retry_days` | 3.0 | assumption | Retry lag |
| `wage_day` | ₱944 | sourced | NCR-28 minimum wage ₱755 + 25% on-cost |
| `haul_cost_per_load` | ₱4,700 | sourced | Maynilad published rate |
| `load_m3` | 10.0 | sourced | Tanker capacity |
| `gate_fee_per_m3` | ₱580 | sourced | Ormoc City ordinance benchmark |

### The tank volume discrepancy — stated, not hidden

The verification annex records a **1.58 m³ mean tank volume**. This model draws uniformly from **0.5–1.5 m³, mean 1.0** — deliberately below the annex figure, because a model that overstates volume overstates haulage and gate fees, and the honest direction for an unsourced parameter is downward.

The cost consequence is real: `sensitivity.csv` shows cost per household rising from **₱5,070** at 0.5–1.5 m³ to **₱5,595** at 0.5–2.5 m³ and **₱6,120** at 0.5–3.5 m³. Completion is unchanged, because pump time is a small part of a 55-minute job.

**When the annex figure is used, quote ₱5,600–₱6,100 per household, not ₱5,070.** A judge who reads both documents will notice. Say it first.

## 7. Results

### Arm sweep — 200 replicates, seed 2026

Households served, as a percentage of each arm's 200.

| Visit effect | Arm 1 | Arm 2 | Difference | 95% CI | ₱/hh served |
|---:|---:|---:|---:|---|---:|
| 0 pts | 40.9% | 54.5% | **+13.7** | 13.0–14.3 | 5,699 |
| 5 pts | 40.8% | 59.7% | +18.8 | 18.2–19.5 | 5,461 |
| 10 pts | 40.9% | 64.6% | +23.8 | 23.1–24.4 | 5,253 |
| 15 pts | 40.9% | 69.5% | +28.7 | 28.0–29.3 | 5,070 |
| 20 pts | 40.9% | 74.5% | +33.6 | 32.9–34.3 | 4,894 |
| 25 pts | 40.9% | 79.6% | +38.8 | 38.1–39.4 | 4,734 |
| 30 pts | 40.9% | 84.6% | **+43.8** | 43.2–44.4 | 4,586 |

Three things to notice:

1. **Arm 1 does not move.** By construction its parameters are fixed. This is a sanity check, not a finding.
2. **The difference is positive at zero awareness effect.** At `uplift = 0`, arm 2 still beats arm 1 by 13.7 points. That is the access channel operating alone — the strongest single result here.
3. **Cost per household falls as coverage rises,** because fixed labour is spread over more households. The direction matters: coverage and unit cost improve together, so this is not a trade-off.

### The decomposition — the finding that matters most

Arm 2 changes two things at once: it removes the physical access barrier, *and* it shortens the response lag. Running arm 2 with arm 1's lag isolates the arrival-side channel.

| | Total | Arrival-side | Response speed |
|---|---:|---:|---:|
| `uplift = 0` | +13.7 | **+8.5 (access only)** | +5.2 |
| `uplift = 0.15` | +28.7 | +22.0 (access + awareness) | +6.7 |

At zero awareness effect, **62% of the arm difference is physical access work and 38% is bookkeeping speed.** Response speed contributes a near-constant 5–7 points regardless of the awareness effect.

This is the defensible version of the thesis: access is not merely present, it is the *larger* of the two channels — but roughly a quarter to two-fifths of the effect comes from shortening the gap between booking and arrival, which costs almost nothing and should be described as logistics, not infrastructure.

### One-at-a-time sensitivity at `uplift = 0.15`

| Assumption varied | Completion | Arm difference | ₱/hh |
|---|---:|---:|---:|
| Baseline uptake 0.45 | 46.5% | +26.4 | 5,816 |
| Baseline uptake 0.55 | 55.2% | +28.7 | 5,070 |
| Baseline uptake 0.65 | 64.0% | +31.3 | 4,521 |
| Floor-work refusal 0.00 | 59.6% | **+19.7** | 4,773 |
| Floor-work refusal 0.25 | 55.2% | +28.7 | 5,070 |
| Floor-work refusal 0.50 | 50.8% | **+37.4** | 5,410 |
| No-show 0.00 | 55.4% | +28.3 | 5,054 |
| No-show 0.25 | 54.9% | +29.0 | 5,079 |
| **1 crew** | 55.2% | +28.7 | **3,066** |
| **2 crews** | 55.2% | +28.7 | 5,070 |
| **3 crews** | 55.2% | +28.7 | 7,074 |
| Tank under house 60% | 55.8% | +27.4 | 5,025 |
| Tank under house 80% | 54.6% | +29.9 | 5,115 |
| Block window 5 days | **44.2%** | +34.8 | 3,192 |
| Block window 12 days | 55.2% | +28.7 | 5,070 |

**Two results are robust:** crew count buys no coverage at all (identical completion, cost triples), and the no-show rate barely matters. **One result is fragile:** the arm difference runs from 19.7 to 37.4 points depending on the floor-work refusal assumption. That single number carries the finding, and it is precisely what the pilot exists to measure.

This is not a weakness of the model. It is the model doing its job — naming the one number that must be observed rather than assumed.

## 8. Reading the outputs — four traps

**Trap 1 — cost per household rewards serving fewer households.** A 5-day window gives ₱3,192/hh, lower than the 12-day window's ₱5,070. It also serves 44.2% instead of 55.2%. The ratio looks better because the programme stopped earlier. **Never quote cost per household without the coverage figure beside it.**

**Trap 2 — the 40.9% level is an artefact.** It is the product of four assumptions: refusal 0.25, arm-1 lag 5 days, 12-day windows, baseline 55%. Do not write "we predict 41% take-up." Write the difference and its sensitivity.

**Trap 3 — the model is not capacity-constrained.** Median queue wait is 0 minutes and the 90th percentile is under 4 minutes, across all replicates. One crew does the same work as three. Any narrative about trucks falling behind is unsupported.

**Trap 4 — the model does not know anything about Paco.** The 0.70 / 0.71 access marginals are IFC national figures. Applying them to ten blocks in Paco is an assumption of transferability, and should be labelled as one.

## 9. Validation

A judge — or a teammate on the morning of submission — can run these in five minutes.

| Check | Expected |
|---|---|
| Conservation | `served + no_booking + late_booking + no_show_final = 400` exactly |
| Reproducibility | Same `--seed` gives byte-identical output |
| Interval width | 200 replicates should give ~±0.6 pts on the arm difference |
| Monotonicity | Arm 2 rate must rise with `uplift`; arm 1 must not move |
| Degenerate cases | `--uplift 0 --crews 1` should not error, and completion should be unchanged from `--crews 3` |

At seed 0 with defaults, the conservation check reads:

```
served 212 + no_booking 174 + late_booking 13 + no_show_final 1 = 400
```

## 10. What the paper may claim

**May claim**

- Under a stated set of assumptions, access remediation raises completion by 8.5 points *before any awareness effect*.
- Response speed adds a further 5–7 points and costs nothing.
- One crew suffices for 400 households in 117 crew-days; the second crew doubles labour cost for zero coverage gain.
- Cost per household served falls from ₱5,699 to ₱4,586 as coverage rises from 47.7% to 62.8%.
- The arm difference is most sensitive to the floor-work refusal rate, which is therefore the quantity the pilot must measure.

**May not claim**

- Any absolute take-up rate as a prediction.
- Any effect on the river, on water quality, or on health.
- That haulage capacity is or is not sufficient (the model was never capacity-constrained).
- That these results are specific to Estero de Paco.

## 11. Reproducing the figure

```bash
python sim/run_scenarios.py --reps 200 --seed 2026
```

`fig_arm_sweep.png` is written at 180 dpi, 11 × 4.2 inches, two panels. Left: arm 1 and arm 2 against the visit effect, with 95% bands and the 55% citywide acceptance line. Right: cost per household, actual versus fully staffed, with the environmental-charge yield band drawn for reference.

The figure is deliberately a *sensitivity display*, not a headline number. A single point estimate would invite the question "how do you know?" — and the honest answer is that you do not, which is why the paper reports a sweep.
