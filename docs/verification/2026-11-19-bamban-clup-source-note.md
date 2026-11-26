# Bamban CLUP source note — located, verified, and what it does (and does not) settle

**Date:** 19 November 2026
**Trigger:** P14 in `SITE_PROFILE_LUCONG_RIVER.md` ("Bamban farms"), which the team believed needed the Bamban CLUP.
**Finding in one line:** the CLUP was located and downloaded in full, but it contains **no Lucong/Lucung River data**. Its real value is as an **adopted regulatory model** for piggery siting, not as a source about the study site.

---

## 1. Where the documents are

The LGU Bamban document library is served from the e.gov.ph news portal, not the dead `bambantarlac.gov.ph` domain:

- Page: <https://elgu-bamban-tarlac-news.e.gov.ph/CLUP>
- Files: <https://elgu-news-cdn.e.gov.ph/bamban-tarlac/pdf/>

The page renders client-side, so its HTML shell is empty; the links are embedded in the Next.js payload. All twelve documents were downloaded to `research/sources/bamban_clup/`.

| Local file | Size | Text layer | Pages |
|---|---:|---|---:|
| `vol1_land_use_plan.pdf` | 10.3 MB | yes | 256 |
| `vol2_zoning_ordinance.pdf` | 21.2 MB | partial (pp. 85–116 scanned) | 142 |
| `vol3_sectoral_studies.pdf` | 14.7 MB | yes | 278 |
| `vol4_climate_disaster_risk.pdf` | — | **download timed out** | — |
| `vol5_clccap.pdf` | 10.9 MB | yes | 296 |
| `vol6_map_atlas.pdf` | 45.2 MB | yes | 176 |
| `existing_general_land_use_map.pdf` | 12.3 MB | scan | 1 |
| `general_zoning_map.pdf` | 16.2 MB | scan | 1 |
| `overlay_zone_map.pdf` | 16.2 MB | scan | 1 |
| `proposed_land_use_map.pdf` | 14.5 MB | scan | 1 |
| `resolution_381-2025_clup.pdf` | 3.7 MB | scan | 2 |
| `resolution_085-2026_zoning.pdf` | 1.2 MB | scan | 2 |

Helper scripts written alongside: `extract.py`, `render.py`, `show.py`, `pages.py`, `locate.py`.

Vol. 4 should be re-fetched if it is ever needed; it is not needed for the current argument.

## 2. Adoption chain (verified from the scanned resolutions)

1. Sangguniang Bayan of Bamban adopts the updated CLUP — **SB Resolution No. 057-2025**.
2. Provincial Land Use Committee endorses it — **PLUC Resolution No. 01, s. 2025**.
3. Sangguniang Panlalawigan of Tarlac approves the **CLUP 2022–2031** — **SP Resolution No. 381-2025**, session of **4 December 2025**.
4. The Integrated Zoning Ordinance is enacted by the Sangguniang Bayan and signed **8 October 2025**.
5. The Sangguniang Panlalawigan approves the **Zoning Ordinance** — **SP Resolution No. 085-2026**, session of **19 March 2026**.

This is a fully ratified, current, citable local instrument — the strongest kind of Philippine planning source.

## 3. The usable content

### 3.1 Section 21.6 / Table 49 — minimum distances for poultry and piggery farms

Zoning Ordinance, Article VI, Section 21.6, ordinance page 92 (PDF p. 98). Verbatim table:

| Minimum distance (m) | From | Applies to |
|---:|---|---|
| 25 | ground water source | all |
| 200 | major road / highway | commercial **poultry** |
| 500 | major road / highway | commercial **piggery** |
| 1,000 | built-up uses | all |
| 1,000 | other poultry or piggery farms | all |

Plus: "Additions, alterations, and other modifications within the same site shall be subject to the inspection and approval of the local government."

This is the single most useful thing in the whole download. It is a **local, adopted, numeric siting schedule** from the municipality immediately southwest of Concepcion.

### 3.2 Waterway easements

Vol. 1 §2.6.3, p. 201:

> "For all existing creeks and waterways within Bamban, a standard easement of 3.00 meters will be enforced... the municipality will establish a more substantial easement of 20.00 meters for the Sacobia River and the Tarlac River."

### 3.3 Agricultural buffer on the Concepcion boundary

Vol. 1, p. 188:

> "A 15.00m buffer zone along agricultural areas near the municipal boundaries, particularly in Capas and Concepcion, to preserve farmland and maintain environmental integrity."

### 3.4 Bamban aligns its industrial zoning to Concepcion's southwest

Vol. 1 §2.6.9, p. 208:

> "The Municipality of Concepcion has also incorporated industrial zones in its proposed land use plans, particularly in its southwest boundary. To mirror and support this regional alignment, a majority of the southeast portion of Bamban is being zoned for industrial use."

### 3.5 Bamban admits livestock manure as a pollution source

Vol. 1 §1.6.9, p. 82:

> "Livestock Waste: Improper disposal of manure from livestock can contaminate water sources and soil, leading to environmental degradation and health risks."

### 3.6 Existing piggery cluster inventory

Vol. 3, Table 5.2.5 (Existing Livestock and Poultry Farms), and Vol. 1, p. 102. Named piggeries include Brookside Farms Corp., Celevy Farm, Agrihog Corp., C & G Farm, Celeca Agro Farm Inc., 3G Piggery Farms Inc., Masaya Swine Farm Inc., QJJ Piggery Farm Inc., Boston Ridge Piggery Farm. Concentrated in Anupul, San Pedro, Culubasa, Sto. Niño, Bangcu.

## 4. What it does *not* settle

- **No mention of "Lucong" or "Lucung" anywhere** in the 1,148 extracted pages. Bamban drains via the Sacobia and the Tarlac, not the Lucung.
- **No water-quality data for the Lucong.**
- **No identification of specific "Bamban farms."**
- Bamban is therefore **not an upstream source** for the Lucong. Any draft sentence implying that would be factually wrong.

### P14 verdict: partly resolved, and the premise was wrong

The shared boundary is real, and Bamban's own CLUP concedes that the farmland strip along the Concepcion boundary needs protection (the 15 m buffer). But the "Bamban farms" note cannot be read as "Bamban is polluting the Lucong."

Most likely reading: the note refers to the **agricultural belt on the Concepcion side of the shared boundary** — i.e. farms near Bamban, inside Concepcion, not farms in Bamban. The CLUP corroborates that such a belt exists and is zoned agricultural; it does not name the farms. **P14 stays open** and still needs a field check or a MENRO/barangay confirmation.

## 5. Second finding: the river's official name

The Concepcion municipal document spells it **"Lucung River"**, twice, and places it in the **Chico River Basin** (part of the Pampanga River System), as a tributary of the Chico alongside the Parua:

> "The town lies in the Chico River Basin, which is part of the greater and bigger Pampanga River System. It is drained mainly by two (2) big rivers coursing through its territories, the Parua River and the Lucung River (tributaries of the Chico River)."

The entry uses **"Lucong."** Both spellings are defensible (local usage vs. official document), but the paper should not silently use one while the only official source uses the other. Recommended fix: first mention becomes "Lucong (Lucung in the municipal record)" — five words, no budget damage, and it pre-empts a judge's "which river is this?"

## 6. Third finding: a misnamed source file (corrected)

`research/sources/concepcion_clup_2024.pdf` is **not** a CLUP. Its first page reads **"MUNICIPAL GOVERNMENT OF CONCEPCION, TARLAC — CITIZEN'S CHARTER 2024."**

Renamed to `concepcion_citizens_charter_2024.pdf` / `.txt`. No script or draft referenced the old filename, so nothing broke.

The drafts already cite it correctly as *Citizen's charter 2024*, so there is **no mis-citation in the text** — only a misleading filename on disk. Flagging it because a future reader (or judge inspecting the folder) would otherwise assume a CLUP is in hand when it is not.

**Consequence:** the project still does **not** possess Concepcion's actual CLUP or Zoning Ordinance. Any claim of the form "Concepcion has no piggery siting rules" is therefore **unsupported** and must not be written. The defensible version is the positive one: *Bamban has adopted Table 49; Concepcion's zoning ordinance has not been obtained, so whether an equivalent schedule exists is unknown.*

## 7. How this changes the paper

The CLUP does not plug a data hole in §2. It strengthens §4 and §5:

- **§4 (recommendation):** adopt a Concepcion siting schedule on the Bamban model — 25 m from groundwater, 500 m from the highway for commercial piggeries, 1,000 m from built-up areas and from other farms. Zero new research cost, locally legitimate, already ratified.
- **§4 (enforcement):** a 20 m riverbank easement on the Lucong, mirroring Bamban's Sacobia/Tarlac standard. This is concrete and cheap.
- **§5 (scaling):** the Capas–Concepcion–Bamban corridor is being zoned industrial in coordination, so piggery siting pressure will rise, not fall. That is an argument for acting now.

## 8. Open items

- [ ] Re-download `vol4_climate_disaster_risk.pdf` if flood exposure is ever cited.
- [ ] Obtain Concepcion's actual Zoning Ordinance before asserting any gap in it.
- [ ] Resolve P14 by field check, not by document.
- [ ] Decide whether the paper adopts the "Lucong (Lucung)" clarification.
