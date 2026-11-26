# Master Schedule — RF2027 Case Study Competition, Phase I

**Team:** Aaron Y. Hernandez · Ellaine T. Jacob · Jolex Alexier S. Cruz
**Window:** Saturday 14 November → Saturday 5 December 2026 (22 days)
**Hard internal date:** every document and letter finished **Tuesday 17 November**
**Hard external date:** **5 December 2026**, 11:59 PM PHT

| File | What it is | When to use it |
|---|---|---|
| [`gantt.html`](gantt.html) | Visual Gantt, 42 tasks, colour by owner | Open in a browser. Print to A3 landscape for a wall copy |
| [`GANTT_MASTER.csv`](GANTT_MASTER.csv) | The same 42 tasks as data | Import to Notion, Sheets, or Excel |
| [`notion_setup.py`](notion_setup.py) | Builds the database + timeline view in your own Notion | Needs a token you create (5 min, instructions in the file header) |

This document is the narrative version: what happens on which day, who is carrying what, and where the plan can break.

---

## 1. The shape of the three weeks

Three phases, and they do not overlap much. Week one is paperwork. Week two is evidence and drafting. Week three is review, production, submission.

```
14–17 Nov   ████████████  Compliance & correspondence   (13 tasks, all 3 people)
18–24 Nov   ██████████    Evidence closure              (6 tasks, Aaron + Ellaine)
20–26 Nov   ████████████  Writing                       (7 tasks, all 3)
21–30 Nov   ████████      Poster                        (4 tasks, Jolex)
27–01 Dec   ██████        Review                        (5 tasks)
01–03 Dec   ████          Production                    (4 tasks)
04–05 Dec   ██            Submission                    (3 tasks)
```

### Phase 0 — Compliance and correspondence (14–17 Nov)

Thirteen tasks, all landing on the same Tuesday. This is the single worst crunch in the schedule: five concurrent tasks per person for four straight days, including a weekend.

| # | Task | Owner |
|---|---|---|
| T01 | Registration form + ₱1,500 team fee | Jolex |
| T02 | Proof of Enrollment ×3 students | Jolex |
| T03 | Adviser's Conforme signed | Aaron |
| T04 | Organizer clarification: AI use, rubric, eligibility | Aaron |
| T05 | Principal endorsement letter | Jolex |
| T06 | Parental consent + DepEd Order 66 Annex C | Jolex |
| T07 | DepEd Advisory 184, s. 2026 attached | Jolex |
| T08 | Barangay letters ×3 (Barangays 671–687) | Ellaine |
| T09 | Manila City Health Department letter | Ellaine |
| T10 | Manila CENRO / Department of Public Services letter | Ellaine |
| T11 | DENR-EMB NCR FOI request | Ellaine |
| T12 | Maynilad data request letter | Ellaine |
| T13 | Eligibility check: Grade 7–12 confirmation (18 Nov) | Aaron |

**What must be true on Tuesday night:** the fee is paid and receipted, three sealed letters are out the door, and T04 has been sent. Everything else in the schedule is downstream of those three facts.

Two of these are not paperwork — they are decisions:

- **T01 is money leaving your pocket.** Do not pay before T04 and T13 come back. If the team is ineligible, the ₱1,500 is the cheapest thing you will lose.
- **T04 is the whole entry.** If the organizers say AI-assisted work is disallowed, the paper as drafted cannot be submitted. Ask before you spend three weeks on it.

### Phase 1 — Evidence closure (18–24 Nov)

| # | Task | Owner | Ends |
|---|---|---|---|
| T14 | G1 site verification walk + 1-km centreline | Aaron | 21 Nov |
| T18 | Reference verification of 24 claims | Aaron | 21 Nov |
| T19 | Legal routing: permits + employment framework | Aaron | 22 Nov |
| T17 | Receiving facility capacity + gate fee | Ellaine | 22 Nov |
| T15 | Access-tier pilot survey (20–30 tanks, exterior only) | Ellaine | 24 Nov |
| T16 | Quotations: lab, hauling, vacuum unit, gate fee | Ellaine | 24 Nov |

**T14 is gate G1.** Until someone walks the reach and fixes chainage 0+000 to 1+000, every site-specific number in the paper is provisional. This is the task that has been outstanding longest.

**T15 does not open tanks.** Exterior observation only: path width, distance to a truck-parkable road, whether the tank sits under the house. Anything involving the inside of a tank needs consent, PPE and a sanitary inspector present, and that is not scheduled before 5 December.

### Phase 2 — Writing (20–26 Nov)

| # | Section | Owner | Words | Dates |
|---|---|---|---|---|
| T20 | §1–2 Background + Diagnosis | Aaron | ~600 | 20–23 Nov |
| T21 | §3–4 Barrier + Design | Aaron | ~550 | 22–25 Nov |
| T22 | §5–7 Plan + Budget + Economics | Ellaine | ~500 | 22–25 Nov |
| T23 | §8–9 KPIs + Scaling blueprint | Jolex | ~350 | 23–26 Nov |
| T24 | §10–11 Implications + Limitations | Aaron | ~250 | 25–26 Nov |
| T25 | References, APA 7 | Aaron | — | 25–26 Nov |
| T26 | Word count reconciliation, ≤2,200 | Jolex | — | 26 Nov |

The section budgets total **2,250 words against a 2,200 cap.** T26 is a single day with no buffer, and it is the day it has to come down. Cut from §1 Background first — the reach history in that section is the most compressible prose in the paper. Draft v0.2 already exists at 2,058 words, so the real job is not writing from zero; it is splitting the existing text across four owners, each of whom rewrites their own sections against the verification annex.

Do not let four people edit one document simultaneously. Work in separate section files and merge in T26.

### Phase 3 — Poster (21–30 Nov)

Jolex owns all four tasks. Outline (T27) runs 21–23 Nov, build (T28) 24–27, sync to the paper (T29) 27–29, export (T30) 30 Nov.

The sync step exists because posters drift. Every number on the poster must match the manuscript after T26 — including the corrected Class C value of **200** MPN/100 mL, not 400.

### Phase 4 — Review (27 Nov – 1 Dec)

| # | Task | Owner | Dates |
|---|---|---|---|
| T31 | Technical review of paper | Aaron | 27–28 Nov |
| T32 | Legal and budget review | Ellaine | 27–28 Nov |
| T33 | Source and originality review | Aaron | 28–29 Nov |
| T34 | Adviser review and sign-off | All | 29–30 Nov |
| T35 | Revisions round | All | 30 Nov – 1 Dec |

Aaron currently owns both T31 and T33 — he reviews his own writing, then reviews his own sources. That is a weak check. **Give T33 to Ellaine** and let her verify that every in-text citation resolves to the annex.

### Phase 5 — Production (1–3 Dec)

Formatting (T36, Jolex), AI declaration (T37, Aaron), rendered-artifact inspection (T38, all), content freeze (T39, all, 3 Dec).

T38 means opening the actual PDF and the actual PNG on two different devices. Layout breaks happen in export, not in the editor. This is also the only task that reads the file the way a judge will.

**T39 is a freeze, not a deadline.** Nothing is edited after 3 December. If something is wrong on 4 December, the choice is submit a flawed paper or submit nothing; the freeze is there so you never have to make it.

### Phase 6 — Submission (4–5 Dec)

Submit to `rf.ysc@upalchemes.org` on **Friday 4 December before 6 PM**, confirm receipt the same day, and hold 5 December as buffer only.

---

## 2. Who is carrying what

| | Aaron | Ellaine | Jolex |
|---|---:|---:|---:|
| Tasks | 13 | 10 | 14 |
| Word responsibility | ~1,400 of 2,200 | ~500 | ~350 |
| Busiest days | 18–21 Nov (4 concurrent) | 14–17 Nov (5 concurrent) | 14–17 Nov (5 concurrent) |
| Idle window | 30 Nov – 2 Dec | 26 Nov – 28 Nov, 30 Nov – 3 Dec | 18–20 Nov |
| Single point of failure | Yes | No | No |

**Aaron is on the critical path and owns both gates.** T04 decides whether the paper may exist; T14 decides whether it can say anything site-specific. He also writes 64% of the words. If one person's week collapses, it will be his, and it will take the entry with it. The mitigation is not more work from him — it is moving T33 and part of §1 to other people.

**Ellaine's work is almost entirely waiting.** Five letters out on 17 November, then four tasks that depend on other people answering. Her risk is silence, not overload. Each letter needs a named recipient, a reference number where one exists, and a follow-up date in her own calendar — 24 November for anything unanswered.

**Jolex carries the most tasks and the least thinking per task.** Fourteen items, most of them mechanical: forms, scans, formatting, export. He is the only person free on 18–20 November, which makes him the natural place to absorb anything that slips out of the 14–17 crunch.

---

## 3. The critical path

```
T04 (organizer ruling) ──────────────────────────────► T37 (AI declaration)
T08/T09 (letters sent, 17 Nov)
   └─► T14 (site walk, 18–21 Nov) ─► T20 (20–23) ─► T21 (22–25) ─► T24 (25–26)
        └─► T31 (27–28) ─► T34 (29–30) ─► T35 (30–1) ─► T36 (1–2) ─► T39 (3) ─► T40 (4)
```

**Float: about one day.** From 19 November onward, a single lost day pushes the submission onto 5 December itself. The only genuine slack in the plan is 4–5 December, and that is the buffer you are trying to keep.

Two places to buy float if you need it:

1. **Compress writing.** §1–2 and §3–4 could each lose a day by drafting from the existing v0.2 text rather than starting over. That returns 2 days.
2. **Start the poster earlier.** Jolex is idle 18–20 November. Moving T27 forward gives T29 more room, and T29 is where poster–paper mismatches get caught.

---

## 4. Four things that can break this plan

**① The 5 December date may not be the paper deadline.**
The RF2027 site describes 5 December as the **registration and payment** deadline, with the case solution due about four weeks later, after a workshop. The competition kit describes Phase I deliverables as due 5 December. This schedule assumes the earlier, stricter reading. That costs you nothing if the site is right, and saves you if the kit is. **Confirm which in T04**, because if the paper is actually due in January, you have bought yourself a month and should spend it on the site survey rather than the poster.

**② Eligibility may exclude one of you.**
The Case Study Competition has historically been open to Grade 7–12 students only. If any member is in college, the team may be disqualified at screening, after the fee is paid. T13 exists for this. Its 18 November end date is the day the **written reply is logged**, not the day the question is asked — send it inside the T04 email on 17 November, because it is the same email asked twice. What matters is that the reply exists before T01 is paid.

**③ The quotation tasks probably will not produce quotations.**
T16 and T17 assume written quotes by 24 November. T12 (Maynilad) was only sent on 17 November, and a concessionaire data request typically takes three to six weeks. You will likely have nothing back by 24 November, and T22 — the budget section, the most closely checked part of the paper — is drafted on top of that gap.

The fix is not to wait. It is to draft the budget from **published benchmarks and label them as such**: ₱4,700 per truck desludging (Maynilad, July 2025), ₱580 per m³ gate fee (Ormoc City ordinance), ₱755/day NCR minimum wage (NCR-28, 26 September 2026). The annex already marks the four lines with no Philippine benchmark — access remediation, the small vacuum unit, the register system, the gate fee — as assumptions. If a quote arrives before 26 November, substitute it; if not, the paper is still defensible because it says what it does not know.

**④ The adviser sign-off is scheduled on a Sunday.**
T34 runs Sunday 29 to Monday 30 November. Advisers do not work Sundays, and more importantly, your adviser cannot review a draft that internal review is still rewriting on 29 November. Add one step and the problem disappears: **deliver the draft to the adviser on Friday 27 November** as a review copy, take comments Monday 30 November, and keep T34 as the formal sign-off meeting. That gives the adviser a weekend and gives you a real revision day.

---

## 5. What is deliberately not scheduled

- **The pilot itself.** Nothing in this schedule desludges a tank, installs an alarm, or takes a water sample. Phase I is a written case solution and a poster. The twelve-month pilot is what the paper *proposes*; executing it is not a competition deliverable, and pretending otherwise would put minors in contact with septage for no scoring benefit.
- **Laboratory analysis and river sampling.** Expensive, slow, and not required before 5 December.
- **JTAs, data-sharing agreements, ethics board submissions.** All of these matter for execution in 2027. None of them gate a Phase I entry.
- **Anything after 5 December.** If the paper deadline really is in January, this schedule ends early by design. Re-plan then, not now.

---

## 6. Definition of done

| Phase | Done means |
|---|---|
| 0 | Fee paid, three letters sent, T04 answered in writing |
| 1 | 1-km centreline mapped with chainage, 24 claims verified in writing, four cost lines sourced or explicitly labelled assumptions |
| 2 | One merged manuscript under 2,200 words with every claim traceable to the annex |
| 3 | Poster exported, every number identical to the manuscript |
| 4 | Adviser has signed; three review memos exist as files, not as conversations |
| 5 | PDF and PNG opened on two devices and inspected; nothing edited after 3 Dec |
| 6 | Email sent before 6 PM on 4 Dec, receipt confirmed the same day |

---

*Generated 14 November 2026. Sources for every figure in this schedule are in [`../docs/verification/2026-11-13-source-verification-annex.md`](../docs/verification/2026-11-13-source-verification-annex.md). The competition rules quoted here come from the RF2027 kit held outside this folder; verify them against the site before paying.*
