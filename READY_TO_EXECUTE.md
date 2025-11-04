# ✅ Ready to Execute v0.1.0 Release

## Status: ALL FIXES APPLIED & READY

### ✅ Fixes Completed

1. **PowerShell Script Fixed:**
   - Updated `verify_prod.ps1` to use `Split-Path -Parent $MyInvocation.MyCommand.Path`
   - Script now correctly detects its own directory

2. **Git Warning Fixed:**
   - Added `git update-index -q --refresh` in `PUSH_AND_VERIFY.md`
   - Prevents index file warnings

### 📋 Current State

- **Tag:** `v0.1.0` exists and is ready
- **Latest Commit:** `f61023e` - "Fix PowerShell script path detection..."
- **All Scripts:** Ready and tested
- **Documentation:** Complete

## 🚀 Execution Commands

### A) Push Release Tag

```bash
cd jj-agent

# Pull latest (if remote exists)
git pull --rebase

# Verify tag
git tag -l v0.1.0

# Push tag (triggers CI/CD)
git push origin v0.1.0
```

**Or use automated script:**
```bash
chmod +x EXECUTE_RELEASE.sh
./EXECUTE_RELEASE.sh
```

### B) After CI/CD Completes - Verification

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

### C) Server Deployment

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
journalctl -u jj-agent --since "10 min ago" -o json | head -n 50
```

### D) Production Smoke Test

```bash
export JJ_ENV=production
export OPENAI_API_KEY=sk-YOUR-KEY
jj run "Create a FastAPI app with JWT auth and PostgreSQL" --workspace ~/code/demo
```

### E) Collect Artifacts

See `ARTIFACTS_COLLECTION.md` for complete template.

**Required:**
1. GitHub Release URL
2. PyPI Package URL
3. Docker Image Digest
4. Verification logs (Linux + Windows)
5. Server proof (health endpoints, systemd status, JSON logs, policy proof)

### F) Post-Release Tidy

**Version Bump:**
```bash
chmod +x POST_RELEASE_TIDY.sh
./POST_RELEASE_TIDY.sh
git commit -am "Bump version to 0.1.1-dev"
git push origin master
```

**Create Roadmap PR:**
```bash
chmod +x CREATE_ROADMAP_PR.sh
./CREATE_ROADMAP_PR.sh
git push -u origin feature/v0.2.0-roadmap
gh pr create --title "v0.2.0 Roadmap" --body-file v0.2.0_ROADMAP_PR.md
```

## 📚 Documentation Files

All documentation is ready:
- `RELEASE_EXECUTION.md` - Complete execution guide
- `RELEASE_EXECUTION_SUMMARY.md` - This summary
- `ARTIFACTS_COLLECTION.md` - Artifact collection template
- `RELEASE_VERIFICATION.md` - Detailed verification steps
- `v0.2.0_ROADMAP_PR.md` - Roadmap PR content
- `PUSH_AND_VERIFY.md` - Quick reference

## 🎯 Next Step

**Execute Step A:** Push the tag to trigger CI/CD

```bash
cd jj-agent
git push origin v0.1.0
```

Then monitor CI/CD and follow steps B-F as outlined above.

---

**Status:** ✅ READY FOR EXECUTION  
**Tag:** v0.1.0  
**Action:** Push tag to remote

