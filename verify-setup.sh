#!/bin/bash

# Hugo Portfolio Setup Verification Script
# This script checks that all required files and configurations are in place

echo "========================================"
echo "Hugo Portfolio Setup Verification"
echo "========================================"
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

errors=0
warnings=0

# Function to check file exists
check_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✓${NC} $1 exists"
        return 0
    else
        echo -e "${RED}✗${NC} $1 is missing"
        ((errors++))
        return 1
    fi
}

# Function to check directory exists
check_dir() {
    if [ -d "$1" ]; then
        echo -e "${GREEN}✓${NC} $1 exists"
        return 0
    else
        echo -e "${RED}✗${NC} $1 is missing"
        ((errors++))
        return 1
    fi
}

# Function to check for string in file
check_content() {
    if grep -q "$2" "$1" 2>/dev/null; then
        echo -e "${GREEN}✓${NC} $1 contains '$2'"
        return 0
    else
        echo -e "${YELLOW}!${NC} $1 missing '$2' (warning)"
        ((warnings++))
        return 1
    fi
}

echo "Checking directory structure..."
echo "================================"
check_dir "content"
check_dir "content/philosophy"
check_dir "content/literature"
check_dir "content/essays"
check_dir "static"
check_dir ".github"
check_dir ".github/workflows"
check_dir "archetypes"
echo ""

echo "Checking configuration files..."
echo "==============================="
check_file "config.yml"
check_file ".github/workflows/hugo.yml"
check_file "archetypes/default.md"
check_file ".gitignore"
echo ""

echo "Checking content files..."
echo "========================="
check_file "content/about.md"
check_file "content/archives.md"
check_file "content/search.md"
echo ""

echo "Checking documentation..."
echo "========================="
check_file "README.md"
check_file "CONTRIBUTING.md"
check_file "QUICKSTART.md"
echo ""

echo "Checking theme..."
echo "================="
if [ -d "themes/PaperMod" ]; then
    echo -e "${GREEN}✓${NC} PaperMod theme directory exists"
    if [ -f "themes/PaperMod/theme.toml" ]; then
        echo -e "${GREEN}✓${NC} PaperMod theme is properly initialized"
    else
        echo -e "${RED}✗${NC} PaperMod theme appears empty"
        echo "   Run: git submodule update --init --recursive"
        ((errors++))
    fi
else
    echo -e "${RED}✗${NC} PaperMod theme is missing"
    echo "   Run: git submodule add https://github.com/adityatelange/hugo-PaperMod.git themes/PaperMod"
    ((errors++))
fi
echo ""

echo "Checking configuration content..."
echo "=================================="
check_content "config.yml" "theme: PaperMod"
check_content "config.yml" "baseURL:"
check_content ".github/workflows/hugo.yml" "actions/deploy-pages"
echo ""

echo "Checking Git repository..."
echo "=========================="
if [ -d ".git" ]; then
    echo -e "${GREEN}✓${NC} Git repository initialized"

    # Check for submodules
    if [ -f ".gitmodules" ]; then
        echo -e "${GREEN}✓${NC} Git submodules configured"
    else
        echo -e "${YELLOW}!${NC} No .gitmodules file (warning)"
        echo "   Run: git submodule add https://github.com/adityatelange/hugo-PaperMod.git themes/PaperMod"
        ((warnings++))
    fi

    # Check current branch
    branch=$(git branch --show-current 2>/dev/null)
    if [ "$branch" = "main" ]; then
        echo -e "${GREEN}✓${NC} On 'main' branch"
    else
        echo -e "${YELLOW}!${NC} Current branch: '$branch' (expected 'main')"
        ((warnings++))
    fi
else
    echo -e "${RED}✗${NC} Not a Git repository"
    ((errors++))
fi
echo ""

echo "Checking Hugo installation..."
echo "============================="
if command -v hugo &> /dev/null; then
    version=$(hugo version 2>&1)
    echo -e "${GREEN}✓${NC} Hugo is installed: $version"
else
    echo -e "${YELLOW}!${NC} Hugo is not installed locally (optional)"
    echo "   GitHub Actions will build without local Hugo"
    echo "   To test locally, install Hugo: https://gohugo.io/installation/"
fi
echo ""

echo "========================================"
echo "Summary"
echo "========================================"
if [ $errors -eq 0 ] && [ $warnings -eq 0 ]; then
    echo -e "${GREEN}✓ All checks passed!${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Update config.yml with your information"
    echo "2. Edit content/about.md"
    echo "3. Add your own articles to content/"
    echo "4. Commit and push to GitHub"
    echo "5. Enable GitHub Pages (Settings → Pages → GitHub Actions)"
elif [ $errors -eq 0 ]; then
    echo -e "${YELLOW}Setup complete with $warnings warnings${NC}"
    echo ""
    echo "Review warnings above and address if needed."
    echo "You can proceed with deployment."
else
    echo -e "${RED}Found $errors errors and $warnings warnings${NC}"
    echo ""
    echo "Please fix the errors above before deploying."
    exit 1
fi

echo ""
echo "See QUICKSTART.md for next steps."
