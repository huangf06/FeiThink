# Project Structure Guide

This document explains the organization and purpose of each file and directory in your Hugo portfolio.

## Directory Tree

```
GitStack/ (Hugo Portfolio Root)
│
├── .github/
│   └── workflows/
│       └── hugo.yml                    # GitHub Actions deployment workflow
│
├── .git/                               # Git repository data (hidden)
│
├── archetypes/
│   └── default.md                      # Template for new content (hugo new)
│
├── content/                            # All your content lives here
│   ├── philosophy/                     # Philosophy category
│   │   └── kant-categorical-imperative.md
│   ├── literature/                     # Literature category
│   │   └── dostoevsky-notes-underground.md
│   ├── essays/                         # Essays category
│   │   └── on-translation.md
│   ├── about.md                        # About page
│   ├── archives.md                     # Archives listing page
│   └── search.md                       # Search page
│
├── static/                             # Static assets (served as-is)
│   ├── images/                         # Images directory
│   ├── css/                            # Custom CSS (optional)
│   ├── favicon.ico                     # Site favicon (add your own)
│   └── .gitkeep                        # Ensures directory is tracked
│
├── themes/
│   └── PaperMod/                       # PaperMod theme (git submodule)
│       ├── layouts/                    # Theme HTML templates
│       ├── assets/                     # Theme CSS/JS
│       ├── static/                     # Theme static files
│       └── theme.toml                  # Theme metadata
│
├── public/                             # Generated site (not in git)
│   └── [Built HTML/CSS/JS]
│
├── resources/                          # Hugo cache (not in git)
│
├── .gitignore                          # Git ignore rules
├── .gitmodules                         # Git submodule configuration
├── config.yml                          # Main Hugo configuration
│
├── README.md                           # Full project documentation
├── CONTRIBUTING.md                     # Article contribution guide
├── QUICKSTART.md                       # Quick start instructions
├── SETUP_COMPLETE.md                   # Post-setup guide
├── PROJECT_STRUCTURE.md                # This file
└── verify-setup.sh                     # Setup verification script
```

## Directory Purposes

### `.github/workflows/`
Contains GitHub Actions workflows for CI/CD.

**hugo.yml**: Automatically builds and deploys your site when you push to `main` branch.
- Triggers on push to main
- Installs Hugo and dependencies
- Builds the site
- Deploys to GitHub Pages

### `archetypes/`
Templates for new content.

**default.md**: The template used when you run `hugo new`. Contains pre-filled front matter structure.

### `content/`
**The heart of your site** - all articles and pages go here.

#### Category Directories
- `philosophy/`: Articles about philosophy, ethics, moral theory
- `literature/`: Literary analysis, book reviews, translations
- `essays/`: Personal reflections, opinion pieces, general writing

**Naming Convention**: Use lowercase with hyphens: `kant-ethics.md`, `dostoevsky-analysis.md`

#### Special Pages
- `about.md`: Your bio, background, contact info
- `archives.md`: Auto-generated timeline of all posts
- `search.md`: Client-side search interface

### `static/`
Files here are served exactly as-is at the site root.

**Use for:**
- Images: `static/images/photo.jpg` → `/images/photo.jpg`
- Favicons: `static/favicon.ico` → `/favicon.ico`
- CSS: `static/css/custom.css` → `/css/custom.css`
- PDFs, downloads, etc.

**Example**: To use an image in markdown:
```markdown
![Alt text](/images/myimage.jpg)
```

### `themes/PaperMod/`
The PaperMod theme (added as git submodule).

**Don't modify theme files directly!** Instead:
- Override layouts by creating files in project root `layouts/`
- Extend CSS by creating `assets/css/extended/custom.css`

### `public/`
Hugo's build output directory (excluded from git).

Contains the final HTML/CSS/JS that gets deployed to GitHub Pages.

**You never need to touch this directly** - Hugo generates it automatically.

### `resources/`
Hugo's cache directory (excluded from git).

Stores processed assets for faster rebuilds.

## File Purposes

### Configuration Files

#### `config.yml`
**The control center** of your site. Controls:
- Site metadata (title, description, author)
- Theme selection and settings
- Menu navigation
- Social links
- Feature toggles
- SEO settings

**When to edit**:
- Changing site info
- Adding/removing menu items
- Configuring features
- Updating social links

#### `.gitignore`
Tells Git which files to ignore.

Excludes:
- `public/` (built output)
- `resources/` (cache)
- `.hugo_build.lock` (build lock file)
- OS files (.DS_Store, Thumbs.db)
- IDE files (.vscode/, .idea/)

#### `.gitmodules`
Tracks git submodules (PaperMod theme).

**Generated automatically** when you add the submodule:
```bash
git submodule add https://github.com/adityatelange/hugo-PaperMod.git themes/PaperMod
```

### Documentation Files

#### `README.md`
Comprehensive guide covering:
- Features overview
- Installation instructions
- Configuration guide
- Deployment process
- Troubleshooting tips

**Audience**: Anyone setting up or maintaining the site.

#### `CONTRIBUTING.md`
Detailed guide for adding articles:
- Front matter reference
- Markdown tips
- Style guidelines
- SEO best practices
- Quality checklist

**Audience**: You (when adding content) and any collaborators.

#### `QUICKSTART.md`
Fast-track setup instructions:
- Minimal steps to get running
- Common customizations
- Quick troubleshooting

**Audience**: Impatient users who want to get started fast.

#### `SETUP_COMPLETE.md`
Post-setup guide:
- What was created
- Next steps required
- Feature overview
- Migration instructions

**Audience**: You (right now after setup completion).

#### `PROJECT_STRUCTURE.md`
This file - explains the project organization.

### Scripts

#### `verify-setup.sh`
Bash script that checks if everything is properly configured:
- Verifies directory structure
- Checks required files exist
- Validates configuration
- Checks theme initialization
- Provides fix suggestions

**Usage**:
```bash
bash verify-setup.sh
```

## Content File Structure

Each article follows this structure:

```markdown
---
# Front Matter (YAML)
title: "Article Title"
date: 2025-10-08
categories: ["Philosophy"]
tags: ["kant", "ethics"]
# ... more metadata
---

# Article Content (Markdown)

## Introduction

Your content...

## Main Sections

### Subsections

More content...

## Conclusion

Final thoughts...
```

### Front Matter Section
YAML metadata between `---` delimiters.

**Purpose**: Tells Hugo about the article (title, date, category, etc.)

### Content Section
Markdown text after front matter.

**Purpose**: The actual article content.

## How Files Relate

### Content → Output
```
content/philosophy/kant.md → public/philosophy/kant/index.html
```

Hugo transforms markdown to HTML based on theme templates.

### Configuration → Behavior
```
config.yml → Controls all site behavior
```

Settings in config.yml affect how Hugo processes content and applies the theme.

### Theme → Appearance
```
themes/PaperMod/ → Provides layouts, styles, scripts
```

The theme defines how content is presented visually.

## Build Process Flow

1. **You write**: `content/philosophy/article.md`
2. **Hugo reads**:
   - `config.yml` for settings
   - `themes/PaperMod/` for layouts
   - `content/` for your content
3. **Hugo processes**:
   - Parses front matter
   - Converts markdown to HTML
   - Applies theme templates
   - Generates navigation, tags, categories
   - Creates RSS, sitemap
4. **Hugo outputs**: `public/philosophy/article/index.html`
5. **GitHub Actions deploys**: `public/` → GitHub Pages

## Customization Locations

### Change Site Info
→ Edit `config.yml`

### Add Article
→ Create file in `content/{category}/`

### Change About Page
→ Edit `content/about.md`

### Add Images
→ Place in `static/images/`

### Custom CSS
→ Create `assets/css/extended/custom.css`

### Modify Layouts
→ Create files in `layouts/` (overrides theme)

### Change Menu
→ Edit `menu.main` in `config.yml`

## Common Operations

### Add New Article
```bash
# Create file
hugo new philosophy/article-name.md

# Or manually
touch content/philosophy/article-name.md
# Add front matter and content
```

### Add Image to Article
```bash
# 1. Copy image to static
cp myimage.jpg static/images/

# 2. Reference in markdown
![Description](/images/myimage.jpg)
```

### Feature Article on Homepage
In article front matter, set:
```yaml
weight: 1  # Lower numbers appear first
```

### Hide Article from Search
```yaml
searchHidden: true
```

### Make Article Draft
```yaml
draft: true  # Won't be published
```

## URL Structure

Hugo generates URLs based on file paths:

| File Location | URL |
|---------------|-----|
| `content/philosophy/kant.md` | `/philosophy/kant/` |
| `content/about.md` | `/about/` |
| `content/essays/translation.md` | `/essays/translation/` |
| `static/images/photo.jpg` | `/images/photo.jpg` |

## Best Practices

### Organization
- Keep categories broad (3-5 total)
- Use tags for specific topics (many possible)
- Use descriptive file names
- Group related articles

### File Naming
- Lowercase with hyphens: `my-article.md`
- Descriptive: `kant-ethics.md` not `article1.md`
- No spaces: `my-article.md` not `my article.md`

### Content Management
- One article per file
- Keep images in `static/images/`
- Organize images by category if many: `static/images/philosophy/`

### Version Control
- Commit articles individually
- Use meaningful commit messages: "Add article: Kant's Ethics"
- Don't commit `public/` or `resources/` (already in .gitignore)

## Development Workflow

### Local Development (Optional)
```bash
# 1. Make changes to content
vim content/philosophy/new-article.md

# 2. Preview locally
hugo server -D

# 3. Check at http://localhost:1313

# 4. Commit when satisfied
git add .
git commit -m "Add article: Title"
git push
```

### Production Deployment (Automatic)
```bash
# Push to GitHub
git push origin main

# GitHub Actions automatically:
# 1. Detects push
# 2. Runs hugo build
# 3. Deploys to GitHub Pages
# 4. Site live in 1-2 minutes
```

## Troubleshooting by Location

### Build Fails
**Check**:
- `.github/workflows/hugo.yml` syntax
- `config.yml` validity (YAML linter)
- Article front matter (valid YAML)

### Theme Not Working
**Check**:
- `themes/PaperMod/` exists and populated
- `.gitmodules` includes PaperMod
- Ran `git submodule update --init --recursive`

### Images Not Showing
**Check**:
- Image in `static/images/`
- Markdown uses `/images/filename.jpg` (with leading slash)
- File name matches exactly (case-sensitive)

### Article Not Appearing
**Check**:
- Front matter has `draft: false`
- File in correct directory (`content/{category}/`)
- Valid front matter (YAML syntax)
- Committed and pushed to GitHub

---

This structure is designed to be simple, maintainable, and scalable as your portfolio grows.