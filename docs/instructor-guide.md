# Instructor Guide – NG-SOC Learning Module 8
## Incident Response and Forensics (Sub Case 1a)
### CyberRangeCZ/KYPO Deployment & Delivery Reference

---

## 1. CyberRangeCZ Layout Constraints (from official docs)

These rules are **mandatory**. Violation will cause the platform to reject the repository.

### 1.1 Required File Structure

```
/topology.yml                          ← MUST be in root; NEVER in a subdirectory
/variables.yml                         ← Optional; only for APG variant-answer generation
/provisioning/
    playbook.yml                       ← Required; main Ansible entry point
    pre-playbook.yml                   ← Optional; installs prerequisites before playbook.yml
    requirements.yml                   ← Optional; Ansible Galaxy dependencies
    roles/
        <role-name>/
            tasks/main.yml             ← Required per role
            defaults/main.yml          ← Optional (role defaults)
            templates/                 ← Optional (Jinja2 templates)
            files/                     ← Optional (static files copied to host)
            handlers/main.yml          ← Optional
            vars/main.yml              ← Optional
    group_vars/                        ← Optional
    host_vars/                         ← Optional
/trainings/                            ← Training definition files (JSON format)
/artifacts/                            ← Synthetic evidence bundles
/docs/                                 ← This guide and student handouts
```

### 1.2 Naming Rules

- Allowed characters: `[a-z A-Z 0-9 -]` only (no underscores, no dots)
- **First character must be lowercase**
- All host, router, and network names must be **globally unique** within the topology

### 1.3 Reserved Ansible Host Groups (never redefine in `groups:`)

| Group | Auto-populated with |
|---|---|
| `management` | Sandbox management node |
| `routers` | All routers from topology |
| `hosts` | All hosts from topology |
| `ssh_nodes` | Nodes using SSH management |
| `winrm_nodes` | Nodes using WinRM management |
| `user_accessible_nodes` | Nodes on `accessible_by_user: true` networks |
| `hidden_hosts` | Hosts marked `hidden: true` |
| `windows_hosts` | Windows OS hosts (v2025.01+) |
| `monitor-os` | Monitoring targets of OS type |
| `monitor-icmp` | Monitoring targets of ICMP type |

Custom groups in this project use the prefix `grp-` to avoid any conflict.

### 1.4 Valid Base Images

| Image ID | OS | Notes |
|---|---|---|
| `debian-12-x86_64` | Debian 12 | Recommended for routers |
| `ubuntu-noble-x86_64` | Ubuntu 24.04 LTS | Recommended for service hosts |
| `centos-8` | CentOS 8 | |
| `windows-10` | Windows 10 | winrm mgmt |
| `windows-server-2019` | Windows Server 2019 | winrm mgmt |
| `kali` | Kali Linux | Red-team host |
| `cirros-0-x86_64` | CirrOS | Minimal test only |

**Cloud-side adjustments**: If `ubuntu-noble-x86_64` is unavailable, substitute `ubuntu-focal-x86_64` (Ubuntu 20.04). If `kali` is unavailable, request import or substitute `ubuntu-noble-x86_64` and install Kali tools via provisioning.

### 1.5 Standard Flavours

| Flavour | vCPU | RAM | Disk |
|---|---|---|---|
| `standard.small` | 1 | 2 GB | 80 GB |
| `standard.medium` | 1 | 4 GB | 80 GB |
| `standard.large` | 2 | 16 GB | 80 GB |

**Resource footprint of this sandbox**: ~14 vCPU, ~70 GB RAM per instance.  
To reduce: downgrade `siem` and `cti` to `standard.medium` and `kali` to `standard.medium` (some services will be slower).

### 1.6 CIDR Constraints

- All CIDRs must be **disjoint** (no overlap between any two networks)
- Must **not overlap** with the management network `100.100.100.0/24` (auto-reserved)
- Gateway addresses are auto-assigned by the platform; router IPs use `.1` per network subnet

### 1.7 Platform-Injected Ansible Variables

Available automatically in all playbook tasks:

```
global_openstack_stack_id     global_pool_id          global_sandbox_id
global_sandbox_name           global_sandbox_ip        global_head_ip
global_ssh_public_user_key    global_ssh_public_mgmt_key
global_syslog_destination_port   (v2025.01+ only)
```

### 1.8 Docker Containers

- Declared in a separate `containers.yml` (not inside `topology.yml`)
- Host must be Debian 12+, Python 3.4+; use `standard.large` for ≥2 containers per host
- **Never reboot** a host running Docker containers during provisioning
- No Guacamole/SPICE console for containers; access via SSH tunnel through the host

### 1.9 Training Definitions

- Stored in **JSON format** (upload/download via REP)
- Linear training levels: `TrainingLevel`, `AssessmentLevel`, `InfoLevel`, `AccessLevel`
- MITRE ATT&CK techniques can be mapped per level
- Correct answers support APG variable substitution for variant sandboxes

---

## 2. Topology Overview

See `README.md` for the full ASCII diagram. Summary:

| Segment | CIDR | User-Accessible | Key Hosts |
|---|---|---|---|
| net-dmz | 10.10.20.0/24 | Yes | web-banking, c2-server (hidden) |
| net-corp | 10.10.30.0/24 | No | employee-ws, file-server, db-server |
| net-security | 10.10.40.0/24 | Yes | siem, analyst-host, cti |
| net-redteam | 10.10.50.0/24 | Yes | kali |

---

## 3. REP Session Preparation Checklist

Complete **before** trainees join the session:

- [ ] Deploy sandbox pool (allow 30–45 minutes for provisioning to complete)
- [ ] Verify all hosts are reachable from the management node
- [ ] Open `http://10.10.40.10:5601` (Wazuh/Kibana) — confirm synthetic alerts are visible
- [ ] Open `https://10.10.40.30` (MISP) — confirm Black Falcon event is loaded with IoCs
- [ ] Open `http://10.10.20.10` (banking web app) — confirm login page loads
- [ ] Verify `employee-ws` is sending periodic beacons to `c2-server` (check SIEM)
- [ ] Enable REP collaboration features: coordination room, task board, discussion threads
- [ ] Assign sandbox roles to trainee accounts in REP
- [ ] Load inject timeline scripts (see §5 below)
- [ ] Brief co-instructors on their inject cues

---

## 4. Exercise-by-Exercise Delivery Notes

### Exercise 1 — Suspicious Network Activity (SOC Analyst Triage)

**Duration**: 45–60 minutes  
**Role**: SOC Analyst Tier 1  
**Platform access**: `siem` (10.10.40.10, port 5601)

**Instructor setup**:
- The `employee-ws` host runs a cron job (`/opt/c2-beacon/beacon.sh`) every 5 minutes that:
  - Opens a TCP connection to `c2-server` (10.10.20.20, port 4444)
  - Writes a synthetic log entry: `POSSIBLE TROJAN INFECTION detected on employee-ws`
  - These events appear in the Wazuh SIEM under rule ID 100001
- Wazuh custom rule also fires on outbound traffic to 10.10.20.20

**Inject script** (paste into REP coordination room at T+0):
```
INJECT 1A [T+00:00]: SIEM Alert — Rule 100001 fired on employee-ws.
Outbound connection to 10.10.20.20:4444 detected.
Endpoint agent log: "possible Trojan infection — process /tmp/.svc_update"
No user reports received. Shift handover in 2 hours.
```

**Formative quiz questions** (deploy via REP quiz module):
1. What two data sources corroborate the alert? *(Expected: SIEM rule + endpoint agent log)*
2. What is the first containment action you would take? *(Expected: isolate the workstation OR block the IP)*
3. Which phase of the IR lifecycle is this? *(Expected: Detection & Analysis)*

**Assessment checklist** (for submitted triage note):
- [ ] IoCs identified: IP 10.10.20.20, port 4444, process `/tmp/.svc_update`
- [ ] Severity justified with evidence (not just opinion)
- [ ] Escalation decision stated with rationale
- [ ] Handover note contains: timestamp, host, alert ID, actions taken
- [ ] Documentation is structured and time-stamped

---

### Exercise 2 — Containment and Eradication (Incident Responder)

**Duration**: 60–90 minutes  
**Role**: CSIRT Analyst / Incident Responder  
**Platform access**: `analyst-host` (10.10.40.20), `siem` (10.10.40.10)

**Instructor setup**:
- `file-server` contains `/srv/data/customers.csv` (synthetic), `/srv/data/README-RANSOM.txt`, and 10 synthetic `.locked` files
- `web-banking` has a deliberately vulnerable PHP login form at `/login.php`
- Wazuh on `siem` shows lateral movement alerts (simulated via pre-loaded log entries)
- Velociraptor server is running on `analyst-host` with agents installed on all corp hosts

**Inject script** (T+0, after Exercise 1 escalation):
```
INJECT 2A [T+00:00]: CSIRT activated. Scope confirmed: web-banking exploited via SQLi
(CVE-2024-XXXX-SIM). Malware deployed on file-server and db-server.
Possible data exfiltration via DNS tunnelling to 10.10.20.20. Persistence:
cron job /etc/cron.d/svc-update on both servers. IR Plan Section 3.2 activated.
```

```
INJECT 2B [T+00:20]: IT reports db-server unresponsive. Customer data table
'accounts' last accessed by user 'dbadmin' at 02:14 UTC — unusual hour.
```

**Assessment checklist** (for incident response report):
- [ ] Evidence collection plan covers: disk image, memory dump, netflow, auth logs
- [ ] Chain-of-custody described (hash verification step present)
- [ ] Containment strategy includes both immediate and long-term measures
- [ ] Eradication steps cover: malware removal, patch, backdoor elimination, persistence removal
- [ ] Recovery plan includes validation tests before going live
- [ ] At least 2 lessons learned identified
- [ ] Communication plan names correct stakeholders (management, legal, IR team)

---

### Exercise 3 — Threat Intelligence Briefing (CTI Analyst)

**Duration**: 45–60 minutes  
**Role**: Cyber Threat Intelligence Analyst  
**Platform access**: `cti` (10.10.40.30, MISP at https://10.10.40.30)

**Instructor setup**:
- MISP contains event "Black Falcon" with the following synthetic IoCs:
  - IP: 10.10.20.20 (C2, already seen in Ex 1)
  - Domain: `update-svc.blackfalcon-sim.internal`
  - MD5: `aabbccdd11223344aabbccdd11223344` (payload dropper)
  - SHA256: `deadbeef00112233...` (stage-2 loader)
  - Email subject: "Urgent: Q4 Wire Transfer Authorisation Required"
  - Email subject: "Security Alert: Verify Your Online Banking Credentials"
- MISP galaxy tag: "MITRE ATT&CK — T1566.001 Spearphishing Attachment"

**Inject script**:
```
INJECT 3A [T+00:00]: FS-ISAC advisory received. Campaign "Black Falcon" actively
targeting regional banking sector. IoCs loaded in MISP (Event #1001).
Management requests CTI brief within 90 minutes for circulation to SOC, IR, and IT.
```

**Assessment checklist** (for Threat Intelligence Brief):
- [ ] TTPs described with MITRE ATT&CK mapping (at minimum T1566, T1071, T1486)
- [ ] IoCs listed and prioritised (high/medium/low reliability)
- [ ] Risk assessment identifies most exposed assets (payment processing, transaction DB)
- [ ] Recommendations are team-specific: SOC / IR / IT each have action items
- [ ] Intelligence dissemination plan (internal format + external ISAC sharing considered)
- [ ] Analyst's Notes section includes confidence level

---

### Exercise 4 — Proactive Security Testing (Pen Tester)

**Duration**: 60–90 minutes  
**Role**: Penetration Tester / Red Team Operator  
**Platform access**: `kali` (10.10.50.10)

**Instructor setup**:
- `web-banking` login page at `http://10.10.20.10/login.php` — vulnerable to SQLi
  - Payload `' OR '1'='1` in username field bypasses authentication
  - `/admin` accessible with username `admin`, password `admin123`
- `db-server` MySQL (port 3306) accessible from `web-banking` app user
- `file-server` SMB share open (no authentication required on `/srv/share`)

**Inject script**:
```
INJECT 4A [T+00:00]: Red Team engagement authorised (scope: 10.10.20.0/24 and
10.10.30.0/24). Rules of engagement: no DoS, no data destruction, document all
findings. Start time logged. Attack surface: web-banking.example.internal (10.10.20.10).
```

**Assessment checklist** (for Penetration Test Report):
- [ ] Attack plan shows multi-stage kill chain (Recon → Initial Access → Exploitation → Lateral Movement)
- [ ] Tools listed with purpose per stage
- [ ] At least 2 critical findings documented with evidence
- [ ] Findings mapped to MITRE ATT&CK (e.g., T1190, T1078, T1021)
- [ ] Root cause analysis per finding (patch gap, misconfig, weak policy)
- [ ] Mitigations are specific and actionable (parameterised queries, MFA, SMB auth)
- [ ] Executive summary intelligible to non-technical reader

---

### Exercise 5 — Tabletop Simulation (IR Coordinator)

**Duration**: 60–90 minutes  
**Role**: IR Coordinator / Facilitator  
**Materials**: `/artifacts/ex5-ransomware/` bundle + `/docs/student-handouts/ex5-after-action-report.md`

**Instructor setup**:
- No sandbox interaction required; this is a facilitated discussion exercise
- Distribute the tabletop scenario brief from `/docs/student-handouts/ex5-tabletop-scenario.md`
- Use REP coordination room as the shared workspace
- Instructor triggers injects on schedule (see below)

**Inject timeline**:

| Time | Inject |
|---|---|
| T+00:00 | Multiple employees report files renamed `.locked`; ransom note on screen |
| T+00:10 | SOC confirms encryption spread to 3 file servers; C2 traffic to 10.10.20.20 |
| T+00:20 | CEO receives ransom email (synthetic, in artefacts bundle) |
| T+00:35 | IT confirms backups are intact for 2 of 3 servers; 1 server backup is 48h old |
| T+00:50 | Regulator notification deadline: 72 hours under NIS2 (inform participants) |
| T+01:00 | Exercise ends; debrief begins |

**Assessment checklist** (for After-Action Report):
- [ ] Exercise objectives stated (2–3 clear objectives)
- [ ] Scenario narrative accurate and immersive
- [ ] Roles and responsibilities mapped for each participant function
- [ ] Walk-through covers all 6 IR phases (Preparation through Post-Incident)
- [ ] Decision log maintained with rationale per decision
- [ ] At least 3 findings/gaps identified
- [ ] Plan update recommendations are specific and actionable
- [ ] Report suitable for CISO/CIO audience

---

## 5. Practical Activities (Section 2.0) — Assessment Integration

### 2.0.1 Multi-channel Spear-Phishing Simulation

**Instructor action**: Release artefacts from `/artifacts/phishing/` via REP file share at the start of Exercise 1.

Contents released:
- `phishing-email.eml` — email with malicious attachment lure
- `phishing-sms.txt` — SMS message with shortened URL
- `phishing-call-script.txt` — voice phishing script (read by instructor or played)
- `suspicious-attachment.zip` (password: `infected`, contains a text file with simulated dropper IOCs)

**Assessed outputs** (collect via REP submission):
- Phishing triage note (lure theme, intent, risk)
- List of extracted observables
- Recommended response action set

**Assessment criteria**:
- [ ] Spear-phishing indicators correctly identified across ≥2 channels
- [ ] Observables list is complete (sender domain, URLs, hash/filename, phone number)
- [ ] Response actions are proportionate (not over-blocking, not under-responding)
- [ ] Documentation structured, time-stamped, suitable for handover

---

### 2.0.2 Collaborative Response Chain

**Instructor action**: Assign roles in REP before session; enable coordination room, task board.

Roles to assign:
- SOC Analyst — `employee-ws` / SIEM triage
- Incident Responder — `analyst-host` / containment
- CTI Analyst — `cti` / Black Falcon brief
- IT Operations — `db-server` / `file-server` recovery coordination
- IR Coordinator — overall tracking + SITREP

**Assessed outputs** (exported from REP task board):
- Task board snapshot with owners, status, deadlines
- Decision log (≥5 key decisions with rationale)
- SITREP suitable for management
- Handover notes for next shift

**Assessment criteria**:
- [ ] Structured collaboration evident (tasks assigned, not just discussed)
- [ ] Decision log complete and accurate
- [ ] SITREP is concise, clear, audience-appropriate
- [ ] Handover notes self-contained (next shift can act without asking questions)

---

### 2.0.3 Express Forensic Report

**Instructor action**: Release artefact bundle from `/artifacts/forensic-bundle/` via REP at the start of Exercise 2. Set a 30-minute analysis window.

Bundle contents:
- `wazuh-alerts-ex2.json` — SIEM alert extract
- `endpoint-process-list.txt` — ps aux output from employee-ws (synthetic)
- `netstat-employee-ws.txt` — netstat -an output (synthetic)
- `web-banking-access.log` — Apache access log with SQLi evidence
- `file-metadata.txt` — find output with .locked file timestamps
- `network-capture.pcap` — 15-packet synthetic pcap (DNS tunnelling simulation)
- `timeline-clues.txt` — key timestamps and events summary

**Instructor action (post-analysis)**: Compile participant inputs into the express forensic report template (`/docs/student-handouts/express-forensic-report-template.md`) and share via REP.

**Assessment criteria**:
- [ ] Inputs traceable to specific artefacts (no invented evidence)
- [ ] Timeline is internally consistent
- [ ] Initial access vector correctly identified
- [ ] Key indicators listed (IP, hash, process name, domain)
- [ ] Recommendations prioritised correctly
- [ ] Professional quality: structured, clear, UK English

---

## 6. Grading Summary

| Activity / Exercise | Weight | Assessed By |
|---|---|---|
| Ex 1 — SOC Triage report | 15% | Checklist §4.1 |
| Ex 2 — IR report | 20% | Checklist §4.2 |
| Ex 3 — CTI Brief | 15% | Checklist §4.3 |
| Ex 4 — Pentest Report | 20% | Checklist §4.4 |
| Ex 5 — After-Action Report | 15% | Checklist §4.5 |
| Activity 2.0.1 — Phishing triage note | 5% | Checklist §5.1 |
| Activity 2.0.2 — Collaborative artefacts | 5% | Checklist §5.2 |
| Activity 2.0.3 — Forensic report inputs | 5% | Checklist §5.3 |

**Pass threshold**: 60% overall; no single exercise below 40%.

---

## 7. Cloud-Side Adjustments Required at Deployment

The following items must be verified or adjusted to match the **target OpenStack environment** before deployment:

1. **Image availability**: Confirm `kali`, `ubuntu-noble-x86_64`, and `debian-12-x86_64` exist in the target cloud. Update `topology.yml` if substitution needed.
2. **Flavour names**: Confirm `standard.small`, `standard.medium`, `standard.large` are valid. Some clouds use `m1.small` etc. — update accordingly.
3. **Management CIDR**: Confirm management network uses `100.100.100.0/24`. If different, verify none of the topology CIDRs conflict.
4. **MISP SMTP**: MISP provisioning disables email by default; if outbound email is required, configure SMTP relay in `provisioning/group_vars/grp-security.yml`.
5. **Wazuh licence**: Wazuh open-source is used; no licence key required. For the commercial stack, update `roles/siem/defaults/main.yml`.
6. **Sandbox pool size**: For a class of 20 students (5 per sandbox), provision 4 sandbox instances. For individual sandboxes, provision 20 instances — coordinate with platform admin on resource quotas.
