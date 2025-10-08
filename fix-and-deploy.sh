#!/bin/bash
set -e

echo "🔧 Fixing and deploying Hugo site..."
cd /mnt/e/GitStack

echo "📝 Staging all files..."
git add .

echo "💾 Committing..."
git commit -m "fix: Add .nojekyll and ensure proper Hugo deployment" || echo "No changes to commit"

echo "🚀 Pushing to GitHub..."
git push origin main

echo ""
echo "✅ Done! GitHub Actions is building your site now."
echo "⏰ Wait 1-2 minutes, then visit:"
echo "   https://huangf06.github.io/GitStack/"
echo ""
