# Research Draft v0.1 — Angle Decision + Paper

> **⚠ SUPERSEDED by [v0.2](2026-11-13-paper-draft-v0.2.md).** Verification found nine errors in this draft, including a wrong regulatory value (Class C fecal coliform is 200, not 400) and a thesis that the evidence does not support. Retained as the audit trail. **Do not use any figure from this file without checking the [source verification annex](../verification/2026-11-13-source-verification-annex.md).**

> **Provenance warning, read first.** This draft was produced with substantial AI assistance: evidence retrieval, source synthesis, option scoring and prose. The Research Fair 2027 kit's declaration excludes AI-generated content, ideas and theories. This file is **research scaffolding for human authorship**, not a submittable entry. It may not be submitted, paraphrased into a submission, or declared as language-only assistance. Gate G0 in the plan still applies. Every factual claim below is tagged in the evidence ledger (§C) so a human author can verify each one independently.

> **Status:** 13 November 2026. Deadline 5 December 2026, 11:59 PM PHT.

---

# A. Why the angle changed

The first angle — verification-first household solid-waste collection — does not survive the evidence. Four findings killed it:

| Finding | Source | Consequence |
|---|---|---|
| "40% of Metro Manila waste is uncollected" is a **misreading**. The World Bank's own page says the 40% includes recovered recyclables and processed biodegradables, and that "there is no data on the quantity of uncollected waste." | WB 2022, p.51 | The headline statistic in the kit's own problem statement is not citable as written |
| Verification-first waste accounting **already ships** in Legazpi (2023), Iloilo AGUBAY (2025), Plaridel RecyclX, TrashTrack, SWEEP, Oro Kalimpyo | ADB 2024; IMT News 2025 | Ingenuity claim collapses |
| RA 11898 §44-G already **mandates** third-party verification of plastic diversion **in kilograms** | RA 11898; DAO 2023-02 | "Cost per verified kilogram" is statutory, not novel |
| Cost: ₱10M ÷ 400 households = **₱76,000 per tonne diverted** at a generous 40% diversion, against verified plastic credits trading at ₱6–13/kg | PCX Markets 2025 | Fatal on Economics (5%) and Practicality (10%) |

The decisive one is not novelty. It is that **solid waste is not the pollutant that matters here.** Plastics exert essentially zero biochemical oxygen demand. The Pasig's failure is a sewage failure.

## Three angles, scored against the actual rubric

| | **A1. Solid waste service** (previous) | **A2. Sensor-instrumented septage** | **A3. Access-constrained septage** (recommended) |
|---|---|---|---|
| Background (10) | 7 | 8 | **9** |
| Rationale (10) | 6 | 7 | **9** |
| Methodology (15) | 8 | 7 | **10** |
| Ingenuity (10) | 3 | 6 | **8** |
| Practicality (10) | 7 | 4 | **9** |
| Economics (5) | 2 | 3 | **5** |
| Environment (10) | 5 | 8 | **9** |
| Health (5) | 4 | 5 | **5** |
| Community (5) | 4 | 4 | **5** |
| Writing (10) | 8 | 8 | **8** |
| References (5) | 5 | 5 | **5** |
| **Total /95** | **59** | **65** | **82** |

**A2 was rejected on engineering, not strategy.** A septic tank's liquid level is fixed by its outlet invert and stays constant while sludge accumulates. Ultrasonic and pressure sensors measure the wrong variable. The Sanergy/SweetSense pilot in Nairobi abandoned pressure transducers for exactly this reason. And at 400 units the sensor is ~80% of year-one cost, not 30%.

**A3 keeps the sensor, but gives it the only role it is physically correct for: overflow and bypass alarm.** Not a desludging trigger.

---

# B. Paper draft

**Word count, non-reference text: 2,061** (limit 2,200)

---

## The Last Meter
### Access-constrained septage collection in a one-kilometre estero reach
**Estero de Paco, Manila — Stream 1: Household Trash Control & Local Waste**

### 1. Background

Estero de Paco is a 2.7–3.0 km tidal tributary of the Pasig River. It drains Paco and Pandacan through Barangays 671–687 and enters the Pasig beside Paco Market. The Pasig is classified Class C under DENR Administrative Order 2016-08: biochemical oxygen demand of 7 mg/L or less, dissolved oxygen of 5 mg/L or more, total suspended solids of 80 mg/L or less, and fecal coliform of 400 MPN/100 mL or less.

Measured performance sits far outside those limits. Six main-stem monitoring stations averaged BOD of 27.8 mg/L in 2018 and 24.2 mg/L in 2019 — roughly four times the standard. Across 2020–2021 sampling, seven of eight stations met the oxygen floor on neap tides but only one of eight did on spring tides. Manila City sites sampled in January 2025 returned fecal coliform between 2.4×10⁵ and 1.1×10⁶ MPN/100 mL, or 600 to 2,750 times the Class C limit. A CCME water quality index computed over 2010–2024 scored every station in every year as "Poor," and forecasts to 2030 show only decimal-level change.

The reach has not lacked attention. It was dredged and cleared in 2009, reopened in 2012 with a linear park and three aerators at roughly ₱20 million, and hosted a US$438,000 Asian Development Bank pilot from 2012 to 2015 that installed a condominial sewer, solar sump pumps, an anaerobic baffled reactor and a constructed wetland for 58 households in Barangay 672. That system reached 87% BOD removal across three months of monitoring, after which monitoring stopped. In March 2025 the DENR cleared structures to reclaim the three-metre easement over 1.7 km of bank in five barangays. In the first half of 2025 alone, 872,625 sacks were removed from Metro Manila waterways by 1,467 estero rangers.

The water did not improve. That is where this proposal begins.

### 2. Root-cause diagnosis

**The load is sewage, not litter.** The most recent apportionment of the Pasig basin (PEMSEA, 2013, 2008 baseline) attributes 83.4% of biochemical oxygen demand to domestic sources, 11.2% to industry and 5.1% to agriculture; it is a unit-load model, not a measurement. Measured microbial source tracking across 55 sink samples from December 2021 to May 2023 found sewage accounted for 93% of all *attributable* fecal contamination — but 57% of the community on average remained unassigned, rising to 62% at downstream Pasig stations.

**Solid waste is not the oxygen problem.** Polyethylene exerts essentially no biochemical oxygen demand. The defensible division is narrower and more useful: septage dominates oxygen demand and fecal loading; solid waste dominates hydraulic and plastic impacts. Metro Manila's drainage system is documented to flood from garbage blockages on 49 streets.

One widely repeated figure should be retired rather than cited. The "60% domestic, 33% industrial, 7% solid waste" split appears in Gorme et al. (2010) without a citation, contradicts that paper's own tables, and traces to a 1990s planning assumption. Repeating it would fail the References criterion.

### 3. The actual constraint

Eighty-four percent of Filipinos depend on septic tanks. In Metro Manila, desludging is already free at the point of use, funded by a roughly 20% environmental charge on the water bill, with both concessionaires publishing barangay-level schedules. Sixty to 71% of customers avail of it at least once.

Yet only 13% of septic tanks in an 800-household survey of low-income Metro Manila had *ever* been emptied, against a mean system age of nine years (World Bank/IFC, 2018).

The barrier is physical. In that same survey, 70% of tanks sat beneath the house, requiring the floor to be broken; 71% of access paths were only person- or motorbike-width; and 18% of toilets stood more than 20 metres from where a truck could park. Twenty-two percent of tanks had no cemented bottom. A standard ten-cubic-metre vacuum tanker cannot reach most of these households, and the lawful corridor is three metres either side of the bank under Article 51 of the Water Code.

Policy has assumed the problem was price and awareness. Manila's ordinance mandates desludging every three to five years; DOH Administrative Order 2019-0047 states both "three to five years" and, elsewhere, "every four years." Neither is enforced at household level. The national subsidy vehicle, the DPWH sewerage and septage programme, was designed for LGUs outside Metro Manila, and by 2025 only two LGUs nationwide had secured subsidy approval. The City of Manila has no septage treatment plant of its own; its septage travels to Caloocan, Quezon City or Las Piñas.

### 4. Proposed intervention

A twelve-month protocol pilot testing whether **access-tiered collection** — not subsidy, not awareness, not instrumentation — closes the desludging gap across one contiguous kilometre.

**(a) A catchment register.** Every tank in the footprint is recorded once: location, access tier, tank condition, last desludging, household size. No comparable barangay-level register exists anywhere in the Philippines. Access tier becomes the routing variable — A for truck-reachable, B for hose-reachable within 30 metres, C for portable-unit only.

**(b) Access-matched equipment.** One 1 m³ portable desludging unit with a 10 m³ mother tanker, the configuration Manila Water deployed in 2025 for narrow streets, plus standard hose runs for tier B.

**(c) Risk-based scheduling.** Desludging is triggered by a published rule combining years since last emptying, household size, tank volume and condition — not by complaint, and not by a sensor.

**(d) A verification layer.** Overflow and bypass alarms at tank outlets, a manifest chain to the receiving treatment plant, and bank observation of the reach.

### 5. Why an alarm and not a sludge sensor

A septic tank's liquid level is fixed by its outlet invert. It remains constant while sludge accumulates at 25 to 77 litres per person per year. Ultrasonic and pressure devices therefore measure the wrong variable, and the only instruments that genuinely resolve a sludge blanket are lowered probes costing USD 1,000 to 15,000. No city-scale instrumented tank programme exists in any country.

An overflow alarm is a different instrument. Float switches cost USD 50 to 250, detect the event that actually discharges raw sewage, and fail safe. It is the only sensor role this pilot claims.

### 6. Twelve-month plan

Months 1–2 establish permissions, the register, the access survey and eight weeks of bank observation. Month 3 delivers equipment, trains the crew, and tests the manifest chain end to end. Months 4–12 run nine collection months with monthly manifest reconciliation and quarterly financial review. Month 12 evaluates and decides handover.

The pilot enrolls 400 households, roughly 30% of the 1,360 estimated to sit within 150 metres of both banks. Equipment and register serve the full corridor, so system cost is amortised across the reach rather than the cohort.

### 7. Budget

| Component | Amount (₱) |
|---|---:|
| Portable 1 m³ desludger, trailer and mother-tanker charter | 2,200,000 |
| Access remediation: floor works and access ports, 400 × 2,800 | 1,120,000 |
| Crew, 8 × 234 days × 900 × 1.25 loading | 2,106,000 |
| Hauling and tipping to permitted facility, 100 loads × 4,700 | 470,000 |
| Hoses, PPE, spill kits and consumables | 400,000 |
| Register, scheduling and manifest system | 350,000 |
| Barangay coordination and household engagement | 300,000 |
| Chain-of-custody audits | 180,000 |
| **Direct service subtotal** | **7,126,000 (71.3%)** |
| Overflow alarms, 400 × 600 | 240,000 |
| Telemetry gateway and connectivity | 120,000 |
| Bank observation and evaluation staff | 400,000 |
| Laboratory monitoring, 5 stations × 12 rounds | 180,000 |
| Survey, permits and legal review | 300,000 |
| Analysis and closeout | 200,000 |
| Controlled contingency | 1,434,000 |
| **Total** | **10,000,000** |

Direct service alone exceeds ₱7 million, so overhead never carries the primary-stream test.

**Economics, stated plainly.** Year-one cost is ₱25,000 per enrolled household. That figure is capital-heavy and should not be read as a service cost: the portable unit and register persist beyond the pilot. Steady-state recurring cost is crew, hauling and audits at roughly ₱2,750,000 across a 1,360-household corridor, or about ₱2,000 per household per year — within the US$10–30 per household annual benchmark for dense Southeast Asian cities, and comparable to the environmental charge already collected on every water bill.

### 8. Quantitative baselines and targets

| Measure | Baseline status | Twelve-month target |
|---|---|---|
| Tank register coverage | 0% — no register exists | 100% of footprint |
| Households desludged on schedule | 13% ever desludged (2016 national sample) | ≥95% of scheduled cohort |
| Tier C households served without manual handling | Not measured | ≥90% |
| Volume with valid manifest to permitted facility | Not measured | 100% |
| Overflow or bypass alarms dispositioned within 24 h | Not measured | 100%; zero unresolved |
| Fecal coliform at reach outfall | 2.4×10⁵–1.1×10⁶ MPN/100 mL (2025) | Report change with interval |
| BOD at reach outfall | 24.2–27.8 mg/L main stem (2018–19) | Report change with interval |
| Cost per household served | ₱25,000 year one | Report; target ≤₱2,000 recurring |

Targets are decision thresholds, not predictions. Environmental results are reported as concentrations at one station, never as river-scale loads or as evidence of restored water quality.

### 9. National scaling blueprint

The scaling argument follows the funding gap. The DPWH programme excludes Metro Manila by design, and only two LGUs nationwide hold subsidy approval. Manila, Caloocan, Pasay, Makati and Quezon City therefore sit outside the national vehicle while carrying the highest septage loads in the country. Stage one replicates the register and access-tier protocol across two or three additional Pasig-connected esteros. Stage two extends to Tullahan, where the same access constraint governs. Stage three addresses Meycauayan, where industrial co-contamination requires separate screening before any household programme is claimed to help.

Replication is a sequence of conditional decisions, not a multiplication of one site's result.

### 10. Implications

**Environment.** The intervention removes oxygen-demanding and fecal loading at source. It makes no claim of river restoration: the modelled 83% domestic share is a model, 57% of measured fecal sources remain unassigned, and one reach is not a river. No structure is placed in the channel, no drain is closed, and no sediment is disturbed.

**Health.** Thirty-six percent of under-five children in low-income Metro Manila reported diarrhoea in the preceding four weeks. The pilot does not claim to reduce disease; it claims to reduce exposure opportunity, and it forbids manual handling of septage by students or volunteers. Occupational safety law covers employees only, so the no-volunteer rule is project policy, not a legal citation.

**Community.** The barangay holds the register, sets the collection window, and receives the manifest record. Handover requires a named budget holder before month 12; otherwise the equipment is removed and the register transferred.

### 11. Limitations

The 13% figure is a 2016 low-income sample, not a Paco measurement. No published measured apportionment of BOD exists for the Pasig; the 83% is modelled. No Philippine study isolates septage as a health exposure. One reach provides no spatial replication, and concurrent national programmes — Kalinisan sa Bagong Pilipinas, Bayanihan sa Estero, the city's weekly barangay cleanups — will confound any observed change. The pilot reports those confounders rather than adjusting them away.

---

# C. Evidence ledger

Every number in the draft, with its tag. **A human author must open each link before submission.**

| Claim | Source | Tag |
|---|---|---|
| Pasig Class C; BOD 7, DO 5, TSS 80, FC 400 | DAO 2016-08 | VERIFIED |
| BOD 27.8 (2018) / 24.2 (2019), six stations | Water Practice & Technology, 2024 | VERIFIED |
| 7/8 pass DO on neap, 1/8 on spring | ibid. | PARTIAL |
| FC 2.4×10⁵–1.1×10⁶, Jan 2025 | Kyushu Univ. repository, 2025 | VERIFIED |
| CCME-WQI "Poor" all stations 2010–2024 | Environ. & Ecol. Res., 2026 | VERIFIED |
| 83.4% domestic BOD (modelled) | PEMSEA, 2013 | PARTIAL |
| 93% of known fecal = sewage; 57% unknown | dela Peña et al., Front. Water, 2025 | VERIFIED |
| 60/33/7 uncited; traces to 1990s estimate | Gorme et al. 2010; Palanca-Tan 2017 | VERIFIED |
| 13% of tanks ever desludged | WB/IFC, 2018, n=800 | VERIFIED |
| 70% under house; 71% narrow access; 18% >20 m | ibid. | VERIFIED |
| 22% no cemented bottom | Palanca-Tan, 2015 | VERIFIED |
| Free desludging; 20% environmental charge | Maynilad / MWSS-RO | VERIFIED |
| 60–71% avail free desludging | MWSS-RO, 2019; Context.ph, 2023 | VERIFIED |
| DOH AO 2019-0047 self-contradiction | AO 2019-0047 Pt. VI.A.9 vs VI.C.1 | VERIFIED |
| NSSMP excludes Metro Manila; 2 LGUs approved | DPWH POM, 25 Mar 2026 | VERIFIED |
| No septage plant in City of Manila; 5 in MM | Eawag; Maynilad 2024 | VERIFIED |
| 1.58 m³ per tank | Maynilad 2019 (233,000 m³ ÷ 147,900) | VERIFIED (computed) |
| 10 m³ tanker; 1 m³ portable unit | Maynilad 2020; Manila Water 2025 | VERIFIED |
| ~1,360 households in 150 m corridor | PSA 2020 + density arithmetic | ASSUMPTION |
| 36% under-5 diarrhoea, 4 weeks | WB/IFC, 2017 | PARTIAL |
| Sanergy abandoned pressure transducers | Sustainability, 2019 | VERIFIED |
| Float alarms USD 50–250 | HomeServe, 2024 | VERIFIED |
| US$10–30/hh/yr desludging benchmark | PMC, 2026 | PARTIAL |
| 872,625 sacks, 1,467 rangers, H1 2025 | DENR-NCR | VERIFIED |
| 49 streets flood from garbage | MMDA, Jul 2025 | VERIFIED |
| Brgy 672 pilot: $438k, 58 HH, 87% BOD | ADB TCR 46308-001 | VERIFIED |

# D. Still unverified — must close before drafting final text

1. **The actual reach.** No verified 1-km centerline, endpoints or chainage for Estero de Paco exists in this research. OSM's named way covers only 397 m. Gate G1 is unpassed.
2. **Paco-specific desludging rate.** The 13% is national low-income. A barangay-level figure would be far stronger.
3. **Access tiers in Paco.** The 70/71/18% figures come from a 2016 national survey, not this reach.
4. **Whether Maynilad's free desludging actually reaches Barangays 671–687** on schedule, and how many households are enrolled.
5. **Receiving facility capacity.** Which septage plant would accept the loads, at what tipping fee, on what hours.
6. **Whether the portable unit is purchasable, leasable, or only available through the concessionaire.**
7. **Organizer ruling on AI use** — Gate G0, still unpassed and still decisive.

# E. What a human author must now do

- Read every source in §C. Delete any claim you cannot personally confirm.
- Replace the 400-household assumption with a counted inventory, or label it as an assumption in the text.
- Walk the reach with an adult and a mapper, or drop the site-specific claims to a "proposed reach."
- Rewrite the prose in your own voice. The structure and evidence can inform you; the sentences must be yours, and only if the organizers permit it.
