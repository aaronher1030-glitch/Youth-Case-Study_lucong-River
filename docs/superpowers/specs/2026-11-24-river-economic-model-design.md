# Lucong River Intervention Model — Design Specification

**Date:** 24 November 2026  
**Status:** Approved design for implementation planning; synthetic-census mode added 24 November 2026  
**Competition deadline:** 5 December 2026, 11:59 PM PHT

## 1. Purpose and decision

Build an auditable mathematical and economic decision model for a 12-month, 1-km Lucong River pilot. The model will compare shed-service configurations and realistic alternatives, enforce the competition constraints, quantify uncertainty, and recommend the least-lifecycle-cost feasible design.

The recommendation must satisfy all of the following:

- Pilot duration no greater than 12 months.
- Total 12-month cash requirement no greater than PHP 10,000,000.
- At least 70% of spending assigned to one focus stream; the shed-service design is expected to assign 100%.
- Predicted station fecal coliform no greater than 8,000 MPN/100 mL in at least 80% of joint uncertainty draws.
- All process, capacity, land, safety, and legal constraints satisfied.

The model is a cost-effectiveness and decision-support model. It does not monetize health or ecosystem benefits and must not be described as proving that the intervention works.

## 2. Evidence basis and limitations

The methodology is grounded in the supplied project materials:

- `WEBINAR_LESSONS_2027_KICKOFF.md`: whole-system balances, explicit objective, counterfactual, trade-offs, repeatability, and honest limitations.
- `schedule/_kit_text.txt`: 1-km reach, 12 months, PHP 10 million, at least 70% focus-stream allocation, baseline/target requirements, and national scaling.
- `MODEL_SPEC_LUCONG.md` and `sim/lucong_model.py`: the existing load, process, cost, and enumeration prototype.
- `docs/DATA_BRIEF_LUCONG.md`: current parameter provenance, budget lines, and missing evidence.
- `docs/drafts/SECTION2_LUCONG_RIVER_SUBMISSION.md`: study reach, baseline water quality, and source-diagnosis uncertainty.
- PSA OpenSTAT swine inventory: province-by-quarter context only; it does not identify Concepcion barangays, individual sheds, head counts, or drainage connections.
- Bamban CLUP piggery inventory: an analogue for spatial clustering only; it is not a Concepcion reach census.

No public source reviewed identifies the sheds draining to the monitored 1-km reach. Public statistics may bound regional context, but they must not be allocated to this reach as if observed. The original webinar screenshots, slides, recording, and kit PDF are not present in the workspace. Exact screenshot content cannot be independently verified. The implementation must rely on the surviving transcription and must not claim that the original screenshots were reviewed.

## 3. Scope

### Included

- The 1-km study reach downstream from Santiago Bridge.
- Shed-service configurations using either a verified shed census or an explicitly synthetic prior-predictive census.
- Load generation, transport/die-off, station-equivalent source share, and capture.
- Seeded synthetic-census scenarios and prior-predictive summaries when observed shed data are unavailable.
- Manure/slurry process balances, digester sizing, tanker throughput, biogas, compost nutrients, and land requirement.
- 12-month cash cost and lifecycle annualized cost.
- Alternatives evaluated on the same station-level functional unit.
- Feasible-design enumeration, uncertainty, sensitivity, and measurement priorities.
- Machine-readable outputs and competition-ready summary artifacts.

### Excluded

- Detailed two-dimensional hydrodynamics, flood routing, sediment transport, or disease transmission.
- Claimed health, fisheries, irrigation, or property benefits.
- Calibration claims before paired field observations exist.
- Automatic transfer of parameters to other rivers.
- A solver-dependent mixed-integer optimization model.

## 4. System architecture

The implementation will contain five independently testable modules.

### 4.1 Evidence and parameter register

Every input will carry:

- Stable parameter identifier.
- Value or range and unit.
- Status: measured, sourced, derived, assumption, or missing.
- Source file, citation, or measurement record.
- Date and responsible collector where applicable.
- Distribution or scenario range used in uncertainty analysis.
- Notes on dependence or correlation with other inputs.

The model will refuse to silently replace missing values with undocumented defaults.

### 4.2 River load and transport module

This module converts source activity into station-equivalent load and predicts the endpoint concentration under each candidate design.

### 4.3 Process and capacity module

This module calculates manure, washwater, slurry, volatile solids, biogas, nutrient output, land requirement, hydraulic retention, and transport capacity.

### 4.4 Economic module

This module calculates 12-month cash cost, lifecycle net present cost, annualized cost, unit costs, and fee-affordability scenarios.

### 4.5 Decision and uncertainty module

This module enumerates candidate designs, applies hard constraints, evaluates target probability, ranks feasible designs, performs sensitivity analysis, and produces the recommendation and figures.

## 5. Required inputs

### 5.1 Shed census — observed or synthetic

#### 5.1.1 Observed census

The observed census file will contain one row per shed with:

- Unique shed identifier.
- Barangay and location or coordinates.
- Head count and count date.
- Source and collector.
- Confirmation that the shed drains to the study reach, or an explicit unknown flag.
- Participation eligibility and known access constraints.

The model will use the supplied census instead of the current 15-shed assumption. If some sheds have unknown drainage connection, the base case will include only confirmed sheds and sensitivity scenarios will include the unresolved sheds.

#### 5.1.2 Synthetic prior-predictive census

Until an observed census is supplied, the model may run in `synthetic` mode. This mode generates reproducible scenario censuses; it does not estimate or identify actual sheds.

The initial declared prior is:

- Number of sheds: uniform integer from 12 through 20, inherited from the existing prototype's planning range.
- Heads per shed: triangular distribution with minimum 8, mode 15, maximum 25, inherited from the existing prototype's planning range.
- Drainage-connection probability: equal-weight discrete scenarios of 0.00, 0.25, 0.50, 0.75, and 1.00 because no reach-level connection data exist.
- Barangay: assigned between Santiago and Alfonso with equal probability.
- Default seed: 2026.
- Default scenario count: 200; the CLI must expose this value.
- Within-scenario joint uncertainty: at least 20,000 draws for production runs.

Every generated row must carry `source="synthetic"` and a scenario identifier. Outputs must include the generating prior, seed, scenario count, and a prominent `SYNTHETIC — NOT FIELD-VERIFIED` label. The public PSA and Bamban data must not be used to assign Concepcion shed counts or head counts; they remain contextual evidence only.

Synthetic results are prior-predictive and conditional on the declared prior. They cannot support a site-specific reliability claim until the census, drainage links, and source attribution are verified.

### 5.2 River and source parameters

Required parameters include:

- Baseline station concentration `C0` in MPN/100 mL, with provenance and uncertainty.
- Discharge `Q` in m3/s at a stated location, date, and flow condition.
- Per-head fecal-coliform generation rate `e` in MPN/head-day, with a cited range.
- Transport/die-off delivery factor `eta` for each source group, or a documented station-equivalent source-share estimate.
- Participation, collection reliability, and treatment-retention fractions.
- Upstream/background concentration or an independently estimated non-target load for source reconciliation.

Until field measurements exist, flow and source share will be represented by pre-declared bounded scenarios. The model will not present one unmeasured flow as fact.

### 5.3 Process parameters

Required parameters include:

- Manure yield per head-day.
- Washwater use per head-day.
- Dry matter and volatile-solids fractions.
- Anaerobic destruction fraction and methane yield.
- Methane fraction and heating values.
- Nutrient fraction and allowable nutrient application rate.
- Digester module volume, hydraulic retention time, tanker volume, working days, trips per day, and utilization allowance.

Each parameter must have a source or an explicit assumption status.

### 5.4 Cost parameters

Required cost lines include:

- Digester modules and gas equipment.
- Tanker(s), carts, pumps, and drums.
- Composting pad and site works.
- Meters and sampling equipment.
- Staff, fuel, maintenance, sampling, administration, training, permits, and manifest system.
- Shed upgrades, replication preparation, and contingency.
- Replacement schedule and residual value, if any.

The 12-month budget must reconcile line by line to PHP 10 million. The older 24-month data brief must not be used as the pilot cost basis without conversion to 12 months.

## 6. Mathematical model

### 6.1 Unit conventions

- Concentration: MPN/100 mL.
- Discharge: m3/s.
- Load: MPN/day.
- Time: day unless stated otherwise.
- Cost: PHP at documented 2026 planning prices.

The conversion from concentration and discharge to daily load is:

\[
L_0 = C_0 \times Q \times 86{,}400 \times 10{,}000
\]

where `C0` is MPN/100 mL and `L0` is MPN/day.

### 6.2 Source load

For shed `i`:

\[
L_i = h_i e_i
\]

Total generated target-source load:

\[
L_{gen} = \sum_i L_i
\]

Station-equivalent target-source load:

\[
L_{target} = \eta L_{gen}
\]

where `eta` is the dimensionless fraction delivered to the station after transport and die-off. If source groups have materially different transport paths, `eta` will be applied by group rather than as one value.

The target-source station share is:

\[
r = \frac{L_{target}}{L_0}
\]

If `r > 1`, or if an independent background estimate makes the source loads incompatible with `L0`, the model will raise a reconciliation error. It will not cap `r` silently.

### 6.3 Capture effectiveness

Capture is decomposed into:

\[
c = p_{enroll} \times p_{collect} \times p_{retain}
\]

- `p_enroll`: fraction of eligible sheds enrolled and active.
- `p_collect`: fraction of scheduled loads actually collected and contained.
- `p_retain`: fraction of collected load retained by the treatment/disposal chain rather than reaching the river.

This prevents manifest coverage alone from being treated as river-load reduction.

### 6.4 Endpoint concentration

Because `r` is defined at the station after transport and die-off:

\[
C_{end} = C_0(1-r c)
\]

Annual station-equivalent load prevented is:

\[
\Delta L = r c L_0 \times 365
\]

For reporting in trillions of MPN per year:

\[
\Delta L_{12} = \frac{\Delta L}{10^{12}}
\]

A required check is:

\[
C_0(1-r c) \le 8{,}000
\quad\Longleftrightarrow\quad
r c \ge 0.5
\]

At 95% retention-adjusted capture, this requires `r >= 0.526`. The model will display this threshold explicitly.

### 6.5 Source reconciliation

Where paired upstream/downstream samples or source-apportionment estimates exist, the model will calculate an independent top-down source-share estimate and compare it with the bottom-up estimate. Material disagreement will be reported as unresolved source attribution. It will not be hidden by fitting or by selecting whichever estimate gives the preferred answer.

### 6.6 Process and capacity balances

The process module will calculate at least:

\[
M = \sum_i h_i m_i
\]

\[
W = \sum_i h_i w_i / 1000
\]

\[
V_{slurry} = M/\rho + W
\]

\[
VS_{in} = M \times dm \times vs
\]

\[
VS_{destroyed} = VS_{in} \times \eta_{VS}
\]

\[
CH_4 = VS_{destroyed} \times Y_{CH_4}
\]

\[
V_{biogas} = CH_4/\phi_{CH_4}
\]

\[
LPG_{eq} = CH_4 \times 35.8/46
\]

Hydraulic feasibility requires:

\[
V_{digester} \ge V_{slurry} \times HRT
\]

Transport feasibility requires:

\[
Trips_{week} \le Tankers \times Workdays \times Trips_{day} \times Utilization
\]

Nutrient/land feasibility requires:

\[
A_{land} = N_{annual}/N_{rate} \le A_{available}
\]

The implementation will report a mass-balance closure check for manure dry matter, volatile solids, gas, digestate/compost, and water. A closure difference greater than 5% will fail verification unless a documented process pathway explains it.

### 6.7 Economic model

The 12-month cash requirement is:

\[
Cash_{12} = CAPEX + OPEX_{12} + Contingency
\]

Lifecycle net present cost over the analysis period is:

\[
NPC = CAPEX + \sum_{t=1}^{T}\frac{OPEX_t + Replacement_t - Salvage_t}{(1+d)^t}
\]

Annualized lifecycle cost is:

\[
EAC = NPC \times \frac{d(1+d)^T}{(1+d)^T-1}
\]

The base case will use zero compost and biogas revenue. Verified credits may appear only in sensitivity scenarios.

Reported unit metrics will include:

\[
PHP/shed\text{-}month = EAC/(Sheds \times 12)
\]

\[
PHP/(10^{12}\ MPN/year) = EAC/\Delta L_{12}
\]

\[
PHP/kg\ VS\ diverted = EAC/(VS_{diverted}/365)
\]

The fee-affordability calculation will use full annualized cost and eligible head-months. It will be reported separately from technical feasibility.

### 6.8 Alternatives

At minimum, compare:

- Shed service.
- Do-nothing/enforcement-only counterfactual.
- Household septage service, if its targetable source share can be bounded.
- In-stream screen/dredging, with removal limits and blockage/disposal costs stated.

Each alternative must use the same station-level functional unit and show whether its inputs are measured, sourced, assumed, or missing. An alternative with unknown cost will be shown as a range, not assigned a fabricated point estimate.

## 7. Design search and decision rule

The declared discrete design space will include:

- Service sets formed from non-empty combinations of confirmed eligible barangay clusters; for this reach the only clusters are Santiago and Alfonso, giving at most three service sets.
- Number of digester modules.
- Number of tankers.
- Number of carts and pumps.
- Service frequency.
- Participation/collection strategy where it changes cost or capacity.

The model will enumerate every combination in the declared design space and record the count of evaluated designs. A candidate is feasible only if:

- It satisfies every hard constraint in Section 1.
- Process and land balances pass.
- Its 12-month cash requirement is within budget.
- Its joint Monte Carlo target probability is at least 80%.
- No required input is missing without an explicit scenario treatment.

Among feasible candidates, the recommendation is the one with the lowest `EAC`. Ties will be broken by lower 12-month cash requirement, then greater eligible-shed coverage. The model will also report the cheapest design at several reduction levels to produce a cost–reduction frontier.

Rejected near-feasible designs will be retained with the exact reason for rejection. If no candidate reaches the 80% threshold, the model will report that no feasible design exists under the declared inputs, identify the binding constraints, and show the least-cost near-feasible designs. It will not lower the threshold after seeing the results.

## 8. Uncertainty and sensitivity

The analysis will include:

1. Deterministic base case.
2. Transparent low/base/high scenario bounds.
3. Seeded Monte Carlo analysis with at least 20,000 joint draws and seed 2026.
4. One-at-a-time tornado analysis.
5. Decision-flip analysis showing which input changes can alter the selected design or the 80% feasibility result.
6. In synthetic mode, a prior-predictive analysis across the declared scenario censuses, reporting connected-head and source-share distributions, selected-design frequencies, target-probability ranges, invalid-scenario counts, and binding constraints.

Distributions will be documented. Triangular distributions may be used only when a mode and lower/upper bounds are justified. Positive rates may use lognormal distributions only when the source supports that form. Otherwise, discrete scenarios will be used.

Shared causes of uncertainty will be represented through scenario blocks or declared correlation. The analysis will not assume independence where variables share a measurement or source. If any draw produces `r > 1` or a negative physical quantity, that draw is physically inconsistent. The model will report the invalid-draw fraction and withhold the target-probability claim until the input ranges or model structure are revised; it will not truncate invalid draws to manufacture a probability.

A lightweight value-of-information layer may rank measurements by their ability to change the design decision, target probability, or dominant constraint, relative to measurement cost. It will be labeled as decision value, not as monetized environmental benefit.

## 9. Verification and acceptance tests

The implementation must pass all of the following:

- Unit conversion tests, including MPN/100 mL to MPN/day.
- `c = 0` gives `C_end = C0`.
- `r = 0` gives no predicted reduction.
- Increasing `c` or `r` cannot increase `C_end`.
- For fixed source loads, increasing `Q` cannot increase the predicted concentration reduction.
- `r > 1` raises a reconciliation error and is never silently capped.
- Digester, tanker, land, budget, duration, and focus-stream constraints cannot be violated by a selected design.
- The selected design meets the 80% target-probability threshold under the declared uncertainty model.
- Mass-balance closure is within 5% or an exception is documented.
- Fixed seed reproduces the same results.
- One selected design is independently recalculated in a spreadsheet and matches within documented rounding.
- Every number in the decision brief traces to an input-register row or a formula output.
- No output claims calibration, compliance with 200 MPN/100 mL, health benefit, or transferability without new evidence.

## 10. Intuitive viewer

The model will include a lightweight interactive viewer built with Streamlit 1.67.0 and Plotly 7.1.0. The viewer is a presentation and exploration layer only; all calculations remain in the tested Python modules and must also run headlessly.

The viewer must show an `OBSERVED CENSUS` or `SYNTHETIC — NOT FIELD-VERIFIED` mode label on every tab. Synthetic mode must display the declared prior and seed before any result and must not use wording that implies actual sheds were counted.

The viewer will contain five tabs:

1. **Overview:** a simple reach schematic from Santiago Bridge through the 1-km study reach, source clusters from the census, KPI cards for the selected design, 12-month cash, annualized cost, predicted endpoint, target probability, and annual load prevented. In synthetic mode, add a prior-predictive distribution of connected heads and selected-design frequencies.
2. **Assumptions:** grouped controls for flow, source share or source-generation parameters, participation, collection reliability, retention, process inputs, and costs. Every control displays its unit, evidence status, source, and allowed range. Sourced values may be changed only as explicit scenarios and must be visually distinguished from the base case.
3. **Designs:** a sortable/filterable table of candidates with feasibility colors plus text labels, violation reasons, cost, reduction, capacity, and land use. A cost–reduction frontier will show dominated and feasible designs.
4. **Compare:** side-by-side comparison of up to three designs, including process balances, constraints, cost breakdown, and uncertainty.
5. **Uncertainty and methods:** endpoint distribution, target threshold, tornado or decision-flip chart, equations, validation status, provenance, and downloads.

The interface will use plain-language labels, explicit units, visible assumption status, and text in addition to color. It will never present an assumption as a measured fact. A static Plotly HTML export will provide a no-server fallback containing the base-case results and figures; it will not pretend to rerun the model interactively.

GitHub comparators reviewed on 24 November 2026 informed this layer:

- `USEPA/RBEROST` and `dkauf42/bayota`: separate load, treatment-efficiency, cost, and target inputs; minimum-cost decisions; scenario sweeps.
- `pyswmm/pyswmm` and `pyswmm/swmmio`: scripted scenarios and tidy tabular inputs/outputs.
- `lanl-ansi/WaterModels.jl`: explicit problem specification separated from solver execution.
- `Rekin226/aquascope`: reach-level views, provenance, observed-versus-modelled labels, and shareable state.

SWMM, PySWMM, ClearWater-riverine, Julia solvers, and BayOTA will not be integrated into the core. They require data, calibration, or solver infrastructure beyond the competition scope. Their useful ideas will be borrowed as design patterns only.

Viewer acceptance requires Streamlit `AppTest` coverage for tab rendering, invalid-input messages, scenario reset, candidate filtering, and download generation, followed by a headed browser check of the golden path and key edge cases.

## 11. Outputs

### Machine-readable

- `parameter_register.csv`
- `candidate_designs.csv`
- `selected_design.json`
- `monte_carlo_summary.csv`
- `sensitivity.csv`
- `alternatives.csv`
- `synthetic_census_example.csv` and `synthetic_scenarios.csv` in synthetic mode
- `prior_predictive_summary.json` in synthetic mode
- `verification_report.txt`

### Figures

- Cost–reduction frontier.
- Endpoint-concentration distribution with the 8,000 threshold.
- Tornado or decision-flip sensitivity figure.
- Existing two-panel competition figure updated from verified outputs.

### Human-readable

- One-page decision brief.
- Short methods note with equations, assumptions, limitations, and reproducibility command.
- Competition-ready equation block, feasible-design table, and two-panel figure.
- Interactive Streamlit viewer and static Plotly HTML export.

## 12. Claim boundaries

The model may state that, under declared assumptions, a design is the least-lifecycle-cost feasible design among those enumerated and has a stated probability of meeting the 8,000 target. In synthetic mode it must add that the probability is conditional on the declared synthetic-census prior and is not a field-verified reliability estimate.

The model may not state that:

- The river will comply with the 200 MPN/100 mL standard within the pilot.
- The intervention is empirically proven before it operates.
- The model is calibrated before field validation.
- A health, fisheries, or downstream benefit has been demonstrated.
- Results transfer to another river without repeating the census and source assessment.

## 13. Completion criteria

The implementation is complete when:

- The verified census is loaded, or synthetic mode runs with the declared prior and produces prior-predictive outputs without claiming observed sheds.
- All five modules run from one documented command in either observed or synthetic mode.
- All acceptance tests pass.
- Outputs are reproducible with a fixed seed.
- The selected design and all rejected constraints are traceable.
- The decision brief and competition artifacts contain no placeholders or unsupported claims.
- The interactive viewer renders all five tabs, distinguishes base values from scenarios, explains rejected designs, and passes `AppTest` plus a headed browser check.
