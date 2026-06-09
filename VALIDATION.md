# VALIDATION.md – Resource and Tool Reference Validation
**Project:** NG-SOC LM8 Sub Case 1a – KYPO Sandbox Definition
**Scope:** All resources, tools, services, and external references cited in the project

This table maps every referenced resource to its implementation status in the sandbox.

---

## Platform Images and Flavours

| Reference | Declared In | Validated | Notes |
|---|---|---|---|
| `ubuntu-noble-x86_64` | topology.yml | ✅ Valid | Used by web-banking, employee-ws, file-server, db-server, siem, analyst-host, cti |
| `debian-12-x86_64` | topology.yml | ✅ Valid | Used by router-perimeter, router-internal, c2-server |
| `kali-2020.4` | topology.yml | ✅ Valid | Used by kali |
| `standard.small` | topology.yml | ✅ Valid | 1vCPU/2GB/80GB |
| `standard.medium` | topology.yml | ✅ Valid | 1vCPU/4GB/80GB |
| `standard.large` | topology.yml | ✅ Valid | 2vCPU/16GB/80GB |

---

## Network CIDRs (must be disjoint from 100.100.100.0/24)

| Network | CIDR | Disjoint? | accessible_by_user |
|---|---|---|---|
| net-dmz | 10.10.20.0/24 | ✅ | true |
| net-corp | 10.10.30.0/24 | ✅ | false |
| net-security | 10.10.40.0/24 | ✅ | true |
| net-redteam | 10.10.50.0/24 | ✅ | true |
| Management (reserved) | 100.100.100.0/24 | N/A | Platform-managed |

---

## Tools and Services Deployed in Sandbox

| Tool / Service | Host | IP:Port | Provisioning Role | Status |
|---|---|---|---|---|
| **Wazuh Manager** (v4.7) | siem | 10.10.40.10:1514/1515 | siem | ✅ Deployed via apt |
| **OpenSearch Dashboards** | siem | 10.10.40.10:5601 | siem (Wazuh all-in-one) | ✅ |
| **Velociraptor** server | analyst-host | 10.10.40.20:8000/8889 | forensics-host | ✅ Binary + config |
| **MISP** (via Docker) | cti | 10.10.40.30:443 | cti-misp | ✅ docker-compose |
| **Apache2 + PHP** (vuln app) | web-banking | 10.10.20.10:80 | web-banking-vuln | ✅ |
| **MySQL** (bankdb) | web-banking + db-server | 3306 | web-banking-vuln / artifacts | ✅ |
| **Samba** file share | file-server | 10.10.30.20:445 | file-server | ✅ |
| **C2 simulator** (Python TCP) | c2-server | 10.10.20.20:4444 | c2-server | ✅ Synthetic only |
| **Wazuh Agent** | employee-ws | — | employee-ws | ✅ |
| **Wazuh Agent** | file-server | — | file-server | ✅ |
| **nmap** | kali | — | kali-redteam | ✅ |
| **nikto** | kali | — | kali-redteam | ✅ |
| **sqlmap** | kali | — | kali-redteam | ✅ |
| **hydra** | kali | — | kali-redteam | ✅ |
| **gobuster** | kali | — | kali-redteam | ✅ |
| **metasploit-framework** | kali | — | kali-redteam | ✅ |
| **SecLists** | kali | /opt/SecLists | kali-redteam | ✅ git clone |
| **Volatility 3** | analyst-host | — | forensics-host | ✅ pip3 install |
| **sleuthkit / autopsy** | analyst-host | — | forensics-host | ✅ apt |
| **tcpdump / tshark** | analyst-host | — | forensics-host | ✅ apt |
| **hashdeep** | analyst-host | — | forensics-host | ✅ apt |

---

## Synthetic Artefacts (All IoCs are Fictitious)

| Artefact | File | Notes |
|---|---|---|
| Phishing email (.eml) | artifacts/phishing/phishing-email.eml | Synthetic sender domain, synthetic attachment hash |
| Phishing SMS | artifacts/phishing/phishing-sms.txt | Synthetic phone number, synthetic short URL |
| Vishing script | artifacts/phishing/phishing-call-script.txt | Role-play only, synthetic URL |
| Attachment metadata | artifacts/phishing/suspicious-attachment.txt | No executable code; static analysis summary only |
| Wazuh alerts bundle | artifacts/forensic-bundle/wazuh-alerts-ex2.json | Synthetic alert JSON, 8 entries |
| Process list | artifacts/forensic-bundle/endpoint-process-list.txt | Synthetic ps/ss output |
| Netstat snapshot | artifacts/forensic-bundle/netstat-employee-ws.txt | Synthetic network connections |
| Apache access log | artifacts/forensic-bundle/web-banking-access.log | Synthetic HTTP requests |
| File metadata | artifacts/forensic-bundle/file-metadata.txt | Synthetic file listings, synthetic hashes |
| Timeline clues | artifacts/forensic-bundle/timeline-clues.txt | Structured evidence for student reconstruction |
| Ransomware tabletop | artifacts/ex5-ransomware/tabletop-scenario.txt | Ransom note text + inject sequence |
| .locked files (10×) | Deployed by file-server role to /srv/data/ | Empty text stubs, no encryption |
| MISP Event #1001 | Seeded by cti-misp role (seed-black-falcon.py) | 8 synthetic IoCs |
| C2 connections log | /var/log/c2-sim/connections.log on c2-server | Written by Python listener |

**IoC verification — none of these are real:**
- IP 10.10.20.20: RFC 1918 private, sandbox-only
- Domain `blackfalcon-sim.internal`: .internal TLD, non-routable
- MD5 `aabbccdd11223344aabbccdd11223344`: patterned hex, not a real malware hash
- SHA256 `deadbeef00112233...`: hex pattern, not a real hash
- BTC wallet `1A2B3C4D5E6F7G8H9I0J`: not a valid BTC address format

---

## Training JSON Files (CyberRangeCZ REP)

| File | Exercise | Level Types | MITRE Techniques |
|---|---|---|---|
| trainings/exercise-1-soc-triage.json | SOC Analyst (Ex 1) | InfoLevel, 3× TrainingLevel, AssessmentLevel | T1071.001, T1053.005 |
| trainings/exercise-2-containment.json | Incident Responder (Ex 2) | InfoLevel, 3× TrainingLevel, AssessmentLevel | T1005, T1041, T1053.005, T1190, T1078, T1486 |
| trainings/exercise-3-cti-briefing.json | CTI Analyst (Ex 3) | InfoLevel, 3× TrainingLevel, AssessmentLevel | T1566.001, T1071.001, T1486, T1005, T1190, T1078 |
| trainings/exercise-4-pentest.json | Pen Tester (Ex 4) | InfoLevel, 4× TrainingLevel, AssessmentLevel | T1190, T1078, T1083, T1005 |
| trainings/exercise-5-tabletop.json | IR Coordinator (Ex 5) | InfoLevel, 4× TrainingLevel, AssessmentLevel | T1486, T1021.002, T1041, T1566.001, T1053.005 |

---

## WP5:M8 Topic Coverage Matrix

| Topic | Ex 1 | Ex 2 | Ex 3 | Ex 4 | Ex 5 | Act 2.0.1 | Act 2.0.2 | Act 2.0.3 |
|---|---|---|---|---|---|---|---|---|
| 1. Incident response lifecycle | ✅ | ✅ | | | ✅ | | ✅ | ✅ |
| 2. Digital forensics fundamentals | | ✅ | | | | | | ✅ |
| 3. Multi-channel phishing / social engineering | ✅ | | | | | ✅ | | |
| 4. SIEM-driven threat detection | ✅ | ✅ | ✅ | | | | | ✅ |
| 5. CTI and threat actor profiling | | | ✅ | ✅ | ✅ | | | |
| 6. Regulatory obligations (NIS2, GDPR) | | ✅ | | | ✅ | | ✅ | |
| 7. Threat-informed penetration testing | | | ✅ | ✅ | | | | |

All 7 topics covered across the 5 exercises and 3 assessed activities. ✅

---

## Naming Rule Compliance

All topology names validated against CyberRangeCZ rules (characters [a-z A-Z 0-9 -], first char lowercase, globally unique):

| Name | Type | Compliant |
|---|---|---|
| net-dmz, net-corp, net-security, net-redteam | networks | ✅ |
| router-perimeter, router-internal | routers | ✅ |
| web-banking, c2-server, employee-ws, file-server, db-server, siem, analyst-host, cti, kali | hosts | ✅ |
| grp-dmz, grp-corp, grp-security, grp-redteam, grp-routing | custom groups | ✅ (grp- prefix avoids reserved names) |

Reserved groups NOT redefined: management, routers, hosts, ssh_nodes, winrm_nodes, user_accessible_nodes, hidden_hosts, windows_hosts, monitor-os, monitor-icmp ✅

---

## Cloud-Side Adjustments Required at Deployment

1. **Wazuh all-in-one installer** (siem role): downloads from packages.wazuh.com. Sandbox must have internet access or a local mirror must be configured.
2. **MISP Docker images** (cti-misp role): pulls from Docker Hub. Same internet access requirement.
3. **SecLists** (kali-redteam role): git clone from GitHub. Internet access required.
4. **Velociraptor binary** (forensics-host role): downloads from GitHub releases. Internet access required.
5. **Management network** (100.100.100.0/24): injected by platform; no overlap with defined networks. ✅
6. **Platform variables** used in playbook: global_ssh_public_user_key (student SSH key injection via common role). All other platform variables (global_openstack_stack_id etc.) are not directly used in this scenario.

---

*Last validated: 2026-06-09 | NG-SOC LM8 Sub Case 1a*
