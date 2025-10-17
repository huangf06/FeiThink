# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Hugo static site project using the PaperMod theme, designed as a Philosophy & Literature Portfolio. The site is deployed to GitHub Pages via GitHub Actions and features academic content including philosophical translations, literary works, and personal essays.

## Essential Commands

### Local Development
```bash
# Start development server with drafts
hugo server -D

# Start development server (published content only)
hugo server

# Build site for production
hugo --gc --minify
```

### Content Management
```bash
# Create new philosophy article
hugo new philosophy/article-name.md

# Create new literature article
hugo new literature/article-name.md

# Create new essay
hugo new essays/article-name.md
```

### Theme Management
```bash
# Initialize/update theme submodule
git submodule update --init --recursive

# Update PaperMod theme to latest version
git submodule update --remote --merge
```

### Deployment
```bash
# Quick deployment using existing script
./auto-deploy.sh

# Manual git deployment (commits and pushes to trigger GitHub Actions)
git add .
git commit -m "Your commit message"
git push origin main
```

## Architecture & Key Components

### Hugo Configuration
- **config.yml**: Main configuration file containing site settings, theme parameters, menu structure, and taxonomy definitions
- **baseURL**: Currently set to `https://huangf06.github.io/GitStack/` - must match actual deployment URL
- **Hugo Version**: 0.146.0 (specified in `.github/workflows/hugo.yml`)

### Content Organization
- **content/** directory structure:
  - `philosophy/`: Philosophical translations and analyses
  - `literature/`: Literary translations and works
  - `essays/`: Personal essays and reflections
  - `about.md`: About page
  - `archives.md`: Archives listing
  - `search.md`: Search page configuration

### Deployment Pipeline
- **GitHub Actions**: Automatic deployment via `.github/workflows/hugo.yml`
  - Triggers on push to main branch
  - Builds with Hugo Extended 0.146.0
  - Deploys to GitHub Pages
- **Local Scripts**:
  - `auto-deploy.sh`: Automated setup and deployment
  - `deploy.sh`, `deploy-simple.sh`: Alternative deployment options
  - Scripts handle submodule initialization automatically

### Theme Integration
- **PaperMod Theme**: Added as git submodule in `themes/PaperMod/`
- Features enabled: search (Fuse.js), table of contents, reading time, breadcrumbs
- Customization points: `config.yml` params section, custom CSS via `assets/css/extended/`

## Front Matter Template

All content files should include this front matter structure:
```yaml
---
title: "Article Title"
date: 2025-10-08
lastmod: 2025-10-08
draft: false
categories: ["Essays"]  # or ["Literature"], ["Philosophy"]
tags: [tag1, tag2, tag3]  # Use kebab-case; minimum 3 tags
summary: "Brief description (50-100 words)"
weight: 999
author: "FeiThink"
showToc: true
TocOpen: false
---
```

**Important Notes:**
- All required fields must be completed
- Tags must use kebab-case (lowercase with hyphens)
- Summary should be 50-100 words describing the article's core content
- `weight: 999` is default; use lower numbers to promote articles
- For detailed format guidelines, see `ARTICLE_FORMAT.md`

## Project-Specific Considerations

### Multi-Environment Scripts
The repository contains both Linux shell scripts (.sh) and Windows batch files (.bat) for deployment operations, supporting cross-platform development.

### Submodule Handling
The PaperMod theme is a git submodule. Always ensure submodules are initialized when cloning or after pulling updates that modify `.gitmodules`.

### GitHub Pages Configuration
- Repository must be named `[username].github.io` or configured with custom domain
- GitHub Actions workflow handles the build and deployment automatically
- Pages source must be set to "GitHub Actions" in repository settings

### Content Categories
The site uses a taxonomy system with three main categories (Philosophy, Literature, Essays) and a flexible tag system. Menu items and navigation are configured to reflect this structure.

### Search Functionality
Client-side search is enabled via Fuse.js. The site generates JSON output for search indexing. Search configuration is in `config.yml` under `fuseOpts`.