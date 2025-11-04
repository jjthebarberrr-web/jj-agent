# Go/No-Go Criteria for v0.1.0 Release

## ✅ GO Criteria (All Must Pass)

### CI/CD Pipeline
- [ ] **CI pipeline green** - All jobs pass (lint, test, build, docker, pypi)
- [ ] **GitHub Release created** - Release exists at https://github.com/ORG/jj-agent/releases/tag/v0.1.0
- [ ] **PyPI package published** - Package available at https://pypi.org/project/jj-agent/0.1.0/
- [ ] **GHCR image published** - Image available at ghcr.io/ORG/jj-agent:v0.1.0 with digest

### Verification Scripts
- [ ] **Linux verification passes** - `verify_prod_linux.log` shows all checks passed
- [ ] **Windows verification passes** - `verify_prod_windows.log` shows all checks passed
- [ ] **No critical errors** - All failures are warnings only

### Server Deployment
- [ ] **Health endpoints OK** - `/healthz` returns `{"status":"healthy","version":"0.1.0"}`
- [ ] **Readiness endpoint OK** - `/readyz` returns `{"status":"ready","version":"0.1.0"}`
- [ ] **Audit logs present** - `state/<job-id>/audit.jsonl` files exist
- [ ] **JSON logs structured** - `journalctl -u jj-agent -o json` shows valid JSON
- [ ] **Systemd service running** - `systemctl status jj-agent` shows active (running)

### Security & Capabilities
- [ ] **Capabilities enforced** - Forbidden paths/commands are blocked
- [ ] **Policy proof exists** - Denial test shows blocked action + audit entry
- [ ] **No policy violations** - All operations respect capabilities

### Production Smoke Test
- [ ] **Smoke test completes** - Job finishes without errors
- [ ] **Files created** - Project folder contains expected files
- [ ] **No forbidden operations** - All actions allowed by capabilities

## ❌ NO-GO Criteria (Any Failure Triggers Rollback)

### CI/CD Failures
- [ ] CI pipeline fails any job
- [ ] GitHub Release not created
- [ ] PyPI package not published
- [ ] GHCR image not published or inaccessible

### Verification Failures
- [ ] Linux verification script fails
- [ ] Windows verification script fails
- [ ] Critical errors in verification logs

### Server Failures
- [ ] Health endpoints fail or return errors
- [ ] Audit logs not generated
- [ ] JSON logs malformed
- [ ] Systemd service fails to start

### Security Failures
- [ ] Capabilities not enforced
- [ ] Forbidden paths/commands allowed
- [ ] Policy violations detected
- [ ] Audit trail missing

### Smoke Test Failures
- [ ] Smoke test fails to complete
- [ ] Job errors or crashes
- [ ] Files not created correctly
- [ ] Policy violations during execution

## Decision Matrix

| Condition | Status | Action |
|-----------|--------|--------|
| All GO criteria pass | ✅ GO | Proceed with release |
| Any NO-GO criteria fail | ❌ NO-GO | Execute rollback procedure |

## Verification Commands

### Check CI/CD Status
```bash
gh run list --workflow=release
gh run view <run-id>
```

### Check Artifacts
```bash
# GitHub Release
gh release view v0.1.0

# PyPI
pip index versions jj-agent

# Docker
docker pull ghcr.io/ORG/jj-agent:v0.1.0
docker inspect ghcr.io/ORG/jj-agent:v0.1.0 --format='{{index .RepoDigests 0}}'
```

### Check Verification
```bash
# Linux
cat verify_prod_linux.log | grep -E "✓|✗|⚠"

# Windows
Get-Content verify_prod_windows.log | Select-String "✓|✗|⚠"
```

### Check Server
```bash
curl -sS http://127.0.0.1:5858/healthz | jq
curl -sS http://127.0.0.1:5858/readyz | jq
sudo systemctl status jj-agent --no-pager
journalctl -u jj-agent -n 20 -o json | jq '.' | head -20
```

### Check Capabilities
```bash
# This should fail with denial
jj run "cat /etc/shadow" --workspace /tmp 2>&1
cat state/*/audit.jsonl | jq 'select(.result.denied == true)' | head -5
```

## Final Decision

After all checks:
- **If all GO criteria pass:** ✅ **GO** - Release approved
- **If any NO-GO criteria fail:** ❌ **NO-GO** - Execute rollback

See `ROLLBACK_PROCEDURE.md` for rollback steps.

