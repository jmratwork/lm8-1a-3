# Exercise 1 – SOC Analyst Triage: Student Handout
**Role:** SOC Analyst Tier 1 | **Duration:** ~45 minutes
**Platform:** Wazuh SIEM at http://10.10.40.10:5601

---

## Scenario

It is 02:13 UTC. You are the on-duty SOC Analyst. Two SIEM alerts have fired on `employee-ws` (10.10.30.10):

- **Rule 100001**: Outbound TCP to 10.10.20.20:4444 (known C2)
- **Rule 100002**: Endpoint log — possible Trojan: `/tmp/.svc_update`

No user has reported anything. Your job is to triage, assess severity, and decide whether to escalate.

---

## Step-by-Step Tasks

### Task 1 – Access the SIEM
1. Open a browser and go to http://10.10.40.10:5601
2. Navigate to **Security Events**
3. Filter by `agent.name: employee-ws`
4. Examine alerts for rule IDs 100001 and 100002

### Task 2 – Document Your Findings
Complete the table:

| Field | Your Finding |
|---|---|
| Source IP | |
| Destination IP | |
| Destination Port | |
| Suspicious process | |
| Suspicious domain (if seen in DNS logs) | |
| Rule IDs triggered | |
| True positive? (Y/N + justification) | |

### Task 3 – Severity Assessment
- [ ] What severity level (P1/P2/P3/P4) do you assign?
- [ ] What is your justification?

### Task 4 – Escalation Note
Draft a brief escalation ticket for the CSIRT team. Include:
- What was detected (summary)
- Evidence (rule IDs, IoCs)
- Actions taken
- What you need from IR

---

## Hints

**True positive check**: Multiple independent sources (network rule + endpoint log) at the same time on the same host = high confidence.

**Severity**: A confirmed banking trojan on a corporate workstation with access to financial data is typically P1 or P2.

**SIEM navigation**: In Wazuh Dashboard → Security Events → add filter → agent.name is employee-ws

---

## Deliverable

Submit: your completed table, severity justification, and escalation note (via REP or as a text file).

---

*NG-SOC LM8 Sub Case 1a | Exercise 1 | British English*
