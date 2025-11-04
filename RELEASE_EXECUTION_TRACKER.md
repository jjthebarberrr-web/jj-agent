# v0.1.0 Release Execution Tracker

## Execution Status

### Step 1: Trigger Release ✅

**Command Executed:**
```bash
cd jj-agent
git push origin v0.1.0
```

**Status:** ⏳ Pending execution
**Note:** Requires remote repository configured and authentication

**CI Secrets Check:**
- [ ] PYPI_API_TOKEN set in CI (GitHub Actions Secrets)
- [ ] GITHUB_TOKEN set in CI (GitHub Actions Secrets)

**CI/CD Monitor:**
- URL: https://github.com/ORG/jj-agent/actions
- Command: `gh run watch --exit-status`

**Expected Artifacts (after CI/CD):**
- [ ] GitHub Release created
- [ ] PyPI package published
- [ ] GHCR image published

---

### Step 2: Verification ⏳

**Status:** Waiting for CI/CD completion

#### Linux/macOS
```bash
pipx install "jj-agent==0.1.0"
chmod +x verify_prod.sh
./verify_prod.sh | tee verify_prod_linux.log
```

**Status:** ⏳ Pending
**Artifact:** `verify_prod_linux.log`

#### Windows PowerShell
```powershell
pipx install "jj-agent==0.1.0"
.\verify_prod.ps1 *>&1 | Tee-Object -FilePath verify_prod_windows.log
```

**Status:** ⏳ Pending
**Artifact:** `verify_prod_windows.log`

---

### Step 3: Server Deployment ⏳

**Status:** Waiting for verification

**Commands (from EXECUTE_NOW_FINAL.md):**
```bash
sudo useradd -r -s /usr/sbin/nologin jj || true
sudo mkdir -p /etc/jj-agent /var/log/jj
sudo cp capabilities.prod.yaml /etc/jj-agent/
printf "JJ_ENV=production\nTZ=America/Phoenix\n" | sudo tee /etc/jj-agent/jj.env
pipx install "jj-agent==0.1.0"
sudo cp jj-agent.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now jj-agent
```

**Health Checks:**
```bash
curl -sS http://127.0.0.1:5858/healthz
curl -sS http://127.0.0.1:5858/readyz
journalctl -u jj-agent -n 30 -o json
```

**Status:** ⏳ Pending
**Artifacts to collect:**
- [ ] Systemd status (one screen)
- [ ] `/healthz` output
- [ ] `/readyz` output
- [ ] Last 20 JSON log lines

---

### Step 4: Policy Proof + Smoke Test ⏳

**Status:** Waiting for server deployment

#### Policy Proof
```bash
# Denial test (should fail)
jj run "cat /etc/shadow" --workspace /tmp 2>&1

# Check audit log
cat state/*/audit.jsonl | jq 'select(.result.denied == true)' | head -5
```

**Status:** ⏳ Pending
**Artifacts:**
- [ ] Denial command output
- [ ] Audit log entry showing `"denied": true`

#### Smoke Test
```bash
export JJ_ENV=production
export JJ_PROD_STRICT=1
export OPENAI_API_KEY=sk-YOUR-KEY

jj run "Create a FastAPI app with JWT auth and PostgreSQL" --workspace ~/code/demo
```

**Status:** ⏳ Pending
**Artifacts:**
- [ ] Command output
- [ ] Project folder: `ls -la ~/code/demo/`

---

### Step 5: Artifact Submission ⏳

**Status:** Waiting for all steps above

**Use template:** `ARTIFACTS_SUBMISSION_TEMPLATE.md`

**Required artifacts:**
1. [ ] GitHub Release URL
2. [ ] PyPI URL
3. [ ] GHCR image digest
4. [ ] `verify_prod_linux.log`
5. [ ] `verify_prod_windows.log`
6. [ ] Systemd status
7. [ ] Health endpoints outputs
8. [ ] JSON logs (last 20 lines)
9. [ ] Policy proof (denial + audit)
10. [ ] Smoke test results
11. [ ] GO_NOGO_CHECKLIST.md completed

---

### Step 6: Post-Release Tidy ⏳

**Status:** Waiting for artifact submission

#### Version Bump
```bash
cd jj-agent
chmod +x POST_RELEASE_TIDY.sh
./POST_RELEASE_TIDY.sh
git commit -am "Bump version to 0.1.1-dev"
git push origin master
```

**Status:** ⏳ Pending

#### Roadmap PR
```bash
chmod +x CREATE_ROADMAP_PR.sh
./CREATE_ROADMAP_PR.sh
git push -u origin feature/v0.2.0-roadmap
gh pr create --title "v0.2.0 Roadmap" --body-file v0.2.0_ROADMAP_PR.md
```

**Status:** ⏳ Pending

---

## Current Status Summary

- ✅ Preflight: PASSED
- ⏳ Step 1: Tag push (ready to execute)
- ⏳ Step 2: Verification (waiting for CI/CD)
- ⏳ Step 3: Server deployment (waiting)
- ⏳ Step 4: Policy proof + smoke test (waiting)
- ⏳ Step 5: Artifact collection (waiting)
- ⏳ Step 6: Post-release tidy (waiting)

---

## Next Action

**Execute Step 1:**
```bash
cd jj-agent
git push origin v0.1.0
```

Then follow steps 2-6 as CI/CD completes and verification runs.

---

**Last Updated:** Release execution started  
**Next Update:** After tag push confirmation

