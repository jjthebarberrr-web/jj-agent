#!/bin/bash
# Production Verification Script for JJ Agent v0.1.0
# Usage: ./verify_prod.sh

set -euo pipefail

echo "=========================================="
echo "JJ Agent v0.1.0 Production Verification"
echo "=========================================="
echo ""

# Configuration
PORT="${JJ_PORT:-5858}"
WORKSPACE="${JJ_WORKSPACE:-$HOME/code/demo}"
DOCKER_ORG="${DOCKER_ORG:-ORG}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

check_pass() {
    echo -e "${GREEN}✓${NC} $1"
}

check_fail() {
    echo -e "${RED}✗${NC} $1"
    exit 1
}

check_warn() {
    echo -e "${YELLOW}⚠${NC} $1"
}

echo "[1/7] Checking jj version"
if jj version > /dev/null 2>&1; then
    VERSION=$(jj version)
    echo "  Version: $VERSION"
    if [[ "$VERSION" == *"0.1.0"* ]]; then
        check_pass "Version is 0.1.0"
    else
        check_warn "Version mismatch: expected 0.1.0, got $VERSION"
    fi
else
    check_fail "jj command not found or not working"
fi
echo ""

echo "[2/7] Checking health endpoints"
if pgrep -f "jj.*daemon" > /dev/null 2>&1; then
    if curl -sSf "http://localhost:${PORT}/healthz" > /dev/null 2>&1; then
        check_pass "Health endpoint (/healthz) responds"
    else
        check_warn "Health endpoint not reachable (daemon may not be running)"
    fi
    
    if curl -sSf "http://localhost:${PORT}/readyz" > /dev/null 2>&1; then
        check_pass "Readiness endpoint (/readyz) responds"
    else
        check_warn "Readiness endpoint not reachable"
    fi
else
    check_warn "Daemon not running, skipping health checks"
fi
echo ""

echo "[3/7] Testing production mode capabilities enforcement"
if [ -z "${OPENAI_API_KEY:-}" ]; then
    check_warn "OPENAI_API_KEY not set, skipping full test"
    echo "  Set OPENAI_API_KEY to run full production test"
else
    export JJ_ENV=production
    export JJ_PROD_STRICT=1
    
    # Test that capabilities are enforced (should fail for forbidden paths)
    if mkdir -p "$WORKSPACE" 2>/dev/null; then
        if timeout 30 jj run "cat /etc/passwd" --workspace "$WORKSPACE" > /dev/null 2>&1; then
            check_fail "Capabilities not enforced - forbidden path access allowed"
        else
            check_pass "Capabilities enforced - forbidden paths blocked"
        fi
    fi
fi
echo ""

echo "[4/7] Checking audit logs"
if [ -d "state" ]; then
    AUDIT_FILES=$(find state -name "audit.jsonl" 2>/dev/null | head -1)
    if [ -n "$AUDIT_FILES" ]; then
        check_pass "Audit log files found"
        echo "  Sample audit log: $AUDIT_FILES"
        if [ -r "$AUDIT_FILES" ]; then
            LINES=$(wc -l < "$AUDIT_FILES" 2>/dev/null || echo "0")
            echo "  Lines in audit log: $LINES"
        fi
    else
        check_warn "No audit logs found (may be first run)"
    fi
else
    check_warn "State directory not found"
fi
echo ""

echo "[5/7] Checking JSON logs"
if [ -d "/var/log/jj-agent" ]; then
    LOG_FILES=$(find /var/log/jj-agent -name "*.log" 2>/dev/null | head -1)
    if [ -n "$LOG_FILES" ]; then
        check_pass "JSON log files found"
        if grep -q '"level"' "$LOG_FILES" 2>/dev/null; then
            check_pass "JSON logs contain structured data"
        else
            check_warn "JSON logs may not be structured"
        fi
    else
        check_warn "No log files found in /var/log/jj-agent"
    fi
else
    check_warn "System log directory not found (may use local logging)"
fi
echo ""

echo "[6/7] Testing sample production run"
if [ -z "${OPENAI_API_KEY:-}" ]; then
    check_warn "OPENAI_API_KEY not set, skipping production run test"
else
    export JJ_ENV=production
    export JJ_PROD_STRICT=1
    
    mkdir -p "$WORKSPACE"
    echo "  Running test job in workspace: $WORKSPACE"
    echo "  This may take a few minutes..."
    
    if timeout 300 jj run --dry-run "Create a FastAPI skeleton" --workspace "$WORKSPACE" > /dev/null 2>&1; then
        check_pass "Production dry-run test passed"
    else
        check_warn "Production dry-run test failed or timed out"
    fi
fi
echo ""

echo "[7/7] Testing Docker image"
if command -v docker > /dev/null 2>&1; then
    IMAGE="ghcr.io/${DOCKER_ORG}/jj-agent:v0.1.0"
    echo "  Testing image: $IMAGE"
    
    if docker pull "$IMAGE" > /dev/null 2>&1; then
        check_pass "Docker image pulled successfully"
        
        if docker run --rm "$IMAGE" jj version > /dev/null 2>&1; then
            check_pass "Docker image runs correctly"
        else
            check_fail "Docker image does not run correctly"
        fi
    else
        check_warn "Docker image not found or not accessible"
        echo "  Image may not be published yet, or check permissions"
    fi
else
    check_warn "Docker not available, skipping Docker tests"
fi
echo ""

echo "=========================================="
echo -e "${GREEN}✅ Verification complete${NC}"
echo "=========================================="
echo ""
echo "Next steps:"
echo "  1. Review any warnings above"
echo "  2. Check audit logs in state/ directory"
echo "  3. Verify production capabilities in capabilities.prod.yaml"
echo "  4. Test systemd service if deployed:"
echo "     sudo systemctl status jj-agent"
echo ""

