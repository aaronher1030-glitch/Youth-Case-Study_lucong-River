# Protocol Pack P1–P6
## The Last Meter — Access-Constrained Septage Collection
### Estero de Paco, Manila · Research Fair 2027 · Stream 1

> **Status:** operational draft, version 0.1, 13 November 2026. **Not authorized for field use.** Every protocol here describes future work. Implementation requires Gate G1 (verified reach) through G5 (commissioning sign-off), plus an accountable implementing entity that is not the school team.
>
> **Provenance:** AI-assisted. Subject to Gate G0 (organizer ruling). See `docs/drafts/2026-11-13-paper-draft-v0.1.md`.

---

## 0. How this pack works

Each protocol has the same seven fields, so they can be audited, handed over, or defended individually:

| Field | Answers |
|---|---|
| **Purpose** | Why this protocol exists |
| **Owner** | Who is accountable when it fails |
| **Trigger** | What starts it |
| **Procedure** | Numbered steps |
| **Records** | What is written down |
| **Acceptance** | The objective pass test |
| **Failure response** | What happens when it fails, and who stops work |

**Values marked `[SET AT G1]`** are placeholders that cannot be filled until the reach is verified. Do not guess them.

### Roles

| Code | Role | Notes |
|---|---|---|
| IO | Implementation owner | Local government unit or contracted entity. **Not the school team.** |
| SR | Service registrar | Holds P1 register, issues schedules |
| SV | Service supervisor | Runs P2, owns crew |
| SO | Safety officer | Owns P5, holds stop-work authority |
| EL | Evaluation lead | Independent of daily collection. Owns P6 |
| RF | Receiving facility operator | Permitted septage treatment plant |
| BR | Barangay counterpart | Consent, scheduling, grievances |
| EN | Qualified engineer | Access assessment, structural checks |

### Forms index

| ID | Form | Protocol |
|---|---|---|
| F1 | Tank Register Entry | P1 |
| F2 | Access Assessment Sheet | P1 |
| F3 | Schedule Card | P2 |
| F4 | Desludging Service Record | P2 |
| F5 | Manifest | P3 |
| F6 | Receiving Receipt | P3 |
| F7 | Alarm Disposition Log | P4 |
| F8 | Incident Report | P5 |
| F9 | Consent Record | P5 |
| F10 | Observation Record | P6 |

---

## P1 — Tank Register and Access Tiering

**Purpose.** Create the catchment register that does not currently exist anywhere in the Philippines, and classify every tank into a physical access tier, because access — not price — is the binding constraint.

**Owner.** SR, with EN for tier assignment. BR validates the household count.

**Trigger.** Gate G1 passed and barangay consent obtained.

### Procedure

1. **Define the footprint.** Registry covers all households within `[SET AT G1]` metres of the verified centreline, chainage 0+000 to 1+000. Record the boundary on the map before any door is knocked.
2. **Assign coded identifiers.** `PAC-[barangay]-[sequence]`. No names in the register. Names, if needed for scheduling, live in a separate consent-held contact sheet accessible only to SR.
3. **Walk the access path, not the property.** For each tank record, measure:
   - narrowest path width in metres
   - distance from the nearest legal truck standing point to the tank inlet, in metres
   - number of steps, thresholds and overhead obstructions
   - whether an external access port exists, and its diameter
4. **Classify the tier** using the rule below. EN confirms every Tier C assignment.
5. **Assess tank condition.** Cover type and seal, presence of a cemented bottom, visible cracks, outlet destination, signs of surcharge. Do not open a sealed tank without consent and PPE.
6. **Record desludging history** as self-reported, with a confidence code: `D` documented, `S` stated, `U` unknown. Never present a stated date as documented.
7. **Score risk** using the rule below. Calibrate it against measured sludge depth before it is used to schedule.
8. **Obtain consent** under P5 before the entry is marked active.
9. **Validate.** BR reviews the count per block. Discrepancy above 10% triggers a re-walk.

### Access tier rule

| Tier | Condition | Consequence |
|---|---|---|
| **A** | 10 m³ tanker can stand within 5 m; path ≥2.5 m wide; turning space present | Standard vacuum tanker |
| **B** | Tanker can stand within 30 m; path ≥1.2 m | Tanker plus hose run |
| **C** | No legal standing point within 30 m, **or** path <1.2 m, **or** no external access port | 1 m³ portable unit, and/or floor works |

### Risk rule (provisional — must be calibrated)

```
risk = (years since last desludging × 1.0)
     + ((household size − 4) × 0.5)
     + condition penalty   [no cemented bottom +2, cracked or unsealed +1, outlet surcharge observed +3]
```

Schedule at `risk ≥ 5`. **Calibration requirement:** measure actual sludge depth and scum thickness on the first 30 tanks in each tier using a sludge judge at the access port. If the rule misclassifies more than 20% of the sample, revise the weights and re-freeze before scheduling begins. The provisional weights are a planning device, not a validated model.

### Records

F1 per tank; F2 per access assessment; a register export in CSV with a published data dictionary.

### Acceptance

100% of the footprint entered; every Tier C assignment confirmed by EN; every active entry has a consent record; register reproducible from raw forms by an independent auditor.

### Failure response

| Failure | Response |
|---|---|
| Household declines | Record as declined; no coercion, no exclusion from other services |
| Tank cannot be located | Record `U`; refer to BR; do not open |
| Boundary disputed | Stop the block; escalate to IO and BR |
| Register and field count diverge >10% | Re-walk before scheduling |

---

## P2 — Scheduled Desludging Service

**Purpose.** Empty tanks on a published schedule using equipment matched to the access tier, without spill, without coercion, and without damaging the tank.

**Owner.** SV. SO holds stop-work authority.

**Trigger.** F3 schedule card issued at least 48 hours before the visit.

### Preconditions

- Consent on file (P5)
- Tier assigned (P1)
- Receiving facility confirmed available for the delivery window (P3)
- Crew trained and equipped (P5)

### Procedure

1. **Notify** through BR channels 48 hours ahead. No public naming of households. No shaming.
2. **Confirm access works.** Floor breaking or access-port installation happens only with written consent, by a competent worker, with reinstatement included in the same visit.
3. **Set containment** before opening: drip tray under the connection, spill kit staged, absorbent at the tank mouth.
4. **Open only a consented, ventilated tank.** No entry. No confined-space work at any point. Headspace hydrogen sulfide in septic tanks is documented at 0–500 ppmv, which is far beyond any personal exposure limit.
5. **Pump out.** Record start and end volume in m³. Do not over-pump: retain a seed layer per the receiving operator's specification unless the tank is being decommissioned.
6. **Inspect and photograph** the tank interior through the port only — no entry — for cracks, root intrusion and outlet condition. Coded images only.
7. **Reinstate** the floor or cover, clean the work area, and confirm with the household representative.
8. **Issue the next-due date** on the spot, and record it in the register.
9. **Reconcile volume** against F5 manifest before leaving the block.

### Tier execution

| Tier | Execution | Constraint |
|---|---|---|
| A | 10 m³ tanker direct | Standard |
| B | 10 m³ tanker plus hose run | Practical suction reach ≈30 m; beyond that, reclassify to C |
| C | 1 m³ portable unit to a 10 m³ mother tanker | Never manual bucketing as a design method |

**Manual handling of septage is prohibited as a planned method.** It forfeits manifest traceability and creates unacceptable exposure. If Tier C cannot be served with the portable unit, the household is deferred with a reason code, not served unsafely.

### Records

F3 schedule card; F4 service record per household (tank ID, date, volume m³, tier, crew lead, consent confirmation, reinstatement, next due, reason code); photographs coded; volume ledger.

### Acceptance

≥95% of scheduled households served within the agreed window; 100% of served households have an F4 with recorded volume; zero spill events; zero unconsented access.

### Failure response

| Failure | Response |
|---|---|
| Sealed or missing cover | Defer with code `ACC`; offer access works under consent |
| Tank structurally unsafe | Stop; refer to EN; do not pump |
| Truck cannot reach | Reclassify tier and reschedule with portable unit |
| Spill occurs | Stop pumping; contain; report under P5 within 1 hour; remediate before leaving |
| Household withdraws consent | Stop immediately; record; no follow-up pressure |

---

## P3 — Chain of Custody and Disposal Verification

**Purpose.** Prove that every cubic metre pumped actually reaches a permitted treatment facility. Without this, the pilot is indistinguishable from the illegal dumping documented in Metro Manila, where a siphoning truck was filmed discharging septage into a Malate canal draining to Manila Bay.

**Owner.** SV for generation; IO for reconciliation. EL audits independently.

**Trigger.** Every collection.

### Procedure

1. **Pre-number manifests.** F5 issued in triplicate: hauler, household block, receiving facility. Digital equivalent permitted; no custom app required.
2. **Record at loading:** manifest ID, tank ID, date and time, volume m³, vehicle plate, crew lead.
3. **Weigh or gauge at delivery.** Record gross and net. Volume-only is acceptable where a weighbridge is unavailable, but the method must be stated.
4. **Obtain F6 receiving receipt** with facility name, permit reference, date, time and accepted volume.
5. **Reconcile within 24 hours.** Expected volume is 1.58 m³ per tank (Maynilad's 2019 figure: 233,000 m³ across 147,900 tanks). Tolerance ±15%. Breach triggers an audit.
6. **Verify the facility permit** annually and re-check before commissioning. A facility operating outside its permit invalidates the whole chain.
7. **Log rejected loads** with reason and disposition.
8. **Publish monthly totals** by barangay.

### Records

F5 manifest (triplicate or digital twin); F6 receipt; monthly reconciliation sheet; permit verification note.

### Acceptance

100% of transferred volume carries a matched manifest and receipt; reconciliation within tolerance every month; zero unaccounted transfers.

### Failure response

| Failure | Response |
|---|---|
| No receipt for a load | Suspend hauling until accounted for; treat as unverified, not as delivered |
| Facility rejects load | Hold in a lawful containment arrangement; do not discharge; escalate to IO same day |
| Volume discrepancy >15% | Audit the route; check for unrecorded transfers |
| Facility permit lapses | Immediately reroute to a permitted facility or suspend service |

---

## P4 — Overflow and Bypass Alarm Response

**Purpose.** Detect the event that actually discharges raw sewage — an overflowing or bypassing tank — and convert it into a documented action within a fixed clock.

**Owner.** SR for the device fleet; SV for dispatch; BR for household contact.

**Trigger.** Alarm received.

### What this device is, and is not

| Is | Is not |
|---|---|
| A float-type high-level alarm at the tank outlet chamber | A sludge-level sensor |
| A bypass and surcharge detector | A desludging trigger |
| A cheap, fail-safe indicator (USD 50–250 class) | A measurement instrument |

**Rationale, stated for the record:** a septic tank's liquid level is fixed by its outlet invert and remains constant while sludge accumulates at 25–77 litres per person per year. Ultrasonic and pressure devices therefore measure the wrong variable. The Sanergy/SweetSense pilot in Nairobi abandoned pressure transducers for this reason. Sludge blanket instruments that do work are lowered probes costing USD 1,000–15,000. The alarm is the only sensor role this pilot claims.

### Procedure

1. **Receive and acknowledge** within 4 hours.
2. **Triage by rule:**

| Signal | Interpretation | Action |
|---|---|---|
| High level, dry weather, no rain in 24 h | Probable full tank or blockage | Site visit within 24 h |
| High level coincident with rainfall or high tide | Possible hydraulic surge | Verify; downgrade if confirmed |
| Repeated alarm at one node, >3 per day | Probable sensor fault or fouling | Maintenance, not dispatch |
| Outlet chamber surcharge | Probable bypass or illegal connection | Site visit within 24 h; refer to IO |

3. **Visit and verify** physically before despatching a truck.
4. **Assign a disposition code:** `FA` false alarm, `FL` genuine full, `BY` bypass, `BL` blockage, `SF` sensor fault.
5. **Resolve** within 72 hours, or open a tracked exception with a reason.
6. **Maintain** the fleet: monthly functional test, quarterly clean of the float chamber, annual battery and seal replacement, corrosion inspection each quarter given the sulfide-rich headspace.
7. **Publish** the false-alarm rate monthly. A device that cries wolf is a liability, not a feature.

### Records

F7 alarm disposition log: node ID, timestamp, signal type, acknowledgement time, visit time, disposition code, resolution time, photographic evidence where relevant.

### Acceptance

100% of alarms acknowledged within 4 hours and dispositioned within 72 hours; false-alarm rate published; zero unresolved alarms at month end.

### Failure response

| Failure | Response |
|---|---|
| Node offline >7 days | Physical inspection; replace or remove the node — a dead node must not sit in the register as if live |
| False-alarm rate >30% | Suspend dispatch from that node; recalibrate or remove |
| Bypass confirmed | Refer to IO and the LGU immediately; document; do not remediate illegally |
| Alarm ignored past clock | Escalate to IO; record as a service failure, not a data gap |

---

## P5 — Safety, Community and Consent

**Purpose.** Protect workers, households and students; make consent real; keep the records lawful.

**Owner.** SO. BR co-owns community conduct.

**Trigger.** Continuous from G1 onward.

### Worker protection

1. **Crews are trained adults under a named employment framework.** RA 11058 expressly excludes the public sector, so the correct framework must be determined and written down — do not assume the Act covers LGU staff or volunteers.
2. **PPE, free to the worker:** gloves, boots, splash goggles, coveralls, and respiratory protection appropriate to sulfide exposure. Replacement on failure.
3. **No confined-space entry, ever.** No entry into a tank, chamber or pit for any reason.
4. **No students or volunteers on trucks, at tanks, or handling septage.** This is project policy. It is *not* a legal citation: no Philippine occupational safety statute reaches volunteers, and the sanitation law requires only provider training. Say so honestly.
5. **Hygiene:** washing facilities at the depot, handwashing before breaks, no eating in the work area.
6. **Vaccination** offered and documented where locally advised.
7. **Stop-work authority** held by SO and by any crew member. Unsafe handling, a spill in progress, or an unstable tank stops the task without penalty.
8. **Incident reporting** within one hour, with a corrective action and a closure date.

### Consent and data

9. **Written consent** for: register entry, desludging, floor works, and photography. Separate ticks, not one blanket box. Withdrawable at any time.
10. **Minimum data.** Coded IDs in the working register; household size as a count only; no health data; no identifiable images; no household-level maps published.
11. **Lawful basis.** A service registry is not research, so the Data Privacy Act's research exclusion does not apply. Record the actual basis — consent or legal obligation — and issue a short privacy notice.
12. **No public naming, no shaming, no photographs of residents.**

### Community

13. **Grievance channel** through BR, acknowledged within 7 days, logged, with a closure note.
14. **No displacement, no eviction, no construction inside the three-metre easement** under Article 51 of the Water Code.

### Records

F8 incident report; F9 consent record; grievance log; PPE issue log; training register.

### Acceptance

Zero serious preventable injuries; 100% of active households have a consent record with separate ticks; zero confined-space entries; 100% of grievances acknowledged within 7 days.

### Failure response

| Failure | Response |
|---|---|
| Confined-space entry proposed | Refuse; escalate to IO; the task is redesigned or abandoned |
| Student or volunteer handling septage | Stop immediately; remove from task |
| Consent ambiguity | Treat as absent consent; stop service |
| Serious incident | Suspend the affected route; external review before resumption |

---

## P6 — Measurement and Evaluation

**Purpose.** Freeze what will be measured, before anything is measured, so that a disappointing result cannot be relabelled as success.

**Owner.** EL, independent of day-to-day collection.

**Trigger.** Signed and dated before the first intervention month.

### Primary outcomes

| Measure | Definition | Target |
|---|---|---|
| **Service delivery** | Households desludged within their scheduled window ÷ households scheduled | ≥95% |
| **Access-tier success** | Tier C households served with the portable unit ÷ Tier C households scheduled | ≥90% |
| **Traceability** | Volume with matched manifest and receipt ÷ total volume transferred | 100% |
| **Environmental** | Fecal coliform and BOD₅ concentration at a fixed outfall station, reported with a 95% interval | Report change; no target claimed in advance |

### Secondary outcomes

Alarm disposition rate; false-alarm rate; register completeness; grievance closure; cost per household served; spill events; reason-code distribution.

### Sampling

- **Water chemistry:** monthly at five fixed stations — one upstream boundary, two within the reach, one at the Pasig confluence, one comparison station outside the reach if permitted. Report dissolved oxygen, temperature, pH, conductivity and turbidity in the field; BOD₅, TSS and a fecal indicator by a recognized laboratory. Confirm method recognition, preservation and holding times **before** the first sample.
- **Floating litter:** twice weekly bank observation at fixed stations, as a secondary physical indicator. Retain it — solid waste still matters hydraulically even though it is not the oxygen problem.

### Analysis rules

1. **Concentrations, not loads.** Without measured discharge, a load calculation is fabrication.
2. **One reach is one site.** Many repeated observations are not many independent sites. Do not call this a replicated experiment.
3. **Confounders are reported, not adjusted away.** Kalinisan sa Bagong Pilipinas, Bayanihan sa Estero, the city's weekly barangay cleanups, rainfall, tides and upstream works will all move these numbers.
4. **Decision rule, fixed in advance.** For any target `T`:
   - *Supported* if the 95% interval lower bound ≥ `T`
   - *Evidence against* if the upper bound < `T`
   - *Inconclusive* otherwise
5. **A result below target is not "no effect."** Report it as measured.
6. **No outcome substitution.** The registered outcome cannot be swapped after the first results.

### Records

F10 observation record; laboratory reports with chain-of-custody forms; frozen protocol with a signature block; a dated pre-registration note filed with IO before month 3.

### Acceptance

Signed and dated protocol on file before intervention; raw records available to an independent auditor; every deviation logged with a reason.

### Failure response

| Failure | Response |
|---|---|
| Laboratory cannot meet method or holding time | Recost and re-plan before sampling; never relabel an unrecognized test as compliant |
| Baseline variance makes the target undetectable | Say so prospectively, in the paper, before the intervention |
| Confounder dominates | Report it; downgrade inference; do not delete the observation |
| Protocol amended after intervention | Publish the amendment and its date; the pre-registered version stays on file |

---

## 7. Gate checklist

| Gate | Question | Evidence | Status |
|---|---|---|---|
| **G0** | May this work inform an entry at all? | Written organizer ruling | **Open** |
| **G1** | Is there a verified, contiguous, accessible 1-km reach? | Centreline map, chainage, endpoints, ownership | **Open** |
| **G2** | Does the service actually fit its constraints? | Register, tier counts, receiving capacity, truck access | **Open** |
| **G3** | Do cost and permission hold? | Quotations, facility permit, employment framework | **Open** |
| **G4** | Is the baseline real and the protocol frozen? | F10 records, P6 signature | **Open** |
| **G5** | Does the chain work end to end? | Dry-run manifest with matched receipt | **Open** |
| **G6** | Who runs it in month 13? | Named budget holder and operator, or a closure plan | **Open** |

---

## 8. What this pack deliberately does not contain

No sludge sensor. No in-channel structure. No drain closure. No treatment plant. No custom application. No AI model. No household personal data in the working register. No claim that collecting waste or septage restores a river.

Those exclusions are the design, not omissions from it.
