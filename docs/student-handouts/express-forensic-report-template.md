# Express Forensic Report Template
**Classification:** RESTRICTED (Training) | **Case Reference:** [CASE-ID]
**Exercise:** Activity 2.0.3 – Express Forensic Report
**Analyst:** [Name] | **Role:** [Role] | **Date (UTC):** [YYYY-MM-DD]
**Submission deadline:** 30 minutes from evidence delivery

---

## Section 1 – Case Summary

| Field | Value |
|---|---|
| Incident ID | |
| Affected Host(s) | |
| Date/Time of First Event (UTC) | |
| Date/Time of Detection (UTC) | |
| Detection Gap | |
| Incident Type | Ransomware / Data Theft / Malware / Other |
| Overall Severity | Critical / High / Medium / Low |

---

## Section 2 – Attack Timeline

Reconstruct the sequence of events chronologically. Use the evidence files provided in `/opt/ngsoc-artifacts/forensic-bundle/`.

| # | Time (UTC) | Event | Evidence Source | MITRE ATT&CK |
|---|---|---|---|---|
| 1 | | Initial phishing email delivered | wazuh-alerts-ex2.json | T1566.001 |
| 2 | | | | |
| 3 | | | | |
| 4 | | | | |
| 5 | | | | |
| 6 | | Ransomware deployed | | T1486 |

**Detection gap** (time between first malicious event and SOC alert):
[Calculate: first event time → SIEM alert time]

---

## Section 3 – Evidence Analysis

### 3.1 Indicators of Compromise

| IoC Type | Value | Confidence | Source | Recommended Action |
|---|---|---|---|---|
| IP | | High / Med / Low | | Block / Monitor / Hunt |
| Domain | | | | |
| File hash (MD5) | | | | |
| File hash (SHA256) | | | | |
| Process name | | | | |
| File path | | | | |

### 3.2 Key Evidence Items

**Wazuh Alerts** (from `wazuh-alerts-ex2.json`):
- Most significant alert: [rule ID, description, time]
- Number of alerts: [count]
- Affected hosts: [list]

**Process List** (from `endpoint-process-list.txt`):
- Suspicious process(es): [name, PID, parent PID]
- Persistence mechanism: [cron entry or other]

**Network Connections** (from `netstat-employee-ws.txt`):
- C2 connection: [src → dst, protocol]
- Lateral movement evidence: [connection to other hosts]

**Web Application Log** (from `web-banking-access.log`):
- SQLi attempt: [timestamp, IP, payload]
- Unauthorised export: [timestamp, query parameter]

**File System** (from `file-metadata.txt`):
- Files encrypted: [count] in [time window]
- Ransom note: [path, timestamp]

---

## Section 4 – Root Cause Analysis

**Primary attack vector:**
[How did the attacker gain initial access?]

**Enabling vulnerabilities:**
1. [Technical vulnerability – e.g. SQLi in login.php]
2. [Process gap – e.g. email macro not blocked]
3. [Configuration weakness – e.g. credential reuse]

**Why was detection delayed?**
[Explain the 12-hour detection gap using evidence]

---

## Section 5 – Impact Assessment

| Category | Assessment |
|---|---|
| Data confidentiality | [Was data accessed/exfiltrated? What type?] |
| Data integrity | [Were files modified/encrypted?] |
| Availability | [Which services were disrupted?] |
| Regulatory exposure | [GDPR? NIS2 notification required?] |
| Estimated business impact | [Qualitative: Low / Medium / High / Critical] |

---

## Section 6 – Recommendations

List in priority order (P1 = immediate, P3 = medium-term):

| Priority | Action | Owner | Deadline |
|---|---|---|---|
| P1 | Isolate affected hosts from network | SOC | Immediate |
| P1 | | | |
| P2 | | | |
| P3 | | | |

---

## Section 7 – Analyst Statement

I confirm that:
- [ ] All evidence items were handled in accordance with chain-of-custody procedures
- [ ] No evidence was modified during analysis
- [ ] Hashes were verified before and after acquisition where applicable
- [ ] This report represents my honest professional assessment

**Analyst signature:** ________________ **Date:** ________________

---
*Template: NG-SOC LM8 Sub Case 1a | Assessed Activity 2.0.3*
*All evidence files in this exercise are synthetic training artefacts.*
