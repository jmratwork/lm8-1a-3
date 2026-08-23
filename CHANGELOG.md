# Changelog — NG-SOC LM8 Sub Case 1a

## v4 — alignment with D5.8 v0.12 (2026-08-23)

Brings the cyber-range repository and its REP training definition into line with
deliverable **D5.8 Learning Module 8 (Sub Case 1a) v0.12**, and repairs several
internal inconsistencies found while doing so.

### Training definition
- **New consolidated definition** `V4_ngsoc-lm8-subcase1a-training.json` (47
  levels: 28 hands-on console tasks, 8 assessments, plus INFO/ACCESS). Replaces
  the earlier V3 (39 levels) and the five per-exercise files under `trainings/`
  (removed — unscored legacy schema; retained in git history).
- **Exercise 4 is now genuine penetration testing** (D5.8 §2.4): added Kali
  reconnaissance (`nmap`) and threat-informed SQL-injection analysis from the
  server access log, with instruction to reproduce the `' OR '1'='1'--` exploit
  manually. Removed the shortcut that handed the learner the MySQL root password.
- **Multi-channel phishing is now analysed** (D5.8 §2.0.1): four levels across
  email, SMS and voice artefacts (sender domain, malicious attachment, smishing
  URL, vishing pretext) plus a triage assessment. Previously the phishing
  artefacts were never opened.
- **Coordination is now assessed** (D5.8 §2.0.2): assessment covering decision
  log, SITREP, evidence→contain→restore sequencing, and the **Communications/PR**
  role.
- **Legal/regulatory obligations assessed** (D5.8 Fig. 2 "criminal investigation
  procedures"): GDPR Art. 33 (72 h) folded into the Exercise 2 assessment; NIS2
  early-warning (24 h) and evidential preservation into the Exercise 5 assessment.
- Fixed the roadmap table and level counts; roadmap now uses relative references
  so it survives future renumbering. Host of the 2.0.1/2.0.2 templates unified to
  `analyst-host`.

### Artefacts & sandbox
- **Resolved a silent drift** between `artifacts/` and the deployed
  `provisioning/roles/artifacts/files/`: the two had diverged to different
  incident dates and codenames ("Operation Black Friday" vs the deployed
  "Operation Locked Ledger"). `artifacts/` is now a documented **mirror** of the
  deployed tree (see `artifacts/README.md`).
- **Removed a phantom evidence path**: the forensic evidence referenced
  `/srv/shares/finance/`, which `file-server` never creates. All evidence now
  points at the canonical `/srv/data/` that the host actually provisions and that
  the ransom note and level 23 already use.

### Documentation
- Coverage matrix rewritten with the **verbatim D5.8 Table 2 topic names**.
- ECSF mapping corrected to the four D5.8 Figure 2 profiles (added Digital
  Forensics Investigator and Cyber Legal, Policy & Compliance Officer).
- **Single grading source of truth** (README): 60 % exercises / 40 % practical
  activities, per D5.8 §2.0.4. Instructor guide §6 now restates it without
  divergence.
- Express forensic report template unified to the seven D5.8 §2.0.3 headings.
- Corrected phantom artefact references in the instructor guide
  (`suspicious-attachment.zip` → `.txt`; `network-capture.pcap` documented as not
  deployed).

### Tooling
- `tools/validate-training.py` — validates every flag against the artefacts the
  sandbox **actually deploys** (not the `artifacts/` mirror) and reports drift.
  Current: **28 ok, 0 warn, 0 fail**.
- `tools/build-v4-phase3.py` — idempotent generator that applied the Phase 3
  level insertions and renumbering (kept for traceability).

### Open items (require decisions or the target platform)
- `mitre_techniques[].technique_key` uses the `TA0011.T1071` (tactic.technique)
  form. **Confirm the accepted form against the target REP instance before
  import**; unify to sub-techniques if required.
- `state` stays `UNRELEASED` until a successful REP import is confirmed.
- A DNS-tunnelling `network-capture.pcap` would strengthen the §2.0.3 "network
  traces" element; not yet generated. `netstat-employee-ws.txt` carries that
  strand meanwhile.
- `origin/main` sits behind `origin/v2` (the branch local `main` tracks); a
  default clone still fetches the older tree.
