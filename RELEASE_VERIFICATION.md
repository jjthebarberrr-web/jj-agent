# v0.1.0 Release Verification Guide

## Quick Start

### Automated Verification (Recommended)

**Unix/Linux/macOS:**
```bash
chmod +x verify_prod.sh
./verify_prod.sh
```

**Windows PowerShell:**
```powershell
.\verify_prod.ps1
```

### Manual Verification Steps

Follow these steps to verify the release after CI/CD completes.

## 1. Pre-Push Verification

Before pushing, verify locally:

```bash
cd jj-agent

# Check git status
git status
git log -1 --oneline
git tag -l v0.1.0

# Verify tag is annotated
git show v0.1.0 --no-patch
```

## 2. Push to Trigger CI/CD

```bash
# Get current branch name
BRANCH=$(git rev-parse --abbrev-ref HEAD)

# Push branch
git push -u origin "$BRANCH"

# Push tag (triggers CI/CD)
git push origin v0.1.0

# Alternative: push both at once
git push origin --follow-tags
```

## 3. Monitor CI/CD Pipeline

### Using GitHub CLI

```bash
# Watch workflow runs
gh run watch --exit-status

# View the release once created
gh release view v0.1.0
```

### Using GitHub Web UI

1. Go to: `https://github.com/ORG/jj-agent/actions`
2. Watch the "release" workflow
3. Verify all jobs pass:
   - ✅ lint
   - ✅ test
   - ✅ build-test
   - ✅ docker
   - ✅ pypi

**Expected Duration**: 5-10 minutes

## 4. Post-Publish Installation

### Install via pipx (Recommended)

```bash
# Fresh, isolated install
pipx install "jj-agent==0.1.0"

# Verify installation
jj doctor
jj version
```

**Expected Output:**
```
jj-agent version 0.1.0
```

### Install via Docker

```bash
# Pull image
docker pull ghcr.io/ORG/jj-agent:v0.1.0

# Verify
docker run --rm ghcr.io/ORG/jj-agent:v0.1.0 jj version
```

## 5. Production Verification Checklist

### 5.1 Capabilities Enforcement

```bash
export JJ_ENV=production
export JJ_PROD_STRICT=1
export OPENAI_API_KEY=sk-...

# Should fail if capabilities.prod.yaml missing
jj run "test" --workspace ~/code/demo
```

**Expected**: Error if `capabilities.prod.yaml` missing

### 5.2 Sandboxed Runner (if Docker available)

```bash
export JJ_RUNTIME=sandboxed
jj run --dry-run "echo test" --workspace ~/code/demo
```

**Expected**: Command runs in Docker container

### 5.3 LocalSafe Runner

```bash
export JJ_RUNTIME=localsafe
jj run --dry-run "echo test" --workspace ~/code/demo
```

**Expected**: Command validated against allowlist

### 5.4 Audit Trail

```bash
# Run a job
jj run "Create FastAPI skeleton" --workspace ~/code/demo

# Check audit logs
ls -la state/*/audit.jsonl
cat state/*/audit.jsonl | jq '.' | head -20
```

**Expected**: 
- Audit log file exists
- Contains JSON entries with: timestamp, tool, args, result, duration_ms

### 5.5 Structured JSON Logs

```bash
# Check logs (if daemon mode)
tail -f /var/log/jj-agent/*.log | jq '.'

# Or check local logs
cat state/*/exec.log | jq '.' | head -10
```

**Expected**: JSON logs with: timestamp, level, message, job_id

### 5.6 Health Endpoints

```bash
# Start daemon
jj run --daemon --listen 127.0.0.1:5858 &

# Test endpoints
curl -sSf http://localhost:5858/healthz
curl -sSf http://localhost:5858/readyz
curl -sSf http://localhost:5858/metrics
```

**Expected**:
- `/healthz`: `{"status":"healthy","version":"0.1.0"}`
- `/readyz`: `{"status":"ready","version":"0.1.0"}`
- `/metrics`: JSON with metrics

### 5.7 Systemd Service (if deployed)

```bash
# Install service
sudo cp jj-agent.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable jj-agent
sudo systemctl start jj-agent

# Check status
sudo systemctl status jj-agent --no-pager

# Check logs
sudo journalctl -u jj-agent -f
```

**Expected**: Service starts and runs without errors

### 5.8 Forbidden Paths/Commands

```bash
# Test forbidden path
jj run "cat /etc/shadow" --workspace ~/code/demo
# Should fail with denial

# Test forbidden command
jj run "rm -rf /" --workspace ~/code/demo
# Should fail with denial

# Check audit log for denial entry
cat state/*/audit.jsonl | jq 'select(.result.denied == true)'
```

**Expected**: All forbidden actions blocked and logged

### 5.9 Full Production Run

```bash
export JJ_ENV=production
export JJ_PROD_STRICT=1
export OPENAI_API_KEY=sk-...

# Run full job
time jj run "Create a FastAPI app with JWT auth and PostgreSQL" \
  --workspace ~/code/demo

# Verify output
ls -la ~/code/demo/
```

**Expected**: 
- Job completes successfully
- Files created in workspace
- Audit logs generated
- No policy violations

## 6. Common Gotchas

### PyPI Issues

**Problem**: Package name unavailable or token lacks publish scope

**Solution**:
- Check package name availability on PyPI
- Verify `PYPI_API_TOKEN` has `pypi:write` scope
- Check PyPI project settings

### Version Conflicts

**Problem**: Version 0.1.0 already exists on PyPI

**Solution**:
- PyPI doesn't allow overwriting versions
- Bump to 0.1.1 if needed
- Delete and re-release if critical

### GHCR Permissions

**Problem**: Docker push fails

**Solution**:
- Verify `GITHUB_TOKEN` has `packages:write` permission
- Check repository → Settings → Actions → General → Workflow permissions
- Ensure token has package write access

### Missing Artifacts

**Problem**: Wheel or sdist missing

**Solution**:
- Check build logs in GitHub Actions
- Verify `setup.py` and `MANIFEST.in` are correct
- Check PyPI page for uploaded files

## 7. Rollback Plan

If critical issues are found after publishing:

### Step 1: Create Hotfix

```bash
git checkout -b hotfix/0.1.1
# ... make fixes ...
git commit -m "Hotfix: <issue description>"
git tag -a v0.1.1 -m "Release v0.1.1 - Hotfix"
git push -u origin hotfix/0.1.1
git push origin v0.1.1
```

### Step 2: Deprecate Old Version

**PyPI:**
- Mark 0.1.0 as deprecated (if possible)
- Or yank the release: `twine yank jj-agent==0.1.0 --reason "Critical bug"`

**GitHub:**
- Add warning to 0.1.0 release notes
- Mark as deprecated

**Docker:**
- Tag 0.1.0 as deprecated
- Recommend 0.1.1 in documentation

### Step 3: Communicate

- Update README with version recommendation
- Add deprecation notice to 0.1.0 release
- Notify users via GitHub discussions/announcements

## 8. Verification Summary

After completing all checks, document:

- [ ] CI/CD pipeline passed
- [ ] PyPI package published
- [ ] Docker image published
- [ ] GitHub Release created
- [ ] Production installation works
- [ ] Capabilities enforced
- [ ] Audit logs generated
- [ ] Health endpoints respond
- [ ] Forbidden actions blocked
- [ ] Full job completes successfully

## 9. Post-Release Actions

Once verified:

1. **Announce Release**
   - Update README with release badge
   - Post on communication channels
   - Update documentation

2. **Monitor**
   - Watch PyPI download stats
   - Monitor GitHub issues
   - Review error logs
   - Check user feedback

3. **Begin v0.2.0**
   - See `ROADMAP.md` for plans
   - Start with web search integration
   - Expand skills library

## Support

If verification fails:
1. Check `RELEASE_CHECKLIST.md`
2. Review `OPERATIONS.md`
3. Check GitHub Actions logs
4. Review audit logs
5. Open GitHub issue with details

