#!/bin/bash
# Complete Release Execution Script
# Executes preflight, tag push, and prepares for verification

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "v0.1.0 Release Execution - Complete"
echo "=========================================="
echo ""

# 0) Preflight
echo "[0] Preflight Checks"
echo "-------------------"

# Check commit
CURRENT_COMMIT=$(git rev-parse HEAD)
if [[ "$CURRENT_COMMIT" == "5dcaf4f"* ]]; then
    echo "✓ Commit matches: $CURRENT_COMMIT"
else
    echo "✗ Commit mismatch! Expected: 5dcaf4f, Got: $CURRENT_COMMIT"
    exit 1
fi

# Check version consistency
echo "✓ Checking version consistency..."
grep -q "0\.1\.0" pyproject.toml || { echo "✗ pyproject.toml version mismatch"; exit 1; }
grep -q "0\.1\.0" jj_agent/__init__.py || { echo "✗ jj_agent/__init__.py version mismatch"; exit 1; }
grep -q "0\.1\.0" CHANGELOG.md || { echo "✗ CHANGELOG.md version mismatch"; exit 1; }
echo "✓ Version consistent across all files"

# Check secrets (warn only)
if [ -z "${PYPI_API_TOKEN:-}" ]; then
    echo "⚠ WARNING: PYPI_API_TOKEN not set (CI must have this)"
else
    echo "✓ PYPI_API_TOKEN is set"
fi

if [ -z "${GITHUB_TOKEN:-}" ] && [ -z "${GHCR_TOKEN:-}" ]; then
    echo "⚠ WARNING: GITHUB_TOKEN/GHCR_TOKEN not set (CI must have this)"
else
    echo "✓ GITHUB_TOKEN/GHCR_TOKEN is set"
fi

echo ""
echo "✅ Preflight checks passed"
echo ""

# 1) Push Tag
echo "[1] Pushing Release Tag"
echo "----------------------"

# Ensure tag exists
if ! git tag -l | grep -q "^v0.1.0$"; then
    echo "Creating tag v0.1.0..."
    git tag -a v0.1.0 -m "Release v0.1.0 - Production Ready"
fi

echo "Pushing tag to origin..."
if git push origin v0.1.0 2>&1; then
    echo ""
    echo "✅ Tag pushed successfully!"
    echo ""
    echo "CI/CD triggered. Monitor at:"
    echo "  https://github.com/ORG/jj-agent/actions"
    echo ""
    echo "Or use: gh run watch --exit-status"
else
    echo ""
    echo "✗ Tag push failed!"
    echo "Check remote configuration: git remote -v"
    echo "Check permissions and try manually: git push origin v0.1.0"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ Release Tag Pushed"
echo "=========================================="
echo ""
echo "Next steps (after CI/CD completes ~5-10 min):"
echo ""
echo "2. Run verification:"
echo "   Linux:  ./verify_prod.sh | tee verify_prod_linux.log"
echo "   Windows: .\\verify_prod.ps1 *>&1 | Tee-Object verify_prod_windows.log"
echo ""
echo "3. Deploy to server (see RELEASE_EXECUTION.md)"
echo ""
echo "4. Run smoke test"
echo ""
echo "5. Collect artifacts (see ARTIFACTS_COLLECTION_FINAL.md)"
echo ""
echo "6. Post-release tidy:"
echo "   ./POST_RELEASE_TIDY.sh"
echo "   ./CREATE_ROADMAP_PR.sh"
echo ""

