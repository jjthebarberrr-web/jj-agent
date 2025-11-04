# v0.1.0 Release Artifacts - Collection Template

## Status: ⏳ Pending CI/CD Completion

After executing all steps, collect these artifacts and return them.

---

## 1. CI/CD Links

### GitHub Release URL
```
https://github.com/ORG/jj-agent/releases/tag/v0.1.0
```
**How to get:**
- Visit: https://github.com/ORG/jj-agent/releases
- Click on v0.1.0
- Copy URL

**Status:** ⏳ Pending CI/CD

### PyPI Package URL
```
https://pypi.org/project/jj-agent/0.1.0/
```
**How to get:**
```bash
pip index versions jj-agent
# Should show: jj-agent (0.1.0)
```

**Status:** ⏳ Pending CI/CD

### GHCR Image Digest
```bash
docker pull ghcr.io/ORG/jj-agent:v0.1.0
docker inspect ghcr.io/ORG/jj-agent:v0.1.0 --format='{{index .RepoDigests 0}}'
```

**Expected format:**
```
ghcr.io/ORG/jj-agent:v0.1.0@sha256:abc123def456...
```

**Status:** ⏳ Pending CI/CD

---

## 2. Verification Logs

### Linux Verification Log
**File:** `verify_prod_linux.log`

**Command:**
```bash
pipx install "jj-agent==0.1.0"
chmod +x verify_prod.sh
./verify_prod.sh | tee verify_prod_linux.log
```

**Status:** ⏳ Pending execution

### Windows Verification Log
**File:** `verify_prod_windows.log`

**Command:**
```powershell
pipx install "jj-agent==0.1.0"
.\verify_prod.ps1 *>&1 | Tee-Object -FilePath verify_prod_windows.log
```

**Status:** ⏳ Pending execution

---

## 3. Server Proof

### Systemd Status (One Screen)
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
journalctl -u jj-agent -n 30 -o json | jq '.' | tail -20
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
jj run "cat /etc/shadow" --workspace /tmp 2>&1

# Check audit log
cat state/*/audit.jsonl | jq 'select(.result.denied == true)' | head -5
```

**Expected:**
- Command fails with denial message
- Audit log contains entry with `"denied": true`

**Status:** ⏳ Pending execution

---

## 5. Production Smoke Test

### Command Output
```bash
export JJ_ENV=production
export OPENAI_API_KEY=sk-REDACTED
jj run "Create a FastAPI app with JWT auth and PostgreSQL" --workspace ~/code/demo
```

**Collect:** Full command output

**Status:** ⏳ Pending execution

### Created Project Path
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

## 6. FINAL_CHECKLIST.md

Mark all items as complete in `FINAL_CHECKLIST.md`:

- [x] Pre-Release: All complete
- [ ] Step 1: Tag pushed
- [ ] Step 2: Verification complete
- [ ] Step 3: Server deployed
- [ ] Step 4: Smoke test passed
- [ ] Step 5: Artifacts collected
- [ ] Step 6: Post-release tidy

---

## Submission Format

When all artifacts are collected, submit in this format:

```
# v0.1.0 Release Artifacts

## CI/CD Links
- GitHub Release: [URL]
- PyPI: [URL]
- GHCR Image: [digest]

## Verification Logs
- Linux: [verify_prod_linux.log contents or path]
- Windows: [verify_prod_windows.log contents or path]

## Server Proof
- Systemd Status: [output]
- /healthz: [output]
- /readyz: [output]
- JSON Logs: [last 20 lines]

## Policy Proof
- Denial Test: [command output + audit entry]

## Smoke Test
- Output: [command output]
- Project Path: [path and file listing]

## Checklist
- [x] FINAL_CHECKLIST.md completed
- [x] All GO criteria passed
```

---

**Last Updated:** Release execution started  
**Next Update:** After CI/CD completion

