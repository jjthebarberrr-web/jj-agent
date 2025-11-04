# v0.1.0 Release - Step-by-Step Execution

## Current Status: ✅ READY

- ✅ Preflight: PASSED
- ✅ Tag: v0.1.0 exists
- ✅ Scripts: Ready
- ✅ Documentation: Complete
- ⚠️ Remote: Needs configuration

---

## Step 1: Configure Remote and Push Tag

### Option A: Use Helper Script
```bash
cd jj-agent
chmod +x CONFIGURE_AND_PUSH.sh
./CONFIGURE_AND_PUSH.sh https://github.com/YOUR-ORG/jj-agent.git
```

### Option B: Manual
```bash
cd jj-agent

# Configure remote
git remote add origin https://github.com/YOUR-ORG/jj-agent.git

# Verify
git remote -v

# Push tag
git push origin v0.1.0
```

**Expected:**
- Tag pushed successfully
- CI/CD triggered
- Monitor at: https://github.com/YOUR-ORG/jj-agent/actions

**Duration:** 5-10 minutes for CI/CD

---

## Step 2: Verification (After CI/CD) 🔍

### Linux/macOS
```bash
pipx install "jj-agent==0.1.0"
chmod +x verify_prod.sh
./verify_prod.sh | tee verify_prod_linux.log
```

### Windows PowerShell
```powershell
pipx install "jj-agent==0.1.0"
.\verify_prod.ps1 *>&1 | Tee-Object -FilePath verify_prod_windows.log
```

**Collect:** Both log files

---

## Step 3: Server Deployment 🖥️

**From EXECUTE_NOW_FINAL.md Section 3:**

```bash
sudo useradd -r -s /usr/sbin/nologin jj || true
sudo mkdir -p /etc/jj-agent /var/log/jj
sudo cp capabilities.prod.yaml /etc/jj-agent/
printf "JJ_ENV=production\nTZ=America/Phoenix\n" | sudo tee /etc/jj-agent/jj.env
pipx install "jj-agent==0.1.0"
sudo cp jj-agent.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now jj-agent

# Health checks
curl -sS http://127.0.0.1:5858/healthz
curl -sS http://127.0.0.1:5858/readyz
journalctl -u jj-agent -n 30 -o json
```

**Collect:**
- Systemd status: `sudo systemctl status jj-agent --no-pager`
- Health endpoints output
- Last 20 JSON log lines

---

## Step 4: Policy Proof + Smoke Test 🔒

### Policy Proof
```bash
# Should fail with denial
jj run "cat /etc/shadow" --workspace /tmp 2>&1

# Check audit log
cat state/*/audit.jsonl | jq 'select(.result.denied == true)' | head -5
```

### Smoke Test
```bash
export JJ_ENV=production
export JJ_PROD_STRICT=1
export OPENAI_API_KEY=sk-YOUR-KEY

jj run "Create a FastAPI app with JWT auth and PostgreSQL" --workspace ~/code/demo
```

**Collect:**
- Denial test output + audit entry
- Smoke test output + project folder

---

## Step 5: Collect Artifacts 📦

**Use template:** `ARTIFACTS_SUBMISSION_TEMPLATE.md`

**Required:**
1. GitHub Release URL
2. PyPI URL
3. GHCR image digest
4. Verification logs (Linux + Windows)
5. Server proof (systemd, health, logs)
6. Policy proof
7. Smoke test results
8. GO_NOGO_CHECKLIST.md completed

**Or use automated collection:**
```bash
chmod +x COLLECT_ARTIFACTS.sh
./COLLECT_ARTIFACTS.sh
```

---

## Step 6: Post-Release Tidy 🎯

```bash
cd jj-agent

# Version bump
chmod +x POST_RELEASE_TIDY.sh
./POST_RELEASE_TIDY.sh
git commit -am "Bump version to 0.1.1-dev"
git push origin master

# Roadmap PR
chmod +x CREATE_ROADMAP_PR.sh
./CREATE_ROADMAP_PR.sh
git push -u origin feature/v0.2.0-roadmap
gh pr create --title "v0.2.0 Roadmap" --body-file v0.2.0_ROADMAP_PR.md
```

---

## Go/No-Go Decision

After all steps, check `GO_NOGO_CHECKLIST.md`:
- ✅ GO if all criteria pass
- ❌ NO-GO if any fail → Execute `ROLLBACK_PROCEDURE.md`

---

## Artifact Submission

Fill in `ARTIFACTS_SUBMISSION_TEMPLATE.md` and return all artifacts.

---

**Status:** ✅ Ready  
**Action:** Configure remote and push tag

