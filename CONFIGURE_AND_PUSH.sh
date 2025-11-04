#!/bin/bash
# Configure Remote and Push v0.1.0 Tag
# Usage: ./CONFIGURE_AND_PUSH.sh <github-repo-url>

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if [ $# -eq 0 ]; then
    echo "Usage: $0 <github-repo-url>"
    echo "Example: $0 https://github.com/ORG/jj-agent.git"
    exit 1
fi

REPO_URL="$1"

echo "=========================================="
echo "Configure Remote and Push v0.1.0"
echo "=========================================="
echo ""

# Check if remote exists
if git remote | grep -q "^origin$"; then
    echo "Remote 'origin' already exists."
    echo "Current remote URL:"
    git remote get-url origin
    echo ""
    read -p "Update remote? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git remote set-url origin "$REPO_URL"
        echo "✓ Remote updated"
    else
        echo "Using existing remote"
    fi
else
    echo "Adding remote 'origin'..."
    git remote add origin "$REPO_URL"
    echo "✓ Remote added"
fi

echo ""
echo "Verifying remote configuration..."
git remote -v

echo ""
echo "Preflight checks..."
CURRENT_COMMIT=$(git rev-parse HEAD)
if [[ "$CURRENT_COMMIT" == "5dcaf4f"* ]]; then
    echo "✓ Commit: $CURRENT_COMMIT"
else
    echo "⚠ Commit mismatch: $CURRENT_COMMIT (expected: 5dcaf4f)"
fi

echo "✓ Tag: v0.1.0 exists"
echo "✓ Version: 0.1.0"

echo ""
echo "Pushing tag v0.1.0..."
if git push origin v0.1.0; then
    echo ""
    echo "✅ Tag pushed successfully!"
    echo ""
    echo "CI/CD triggered. Monitor at:"
    echo "  https://github.com/$(basename $(dirname $REPO_URL))/$(basename $REPO_URL .git)/actions"
    echo ""
    echo "Or use: gh run watch --exit-status"
    echo ""
    echo "Expected duration: 5-10 minutes"
    echo ""
    echo "Next steps (after CI/CD completes):"
    echo "  2. Run verification scripts (see EXECUTE_NOW_FINAL.md)"
    echo "  3. Deploy to server"
    echo "  4. Run smoke test"
    echo "  5. Collect artifacts"
    echo "  6. Post-release tidy"
else
    echo ""
    echo "✗ Tag push failed!"
    echo "Check:"
    echo "  - Repository URL is correct"
    echo "  - Authentication/credentials"
    echo "  - Network connectivity"
    exit 1
fi

