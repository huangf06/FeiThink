#!/bin/bash

# Deployment Script for FeiThink
# This script handles the full deployment process for the blog

set -e  # Exit on error

echo "======================================="
echo " FeiThink - Deployment Script"
echo "======================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored messages
print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_info() {
    echo -e "${YELLOW}➜${NC} $1"
}

# Check if we're in the right directory
if [ ! -f "config.yml" ]; then
    print_error "Error: config.yml not found. Please run this script from the root of your Hugo site."
    exit 1
fi

# Step 1: Update git submodules (PaperMod theme)
print_info "Updating theme submodules..."
git submodule update --init --recursive
print_success "Theme submodules updated"

# Step 2: Clean previous build
print_info "Cleaning previous build artifacts..."
rm -rf public/
rm -rf resources/_gen/
print_success "Previous build cleaned"

# Step 3: Check for Hugo installation
if ! command -v hugo &> /dev/null; then
    print_error "Hugo is not installed. Please install Hugo first."
    print_info "Visit: https://gohugo.io/getting-started/installing/"
    exit 1
fi

# Step 4: Build the site
print_info "Building site with Hugo..."
hugo --gc --minify --buildDrafts=false

if [ $? -eq 0 ]; then
    print_success "Site built successfully"
else
    print_error "Build failed. Please check the error messages above."
    exit 1
fi

# Step 5: Check if public directory was created
if [ ! -d "public" ]; then
    print_error "Build directory 'public' not found. Build may have failed."
    exit 1
fi

# Step 6: Display build statistics
echo ""
print_info "Build Statistics:"
echo "  Total files: $(find public -type f | wc -l)"
echo "  HTML files: $(find public -name "*.html" | wc -l)"
echo "  CSS files: $(find public -name "*.css" | wc -l)"
echo "  Total size: $(du -sh public | cut -f1)"

# Step 7: Git operations
echo ""
print_info "Preparing for deployment..."

# Check git status
if [[ $(git status --porcelain) ]]; then
    print_info "Uncommitted changes detected. Adding and committing..."

    # Add all changes
    git add .

    # Create commit message with timestamp
    TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
    COMMIT_MSG="feat: Update bilingual portfolio - $TIMESTAMP

- Added/updated bilingual content in dialogues, reflections, critiques sections
- Enhanced CSS for bilingual display
- Updated timeline and essential reads
- Improved navigation structure"

    git commit -m "$COMMIT_MSG"
    print_success "Changes committed"
else
    print_info "No uncommitted changes detected"
fi

# Step 8: Push to GitHub
echo ""
read -p "Do you want to push to GitHub? (y/n): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_info "Pushing to GitHub..."
    git push origin main

    if [ $? -eq 0 ]; then
        print_success "Successfully pushed to GitHub"
        print_info "GitHub Actions will now build and deploy your site"
        echo ""
        print_success "Deployment initiated successfully!"
        echo ""
        echo "======================================="
        echo " Your site will be available at:"
        echo " https://huangf06.github.io/FeiThink/"
        echo " (May take 2-5 minutes for changes to appear)"
        echo "======================================="
    else
        print_error "Push failed. Please check your GitHub credentials and connection."
        exit 1
    fi
else
    print_info "Skipping push to GitHub"
    echo ""
    print_success "Build completed locally. Run 'git push origin main' when ready to deploy."
fi

# Step 9: Optional local preview
echo ""
read -p "Would you like to preview the site locally? (y/n): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_info "Starting local server at http://localhost:1313"
    print_info "Press Ctrl+C to stop the server"
    hugo server -D
fi

print_success "Script completed successfully!"