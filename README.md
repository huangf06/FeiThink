# FeiThink

A personal blog about philosophy, technology, and life, built with Hugo and hosted on GitHub Pages.

## 🌐 Live Site

Visit: [https://huangf06.github.io/FeiThink/](https://huangf06.github.io/FeiThink/)

## ✨ Features

- **Responsive Design**: Mobile-friendly, clean academic aesthetic
- **Content Organization**: Categories (Philosophy, Literature, Essays) and Tags
- **Search Functionality**: Client-side search powered by Fuse.js
- **SEO Optimized**: Meta tags, sitemap, Open Graph support
- **Theme Toggle**: Automatic/Light/Dark mode
- **Reading Features**:
  - Table of contents
  - Reading time estimates
  - Related articles
  - Code highlighting
- **RSS Feed**: Subscribe to updates
- **Archives**: Timeline view of all posts
- **Social Integration**: GitHub, LinkedIn, Email links

## 🚀 Quick Start

### Prerequisites

- Hugo Extended (v0.110.0 or later)
- Git

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/yourusername.github.io.git
   cd yourusername.github.io
   ```

2. **Initialize submodules** (PaperMod theme)
   ```bash
   git submodule update --init --recursive
   ```

3. **Run local server**
   ```bash
   hugo server -D
   ```

4. **View site**
   Open `http://localhost:1313` in your browser

### Installing Hugo

**macOS:**
```bash
brew install hugo
```

**Windows (Chocolatey):**
```bash
choco install hugo-extended
```

**Linux (Snap):**
```bash
snap install hugo
```

**Or download from**: https://github.com/gohugoio/hugo/releases

## 📝 Adding New Content

### Create a new article

```bash
hugo new philosophy/my-new-article.md
# or
hugo new literature/my-new-article.md
# or
hugo new essays/my-new-article.md
```

This creates a new file with the proper front matter template.

### Front Matter Template

```yaml
---
title: "Article Title"
date: 2025-10-08
lastmod: 2025-10-08
draft: false
categories: ["Philosophy"]  # or ["Literature"], ["Essays"]
tags: ["tag1", "tag2", "tag3"]
summary: "Brief description for SEO and card display"
weight: 999  # Lower numbers appear first in lists
author: "Your Name"
showToc: true
TocOpen: false
---
```

### Publishing

1. **Set draft to false** in front matter
2. **Commit and push**
   ```bash
   git add .
   git commit -m "Add new article: Title"
   git push
   ```
3. **GitHub Actions automatically builds and deploys** (takes 1-2 minutes)

## 📁 Project Structure

```
.
├── .github/
│   └── workflows/
│       └── hugo.yml          # GitHub Actions deployment
├── archetypes/
│   └── default.md            # Template for new posts
├── content/
│   ├── philosophy/           # Philosophy articles
│   ├── literature/           # Literature articles
│   ├── essays/               # Personal essays
│   ├── about.md              # About page
│   ├── archives.md           # Archives page
│   └── search.md             # Search page
├── static/
│   ├── images/               # Images
│   └── css/                  # Custom CSS (if needed)
├── themes/
│   └── PaperMod/             # Theme submodule
├── config.yml                # Main configuration
└── README.md
```

## ⚙️ Configuration

### Update Your Information

Edit `config.yml`:

1. **Base URL**: Change `baseURL` to your GitHub Pages URL
2. **Personal Info**: Update `author`, `title`, `description`
3. **Social Links**: Update GitHub, LinkedIn, Email URLs
4. **Menu**: Customize navigation if needed

### Enable Google Analytics (Optional)

Uncomment in `config.yml`:
```yaml
params:
  analytics:
    google:
      SiteVerificationTag: "YOUR-TAG-HERE"
```

### Enable Comments (Optional)

PaperMod supports giscus/utterances. See [PaperMod docs](https://github.com/adityatelange/hugo-PaperMod/wiki/Features#comments).

## 🎨 Customization

### Change Theme Settings

Edit `config.yml` under `params:` section:
- Enable/disable profile mode on homepage
- Adjust social icons
- Modify menu items
- Configure search options

### Add Custom CSS

Create `assets/css/extended/custom.css` and add your styles.

### Modify About Page

Edit `content/about.md` with your background and philosophy.

## 🚢 Deployment

### GitHub Pages Setup

1. **Go to repository Settings → Pages**
2. **Source**: Select "GitHub Actions"
3. **Custom domain** (optional): Add your domain and enable HTTPS

### Automatic Deployment

Every push to `main` branch triggers automatic deployment via GitHub Actions.

Monitor deployment: `Actions` tab in your GitHub repository.

## 📋 Maintenance

### Update Theme

```bash
git submodule update --remote --merge
git commit -am "Update PaperMod theme"
git push
```

### Update Hugo Version

Edit `.github/workflows/hugo.yml` and change `HUGO_VERSION`.

## 🛠️ Troubleshooting

### Build Fails

1. Check GitHub Actions logs in repository
2. Verify `config.yml` syntax
3. Ensure all front matter is valid YAML
4. Check that theme submodule is initialized

### Styles Look Wrong

1. Clear browser cache
2. Check baseURL matches your actual URL
3. Verify theme submodule is up to date

### Search Not Working

1. Ensure `config.yml` includes JSON output format
2. Verify `content/search.md` exists with correct front matter

## 📚 Resources

- **Hugo Documentation**: https://gohugo.io/documentation/
- **PaperMod Theme**: https://github.com/adityatelange/hugo-PaperMod
- **PaperMod Wiki**: https://github.com/adityatelange/hugo-PaperMod/wiki
- **Hugo Forums**: https://discourse.gohugo.io/

## 📄 License

Content: © Your Name. All rights reserved.

Theme (PaperMod): MIT License

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on adding articles and improving the site.

---

Built with ❤️ using [Hugo](https://gohugo.io/) and [PaperMod](https://github.com/adityatelange/hugo-PaperMod)
