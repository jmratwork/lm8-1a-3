# NG-SOC LM8 Sub Case 1a – KYPO Sandbox Definition
**Learning Module 8: Incident Response and Forensics**
CyberRangeCZ / KYPO Platform | NG-SOC WP5 Training Scenario

---

## Security Notice

> **All IoCs, hashes, IP addresses, domains, email subjects, and artefacts in this repository are entirely synthetic and sandbox-contained.**
> No real malware is present. No exploits target external systems. All "vulnerabilities" are deliberately introduced training artefacts in an isolated network.
> The C2 IP (10.10.20.20) is an RFC 1918 address that only exists inside the sandbox.
> The domain `blackfalcon-sim.internal` is a non-routable .internal name.

---

## Network Topology

```
WAN / Management (100.100.100.0/24 – platform automatic, all nodes)
              │                              │
              ▼                              ▼
   ┌─────────────────┐       ┌──────────────────────┐
   │  router-perimeter│◄─────►   router-internal    │
   │  gw: 10.10.20.1 │  WAN  │  gw: .30.1/.40.1    │
   │  debian-12      │       │  debian-12           │
   │  standard.small │       │  standard.small      │
   └────────┬────────┘       └──────────┬───────────┘
             │                           │
    ┌────────▼────────┐       ┌──────────▼───────────┐
    │  net-dmz        │       │  net-corp             │
    │  10.10.20.0/24  │       │  10.10.30.0/24        │
    │  (user-access)  │       │  (no user-access)     │
    │                 │       │                       │
    │  web-banking    │       │  employee-ws          │
    │  10.10.20.10    │       │  10.10.30.10          │
    │  ubuntu-noble   │       │  ubuntu-noble         │
    │  std.medium     │       │  std.small            │
    │                 │       │                       │
    │  c2-server      │       │  file-server          │
    │  10.10.20.20    │       │  10.10.30.20          │
    │  debian-12      │       │  ubuntu-noble         │
    │  std.small      │       │  std.small            │
    │  hidden: true   │       │                       │
    └─────────────────┘       │  db-server            │
                              │  10.10.30.30          │
    ┌─────────────────┐       │  ubuntu-noble         │
    │  net-security   │       │  std.medium           │
    │  10.10.40.0/24  │       └───────────────────────┘
    │  (user-access)  │
    │                 │       ┌───────────────────────┐
    │  siem           │       │  net-redteam          │
    │  10.10.40.10    │       │  10.10.50.0/24        │
    │  ubuntu-noble   │       │  (user-access)        │
    │  std.large      │       │                       │
    │  Wazuh+OpenSearch       │  kali                 │
    │                 │       │  10.10.50.10          │
    │  analyst-host   │       │  kali                 │
    │  10.10.40.20    │       │  std.large            │
    │  ubuntu-noble   │       └───────────────────────┘
    │  std.medium     │
    │  Velociraptor   │
    │                 │
    │  cti            │
    │  10.10.40.30    │
    │  ubuntu-noble   │
    │  std.large      │
    │  MISP (Docker)  │
    └─────────────────┘
```

**Resource footprint per instance:** ~14 vCPU, ~70 GB RAM

---

## Repository Structure

```
lm8-1a-3/
├── topology.yml                          # CyberRangeCZ topology (MUST stay in root)
├── README.md                             # This file
├── VALIDATION.md                         # Resource & tool validation table
│
├── provisioning/
│   ├── playbook.yml                      # 7-play Ansible playbook
│   ├── requirements.yml                  # Galaxy dependencies (empty)
│   ├── group_vars/
│   │   ├── all.yml                       # Global variables
│   │   ├── grp-security.yml              # Wazuh/MISP config
│   │   └── grp-corp.yml                  # Corp host config
│   └── roles/
│       ├── common/                       # Baseline: timezone, locale, hosts, user, MOTD
│       ├── router-config/                # ip_forward, iptables, static routes
│       ├── web-banking-vuln/             # DELIBERATELY VULNERABLE Apache+PHP+MySQL
│       ├── c2-server/                    # Synthetic C2 simulator (Python TCP listener)
│       ├── employee-ws/                  # Wazuh agent, beacon cron, pre-seeded logs
│       ├── file-server/                  # Samba, .locked files, ransom note, enc log
│       ├── siem/                         # Wazuh manager, custom rules, pre-seeded alerts
│       ├── forensics-host/               # DFIR tools, Velociraptor, CoC template
│       ├── kali-redteam/                 # Pen-test tools, SecLists, engagement brief
│       ├── cti-misp/                     # MISP Docker, seed script (Black Falcon event)
│       └── artifacts/                    # Student handout templates, artefact deployment
│
├── trainings/
│   ├── exercise-1-soc-triage.json        # SOC Analyst – SIEM triage
│   ├── exercise-2-containment.json       # Incident Responder – containment/eradication
│   ├── exercise-3-cti-briefing.json      # CTI Analyst – MISP threat intel
│   ├── exercise-4-pentest.json           # Pen Tester – SQLi + brute force
│   └── exercise-5-tabletop.json          # IR Coordinator – ransomware tabletop
│
├── artifacts/
│   ├── phishing/
│   │   ├── phishing-email.eml            # Synthetic spear-phishing email
│   │   ├── phishing-sms.txt              # Synthetic smishing message
│   │   ├── phishing-call-script.txt      # Synthetic vishing transcript
│   │   └── suspicious-attachment.txt     # Static attachment metadata (no code)
│   ├── forensic-bundle/
│   │   ├── wazuh-alerts-ex2.json         # 8 synthetic SIEM alerts
│   │   ├── endpoint-process-list.txt     # Synthetic ps/netstat output
│   │   ├── netstat-employee-ws.txt       # Synthetic network connections
│   │   ├── web-banking-access.log        # Synthetic Apache log with SQLi evidence
│   │   ├── file-metadata.txt             # Synthetic file listing + encryption events
│   │   └── timeline-clues.txt            # Ordered clues for timeline reconstruction
│   └── ex5-ransomware/
│       └── tabletop-scenario.txt         # Inject sequence + ransom note text
│
└── docs/
    ├── instructor-guide.md               # Full instructor reference (32KB+)
    └── student-handouts/
        ├── exercise-1-handout.md         # SOC Analyst tasks
        ├── exercise-2-handout.md         # Incident Responder tasks
        ├── exercise-3-handout.md         # CTI Analyst tasks
        ├── exercise-4-handout.md         # Pen Tester tasks
        ├── ex5-tabletop-scenario.md      # IR Coordinator tabletop guide
        ├── ex5-after-action-report.md    # AAR template (Ex 5 / Activity 2.0.2)
        └── express-forensic-report-template.md  # Activity 2.0.3 report template
```

---

## WP5:M8 Coverage Matrix

| Topic | Ex 1 | Ex 2 | Ex 3 | Ex 4 | Ex 5 | 2.0.1 | 2.0.2 | 2.0.3 |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Incident response lifecycle | ✅ | ✅ | | | ✅ | | ✅ | ✅ |
| Digital forensics fundamentals | | ✅ | | | | | | ✅ |
| Multi-channel phishing / social engineering | ✅ | | | | | ✅ | | |
| SIEM-driven threat detection | ✅ | ✅ | ✅ | | | | | ✅ |
| CTI and threat actor profiling | | | ✅ | ✅ | ✅ | | | |
| Regulatory obligations (NIS2, GDPR) | | ✅ | | | ✅ | | ✅ | |
| Threat-informed penetration testing | | | ✅ | ✅ | | | | |

**All 7 topics covered.** ✅

---

## ECSF Role Mapping

| Exercise | Role | ECSF Profile |
|---|---|---|
| Exercise 1 | SOC Analyst Tier 1 | Cyber Incident Responder |
| Exercise 2 | CSIRT Analyst / Incident Responder | Cyber Incident Responder |
| Exercise 3 | CTI Analyst | Cyber Threat Intelligence Specialist |
| Exercise 4 | Penetration Tester | Penetration Tester |
| Exercise 5 | IR Coordinator | Cyber Incident Responder / CISO |

---

## MITRE ATT&CK Techniques Covered

| Technique | Name | Exercise(s) |
|---|---|---|
| T1566.001 | Spearphishing Attachment | Ex 3, Ex 5, Act 2.0.1 |
| T1190 | Exploit Public-Facing Application (SQLi) | Ex 2, Ex 3, Ex 4 |
| T1078 | Valid Accounts | Ex 2, Ex 3, Ex 4 |
| T1071.001 | C2 via Application Layer Protocol | Ex 1, Ex 3 |
| T1053.005 | Scheduled Task/Job: Cron | Ex 1, Ex 2, Ex 5 |
| T1486 | Data Encrypted for Impact | Ex 2, Ex 3, Ex 5 |
| T1005 | Data from Local System | Ex 2, Ex 3, Ex 4 |
| T1041 | Exfiltration Over C2 Channel | Ex 2, Ex 5 |
| T1021.002 | Lateral Movement: SMB | Ex 5 |
| T1083 | File and Directory Discovery | Ex 4 |

---

## Deployment

### Prerequisites
- CyberRangeCZ / KYPO platform access
- OpenStack tenant with sufficient quota (~14 vCPU, ~70 GB RAM per instance)
- Internet connectivity from sandbox hosts (for package downloads at provision time)

### Deploy
1. Upload this repository to the KYPO platform
2. Create a new sandbox definition pointing to `topology.yml` (root of this repo)
3. Provision takes approximately 30–45 minutes
4. Verify after provisioning:
   - Wazuh Dashboard: http://10.10.40.10:5601 (admin / admin, change on first login)
   - MISP: https://10.10.40.30 (admin@admin.test / admin, change on first login → NGSOCAdmin2025!)
   - Web banking: http://10.10.20.10 (admin / admin123 – deliberately weak)
   - Kali: SSH to 10.10.50.10 as `analyst`

### Instructor Checklist
See [docs/instructor-guide.md](docs/instructor-guide.md) → Section 3 for full REP session preparation checklist.

---

## Grading

| Component | Weight | Pass Threshold |
|---|---|---|
| Exercises 1–5 (knowledge checks) | 60% | No exercise below 40% |
| Activity 2.0.1 (multi-channel phishing triage) | 15% | — |
| Activity 2.0.2 (collaborative response chain) | 15% | — |
| Activity 2.0.3 (express forensic report) | 10% | — |
| **Overall pass** | — | **≥ 60% overall** |

---

*NG-SOC WP5 | Learning Module 8 – Incident Response and Forensics | Sub Case 1a*
*CyberRangeCZ KYPO Sandbox Definition | British English | 2026*
