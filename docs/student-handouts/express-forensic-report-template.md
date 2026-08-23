# Express Forensic Report Template

**Classification:** RESTRICTED (Training) | **Reference:** [EFR-001]
**Analyst:** [Name / Role] | **Date/Time (UTC):** [YYYY-MM-DDTHH:MM:SSZ]
**Case:** NG-SOC LM8 – Black Falcon Campaign (Activity 2.0.3)
**Submission window:** 30 minutes from artefact release

> **Mirror, not source.** The authoritative copy of this template is deployed to
> `~/reports/express-forensic-report.md` on `analyst-host` by the
> `forensics-host` role. Edit it there; this file exists so instructors can read
> the structure without deploying the range.
>
> The seven headings below are fixed by **D5.8 Section 2.0.3** and must not be
> renamed or reordered — the assessment checklist maps to them one-to-one.

---

## 1. Scope and Assumptions

**Systems examined:**
- [ ] employee-ws (10.10.30.10)
- [ ] file-server (10.10.30.20)
- [ ] db-server (10.10.30.30)
- [ ] web-banking (10.10.20.10)

**Time window:** [start UTC] – [end UTC]

**Assumptions and limitations:**
[Document what you could NOT examine and why – missing logs, live system vs image, etc.]

**Confidence in findings:** HIGH / MEDIUM / LOW — [justify]

---

## 2. Artefacts Reviewed

| # | Artefact | Source | Hash (SHA256) | Integrity |
|---|---|---|---|---|
| 1 | wazuh-alerts-ex2.json | /opt/ngsoc-artifacts/forensic-bundle/ | | PASS/FAIL |
| 2 | endpoint-process-list.txt | /opt/ngsoc-artifacts/forensic-bundle/ | | PASS/FAIL |
| 3 | netstat-employee-ws.txt | /opt/ngsoc-artifacts/forensic-bundle/ | | PASS/FAIL |
| 4 | web-banking-access.log | /opt/ngsoc-artifacts/forensic-bundle/ | | PASS/FAIL |
| 5 | file-metadata.txt | /opt/ngsoc-artifacts/forensic-bundle/ | | PASS/FAIL |
| 6 | timeline-clues.txt | /opt/ngsoc-artifacts/forensic-bundle/ | | PASS/FAIL |

---

## 3. Timeline (High Level)

| Time (UTC) | Event | Evidence Source | ATT&CK |
|---|---|---|---|
| | | | |
| | | | |
| | | | |

[Fill in from timeline-clues.txt and corroborating artefacts]

---

## 4. Findings

### F-01 – [Title]
**Severity:** CRITICAL / HIGH / MEDIUM / LOW
**Host:** [hostname]
**Description:** [What happened, in plain language]
**Evidence:** [Which artefact(s) confirm this finding]
**ATT&CK Technique:** [Txxxx – Name]

### F-02 – [Title]
[Repeat structure for each finding]

> Cover, where the evidence supports it: probable initial access, persistence,
> lateral movement, and exfiltration/encryption indicators.

---

## 5. Indicators of Compromise

| Type | Value | Source | Confidence |
|---|---|---|---|
| IP | | | HIGH/MED/LOW |
| Domain | | | |
| MD5 | | | |
| SHA256 | | | |
| Filename | | | |
| File path | | | |

[Cross-check against MISP (Exercise 3) for known IoCs]

---

## 6. Impact Assessment

**Confidentiality:** [Was data exfiltrated or accessed without authorisation?]
**Integrity:** [Were files modified, encrypted or deleted?]
**Availability:** [Were systems or services disrupted?]

**Estimated affected users / records:** [number or "unknown"]
**Regulatory implications:** [GDPR, NIS2, sector-specific — any notification obligation?]

---

## 7. Recommendations

| Priority | Recommendation | Owner | Target Date |
|---|---|---|---|
| IMMEDIATE | | IT Security | |
| SHORT-TERM | | | |
| LONG-TERM | | | |

**Immediate containment actions taken during this investigation:**
1.
2.
3.

---

*Assessment criteria (D5.8 §2.0.3): evidence-based reasoning traceable to the
artefacts provided; internally consistent timeline; key indicators and affected
scope identified; recommendations actionable and prioritised; professional
structure and clarity (UK English).*
