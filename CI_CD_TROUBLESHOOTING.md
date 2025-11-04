# CI/CD Troubleshooting Guide

## Issue: No CI/CD Activity After Tag Push

### Verification Steps

1. **Tag Push Confirmed:**
   - ✅ Tag `v0.1.0` exists on remote: `daf14fcdf10d7b42d62c961d3300dff18f7c404c`
   - ✅ Tag exists locally: `v0.1.0`

2. **Workflow File Status:**
   - ✅ Workflow file exists: `.github/workflows/release.yml`
   - ⚠️ Need to verify it's committed and pushed to main/master branch

3. **Workflow Configuration:**
   - ✅ Trigger: `on: push: tags: - "v*"` (correct)
   - ✅ Should trigger on `v0.1.0` tag push

### Common Issues & Solutions

#### Issue 1: Workflow File Not Committed/Pushed
**Symptom:** Workflow file exists locally but not in repository

**Solution:**
```bash
cd jj-agent
git add .github/workflows/release.yml
git commit -m "Add GitHub Actions release workflow"
git push origin master
```

#### Issue 2: Workflow File Not on Main Branch
**Symptom:** Workflow file exists but on wrong branch

**Solution:**
```bash
cd jj-agent
git checkout master
git merge <branch-with-workflow>
git push origin master
```

#### Issue 3: GitHub Actions Disabled
**Symptom:** No workflows show up in Actions tab

**Solution:**
1. Go to: Repository → Settings → Actions → General
2. Ensure "Allow all actions and reusable workflows" is enabled
3. Check "Workflow permissions" are set correctly

#### Issue 4: Tag Push Didn't Trigger Workflow
**Symptom:** Tag pushed but no workflow run

**Solution:**
- Verify tag matches pattern: `v*` (should match `v0.1.0`)
- Re-trigger by pushing tag again or creating a new tag
- Check Actions tab filters (may be filtered by branch)

#### Issue 5: Workflow File Syntax Error
**Symptom:** Workflow exists but shows errors

**Solution:**
```bash
# Validate workflow syntax
cd jj-agent
# Check if file is valid YAML
python -c "import yaml; yaml.safe_load(open('.github/workflows/release.yml'))"
```

### Manual Workflow Trigger

If automatic trigger doesn't work, you can manually trigger:

1. Go to: https://github.com/jjthebarberrr-web/jj-agent/actions
2. Click "Run workflow"
3. Select branch: `master`
4. Enter tag: `v0.1.0`

### Verification Checklist

- [ ] `.github/workflows/release.yml` exists in repository
- [ ] Workflow file is committed to `master` branch
- [ ] Workflow file is pushed to remote
- [ ] GitHub Actions is enabled in repository settings
- [ ] Tag `v0.1.0` exists on remote
- [ ] Workflow trigger pattern matches: `v*`
- [ ] No syntax errors in workflow file

### Next Steps

1. **Commit and push workflow file:**
   ```bash
   cd jj-agent
   git add .github/workflows/release.yml
   git commit -m "Add GitHub Actions release workflow"
   git push origin master
   ```

2. **Verify on GitHub:**
   - Go to: https://github.com/jjthebarberrr-web/jj-agent/tree/master/.github/workflows
   - Confirm `release.yml` is visible

3. **Re-trigger workflow:**
   - Option A: Push tag again: `git push origin v0.1.0 --force`
   - Option B: Create new tag: `git tag v0.1.0-1 && git push origin v0.1.0-1`
   - Option C: Manually trigger from Actions tab

4. **Check Actions tab:**
   - Go to: https://github.com/jjthebarberrr-web/jj-agent/actions
   - Look for workflow runs

### Repository Settings Check

1. **Repository → Settings → Actions → General:**
   - ✅ "Allow all actions and reusable workflows"
   - ✅ "Workflow permissions" → "Read and write permissions"

2. **Repository → Settings → Actions → Runners:**
   - ✅ GitHub-hosted runners enabled

3. **Repository → Settings → Actions → Runners → Self-hosted:**
   - ✅ (If using self-hosted, ensure runners are online)

### Contact Points

If issues persist:
1. Check GitHub Actions status: https://www.githubstatus.com/
2. Review workflow run logs if any appear
3. Check repository settings for Actions restrictions

