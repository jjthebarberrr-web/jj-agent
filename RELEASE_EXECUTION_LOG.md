# v0.1.0 Release Execution Log

## Execution Timeline

### Step 1: Push Tag (Trigger CI/CD) ✅

**Timestamp:** Starting now  
**Command:**
```bash
cd jj-agent
./EXECUTE_RELEASE.sh
# or: git push origin v0.1.0
```

**Status:** ⏳ Ready to execute

**Note:** Actual push requires remote repository configured. If no remote exists, the script will indicate this.

---

### Step 2: Verification Scripts (After CI/CD) ⏳

**Status:** Waiting for CI/CD completion

**Linux/macOS:**
```bash
pipx install "jj-agent==0.1.0"
chmod +x verify_prod.sh
./verify_prod.sh | tee verify_prod_linux.log
```

**Windows PowerShell:**
```powershell
pipx install "jj-agent==0.1.0"
.\verify_prod.ps1 *>&1 | Tee-Object -FilePath verify_prod_windows.log
```

**Logs to collect:**
- `verify_prod_linux.log`
- `verify_prod_windows.log`

---

### Step 3: Server Deployment ⏳

**Status:** Waiting for verification

**Commands:**
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

**Artifacts to collect:**
- Systemd status output
- Health endpoint responses
- JSON log lines (last 20)

---

### Step 4: Production Smoke Test ⏳

**Status:** Waiting for server deployment

**Command:**
```bash
export JJ_ENV=production
export OPENAI_API_KEY=sk-REDACTED
jj run "Create a FastAPI app with JWT auth and PostgreSQL" --workspace ~/code/demo
```

**Artifacts to collect:**
- Command output
- Project folder path and contents

---

### Step 5: Artifacts Collection ⏳

**Status:** Waiting for all steps above

**Required artifacts:**
1. CI/CD links (GitHub Release, PyPI, Docker digest)
2. Verification logs (Linux + Windows)
3. Server proof (systemd, health endpoints, JSON logs)
4. Policy proof (denial test + audit entry)
5. Smoke test results
6. PRODUCTION_READY.md checklist confirmation

See `ARTIFACTS_TEMPLATE.md` for detailed collection guide.

---

### Step 6: Post-Release Tidy ✅

**Status:** Scripts ready

**Version Bump:**
```bash
./POST_RELEASE_TIDY.sh
git commit -am "Bump version to 0.1.1-dev"
git push origin master
```

**Roadmap PR:**
```bash
./CREATE_ROADMAP_PR.sh
git push -u origin feature/v0.2.0-roadmap
gh pr create --title "v0.2.0 Roadmap" --body-file v0.2.0_ROADMAP_PR.md
```

---

## Current Status

**Step 1:** ⏳ Ready to execute  
**Step 2:** ⏳ Waiting for CI/CD  
**Step 3:** ⏳ Waiting for verification  
**Step 4:** ⏳ Waiting for deployment  
**Step 5:** ⏳ Waiting for artifacts  
**Step 6:** ✅ Scripts ready

---

## Notes

- All scripts are tested and ready
- Documentation is complete
- Tag v0.1.0 exists locally
- Push to remote will trigger CI/CD
- Monitor CI/CD at: https://github.com/ORG/jj-agent/actions

---

**Last Updated:** Release execution started  
**Next Update:** After tag push


