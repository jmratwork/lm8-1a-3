# Exercise 3 – CTI Analyst: Student Handout
**Role:** Cyber Threat Intelligence Analyst | **Duration:** ~45 minutes
**Platform:** MISP at https://10.10.40.30 (admin / NGSOCAdmin2025!)

---

## Scenario

The FS-ISAC has issued an advisory about the **Black Falcon** banking malware campaign. Your MISP has been pre-loaded with Event #1001. The C2 IP from this event (10.10.20.20) matches the alert from Exercise 1. This means your organisation may be an active target.

Your task: produce a **Threat Intelligence Brief** for internal distribution.

---

## MISP Quick Start

1. Go to https://10.10.40.30
2. Log in: admin / NGSOCAdmin2025!
3. Navigate to Event List → Event #1001 (Black Falcon – Banking Trojan Campaign)
4. Review all attributes (IoCs) in the event
5. Export: Event #1001 → Download → CSV

---

## Tasks

### Task 1 – IoC Analysis
For each IoC in MISP Event #1001, complete the table:

| IoC Type | Value | Reliability | Defensive Action |
|---|---|---|---|
| IP | 10.10.20.20 | High (live traffic confirmed) | Block at firewall |
| Domain | update-svc.blackfalcon-sim.internal | | |
| MD5 hash | aabbccdd... | | |
| SHA256 hash | deadbeef... | | |
| Email subject | Q4 Wire Transfer... | | |
| Filename | Q4-wire-transfer-auth.docm | | |

### Task 2 – Risk Assessment
- Which 3 assets are most at risk?
- Identify 2 defensive gaps in your current controls
- State likelihood and impact (High / Medium / Low each)

### Task 3 – Team Recommendations
Write one specific recommendation for each team:
- SOC: [threat hunting task]
- IR: [preparation step]
- IT/Infrastructure: [preventive control]

### Task 4 – Dissemination Plan
- What TLP marking is appropriate for each audience?
- Should these IoCs be shared externally (FS-ISAC / national CERT)?

---

## TLP Reference

| Marking | Who Can Share |
|---|---|
| TLP:RED | Named recipients only |
| TLP:AMBER | Your organisation and trusted partners |
| TLP:GREEN | Community (sector peers) |
| TLP:WHITE | Public |

---

## Deliverable

Submit: completed IoC table, risk assessment, team recommendations, dissemination plan. Upload as a note to MISP Event #1001 or submit via REP.

---

*NG-SOC LM8 Sub Case 1a | Exercise 3 | British English*
