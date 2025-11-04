# 🚀 EXECUTE v0.1.0 RELEASE NOW

## ✅ Preflight: PASSED

- ✅ Commit: `5dcaf4f` (matches expected)
- ✅ Version: `0.1.0` (consistent across all files)
- ✅ Tag: `v0.1.0` exists
- ⚠️ CI Secrets: Verify `PYPI_API_TOKEN` and `GITHUB_TOKEN` are set in CI

---

## Step 1: Trigger Release ⚡

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

**This triggers CI/CD. Monitor at:**
- https://github.com/ORG/jj-agent/actions
- Or: `gh run watch --exit-status`

**Expected duration:** 5-10 minutes

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

**Follow RELEASE_EXECUTION.md Section C:**

```bash
sudo useradd -r -s /usr/sbin/nologin jj || true
sudo mkdir -p /etc/jj-agent /var/log/jj
sudo cp capabilities.prod.yaml /etc/jj-agent/
printf "JJ_ENV=production\nTZ=America/Phoenix\n" | sudo tee /etc/jj-agent/jj.env
pipx install "jj-agent==0.1.0"
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
- Health endpoints output
- Last 20 JSON log lines

---

## Step 4: Production Smoke Test 🧪

```bash
export JJ_ENV=production
export JJ_PROD_STRICT=1
export OPENAI_API_KEY=sk-YOUR-KEY

jj run "Create a FastAPI app with JWT auth and PostgreSQL" --workspace ~/code/demo
```

**Collect:**
- Command output
- Project folder: `ls -la ~/code/demo/`

---

## Step 5: Policy Proof 🔒

```bash
# Should fail with denial
jj run "cat /etc/shadow" --workspace /tmp 2>&1

# Check audit log
cat state/*/audit.jsonl | jq 'select(.result.denied == true)' | head -5
```

**Collect:**
- Denial command output
- Audit log entry showing `"denied": true`

---

## Step 6: Collect All Artifacts 📦

### Automated
```bash
chmod +x COLLECT_ARTIFACTS.sh
./COLLECT_ARTIFACTS.sh
```

### Manual (see ARTIFACTS_COLLECTION_FINAL.md)

**Required artifacts:**
1. **CI/CD Links:**
   - GitHub Release URL
   - PyPI URL
   - GHCR image digest

2. **Verification Logs:**
   - `verify_prod_linux.log`
   - `verify_prod_windows.log`

3. **Server Proof:**
   - Systemd status (one screen)
   - `/healthz` output
   - `/readyz` output
   - Last 20 JSON log lines

4. **Policy Proof:**
   - Denial test output
   - Audit log entry

5. **Smoke Test:**
   - Command output
   - Project folder path

6. **Checklist:**
   - `GO_NOGO_CHECKLIST.md` completed

---

## Step 7: Post-Release Tidy 🎯

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

## Go/No-Go Decision ✅/❌

After all steps, check `GO_NOGO_CHECKLIST.md`:

**✅ GO if all pass:**
- CI pipeline green
- All artifacts present
- Verification passes
- Health endpoints OK
- Capabilities enforced
- Smoke test completes

**❌ NO-GO if any fail:**
- Execute `ROLLBACK_PROCEDURE.md`

---

## Artifact Submission

Use `ARTIFACTS_SUBMISSION_TEMPLATE.md` to format your submission.

---

## Quick Reference

**Scripts:**
- `EXECUTE_RELEASE_FINAL.sh` - Push tag
- `COLLECT_ARTIFACTS.sh` - Collect artifacts
- `POST_RELEASE_TIDY.sh` - Version bump
- `CREATE_ROADMAP_PR.sh` - Roadmap PR

**Documentation:**
- `RELEASE_EXECUTION_COMPLETE.md` - Complete guide
- `ARTIFACTS_COLLECTION_FINAL.md` - Artifact details
- `GO_NOGO_CHECKLIST.md` - Decision criteria
- `ROLLBACK_PROCEDURE.md` - Rollback steps

---

**Status:** ✅ READY TO EXECUTE  
**Action:** Run Step 1 now: `git push origin v0.1.0`

