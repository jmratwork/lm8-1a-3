# NG-SOC LM8 Sub Case 1a-3 – Incident Response and Forensics
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
├── V4_ngsoc-lm8-subcase1a-training.json  # REP training definition (47 levels)
├── README.md                             # This file
├── VALIDATION.md                         # Resource & tool validation table
├── CHANGELOG.md                          # Version history (v4 alignment with D5.8)
│
├── tools/
│   ├── validate-training.py              # Validates every flag against what is DEPLOYED
│   └── build-v4-phase3.py                # Generator that applied the Phase 3 levels
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
├── artifacts/                            # MIRROR of provisioning/roles/artifacts/files/
│   ├── README.md                         # why this is a mirror; how to re-sync
│   ├── phishing/
│   │   ├── phishing-email.eml            # Synthetic spear-phishing email
│   │   ├── phishing-sms.txt              # Synthetic smishing message
│   │   ├── phishing-call-script.txt      # Synthetic vishing transcript
│   │   └── suspicious-attachment.txt     # Static attachment metadata (no code)
│   ├── forensic-bundle/
│   │   ├── wazuh-alerts-ex2.json         # 11 synthetic SIEM alerts
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

Topic names below are taken **verbatim from D5.8 Table 2** so that the
deliverable and this repository can be cross-read line by line.

| WP5:M8 Topic (D5.8 Table 2) | Where in this repository |
|---|---|
| Incident handling and documentation | Exercises 1, 2, 5; activity 2.0.2 templates (decision log, SITREP, handover) |
| Threat intelligence enrichment and exploitation | Exercise 3; MISP event #1001 seeded by `cti-misp` |
| Containment, acquisition, eradication procedures | Exercises 2 & 5; `forensics-host` DFIR toolset and chain-of-custody template |
| SIEM alert triage and correlation | Exercise 1; Wazuh rules 100001–100005 on `siem` |
| Vulnerability identification in financial infrastructures | Exercises 3 & 4; `web-banking-vuln` (SQLi, weak admin credential, exposed `/backup`) |
| Use of CyberRangeCZ/KYPO simulators and REP tooling (scenario injects, collaboration space, quizzes, assessed practical submissions) | `topology.yml`; `V4_ngsoc-lm8-subcase1a-training.json` (47 levels: injects, 28 console tasks, 8 assessments) |
| ECSF role mapping and learning outcome alignment | Table below; every exercise carries an ECSF-aligned role |

**All 7 topics covered.** ✅

---

## ECSF Role Mapping

Profiles are the four named in **D5.8 Figure 2**. "Scenario role" is the job
title the learner plays; "ECSF profile" is the framework profile it maps to.

| Exercise / Activity | Scenario role | ECSF profile (D5.8 Figure 2) |
|---|---|---|
| Exercise 1 | SOC Analyst Tier 1 | Cyber Incident Responder |
| Exercise 2 | CSIRT Analyst / Incident Responder | Cyber Incident Responder |
| Activity 2.0.3 | Forensic analyst | **Digital Forensics Investigator** |
| Exercise 3 | CTI Analyst | Cyber Threat Intelligence Specialist |
| Exercise 4 | Penetration Tester (Red Team Operator) | Cyber Incident Responder *(offensive testing feeds the responder's threat-informed practice; Penetration Tester is not among the four M8 profiles)* |
| Exercise 5 | IR Coordinator / Facilitator | Cyber Incident Responder + **Cyber Legal, Policy & Compliance Officer** (NIS2 / GDPR notification decisions) |

> Coverage note: the *Cyber Legal, Policy & Compliance Officer* strand is
> currently carried by the Exercise 5 tabletop discussion only. Deepening it
> (criminal-investigation procedure, evidential admissibility, regulator
> notification as assessed items) is tracked as pending work.

---

## MITRE ATT&CK Techniques Covered

Techniques tagged on the training levels of `V4_ngsoc-lm8-subcase1a-training.json`:

| Technique | Name | Where |
|---|---|---|
| T1566 / T1566.001 | Phishing / Spearphishing Attachment | Ex 1, Ex 2, Act 2.0.1 |
| T1566.004 | Phishing via Service (smishing / vishing) | Act 2.0.1 |
| T1111 | Multi-Factor Authentication Interception (OTP relay) | Act 2.0.1 |
| T1071.001 | C2 via Application Layer Protocol | Ex 1, Ex 2 |
| T1571 | Non-Standard Port (C2 on 4444) | Ex 1 |
| T1543 | Create or Modify System Process (malware stub) | Ex 1 |
| T1053.005 | Scheduled Task/Job: Cron | Ex 1 |
| T1070 | Indicator Removal (beacon eradication) | Ex 2 |
| T1046 | Network Service Discovery (nmap recon) | Ex 4 |
| T1190 | Exploit Public-Facing Application (SQLi) | Ex 4 |
| T1110 | Brute Force | Act 2.0.3, Ex 4 |
| T1083 | File and Directory Discovery (exposed /backup) | Ex 2, Ex 4 |
| T1021.002 | Lateral Movement: SMB | Act 2.0.3 |
| T1486 | Data Encrypted for Impact | Ex 2, Ex 3, Ex 5 |

> This lists the ATT&CK tags carried by the console levels. The scenario
> narrative also exercises Valid Accounts (T1078), Data from Local System
> (T1005) and Exfiltration Over C2 (T1041) in the artefacts and briefings.

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
   - Kali: open its **GUI console** from the topology panel (log in as `analyst` / `ngsoc-analyst`)

> **Host access is via the REP/Guacamole GUI console**, not an SSH client — the
> training levels are written for the in-browser console (right-click a host →
> Open console). `sudo` works without a password.

### Instructor Checklist
See [docs/instructor-guide.md](docs/instructor-guide.md) → Section 3 for full REP session preparation checklist.

---

## Grading

**This table is the single source of truth for weighting.**
`docs/instructor-guide.md` §6 restates it and must not diverge.

| Component | Weight | Assessed how | Pass threshold |
|---|---|---|---|
| Exercises 1–5 | **60 %** | In-platform: 28 console flags + 8 assessment levels (REP-scored) | No exercise below 40 % |
| Activity 2.0.1 — multi-channel phishing triage | 15 % | Instructor-graded submission (triage note, observables, action set) | — |
| Activity 2.0.2 — collaborative response chain | 15 % | Instructor-graded artefacts (task board, decision log, SITREP, handover) | — |
| Activity 2.0.3 — express forensic report | 10 % | Instructor-graded participant inputs, consolidated by the facilitator | — |
| **Overall pass** | — | — | **≥ 60 % overall** |

The 60/40 split follows **D5.8 §2.0.4**, which weights (i) technical correctness,
(ii) completeness and quality of documentation and (iii) communication and
coordination under time pressure equally. Dimensions (ii) and (iii) live almost
entirely in the three practical activities, so they carry 40 % between them.

---

*NG-SOC WP5 | Learning Module 8 – Incident Response and Forensics | Sub Case 1a*
*CyberRangeCZ KYPO Sandbox Definition | British English | 2026*
