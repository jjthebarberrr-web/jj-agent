# v0.1.0 Release Instructions

## Status: ✅ Ready for Release

All code is complete, tested, and documented. The release tag `v0.1.0` has been created locally.

## Next Steps

### 1. Push to Remote Repository

```bash
cd jj-agent

# Push commits
git push origin main  # or master, depending on your default branch

# Push tags (this triggers CI/CD)
git push origin v0.1.0
```

### 2. CI/CD Pipeline (Automatic)

Once the tag is pushed, GitHub Actions will:

1. **Run Tests**
   - Lint with ruff
   - Format check with black
   - Type check with mypy
   - Run pytest suite

2. **Build Artifacts**
   - Build Python wheels
   - Build Docker image

3. **Publish**
   - Push Docker image to `ghcr.io/ORG/jj-agent:v0.1.0`
   - Push Docker image to `ghcr.io/ORG/jj-agent:latest`
   - Publish to PyPI as `jj-agent==0.1.0`

4. **Create Release**
   - Create GitHub Release from tag
   - Attach release notes

### 3. Verify Release

After CI/CD completes (usually 5-10 minutes):

#### Check PyPI
```bash
pip index versions jj-agent
# Should show: jj-agent (0.1.0)
```

#### Check Docker
```bash
docker pull ghcr.io/ORG/jj-agent:v0.1.0
docker run --rm ghcr.io/ORG/jj-agent:v0.1.0 jj version
# Should show: jj-agent version 0.1.0
```

#### Check GitHub Release
- Visit: `https://github.com/ORG/jj-agent/releases/tag/v0.1.0`
- Verify release notes are present

### 4. Production Installation Test

```bash
# Install via pipx
pipx install jj-agent

# Verify installation
jj doctor
jj version

# Test production mode
export JJ_ENV=production
export JJ_PROD_STRICT=1
export OPENAI_API_KEY=sk-your-key-here

# Test with dry-run first
jj run --dry-run "Create FastAPI skeleton" --workspace ~/code/demo

# Full test
jj run "Create a FastAPI app with JWT auth and PostgreSQL" --workspace ~/code/demo
```

### 5. Verify Production Features

Check that all production features work:

```bash
# 1. Capabilities enforcement
# Should fail if capabilities.prod.yaml missing in production
export JJ_ENV=production
jj run "test" --workspace ~/code/demo

# 2. Audit logs
ls -la ~/code/demo/../jj-agent/state/*/audit.jsonl
# Should show audit log files

# 3. Health endpoints (if daemon mode)
jj run --daemon &
curl http://localhost:5858/healthz
curl http://localhost:5858/readyz
curl http://localhost:5858/metrics

# 4. Denied actions
# Try a forbidden command (should be denied)
jj run "rm -rf /" --workspace ~/code/demo
# Should fail with denial message
```

## Release Checklist

- [x] Code complete
- [x] Tests written
- [x] Documentation complete
- [x] CI/CD configured
- [x] Local tag created
- [ ] **Push to remote** (you need to do this)
- [ ] CI/CD runs successfully
- [ ] PyPI package published
- [ ] Docker image published
- [ ] GitHub Release created
- [ ] Production installation verified
- [ ] All production features tested

## Post-Release

Once v0.1.0 is confirmed stable:

1. **Update Documentation**
   - Add release badge to README
   - Update installation instructions if needed

2. **Monitor**
   - Check PyPI download stats
   - Monitor GitHub issues
   - Review error logs

3. **Begin v0.2.0**
   - See `ROADMAP.md` for planned features
   - Start with web search integration
   - Expand skills library

## Troubleshooting

### CI/CD Fails
- Check GitHub Actions logs
- Verify secrets are set (PYPI_API_TOKEN, GITHUB_TOKEN)
- Check Docker registry permissions

### PyPI Upload Fails
- Verify PYPI_API_TOKEN is correct
- Check package name availability
- Ensure version number is unique

### Docker Build Fails
- Check Dockerfile syntax
- Verify base images are accessible
- Check registry permissions

## Support

If you encounter issues:
1. Check `RELEASE_CHECKLIST.md`
2. Review `OPERATIONS.md`
3. Check GitHub Issues
4. Review audit logs in `state/`

