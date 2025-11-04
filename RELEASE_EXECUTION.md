# v0.1.0 Release Execution Guide

## Complete End-to-End Release Process

This guide walks through the complete release execution from tag push to verification.

## A) Push Release Tag

### Automated (Recommended)

**Unix/Linux/macOS:**
```bash
chmod +x EXECUTE_RELEASE.sh
./EXECUTE_RELEASE.sh
```

**Windows PowerShell:**
```powershell
.\EXECUTE_RELEASE.ps1
```

### Manual

```bash
cd jj-agent

# Pull latest
git pull --rebase

# Verify tag exists
git tag -l v0.1.0

# Push tag (triggers CI/CD)
git push origin v0.1.0
```

### Monitor CI/CD

**GitHub CLI:**
```bash
gh run watch --exit-status
gh release view v0.1.0
```

**Or watch in browser:**
- https://github.com/ORG/jj-agent/actions

**Expected Duration:** 5-10 minutes

## B) Verification Scripts

### After CI/CD Completes

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

**Expected Output:**
- All checks pass (✓)
- Warnings acceptable (⚠)
- No failures (✗)

## C) Server Deployment (Production)

### Install & Configure Service

```bash
# Create user
sudo useradd -r -s /usr/sbin/nologin jj || true

# Create directories
sudo mkdir -p /etc/jj-agent /var/log/jj
sudo chown jj:jj /var/log/jj

# Copy capabilities
sudo cp capabilities.prod.yaml /etc/jj-agent/

# Create environment file
sudo tee /etc/jj-agent/jj.env > /dev/null <<EOF
JJ_ENV=production
TZ=America/Phoenix
OPENAI_API_KEY=sk-YOUR-KEY-HERE
EOF

# Install agent
pipx install "jj-agent==0.1.0"

# Install service
sudo cp jj-agent.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now jj-agent
```

### Health Checks

```bash
# Test endpoints
curl -sS http://127.0.0.1:5858/healthz
curl -sS http://127.0.0.1:5858/readyz

# Check logs
journalctl -u jj-agent --since "10 min ago" -o json | head -n 50
```

**Expected Output:**
- `/healthz`: `{"status":"healthy","version":"0.1.0"}`
- `/readyz`: `{"status":"ready","version":"0.1.0"}`
- JSON logs with structured format

## D) Production Smoke Test

```bash
export JJ_ENV=production
export JJ_PROD_STRICT=1
export OPENAI_API_KEY=sk-YOUR-KEY-HERE

# Run full job
jj run "Create a FastAPI app with JWT auth and PostgreSQL" \
  --workspace ~/code/demo

# Verify output
ls -la ~/code/demo/
cat ~/code/demo/requirements.txt
```

**Expected:**
- Job completes successfully
- Files created in workspace
- Audit logs generated
- No policy violations

## E) Artifacts to Collect

### CI/CD Links

1. **GitHub Release URL:**
   ```
   https://github.com/ORG/jj-agent/releases/tag/v0.1.0
   ```

2. **PyPI Package URL:**
   ```
   https://pypi.org/project/jj-agent/0.1.0/
   ```

3. **Docker Image Digest:**
   ```bash
   docker pull ghcr.io/ORG/jj-agent:v0.1.0
   docker inspect ghcr.io/ORG/jj-agent:v0.1.0 | jq '.[0].RepoDigests'
   ```
   Example: `ghcr.io/ORG/jj-agent:v0.1.0@sha256:abc123...`

### Verification Logs

- `verify_prod_linux.log` - Linux verification output
- `verify_prod_windows.log` - Windows verification output

### Server Proof

1. **Health Endpoints:**
   ```bash
   curl -sS http://127.0.0.1:5858/healthz
   curl -sS http://127.0.0.1:5858/readyz
   ```

2. **Systemd Status:**
   ```bash
   sudo systemctl status jj-agent --no-pager
   ```

3. **JSON Logs:**
   ```bash
   journalctl -u jj-agent --since "10 min ago" -o json | jq '.' | head -20
   ```

4. **Policy Proof (Denial Test):**
   ```bash
   # This should fail with denial
   jj run "cat /etc/shadow" --workspace /tmp 2>&1 | tee denial_test.log
   
   # Check audit log for denial entry
   cat state/*/audit.jsonl | jq 'select(.result.denied == true)' | head -5
   ```

### Final Checklist

From `PRODUCTION_READY.md`:

- [x] Production mode enforced
- [x] Capabilities file required
- [x] Sandboxing available
- [x] Audit logging enabled
- [x] Secrets redacted
- [x] Metrics collected
- [x] Health endpoints available
- [x] CI/CD pipeline configured
- [x] Documentation complete

## F) Post-Release Tidy

### Version Bump

```bash
# Update version to 0.1.1-dev
sed -i 's/0\.1\.0/0.1.1-dev/g' jj_agent/__init__.py
sed -i 's/0\.1\.0/0.1.1-dev/g' config.py

# Commit
git add jj_agent/__init__.py config.py
git commit -m "Bump version to 0.1.1-dev"
git push origin master
```

### Create v0.2.0 Roadmap PR

Create a PR with:
- Web search integration
- RAG improvements
- Skills library expansion
- Faster planning & caching

See `ROADMAP.md` for details.

## Troubleshooting

### CI/CD Fails
- Check GitHub Actions logs
- Verify secrets are set
- Check Docker registry permissions

### Verification Fails
- Review `RELEASE_VERIFICATION.md`
- Check audit logs
- Verify capabilities file

### Service Won't Start
- Check `journalctl -u jj-agent`
- Verify capabilities file exists
- Check permissions

## Support

For issues:
1. Check `RELEASE_VERIFICATION.md`
2. Review `OPERATIONS.md`
3. Check GitHub Issues
4. Review audit logs

