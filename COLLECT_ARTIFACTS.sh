#!/bin/bash
# Artifact Collection Script
# Run this after completing all verification steps

set -euo pipefail

ARTIFACTS_DIR="release_artifacts_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$ARTIFACTS_DIR"

echo "=========================================="
echo "Collecting Release Artifacts"
echo "=========================================="
echo ""

# CI/CD Links
echo "[1] Collecting CI/CD links..."
cat > "$ARTIFACTS_DIR/ci_links.txt" <<EOF
GitHub Release: https://github.com/ORG/jj-agent/releases/tag/v0.1.0
PyPI: https://pypi.org/project/jj-agent/0.1.0/
Docker Image: ghcr.io/ORG/jj-agent:v0.1.0
EOF

# Get Docker digest if available
if command -v docker > /dev/null 2>&1; then
    if docker pull ghcr.io/ORG/jj-agent:v0.1.0 > /dev/null 2>&1; then
        docker inspect ghcr.io/ORG/jj-agent:v0.1.0 --format='{{index .RepoDigests 0}}' >> "$ARTIFACTS_DIR/ci_links.txt" 2>&1 || true
    fi
fi

echo "✓ CI/CD links saved to $ARTIFACTS_DIR/ci_links.txt"

# Verification logs
echo ""
echo "[2] Collecting verification logs..."
if [ -f "verify_prod_linux.log" ]; then
    cp verify_prod_linux.log "$ARTIFACTS_DIR/"
    echo "✓ Linux verification log copied"
else
    echo "⚠ Linux verification log not found"
fi

if [ -f "verify_prod_windows.log" ]; then
    cp verify_prod_windows.log "$ARTIFACTS_DIR/"
    echo "✓ Windows verification log copied"
else
    echo "⚠ Windows verification log not found"
fi

# Server proof
echo ""
echo "[3] Collecting server proof..."
if command -v curl > /dev/null 2>&1; then
    curl -sS http://127.0.0.1:5858/healthz > "$ARTIFACTS_DIR/healthz.txt" 2>&1 || echo "Health endpoint not reachable" > "$ARTIFACTS_DIR/healthz.txt"
    curl -sS http://127.0.0.1:5858/readyz > "$ARTIFACTS_DIR/readyz.txt" 2>&1 || echo "Ready endpoint not reachable" > "$ARTIFACTS_DIR/readyz.txt"
    echo "✓ Health endpoints saved"
fi

if command -v systemctl > /dev/null 2>&1 && [ -n "${SUDO_USER:-}" ]; then
    sudo systemctl status jj-agent --no-pager > "$ARTIFACTS_DIR/systemd_status.txt" 2>&1 || echo "Service not running" > "$ARTIFACTS_DIR/systemd_status.txt"
    echo "✓ Systemd status saved"
fi

if command -v journalctl > /dev/null 2>&1 && [ -n "${SUDO_USER:-}" ]; then
    sudo journalctl -u jj-agent -n 30 -o json 2>&1 | tail -20 > "$ARTIFACTS_DIR/json_logs.txt" || echo "Logs not available" > "$ARTIFACTS_DIR/json_logs.txt"
    echo "✓ JSON logs saved"
fi

# Policy proof
echo ""
echo "[4] Collecting policy proof..."
if [ -d "state" ]; then
    find state -name "audit.jsonl" -exec cat {} \; 2>/dev/null | jq 'select(.result.denied == true)' 2>/dev/null | head -5 > "$ARTIFACTS_DIR/policy_proof.txt" || echo "No denials found" > "$ARTIFACTS_DIR/policy_proof.txt"
    echo "✓ Policy proof saved"
fi

# Smoke test
echo ""
echo "[5] Collecting smoke test results..."
if [ -d "$HOME/code/demo" ]; then
    ls -la "$HOME/code/demo" > "$ARTIFACTS_DIR/smoke_test_files.txt" 2>&1 || true
    echo "✓ Smoke test files listed"
fi

echo ""
echo "=========================================="
echo "✅ Artifacts collected in: $ARTIFACTS_DIR"
echo "=========================================="
echo ""
ls -la "$ARTIFACTS_DIR"
echo ""
echo "Review artifacts and submit as per ARTIFACTS_COLLECTION_FINAL.md"
echo ""

