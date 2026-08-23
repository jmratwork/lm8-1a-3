#!/usr/bin/env python3
"""
build-v4-phase3.py - apply Phase 3 (pedagogical alignment with D5.8) to V4.

Loads the validated 39-level V4, inserts the new levels, renumbers every
`order` to a contiguous 0..N, and writes V4 back. Run once; idempotent-guarded
by a marker level title so a second run is a no-op.

New content:
  2.0.1  4 hands-on phishing-analysis levels + 1 assessment
  2.0.2  1 coordination assessment (incl. Communications/PR role)
  Ex.4   2 hands-on red-team levels (nmap recon, SQLi evidence analysis)
  3.4    NIS2 / GDPR / evidential-preservation questions folded into the
         Exercise 2 and Exercise 5 assessments (no new levels)
"""

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
V4 = REPO / "V4_ngsoc-lm8-subcase1a-training.json"

MARKER = "Phishing analysis - the email sender domain"


def tl(title, answer, content, solution, cmd_hint, where_hint,
       techniques=None, cmds=None):
    """Build a TRAINING_LEVEL (order filled in later)."""
    return {
        "title": title,
        "level_type": "TRAINING_LEVEL",
        "order": None,
        "estimated_duration": 10,
        "minimal_possible_solve_time": 1,
        "answer": answer,
        "answer_variable_name": None,
        "content": content,
        "solution": solution,
        "solution_penalized": True,
        "hints": [
            {"title": "Command", "content": cmd_hint, "hint_penalty": 10, "order": 0},
            {"title": "Where to read it", "content": where_hint, "hint_penalty": 20, "order": 1},
        ],
        "incorrect_answer_limit": 100,
        "attachments": [],
        "max_score": 50,
        "variant_answers": False,
        "reference_solution": [],
        "mitre_techniques": [{"technique_key": t} for t in (techniques or [])],
        "expected_commands": cmds or ["grep", "cat"],
        "commands_required": False,
    }


# --- 2.0.1 phishing-analysis levels ---------------------------------------
P = "/opt/ngsoc-artifacts/phishing"

phish_levels = [
    tl(
        MARKER,
        "nordik-bank-internal.example",
        f"The email lure is staged on **`analyst-host`** at `{P}/phishing-email.eml`. The sender is spoofed to look internal.\n\n**Host:** `analyst-host` (10.10.40.20) - right-click it -> Open console (log in as `analyst` / `ngsoc-analyst`).\n**Run:** `grep -i \"^From:\" {P}/phishing-email.eml`\n\n**Flag:** the **domain** of the spoofed sender address (the part after the `@`).",
        f"On `analyst-host`, run:\n\n`grep -i \"^From:\" {P}/phishing-email.eml`\n\nThe sender is `t.hauser@nordik-bank-internal.example`; the answer is **`nordik-bank-internal.example`**.",
        f"Open `analyst-host`'s console and run: `grep -i \"^From:\" {P}/phishing-email.eml`",
        "The domain after the @ in the From: header.",
        ["TA0001.T1566"],
    ),
    tl(
        "Phishing analysis - the malicious attachment",
        "Q4-wire-transfer-auth.docm",
        f"The static-analysis summary of the lure attachment is at `{P}/suspicious-attachment.txt` (no executable code - metadata only).\n\n**Host:** `analyst-host` (10.10.40.20) - right-click it -> Open console (log in as `analyst` / `ngsoc-analyst`).\n**Run:** `grep -i filename {P}/suspicious-attachment.txt`\n\n**Flag:** the **filename** of the macro-enabled attachment.",
        f"On `analyst-host`, run:\n\n`grep -i filename {P}/suspicious-attachment.txt`\n\nThe answer is **`Q4-wire-transfer-auth.docm`**.",
        f"Open `analyst-host`'s console and run: `grep -i filename {P}/suspicious-attachment.txt`",
        "The .docm filename in the metadata.",
        ["TA0001.T1566"],
    ),
    tl(
        "Phishing analysis - the smishing lure URL",
        "nordik-sec-verify.example",
        f"A second channel: an SMS (smishing) lure at `{P}/phishing-sms.txt` carries a link to a credential-harvesting page.\n\n**Host:** `analyst-host` (10.10.40.20) - right-click it -> Open console (log in as `analyst` / `ngsoc-analyst`).\n**Run:** `grep -o 'http://[^ ]*' {P}/phishing-sms.txt`\n\n**Flag:** the **domain** of the smishing link (between `http://` and the first `/`).",
        f"On `analyst-host`, run:\n\n`grep -o 'http://[^ ]*' {P}/phishing-sms.txt`\n\nThe link is `http://nordik-sec-verify.example/auth?token=BF-SIM-001`; the answer is **`nordik-sec-verify.example`**.",
        f"Open `analyst-host`'s console and run: `grep -o 'http://[^ ]*' {P}/phishing-sms.txt`",
        "The host part of the http:// link.",
        ["TA0001.T1566.004"],
    ),
    tl(
        "Phishing analysis - the vishing pretext",
        "vpn-portal.nordik-internal.example",
        f"A third channel: a voice-phishing (vishing) call script at `{P}/phishing-call-script.txt`. The caller directs the victim to a fake portal to read back a one-time code (real-time MFA bypass).\n\n**Host:** `analyst-host` (10.10.40.20) - right-click it -> Open console (log in as `analyst` / `ngsoc-analyst`).\n**Run:** `grep -i portal {P}/phishing-call-script.txt`\n\n**Flag:** the **fake VPN portal domain** the caller tells the victim to visit.",
        f"On `analyst-host`, run:\n\n`grep -i portal {P}/phishing-call-script.txt`\n\nThe answer is **`vpn-portal.nordik-internal.example`**.",
        f"Open `analyst-host`'s console and run: `grep -i portal {P}/phishing-call-script.txt`",
        "The vpn-portal.* address in the transcript.",
        ["TA0001.T1566.004", "TA0006.T1111"],
    ),
]

phish_assessment = {
    "title": "Practical 2.0.1 - Phishing Triage (Assessment)",
    "level_type": "ASSESSMENT_LEVEL",
    "order": None,
    "estimated_duration": 8,
    "minimal_possible_solve_time": None,
    "questions": [
        {
            "question_type": "MCQ",
            "text": "Across the three channels, which single indicator is common to the email, the SMS and the call?",
            "points": 50, "penalty": 0, "order": 0, "answer_required": True,
            "choices": [
                {"text": "A manufactured sense of urgency plus a request to act outside normal process", "correct": True, "order": 0},
                {"text": "A valid digital signature", "correct": False, "order": 1},
                {"text": "The victim's correct full account number", "correct": False, "order": 2},
                {"text": "A link to the genuine bank domain", "correct": False, "order": 3},
            ],
        },
        {
            "question_type": "MCQ",
            "text": "The vishing call asks the employee to read back a 6-digit code from a portal. This is:",
            "points": 50, "penalty": 0, "order": 1, "answer_required": True,
            "choices": [
                {"text": "Harmless - OTPs cannot be reused", "correct": False, "order": 0},
                {"text": "A real-time OTP relay attack that defeats MFA (T1111)", "correct": True, "order": 1},
                {"text": "A password reset", "correct": False, "order": 2},
            ],
        },
        {
            "question_type": "MCQ",
            "text": "A proportionate first response set for this multi-channel lure is:",
            "points": 50, "penalty": 0, "order": 2, "answer_required": True,
            "choices": [
                {"text": "Block the sender domain and lure URL, warn staff of the theme, and remind them IT never asks for OTPs", "correct": True, "order": 0},
                {"text": "Reset every employee password immediately with no notice", "correct": False, "order": 1},
                {"text": "Ignore it until a user actually clicks", "correct": False, "order": 2},
            ],
        },
        {
            "question_type": "FFQ",
            "text": "Which ATT&CK technique ID covers phishing delivered via SMS/service (smishing)? (Txxxx.xxx)",
            "points": 50, "penalty": 0, "order": 3, "answer_required": True,
            "choices": [{"text": "T1566.004", "correct": True, "order": 0}],
        },
    ],
    "instructions": "Answer as the SOC analyst producing the phishing triage note (D5.8 Activity 2.0.1): indicators across channels, intent, and a proportionate response set.",
    "assessment_type": "TEST",
}

# --- 2.0.2 coordination assessment ----------------------------------------
coord_assessment = {
    "title": "Practical 2.0.2 - Collaborative Response Chain (Assessment)",
    "level_type": "ASSESSMENT_LEVEL",
    "order": None,
    "estimated_duration": 8,
    "minimal_possible_solve_time": None,
    "questions": [
        {
            "question_type": "MCQ",
            "text": "When Legal, IT Operations and the CFO give conflicting instructions (preserve evidence vs. restore in 2 hours), the correct sequencing is:",
            "points": 50, "penalty": 0, "order": 0, "answer_required": True,
            "choices": [
                {"text": "Restore first to cut downtime, preserve evidence if time allows", "correct": False, "order": 0},
                {"text": "Preserve evidence, then contain, then rebuild from clean media", "correct": True, "order": 1},
                {"text": "Wait for the ransom deadline before deciding", "correct": False, "order": 2},
            ],
        },
        {
            "question_type": "MCQ",
            "text": "Which role owns the internal and external statements (including the holding line to a journalist)?",
            "points": 50, "penalty": 0, "order": 1, "answer_required": True,
            "choices": [
                {"text": "The SOC analyst", "correct": False, "order": 0},
                {"text": "The Communications / PR role, coordinating with Legal and the Incident Commander", "correct": True, "order": 1},
                {"text": "Whoever answers the phone", "correct": False, "order": 2},
                {"text": "The penetration tester", "correct": False, "order": 3},
            ],
        },
        {
            "question_type": "MCQ",
            "text": "A good decision log entry records, at minimum:",
            "points": 50, "penalty": 0, "order": 2, "answer_required": True,
            "choices": [
                {"text": "Time, decision, rationale, and who decided", "correct": True, "order": 0},
                {"text": "Only the final outcome", "correct": False, "order": 1},
                {"text": "Nothing - decisions are kept verbal for speed", "correct": False, "order": 2},
            ],
        },
        {
            "question_type": "MCQ",
            "text": "A SITREP for management should be:",
            "points": 50, "penalty": 0, "order": 3, "answer_required": True,
            "choices": [
                {"text": "A raw dump of every SIEM alert", "correct": False, "order": 0},
                {"text": "Concise: impact, actions taken, immediate next steps, and risks", "correct": True, "order": 1},
                {"text": "Withheld until the incident is fully closed", "correct": False, "order": 2},
            ],
        },
    ],
    "instructions": "Answer as the IR Coordinator running the collaborative response chain (D5.8 Activity 2.0.2): task allocation, decision logging, cross-role communication including Communications/PR.",
    "assessment_type": "TEST",
}

# --- Ex.4 red-team hands-on levels ----------------------------------------
FB = "/opt/ngsoc-artifacts/forensic-bundle"

ex4_levels = [
    tl(
        "Pen test - reconnaissance from Kali",
        "80",
        "Begin the engagement from **`kali`** (10.10.50.10). Scan the banking host to confirm the exposed service before you test the web app.\n\n**Host:** `kali` (10.10.50.10) - right-click it -> Open console (log in as `analyst` / `ngsoc-analyst`).\n**Run:** `nmap -Pn -p- 10.10.20.10`\n\n**Flag:** the **TCP port** on which the banking web application is served (digits only).",
        "On `kali`, run:\n\n`nmap -Pn 10.10.20.10`\n\nApache serves the app on **`80`**.",
        "Open `kali`'s console and run: `nmap -Pn 10.10.20.10`",
        "The open http port in the nmap output.",
        ["TA0007.T1046"],
        ["nmap"],
    ),
    tl(
        "Pen test - identify the SQL-injection tool from server evidence",
        "sqlmap",
        f"Threat-informed testing means understanding how the intrusion probed the login form. The Apache access log is in the forensic bundle on **`analyst-host`** at `{FB}/web-banking-access.log`. Find the automated tool that fired the `' OR '1'='1` and `UNION SELECT` probes at `/login.php`.\n\n**Host:** `analyst-host` (10.10.40.20) - right-click it -> Open console (log in as `analyst` / `ngsoc-analyst`).\n**Run:** `grep -i \"login.php\" {FB}/web-banking-access.log | grep -io 'sqlmap'`\n\n**Flag:** the **name of the tool** (as seen in the User-Agent) that performed the SQL-injection probes.\n\n> Having identified the technique from the evidence, reproduce it manually from `kali` against `http://10.10.20.10/login.php` (payload `' OR '1'='1'--`) and write the finding up in your pen-test report.",
        f"On `analyst-host`, run:\n\n`grep -i \"login.php\" {FB}/web-banking-access.log | grep -io 'sqlmap'`\n\nThe SQL-injection probes carry the `sqlmap/1.7.8` User-Agent; the answer is **`sqlmap`**.",
        f"Open `analyst-host`'s console and run: `grep -i sqlmap {FB}/web-banking-access.log`",
        "The User-Agent on the POST /login.php probe lines.",
        ["TA0001.T1190"],
        ["grep", "cat"],
    ),
]


def main():
    data = json.loads(V4.read_text(encoding="utf-8"))
    levels = data["levels"]

    if any(l.get("title") == MARKER for l in levels):
        print("Phase 3 already applied - nothing to do.")
        return 0

    by_title = {l["title"]: i for i, l in enumerate(levels)}

    def after(title, new):
        i = by_title[title]
        for off, lvl in enumerate(new, start=1):
            levels.insert(i + off, lvl)
        # rebuild index after each insertion batch
        by_title.clear()
        by_title.update({l["title"]: n for n, l in enumerate(levels)})

    # 2.0.1: four analysis levels after the practical INFO, assessment after the template locate
    after("Practical 2.0.1 - Multi-channel Spear-Phishing Simulation", phish_levels)
    after("Phishing triage - locate the triage-note template", [phish_assessment])
    # 2.0.2: coordination assessment after the SITREP-locate level
    after("Collaboration - locate the SITREP template", [coord_assessment])
    # Ex.4: two hands-on levels after the exercise INFO
    after("Exercise 4 - Proactive Security Testing (Penetration Tester)", ex4_levels)

    # renumber
    for n, lvl in enumerate(levels):
        lvl["order"] = n

    # 3.4 - fold NIS2 / GDPR / evidential questions into existing assessments
    def add_q(title, q):
        for lvl in levels:
            if lvl["title"] == title:
                q["order"] = len(lvl["questions"])
                lvl["questions"].append(q)
                return
        raise KeyError(title)

    add_q("Exercise 2 - Eradication & Forensic Fundamentals (Assessment)", {
        "question_type": "MCQ",
        "text": "Customer PII was accessed during this intrusion. Under GDPR Article 33, a notifiable personal-data breach must be reported to the supervisory authority within:",
        "points": 50, "penalty": 0, "answer_required": True,
        "choices": [
            {"text": "72 hours of becoming aware", "correct": True, "order": 0},
            {"text": "30 days", "correct": False, "order": 1},
            {"text": "Only after full remediation", "correct": False, "order": 2},
            {"text": "There is no deadline", "correct": False, "order": 3},
        ],
    })
    add_q("Exercise 5 - Tabletop Decisions & Plan Gaps (Assessment)", {
        "question_type": "MCQ",
        "text": "SecureBank is an essential entity under NIS2. The NIS2 early-warning to the CSIRT/competent authority is due within:",
        "points": 25, "penalty": 0, "answer_required": True,
        "choices": [
            {"text": "24 hours of becoming aware of the significant incident", "correct": True, "order": 0},
            {"text": "72 hours", "correct": False, "order": 1},
            {"text": "One week", "correct": False, "order": 2},
            {"text": "NIS2 has no reporting timeline", "correct": False, "order": 3},
        ],
    })
    add_q("Exercise 5 - Tabletop Decisions & Plan Gaps (Assessment)", {
        "question_type": "MCQ",
        "text": "Before wiping the compromised file-server, the Legal team requires evidence preservation. The correct action is to:",
        "points": 25, "penalty": 0, "answer_required": True,
        "choices": [
            {"text": "Image the disk with a write-blocker and record hashes before any rebuild", "correct": True, "order": 0},
            {"text": "Delete the logs to prevent leaks", "correct": False, "order": 1},
            {"text": "Rebuild first; evidence can be reconstructed later", "correct": False, "order": 2},
        ],
    })

    # refresh the roadmap table + counts on INFO level 0
    info0 = levels[0]
    tl_count = sum(1 for l in levels if l["level_type"] == "TRAINING_LEVEL")
    as_count = sum(1 for l in levels if l["level_type"] == "ASSESSMENT_LEVEL")
    n = len(levels)
    info0["content"] = (
        "# NG-SOC Learning Module 8 - Incident Response and Forensics (Sub Case 1a)\n\n"
        "Welcome to the instructor-led, cyber-range edition of **Learning Module 8**. "
        f"Over **{n} levels** ({tl_count} hands-on console tasks and {as_count} assessments) "
        "you will work the full incident-response lifecycle (NIST SP 800-61r2: "
        "*Preparation -> Detection & Analysis -> Containment, Eradication & Recovery -> Post-Incident*) "
        "across the five ECSF-aligned roles of the module. The exact level numbers appear in the "
        "level list on the left; each block is introduced by its own INFO level.\n\n"
        "| Block | Role (ECSF) |\n|---|---|\n"
        "| Overview & range access | - |\n"
        "| **Ex. 1** | SOC Analyst - Triage |\n"
        "| Practical 2.0.1 | Multi-channel spear-phishing (email / SMS / voice) |\n"
        "| Practical 2.0.2 | Collaborative response chain |\n"
        "| **Ex. 2** | Incident Responder - Containment/Eradication |\n"
        "| Practical 2.0.3 | Express forensic report |\n"
        "| **Ex. 3** | CTI Analyst - *Black Falcon* briefing |\n"
        "| **Ex. 4** | Penetration Tester - banking system |\n"
        "| **Ex. 5** | IR Coordinator - ransomware tabletop |\n"
        "| Wrap-up & debrief | - |\n\n"
        "**The scenario.** A financial institution running an online-banking platform is targeted by "
        "the fictitious **\"Black Falcon\"** campaign: spear-phishing -> trojan on a workstation -> "
        "C2 beacon -> lateral movement -> ransomware on the file server. Every artefact in this range "
        "is **synthetic and contained**.\n\n"
        "**How answers work.** Most levels are *console* tasks: you log into a sandbox host and use the "
        "tools provisioned by the range (Wazuh, `jq`, `grep`, `nmap`, `curl`, The Sleuth Kit, `strings`, "
        "MISP, Kali) to recover a **flag** - a real value present on the machines. Submit it exactly as shown.\n\n"
        "**Reference frameworks** used throughout: NIST SP 800-61r2, ENISA ECSF, MITRE ATT&CK, "
        "FIRST CSIRT Services Framework.\n\n"
        "> Tip: use the **Chrome** browser. If a submission misbehaves, log out and back in.\n"
    )

    # description count
    data["description"] = data["description"].replace(
        "39 levels (22 hands-on console tasks, 6 assessments)",
        f"{n} levels ({tl_count} hands-on console tasks, {as_count} assessments)",
    )
    data["estimated_duration"] = sum(l.get("estimated_duration") or 0 for l in levels)

    V4.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Phase 3 applied: {n} levels ({tl_count} training, {as_count} assessment).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
