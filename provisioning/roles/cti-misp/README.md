# Role: cti-misp

Deploys MISP (Malware Information Sharing Platform) on the CTI host via Docker Compose,
then seeds it with Black Falcon campaign IoCs for Exercise 3.

## Docker Hub rate limiting

The compose file pulls `mariadb:10.11` and `redis:7-alpine` from Docker Hub.
Anonymous pulls are rate-limited to ~100 pulls / 6 h per IP (as of 2025).
In a classroom or cloud environment where multiple sandboxes share an egress IP this
limit is hit quickly, causing the `Start MISP containers` task to fail with:

```
toomanyrequests: You have reached your pull rate limit.
```

### Option A — Docker Hub authenticated pull (recommended for production deployments)

Log in to Docker Hub before running the role.  Add a pre-task to the play or run
manually on the CTI host:

```bash
docker login -u <dockerhub_user> -p <dockerhub_token>
```

Authenticated free-tier accounts receive 200 pulls / 6 h per account.

To automate this via Ansible, the following vars and task block can be added to
this role **before** the "Start MISP containers" task.  These changes are **not
applied** in the current codebase — they are shown here as a safe opt-in extension:

```yaml
# In group_vars/all.yml or host_vars/cti-host.yml (vault the credentials):
# docker_registry_user: ""      # set to Docker Hub username to enable
# docker_registry_token: ""     # Docker Hub personal access token (PAT)

# --- PROPOSED TASK (not applied) ---
# - name: Authenticate to Docker Hub (optional, avoids rate limits)
#   community.docker.docker_login:
#     username: "{{ docker_registry_user }}"
#     password: "{{ docker_registry_token }}"
#   when:
#     - docker_registry_user is defined
#     - docker_registry_user | length > 0
#   no_log: true
```

### Option B — Internal registry mirror

If your KYPO cloud has a registry mirror or cache (e.g. Harbor, Nexus, AWS ECR pull-
through cache), override the image references by setting these vars before the role
runs and templating them into the compose file.  This requires changes to
`tasks/main.yml` to replace hardcoded image names with variables — not done here to
keep the role self-contained.

### Option C — Pre-pull images into a custom base image

Build a custom base image that already contains the required layers and push it to
a registry accessible from the sandbox network.  Update the compose `image:` fields
to point to the custom image.  No Ansible change is needed beyond updating the image
references.

## Post-deploy: seeding IoCs

After MISP is up, run the seed script manually (API key required — see
`/opt/misp-docker/README-SEED.md` on the CTI host).

## Dependencies

- Docker engine (`docker.io`, `docker-compose`, `python3-docker`) — installed by this role
- Network access to `ghcr.io` (MISP image) and Docker Hub (`mariadb`, `redis`)
- `standard.large` flavour recommended (MariaDB + Redis + PHP-FPM + nginx)
