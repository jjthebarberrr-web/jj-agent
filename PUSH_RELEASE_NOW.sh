#!/bin/bash
# Push v0.1.0 Release Tag
# This script configures the remote (if needed) and pushes the tag

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# REPLACE THIS WITH YOUR GITHUB REPO URL
GITHUB_REPO_URL="${GITHUB_REPO_URL:-}"

if [ -z "$GITHUB_REPO_URL" ]; then
    echo "ERROR: GITHUB_REPO_URL not set"
    echo ""
    echo "Usage:"
    echo "  export GITHUB_REPO_URL='https://github.com/YOUR-ORG/jj-agent.git'"
    echo "  ./PUSH_RELEASE_NOW.sh"
    echo ""
    echo "Or set inline:"
    echo "  GITHUB_REPO_URL='https://github.com/YOUR-ORG/jj-agent.git' ./PUSH_RELEASE_NOW.sh"
    exit 1
fi

echo "=========================================="
echo "Push v0.1.0 Release Tag"
echo "=========================================="
echo ""
echo "Repository URL: $GITHUB_REPO_URL"
echo ""

# Check if remote exists
if git remote | grep -q "^origin$"; then
    CURRENT_URL=$(git remote get-url origin)
    if [ "$CURRENT_URL" != "$GITHUB_REPO_URL" ]; then
        echo "Remote 'origin' exists with different URL:"
        echo "  Current: $CURRENT_URL"
        echo "  New:     $GITHUB_REPO_URL"
        echo ""
        read -p "Update remote? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            git remote set-url origin "$GITHUB_REPO_URL"
            echo "✓ Remote updated"
        else
            echo "Using existing remote"
        fi
    else
        echo "✓ Remote 'origin' already configured correctly"
    fi
else
    echo "Adding remote 'origin'..."
    git remote add origin "$GITHUB_REPO_URL"
    echo "✓ Remote added"
fi

echo ""
echo "Verifying remote configuration..."
git remote -v

echo ""
echo "Preflight checks..."
CURRENT_COMMIT=$(git rev-parse HEAD)
echo "  Commit: $CURRENT_COMMIT"
if git tag -l | grep -q "^v0.1.0$"; then
    echo "  Tag: v0.1.0 exists ✓"
else
    echo "  Tag: v0.1.0 missing ✗"
    exit 1
fi

echo "  Version: 0.1.0 ✓"

echo ""
echo "Pushing tag v0.1.0..."
if git push origin v0.1.0; then
    echo ""
    echo "✅ Tag pushed successfully!"
    echo ""
    echo "CI/CD triggered. Monitor at:"
    REPO_NAME=$(basename "$GITHUB_REPO_URL" .git)
    REPO_ORG=$(basename $(dirname "$GITHUB_REPO_URL"))
    echo "  https://github.com/$REPO_ORG/$REPO_NAME/actions"
    echo ""
    echo "Or use: gh run watch --exit-status"
    echo ""
    echo "Expected duration: 5-10 minutes"
    echo ""
    echo "Next steps (after CI/CD completes):"
    echo "  See: EXECUTE_NOW_FINAL.md"
else
    echo ""
    echo "✗ Tag push failed!"
    echo "Check:"
    echo "  - Repository URL is correct"
    echo "  - Authentication/credentials"
    echo "  - Network connectivity"
    exit 1
fi

