# 🚀 EXECUTE v0.1.0 RELEASE NOW

## Status: ✅ READY TO EXECUTE

All fixes applied, all scripts ready, all documentation complete.

---

## Step 1: Push Tag (DO THIS NOW)

### Option A: Use Script
```bash
cd jj-agent
chmod +x EXECUTE_RELEASE.sh
./EXECUTE_RELEASE.sh
```

### Option B: Manual Push
```bash
cd jj-agent
git push origin v0.1.0
```

**This triggers CI/CD. Monitor at:**
- https://github.com/ORG/jj-agent/actions
- Or: `gh run watch --exit-status`

**Expected Duration:** 5-10 minutes

---

## Step 2: After CI/CD Completes - Verification

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

**Collect:** `verify_prod_linux.log` and `verify_prod_windows.log`

---

## Step 3: Server Deployment

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
journalctl -u jj-agent -n 50 -o json
```

**Collect:**
- Systemd status: `sudo systemctl status jj-agent --no-pager`
- Health endpoints output
- Last 20 JSON log lines

---

## Step 4: Production Smoke Test

```bash
export JJ_ENV=production
export OPENAI_API_KEY=sk-YOUR-KEY
jj run "Create a FastAPI app with JWT auth and PostgreSQL" --workspace ~/code/demo
```

**Collect:**
- Command output
- Project folder: `ls -la ~/code/demo/`

---

## Step 5: Collect Artifacts

See `ARTIFACTS_TEMPLATE.md` for complete list:

1. **CI/CD Links:**
   - GitHub Release URL
   - PyPI URL
   - Docker image digest

2. **Verification Logs:**
   - `verify_prod_linux.log`
   - `verify_prod_windows.log`

3. **Server Proof:**
   - Systemd status
   - Health endpoints
   - JSON logs (20 lines)

4. **Policy Proof:**
   ```bash
   jj run "cat /etc/shadow" --workspace /tmp 2>&1
   cat state/*/audit.jsonl | jq 'select(.result.denied == true)' | head -5
   ```

5. **Smoke Test:**
   - Command output
   - Project folder contents

---

## Step 6: Post-Release Tidy

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

## PRODUCTION_READY.md Checklist

All items from `PRODUCTION_READY.md` are ✅ complete:

- ✅ Production mode enforced
- ✅ Capabilities file required
- ✅ Sandboxing available
- ✅ Audit logging enabled
- ✅ Secrets redacted
- ✅ Metrics collected
- ✅ Health endpoints available
- ✅ CI/CD pipeline configured
- ✅ Documentation complete

---

## Current State

- ✅ Tag v0.1.0 exists
- ✅ All scripts fixed and tested
- ✅ Documentation complete
- ✅ Post-release scripts ready
- ⏳ **Ready for tag push**

---

## START HERE

**Execute Step 1 now:**
```bash
cd jj-agent
git push origin v0.1.0
```

Then follow steps 2-6 as CI/CD completes.

