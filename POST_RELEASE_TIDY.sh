#!/bin/bash
# Post-Release Tidy Script
# Bumps version to 0.1.1-dev and prepares for v0.2.0 development

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "Post-Release Tidy: Bump to 0.1.1-dev"
echo "=========================================="
echo ""

# Update version in files
echo "Updating version to 0.1.1-dev..."

# Update jj_agent/__init__.py
if [ -f "jj_agent/__init__.py" ]; then
    sed -i.bak 's/__version__ = os.getenv("JJ_VERSION", "0\.1\.0")/__version__ = os.getenv("JJ_VERSION", "0.1.1-dev")/' jj_agent/__init__.py
    rm -f jj_agent/__init__.py.bak
    echo "  Updated jj_agent/__init__.py"
fi

# Update config.py
if [ -f "config.py" ]; then
    sed -i.bak 's/self.version = os.getenv("JJ_VERSION", "0\.1\.0")/self.version = os.getenv("JJ_VERSION", "0.1.1-dev")/' config.py
    rm -f config.py.bak
    echo "  Updated config.py"
fi

echo ""
echo "Version bumped to 0.1.1-dev"
echo ""
echo "Next steps:"
echo "  1. Review changes: git diff"
echo "  2. Commit: git commit -am 'Bump version to 0.1.1-dev'"
echo "  3. Push: git push origin master"
echo "  4. Create v0.2.0 roadmap PR (see v0.2.0_ROADMAP_PR.md)"
echo ""

