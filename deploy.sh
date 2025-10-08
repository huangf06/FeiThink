#!/bin/bash

# Hugo Portfolio Deployment Script
# Run this script to deploy your portfolio

set -e  # Exit on error

echo "========================================"
echo "Hugo Portfolio Deployment"
echo "========================================"
echo ""

# Navigate to project directory
cd /mnt/e/GitStack || exit 1
echo "✓ Changed to project directory"

# Check if we're in a git repo
if [ ! -d ".git" ]; then
    echo "✗ Error: Not a git repository"
    exit 1
fi

echo "✓ Git repository confirmed"
echo ""

# Step 1: Add PaperMod theme
echo "Step 1: Adding PaperMod theme..."
if [ -d "themes/PaperMod/.git" ]; then
    echo "✓ PaperMod theme already exists"
else
    echo "  Adding theme as git submodule..."
    git submodule add --depth=1 https://github.com/adityatelange/hugo-PaperMod.git themes/PaperMod
    echo "✓ Theme added successfully"
fi
echo ""

# Step 2: Initialize submodules
echo "Step 2: Initializing submodules..."
git submodule update --init --recursive
echo "✓ Submodules initialized"
echo ""

# Step 3: Check for required config updates
echo "Step 3: Checking configuration..."
if grep -q "yourusername" config.yml; then
    echo "⚠ WARNING: config.yml still contains 'yourusername'"
    echo "  Please update the following in config.yml:"
    echo "  - baseURL (line with yourusername.github.io)"
    echo "  - author name"
    echo "  - social links (github, linkedin, email)"
    echo ""
    read -p "Have you updated config.yml? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Please update config.yml first, then run this script again"
        exit 1
    fi
fi
echo "✓ Configuration checked"
echo ""

# Step 4: Stage all files
echo "Step 4: Staging files for commit..."
git add .
echo "✓ Files staged"
echo ""

# Step 5: Show what will be committed
echo "Files to be committed:"
git status --short
echo ""

# Step 6: Commit
echo "Step 5: Committing changes..."
read -p "Enter commit message (or press Enter for default): " commit_msg
if [ -z "$commit_msg" ]; then
    commit_msg="feat: Initial Hugo portfolio setup with PaperMod theme"
fi
git commit -m "$commit_msg"
echo "✓ Changes committed"
echo ""

# Step 7: Check remote
echo "Step 6: Checking remote repository..."
if git remote | grep -q "origin"; then
    remote_url=$(git remote get-url origin)
    echo "✓ Remote 'origin' found: $remote_url"
else
    echo "✗ No remote 'origin' configured"
    echo "  Please add a remote first:"
    echo "  git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPO.git"
    exit 1
fi
echo ""

# Step 8: Push
echo "Step 7: Pushing to GitHub..."
read -p "Ready to push to GitHub? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    git push -u origin main
    echo "✓ Pushed successfully!"
else
    echo "Skipping push. You can push manually later with:"
    echo "  git push -u origin main"
fi
echo ""

echo "========================================"
echo "Deployment Script Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. Go to your GitHub repository"
echo "2. Navigate to Settings → Pages"
echo "3. Under 'Source', select 'GitHub Actions'"
echo "4. Wait 1-2 minutes for deployment"
echo "5. Visit your site!"
echo ""
echo "Your site will be at:"
echo "https://YOUR-USERNAME.github.io/blog-portfolio/"
echo "(or YOUR-USERNAME.github.io if repo name is YOUR-USERNAME.github.io)"
