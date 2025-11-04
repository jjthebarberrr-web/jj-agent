# v0.1.0 Release Artifacts - Submission Template

Fill in this template after completing all verification steps.

---

## 1. CI/CD Links

### GitHub Release URL
```
[Paste URL here]
Example: https://github.com/ORG/jj-agent/releases/tag/v0.1.0
```

### PyPI Package URL
```
[Paste URL here]
Example: https://pypi.org/project/jj-agent/0.1.0/
```

### GHCR Image Digest
```
[Paste digest here]
Example: ghcr.io/ORG/jj-agent:v0.1.0@sha256:abc123def456...
```

**How to get:**
```bash
docker pull ghcr.io/ORG/jj-agent:v0.1.0
docker inspect ghcr.io/ORG/jj-agent:v0.1.0 --format='{{index .RepoDigests 0}}'
```

---

## 2. Verification Logs

### Linux Verification Log
**File:** `verify_prod_linux.log`

**Contents or path:**
```
[Paste log contents or provide path]
```

### Windows Verification Log
**File:** `verify_prod_windows.log`

**Contents or path:**
```
[Paste log contents or provide path]
```

---

## 3. Server Proof

### Systemd Status (One Screen)
```
[Paste systemctl status jj-agent --no-pager output]
```

### Health Endpoint: /healthz
```
[Paste curl -sS http://127.0.0.1:5858/healthz output]
Expected: {"status":"healthy","version":"0.1.0"}
```

### Health Endpoint: /readyz
```
[Paste curl -sS http://127.0.0.1:5858/readyz output]
Expected: {"status":"ready","version":"0.1.0"}
```

### JSON Logs (Last 20 lines)
```
[Paste last 20 lines from journalctl -u jj-agent -o json]
```

---

## 4. Policy Proof

### Denial Test Output
```bash
# Command executed:
jj run "cat /etc/shadow" --workspace /tmp

# Output:
[Paste command output showing denial]
```

### Audit Log Entry
```json
[Paste audit.jsonl entry showing "denied": true]
```

---

## 5. Production Smoke Test

### Command Output
```bash
# Command executed:
export JJ_ENV=production
export OPENAI_API_KEY=sk-REDACTED
jj run "Create a FastAPI app with JWT auth and PostgreSQL" --workspace ~/code/demo

# Output:
[Paste full command output]
```

### Created Project Path
```bash
# Path: ~/code/demo

# Files:
[Paste ls -la ~/code/demo/ output]
```

---

## 6. GO_NOGO_CHECKLIST.md

### Status: ✅ GO / ❌ NO-GO

**All GO criteria passed:**
- [x] CI pipeline green
- [x] All artifacts present (Release, PyPI, GHCR)
- [x] Verification scripts pass (Linux & Windows)
- [x] Health endpoints OK
- [x] Audit logs present
- [x] Capabilities enforced
- [x] Smoke test completes without violations

**If NO-GO:** See `ROLLBACK_PROCEDURE.md`

---

## 7. Final Checklist

- [x] All CI/CD artifacts collected
- [x] Verification logs collected
- [x] Server proof collected
- [x] Policy proof collected
- [x] Smoke test results collected
- [x] GO_NOGO_CHECKLIST.md completed
- [x] Post-release tidy completed (version bump + roadmap PR)

---

## Submission

Once all artifacts are collected, submit this filled template.

**Status:** ⏳ Pending completion of all steps

