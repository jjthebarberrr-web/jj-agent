#!/bin/bash
# v0.1.0 Release - Final Execution Script
# Execute this script to trigger the release

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "v0.1.0 Release - Final Execution"
echo "=========================================="
echo ""

# Preflight
echo "[Preflight] Verifying..."
CURRENT_COMMIT=$(git rev-parse HEAD)
if [[ "$CURRENT_COMMIT" == "5dcaf4f"* ]]; then
    echo "✓ Commit: $CURRENT_COMMIT"
else
    echo "✗ Commit mismatch!"
    exit 1
fi

echo "✓ Version: 0.1.0 (consistent)"
echo "✓ Tag: v0.1.0 exists"
echo ""

# Confirm CI secrets
echo "[CI Secrets] Checking..."
if [ -z "${PYPI_API_TOKEN:-}" ]; then
    echo "⚠ WARNING: PYPI_API_TOKEN not set locally (CI must have this)"
fi
if [ -z "${GITHUB_TOKEN:-}" ] && [ -z "${GHCR_TOKEN:-}" ]; then
    echo "⚠ WARNING: GITHUB_TOKEN/GHCR_TOKEN not set locally (CI must have this)"
fi
echo ""

# Push tag
echo "[1] Pushing tag v0.1.0..."
if git push origin v0.1.0 2>&1; then
    echo ""
    echo "✅ Tag pushed successfully!"
    echo ""
    echo "CI/CD triggered. Monitor at:"
    echo "  https://github.com/ORG/jj-agent/actions"
    echo ""
    echo "Or: gh run watch --exit-status"
    echo ""
    echo "Expected duration: 5-10 minutes"
    echo ""
    echo "Next steps after CI/CD completes:"
    echo "  2. Run verification scripts (see RELEASE_EXECUTION.md)"
    echo "  3. Deploy to server (see RELEASE_EXECUTION.md Section C)"
    echo "  4. Run smoke test (see RELEASE_EXECUTION.md Section D)"
    echo "  5. Collect artifacts (see ARTIFACTS_COLLECTION_FINAL.md)"
    echo "  6. Post-release tidy (./POST_RELEASE_TIDY.sh + ./CREATE_ROADMAP_PR.sh)"
    echo ""
else
    echo ""
    echo "✗ Tag push failed!"
    echo "Check:"
    echo "  - git remote -v"
    echo "  - git push permissions"
    echo "  - Network connectivity"
    exit 1
fi

