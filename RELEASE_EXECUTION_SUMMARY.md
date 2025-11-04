# v0.1.0 Release Execution Summary

## ✅ Fixes Applied

1. **PowerShell Script:** Fixed path detection using `Split-Path -Parent $MyInvocation.MyCommand.Path`
2. **Git Warning:** Added `git update-index -q --refresh` in PUSH_AND_VERIFY.md

## 📋 Release Execution Steps

### A) Push Release Tag

**Status:** Ready to execute

```bash
cd jj-agent
git pull --rebase
git tag v0.1.0  # Already exists
git push origin v0.1.0
```

**Automated script available:**
```bash
chmod +x EXECUTE_RELEASE.sh
./EXECUTE_RELEASE.sh
```

### B) Verification Scripts

**After CI/CD completes:**

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

**Production setup (America/Phoenix):**

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

**Health checks:**
```bash
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

### E) Artifacts to Collect

See `ARTIFACTS_COLLECTION.md` for complete list:

1. **CI/CD Links:**
   - GitHub Release URL
   - PyPI Package URL  
   - Docker Image Digest

2. **Verification Logs:**
   - verify_prod_linux.log
   - verify_prod_windows.log

3. **Server Proof:**
   - Health endpoint outputs
   - Systemd status
   - JSON logs (20 lines)
   - Policy proof (denial test)

4. **Production Smoke Test:**
   - Job completion status
   - Output files

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

## 🎯 Current Status

- ✅ Scripts fixed and tested
- ✅ Release documentation complete
- ✅ Verification scripts ready
- ✅ Post-release scripts prepared
- ⏳ **Ready for tag push**

## 📝 Next Actions

1. **Push tag** to trigger CI/CD
2. **Monitor** CI/CD pipeline (5-10 min)
3. **Run verification** scripts after CI/CD
4. **Deploy** to server
5. **Collect artifacts**
6. **Bump version** to 0.1.1-dev
7. **Create roadmap PR**

## 📚 Documentation

All documentation is ready:
- `RELEASE_EXECUTION.md` - Complete execution guide
- `ARTIFACTS_COLLECTION.md` - Artifact collection template
- `RELEASE_VERIFICATION.md` - Detailed verification steps
- `v0.2.0_ROADMAP_PR.md` - Roadmap PR content

