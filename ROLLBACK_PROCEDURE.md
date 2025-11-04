# Rollback Procedure for v0.1.0

## When to Rollback

**NO-GO Criteria (trigger rollback if any fail):**
- CI pipeline fails
- Missing artifacts (Release, PyPI, GHCR)
- Verification scripts fail on Linux or Windows
- Health endpoints fail
- Audit logs missing
- Capabilities not enforced
- Smoke test fails with policy violations

## Rollback Steps

### 1. PyPI Yank

**Option A: Via twine (if you have access)**
```bash
pip install twine
twine yank jj-agent==0.1.0 --reason "Critical bug - rollback" \
  --repository-url https://upload.pypi.org/legacy/
```

**Option B: Via PyPI Web UI**
1. Go to: https://pypi.org/project/jj-agent/0.1.0/
2. Click "Manage" or "Admin"
3. Select "Yank release"
4. Enter reason: "Critical bug - rollback"

### 2. GitHub Release & Tag

```bash
cd jj-agent

# Delete local tag
git tag -d v0.1.0

# Delete remote tag
git push origin :refs/tags/v0.1.0

# Delete GitHub Release (via UI or API)
# Visit: https://github.com/ORG/jj-agent/releases/tag/v0.1.0
# Click "Delete release" button
```

**Or via GitHub CLI:**
```bash
gh release delete v0.1.0 --yes
gh api repos/ORG/jj-agent/git/refs/tags/v0.1.0 -X DELETE
```

### 3. GHCR Image

**Via GitHub Packages UI:**
1. Go to: https://github.com/ORG/jj-agent/packages
2. Find package: `jj-agent`
3. Click on version `v0.1.0`
4. Delete the version tag

**Or via GitHub CLI:**
```bash
gh api user/packages/container/jj-agent/versions \
  --jq '.[] | select(.metadata.container.tags[] == "v0.1.0") | .id' | \
  xargs -I {} gh api user/packages/container/jj-agent/versions/{} -X DELETE
```

### 4. Hotfix Process

```bash
cd jj-agent

# Bump to hotfix version
./POST_RELEASE_TIDY.sh  # Sets to 0.1.1-dev

# Create hotfix branch
git checkout -b hotfix/0.1.1

# Make fixes...
git add .
git commit -m "Hotfix: <issue description>"

# Tag hotfix
git tag -a v0.1.1 -m "Release v0.1.1 - Hotfix"

# Push hotfix
git push -u origin hotfix/0.1.1
git push origin v0.1.1

# CI/CD will build and publish v0.1.1
```

### 5. Communication

**Update documentation:**
- Add deprecation notice to v0.1.0 release (if still visible)
- Update README with version recommendation
- Create GitHub issue documenting the rollback

**Notify users:**
- Update release notes
- Post in communication channels
- Update any public documentation

## Rollback Checklist

- [ ] PyPI version yanked
- [ ] GitHub Release deleted
- [ ] GitHub tag deleted
- [ ] GHCR image deleted
- [ ] Hotfix version created (0.1.1)
- [ ] Fixes committed
- [ ] Hotfix tagged and pushed
- [ ] Documentation updated
- [ ] Users notified

## Prevention

After rollback, review:
1. What caused the failure?
2. How can we prevent it in the future?
3. Update CI/CD checks
4. Improve testing
5. Add additional preflight checks

