# Simulation & Data Stack
## What is buildable for the Estero de Paco entry, and what is decoration

**Date:** 14 November 2026
**Status:** options assessed against verified data availability, not aspiration
**Constraint:** Phase I is a written case solution plus a poster. Anything below is *supporting evidence*, never a substitute for the submission.

---

## 0. The decision that comes first

A water-flow simulation answers: **where does the water go, and how long does it stay?**

It does not answer: **how much BOD comes out.** That question was already closed in the [verification annex](../verification/2026-11-13-source-verification-annex.md) — a tank emptied once a decade releases 0.43 L/day, and four occupants discharge ~40 g BOD/day regardless. A flow model will not reopen it.

So the simulation is worth building only if it serves the actual thesis: **which barrier binds — access or awareness.** Two of the three builds below serve that directly. The hydraulic model does not, and should be treated as optional.

| Build | Serves the thesis? | Cost | Time | Judged defensible? |
|---|---|---|---|---|
| **A. Tidal exchange model** | Indirectly (fate of an overflow) | ₱0 | 3–5 days | Yes, if reported as a bound |
| **B. Service simulation (SimPy)** | **Directly — it tests the two arms** | ₱0 | 5–8 days | Yes, strongly |
| **C. Satellite channel map** | Yes (supplies A's area, G1's geometry) | ₱0 | 3–4 days | Yes, if modest claims |
| D. HEC-RAS/SFINCS reach model | Weakly | ₱50k–120k | 3–4 weeks | Only with survey + 2 loggers |
| E. Sensor node | No (it is the pilot, not the paper) | ₱3,700/node | 1 week | Yes, but out of scope for Phase I |

---

## 1. What the data actually allows

Verified 13–14 November 2026. This table is the whole reason to be modest.

| Source | What it gives | What it does not | Access |
|---|---|---|---|
| **IOC Sea Level Station `mani`** (GLOSS 73, South Harbor) | Real-time water level, ~5-min, JSON | Flow, current, anything inside the estero | `ioc-sealevelmonitoring.org/service.php?query=data&code=mani&format=json&period=1` |
| **UHSLC station 370** | Hourly QC'd sea level, 1984→present | Same | `uhslc.soest.hawaii.edu/stations/?stn=370` |
| **PSMSL 145** | Monthly means, 1901–2024 | Anything sub-tidal | `psmsl.org/data/obtaining/stations/145.php` |
| **Sentinel-2 L2A** (tile T51PTS) | 10 m B2/B3/B4/B8; ~5-day cadence; free | Water quality at 30 m width — 3 pixels across | CDSE + STAC API |
| **Sentinel-1 GRD** | 10 m SAR, ~6-day revisit | Anything under dense canopy | CDSE |
| **Planet Education** | 3 m, 8-band, free for university email, 30-day latency | Redistribution; SkySat 50 cm | `planet.com/industries/education-and-research` |
| **Project NOAH hazard maps** | 5/25/100-yr polygons at ~10 m | Channel hydraulics — a 10 m grid cannot see a 30 m channel | `noah.up.edu.ph` |
| **Phil-LiDAR / LiPAD** | **Dead.** Domain no longer resolves | The 1 m DTM Metro Manila needs | Email `lipad@dream.upd.edu.ph`; expect 2–6 weeks or nothing |
| **DENR-EMB water quality** | PDF reports only | Any machine-readable series | FOI request to PRCMO |
| **Open Buildings v3 / Overture** | Footprints incl. informal clusters | Household counts without census anchoring | `sites.research.google/open-buildings` |

**Two hard absences:**
1. **No bathymetry.** LiDAR stops at the waterline. Every DEM-based cross-section is fiction until someone sounds the channel.
2. **No flow data.** The estero has no discharge record at any point, ever.

Any model that pretends otherwise will be caught by one question: *"what did you calibrate against?"*

---

## 2. Build B first — the service simulation

**This is the strongest technical object available to this team**, because it simulates the thing the paper actually claims: a service delivered to 400 households under two notification arms.

### What it is

A discrete-event simulation in **SimPy** (pure Python, free, deterministic seeds, reproducible by a judge with `pip install -r requirements.txt`).

### What it models

```
Household queue ──► Notification (arm 1 or 2) ──► Booking ──► Crew dispatch
                                                              │
                        Access tier F1 / F2 / F3 ◄────────────┘
                                                              │
                    Pump time ──► Transfer to tanker ──► Haul ──► Gate queue ──► Disposal
```

### Parameters, and where each one comes from

| Parameter | Value | Source |
|---|---|---|
| Households | 400 | Design |
| Arm split | 200 / 200 by block | Design |
| Baseline uptake, arm 1 | 55% | MWSS acceptance, 2025 |
| Arm 2 uplift | **the quantity being tested** | Sweep 0–30 points |
| Tank volume pumped | 0.5–1.5 m³ | Service records; 1.58 m³ mean is the annex figure |
| Portable unit capacity | 1 m³ | Manila Water prototype spec |
| Pump rate | 200–400 L/min | Commercial vacuum unit spec |
| Access setup time (F2) | 5–20 min | Hose run, floor access |
| Travel speed in barangay | 10–15 km/h | Assumption, state it |
| Working day | 8 h, 234 days | Budget line |
| No-show rate | 10–20% | Assumption |

### What it outputs

- Households completed per arm, with 95% CI over 200 replicates
- **The arm difference** — the paper's primary endpoint, as a distribution rather than a claim
- A **decomposition** of that difference into physical access work versus response speed
- Cost per household served, and which assumption dominates it
- Sensitivity: one-at-a-time over every parameter a judge might challenge, **not** Sobol indices — a Sobol decomposition was considered and dropped, because seven swept parameters × 200 replicates already costs two minutes and the ranking that matters (floor-work refusal, then response lag) is unambiguous at this resolution. Claiming Sobol without running it would be worse than not claiming it.

### Built, and where to find it

The model exists. `sim/README.md` carries the full parameter provenance, the results tables, the validation checks, and the explicit non-claims. Run it with `python sim/run_scenarios.py --reps 200`.

One correction to the table above, discovered on building it: the model draws tank volume from **0.5–1.5 m³ (mean 1.0)**, below the annex's 1.58 m³ mean, and the README reports the cost consequence (₱5,070 → ₱6,120 per household across the plausible range) rather than hiding it.

### Why this beats a hydraulic model here

The judge's question for a service design is not "what is the Manning's n of the reach" — it is **"what happens if access is the barrier, and what happens if it isn't?"** A SimPy model answers that in one figure. A 2D hydraulic model cannot answer it at all.

---

## 3. Build A — the tidal exchange model

Cheap, and honest if reported as a bound.

### The calculation

```
Plan area A        from the satellite channel map (§4)
Mean tidal range   Δh from the `mani` gauge, 30 days
Tidal prism        P = A × Δh
High-water volume  V = A × mean depth        (mean depth is the weak input)
Fraction renewed   f = P / (P + V)
Flushing time      T_f = V × 12.42 h / P
```

### What it can say

> "Bulk flushing time is of order 1–5 days, dominated by tidal exchange rather than freshwater inflow."

### What it cannot say

Any spatial pattern, any plume path, any concentration. Real tidal trapping makes true flushing **2–5× slower** than the prism estimate — report that as the error direction, not as a correction.

**Report it as a range, never a number.** A single figure will be read as a measurement.

---

## 4. Build C — the satellite channel map

The one place satellite imaging earns its place, because the channel is 20–40 m wide and the questions are geometric, not radiometric.

### Works

| Task | Band / product | Why it works |
|---|---|---|
| Channel centreline and width | Sentinel-2 **B8** (10 m) or **B3** | Channel is 2–4 pixels wide; width is measurable to ±10 m over a reach |
| Water mask / plan area | **NDWI** = (B3 − B8)/(B3 + B8) | Robust at 10 m |
| Structure clearing, March 2025 | Sentinel-1 SAR before/after | 30 m stretches of clearing visible; individual shacks are not |
| Bank change over time | Sentinel-2 stack, 2019→2026 | 5-day cadence, free archive |
| Reach length check for G1 | B8 + OSM roads | Cross-checks the 2.7–3.0 km figure |

### Does not work

- **Turbidity or chlorophyll retrieval.** Ten-metre pixels, three across the channel, adjacency effects dominating. Any map produced will be an artefact of mixed pixels.
- **Individual structure detection.** A 10×15 m shack is one pixel.
- **Bathymetry.** Water is opaque at these wavelengths.

### Access

```
Copernicus Data Space:  https://dataspace.copernicus.eu
STAC search:            https://catalogue.dataspace.copernicus.eu/stac/search
Earth Engine:           free Community Tier, 150 EECU-hours/month,
                        requires a Cloud project + eligibility questionnaire
```

---

## 5. Build D — the reach model, only after G1

Not recommended for Phase I. If the project survives into 2027, this is the correct build:

| Item | Requirement |
|---|---|
| Tool | **HEC-RAS 7.0.2** (2D, diffusion wave) or **SFINCS 2.5.0** |
| Geometry | 9–12 surveyed cross-sections at 100 m spacing |
| Mesh | 4 m cells in channel, 8 m on banks, ~5,000–6,000 cells |
| Manning's n | 0.030–0.040 silted concrete; 0.045–0.070 earth/trash; **report a ±30% band** |
| Downstream BC | Measured water level at the confluence, 15-min, ≥30 days spanning spring and neap |
| Upstream BC | Zero inflow. The head is effectively dead-end. Do not invent a freshwater discharge |
| Calibration | **Two loggers minimum** (confluence + mid-reach) plus a barometer |
| Runtime | SFINCS 5–15 min/simulated year; HEC-RAS 2D 1–3 h/year — a normal laptop is enough |

**One logger at the downstream end calibrates nothing.** It becomes the boundary condition, so every roughness value fits equally well. That is the single most common way a student hydraulic model becomes unfalsifiable.

**Manual cross-sections beat every instrument here.** Staff, tape, three people, one hour per section, ±0.05–0.10 m. An echo sounder reads the *fluff* layer, not the bed, and disagrees with a probe by 0.2–0.5 m.

---

## 6. The sensor node — real, cheap, and out of scope

₱3,680 in parts (e-Gizmo, Taft Avenue, walk-in prices, Nov 2026):

| Part | ₱ |
|---|---:|
| ESP32-S3 DevKitC | 469 |
| JSN-SR04T waterproof ultrasonic | 310 |
| Turbidity sensor + amp | 599 |
| Air780E LTE Cat-1 | 750 |
| RTC + microSD | 250 |
| 2×18650 + TP4056 + solar | 600 |
| IP66 box, glands, desiccant | 450 |
| Sundries | 252 |

**What fails first:** the turbidity window (biofilm in 2–4 weeks), then the ultrasonic face, then the glands. Level sensing is easy; fouling is the problem. LTE Cat-1 on a Smart/Globe IoT SIM is the only realistic link — Metro Manila's free LoRaWAN coverage is 2 online gateways out of 77 mapped.

This belongs to the 2027 pilot, not the 5 December submission.

---

## 7. Where LLMs help, and where they will sink you

### Help

- Generating model input files from a spec (SWMM `.inp`, SimPy process classes, HEC-RAS RAS Mapper tables)
- Writing parsing code for output reports
- Extracting tables from PDFs — **then re-checking 10% by hand**
- Drafting documentation, docstrings, `requirements.txt`, figure captions
- Explaining a diagnostic ("NSE 0.4 vs 0.7") so a student can defend the choice

### Do not

- Let an LLM compute, calibrate, or "run" anything
- Trust a parameter value it supplies — Manning's n, septage generation rates, infiltration. Every parameter needs a citation a human resolved
- Trust a DOI. Assume it is fabricated until opened
- Claim an LLM-in-the-loop agent as the novelty

**The published ceiling is lower than the demo videos suggest.** HydroAgent (2026) benchmarked nine frontier agents on calibrating a hydrologic model: best-of-20-round NSE ranged from **0.75 down to −0.16**, and no model matched a human expert except one, on one gauge. AQUAH (2025) genuinely runs terrain fetch → model → report, and its own authors say calibration and validation are "still needed for operational deployment."

**Use the LLM as a convenience layer, and report its failure rate.** That is a defensible contribution. Claiming it as a modelling advance is not.

### The AI disclosure line

> AI-generated = the substantive intellectual output came from the model.
> AI-assisted = the model was a tool you directed and verified.

Keep a prompt log. Disclose model, version, and what it produced. The test: **if you cannot explain a block of code with the chat window closed, it is AI-generated.** Gate G0 — the organizer's ruling — has still not been asked.

---

## 8. How to put the data in

The instruction set. Create this structure; every downstream script reads only from here.

```
data/
├── 01_tide/
│   ├── mani_2026_raw.json          as downloaded, never edited
│   ├── mani_2026_hourly.csv        parsed: timestamp_utc, water_level_m, flag
│   └── README.md                   station code, datum, retrieval date, gaps
├── 02_satellite/
│   ├── scenes.csv                  scene_id, datetime, cloud_pct, tile, source
│   ├── derived/
│   │   ├── channel_centerline.geojson     chainage 0+000 → 1+000
│   │   ├── channel_width.csv             chainage_m, width_m, method
│   │   └── plan_area.csv                 reach_id, plan_area_m2, method
│   └── README.md                   bands used, thresholds, processing date
├── 03_survey/
│   ├── cross_sections.csv          section_id, chainage_m, offset_m, bed_elev_m, method
│   ├── loggers.csv                 device_id, serial, location, deployed, retrieved, drift_check
│   └── README.md                   datum, instrument, who measured
├── 04_households/
│   ├── register.csv                hh_id, block, arm, access_tier, tank_location, distance_to_road_m
│   └── README.md                   consent basis, anonymisation rule
├── 05_service/
│   ├── manifests.csv               manifest_id, hh_id, date, volume_m3, hauler, facility, receipt_no
│   └── truck_cycles.csv            cycle_id, start, end, hh_id, setup_min, pump_min, travel_min
├── 06_costs/
│   └── quotes.csv                  item, supplier, date, unit, qty, price_php, source_type
└── 07_literature/
    └── claims.csv                  claim, value, unit, source_short, page, verified_on, status
```

### Column rules

- **ISO 8601 dates only** (`2026-11-14T08:00:00Z`). No `11/14/2026` — it is ambiguous and it is the single most common cause of a broken time series.
- **UTC for tide, PHT (UTC+8) for fieldwork.** Record which, in the column name.
- **Units in the header.** `water_level_m`, `volume_m3`, `distance_m`. Never a bare `value`.
- **`method` column on every derived number.** `lidar`, `staff`, `echosounder`, `assumed`, `sentinel2_b8`. A judge asking "where did this come from" should be answerable from the file.
- **`status` in `claims.csv`**: `verified`, `partial`, `withdrawn`. The annex already uses these three words.
- **Never overwrite raw data.** `_raw` files are write-once.

### Retrieval

```bash
# Tide — last 30 days, 5-minute
curl "http://www.ioc-sealevelmonitoring.org/service.php?query=data&code=mani&format=json&period=30" \
  -o data/01_tide/mani_2026_raw.json
```

```python
# Sentinel-2 — STAC search over the reach
import requests
bbox = [120.985, 14.575, 121.000, 14.590]
r = requests.post(
    "https://catalogue.dataspace.copernicus.eu/stac/search",
    json={"collections": ["sentinel-2-l2a"], "bbox": bbox,
          "datetime": "2025-01-01/2026-11-14",
          "query": {"eo:cloud_cover": {"lt": 20}}, "limit": 100},
)
```

### Validation before anything enters the paper

1. **Row count matches expectation.** 30 days at 5-min = 8,640 rows, minus gaps. Print the count.
2. **Monotonic timestamps, no duplicates, no DST.** The Philippines has no DST — any timestamp shift is a bug.
3. **Units checked against a known value.** A Manila Bay tidal range is roughly 1–2 m. If the parse gives 200, the unit is centimetres.
4. **Every derived number has a `method`.**
5. **Reproduce one figure from raw to final by rerunning the script from an empty `derived/`.**

---

## 9. Traps

| Trap | Why it kills the entry |
|---|---|
| **A 2D model with assumed bathymetry** | The result is a drawing of your assumptions. First judge question: "where are your cross-sections?" |
| **Calibrating to the only gauge you have** | Unfalsifiable by construction |
| **Sentinel-2 water quality on a 30 m channel** | Mixed pixels; the map is an artefact |
| **A single flushing-time number** | Reads as a measurement; it is an order-of-magnitude bound |
| **An "AI agent that runs the model" as the novelty** | 2026 state of the art underperforms a human; judges in a science fair will know |
| **Building the pilot instead of the paper** | Phase I is a document. No tank gets emptied before 5 December |
| **Adding a simulation the rubric does not score** | It costs days that T14 and T20 need |

---

## 10. If you build only one thing

**Build B, the SimPy service simulation.** It is the only object on this list that produces the paper's primary endpoint — the arm difference — as a distribution instead of an assertion. It costs nothing, runs on a laptop, and a judge can rerun it.

Then, if there is time, **Build C** for the channel geometry, and **Build A** as its companion bound.

**Build D only after someone walks the reach and sounds ten cross-sections.** Until then it is a picture of an assumption.
