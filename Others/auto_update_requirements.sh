#!/bin/bash

# Auto-update Requirements Documentation Script
# This script generates requirements documentation and commits/pushes changes

echo "🔄 Starting requirements documentation update..."

# Get the project root (parent directory of Others folder)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Change to project root
cd "$PROJECT_ROOT"

# Generate documentation
echo "📝 Generating requirements documentation..."
python3 Others/generate_requirements_doc.py

# Check if there are changes
if git diff --quiet Others/docs/; then
    echo "✅ No changes detected in documentation"
    exit 0
fi

# Add changes
echo "📦 Adding changes to git..."
git add Others/docs/

# Commit changes
echo "💾 Committing changes..."
git commit -m "Auto-update requirements documentation

- Updated requirements specification based on current codebase
- Regenerated auto-generated documentation
- Updated localization data

Generated on: $(date)"

# Push changes
echo "🚀 Pushing changes to remote..."
git push origin main

echo "✅ Requirements documentation updated successfully!" 