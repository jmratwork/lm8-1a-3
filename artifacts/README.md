# artifacts/ — mirror, not source

**Do not edit the files in this directory.** They are a read-only mirror of the
artefacts the sandbox actually deploys.

| | |
|---|---|
| **Source of truth** | `provisioning/roles/artifacts/files/` |
| **This directory** | mirror, for reading the artefacts without walking the Ansible tree |
| **Deployed to** | `/opt/ngsoc-artifacts/` on `analyst-host`, `db-server` and `kali` |

## Why this note exists

These two trees silently drifted apart. The mirror still described the incident
as *"Operation Black Friday"* in June 2026, while the sandbox deployed
*"Operation Locked Ledger"* in November 2025 — different codename, different
dates, different alert bundle. Anyone reviewing the module against this
directory drew conclusions that did not hold in the running range.

Both trees were re-synchronised from `provisioning/` on 2026-08-23. The previous
mirror contents remain in git history.

## Re-syncing

After changing anything under `provisioning/roles/artifacts/files/`:

```bash
cd provisioning/roles/artifacts/files
find . -type f -exec cp --parents {} ../../../../artifacts/ \;
```

`tools/validate-training.py` reports any drift between the two trees as a
warning, so a stale mirror shows up on the next validation run.
