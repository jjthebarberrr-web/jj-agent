# v0.1.0 Release - Complete Execution Guide

## Status: ✅ READY TO EXECUTE

All preflight checks passed. Execute the release process step by step.

---

## Step 1: Trigger Release

### Option A: Automated Script
```bash
cd jj-agent
chmod +x EXECUTE_RELEASE_FINAL.sh
./EXECUTE_RELEASE_FINAL.sh
```

### Option B: Manual Push
```bash
cd jj-agent
git push origin v0.1.0
```

**Expected:**
- Tag pushed successfully
- CI/CD triggered
- Monitor at: https://github.com/ORG/jj-agent/actions

**Duration:** 5-10 minutes for CI/CD to complete

---

## Step 2: Verification (After CI/CD)

### Linux/macOS
```bash
pipx install "jj-agent==0.1.0"
chmod +x verify_prod.sh
./verify_prod.sh | tee verify_prod_linux.log
```

**Collect:** `verify_prod_linux.log`

### Windows PowerShell
```powershell
pipx install "jj-agent==0.1.0"
.\verify_prod.ps1 *>&1 | Tee-Object -FilePath verify_prod_windows.log
```

**Collect:** `verify_prod_windows.log`

---

## Step 3: Server Deployment

**Follow RELEASE_EXECUTION.md Section C exactly:**

```bash
# Create user
sudo useradd -r -s /usr/sbin/nologin jj || true

# Create directories
sudo mkdir -p /etc/jj-agent /var/log/jj
sudo chown jj:jj /var/log/jj

# Copy capabilities
sudo cp capabilities.prod.yaml /etc/jj-agent/

# Create environment file
printf "JJ_ENV=production\nTZ=America/Phoenix\n" | sudo tee /etc/jj-agent/jj.env

# Install agent
pipx install "jj-agent==0.1.0"

# Install service
sudo cp jj-agent.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now jj-agent

# Verify
curl -sS http://127.0.0.1:5858/healthz
curl -sS http://127.0.0.1:5858/readyz
journalctl -u jj-agent -n 30 -o json
```

**Collect:**
- Systemd status: `sudo systemctl status jj-agent --no-pager`
- Health endpoints: `/healthz` and `/readyz` outputs
- JSON logs: Last 20 lines from `journalctl -u jj-agent -o json`

---

## Step 4: Production Smoke Test

```bash
export JJ_ENV=production
export JJ_PROD_STRICT=1
export OPENAI_API_KEY=sk-YOUR-KEY

jj run "Create a FastAPI app with JWT auth and PostgreSQL" --workspace ~/code/demo
```

**Verify:**
- Job completes successfully
- No policy violations
- Files created in `~/code/demo`

**Collect:**
- Command output
- Project folder listing: `ls -la ~/code/demo/`

---

## Step 5: Policy Proof

```bash
# Attempt forbidden action (should fail)
jj run "cat /etc/shadow" --workspace /tmp 2>&1

# Check audit log for denial
cat state/*/audit.jsonl | jq 'select(.result.denied == true)' | head -5
```

**Collect:**
- Denial command output
- Audit log entry showing `"denied": true`

---

## Step 6: Collect Artifacts

### Automated Collection
```bash
chmod +x COLLECT_ARTIFACTS.sh
./COLLECT_ARTIFACTS.sh
```

### Manual Collection

**CI/CD Links:**
- GitHub Release: https://github.com/ORG/jj-agent/releases/tag/v0.1.0
- PyPI: https://pypi.org/project/jj-agent/0.1.0/
- Docker Digest: `docker inspect ghcr.io/ORG/jj-agent:v0.1.0 --format='{{index .RepoDigests 0}}'`

**Verification Logs:**
- `verify_prod_linux.log`
- `verify_prod_windows.log`

**Server Proof:**
- Systemd status (one screen)
- `/healthz` output
- `/readyz` output
- Last 20 JSON log lines

**Policy Proof:**
- Denial test output
- Audit log entry

**Smoke Test:**
- Command output
- Project folder path

**Checklist:**
- Mark `GO_NOGO_CHECKLIST.md` as complete

---

## Step 7: Post-Release Tidy

### Version Bump
```bash
cd jj-agent
chmod +x POST_RELEASE_TIDY.sh
./POST_RELEASE_TIDY.sh
git commit -am "Bump version to 0.1.1-dev"
git push origin master
```

### Create Roadmap PR
```bash
chmod +x CREATE_ROADMAP_PR.sh
./CREATE_ROADMAP_PR.sh
git push -u origin feature/v0.2.0-roadmap
gh pr create --title "v0.2.0 Roadmap" --body-file v0.2.0_ROADMAP_PR.md
```

---

## Go/No-Go Decision

After all steps, check `GO_NOGO_CHECKLIST.md`:

**✅ GO if:**
- CI pipeline green
- All artifacts present (Release, PyPI, GHCR)
- Verification scripts pass
- Health endpoints OK
- Audit logs present
- Capabilities enforced
- Smoke test completes without violations

**❌ NO-GO if any fail:**
- Execute `ROLLBACK_PROCEDURE.md`

---

## Artifact Submission Template

Use `ARTIFACTS_COLLECTION_FINAL.md` template:

```
# v0.1.0 Release Artifacts

## CI/CD Links
- GitHub Release: [URL]
- PyPI: [URL]
- GHCR Image: [digest]

## Verification Logs
- Linux: [log contents/path]
- Windows: [log contents/path]

## Server Proof
- Systemd Status: [output]
- /healthz: [output]
- /readyz: [output]
- JSON Logs: [last 20 lines]

## Policy Proof
- Denial Test: [output + audit entry]

## Smoke Test
- Output: [command output]
- Project Path: [path and files]

## Checklist
- [x] GO_NOGO_CHECKLIST.md completed
- [x] All GO criteria passed
```

---

## Quick Reference

**Execute:**
- `./EXECUTE_RELEASE_FINAL.sh` - Push tag

**After CI/CD:**
- `./verify_prod.sh` - Linux verification
- `.\verify_prod.ps1` - Windows verification

**Collect:**
- `./COLLECT_ARTIFACTS.sh` - Automated collection

**Post-Release:**
- `./POST_RELEASE_TIDY.sh` - Version bump
- `./CREATE_ROADMAP_PR.sh` - Roadmap PR

---

**Status:** ✅ READY  
**Action:** Execute Step 1 now

