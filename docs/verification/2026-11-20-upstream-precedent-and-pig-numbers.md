# Upstream, precedent and pig numbers — what the search produced

**Date:** 20 November 2026
**Purpose:** the three threads requested for the Introduction and Rationale — an upstream piggery inventory, a precedent for a shed-level collection service, and a number for the pig population.
**Rule followed:** nothing enters the paper unless a held source supports it. Inferences are labelled.

---

## 1. Is Bamban upstream of the reach?

Partly, and the honest answer is "the drainage comes from that side, but nobody has traced the drains."

Traced on OpenStreetMap via the Overpass API (20 Nov 2026), querying `waterway` within 250 m of Santiago Bridge (15.3300 N, 120.6284 E):

| OSM id | Name | Type | Course |
|---|---|---|---|
| 265729651 | **Sapang Kawayan** | river | 15.3253, 120.5845 → 15.3335, 120.7383 (west to east) |
| — | Susuba Creek | creek | 6 ways, 15.2845–15.3253 N, 120.559–120.5867 E |

Only one waterway lies within 250 m of the bridge: Sapang Kawayan, and it runs **west to east**, which matches the paper's existing statement that the reach runs downstream from Santiago Bridge toward 120.6367 E. Its western end (15.3253, 120.5845) meets Susuba Creek, which rises in the **southwest at 15.2845, 120.559**.

Anupul's place node is at **15.2909, 120.5633** — about 0.9 km from Susuba Creek's head. So the head of the drainage that reaches the bridge is on the Bamban side of the boundary, and Anupul is the nearest mapped settlement to it.

**What is verified:** the channel's upstream end points southwest, toward Bamban; Bamban's land use plan documents 14 commercial piggeries, four of them in Anupul.
**What is not verified:** that any Anupul drain actually reaches the reach, and where the Concepcion–Bamban boundary crosses the creek. No barangay boundary relation exists in OSM, so a point-in-polygon test was not possible.
**Consequence for the paper:** the Bamban inventory is cited as the regional pattern. The paper says "whether their runoff reaches the reach is untested", which is true and is a Month-1 task.

### The naming problem

OSM names the channel at the bridge **Sapang Kawayan**, not Lucong. The municipal charter calls it **Lucung**; EMB's station is at Santiago Bridge. Three names, one channel, most likely. This is worth one question to MENRO, because a judge who opens OSM will see the other name. The paper does not mention the OSM name.

## 2. Pig numbers

| Source | Figure | Note |
|---|---|---|
| Municipality of Bamban, CLUP Vol. 3, Table 5.2.5 (PDF pp. 187–188, doc pp. 179–181) | **21 livestock and poultry establishments**, listed by barangay and name | Table's own total row says 21; the extracted rows number 20 (14 piggeries + 6 poultry). One row may have been lost at the page break. **Cite the table, not a hand count.** |
| Same, by barangay | Anupul 6 (4 piggeries: Celevy, Brookside, Agrihog, C and G), Bangcu 2, Culubasa 2, San Pedro 3, San Rafael 2, VDR 5 | Named corporations include Agrihog Corp, 3G Piggery Farms Inc., Masaya Swine Farm Inc., Cathay Farms Development Inc., Bounty Fresh (poultry) |
| Bamban CLUP Vol. 1, settlement section | Anupul "has a strong presence of piggery and poultry farms … along McArthur Highway", naming Brookside, Celevy, Boston Ridge, Anupul Farm, Poultrypure | More names than Table 5.2.5; the table is sourced to MPDO 2016, so the prose may be newer |
| Concepcion Citizen's Charter 2024 | "There are also livestock industries in the town which are located in the agricultural areas" | Official, municipal, and the only municipal statement we hold |
| **Concepcion Farms, Inc.** — Tarlac Weekender, 3 Sept 2017 | **more than 10,000 heads**, >5 ha, Barangay San Jose, ~500 m from the commercial district, along the Concepcion–La Paz road | One farm in one barangay, larger than the paper's entire assumed cluster |
| Charoen Pokphand Foods, 2012 (trade press) | two swine farms in Concepcion; 25,450 parent-stock capacity; ₱1.352 bn | Corroborates industrial-scale swine in the municipality |
| PSA RSSO III, 20 June 2025 | Tarlac hog production **13,108.77 t live weight**, Q1 2025, +4.37% year on year | Provincial, not municipal. PSA publishes no municipal hog inventory |
| PCAARRD, 2024 | Tarlac among the country's top five swine provinces | Provincial scale only |

**Why no municipal head count:** PSA's Livestock and Poultry Survey publishes province-level inventory and volume. Municipal figures live in the municipal agricultural profile or the CLUP, neither of which is public for Concepcion. So the paper's "15 sheds × 12 head" remains an assumption, and the Concepcion Farms figure shows how far off it could be. **P8 is now the single most valuable piece of fieldwork.**

## 3. Precedent for a shed-level collection service

**No Philippine LGU or cooperative is documented running one.** What exists falls into three buckets, and the gap between them is the project's novelty claim.

### Bucket 1 — the rule, without the service

| LGU | Instrument | What it requires | What it does not do |
|---|---|---|---|
| **Naga City** | Ordinance 2017-073 (enacted 10 Oct 2017) | Farm registration as a condition of the business permit; three-chamber septic tank; **biogas digester**; sealed warehouse for wet manure; mortality pit; ECC; PCO; quarterly joint inspection; Mayor may issue cease-and-desist and cancel the permit | Moves no manure. The farm must comply or close |
| Naga City | Ordinance 2024-086 (6 Aug 2024) | Tightened: backyard ≤10 hogs, no expansion of commercial farms, wastewater discharge permit, zoning clearance, quarterly inspection | Still no collection service — and the amending ordinance says complaints "continue" |
| Calamba, Misamis Occidental | Ordinance 07-s.2020 | Barangay clearance, sanitary permit, ECC for large farms, septic tank | No service |
| Narvacan, Ilocos Sur | Ordinance 02-s.2023 | Task force; certificate to operate as a permit condition; biogas digester or septic tank; 25 m from groundwater | No service |
| Bayog, Zamboanga del Sur | Ordinance 13-191-16 | 500–1,000 m from built-up areas; 200 m from highways; MENRO inspection | No service |
| Aguilar, Pangasinan | Ordinance 57-s.2024 | Regulates piggery and poultry operation | No service |

**The Naga pair is the strongest citation in the whole search.** A city wrote the strictest farm ordinance in the country, enforced it through the business permit, and five years later amended it because odor and health complaints continued. That is the argument for a service in one sentence, and it comes from the LGU itself.

### Bucket 2 — the digester, on the farm

- Rockefeller Poultry Farm, Polanco, Zamboanga del Norte: four lagoons and a dome digester funded by a ₱5 m DOST SETUP loan; 50,000–100,000 head; electricity cost cut from ₱800–900k to ₱40–50k a month (*Daily Tribune*, 23 Aug 2026).
- Bantayan Island, Cebu: co-digestion at 25 t/day chicken dung, 200 m³/day pig slurry, 9 t/day Napier grass; 400 kW (IEA Bioenergy / Sustainability 2019 case study).
- Majayjay, Laguna (IDRC study, data as of Dec 1998): 80% of backyard and commercial farms discharge to creeks; **collection is named as the heaviest operating cost** of a hog-waste plant.

### Bucket 3 — the prototype

- Marikina River Basin feasibility study: 15 m³/day swine slurry + 5 m³/day food waste → 882 Nm³/day biogas, 1,611 kWh/day.

**Verdict for §4.** The novel element is not digestion, not regulation, and not farm-scale digesters. It is a hauler that moves manure from many small sheds to one digester, with the permit as the enforcement hook. No held source shows anyone in the Philippines doing that, and two sources show why the alternatives stall.

---

## Reference entries this adds

**APA 7, to be added if cited:**

- City Government of Naga. (2017). *Ordinance no. 2017-073: An ordinance regulating the operation of commercial and backyard poultry, piggery and other livestock farms in Naga City*. https://www2.naga.gov.ph/wp-content/uploads/2021/06/ord2017-073.pdf
- City Government of Naga. (2024). *Ordinance no. 2024-086: An ordinance establishing additional regulatory measures in the operation of commercial and backyard poultry, piggery and other livestock farms in Naga City*. https://www2.naga.gov.ph/sp_ordinances/ordinance-no-2024-086/
- Tarlac Weekender. (2017, September 3). *Prov'l vs town dads brewing in Tarlac over 'nuisance' piggery farm*. https://www.tarlacweekender.com/provl-vs-town-dads-brewing-in-tarlac-over-nuisance-piggery-farm/
- Municipality of Bamban. (2026). *Comprehensive land use plan 2022–2031, Volume 3: Sectoral studies* (Table 5.2.5, Existing livestock and poultry farms). https://elgu-bamban-tarlac-news.e.gov.ph/CLUP

## What is still owed

1. **P8** — the shed census. Now demonstrably the weakest number in the paper.
2. **MENRO confirmation** of the channel's name and of which upstream drains reach it.
3. A decision on citing Tarlac Weekender alone for the 2017 closure. Two articles from the same outlet corroborate each other; nothing independent does. The paper attributes the legal reason to the vice governor, which is what the report actually says.
