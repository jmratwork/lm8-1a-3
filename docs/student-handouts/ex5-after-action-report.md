# After-Action Report Template
**Exercise:** Exercise 5 – Ransomware Crisis Tabletop | **Incident:** "Operation Black Friday"
**Classification:** TRAINING USE ONLY
**Report prepared by:** [Name] | **Role:** IR Coordinator
**Report date (UTC):** [YYYY-MM-DD] | **Review period:** [Incident start – close]

---

## 1. Executive Summary

[2–3 sentences summarising what happened, what the impact was, and the primary lesson learned.]

---

## 2. Incident Timeline (Reconstructed)

| Time (UTC) | Phase | Event | Detection / Response |
|---|---|---|---|
| 09:14 | Initial Access | Phishing email received | Not detected |
| | | | |
| | | | |
| 02:15 | Impact | Ransomware deployment | SIEM alert (not escalated) |
| 14:20 | | IT Operations escalation | — |
| 14:35 | Response | IR team activated | — |

**Detection Gap:** _______ hours (time from first malicious event to IR activation)
**Significance:** [What could have changed with 1-hour vs 12-hour detection?]

---

## 3. Root Cause Analysis

Do not assign blame to individuals. Identify systemic causes.

### Technical Root Causes

| # | Root Cause | Evidence | Phase Enabled |
|---|---|---|---|
| 1 | SQL Injection in login.php (no parameterised queries) | web-banking-access.log | Initial access |
| 2 | | | |
| 3 | | | |

### Process Root Causes

| # | Root Cause | Evidence | Phase Enabled |
|---|---|---|---|
| 1 | SIEM alert at 02:15 not escalated by night shift | wazuh-alerts-ex2.json | 12-hour delay |
| 2 | | | |

### Detection Opportunities Missed

| When | Opportunity | Why Missed |
|---|---|---|
| 09:14 | Phishing email with FAIL SPF/DKIM | Email filter not checking SPF/DKIM |
| 02:13 | First C2 beacon | Rule fired, not escalated |
| | | |

---

## 4. What Went Well

[These are just as important as root causes — record approaches that should be repeated.]

1. [Example: SIEM rules for ransomware behaviour (rule 100004) correctly identified mass file rename]
2. [Example: CTI integration — MISP match confirmed threat actor and enabled correct response escalation]
3. [Add your own from the exercise]

---

## 5. Improvement Actions (SMART)

Format: **Specific, Measurable, Achievable, Relevant, Time-bound**

### Technical Improvements

| # | Action | Owner | Deadline | Success Metric |
|---|---|---|---|---|
| T1 | Block .docm attachments from external senders at email gateway | IT Operations | Within 5 business days | Email filter policy updated; tested with sample |
| T2 | Deploy parameterised queries in login.php; code review of all PHP files | Development | Within 2 weeks | DAST scan shows no SQLi findings |
| T3 | | | | |

### Process Improvements

| # | Action | Owner | Deadline | Success Metric |
|---|---|---|---|---|
| P1 | Update SIEM escalation policy: all rule level ≥12 alerts must be escalated within 15 minutes, night shift included | SOC Lead | Within 30 days | Documented policy; tested in next table-top |
| P2 | Quarterly IR tabletop exercises; include ransomware and data breach scenarios | Security Team | Rolling (next in 90 days) | Exercise conducted; AAR produced |
| P3 | | | | |

---

## 6. Regulatory Obligations Summary

| Obligation | Triggered? | Deadline | Status |
|---|---|---|---|
| NIS2 early warning (24h) | Yes / No | [YYYY-MM-DDTHH:MMZ] | Completed / Pending |
| NIS2 notification (72h) | Yes / No | [YYYY-MM-DDTHH:MMZ] | Completed / Pending |
| GDPR Article 33 (72h) | Yes / No | [YYYY-MM-DDTHH:MMZ] | Completed / Pending |
| GDPR Article 34 (individuals) | Yes / No | Without undue delay | Completed / Pending |

---

## 7. Collaborative Response Chain Reflection

Complete the table: which role contributed to which phase?

| Phase | Exercise Role | Contribution |
|---|---|---|
| Detection & Triage | SOC Analyst (Ex 1) | |
| Scoping & Evidence | Incident Responder (Ex 2) | |
| Threat Intelligence | CTI Analyst (Ex 3) | |
| Attack Perspective | Pen Tester (Ex 4) | |
| Coordination | IR Coordinator (Ex 5) | |

**What would have failed without any one role?**
[Analyse the interdependencies — what did each role provide that the others could not?]

---

## 8. WP5:M8 Topic Coverage

| Topic | Demonstrated in This Exercise |
|---|---|
| Incident response lifecycle | |
| Digital forensics fundamentals | |
| Multi-channel phishing | |
| SIEM-driven detection | |
| CTI and threat actor profiling | |
| Regulatory obligations (NIS2, GDPR) | |
| Threat-informed security testing | |

---

*Template: NG-SOC LM8 Sub Case 1a | Assessed Activity 2.0.2 After-Action Report*
*Submit completed report to your instructor via REP or the shared drive.*
