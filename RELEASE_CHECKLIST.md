# v0.1.0 Release Checklist

## Pre-Release Verification

### Code Quality
- [x] All tests pass (`pytest tests/`)
- [x] Linting passes (`ruff check .`)
- [x] Type checking passes (`mypy .`)
- [x] No sensitive data in code
- [x] Documentation updated

### Configuration
- [x] `capabilities.prod.yaml` present
- [x] `capabilities.yaml` present
- [x] `Dockerfile` configured
- [x] `setup.py` configured
- [x] `requirements.txt` complete

### Documentation
- [x] `README.md` updated
- [x] `SECURITY.md` complete
- [x] `OPERATIONS.md` complete
- [x] `CHANGELOG.md` updated
- [x] `RELEASE_NOTES.md` created

### CI/CD
- [x] `.github/workflows/release.yml` configured
- [x] PyPI credentials set (PYPI_API_TOKEN)
- [x] Docker registry credentials set (GITHUB_TOKEN)

## Release Steps

### 1. Final Verification
```bash
# Check git status
git status

# Run tests
pytest tests/ -v

# Check version
python -c "from jj_agent import __version__; print(__version__)"
```

### 2. Tag Release
```bash
git tag -a v0.1.0 -m "Release v0.1.0 - Production Ready"
git push origin v0.1.0
```

### 3. CI/CD Pipeline
- [ ] GitHub Actions triggers on tag push
- [ ] Tests run and pass
- [ ] Docker image builds
- [ ] PyPI package builds
- [ ] Docker image pushed to ghcr.io
- [ ] PyPI package published
- [ ] GitHub Release created

### 4. Post-Release Verification

#### Install via pipx
```bash
pipx install jj-agent
jj doctor
jj version
```

#### Install via Docker
```bash
docker pull ghcr.io/ORG/jj-agent:v0.1.0
docker run --rm ghcr.io/ORG/jj-agent:v0.1.0 jj version
```

#### Production Mode Test
```bash
export JJ_ENV=production
export JJ_PROD_STRICT=1
export OPENAI_API_KEY=sk-...

# Test capabilities enforcement
jj run --dry-run "Create FastAPI skeleton" --workspace ~/code/demo

# Test full execution
jj run "Create a FastAPI app with JWT auth and PostgreSQL" --workspace ~/code/demo
```

#### Verify Production Features
- [ ] `capabilities.prod.yaml` strictly enforced
- [ ] Sandboxed runner works (if Docker available)
- [ ] LocalSafe runner works
- [ ] Audit logs generated in `state/<job-id>/audit.jsonl`
- [ ] No forbidden paths allowed
- [ ] No forbidden commands allowed
- [ ] Job completes successfully
- [ ] Health endpoints respond (`/healthz`, `/readyz`)
- [ ] Metrics endpoint works (`/metrics`)

## Post-Release

### Announcements
- [ ] Update README with release badge
- [ ] Create GitHub Release notes
- [ ] Announce on communication channels

### Monitoring
- [ ] Monitor error rates
- [ ] Check metrics
- [ ] Review audit logs
- [ ] Monitor PyPI downloads
- [ ] Monitor Docker pulls

## Next Steps

After v0.1.0 is stable:
1. Begin v0.2.0 development
2. Implement web search integration
3. Expand skills library
4. Improve RAG capabilities
5. Add plan caching

