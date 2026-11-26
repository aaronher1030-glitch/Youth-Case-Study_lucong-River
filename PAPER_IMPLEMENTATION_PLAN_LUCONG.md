# Lucong River Case Study — Step-by-Step Paper Implementation Plan

**Working paper title:** *Eighty Times the Limit: A Shed-Level Manure Service and Load-Balance Model for the Lucong River, Concepcion, Tarlac*  
**Competition scope:** One **1-km reach**, a **12-month proof-of-concept pilot**, and a total cost of **no more than Php 10 million**.  
**Focus rule:** At least **70%** of spending must support one focus stream. The current shed-service design assigns **100% to Stream 2: commercial/industrial pollution**, specifically commercial piggery waste.  
**Current direction:** Diagnose fecal loading, test whether piggery manure is the dominant controllable source, and propose a sealed-sump → collection → manifest → digestion → compost service.  
**Phase I reminder shown in the meeting:** December 5, 2026, 11:59 PM PHT; Case Study Paper, PDF, and Digital Poster (JPG/PNG). Confirm the current official deadline, email, and file rules before submission.

## Source documents this plan builds on

- [Current paper draft v1.1](docs/drafts/2026-11-23-paper-v1.1.md) — latest paper structure, design, model, and 12-month budget.
- [Site profile and root-cause diagnosis](docs/drafts/SITE_PROFILE_LUCONG_RIVER.md) — profile evidence, DPSIR diagnosis, and open field items.
- [Data brief](docs/DATA_BRIEF_LUCONG.md) — parameter provenance and unresolved evidence.
- [Approved model design](docs/superpowers/specs/2026-11-24-river-economic-model-design.md) — model boundaries, uncertainty rules, and decision constraints.

> **Use the current paper and approved model design over older drafts.** In particular, do not mix in the older 24-month budget, 2,000/200 targets, 30 m³ biogas estimate, 18 kg LPG estimate, Estero de Paco material, or Stream 3 cleaning proposal.

---

# Part 1 — Summary of Lessons from the Meeting

## 1. Start with the environment, then the law, then the cost

- First establish **what is wrong, how bad it is, where it comes from, and how it is measured**.
- Then identify **who is responsible and which rules apply**.
- Only then determine **what the pilot costs, who pays, and who operates it**.
- For Lucong, the order is:
  1. Fecal-coliform exceedance and source pathways.
  2. Piggery permits, sewerage, legal authority, and responsibilities.
  3. Collection, digestion, composting, budget, and fees.

## 2. Keep the study narrow enough to finish

- One defined 1-km reach.
- One main pollution stream: commercial piggery waste.
- One service concept.
- One measurable station-level outcome.
- One 12-month budget.
- Scaling to other reaches is a blueprint, not part of the pilot claim.

## 3. The six proposal flaws are the paper’s review checklist

- **Too big:** Do not propose cleaning the whole Lucong or Chico river system.
- **Over budget:** Keep the 12-month cash requirement at or below Php 10 million.
- **Nothing to measure:** Every objective needs a baseline, unit, target, method, and date.
- **Treats a symptom:** Removing visible trash or odor does not necessarily stop fecal loading.
- **No people:** Name the shed owners, MENRO, barangays, operators, payer, maintainer, and regulator.
- **No comparison:** Compare the service against realistic alternatives and a do-minimum baseline.

## 4. Evidence must have provenance

- Separate **published evidence**, **team measurements**, **derived values**, **assumptions**, and **missing data**.
- Every important number needs a source, date, unit, and status.
- The published **16,000 MPN/100 mL** value is documentary evidence, not a new team baseline.
- The exact station, quarter, sample count, and classification behind that row still require confirmation.

## 5. Match the method to the question

- A survey can measure reported practices, willingness to participate, and fee affordability.
- It cannot prove the actual fecal load or the effect of the service.
- Source attribution requires drain mapping, paired water samples, shed census, and flow information.
- Cost-effectiveness requires process balances, itemized costs, alternatives, and uncertainty analysis.

## 6. Diagnose the source and pathway, not only the visible condition

- Use the chain **driver → pressure → state → impact → response**.
- The current working diagnosis is:
  - **Driver:** unmonitored commercial piggery operations.
  - **Pressure:** manure and washwater entering drains, banks, or the channel.
  - **State:** fecal coliform at 16,000 MPN/100 mL while BOD and DO remain within limits.
  - **Impact:** potential contact, irrigation, amenity, and ecosystem risks; several impacts remain unquantified.
  - **Response gap:** rules regulate farms, but the reviewed instruments do not provide a manure-haulage service.
- Household sewerage remains a live alternative explanation.

## 7. Name the whole system

- Identify who generates the waste, who collects it, who owns the land, who permits the facility, who pays, who operates, and who maintains it.
- The proposed service cannot be described as feasible until these roles are confirmed.
- “The LGU” or “the community” is not a sufficient owner statement.

## 8. Compare options on the same basis

- Compare:
  - Do-minimum/current practice.
  - Enforcement alone.
  - On-farm digestion without haulage.
  - Piped collection/treatment.
  - In-stream interception.
  - The proposed shed-level collection and centralized digestion service.
- Use the same functional unit and constraints.
- The current paper argues that the service is the **least-cost feasible option**, not the highest-scoring option in an arbitrary weighted matrix.

## 9. Models support decisions; they do not prove field performance

- Use the load balance to show how capture and source share affect station concentration.
- Use process balances to size digesters, tankers, gas equipment, compost, and land.
- Use lifecycle costing to compare designs over time.
- Report uncertainty and sensitivity.
- Do not call model outputs “measured results” or claim calibration before paired field observations exist.

## 10. The contribution is the service, not the digester

- Covered digesters already exist.
- The proposed contribution is the coupling of:
  - Sealed containment,
  - Scheduled collection,
  - A manifest for every load,
  - Central digestion,
  - Compost/biogas return,
  - Permit-condition accountability.
- The paper must support this novelty claim with a documented comparison of existing rules and services.

## 11. State limits before the judges find them

- The **8,000 MPN/100 mL** target is conditional on the sheds’ share of the load and capture performance.
- The **200 MPN/100 mL** standard is not promised.
- The 15-shed census is an assumption until verified.
- The tanker price lacks a written quotation.
- The authority to attach waste-service conditions to permits needs confirmation.
- The AI declaration awaits the organizer’s ruling.

## 12. Keep the paper, poster, and presentation numerically identical

- Use one locked set of numbers.
- Label each value as **published**, **measured**, **derived**, **assumed**, or **missing**.
- Use the same 1-km boundary, baseline, target, budget, and timeline everywhere.
- The meeting flags more than 2,200 words as a pitfall; cut background before cutting evidence and analysis.

---

# Part 2 — Locked Research Identity and Current Decisions

## Primary research question

**Which source contributes most to the fecal-coliform load at the Santiago Bridge monitoring station, and can a shed-level manure collection, digestion, and compost service reduce the station concentration to a conditional target of 8,000 MPN/100 mL within 12 months and Php 10 million?**

## Secondary questions

1. What are the physical and social conditions of the monitored 1-km reach?
2. How many sheds and animal heads drain to the reach?
3. What fraction of the station fecal load do those sheds contribute?
4. What capture rate is operationally achievable?
5. Which service design is feasible and least-cost under the competition constraints?
6. Who permits, pays, operates, maintains, and monitors the service?
7. What evidence would falsify the piggery-led diagnosis?

## Central argument

- The Lucong’s published water-quality pattern indicates fecal loading rather than a strong industrial oxygen-demand signal.
- Commercial piggery waste is the leading controllable-source hypothesis, but its share is not yet measured.
- A service that contains, collects, manifests, treats, and returns manure addresses the gap between farm-level regulation and actual waste removal.
- The station-level benefit is conditional on source share, capture, flow, and participation.

## Evidence-status table for the paper

| Item | Current value/decision | Status | How the paper should describe it |
|---|---|---|---|
| River | Lucong; “Lucung” in some LGU records | Published | Use Lucong and note the spelling variant if useful |
| Monitored reach | 1.0 km downstream from Santiago Bridge | Derived from mapping | Confirm exact endpoints and GPS before final submission |
| Full bridge-to-bridge reach | 1.52 km | Derived | Context only; not the pilot boundary |
| Barangays | Santiago and Alfonso, Concepcion, Tarlac | Published | State as site context |
| Population | 15,220 residents | Published, 2020 | Cite PhilAtlas |
| Households | 3,148 | Published, 2015 | Do not label as 2020 |
| Fecal coliform | 16,000 MPN/100 mL | Published; provenance incomplete | “The EMB report lists…” until row provenance is confirmed |
| Reference limit | 200 MPN/100 mL | Published in DAO 2016-08 | Confirm applicable classification before calling the reach Class C |
| BOD / DO / pH / temperature | 5 mg/L / 6.7 mg/L / 7.83 / 30.4 °C | Published | Use to support the fecal-loading argument |
| Main source | Commercial piggery manure | Working hypothesis; medium confidence | “The leading hypothesis…” until field attribution |
| Sewerage | No sewer network reported | Missing written confirmation | Verify with LGU/MENRO before stating as settled |
| Sheds on reach | 15 in the current design | Assumption | Label as planning case until census |
| Heads per shed | 15 in current paper; 12 in older brief | Conflict to resolve | Reconcile before freezing process and cost numbers |
| Design | 3 × 25 m³ digesters, 2,000-L tanker, 2 carts, compost pad | Current draft design | Subject to census, flow, quotations, and permits |
| 12-month budget | Php 6,837,000 | Current draft estimate | Itemize and label unquoted lines |
| Station target | 8,000 MPN/100 mL | Conditional model target | State the source-share/capture condition |
| Compliance | 200 MPN/100 mL | Not achieved by the proposed claim | Do not promise compliance |
| Novelty | Permit–manifest–haulage coupling | Proposed contribution | Support with legal/service comparison |

---

# Part 3 — PPT Conversion Map

Use **one message, one main visual, and 3–5 bullets per slide**.

| Slide | Title | Required content | Visual | Paper source |
|---|---|---|---|---|
| 1 | Eighty Times the Limit | Title, site, team, adviser | Lucong photo with reach marked | Title/Abstract |
| 2 | The problem is specific | 16,000 vs 200; BOD and DO pass | Water-quality bar chart | Introduction/Baseline |
| 3 | One reach, one year, one budget | 1 km, 12 months, Php 10M, Stream 2 | Boundary map + constraint icons | Scope |
| 4 | Target-site profile | Santiago/Alfonso, population, land use, access, services | Annotated map | Site Profile |
| 5 | Root diagnosis | Piggery hypothesis, sewerage alternative, source pathway | DPSIR/causal-chain diagram | Root Diagnosis |
| 6 | What Month 1 must prove | Census, drains, paired samples, flow, permissions | Falsification-test table | Diagnosis/Methods |
| 7 | The proposed service | Sump → tanker → manifest → digester → compost/field | Process-flow diagram | Proposed Plan |
| 8 | Why a service, not only a rule | Regulatory gap and failed/limited alternatives | Comparison table | Options/Legal |
| 9 | How the model works | C = C₀(1 − s·c), source share, capture, flow | Model schematic | Methodology |
| 10 | Conditional target | 8,000 only if source share/capture support it | Sensitivity/uncertainty chart | Model Results |
| 11 | Design and budget | 15-shed planning case, 3 digesters, Php 6.837M | Budget table + 70/30 check | Feasibility |
| 12 | Twelve-month implementation | Verify, build, operate, audit, hand over | Gantt chart | Implementation |
| 13 | Risks and responsibilities | Methane, spills, land/nutrients, safety, owner | Risk/role matrix | Implications |
| 14 | Contribution and next decision | Permit–manifest service; approve conditional pilot | Three takeaways | Conclusion |

---

# Part 4 — Step-by-Step Paper Outline

## Section 0 — Title Page and Front Matter

### Required parts
- Final paper title.
- School, team number, names, and roles.
- Adviser.
- Submission date.
- Study location.
- Abstract and keywords according to the official template.
- AI declaration according to the organizer’s ruling.

### Focus
- Verified names and affiliations.
- A title that matches the actual study.

### Do not include
- Unverified placeholders in the submitted file.
- A title that promises river-wide cleanup or compliance.

### Done when
- Every front-matter field is complete and verified.

### PPT use
- Slide 1.

---

## Section 1 — Abstract

### Required parts
- **Problem:** published fecal coliform of 16,000 MPN/100 mL at the Lucong station, 80 times the 200 reference value.
- **Diagnosis:** fecal-loading pattern; piggery manure is the leading controllable-source hypothesis, with sewerage as an alternative.
- **Proposal:** shed-level containment, collection, manifest, digestion, and compost service.
- **Method:** source attribution, load balance, process/capacity balances, lifecycle costing, alternatives, and uncertainty.
- **Conditional outcome:** 8,000 MPN/100 mL only if measured source share and capture support it.
- **Feasibility:** current 15-shed planning case costs Php 6.837 million over 12 months.
- **Contribution:** a traceable waste service linked to permits and manifests.
- **Limitation:** census, drainage links, flow, and source share remain unverified.

### Writing rule
- Distinguish **published baseline**, **model prediction**, and **proposed activity**.
- Do not state that the pilot has already reduced pollution.

### PPT use
- Speaker notes or closing summary.

---

## Section 2 — Introduction and Scope

### Required parts
1. **Local problem**
   - Lucong River, Concepcion, Tarlac.
   - Published fecal-coliform exceedance.
   - Why the issue matters to Santiago and Alfonso.
2. **Specific failure**
   - Fecal coliform fails while BOD, DO, pH, and temperature pass.
   - The pattern points to fecal loading, not conventional high-oxygen-demand industrial effluent.
3. **Research gap**
   - No verified reach-level shed census.
   - No measured source apportionment.
   - No demonstrated haulage service linking farm permits to waste removal.
4. **Objective**
   - Diagnose the dominant controllable source and design a feasible service.
5. **Research questions**
   - Use Part 2.
6. **Scope**
   - 1 km downstream of Santiago Bridge.
   - 12 months.
   - ≤Php 10 million.
   - Stream 2 focus.
7. **Significance**
   - A measurable station-level pilot.
   - A cost curve and service template for other reaches.
8. **Brief context**
   - Only literature needed to justify the method, legal gap, or technical feasibility.

### Focus
- The specific decision the study supports.

### Do not focus on
- A long national history of water pollution.
- All possible pollutants or all river users.
- Whole-basin cleanup.

### Done when
- The problem, gap, objective, and scope are clear in one page or less.

### PPT use
- Slides 2–3.

---

## Section 3 — Target-Site Profile

### Required parts
1. **Location and boundaries**
   - Santiago Bridge coordinates: approximately 15.3300° N, 120.6284° E.
   - Monitored endpoint: approximately 15.3334° N, 120.6367° E.
   - Full reach to Alfonso Bridge: 1.52 km.
   - Exact GPS must be field-confirmed.
2. **Physical setting**
   - West-to-east flow.
   - Wet and dry seasons.
   - Channel width estimate and measured cross-sections.
   - Flood/gauge evidence.
3. **Land use**
   - Built-up banks in Santiago and Alfonso.
   - Housing, shops, roads, farm lots, paddies, and vegetation.
4. **People and services**
   - Population and household counts with census years.
   - Waste collection, septic tanks, and sewer status.
   - Vendors, fisherfolk, and river users where verified.
5. **Existing infrastructure**
   - Bridges, roads, drains, dikes, sampling station, power, and access.
6. **Data availability**
   - EMB monitoring.
   - MENRO records.
   - Barangay and MDRRMO data.
   - Missing records.
7. **Rules and programs**
   - Existing permits, inspections, cleanups, monitoring, and ordinances.

### Required visual
- Annotated map with:
  - 1-km boundary,
  - Start/end coordinates,
  - North arrow and scale,
  - Barangay labels,
  - Land-use zones,
  - Known drains/outfalls,
  - Proposed sampling stations,
  - Proposed service site,
  - Access route.

### Current profile facts to preserve
- 15,220 residents in Santiago and Alfonso, using 2020 population data.
- 3,148 households, using 2015 household data.
- 3.7 m gauge reading at Santiago Bridge on July 22, 2025.
- Published photos show turbid gray-green water and bank litter.
- Width is estimated; depth and cross-sections are not yet measured.
- Individual outfalls and sheds cannot be plotted until MENRO records and field verification are available.

### Focus
- Conditions that affect diagnosis, sampling, design, access, and operation.

### Do not include
- Unverified outfalls.
- Unsupported claims that Bamban farms drain into this reach.
- Unverified irrigation infrastructure or quantified fisheries impacts.
- Mixed census years presented as one year.

### Done when
- Another team could locate the reach and understand its main physical and social conditions.

### PPT use
- Slide 4.

---

## Section 4 — Baseline and Evidence Base

### Required parts
1. **Published monitoring table**
   - Fecal coliform, BOD, DO, pH, and temperature.
   - Comparator stations to show different pollution signatures.
2. **Provenance note**
   - EMB Region III report and monitoring round.
   - Exact station, quarter, sample count, and classification still to confirm.
3. **Primary baseline plan**
   - Above/below piggery-cluster samples.
   - Drain and outfall samples.
   - Dry-season flow at the bridge.
   - Shed census.
   - Waste quadrats.
   - River-use and service interviews.
4. **Evidence register**
   - Claim, source, date, method, status, limitation.
5. **Baseline interpretation**
   - Fecal-loading signature.
   - Passing BOD/DO.
   - Uncertainty in source apportionment.

### Required evidence labels
- **Published:** held in an external document.
- **Team-measured:** collected by the team with a documented method.
- **Derived:** arithmetic from stated inputs.
- **Assumption:** chosen for planning and tested later.
- **Missing:** required but not available.

### Focus
- Evidence that changes the diagnosis, design, or target.

### Do not include
- One-day observations described as a complete baseline.
- National livestock statistics allocated to this reach.
- Published monitoring described as new team sampling.

### Done when
- Every baseline statement has a source, unit, date, location, and limitation.

### PPT use
- Slide 2.

---

## Section 5 — Root-Cause Diagnosis

### Purpose
- Show why fecal pollution persists and how the proposed service interrupts it.

### Required parts
- DPSIR diagnosis.
- Source-to-receptor causal chain.
- Source ranking.
- Live alternative explanation.
- Falsification test.
- Evidence-confidence statement.

### Required DPSIR table

| Element | Lucong working diagnosis | Evidence | Confidence/status |
|---|---|---|---|
| Driver | Unmonitored commercial piggery operations | EMB reports livestock discharge; permits/inspection inventory incomplete | Medium |
| Pressure | Manure and washwater | Sump/drain pathways to be mapped | Hypothesis pending field confirmation |
| State | Fecal coliform 16,000; BOD/DO within limits | Published EMB table | Published; row provenance incomplete |
| Impact | Contact, irrigation, amenity, ecosystem risk | Some use/condition evidence; health and fisheries effects unquantified | Mixed |
| Response | Monitoring, cleanups, permits, rules | Existing responses do not provide haulage | Published documents; local authority to confirm |

### Required causal chain
- **Source:** sheds draining to the reach.
- **Pathway:** direct discharge, drains, bank seepage, runoff, or washwater.
- **Transport:** river flow and die-off.
- **State:** station fecal-coliform concentration.
- **Intervention point:** sealed sump and collection before discharge.

### Falsification test
- Census sheds with MENRO.
- GPS-tag every shed and drain.
- Sample above and below each cluster.
- Measure dry-season discharge at the bridge.
- Compare fecal-coliform gradients.
- If concentrations do not rise below piggery clusters, shift weight toward household sewerage or other sources.

### Source ranking

| Source | Current assessment | Evidence needed to change the ranking |
|---|---|---|
| Commercial piggery manure | Leading controllable-source hypothesis | Census, drainage links, paired samples, source share |
| Household sewerage/septic systems | Major alternative contributor | Septic/desludging records, household survey, source markers |
| Uncollected solid waste | Secondary contributor | Waste mass/composition and pathway observations |
| Agricultural runoff | Possible contributor | Parcel/drain tracing and nutrient/source evidence |
| Bamban-origin runoff | Unresolved | Trace drains across the municipal boundary |

### Focus
- The dominant controllable source and the conditions that sustain it.

### Do not include
- “Piggeries are proven to cause all pollution.”
- “No sewer exists” without written confirmation.
- Bamban farms named as polluters without a traced pathway.
- Visible trash treated as the main cause of fecal coliform.

### Done when
- The diagnosis states a leading hypothesis, a live alternative, and the test that distinguishes them.

### PPT use
- Slides 5–6.

---

## Section 6 — Stakeholder, Legal, and Institutional Analysis

### Required parts
1. **Stakeholder roles**
   - Shed owners.
   - Barangay officials and monitors.
   - MENRO.
   - Municipal Agriculture Office.
   - Mayor/permit office.
   - Health office.
   - Operators/cooperative.
   - Farmers receiving compost.
   - Downstream users.
2. **Role matrix**
   - Who decides?
   - Who permits?
   - Who pays capital?
   - Who pays collection?
   - Who operates?
   - Who maintains?
   - Who monitors?
   - Who enforces?
3. **Legal review**
   - Existing permit requirements.
   - Authority to condition permits on waste handling.
   - Barangay resolution and health-certificate linkage.
   - Environmental, siting, transport, labor, and safety requirements.
4. **Precedent comparison**
   - Naga City’s farm-level regulation.
   - Other reviewed ordinances.
   - The documented gap: regulation without haulage.

### Current legal caution
- The current paper proposes attaching a waste-service condition to the Mayor’s permit.
- This authority is **not yet confirmed**.
- Do not state that Concepcion has no siting rules; its zoning ordinance has not been obtained.
- Bamban’s numeric siting schedule is a comparator, not automatically Concepcion law.

### Focus
- Roles and approvals needed to make the service operational.

### Do not include
- Generic “community participation.”
- Unverified enforcement powers.
- Accusations against named farms without evidence.

### Done when
- Every major activity has a proposed owner and a documented or explicitly unresolved authority.

### PPT use
- Slides 8 and 13.

---

## Section 7 — Options Appraisal

### Required parts
- Options and do-minimum comparator.
- Common decision criteria.
- Hard constraints.
- Comparative justification.
- Sensitivity or robustness note.

### Required comparison

| Option | What it addresses | Main constraint | Current assessment |
|---|---|---|---|
| Do-minimum/current practice | No new service | Load continues | Baseline comparator |
| Enforcement alone | Noncompliance | Prior closure order was voided; inspection capacity unresolved | Insufficient alone |
| On-farm digestion only | Treatment at source | Manure still accumulates; no haulage | Partial response |
| Piped plant | Centralized conveyance | No sewer network; capital likely exceeds cap | Not feasible within current scope |
| In-stream interception | Captures material in channel | Blockage/flood liability; does not treat at source | High risk |
| Shed-level collection + central digestion | Contains and moves manure before discharge | Requires census, tanker, site, operators, permits, and manifests | Leading feasible option |
| Combined source control + service | Adds low-volume washing and farm practices | More coordination | Evaluate after census |

### Required decision criteria
- Station-level fecal-load reduction.
- Capture reliability.
- Capital and lifecycle cost.
- Operational complexity.
- Land and nutrient requirements.
- Legal/institutional fit.
- Safety and environmental side effects.
- Scalability.

### Rules
- Compare options using the same functional unit.
- Apply hard constraints before ranking.
- Use weighted scoring only if weights are justified and sensitivity-tested.
- The current paper’s claim is **least-cost among feasible designs**, not universal superiority.

### PPT use
- Slide 8.

---

## Section 8 — Proposed 12-Month Pilot Plan

### Required parts
- Pilot objective and intervention logic.
- Service chain and components.
- Twelve-month schedule.
- Itemized budget and 70/30 check.
- Roles and O&M.
- Risks and scale-up logic.

### Pilot objective
- Prevent the verified share of piggery manure from reaching the 1-km reach and conditionally reduce station fecal coliform to 8,000 MPN/100 mL.

### Service chain
1. **Sealed sump and drum at each participating shed.**
2. **Weekly collection by vacuum tanker/cart.**
3. **Weighing and manifest for every load.**
4. **Central covered anaerobic digestion.**
5. **Biogas use or safe flaring.**
6. **Digestate dewatering and composting with rice husk.**
7. **Compost return under a nutrient/land plan.**
8. **Quarterly water-quality and service audit.**

### Current planning design
- 15 sheds.
- 3 × 25 m³ covered digesters.
- One 2,000-L vacuum tanker.
- Two motorized carts.
- Roofed composting pad.
- Biogas-use kit.
- Paved yard, fencing, access, and signage.
- Three operating posts.

> This is a planning case, not a verified final design. Census, washwater use, source share, site consent, and quotations may change it.

### Twelve-month schedule

| Phase | Months | Required work | Decision gate |
|---|---|---|---|
| 0. Preparation | 1 | Confirm reach, roles, permissions, evidence register | Governance and access confirmed |
| 1. Verification | 1–2 | Shed census, drain GPS, paired samples, flow, land consent, tanker quote | Diagnosis and source share support the service |
| 2. Design/procurement | 3–5 | Finalize capacity, permits, procure equipment, prepare site, train operators | Budget, safety, and legal checks pass |
| 3. Operation | 6–11 | Weekly route, manifests, maintenance, quarterly sampling | Capture and cost tracked |
| 4. Evaluation/handover | 12 | Baseline comparison, cost curve, audit, O&M handover | Continue, modify, or stop |

### Current draft budget

| Item | 12-month amount |
|---|---:|
| Capital: digesters, tanker, carts, pad, gas, site | Php 4,485,000 |
| Sampling | Php 240,000 |
| Staff | Php 1,140,000 |
| Maintenance, fuel, consumables | Php 912,000 |
| Administration | Php 60,000 |
| **Total** | **Php 6,837,000** |

### Budget checks
- [ ] Total remains ≤Php 10,000,000.
- [ ] Stream 2 spending remains ≥70%; current design is 100%.
- [ ] Every line has quantity, unit cost, source/date, and status.
- [ ] Tanker quotation is obtained or the estimate is explicitly labeled.
- [ ] O&M, sampling, waste handling, and safety are included.
- [ ] No compost revenue is counted unless supported.
- [ ] Capital payer and collection-fee mechanism are confirmed.

### Operations and maintenance
- Route schedule and backup vehicle plan.
- Weighing/logging and manifest storage.
- Digester inspection and pressure testing.
- Gas safety and flaring.
- Compost turning and nutrient application.
- Tanker spill response and washdown.
- Spare parts and consumables.
- Operator training and protective equipment.

### Focus
- A limited, costed service with named owners and measurable operation.

### Do not include
- A shopping list of unrelated technologies.
- Unitemized lump sums.
- A “sustainable” claim without an O&M owner.
- Full-river benefits attributed to a 1-km service.

### Done when
- The pilot can be costed, permitted, operated, monitored, and handed over.

### PPT use
- Slides 7, 11, and 12.

---

## Section 9 — Methodology

### Required parts
- Study design and boundaries.
- Source-attribution protocol.
- Load and process balances.
- Economic and alternatives analysis.
- Uncertainty and sensitivity.
- Monitoring, ethics, and safety.

### Study design
- Mixed-methods case study.
- Documentary evidence review.
- Reach mapping and census.
- Repeated paired water sampling.
- Process and capacity modeling.
- Lifecycle costing.
- Alternative appraisal.
- Uncertainty and sensitivity analysis.

### A. Source-attribution method

| Question | Data | Method | Output |
|---|---|---|---|
| How many sheds drain to the reach? | MENRO/barangay records + field census | One row per shed; drainage status confirmed/unknown | Verified census |
| Where are the pathways? | Drains, outfalls, bank seepage | GPS walk and annotated map | Source-pathway map |
| Do clusters raise fecal coliform? | Above/below samples | Paired repeated sampling | Source-gradient evidence |
| What is the station flow? | Dry-season discharge | Field measurement/gauging with uncertainty | Q estimate |
| What is sewerage’s role? | Septic/desludging records and household evidence | Records + interviews + sampling | Alternative-source assessment |

### B. River load model

Define:

- \(C_0\): baseline station fecal-coliform concentration.
- \(Q\): dry-season discharge at a stated location and condition.
- \(h\): verified animal heads draining to the reach.
- \(e\): fecal-coliform generation per head-day.
- \(L\): shed load.
- \(L_0\): station load.
- \(s = L/L_0\): shed share of station load.
- \(c\): fraction of shed load captured and prevented from discharge.

Core relationship:

\[
C = C_0(1-s c)
\]

### Interpretation
- High source share + high capture → large predicted reduction.
- Low source share → little station-level change even with excellent capture.
- The current conditional target is **8,000 MPN/100 mL**, not compliance at 200.
- The current paper associates the target with \(s \ge 0.6\), which implies \(Q \le 0.03\ \text{m}^3/\text{s}\) under its current census assumptions.
- Month 1 must test both source share and flow.

### Modeling rules
- Use consistent units and show the concentration-to-load conversion.
- Every parameter must be measured, sourced, derived, assumed, or missing.
- Do not silently replace missing values.
- Report transport/die-off and background load if used.
- Do not call the model calibrated before field validation.

### C. Process and capacity balances

Calculate:

- Manure and washwater volumes.
- Slurry volume entering digesters.
- Hydraulic retention time.
- Tanker trips and weekly throughput.
- Volatile solids and biogas.
- Methane energy and LPG equivalent.
- Digestate and compost quantities.
- Nutrient output and required land.
- Staff and maintenance workload.

### Current arithmetic to reconcile
- The current paper uses **15 sheds × 15 heads = 225 heads**.
- The older data brief uses **15 sheds × 12 heads = 180 heads**.
- Do not mix these cases.
- Use the corrected gas arithmetic from the current paper/model work, not the older 30 m³ biogas / 18 kg LPG figures.

### D. Economic method

- Twelve-month cash budget.
- Lifecycle net present cost.
- Annualized cost.
- Levelized cost per shed-month.
- Cost per head-month.
- Fee affordability scenarios.
- Replacement/residual assumptions.
- Sensitivity to census, washwater, tanker price, and capture.

### E. Alternatives and feasibility
- Enumerate feasible configurations.
- Apply hard constraints first:
  - ≤12 months.
  - ≤Php 10M.
  - ≥70% one focus stream.
  - Process/capacity requirements.
  - Land, safety, and legal constraints.
- Rank feasible designs by lifecycle cost and performance.
- Report infeasible designs and why they fail.

### F. Uncertainty and synthetic scenarios
- If no observed census exists, any synthetic census must be labeled **“SYNTHETIC — NOT FIELD-VERIFIED.”**
- Report the prior, seed, scenario count, and assumptions.
- Do not use provincial or Bamban statistics as if they were Concepcion reach counts.
- Report the probability of meeting the conditional target only as prior-predictive until field data exist.

### G. Monitoring and evaluation

| Indicator | Baseline | Target/criterion | Frequency |
|---|---|---|---|
| Station fecal coliform | Published 16,000; new baseline to collect | Conditional 8,000 if source share/capture support it | Quarterly |
| Shed census and drainage links | Missing | Verified census and map | Month 1 |
| Manifest coverage | 0% in proposed service | Defined coverage target, e.g., 95% of shed-weeks | Monthly/quarterly |
| Manure diverted | 0 in service | Derived from verified census and measured loads | Monthly |
| Capture reliability | Unknown | Measured collection/treatment fraction | Monthly |
| Cost per shed-month | Model estimate | Published actual cost curve | Quarterly |
| Safety/environmental incidents | Baseline to define | Recorded and reviewed | Continuous |

### H. Ethics and safety
- Permission for site access, sampling, interviews, and land use.
- Consent and confidentiality for participants.
- No unsafe water entry.
- Confined-space protocol for digesters.
- Hydrogen sulfide monitoring, harness, and second-person watch.
- Tetanus/leptospirosis protection and PPE.
- Methane pressure testing and flaring.
- Spill prevention and washdown containment.
- Nutrient budget for compost application.

### Focus
- Repeatable methods tied to a decision.

### Do not include
- Complex models without data.
- Survey beliefs presented as measured pollution.
- Synthetic results presented as observed.
- Calibration or field-proof claims before validation.

### Done when
- Another reader could reproduce the workflow and understand its limits.

### PPT use
- Slides 6, 9, 10, and 12.

---

## Section 10 — Expected Outputs and Evaluation

### Required parts
- Physical and documentary outputs.
- Baseline and source-attribution outputs.
- Design, budget, and cost curve.
- Conditional performance target.
- Monitoring and evaluation rules.

### Required outputs
- Verified or explicitly synthetic shed census.
- Source-pathway map.
- Baseline monitoring table.
- Source-attribution conclusion with confidence.
- Recommended service design.
- Itemized 12-month budget.
- Lifecycle cost curve.
- Conditional station-level target.
- Manifest and monitoring system.
- O&M and safety plan.
- Scale-up blueprint.

### Results rules
- If pilot data do not exist, title this section **“Expected Outputs and Evaluation Plan.”**
- Do not present projected reductions as measured.
- Report negative findings and missed targets.
- Separate model results from field observations.
- State whether the conditional target was met, missed, or not testable.

### PPT use
- Slides 10–12.

---

## Section 11 — Implications, Limitations, and Scaling

### Required parts
- Interpretation of diagnosis and performance.
- Economic and governance implications.
- Side effects and risks.
- Limitations and alternative interpretations.
- Conditional scaling requirements.

### Required discussion points
1. **Diagnosis**
   - Does field evidence support piggery dominance?
   - How much remains attributable to sewerage or other sources?
2. **Performance**
   - Is the service capturing the intended share?
   - Does station concentration respond as predicted?
3. **Economics**
   - Are costs within the cap?
   - Are fees affordable?
   - Which assumption drives cost most?
4. **Governance**
   - Can permits, manifests, and enforcement be integrated?
   - Who owns O&M after the pilot?
5. **Side effects**
   - Methane, hydrogen sulfide, spills, worker safety, land/nutrient limits.
   - Potential shifts of pollution to another life-cycle stage.
6. **Limitations**
   - Incomplete EMB provenance.
   - Unverified census and drainage.
   - Flow uncertainty.
   - No paired field calibration yet.
   - No control/reach comparison unless designed.
   - Unconfirmed legal authority and quotations.
7. **Scaling**
   - Repeat only after verifying source share and capture in the new reach.
   - Recompute flow, census, land, nutrient, and cost parameters.
   - Do not transfer the Lucong target automatically.

### Focus
- Uncertainty, decision relevance, and replication conditions.

### Do not include
- Demonstrated health, fisheries, irrigation, or downstream benefits.
- River-system improvement claims.
- A generic “more studies are needed” ending without specific next measurements.

### PPT use
- Slide 13.

---

## Section 12 — Conclusion and Recommendation

### Required parts
- Direct answer to the research question.
- Leading source hypothesis and remaining uncertainty.
- Recommended service and why it is feasible.
- Conditional target and condition.
- Most important unresolved evidence.
- Specific next decision:
  - Approve Month 1 verification,
  - Secure land and legal authority,
  - Obtain the tanker quotation,
  - Confirm operators and payer, or
  - Proceed to a conditional pilot.

### Done when
- The conclusion follows from the evidence and introduces no new claims.

### PPT use
- Slide 14.

---

## Section 13 — References, Appendices, and Declaration

### Required parts
- Verified references in the required style.
- Official laws and agency documents.
- Appendices if permitted:
  - Census template.
  - Drain/outfall map.
  - Sampling protocol.
  - Parameter register.
  - Model equations and assumptions.
  - Budget and quotations.
  - Manifest template.
  - Risk and O&M plan.
  - Monitoring forms.
- AI declaration according to the organizer’s ruling.

### Rules
- Verify every citation.
- Do not guess identifiers, page numbers, or publication details.
- Disclose AI assistance plainly if required.
- Keep appendices within official limits.

---

# Part 5 — Focus / Non-Focus Control Sheet

| Topic | Focus on | Exclude or minimize |
|---|---|---|
| Geography | 1 km downstream of Santiago Bridge | Whole Lucong/Chico/Pampanga cleanup |
| Pollution stream | Commercial piggery manure | Paco household-waste or Stream 3 cleaning material |
| Diagnosis | Fecal-loading signature and source attribution | Treating trash/odor as the main fecal source |
| Evidence | Published, measured, derived, assumed, missing | Provincial statistics assigned to the reach |
| Baseline | Published row plus new paired field baseline | Calling the published row a new team measurement |
| Target | Conditional 8,000 MPN/100 mL | Promising 200 compliance |
| Design | 15-shed planning service, subject to verification | Digester novelty claims |
| Contribution | Permit–manifest–haulage coupling | “We invented the digester” |
| Budget | 12-month, itemized, ≤Php 10M | Older 24-month Php 10M budget |
| People | Named permit, payer, operator, maintainer, monitor | “The community/LGU will handle it” |
| Model | Load/process/cost decision support | Hydrodynamic or disease models without data |
| Results | Conditional predictions and planned evaluation | Fabricated field results |
| Impacts | Documented risks and unquantified benefits | Claimed health/fisheries improvements |
| Writing | Analysis, evidence, numbers | Long background history |
| Presentation | One message and one visual per slide | Dense paper paragraphs on slides |

---

# Part 6 — Required Evidence and Open-Issue Register

| Priority | Open item | Why it matters | Required action | Status |
|---|---|---|---|---|
| Critical | EMB Lucong row provenance | Supports the headline 16,000 value | Confirm station, quarter, sample count, classification | Open |
| Critical | Shed census and head count | Sets design, cost, source share, and target | MENRO/barangay registry + field verification | Open |
| Critical | Drainage links | Determines which sheds affect the reach | GPS walk and map | Open |
| Critical | Dry-season flow Q | Determines source share and target feasibility | Field gauging/record request | Open |
| Critical | Legal authority for permit condition | Makes the service enforceable | Written legal/MENRO confirmation | Open |
| High | Exact reach GPS | Defines the 1-km boundary | Handheld GPS, averaged fixes | Open |
| High | No-sewer confirmation | Supports the conveyance argument | Written LGU/MENRO record | Open |
| High | Tanker quotation | Largest unsupported cost line | Obtain dated supplier quote | Open |
| High | 15 vs 12 heads/shed conflict | Changes all process/cost calculations | Reconcile current paper and older brief | Open |
| High | Site consent and land availability | Required for digesters/compost | Written consent and site plan | Open |
| High | Payer/operator/maintainer | Required for feasibility | Confirm LGU/cooperative/shed fee arrangement | Open |
| High | AI-use ruling | Required declaration | Obtain organizer response | Open |
| Medium | Vendors/fisherfolk/river use | Supports impact section | Registry/interviews | Open |
| Medium | Waste quadrats | Tests secondary solid-waste contribution | Three 100-m² quadrats | Open |
| Medium | Concepcion zoning ordinance | Prevents false claim of no siting rules | Obtain official copy | Open |
| Medium | Bamban drain pathway | Resolves upstream-source uncertainty | MPDO/MENRO map review | Open |

---

# Part 7 — Step-by-Step Writing and Production Plan

## Step 1 — Freeze the research identity
**Deliverable:** One-page scope statement.
- Confirm title, reach, stream, question, target, budget cap, and exclusions.
- Use the current paper’s 12-month direction.
**Done when:** All sections use the same scope language.

## Step 2 — Reconcile the number set
**Deliverable:** Master number table.
- Resolve 225 vs 180 heads.
- Use the current 12-month budget.
- Use the current gas calculations.
- Use the conditional 8,000 target.
- Mark every value by evidence status.
**Done when:** No conflicting values remain across paper, poster, and slides.

## Step 3 — Close critical provenance
**Deliverable:** Evidence notes for EMB and legal claims.
- Confirm the 16,000 row.
- Confirm applicable classification.
- Confirm no-sewer statement.
- Confirm permit-condition authority.
**Done when:** Load-bearing claims have documents or explicit caveats.

## Step 4 — Complete the site profile
**Deliverable:** Profile table and annotated map.
- Verify endpoints, GPS, land use, services, and access.
- Separate measured, estimated, and missing fields.
**Done when:** Slide 4 can be built without invention.

## Step 5 — Write the diagnosis with a falsification test
**Deliverable:** DPSIR table and causal chain.
- State piggery hypothesis, sewerage alternative, and Month 1 test.
- Rank sources by evidence confidence.
**Done when:** The diagnosis is specific and challengeable.

## Step 6 — Write the service mechanism
**Deliverable:** Process-flow diagram and component list.
- Explain each step from sump to field.
- Link each component to a diagnosed pathway.
**Done when:** A nontechnical reader can follow the waste.

## Step 7 — Complete the options appraisal
**Deliverable:** Comparison table.
- Include do-minimum and realistic alternatives.
- Explain why each alternative fails or remains partial.
**Done when:** The recommendation is comparative, not assertive.

## Step 8 — Finalize methodology and model
**Deliverable:** Question-to-method matrix and model note.
- Load balance.
- Process/capacity balances.
- Lifecycle costing.
- Uncertainty.
- Synthetic-data labels.
**Done when:** Every model output is traceable to an input and assumption.

## Step 9 — Finalize budget, timeline, and roles
**Deliverable:** Itemized budget, Gantt chart, and role matrix.
- Dated quotations or explicit estimates.
- 70/30 check.
- Payer, operator, maintainer, monitor, and regulator.
**Done when:** The pilot is implementable on paper.

## Step 10 — Draft in evidence order
**Deliverable:** Complete first draft.
Recommended order:
1. Site profile.
2. Baseline.
3. Diagnosis.
4. Proposed service.
5. Methodology/model.
6. Budget/feasibility.
7. Implications/limitations.
8. Introduction.
9. Conclusion.
10. Abstract.
**Done when:** The introduction and abstract reflect the actual evidence.

## Step 11 — Build visuals before cutting words
**Deliverable:** Final figure/table set.
- Map.
- Water-quality chart.
- DPSIR/causal chain.
- Service flow.
- Model schematic.
- Target/sensitivity chart.
- Budget.
- Gantt.
- Risk/role matrix.
**Done when:** Each major claim has a visual home.

## Step 12 — Map into the official template
**Deliverable:** Template-compliant manuscript.
- If using the current v1.1 structure:
  - Introduction = problem, site profile, diagnosis, Month 1 test.
  - Suggested Process/Product = service, schedule, inputs, steps.
  - Expected End Output = manifests, monitoring, cost curve, local value.
  - Feasibility/Economic Analysis = model, alternatives, budget, roles.
  - Implications = environment, health, community, risks, scaling.
  - References/AI Declaration = verified sources and ruling.
**Done when:** No required official section is missing.

## Step 13 — Cut to the word limit
**Deliverable:** Submission-length paper.
- Cut background first.
- Preserve evidence, methods, numbers, and limitations.
- Remove repeated scope statements.
**Done when:** The official word count passes.

## Step 14 — Cross-check paper, poster, and PPT
**Deliverable:** Consistent package.
- Same baseline, target, budget, design, and dates.
- Same rounding and units.
- Same observed/projected labels.
**Done when:** No number or claim conflicts.

## Step 15 — Render and inspect
**Deliverable:** Final PDF and poster image.
- Open the actual PDF and PNG on two devices.
- Check fonts, tables, figures, captions, and readability.
- Freeze content before submission.
**Done when:** The exported files are readable, not only the source documents.

## Step 16 — Submit and retain evidence
**Deliverable:** Submission record.
- Verify deadline and email.
- Send required files.
- Confirm receipt.
- Keep sent files and confirmation.
**Done when:** Receipt is documented.

---

# Part 8 — Claim-Control Rules

| Label | Meaning | Safe wording |
|---|---|---|
| Published | Stated in an external document | “EMB Region III reports…” |
| Team-measured | Collected with a documented method | “Samples collected on… showed…” |
| Derived | Arithmetic from stated inputs | “Using…, the calculated value is…” |
| Assumption | Planning input awaiting verification | “The design assumes…” |
| Synthetic | Generated scenario, not observed | “Under the declared synthetic prior…” |
| Projected | Model result under assumptions | “The model predicts…” |
| Proposed | Planned activity | “The pilot proposes…” |
| Missing | Required evidence unavailable | “This remains to be verified…” |

## Phrases to avoid
- “Piggeries cause all Lucong pollution.”
- “The 16,000 value is our field baseline.”
- “The pilot will make the river compliant.”
- “The 15 sheds are verified.”
- “The LGU will pay and maintain it.”
- “The permit condition is legally authorized.”
- “The model proves the service works.”
- “The project improves health/fisheries/irrigation.”
- “The digester is the innovation.”

---

# Part 9 — Final Completion Checklist

## Scope and profile
- [ ] One 1-km reach is defined and mapped.
- [ ] Santiago/Alfonso profile is accurate and census years are labeled.
- [ ] Current Stream 2 piggery focus is consistent everywhere.
- [ ] Paco/Stream 3 and river-wide cleanup material are excluded.

## Evidence and baseline
- [ ] 16,000 is labeled as published, with provenance caveat until confirmed.
- [ ] BOD/DO/pH/temperature values are correct.
- [ ] Every number has a source, date, unit, and status.
- [ ] No provincial or Bamban counts are assigned to the reach.
- [ ] Team baseline and published baseline are distinguished.

## Diagnosis
- [ ] Piggery hypothesis and sewerage alternative are both stated.
- [ ] Source → pathway → state → impact → response is shown.
- [ ] Month 1 falsification test is explicit.
- [ ] No unverified Bamban pathway or named polluter is asserted.

## Proposed plan
- [ ] Sump → collection → manifest → digestion → compost chain is clear.
- [ ] Current 15-shed planning design is labeled as provisional.
- [ ] Twelve-month schedule is complete.
- [ ] Budget is itemized and ≤Php 10M.
- [ ] Stream 2 share is ≥70%.
- [ ] Payer, operator, maintainer, monitor, and regulator are named or marked unresolved.
- [ ] O&M, safety, and nutrient/land requirements are included.

## Methodology
- [ ] Load balance and process/capacity balances are explained.
- [ ] Source share, capture, flow, and uncertainty are explicit.
- [ ] Alternatives are compared on the same basis.
- [ ] Synthetic scenarios are prominently labeled.
- [ ] No calibration or empirical-proof claim is made prematurely.

## Results and claims
- [ ] 8,000 is conditional.
- [ ] 200 compliance is not promised.
- [ ] Projected and measured results are separated.
- [ ] Health, fisheries, irrigation, and downstream benefits are not claimed without evidence.
- [ ] Permit–manifest–haulage is the contribution, not the digester.

## Submission
- [ ] Current paper and approved model design override older drafts.
- [ ] 225 vs 180 heads is reconciled.
- [ ] Old 24-month budget and gas figures are absent.
- [ ] References are verified.
- [ ] AI declaration follows the organizer’s ruling.
- [ ] Paper, PDF, poster, and PPT are numerically identical.
- [ ] Exported files are inspected on two devices.
- [ ] Deadline, email, formats, and receipt are confirmed.

---

# Part 10 — Meeting Image Traceability

| Image prefix | Lesson used |
|---|---|
| d674a1c8 / ad9bc8f5 | Environment first, then law, then cost |
| 9d1dc2d4 | Six flaws: scope, budget, measurement, symptoms, people, comparison |
| 60917084 | Deadline, required files, People’s Choice weighting |
| 46cf491b | Life-cycle thinking and functional unit |
| d87483a4 | Industrial ecology, LCA, input-output toolkit |
| 79be4ed6 | Match method to question; beliefs versus actual effects |
| 1f2cc710 | Site selection and profile requirements |
| d768fa10 | System boundaries and how effects spread |
| 385d06cc | Primary, published, official evidence and source checks |
| c1e43a1c | Whole-system stakeholders |
| da54dc8d | 1 km, 12 months, Php 10M, 70/30, scaling |
| 12a6709b / cf5c899f | Research can lead to practical and publishable contributions |
| ad502414 | National causes are context, not local proof |
| 3d430f23 | Clear gap, sound method, real contribution, honest limits |
| 528896c1 | Common pitfalls, including the 2,200-word warning |
| 10d193a8 | Map system, write math, set goal, test answer |

---

## Immediate Next Actions

1. **Confirm the EMB row behind 16,000 MPN/100 mL.**
2. **Reconcile 225 versus 180 animal heads in the current design.**
3. **Request the MENRO shed, permit, drain, and inspection records.**
4. **Verify the 1-km endpoints with GPS.**
5. **Obtain a written tanker quotation.**
6. **Confirm no-sewer status and permit-condition authority.**
7. **Complete the source-attribution and flow plan for Month 1.**
8. **Freeze the 12-month budget and conditional 8,000 target.**
9. **Draft the evidence-heavy sections before the abstract.**
10. **Build the 14-slide sequence only after the paper’s number set is locked.**
