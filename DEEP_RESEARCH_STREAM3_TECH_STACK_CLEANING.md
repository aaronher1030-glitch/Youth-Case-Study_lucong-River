# Deep Research: Stream 3 Tech Stack — Water Testing, Pollutant ID & River Cleaning
> Generated 2026-11-16 | Depth: deep (degraded: solo retrieval) | Sources: 30

Companion to `DEEP_RESEARCH_RF2027_WATERWAY_FEASIBILITY.md`. Answers: what tech stack should the CSC paper propose for (a) testing the water, (b) identifying pollutants, (c) cleaning the river — phased **Month 1 acquire → cleaning → maintenance** — at ₱10M plan level for one 1-km urban estero reach (Estero de Paco context), and which published plans can be borrowed. Per the team's decision, the paper now **pivots to Stream 3 (in-river restoration)** as the ≥70% stream.

## TL;DR

For a 1-km tidal estero, the defensible Stream 3 stack is **low-tech, locally built, labor-intensive**: 1–2 locally fabricated floating trash booms (TrashBoom-type) + a small boat crew with hand extraction + sorting/weighing + a lab-backed monitoring line — not imported machines. The Ocean Cleanup Interceptor, Mr. Trash Wheel, and bubble barriers are designed for rivers/harbors far larger and costlier than a ₱10M pilot; Seabin is contraindicated by peer-reviewed evidence. The single strongest finding across all precedents is that **cleaning without source control and a funded maintenance owner reverts** (ADB Estero de Paco; PRRC abolition), so the 3-phase plan must hard-wire Phase 3 governance from Month 1.

## Executive Summary

Three questions were researched: what to test with, how to identify pollutants, and how river cleaning actually works at this scale.

**Testing the water.** A two-tier stack is standard: (1) a handheld multiparameter meter for field readings (pH, dissolved oxygen, conductivity, turbidity, temperature) — the YSI ProDSS class costs about US$2,267 (~₱130k) and mid-tier Hanna/Milwaukee units run ₱15k–70k [1][2][3]; and (2) an accredited laboratory panel (BOD, COD, ammonia, phosphate, nitrate, TSS, fecal coliform) benchmarked against DENR water quality guidelines (DAO 2016-08, updated by DAO 2021-19) [4][5]. Philippine capacity exists: LLDA runs an accredited water laboratory (10–15 working days turnaround) and EMB maintains a recognized-laboratory roster [6][7]. Citizen-grade strips and colorimetric kits are cheap but accuracy is parameter-dependent — physical parameters (pH, temperature, DO) agree well with labs, while nitrate/phosphate strips are unreliable [8][9][10][11], so they are screening tools only.

**Identifying pollutants.** For macroplastics, the working method everywhere is capture-then-sort with brand audits (Ocean Conservancy ICC data cards) [15][41]. For microplastics, the Mekong River Commission's 2024 riverine protocol (manta/net surface sampling, density separation with saturated NaCl, filtration, microscopy) is a free, replicable SOP [12], with peer-reviewed extraction protocols [13] and an analytical review [14] as backup; polymer-level ID (FTIR) is a partner-lab task. Heavy metals (Pb, Hg, Cd) are lab-only (AAS/ICP) — plan a small quarterly panel via an EMB-recognized lab [7].

**Cleaning the river.** The proven machinery spectrum: passive booms/traps (TrashBoom, Bandalong, Interceptor Barrier/Guard) that concentrate floating litter for extraction; mechanical extraction (crew + boat, conveyor barges like Interceptor Tender); and high-capital machines (Interceptor Original, Mr. Trash Wheel) for large rivers and harbors [15][17][18]. Multi-criteria studies favor simple booms for small rivers [24]; boom performance is real but design- and flow-dependent [23]. Failures to avoid: Seabin showed "minimal benefit" and bycatch mortality in a tidal-marina trial [30]; river-spanning racks can cause flood backwater (already established via Honingh 2020 in the dossier); the 86% bubble-barrier capture figure is vendor-reported and requires compressor infrastructure [27][28][29].

**Operations and the maintenance lesson.** The closest precedent is literally the target site: the 2009 PRRC physical cleanup of Estero de Paco (bank clearing, dredging, aerators) left the canal still unable to sustain aquatic life; the follow-on ADB pilot (2012–2015, US$438,361) succeeded by pairing low-cost infrastructure with River Warriors, waste storage points, MRFs, and a turnover MOU — its stated lesson is that infrastructure is wasted if dumping behavior continues [31]. The Pasig program's commissioner (PRRC) was abolished in 2019 with the river called "uncleanable," after having removed ~30 million kg of waste — a governance, not a technology, failure [32][33][34]. Malaysia's River of Life (RM 3.36B, 110 km) budgets 588 gross-pollutant-trap/log-boom/trash-rack units but identifies **sewage (80.1% of pollution load), not floating litter, as the main source** — an honest caveat for any water-quality claim a Stream 3 paper makes [35].

## 1. Status Quo — the tech stack, component by component [Confidence: High]

### 1.1 Water-quality testing stack

| Tier | Product | Parameters | Indicative cost | Role in the pilot |
|---|---|---|---|---|
| Flagship | YSI ProDSS multiparameter (4-sensor) | pH, DO, cond., turbidity, temp | US$2,267 ≈ ₱130k [1] | One unit, monthly rounds |
| Mid | YSI ProQuatro | Same, 4 ports | US$1,537 ≈ ₱90k [2] | Alternative flagship |
| Mid | Hanna HI98194 / Milwaukee-class handhelds | pH, DO, cond., turbidity | ₱15k–70k [3] | Backup + student training |
| Screening | Test strips, colorimetric kits, turbidity tube, Secchi disk | nitrate, phosphate, pH, turbidity | ₱2k–15k per kit [8][10] | Weekly screening between lab rounds |

Field readings must be anchored to the national benchmarks: DENR DAO 2016-08 defines water-body classification and guidelines (Class C = fishery water; esteros typically Class C/D) [4], updated for selected parameters by DAO 2021-19 [5]. Laboratory analysis in-country is available from LLDA's laboratory (processing 10–15 working days) and EMB-recognized private labs [6][7]; the dossier already budgeted ₱3,000/sample from the PH Sanitation Sourcebook — carry it with a verify-at-quote-time flag. A realistic monthly panel: BOD5, COD, NH3-N, PO4-P, NO3-N, TSS, fecal coliform at 5 stations.

Evidence on cheap kits is mixed and parameter-specific: a 2025 Frontiers study found low-cost colorimetric nitrate/phosphate tests unreliable for citizen data [8]; a 2025 PMC validation found strong lab correlation (r > 0.85) for pH, lead, hardness using hybrid protocols [9]; South African strip testing found pH and nitrate acceptable but hardness error-prone [10]; an Indonesian river comparison found citizen/researcher agreement high for physical parameters [11]. Rule for the paper: **strips/kits = trend screening; accredited lab = the decision-grade data**.

### 1.2 Pollutant identification

- **Floating/macrolitter characterization:** sort, count, weigh, and brand-audit captures using the Ocean Conservancy ICC data card (free, field-proven, globally comparable) [15][41]. This doubles as the paper's root-cause evidence.
- **Microplastics:** MRC's *Protocol for Riverine Microplastic Monitoring* (2024) is the free SOP — surface sample (net/manta or grab), density separation with saturated NaCl, oxidative digestion, filtration, microscopy [12]; step-by-step extraction/analysis protocols are published [13] and a 2026 review catalogs the analytical options [14]. A student-feasible pilot: 2 rounds × 3 stations, consumables-level cost, polymer confirmation (FTIR) as a partner-university courtesy analysis.
- **Heavy metals:** Pb/Hg/Cd by AAS/ICP at an EMB-recognized laboratory [7]; 2 rounds × 3 stations is enough to characterize, not monitor, this pollution class.

### 1.3 Cleaning machinery — what exists and what fits

| Technology | How it works | Scale/cost reality | Fit for a 20–30 m tidal estero on ₱10M |
|---|---|---|---|
| **Locally built TrashBoom-type boom** | Floating HDPE-pipe barrier with suspended net, angled to bank collection point; low-cost, local, low-tech ("3L" model) [25][24]; modular variants exist (CLEAR RIVERS LT1 [26]) | Local fabrication; thousands-class per line [25] | **YES — primary capture device** |
| Bandalong litter trap | Floating HDPE trap using current to guide litter into basket [19][20][22] | Turnkey import; city-scale procurement (Fort Worth installs) [20][21] | Optional second unit; import cost likely prohibitive — get quotes |
| Interceptor Barrier + Tender | Permeable U-barrier + conveyor barge offloading to dumpster [15] | Program-scale (Jamaica gullies) [15] | Barrier concept borrowable; barge overkill |
| Interceptor Original | Solar-powered conveyor catamaran [15] | Deployed in 6 countries; multi-million-USD class [15] | **NO** |
| Mr. Trash Wheel | Waterwheel + barge conveyor, harbor interception; 1,253 t by 2019 [17][18] | Harbor scale, US-funded [17] | **NO** (design inspiration only) |
| Great Bubble Barrier | Diagonal air curtain; vendor-reported 86% floating-plastic capture in Amsterdam [27][28][29] | Compressor + power + engineered install | **NO** (cost/infrastructure; vendor-reported figure) |
| Seabin | Pumped skimmer bin | Peer-reviewed tidal-marina trial: "minimal benefit," bycatch mortality [30] | **NO — contraindicated** |
| Manual crew + boat + nets | Daily extraction from boom point and banks; sorting, weighing, hauling | Labor-dominated; the actual workhorse of every program cited [15][31][37] | **YES — the core of Phase 2** |
| Dredging (silt) | Amphibious excavator or slurry pump | DPWH proceedings cite ₱36–67/m³ in specific contexts — treat as indicative only; estero-scale pumping is costlier [36] | Small spot-dredging allowance only |

**Cross-cutting failure evidence (carry into the paper):** boom capture varies with design, flow, and vegetation [23]; multi-criteria analysis of Indonesian river deployments ranked simple TrashBooms best overall [24]; Clean Currents' Citarum project fought seasonal water-level swings and water-hyacinth outbreaks that defeat rigid hardware [37]; Ichthion downgraded from complex to simple technology at its second site after maintenance burden [37].

## 2. Emerging Trends [Confidence: Medium]

- **Open operational playbooks.** The Clean Currents Coalition (8 rivers, 8 countries, Benioff Ocean Science Lab) published a free Field Guide covering permits, site selection, technology selection, waste management, installation/O&M, data collection, community engagement, communications, and finance & budget [37][38] — the single most borrowable blueprint found (Section 4 maps it).
- **City-scale portfolios instead of single machines.** The Ocean Cleanup's 30 Cities Program runs Interceptor families per city (Kingston, Mumbai) with an end-to-end process: city assessment → Smart River Survey research → deployment/ops → waste management → coastal sweeps [15].
- **Data-first cleanup.** ICC-style brand audits and AI-camera debris categorization (Ocean Cleanup's Smart River Survey) are becoming the standard evidence layer linking captured waste to upstream sources [15][41].
- **Hybrid monitoring.** Peer-reviewed 2025 work supports combining cheap citizen measurements with periodic lab validation rather than either extreme [9][11].

## 3. Critical Assessment — why river cleaning fails, and what a skeptic will say [Confidence: High]

1. **Cleaning alone reverts.** At Estero de Paco itself, the 2009 physical cleanup (dredge, aerators, bank clearing) failed to restore the canal; the ADB pilot's own lesson: infrastructure is wasted if dumping behavior continues [31]. A Stream 3 paper that promises lasting water quality from booms alone is not credible.
2. **Maintenance is a governance risk, not an engineering one.** PRRC — which had removed ~30 million kg of waste — was abolished in 2019; Pasig was called "uncleanable" [32][33][34]. Phase 3 must name the maintenance owner (barangay + LGU MOA, matching the ADB turnover model [31]) before Month 1 ends.
3. **Litter is not the main water-quality driver.** River of Life attributes 80.1% of Klang's pollution load to sewage; floating-litter hardware improves aesthetics and solids but BOD/pathogen gains come from sanitation investment [35]. The paper should promise litter-flow reduction (measurable) rather than Class-C water compliance (not achievable by cleaning).
4. **Vendor numbers are optimistic.** The 86% bubble-barrier figure is company-reported [27]; Interceptor tonnage claims come from project media [16]. Independent peer-reviewed evaluations exist and are unflattering when hardware is mismatched (Seabin) [30], boom efficiency is design-dependent [23].
5. **Tidal reversal double-counting** (already in the dossier): in a tidal estero the same item can pass a transect twice; counting rules must be pass-adjusted, and the boom must have a flood bypass or it becomes a flood hazard (Honingh 2020, dossier ref [8]).

## 4. Action Plan — three phases (user-specified structure)

Mapped to the kit's 12-month pilot; ₱10M split honoring ≥70% to Stream 3.

### Phase 1 — Month 1: acquire everything needed

- [ ] **Permits & agreements first:** barangay resolution; city LGU; DENR-EMB NCR coordination; flood-control clearance (MMDA/city engineering) for any in-stream structure; right-of-way for the collection point. (CCC Field Guide: permitting is the universal first bottleneck [37].)
- [ ] **Fabricate 2 boom lines** (TrashBoom-type: HDPE floats + galvanized frame + net skirt + anchor blocks + flood bypass/quick-release), ~25 m each, angled 45° to the extraction bank — locally built per the 3L model [24][25].
- [ ] **Buy the monitoring stack:** 1 multiparameter meter (₱90k–130k) [1][2], backup pen meters (₱40k), screening kits/turbidity tube/Secchi (₱25k), Van Dorn sampler + coolers + preservatives (₱45k).
- [ ] **Contract the lab panel:** 5 stations × monthly × ₱3,000–3,500/sample (BOD5, COD, NH3, PO4, NO3, TSS, fecal coliform) via LLDA or EMB-recognized lab [6][7]; book FTIR/metals partner for 2 microplastic + 2 metals rounds [7][12].
- [ ] **Buy extraction equipment:** 2 flat-bottom boats with small outboards (₱500k), nets/rakes/grabs/bins (₱150k), sorting pen + tarpaulins + platform scale (₱100k), PPE for 6 crew (waders, gloves, boots, life vests, first-aid; quarterly replacement — ₱250k), safety/leptospirosis protocol (RA 11058 duties apply).
- [ ] **Stand up the data system:** ICC data cards + ledger + simple dashboard [41]; counting rules pre-registered (downstream-direction passage rate, size class, pass-adjusted for tide — reuse the dossier's decision rule).
- [ ] **Hire & train:** 6 crew + 1 supervisor (wage anchor ₱755/day NCR non-agricultural + 25% loading — dossier §4, NWPC); 2 observation staff; waste-worker vaccination/hygiene briefing.
- [ ] **Sign the hauler + MRF chain:** residual-to-sanitary-landfill contract, recyclables route to barangay MRF (CCC: know your waste-management capacity before capture starts [37]).
- [ ] **Month 1 exit test:** boom installed and load-tested, crew certified, first lab round in from all 5 stations, data system live, MOA drafts (LGU + turnover) filed.

**Phase 1 budget anchor (indicative, machine-checked sums):**

| Block | ₱ |
|---|---|
| 2 boom lines fabricated + anchors + bypass | 600,000 |
| Boats + outboards | 500,000 |
| Hand tools/nets/grabs/bins | 150,000 |
| Sorting pen + scale + tarps | 100,000 |
| PPE (6 crew, quarterly replacement) | 250,000 |
| Crew wages (6 × 260 d × ₱900 × 1.25) | 1,755,000 |
| Supervisor (260 d) | 540,000 |
| Hauling + disposal | 1,500,000 |
| Spot-dredging allowance | 400,000 |
| Training + safety | 240,000 |
| Boom/boat maintenance | 300,000 |
| Community brigades (quarterly) | 200,000 |
| Audits + communications | 160,000 |
| Direct backup | 405,000 |
| **Direct (Stream 3) subtotal** | **7,100,000 (71.0%)** |
| Monitoring stack (meter 135k, backup meters 40k, screening kits 25k, lab panel 210k, microplastics 120k, metals 36k, sampling gear 45k, obs staff 234k, data system 40k, travel 72k) | 957,000 |
| Admin (permits, MOAs, misc) | 343,000 |
| Reserve (16%) | 1,600,000 |
| **Total** | **10,000,000** |

Steady-state burn ≈ **₱400k/month** (wages ~191k + hauling 125k + lab 17.5k + boom/boat maintenance 25k + obs staff 19.5k + PPE/travel/consumables remainder).

### Phase 2 — Months 2–6: cleaning (intensive)

- [ ] Daily boom-point extraction (crew + boat); record kg/day by category on ICC cards [41]; weekly brand audit summary.
- [ ] Twice-weekly bank/wading sweeps of the reach; quarterly community brigade ([37]: capture projects earn their license through visible community value).
- [ ] Monthly lab rounds at 5 stations + field meter readings; weekly screening strips; log vs DAO 2016-08/2021-19 benchmarks [4][5].
- [ ] Adaptive relocation: move boom with seasonal flow/hyacinth loads (Citarum lesson [37]); inspect anchors after every heavy-rain event; flood protocol: open bypass/deflate line when PAGASA raises warning levels.
- [ ] Sort → weigh → divert: recyclables to MRF, residuals to contracted hauling (TerraCycle Bangkok's near-zero-landfill discipline is the aspiration, sanitary landfill is the floor [37]).
- [ ] Mid-pilot review (Month 4): boom capture rate vs passage-rate estimate; if capture < 30% of assessed floating load, re-angle/add second line before spending reserve.

### Phase 3 — Months 7–12: maintenance (steady state + exit)

- [ ] Cadence downshift: boom emptied 5×/week, one deep-clean/month, lab rounds monthly → bimonthly if stable.
- [ ] Trend review each month against baseline with the dossier's decision rule (R = 100×(1−μ_service/μ_no_service), 95% interval, target 20%; LB ≥ T supported, UB < T evidence-against, else inconclusive).
- [ ] Recurrence watch: litter return after any 2-week service gap is the expected failure mode [31][32]; log and report it honestly.
- [ ] Handover package (Month 10–12): barangay/LGU MOA naming the maintenance owner, O&M cost table (~₱400k/month), boom fabrication drawings (local replication), monitoring SOP — the ADB turnover model [31] applied to avoid the PRRC ending [32][34].
- [ ] National scaling blueprint data for the paper: cost/kg removed, capture-rate curve, and a Pasig-tributary replication menu (kit deliverable), benchmarked against River of Life's GPT/log-boom program [35] and Clean Currents' playbooks [37]; frame the replication roadmap the way Plastic Smart Cities builds city action plans from baselines [39][40].

## 5. Open Questions & Caveats

- **"TUS"** — interpreted per your clarification as trash traps/machines; if you meant a specific product named TUS, tell me and I'll add a section.
- Vendor prices (Bandalong turnkey, turnkey boom imports) are not published; the plan prices local fabrication instead. Get two quotes before any real procurement.
- The DPWH ₱36–67/m³ dredging figure comes from a conference paper on specific works [36]; estero pumping rates will differ — treat as order-of-magnitude only.
- Ciliwung's daily task-force operations could not be verified from primary sources in this run; excluded rather than guessed.
- FTIR access in PH universities (UP MSI et al.) is assumed feasible but unquoted; the microplastic line is consumables + courtesy analysis, and must be re-planned if no partner lab commits.
- This report pivots the paper to Stream 3. The existing `docs/superpowers/plans/2026-11-11-waterway-pilot-implementation.md` and the dossier's weighted matrix (source-control 75 vs in-river options 46–59) still recommend Stream 1; the pivot is the team's call and both documents need a Stream 3 rework before drafting §2–§5 of the paper. The ADB/PRRC evidence above is the honest counterweight to keep in the paper's discussion.

## Methodology

Deep-research pipeline run **solo**: subagent dispatch (Agent tool) was disabled in this session, so Wave-1 retrieval (4 planned areas), triangulation, verification, synthesis, and writing were executed by the lead agent directly — a degradation from the skill's standard architecture, noted per its error-handling protocol. 12 WebSearch + 4 WebFetch calls; ~30 sources retained after deduplication. Phase 3.1 spot-check: the 12 highest-impact claims were checked against fetched full pages (ADB case study, CCC Field Guide, Ocean Cleanup rivers page, River of Life official page) or Tier-1/2 abstracts; the DPWH dredging figure is the one claim downgraded to indicative (context-limited snippet). No RESEARCH_CONTEXT.md exists; the existing feasibility dossier is a companion, not a baseline for update. Outline unchanged from plan (<50% structural drift).

## Bibliography

[1] YSI (Xylem) — ProDSS Multiparameter Digital Water Quality Meter (price US$2,267) — https://www.ysi.com/prodss — Accessed 2026-11-16 — Tier: 2
[2] YSI (Xylem) — ProQuatro Multiparameter Meter (price US$1,537) — https://www.ysi.com/proquatro — Accessed 2026-11-16 — Tier: 2
[3] GAIMC — Multiparameter Water Quality Meter Buying Guide (YSI US$1,500–5,000+ band) — https://www.gaimc.com/Newsinfo/Multiparameter-Water-Quality-Meter-Buying-Guide-2025 — Accessed 2026-11-16 — Tier: 3
[4] DENR — DAO 2016-08: Water Quality Guidelines and General Effluent Standards — https://eeci.ph/wp-content/uploads/2021/03/DENR_DAO-2016-08-WQG-and-GEW-2016.pdf — Accessed 2026-11-16 — Tier: 1
[5] DENR — DAO 2021-19: Updated Water Quality Guidelines for Selected Parameters — https://weap-phil.org/wp-content/uploads/2023/02/DAO-2021-19-Updated-Water-Quality-Guidelines-WQG-and-General-Effluent-Standards-GES-for-Selected-Parameters62.pdf — Accessed 2026-11-16 — Tier: 1
[6] Laguna Lake Development Authority — Laboratory Services (water/wastewater analysis, 10–15 working days) — https://llda.gov.ph/laboratory-services/ — Accessed 2026-11-16 — Tier: 1
[7] EMB-DENR — Recognized Environmental Laboratories: ACA Water Analysis and Laboratory Services — https://erlsd.emb.gov.ph/recognized-environmental-laboratory-aca-water-analysis-and-laboratory-services-inc/ — Accessed 2026-11-16 — Tier: 1
[8] von Benzon, E. et al. (2025) — Reliability of low-cost colorimetric phosphate and nitrate tests — Frontiers in Environmental Science 13:1667241 — https://www.frontiersin.org/journals/environmental-science/articles/10.3389/fenvs.2025.1667241/full — Accessed 2026-11-16 — Tier: 1
[9] McCarty, D. A. et al. (2025) — Accessible water quality monitoring through hybrid human-technology approaches (r > 0.85 vs lab) — PMC12000188 — https://pmc.ncbi.nlm.nih.gov/articles/PMC12000188/ — Accessed 2026-11-16 — Tier: 1
[10] South African Journal of Science (2026) — How accurate are water quality test strips? — https://sajs.co.za/pt/article/view/23287 — Accessed 2026-11-16 — Tier: 1
[11] Comparison of Water Quality Monitoring Between Citizen Science and Researchers, Bantimurung River (2025) — ResearchGate 393040426 — https://www.researchgate.net/publication/393040426 — Accessed 2026-11-16 — Tier: 2
[12] Mekong River Commission (2024) — Protocol for Riverine Microplastic Sampling and Monitoring (P-RMM) — https://www.mrcmekong.org/wp-content/uploads/2024/09/P-RMM.pdf — Accessed 2026-11-16 — Tier: 1
[13] Vural, T. et al. (2025) — Protocol for extraction and analysis of microplastics in river surface water (manta trawl) — ScienceDirect S2666166725004630 — https://www.sciencedirect.com/science/article/pii/S2666166725004630 — Accessed 2026-11-16 — Tier: 1
[14] Sotnikova, Y. S. et al. (2026) — Microplastics in River Water: Features of Analytical Approaches — Environments 13(1):50 (MDPI) — https://www.mdpi.com/2076-3298/13/1/50 — Accessed 2026-11-16 — Tier: 1
[15] The Ocean Cleanup — Rivers | The Interceptor (1000 rivers = 80%; Interceptor Original/Barrier/Barricade/Guard/Tender; 30 Cities; end-to-end process) — https://theoceancleanup.com/rivers/ — Accessed 2026-11-16 — Tier: 2
[16] The Ocean Cleanup — Trials New Interceptor in World's Most Polluting River (Motagua, Guatemala) — https://theoceancleanup.com/updates/the-ocean-cleanup-trials-new-interceptor-in-worlds-most-polluting-river/ — Accessed 2026-11-16 — Tier: 2
[17] Nicholas Institute, Duke University — Inner Harbor Water Wheel (Mr. Trash Wheel): ~1,253 tons collected as of 2019 — http://nicholasinstitute.duke.edu/plastics-technologies/inner-harbor-water-wheel-mr-trash-wheel — Accessed 2026-11-16 — Tier: 1
[18] Mr. Trash Wheel — How It Works (solar + hydro power) — https://www.mrtrashwheel.com/how-it-works — Accessed 2026-11-16 — Tier: 2
[19] Storm Water Systems — Bandalong Bandit Litter Trap specifications (4' × 6.5' HDPE) — https://www.stormwatersystems.com/bandalong-bandit-litter-trap — Accessed 2026-11-16 — Tier: 3
[20] City of Fort Worth — Bandalong Litter Trap program page — https://www.fortworthtexas.gov/departments/environmental-services/initiatives/bandalong — Accessed 2026-11-16 — Tier: 2
[21] Hopkins, G. / Storm Water Systems (2024) — Public/Private Partnerships for Trash Trap Technologies (ANJEC presentation PDF) — https://anjec.org/wp-content/uploads/2024/05/Gary-Hopkins-Stormwater-Systems.pdf — Accessed 2026-11-16 — Tier: 2
[22] Global Plastics Hub — Bandalong Litter Trap technology entry — https://globalplasticshub.org/technology/9 — Accessed 2026-11-16 — Tier: 2
[23] Blettler, M. C. M. et al. (2023) — Testing the effectiveness of a river boom under real conditions — Science of the Total Environment (S0048969723005569) — https://www.sciencedirect.com/science/article/abs/pii/S0048969723005569 — Accessed 2026-11-16 — Tier: 1
[24] Budiawan, W. et al. (2023) — TrashBoom design selection by multi-criteria analysis — International Journal of Environmental Science and Development 15(4) — https://www.ijesd.org/vol15/IJESD-V15N4-1485.pdf — Accessed 2026-11-16 — Tier: 1
[25] Plastic Fischer — TrashBoom / low-cost, local, low-tech (3L) model — https://plasticfischer.com/ (see also https://globalfundcoralreefs.org/reef-plus/finance-solutions/trashboom/) — Accessed 2026-11-16 — Tier: 2
[26] CLEAR RIVERS — LT1 Modular Litter Trap — https://www.clearrivers.eu/litter-traps — Accessed 2026-11-16 — Tier: 2
[27] The Great Bubble Barrier — Bubble Barrier Amsterdam: 86% of floating plastic captured (vendor-reported) — https://thegreatbubblebarrier.com/bubble-barrier-amsterdam-a-success-in-tackling-plastic-pollution/ — Accessed 2026-11-16 — Tier: 2
[28] UNESCO — The Great Bubble Barrier (2023) — https://www.unesco.org/en/articles/great-bubble-barrier — Accessed 2026-11-16 — Tier: 2
[29] Plastiverse — The Great Bubble Barrier tool entry (86% Amsterdam pilot; ship/fish passage) — https://www.plastiverse.org/tools/the-great-bubble-barrier — Accessed 2026-11-16 — Tier: 2
[30] Parker-Jurd, F. N. F. et al. (2022) — Evaluating the performance of the 'Seabin' — fixed-point litter removal device for sheltered waters (minimal benefit; bycatch mortality) — University of Plymouth PEARL — https://pearl.plymouth.ac.uk/cgi/viewcontent.cgi?article=1765&context=bms-research — Accessed 2026-11-16 — Tier: 1
[31] ADB / Development Asia (2016) — How to Revive an Ailing River (Estero de Paco pilot: US$438,360.94, 2012–2015; River Warriors; $60k wetland 30 m³/day; turnover MOU; sustainability lessons) — https://development.asia/case-study/how-revive-ailing-river — Accessed 2026-11-16 — Tier: 1
[32] Inquirer.net (2019-11-15) — Pasig River rehab agency abolished (PRRC dissolved; "uncleanable") — https://newsinfo.inquirer.net/1190140/pasig-river-rehab-agency-abolished — Accessed 2026-11-16 — Tier: 2
[33] Department of Budget and Management — PRRC milestones (30 million kg solid waste removed) — https://www.dbm.gov.ph/index.php/management-2/580-prrc-highlights-milestones-and-priority-rehabilitation-activities-for-the-pasig-river-system — Accessed 2026-11-16 — Tier: 1
[34] Jazmines, M. M. (2023) — A case of the Pasig River Rehabilitation Commission's dissolution — Chulalongkorn University thesis — https://digital.car.chula.ac.th/cgi/viewcontent.cgi?article=13523&context=chulaetd — Accessed 2026-11-16 — Tier: 1
[35] River of Life, Federal Territory of Kuala Lumpur (JWP) — River Cleaning (RM 3.36B; 110 km; 8 rivers; 588 GPT/log boom/trash racks; 309 grease traps; sewage 80.1% of load) — https://rolkl.jwp.gov.my/river-cleaning — Accessed 2026-11-16 — Tier: 1
[36] Western Dredging Association 2022 Proceedings (1A-2) — DPWH innovative shoreline/river solutions (dredging cost figures ₱36–67/m³ in cited contexts) — https://www.westerndredging.org/phocadownload/2022_Houston/Proceedings/1A-2.pdf — Accessed 2026-11-16 — Tier: 2
[37] Clean Currents Coalition — Field Guide for Cleaner Currents (permits, site selection, technology selection, waste management, O&M, data, community, communications, finance) — https://cleancurrentscoalition.org/field-guide/ — Accessed 2026-11-16 — Tier: 2
[38] Benioff Ocean Science Laboratory, UCSB — Clean Currents Coalition overview (8 teams, 8 countries) — https://bosl.ucsb.edu/project/clean-currents-coalition/ — Accessed 2026-11-16 — Tier: 1
[39] WWF Plastic Smart Cities — Plastic Smart Guides for Cities (baseline → action plan) — https://plasticsmartcities.org/plastic-smart-cities-guide/ — Accessed 2026-11-16 — Tier: 2
[40] Tasseron, P. F. et al. (2026) — Plastic pathways and intervention strategies in urban waterways (Plastic Smart Cities roadmaps) — ScienceDirect S2667010026000582 — https://www.sciencedirect.com/science/article/pii/S2667010026000582 — Accessed 2026-11-16 — Tier: 1
[41] Ocean Conservancy — International Coastal Cleanup (program + volunteer data card PDF) — https://oceanconservancy.org/work/plastics/cleanups-icc/ and https://www.coastal.ca.gov/publiced/ccd/OC-DataCards_volunteer.pdf — Accessed 2026-11-16 — Tier: 2

## Source Extracts (key quotes for follow-up)

### [15] The Ocean Cleanup — Rivers
- **Summary:** "just 1000 of the three million rivers found around the world are responsible for 80% of riverine pollution." Interceptor family: Original (solar conveyor; Indonesia, Malaysia, Dominican Republic, Vietnam, USA, Thailand), Barrier (permeable U-barrier buffering trash), Barricade (dual booms, Guatemala), Guard (shallow, beachable, "no-return boom"), Tender (conveyor barge offloading to dumpster, shared across sites). 30 Cities Program; end-to-end: city assessment → research (Smart River Survey) → deployment/ops → waste management → coastal sweep.
- **Key quotes:** "Factors like river width, depth, flow speed, debris composition, seasonality, and tides all have a major influence on the success of a river intervention."
- **Source type:** NGO/industry — **Tier 2**

### [30] Parker-Jurd et al. 2022 — Seabin evaluation
- **Summary:** Independent trial in an urban tidal marina (SW UK).
- **Key quotes:** "in this location the Seabin was of minimal benefit in terms of marine litter removal and resulted in mortality of marine organisms."
- **Source type:** peer-reviewed — **Tier 1**

### [31] ADB — How to Revive an Ailing River
- **Summary:** 2009 PRRC cleanup (bank clearing, garbage removal, dredging, floating aerators) left the estero "still reeked and remained unable to sustain aquatic life." ADB pilot Aug 2012–Jan 2015, US$438,360.94: River Warriors; waste collection/transfer/storage points + adjusted truck routes + containers; MRFs at community and Paco Market (segregation paying collector wages); condominial sewerage for Barangay 672 (58 households, 496 people): PVC + sump pit + solar pumps + anaerobic baffled reactor + artificial wetland (30 m³/day, US$60,000). Turnover MOU to local organizations.
- **Key quotes:** "The infrastructure built within the community would have been wasted if people did not know how to use it and if they continued dumping waste in the river."
- **Source type:** multilateral case study — **Tier 1**

### [35] River of Life — River Cleaning
- **Summary:** Official program page. RM 3.36 billion, 110 km, 8 rivers, 13 key initiatives, 76 work packages: 309 communal grease traps, 588 GPT/log boom/trash racks, 10 wastewater treatment, 15 river water treatment plants. Pollution source split: sewage 80.1%, others 12.6%, food outlets 3.9%, industry 3.4%. "Upgrading existing sewerage facilities is the most impactful and important initiative."
- **Source type:** government — **Tier 1**

### [37] Clean Currents Coalition — Field Guide
- **Summary:** Open-access playbook from 8 river projects on 4 continents. Sections: Permits; Site Selection ("observe prospective sites... over multiple seasons"); Technology Selection (Ichthion simplified tech after O&M burden); Waste Management (TerraCycle Bangkok: wash/dry/sort, residual to waste-to-energy; "identify all possible waste management solutions" during siting); Installation/O&M (Citarum: import delays, water-level swings, hyacinth outbreaks; "never abandon derelict infrastructure in a river"); Data Collection; Community Engagement; Communications; Finance & Budget.
- **Source type:** NGO coalition handbook — **Tier 2**
