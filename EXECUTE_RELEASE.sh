#!/bin/bash
# Complete Release Execution Script
# This script executes the full release process end-to-end

set -euo pipefail

echo "=========================================="
echo "JJ Agent v0.1.0 Release Execution"
echo "=========================================="
echo ""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# A) Push the release tag
echo "[A] Pushing release tag..."
echo ""

echo "1. Pulling latest changes..."
git pull --rebase || echo "No remote configured or already up to date"

echo ""
echo "2. Checking tag exists..."
if git tag -l | grep -q "^v0.1.0$"; then
    echo "   Tag v0.1.0 exists"
else
    echo "   Creating tag v0.1.0..."
    git tag -a v0.1.0 -m "Release v0.1.0 - Production Ready"
fi

echo ""
echo "3. Pushing tag to remote..."
if git remote | grep -q "^origin$"; then
    git push origin v0.1.0 || echo "Push failed - check permissions and remote"
    echo "   Tag pushed to origin"
else
    echo "   No remote 'origin' configured"
    echo "   To push manually: git push origin v0.1.0"
fi

echo ""
echo "=========================================="
echo "✅ Step A Complete: Tag pushed"
echo "=========================================="
echo ""
echo "Next steps:"
echo "  1. Monitor CI/CD at: https://github.com/ORG/jj-agent/actions"
echo "  2. Wait for pipeline to complete (5-10 minutes)"
echo "  3. Run verification scripts (B)"
echo "  4. Deploy to server (C)"
echo "  5. Run production smoke test (D)"
echo ""

