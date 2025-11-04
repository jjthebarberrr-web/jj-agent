# Release Artifacts Collection

## Required Artifacts for v0.1.0 Release

Collect these artifacts after CI/CD completes and verification passes.

### 1. CI/CD Links

#### GitHub Release URL
```
https://github.com/ORG/jj-agent/releases/tag/v0.1.0
```

**To get:**
- Visit: https://github.com/ORG/jj-agent/releases
- Click on v0.1.0 release
- Copy URL

#### PyPI Package URL
```
https://pypi.org/project/jj-agent/0.1.0/
```

**To get:**
```bash
# Verify package exists
pip index versions jj-agent

# Visit in browser
# https://pypi.org/project/jj-agent/0.1.0/
```

#### Docker Image Digest
```bash
# Pull image
docker pull ghcr.io/ORG/jj-agent:v0.1.0

# Get digest
docker inspect ghcr.io/ORG/jj-agent:v0.1.0 | jq '.[0].RepoDigests'

# Or
docker inspect ghcr.io/ORG/jj-agent:v0.1.0 --format='{{index .RepoDigests 0}}'
```

**Expected format:**
```
ghcr.io/ORG/jj-agent:v0.1.0@sha256:abc123def456...
```

### 2. Verification Logs

#### Linux Verification Log
```bash
./verify_prod.sh | tee verify_prod_linux.log
```

**File:** `verify_prod_linux.log`

#### Windows Verification Log
```powershell
.\verify_prod.ps1 *>&1 | Tee-Object -FilePath verify_prod_windows.log
```

**File:** `verify_prod_windows.log`

### 3. Server Proof

#### Health Endpoints Output
```bash
curl -sS http://127.0.0.1:5858/healthz
curl -sS http://127.0.0.1:5858/readyz
```

**Expected:**
```json
{"status":"healthy","version":"0.1.0"}
{"status":"ready","version":"0.1.0"}
```

#### Systemd Status
```bash
sudo systemctl status jj-agent --no-pager
```

**Expected:** Service active and running

#### JSON Logs (20 lines)
```bash
journalctl -u jj-agent --since "10 min ago" -o json | jq '.' | head -20
```

**Expected:** Structured JSON with timestamp, level, message, job_id

#### Policy Proof (Denial Test)
```bash
# Attempt forbidden action
jj run "cat /etc/shadow" --workspace /tmp 2>&1 | tee denial_test.log

# Check audit log
cat state/*/audit.jsonl | jq 'select(.result.denied == true)' | head -5
```

**Expected:**
- Command fails with denial message
- Audit log contains denial entry with `"denied": true`

### 4. Production Smoke Test Results

```bash
export JJ_ENV=production
export OPENAI_API_KEY=sk-...

jj run "Create a FastAPI app with JWT auth and PostgreSQL" \
  --workspace ~/code/demo 2>&1 | tee smoke_test.log
```

**Expected:**
- Job completes successfully
- Files created in workspace
- Audit logs generated

### 5. Final Checklist

From `PRODUCTION_READY.md`:

- [ ] Production mode enforced
- [ ] Capabilities file required
- [ ] Sandboxing available
- [ ] Audit logging enabled
- [ ] Secrets redacted
- [ ] Metrics collected
- [ ] Health endpoints available
- [ ] CI/CD pipeline configured
- [ ] Documentation complete

## Artifact Collection Script

```bash
#!/bin/bash
# Collect all release artifacts

ARTIFACTS_DIR="release_artifacts_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$ARTIFACTS_DIR"

echo "Collecting release artifacts..."

# CI/CD Links
echo "GitHub Release: https://github.com/ORG/jj-agent/releases/tag/v0.1.0" > "$ARTIFACTS_DIR/ci_links.txt"
echo "PyPI: https://pypi.org/project/jj-agent/0.1.0/" >> "$ARTIFACTS_DIR/ci_links.txt"
docker inspect ghcr.io/ORG/jj-agent:v0.1.0 --format='{{index .RepoDigests 0}}' >> "$ARTIFACTS_DIR/ci_links.txt"

# Verification logs
cp verify_prod_linux.log "$ARTIFACTS_DIR/" 2>/dev/null || echo "Linux log not found"
cp verify_prod_windows.log "$ARTIFACTS_DIR/" 2>/dev/null || echo "Windows log not found"

# Health endpoints
curl -sS http://127.0.0.1:5858/healthz > "$ARTIFACTS_DIR/healthz.txt" 2>&1
curl -sS http://127.0.0.1:5858/readyz > "$ARTIFACTS_DIR/readyz.txt" 2>&1

# Systemd status
sudo systemctl status jj-agent --no-pager > "$ARTIFACTS_DIR/systemd_status.txt" 2>&1

# JSON logs
journalctl -u jj-agent --since "10 min ago" -o json | jq '.' | head -20 > "$ARTIFACTS_DIR/json_logs.txt" 2>&1

# Policy proof
cat state/*/audit.jsonl | jq 'select(.result.denied == true)' | head -5 > "$ARTIFACTS_DIR/policy_proof.txt" 2>&1

echo "Artifacts collected in: $ARTIFACTS_DIR"
ls -la "$ARTIFACTS_DIR"
```

## Submission Template

```
# v0.1.0 Release Artifacts

## CI/CD Links
- GitHub Release: [URL]
- PyPI Package: [URL]
- Docker Image: [digest]

## Verification Logs
- Linux: [verify_prod_linux.log]
- Windows: [verify_prod_windows.log]

## Server Proof
- Health endpoints: [output]
- Systemd status: [output]
- JSON logs: [20 lines]
- Policy proof: [denial test + audit entry]

## Production Smoke Test
- Result: [success/failure]
- Log: [smoke_test.log]

## Final Checklist
- [ ] All items checked
```

