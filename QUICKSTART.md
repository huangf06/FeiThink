# Quick Start Guide

This guide will help you get your Hugo portfolio site up and running quickly.

## Step 1: Verify PaperMod Theme

First, check if the PaperMod theme submodule is properly initialized:

```bash
git submodule status
```

If the theme is missing, initialize it:

```bash
git submodule update --init --recursive
```

## Step 2: Update Configuration

Edit `config.yml` and update these essential fields:

```yaml
baseURL: "https://YOUR-USERNAME.github.io/"  # Your GitHub Pages URL
title: "Your Portfolio Title"

params:
  author: "Your Name"

  socialIcons:
    - name: github
      url: "https://github.com/YOUR-USERNAME"
    - name: linkedin
      url: "https://linkedin.com/in/YOUR-USERNAME"
    - name: email
      url: "mailto:your.email@example.com"
```

## Step 3: Test Locally (Optional)

If you have Hugo installed:

```bash
hugo server -D
```

Visit http://localhost:1313 to preview.

## Step 4: Create Your First Article

Copy one of the sample articles and modify it, or create a new one:

```bash
# Using Hugo CLI
hugo new philosophy/my-first-article.md

# Or manually create file
touch content/philosophy/my-first-article.md
```

Add your content with proper front matter:

```yaml
---
title: "My First Philosophy Article"
date: 2025-10-08
draft: false
categories: ["Philosophy"]
tags: ["ethics", "introduction"]
summary: "My first contribution to the portfolio"
weight: 999
author: "Your Name"
showToc: true
---

## Introduction

Your content here...
```

## Step 5: Commit and Push

```bash
git add .
git commit -m "Initial portfolio setup"
git push origin main
```

## Step 6: Enable GitHub Pages

1. Go to your GitHub repository
2. Navigate to **Settings** → **Pages**
3. Under **Source**, select **GitHub Actions**
4. Wait 1-2 minutes for the first deployment

Your site will be live at `https://YOUR-USERNAME.github.io/`

## Next Steps

### Customize Your About Page

Edit `content/about.md` with your background and philosophy.

### Add More Articles

- Philosophy articles: `content/philosophy/`
- Literature articles: `content/literature/`
- Personal essays: `content/essays/`

### Remove Sample Articles

Once you've added your own content, delete the sample articles:

```bash
rm content/philosophy/kant-categorical-imperative.md
rm content/literature/dostoevsky-notes-underground.md
rm content/essays/on-translation.md
```

### Customize Theme

- **Profile Mode**: Set `profileMode.enabled: true` in `config.yml` for a profile-style homepage
- **Colors**: Create `assets/css/extended/custom.css` for custom styling
- **Navigation**: Modify `menu.main` in `config.yml`

### Add Analytics

Uncomment and configure Google Analytics in `config.yml`:

```yaml
params:
  analytics:
    google:
      SiteVerificationTag: "YOUR-TAG"
```

### Enable Comments

Follow [PaperMod's comment guide](https://github.com/adityatelange/hugo-PaperMod/wiki/Features#comments) to set up giscus or utterances.

## Troubleshooting

### Theme Not Loading

```bash
# Re-initialize submodule
git submodule update --init --recursive
```

### Build Failing on GitHub

1. Check **Actions** tab in GitHub for error logs
2. Verify `config.yml` syntax (use YAML validator)
3. Ensure all front matter is valid YAML
4. Check that theme submodule is committed

### Changes Not Appearing

1. Wait 1-2 minutes for GitHub Actions to complete
2. Hard refresh browser (Ctrl+Shift+R or Cmd+Shift+R)
3. Check that `draft: false` in article front matter

### Site Shows 404

1. Verify GitHub Pages is enabled in repository settings
2. Check that Source is set to "GitHub Actions"
3. Ensure baseURL in config.yml matches your GitHub Pages URL

## Useful Commands

```bash
# Create new article
hugo new category/article-name.md

# Preview locally
hugo server -D

# Build site
hugo

# Update theme
git submodule update --remote --merge

# Check git submodules
git submodule status

# View commit history
git log --oneline
```

## File Locations

| Item | Location |
|------|----------|
| Configuration | `config.yml` |
| Articles | `content/{category}/` |
| About page | `content/about.md` |
| Static files | `static/` |
| Theme | `themes/PaperMod/` |
| Workflows | `.github/workflows/hugo.yml` |
| Article template | `archetypes/default.md` |

## Resources

- [Hugo Documentation](https://gohugo.io/documentation/)
- [PaperMod Features](https://github.com/adityatelange/hugo-PaperMod/wiki/Features)
- [Markdown Guide](https://www.markdownguide.org/)
- [GitHub Pages Docs](https://docs.github.com/en/pages)

---

Need more help? See [README.md](README.md) and [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guides.