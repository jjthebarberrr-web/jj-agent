# v0.1.0 Release Artifacts Template

## Collection Status: ⏳ Pending CI/CD Completion

**Note:** This template will be populated after CI/CD completes and verification runs.

---

## 1. CI/CD Links

### GitHub Release URL
```
https://github.com/ORG/jj-agent/releases/tag/v0.1.0
```
**Status:** ⏳ Pending CI/CD completion

### PyPI Package URL
```
https://pypi.org/project/jj-agent/0.1.0/
```
**Status:** ⏳ Pending CI/CD completion

### Docker Image + Digest
```bash
# After CI/CD completes:
docker pull ghcr.io/ORG/jj-agent:v0.1.0
docker inspect ghcr.io/ORG/jj-agent:v0.1.0 --format='{{index .RepoDigests 0}}'
```
**Expected format:**
```
ghcr.io/ORG/jj-agent:v0.1.0@sha256:abc123def456...
```
**Status:** ⏳ Pending CI/CD completion

---

## 2. Verification Logs

### Linux Verification Log
**File:** `verify_prod_linux.log`

**To generate after CI/CD:**
```bash
pipx install "jj-agent==0.1.0"
chmod +x verify_prod.sh
./verify_prod.sh | tee verify_prod_linux.log
```

**Status:** ⏳ Pending execution

### Windows Verification Log
**File:** `verify_prod_windows.log`

**To generate after CI/CD:**
```powershell
pipx install "jj-agent==0.1.0"
.\verify_prod.ps1 *>&1 | Tee-Object -FilePath verify_prod_windows.log
```

**Status:** ⏳ Pending execution

---

## 3. Server Proof

### Systemd Status
```bash
sudo systemctl status jj-agent --no-pager
```

**Expected output:**
```
● jj-agent.service - JJ Agent Service
     Loaded: loaded (/etc/systemd/system/jj-agent.service; enabled; preset: enabled)
     Active: active (running) since ...
     Main PID: 12345 (python)
     ...
```

**Status:** ⏳ Pending server deployment

### Health Endpoints

**/healthz:**
```bash
curl -sS http://127.0.0.1:5858/healthz
```

**Expected:**
```json
{"status":"healthy","version":"0.1.0"}
```

**/readyz:**
```bash
curl -sS http://127.0.0.1:5858/readyz
```

**Expected:**
```json
{"status":"ready","version":"0.1.0"}
```

**Status:** ⏳ Pending server deployment

### JSON Logs (Last 20 lines)
```bash
journalctl -u jj-agent -n 50 -o json | jq '.' | tail -20
```

**Expected format:**
```json
{
  "timestamp": "2024-11-03T...",
  "level": "INFO",
  "message": "...",
  "job_id": "...",
  ...
}
```

**Status:** ⏳ Pending server deployment

---

## 4. Policy Proof

### Denial Test
```bash
# Attempt forbidden action
jj run "cat /etc/shadow" --workspace /tmp 2>&1 | tee denial_test.log

# Check audit log for denial
cat state/*/audit.jsonl | jq 'select(.result.denied == true)' | head -5
```

**Expected:**
- Command fails with denial message
- Audit log contains entry with `"denied": true`

**Status:** ⏳ Pending execution

---

## 5. Production Smoke Test

### Command
```bash
export JJ_ENV=production
export OPENAI_API_KEY=sk-REDACTED
jj run "Create a FastAPI app with JWT auth and PostgreSQL" --workspace ~/code/demo
```

### Output
**Status:** ⏳ Pending execution

### Resulting Project Folder
```bash
ls -la ~/code/demo/
```

**Expected files:**
- `main.py`
- `requirements.txt`
- `docker-compose.yml`
- `test_main.py`
- `README.md`

**Status:** ⏳ Pending execution

---

## 6. PRODUCTION_READY.md Checklist

### ✅ Completed Features

- [x] Production mode with strict enforcement
- [x] Security sandboxing (LocalSafe + Docker)
- [x] Production capabilities system
- [x] Structured JSON logging
- [x] Audit trail logging
- [x] Metrics collection
- [x] Error monitoring integration
- [x] Health endpoints
- [x] Systemd service
- [x] Docker image
- [x] CI/CD automation

### ✅ Documentation
- [x] README.md (updated)
- [x] SECURITY.md
- [x] OPERATIONS.md
- [x] CHANGELOG.md
- [x] ROADMAP.md
- [x] RELEASE_NOTES.md

### ✅ Testing
- [x] Unit tests
- [x] E2E smoke tests
- [x] Security tests

**Status:** ✅ All items completed

---

## Next Steps

1. ⏳ Wait for CI/CD to complete (5-10 minutes)
2. ⏳ Run verification scripts (B)
3. ⏳ Deploy to server (C)
4. ⏳ Run production smoke test (D)
5. ⏳ Collect all artifacts (E)
6. ✅ Post-release tidy (F) - Scripts ready

---

**Last Updated:** Release execution started  
**Next Update:** After CI/CD completion

