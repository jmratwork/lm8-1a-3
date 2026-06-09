# Exercise 2 – Incident Responder: Student Handout
**Role:** CSIRT Analyst / Incident Responder | **Duration:** ~60 minutes
**Platforms:** analyst-host (10.10.40.20), SIEM at http://10.10.40.10:5601

---

## Scenario

The SOC has escalated an active incident. You have been handed the escalation note from Exercise 1. Additional findings since escalation:

- **employee-ws** confirmed infected (C2 beacon to 10.10.20.20:4444)
- **web-banking** exploited via SQL injection; backdoor dropped
- **file-server** and **db-server** show lateral movement indicators
- Customer data (`bankdb.accounts`) accessed at 02:14 UTC
- Cron job `/etc/cron.d/svc-update` present on compromised hosts

---

## Quick Reference

| Tool | Location | Use |
|---|---|---|
| Velociraptor | https://10.10.40.20:8889 | Remote process/file enumeration |
| Volatility 3 | `vol3` command | Memory forensics |
| Wazuh | http://10.10.40.10:5601 | SIEM cross-host alerts |
| forensics-quickref.txt | `~/tools/forensics-quickref.txt` | Command cheatsheet |
| Chain of custody | `~/reports/chain-of-custody-template.txt` | Evidence tracking |

---

## Tasks

### Task 1 – Evidence Collection
1. For each affected host, state the evidence you will collect (type + tool + hash method)
2. Complete the chain-of-custody template: `~/reports/chain-of-custody-template.txt`
3. Using Velociraptor, enumerate processes on `file-server`

### Task 2 – Containment Decision
Answer and justify:
- [ ] Isolate `employee-ws` from network: Yes/No and why?
- [ ] Block C2 IP (10.10.20.20) at router-perimeter: Yes/No and how?
- [ ] Disable `dbadmin` account: Yes/No and why?
- Document in `~/handouts/decision-log.md`

### Task 3 – Eradication and Recovery
1. List ALL steps to remove the threat (all affected hosts)
2. How do you verify each host is clean?
3. Which hosts restore from backup vs. rebuild?
4. Draft SITREP using `~/handouts/sitrep-template.md`

### Task 4 – NIS2 Notification
- Does this incident require NIS2 notification? Yes/No + justification
- When does the 24-hour clock start?

---

## Order of Volatility (always collect in this order)

1. Running processes → 2. Network connections → 3. Open files → 4. System logs → 5. Disk image

---

## Deliverable

Submit: evidence collection plan, containment decisions (from decision log), SITREP, NIS2 notification decision.

---

*NG-SOC LM8 Sub Case 1a | Exercise 2 | British English*
