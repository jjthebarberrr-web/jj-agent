#!/bin/bash
# v0.1.0 Release Execution with Preflight Checks
# This script executes the complete release process with safety checks

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "v0.1.0 Release Execution"
echo "=========================================="
echo ""

# 0) Preflight Checks
echo "[0] Preflight Checks"
echo "-------------------"
echo ""

echo "1. Checking current commit..."
CURRENT_COMMIT=$(git rev-parse HEAD)
EXPECTED_COMMIT="5dcaf4f"
if [[ "$CURRENT_COMMIT" == "$EXPECTED_COMMIT"* ]]; then
    echo "   ✓ Commit matches: $CURRENT_COMMIT"
else
    echo "   ✗ Commit mismatch! Expected: $EXPECTED_COMMIT, Got: $CURRENT_COMMIT"
    echo "   Please ensure you're on the correct commit"
    exit 1
fi

echo ""
echo "2. Checking version consistency..."
VERSION_FILES=("pyproject.toml" "jj_agent/__init__.py" "CHANGELOG.md")
VERSION_OK=true

for file in "${VERSION_FILES[@]}"; do
    if grep -q "0\.1\.0" "$file" 2>/dev/null; then
        echo "   ✓ $file contains 0.1.0"
    else
        echo "   ✗ $file missing or incorrect version"
        VERSION_OK=false
    fi
done

if [ "$VERSION_OK" = false ]; then
    echo "   Version consistency check failed!"
    exit 1
fi

echo ""
echo "3. Checking CI secrets..."
if [ -z "${PYPI_API_TOKEN:-}" ]; then
    echo "   ⚠ WARNING: PYPI_API_TOKEN not set (CI must have this)"
else
    echo "   ✓ PYPI_API_TOKEN is set"
fi

if [ -z "${GITHUB_TOKEN:-}" ] && [ -z "${GHCR_TOKEN:-}" ]; then
    echo "   ⚠ WARNING: GITHUB_TOKEN/GHCR_TOKEN not set (CI must have this)"
else
    echo "   ✓ GITHUB_TOKEN/GHCR_TOKEN is set"
fi

echo ""
echo "✅ Preflight checks passed"
echo ""

# 1) Push Tag
echo "[1] Pushing Release Tag"
echo "----------------------"
echo ""

# Ensure tag exists
if ! git tag -l | grep -q "^v0.1.0$"; then
    echo "Creating tag v0.1.0..."
    git tag -a v0.1.0 -m "Release v0.1.0 - Production Ready"
fi

echo "Pushing tag to origin..."
if git push origin v0.1.0; then
    echo "✅ Tag pushed successfully"
    echo ""
    echo "CI/CD triggered. Monitor at:"
    echo "  https://github.com/ORG/jj-agent/actions"
    echo ""
    echo "Or use: gh run watch --exit-status"
else
    echo "✗ Tag push failed!"
    echo "Check remote configuration and permissions"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ Step 1 Complete: Tag Pushed"
echo "=========================================="
echo ""
echo "Next steps (after CI/CD completes):"
echo "  2. Run verification scripts"
echo "  3. Deploy to server"
echo "  4. Run production smoke test"
echo "  5. Collect artifacts"
echo ""
echo "See EXECUTE_NOW.md for complete instructions."
echo ""

