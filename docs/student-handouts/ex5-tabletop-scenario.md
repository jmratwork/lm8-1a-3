# Exercise 5 – Ransomware Crisis Tabletop: Student Guide
**Role:** IR Coordinator | **Duration:** ~60 minutes
**Format:** Tabletop simulation (no hands-on technical work)

---

## Your Role

You are the **IR Coordinator** at SecureBank. You do not execute technical tasks directly — your job is to:
- Maintain situational awareness across all teams
- Make and document key decisions
- Drive the response process to the correct next step
- Handle escalation and communication
- Ensure regulatory obligations are met

---

## Exercise Structure

The instructor will deliver **6 injects** at 5–10 minute intervals. After each inject:
1. Discuss with your team what just changed
2. Make decisions (document in `~/handouts/decision-log.md`)
3. State what you are delegating to which team

---

## Starting Situation

It is 14:35 UTC, Tuesday. You have just received two simultaneous calls:
- **IT Operations**: "File server is inaccessible, all files have .locked extension"
- **CFO's office**: "Client-facing banking services are degraded"

The full scenario brief (with all 6 injects) is at:
`/opt/ngsoc-artifacts/ex5-ransomware/tabletop-scenario.txt`

---

## Templates You Will Need

| Template | Location | Used When |
|---|---|---|
| Decision Log | `~/handouts/decision-log.md` | Throughout – log every decision |
| SITREP | `~/handouts/sitrep-template.md` | After each major update |
| Handover Notes | `~/handouts/handover-notes.md` | End of exercise |

---

## Key Decisions You Must Make

For each decision, record: **Time**, **Decision**, **Rationale**, **Who decided**

1. Is this a confirmed incident or an alert requiring triage? How do you know?
2. What IR plan tier do you activate? (Major / Significant / Minor)
3. Who do you notify immediately? (Hint: CISO, IT Director, Legal, DPO)
4. Do you isolate file-server now, or wait for forensics to finish?
5. Has the NIS2 24-hour early warning clock started? When did it start?
6. Is this a GDPR personal data breach? What do you do?
7. What do you say to the journalist?

---

## Regulatory Reference Card

### NIS2 Directive (Financial Sector – Essential Entity)
| Timeline | Obligation |
|---|---|
| Within **24 hours** of awareness | Early warning to national competent authority / CSIRT |
| Within **72 hours** of awareness | Full incident notification (description, impact, measures taken) |
| Within **1 month** | Final report |

### GDPR Article 33 (Data Breach)
| Timeline | Obligation |
|---|---|
| Within **72 hours** of awareness | Notify supervisory authority (if risk to individuals) |
| Without undue delay | Notify affected individuals (if high risk) |

**Key question**: Was customer data accessed or exfiltrated? → Yes → GDPR breach notification likely required.

---

## What Makes a Good IR Coordinator

By the end of this exercise, you should be able to demonstrate:

- [ ] Confirmed the incident and activated the correct IR tier
- [ ] Maintained a clear decision log with time/rationale/owner for every decision
- [ ] Resolved the Legal vs. Operations conflict correctly (evidence → contain → restore)
- [ ] Made a reasoned call on NIS2 notification timing
- [ ] Made a reasoned call on GDPR notification
- [ ] Drafted or delegated a management-level SITREP
- [ ] Identified at least 2 root causes and 2 improvement actions

---

## Assessment Criteria (Assessed Activity 2.0.2)

This exercise contributes to the **Collaborative Response Chain** assessment.
Your team will be assessed on:
- Quality of the decision log (decisions documented with rationale)
- Regulatory decision-making (NIS2 + GDPR)
- Team coordination (evidence of cross-role collaboration)
- After-action review quality (honest root cause analysis)

---

*NG-SOC LM8 Sub Case 1a | Exercise 5 | British English edition*
*All scenario details, ransom notes, and IoCs are synthetic training artefacts.*
