# 🚀 Push & Verify v0.1.0 Release

## Quick Commands

### 1. Push to Trigger CI/CD

```bash
cd jj-agent

# Sanity check
git update-index -q --refresh
git status
git log -1 --oneline
git tag -l v0.1.0

# Get branch name
BRANCH=$(git rev-parse --abbrev-ref HEAD)

# Push branch + tag
git push -u origin "$BRANCH"
git push origin v0.1.0

# Or single command
git push origin --follow-tags
```

### 2. Monitor CI/CD

**GitHub CLI:**
```bash
gh run watch --exit-status
gh release view v0.1.0
```

**Or watch in browser:**
- https://github.com/ORG/jj-agent/actions

### 3. Install & Verify

```bash
# Install
pipx install "jj-agent==0.1.0"

# Quick check
jj doctor
jj version

# Production test
export JJ_ENV=production
export JJ_PROD_STRICT=1
export OPENAI_API_KEY=sk-...

jj run --dry-run "Create FastAPI skeleton" --workspace ~/code/demo
```

### 4. Automated Verification

**Unix/Linux/macOS:**
```bash
chmod +x verify_prod.sh
./verify_prod.sh
```

**Windows:**
```powershell
.\verify_prod.ps1
```

## Verification Checklist

After CI/CD completes, verify:

- [ ] PyPI package: https://pypi.org/project/jj-agent/0.1.0/
- [ ] Docker image: `docker pull ghcr.io/ORG/jj-agent:v0.1.0`
- [ ] GitHub Release: https://github.com/ORG/jj-agent/releases/tag/v0.1.0
- [ ] Production install works: `pipx install jj-agent`
- [ ] Capabilities enforced
- [ ] Audit logs generated
- [ ] Health endpoints respond
- [ ] Full job completes successfully

## Common Issues

**PyPI publish fails:**
- Check `PYPI_API_TOKEN` has `pypi:write` scope
- Verify package name is available

**Docker push fails:**
- Check `GITHUB_TOKEN` has `packages:write` permission
- Verify repository permissions

**Version conflict:**
- PyPI doesn't allow overwriting versions
- Bump to 0.1.1 if needed

## Full Documentation

- `RELEASE_VERIFICATION.md` - Detailed verification steps
- `RELEASE_CHECKLIST.md` - Complete checklist
- `RELEASE_INSTRUCTIONS.md` - Step-by-step guide
- `OPERATIONS.md` - Operations guide

## Post-Release

Once verified:
1. Mark release as stable
2. Update documentation badges
3. Begin v0.2.0 development (see `ROADMAP.md`)

