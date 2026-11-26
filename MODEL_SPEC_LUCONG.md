# Model Spec — Economic & Mathematical Model for the Lucong Shed-Service Entry

**Purpose:** turn §5 of `docs/drafts/2026-11-19-paper-v1.0-submittable.md` from a budget table into a model that predicts an outcome, prices it, compares it against alternatives, and names the one assumption that decides the answer.

**Written:** 23 Nov 2026. **Deadline:** 5 Dec 2026, 11:59 PM PHT (12 days).

---

## 0. First, correct the framing

You cannot *empirically prove* a service works before it runs. A model cannot do that, and Dr. Aviso's session said so explicitly: *"Models turn hard questions into clear choices"* — not into proof.

What a model **can** prove, and what will read as rigorous to this judge:

> Under stated assumptions, this design delivers X% of the identified load at ₱Y per unit, and no cheaper feasible design does better. The pilot exists to measure the one assumption that carries the result.

That sentence is defensible. "Our solution is proven to work" is not, and overclaiming was named on the slide as *"a common reason for rejection."*

The strongest move available to you is the opposite of hype: **use the model to find where your own draft is wrong, then fix the draft.** Section 4 below finds one such place.

---

## 1. What §5 has now, and what is missing

| Rubric asks for | Current §5 | Gap |
|---|---|---|
| Estimated costs | Table 2, ₱10.0M | Present, but no unit-cost logic |
| Efficiency of the process | "about a third of volatile solids to gas" | Assertion, not a balance |
| Technical feasibility | Standard PH equipment, cited | Adequate |
| National scaling | Tarlac station list + Bamban zoning | Adequate |
| **Economic analysis** | ₱/shed-month at 15 and 60 sheds | **No counterfactual, no comparison, no outcome priced** |
| **Proof it works** | Target stated (16,000 → 2,000) | **No mechanism connecting service → concentration** |

The webinar's six-flaw drill maps onto this directly. Your draft currently has **"nothing to measure"** (a target with no model behind it) and **"no comparison"** (no other option scored). Those are two of the six.

---

## 2. The model, in four blocks

Each block is small enough to build, explain, and defend. Do them in order; each one feeds the next.

### Block 1 — Load balance: shed → river (the block that proves "it can work")

**Functional unit (fix this first, everything is priced per unit of it):**
> 1 kg of volatile solids diverted, or 1 × 10¹² MPN of fecal coliform prevented from reaching the reach per year.

**Source term.**

```
L_gen  = Σ_i  n_i · e_h · 365            [MPN/yr]   generated load at n sheds
L_dis  = L_gen · (1 − c)                 [MPN/yr]   load still discharged
```

- `n_i` = heads at shed i (census, to be measured)
- `e_h` = fecal coliform per head-day (literature; source and year required)
- `c` = capture rate (fraction of generated load actually collected; from manifest coverage, 0.8–0.95)

**In-stream term (steady state, well mixed, first order).**

```
C = ( L_up + L_dis ) / ( Q · 86 400 )    [MPN/m³ → ÷100 for MPN/100 mL]
```

- `Q` = dry-season discharge at Santiago Bridge (m³/s) — **measure this**
- `L_up` = upstream load entering the reach (from the station above the clusters, or by difference)

**The reduction identity (this is the whole argument in one line).**

```
ΔC / C₀ = s · c          where   s = L_local / (L_up + L_local)
```

Predicted endpoint:

```
C_end = C₀ · (1 − s · c)
```

**Why this is the right model:** it has one free parameter that matters (`s`), one you control (`c`), and one you can measure (`Q`). Everything else is bookkeeping. It also makes the failure mode explicit — you cannot remove load you do not control, no matter how good the service is.

**Data needed, cheapest form:**

| Input | How to get it before 5 Dec | Tier |
|---|---|---|
| `Q` | Float method at Santiago Bridge: tape the width, depth at 5 points, time an orange peel over 10 m, `Q = 0.85 · v · A`. One afternoon | Primary |
| `n_i` | MENRO business registry + barangay list of piggeries and head counts | Official |
| `e_h` | Published excretion/coliform loading rate per head | Published |
| `s` | Two grab samples above and below the shed cluster, same day, same tide state | Primary (proxy) |
| `C₀` | Already have: 16,000 MPN/100 mL (EMB, Oct 2024–2025 round) | Official |

If `Q` is not measured, say so and run the model at three values (0.05, 0.2, 0.5 m³/s) as a **bound**, exactly as the earlier stack note did for flushing time. Never present a single unmeasured `Q`.

### Block 2 — Process balance: does the design actually hold the load? (LCA-lite)

This is what separates "a plan" from "an engineered system." Four balances, all in kg/day.

**Volatile solids and gas.**

```
VS_in = M · dm · vs                     [kg VS/day]
G     = Y · η · VS_in                   [m³ CH₄/day]     Y ≈ 0.30–0.40 m³/kg VS destroyed
E     = G · 35.8                        [MJ/day]
LPG_eq = E / 46                         [kg LPG/day]
```

**Compost mass and carbon balance.**

```
M_compost = M_digestate_DM + M_husk
C:N       = (C_d + C_h) / (N_d + N_h)   target 25–30
```

**Land constraint (the one that quietly decides feasibility).**

```
A_land = (M_compost · N_compost · 365) / N_rate     [ha]
```

with `N_rate` ≈ 120 kg N/ha for lowland rice. If `A_land` exceeds the farmland actually available behind the levees, the compost has nowhere to go and the "nothing is discharged" claim fails. **This is the second binding constraint after budget.**

**Hydraulic sizing (check the design is not undersized).**

```
V_digester ≥ Q_slurry · HRT             HRT = 10–15 d
trips/week  = Q_slurry_weekly / V_tanker
```

Do this for 15 sheds and for 60, and plot capacity against head count. The design must be a *function* of the census, not a fixed guess.

**What this block proves:** that 450 kg manure + 5 m³ washwater/day can physically pass through 3 × 25 m³ digesters, that the gas claim is arithmetically consistent, that the compost fits on real land, and that one 2,000 L tanker can do the route. You currently assert all four. This block shows them.

### Block 3 — Cost model: price the outcome, not the equipment

```
TC     = CAPEX + Σ_t OPEX_t / (1+r)^t
OPEX   = labour(n) + fuel(trips) + maintenance + sampling + administration
```

Two unit costs, reported together (never one alone — that was "Trap 1" in the earlier sim README):

```
₱ per shed-month        = TC / (n · months)
₱ per kg VS diverted    = TC / (c · M · dm · vs · 365 · years)
```

And the headline number the judge will remember:

```
₱ per 10¹² MPN prevented  = TC / (s · c · L_total · years / 10¹²)
```

**Financing (the "who pays" question the webinar put under "No people"):**

```
break-even fee per head-month = (OPEX − compost/biogas credit) / (n_heads · 12)
```

Compare that to a plausible piggery margin per head. If the fee exceeds it, the permit condition is the only enforcement and you must say so — that is an honest, defensible finding, not a weakness.

Revenues: set compost and biogas credit to **zero** in the base case, as the draft already does. Show the credit only as upside in sensitivity.

### Block 4 — Design search and comparison (the "might even be best" block)

**4a. Enumerate, don't optimize.**

Do not build an MILP. Enumerate the feasible designs and pick the cheapest that meets the target:

```
for modules m in 2..6:
  for sheds n in 10..80:
    for frequency f in {1, 2} per week:
      if capacity_ok and budget ≤ 10M and land_ok and months = 12:
        record (m, n, f, cost, load_removed, ₱/unit)
```

Present it as: *"We enumerated all designs that fit the budget and capacity limits; the chosen one is the least-cost feasible design."* That is an optimization result a Grade 12 team can defend line by line, with no solver to explain.

Output: a **cost curve** (₱ per kg VS diverted vs sheds served) and an **efficient frontier** (cost vs % load removed). Your design should sit on the frontier. If it does not, the model just told you to change the design — that is the model working.

**4b. Score the alternatives on the same functional unit.**

| Option | Physical ceiling on `s·c` | Cost per unit | Legal | Measurable in 12 mo |
|---|---|---|---|---|
| Shed service (yours) | `c` up to 0.95, limited by `s` | compute | Permit condition exists | Yes — manifests + station |
| Household septic desludging | limited by household share | compute | Ord. 8491-style framework, different LGU | Yes |
| In-stream screen + dredge | removes floating fraction only; blockage risk | compute | Easement limits | Partly |
| Enforcement only (no service) | ~0 (rule already failed in 2017) | low | Ordinance voided | No |

The 2017 Concepcion case is your evidence that enforcement alone has a ceiling of zero. That is a *measured* failure, not an opinion — use it.

**"Best" means one of two things, and you must say which:**

- **Dominance:** cheaper *and* removes more load → no trade-off to argue.
- **Frontier:** cheapest way to hit a stated reduction → argue the reduction is the right goal.

Never claim "best" on a weighted score out of 100. A judge can reassign your weights.

**4c. Uncertainty: name the number that carries the answer.**

Triangular distributions on `s`, `c`, `n_heads`, `e_h`, `Q`; 10,000 draws; report:

- distribution of `C_end` and of ₱ per unit
- **P(C_end ≤ 2,000)** and P(C_end ≤ 8,000)
- a tornado chart, one parameter at a time

Expected result: the answer is dominated by `s` (what share of the load is yours) and the census (`n_heads`). That is exactly the "sensitivity names what the pilot must measure" logic already used well in `sim/README.md`. **Reuse that voice — it is the strongest writing in the project.**

---

## 3. The output set (what goes in the paper)

Three objects, no more:

1. **One equation block** (the four lines of Block 1).
2. **One table:** design search — 4–5 feasible designs × (modules, sheds, frequency, CAPEX, annual OPEX, ₱/kg VS, % load removed).
3. **One figure, two panels:** (left) cost vs % load removed with the four options plotted; (right) tornado of `C_end` sensitivity.

Everything else — census, routes, manifests — stays in prose.

---

## 4. The arithmetic that will change your draft

Your target is 16,000 → 2,000 MPN/100 mL. That is a **87.5% reduction of total load at the station**.

From the identity `ΔC/C₀ = s · c`:

```
s ≥ 0.875 / c
c = 0.95  →  s ≥ 0.92
c = 0.90  →  s ≥ 0.97
```

**To reach 2,000, piggeries would have to be 92–97% of the coliform load at Santiago Bridge.** Your own diagnosis says household sewerage is "close behind" the piggeries. Those two statements cannot both be true. A judge with a calculator will find this, and it is the kind of internal contradiction that ends an entry's credibility.

Three honest fixes, pick one:

1. **Retarget to what the service can deliver.** If `s = 0.5` and `c = 0.9`, the predicted endpoint is `16,000 × (1 − 0.45) = 8,800`. State 8,000 as the target, with `s` to be measured in Month 1.
2. **Make the target conditional.** "A 50% reduction at the station, conditional on sheds contributing ≥55% of the load; Month 1 measures `s` and the target is confirmed or revised before operations begin." This is the strongest version: it is falsifiable and it pre-commits.
3. **Widen the service** to include household septage — but that breaks 12 months and ₱10M. Do not do this now.

Option 2 is the one that reads as science rather than sales. It also matches the webinar's line: *"Strong manuscripts also state limits honestly."*

---

## 5. Three checkable errors in the current draft

Fix these before anything else; each takes minutes and each is catchable by a judge.

| # | Where | Problem | Fix |
|---|---|---|---|
| 1 | §3, "Plan of action" | **24 months**, four phases. The challenge caps the pilot at **12 months** (webinar slide, 2:05 PM: "12 months — a proof-of-concept pilot"). | Compress to a 12-month pilot; put long-term operation in the scaling blueprint, not the pilot |
| 2 | §5, "Overall plan" | ₱25,600/shed-month at 15 sheds and ₱6,400 at 60. `10,000,000 ÷ 15 ÷ 24 = 27,778`; `÷ 60 ÷ 24 = 6,944`. The quoted figures imply **26 months**, not 24. | Recompute, or state the 26-month basis. Also label it life-cycle (CAPEX included) so it is not read as OPEX |
| 3 | §3, Step 4 | "30 m³ biogas/day or 18 kg LPG equivalent." 30 m³ at 60% CH₄ ≈ 18 m³ CH₄ × 35.8 MJ ≈ 45 kg CH₄ ≈ **10–14 kg LPG**. | Recompute from `VS_in × Y × η`, show the two lines, state the methane fraction assumed |

A fourth, not an error but a risk: **the census.** At 15 sheds × 30 kg/day = 450 kg/day, the whole design holds together (5.45 m³/day inflow, ~14-day HRT, ~2 tanker trips/week). If the census finds commercial sheds of 100–500 heads, manure alone is 3–15 t/day and the tanker and digesters are an order of magnitude too small. **The model must be size-as-a-function-of-census, not size-fixed-then-defended.** This is the single biggest technical risk in the entry, and the mass balance is the only thing that surfaces it.

---

## 6. Twelve-day build plan (23 Nov → 5 Dec)

| Day | Task | Output |
|---|---|---|
| 1 (24 Nov) | Field: flow measurement at Santiago Bridge; three 100 m² bank quadrats; photos; note tide state | `Q` with method tag; visible-waste count |
| 1–2 | MENRO/barangay piggery list with head counts; confirm 15 sheds or correct it | census table, sourced |
| 2–3 | Block 1 in a 60-line Python script or a spreadsheet: load balance, `s`, `c`, `C_end` | predicted endpoint range |
| 3–4 | Block 2: VS, gas, compost, C:N, land area, digester sizing for 15 and 60 sheds | capacity table |
| 4–5 | Block 3: cost model; two unit costs; break-even fee | cost curve |
| 5–6 | Block 4a: enumerate designs; pick least-cost feasible | design table |
| 6–7 | Block 4b: score the four options on the same metric | frontier figure |
| 7–8 | Block 4c: Monte Carlo + tornado; identify binding parameter | sensitivity figure |
| 8–9 | Rewrite §5 (650 words) around the model; retarget per §4 | new §5 |
| 9–10 | Fix §3 to 12 months; fix the three errors; reconcile numbers across §3, §5, poster | clean draft |
| 10–11 | Poster: three numbers (₱/unit, % load removed, P(target)), one figure | poster |
| 11–12 | Full read-through: every number traceable to a source or a script; word count; format | submission |

**Cut order if time runs short:** Block 4c → Block 4b (keep a table instead of a figure) → Block 2 gas detail. **Do not cut Block 1.** It is the only block that answers "does it work."

---

## 7. Verification before you claim anything

| Check | Expected |
|---|---|
| Mass balance closes | manure in = gas + compost + water loss, within 5% |
| Units | MPN/100 mL vs MPN/L vs MPN/m³ — one conversion table, used everywhere |
| Monotonicity | `C_end` falls as `c` rises, rises as `s` rises |
| Degenerate cases | `c=0 → C_end = C₀`; `s=0.1, c=1 → C_end = 0.9·C₀` |
| Budget | design search never returns > ₱10.0M; 100% of spend in Stream 2 (≥70% satisfied) |
| Reproducibility | fixed seed; a judge can rerun and get the same numbers |
| Census sensitivity | rerun at 15, 30, 60 sheds; design must visibly change |

---

## 8. What you may and may not claim

**May claim**

- Under stated assumptions, the service reduces station fecal coliform from 16,000 to a predicted range of X–Y MPN/100 mL, with the shed share `s` identified as the binding unknown.
- The selected design is the least-cost feasible design among those enumerated inside the ₱10M / 12-month / 1-km limits.
- Cost per kg of volatile solids diverted is ₱A, and per shed-month is ₱B, both including capital.
- Enforcement alone has a demonstrated ceiling of zero in this municipality (2017 ordinance, voided).

**May not claim**

- That the river will meet the 200 MPN/100 mL standard within the pilot.
- That the model is calibrated — it is parameterised, and one parameter (`s`) is measured only as a proxy.
- Any health, fisheries, or downstream effect.
- That the result transfers to other Tarlac reaches without repeating the census.

---

## 9. On the AI declaration

The model is exactly the kind of "substantive intellectual output" the kit's declaration targets. Three rules, from the project's own earlier note:

1. **You must be able to derive every equation with the chat window closed.** If you cannot, it is not yours to submit.
2. **Keep the prompt log** and the parameter sources; disclose tools and what they touched.
3. **The organizer's ruling gates this.** The email went 19 Nov with a 28 Nov reply date. Do not build the submission's core on a model whose provenance you cannot declare. If no reply arrives, send the follow-up; silence is not permission.

The honest position, if asked: the equations are standard mass balance; the parameter values come from cited sources and your own measurements; the code was written with AI assistance and verified line by line against the checks in §7.
