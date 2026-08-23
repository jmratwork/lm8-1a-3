#!/usr/bin/env python3
"""
validate-training.py - NG-SOC LM8 Sub Case 1a

Validates a CyberRangeCZ/KYPO training definition against what the sandbox
ACTUALLY deploys.

Critical distinction this tool enforces:
  provisioning/roles/artifacts/files/  -> what Ansible copies onto the hosts
  artifacts/                           -> repo-level documentation copy

Only the first is authoritative. Checking answers against artifacts/ produces
false results whenever the two have drifted apart.

For every TRAINING_LEVEL the tool checks:
  1. the file path named in the level resolves to a deployed source
  2. the grep/search pattern in the "Run:" command exists in that source
  3. the expected answer exists in that source

Usage:
    python tools/validate-training.py V4_ngsoc-lm8-subcase1a-training.json
"""

import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# Sandbox path -> repo source(s) that provision it.
# Ordered: first match wins.
PATH_MAP = [
    (r"^/opt/ngsoc-artifacts/(.+)$", "provisioning/roles/artifacts/files/{0}"),
    (r"^/opt/ngsoc-alerts/", "provisioning/roles/siem/tasks/main.yml"),
    (r"^/var/ossec/etc/rules/", "provisioning/roles/siem/tasks/main.yml"),
    (r"^/srv/data/", "provisioning/roles/file-server/tasks/main.yml"),
    (r"^/home/analyst/handouts/", "provisioning/roles/artifacts/tasks/main.yml"),
    (r"^/home/analyst/reports/", "provisioning/roles/forensics-host/tasks/main.yml"),
    (r"^/tmp/\.svc_update", "provisioning/roles/employee-ws/tasks/main.yml"),
    (r"^/etc/cron\.d/", "provisioning/roles/employee-ws/tasks/main.yml"),
    (r"^/opt/c2-beacon/", "provisioning/roles/employee-ws/tasks/main.yml"),
    (r"^/var/www/html/banking/", "provisioning/roles/web-banking-vuln/tasks/main.yml"),
]

# Levels whose answer is derived (counted, computed, read from topology) rather
# than present verbatim in a provisioning file. Checked as WARN, not FAIL.
DERIVED_ANSWERS = {
    "10",            # count of .locked files
    "10.10.30.10",   # patient zero, read via `hostname -I`
    "backup",        # directory name
}


def deployed_sources(text, fallback=True):
    """Resolve every sandbox path mentioned in a level to repo source files.

    Falls back to the whole provisioning tree when a level names no path
    (e.g. levels answered with `hostname -I`).
    """
    out = []
    for raw in re.findall(r"(/[\w./\-]+|http://[\d.]+/[\w./\-]*)", text):
        path = raw
        if path.startswith("http://"):
            # web-banking served content
            out.append(REPO / "provisioning/roles/web-banking-vuln")
            continue
        for pattern, target in PATH_MAP:
            m = re.match(pattern, path)
            if m:
                tgt = target.format(*m.groups()) if m.groups() else target
                p = REPO / tgt
                if p.exists():
                    out.append(p)
                break
    if not out and fallback:
        out.append(REPO / "provisioning")
    return out


def read(p):
    """Concatenate a source. For directories, include the file NAMES too -
    levels answered with `ls` expect a filename, not file content."""
    if p.is_dir():
        buf = []
        for f in sorted(p.rglob("*")):
            if f.is_file():
                buf.append(f.name)
                try:
                    buf.append(f.read_text(encoding="utf-8", errors="replace"))
                except OSError:
                    pass
        return "\n".join(buf)
    try:
        return p.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def run_pattern(content):
    """Extract the search pattern from the level's `Run:` command.

    Returns (cmd, pattern, ignore_case). The pattern is treated as a regex,
    so `grep -o '"dstip":"[^"]*"'` is matched as written rather than
    literally, and `grep -i` maps to a case-insensitive search.
    """
    m = re.search(r"\*\*Run:\*\*\s*`([^`]+)`", content)
    if not m:
        return None, None, False
    cmd = m.group(1)
    ignore_case = bool(re.search(r"grep\s+(?:-\w*\s+)*-\w*i", cmd))
    # a single-quoted argument may itself contain double quotes, so try it first
    q = re.search(r"grep(?:\s+-\w+)*\s+'([^']+)'", cmd) or \
        re.search(r'grep(?:\s+-\w+)*\s+"([^"]+)"', cmd)
    if q:
        return cmd, q.group(1), ignore_case
    g = re.search(r"grep(?:\s+-\w+)*\s+(\S+)", cmd)
    if g and not g.group(1).startswith("/"):
        return cmd, g.group(1).strip("'\""), ignore_case
    return cmd, None, ignore_case


def found(pattern, blob, ignore_case):
    """Match `pattern` against `blob` as a regex, falling back to literal."""
    flags = re.MULTILINE | (re.IGNORECASE if ignore_case else 0)
    try:
        if re.search(pattern, blob, flags):
            return True
    except re.error:
        pass
    hay = blob.lower() if ignore_case else blob
    needle = pattern.lower() if ignore_case else pattern
    return needle in hay


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    training = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))

    fails, warns, oks = [], [], []
    orders = []

    for lvl in training["levels"]:
        orders.append(lvl.get("order"))
        if lvl.get("level_type") != "TRAINING_LEVEL":
            continue

        title = lvl.get("title", "?")
        order = lvl.get("order")
        answer = lvl.get("answer", "")
        content = lvl.get("content", "")

        srcs = deployed_sources(content + "\n" + lvl.get("solution", ""))
        label = f"L{order:>2} {title[:52]}"

        if not srcs:
            warns.append(f"{label}: no deployed source resolved from the level text")
            continue

        blob = "\n".join(read(s) for s in srcs)
        cmd, pattern, ignore_case = run_pattern(content)

        if pattern and not found(pattern, blob, ignore_case):
            fails.append(
                f"{label}: search pattern {pattern!r} NOT FOUND in "
                f"{', '.join(str(s.relative_to(REPO)) for s in srcs)}"
            )
            continue

        if answer and answer not in blob:
            if answer in DERIVED_ANSWERS:
                warns.append(f"{label}: answer {answer!r} is derived (not literal) - review by hand")
            else:
                fails.append(
                    f"{label}: answer {answer!r} NOT FOUND in "
                    f"{', '.join(str(s.relative_to(REPO)) for s in srcs)}"
                )
            continue

        oks.append(label)

    # --- structural checks -------------------------------------------------
    struct = []
    n = len(training["levels"])
    if orders != sorted(orders) or orders != list(range(n)):
        struct.append(f"level `order` values are not a contiguous 0..{n-1} sequence")
    for field in ("title", "description", "state"):
        if field not in training:
            struct.append(f"missing top-level field: {field}")
    declared = re.findall(r"(\d+)\s+(?:console-based\s+)?levels", training.get("description", ""))
    declared += re.findall(r"Over \*\*(\d+) levels\*\*", training["levels"][0].get("content", ""))
    for d in set(declared):
        if int(d) != n:
            struct.append(f"text declares {d} levels but the file contains {n}")

    # drift between the two artefact trees
    drift = []
    docs = REPO / "artifacts"
    dep = REPO / "provisioning/roles/artifacts/files"
    for f in sorted(docs.rglob("*")):
        if f.is_file():
            twin = dep / f.relative_to(docs)
            if twin.exists() and read(f).strip() != read(twin).strip():
                drift.append(str(f.relative_to(REPO)))

    # --- report ------------------------------------------------------------
    print(f"\n  Training : {training['title']}")
    print(f"  Levels   : {n}  ({len(oks)+len(warns)+len(fails)} flags checked)\n")

    for f in fails:
        print(f"  FAIL  {f}")
    for w in warns:
        print(f"  WARN  {w}")
    for o in oks:
        print(f"  ok    {o}")

    if struct:
        print("\n  Structural:")
        for s in struct:
            print(f"  FAIL  {s}")

    if drift:
        print("\n  Artefact drift (artifacts/ differs from what is deployed):")
        for d in drift:
            print(f"  WARN  {d}")

    print(f"\n  {len(oks)} ok, {len(warns)} warn, {len(fails)+len(struct)} fail\n")
    return 1 if (fails or struct) else 0


if __name__ == "__main__":
    sys.exit(main())
