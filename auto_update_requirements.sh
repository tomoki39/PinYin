#!/bin/bash

# Auto-update Requirements Documentation Script
# This script generates requirements documentation and commits/pushes changes

echo "🔄 Starting requirements documentation update..."

# Generate documentation
echo "📝 Generating requirements documentation..."
python3 generate_requirements_doc.py

# Check if there are changes
if git diff --quiet docs/; then
    echo "✅ No changes detected in documentation"
    exit 0
fi

# Add changes
echo "📦 Adding changes to git..."
git add docs/

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