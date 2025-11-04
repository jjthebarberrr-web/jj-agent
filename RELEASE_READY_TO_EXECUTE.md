# ✅ v0.1.0 Release - READY TO EXECUTE

## Preflight Status: ✅ PASSED

- ✅ Commit: `5dcaf4f` (matches expected)
- ✅ Version: `0.1.0` (consistent across all files)
- ✅ Tag: `v0.1.0` exists locally
- ⚠️ Remote: Not configured (needs setup)

---

## Step 0: Configure Remote (If Needed)

**Check remote:**
```bash
cd jj-agent
git remote -v
```

**If no remote exists, configure it:**
```bash
git remote add origin <your-github-repo-url>
# Example: git remote add origin https://github.com/ORG/jj-agent.git
```

**Verify CI Secrets (in GitHub Actions):**
- Go to: Repository → Settings → Secrets and variables → Actions
- Verify `PYPI_API_TOKEN` is set
- Verify `GITHUB_TOKEN` is set (or uses `GITHUB_TOKEN` default)

---

## Step 1: Trigger Release 🚀

**Execute:**
```bash
cd jj-agent
git push origin v0.1.0
```

**Or use script:**
```bash
cd jj-agent
chmod +x EXECUTE_RELEASE_FINAL.sh
./EXECUTE_RELEASE_FINAL.sh
```

**Expected:**
- Tag pushed successfully
- CI/CD triggered at: https://github.com/ORG/jj-agent/actions
- Monitor: `gh run watch --exit-status`

**Duration:** 5-10 minutes

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

## Step 5: Submit Artifacts 📦

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

## Usage After Release

Once released, use on your machine:

```bash
pipx install "jj-agent==0.1.0"

export JJ_ENV=production
export OPENAI_API_KEY="your-key"

jj run "Create a FastAPI app with JWT auth and PostgreSQL" --workspace ~/code/demo
```

---

## Status

✅ **All preflight checks passed**  
✅ **All scripts ready**  
✅ **All documentation complete**  
⚠️ **Remote needs configuration** (if not already set)

**Next Action:** Configure remote (if needed), then push tag

---

**Ready to execute!**

