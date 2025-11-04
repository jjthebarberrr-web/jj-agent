#!/bin/bash
# Create v0.2.0 Roadmap PR
# Creates a PR with the roadmap for v0.2.0 development

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "Creating v0.2.0 Roadmap PR"
echo "=========================================="
echo ""

# Create branch
BRANCH="feature/v0.2.0-roadmap"
echo "Creating branch: $BRANCH"
git checkout -b "$BRANCH" 2>/dev/null || git checkout "$BRANCH"

# Ensure roadmap file exists
if [ ! -f "v0.2.0_ROADMAP_PR.md" ]; then
    echo "Error: v0.2.0_ROADMAP_PR.md not found"
    exit 1
fi

# Add roadmap file
git add v0.2.0_ROADMAP_PR.md

# Create commit
echo "Creating commit..."
git commit -m "Add v0.2.0 roadmap: Web search, RAG improvements, skills expansion, faster planning" || echo "No changes to commit"

echo ""
echo "PR Ready!"
echo ""
echo "Next steps:"
echo "  1. Push branch: git push -u origin $BRANCH"
echo "  2. Create PR: gh pr create --title 'v0.2.0 Roadmap' --body-file v0.2.0_ROADMAP_PR.md"
echo "   Or: Visit GitHub and create PR from $BRANCH"
echo ""

