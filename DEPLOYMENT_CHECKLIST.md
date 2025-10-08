# Deployment Checklist

Use this checklist to ensure your Hugo portfolio is properly configured before deploying to GitHub Pages.

## Pre-Deployment Setup

### 1. Theme Installation
- [ ] Run `git submodule add --depth=1 https://github.com/adityatelange/hugo-PaperMod.git themes/PaperMod`
- [ ] Run `git submodule update --init --recursive`
- [ ] Verify `themes/PaperMod/theme.toml` exists

### 2. Configuration Updates

Edit `config.yml` and update:

- [ ] `baseURL` - Change to your GitHub Pages URL
  ```yaml
  baseURL: "https://YOUR-USERNAME.github.io/"
  ```

- [ ] `title` - Your site title
  ```yaml
  title: "Your Portfolio Title"
  ```

- [ ] `params.author` - Your name
  ```yaml
  params:
    author: "Your Name"
  ```

- [ ] Social links - Update all URLs
  ```yaml
  socialIcons:
    - name: github
      url: "https://github.com/YOUR-USERNAME"
    - name: linkedin
      url: "https://linkedin.com/in/YOUR-USERNAME"
    - name: email
      url: "mailto:your.email@example.com"
  ```

- [ ] `params.description` - Site description
- [ ] `params.keywords` - SEO keywords

### 3. Content Customization

- [ ] Edit `content/about.md` with your information
- [ ] Review sample articles:
  - [ ] Keep, modify, or delete `content/philosophy/kant-categorical-imperative.md`
  - [ ] Keep, modify, or delete `content/literature/dostoevsky-notes-underground.md`
  - [ ] Keep, modify, or delete `content/essays/on-translation.md`
- [ ] Add at least one of your own articles

### 4. Repository Setup

- [ ] Repository is named correctly:
  - Option A: `YOUR-USERNAME.github.io` (user site)
  - Option B: Any name (project site, adjust baseURL accordingly)
- [ ] Repository is public (required for free GitHub Pages)
- [ ] All files committed to `main` branch

### 5. File Verification

Run verification script:
```bash
bash verify-setup.sh
```

Or manually check:
- [ ] `config.yml` exists and is valid YAML
- [ ] `.github/workflows/hugo.yml` exists
- [ ] `content/` directory has articles
- [ ] `themes/PaperMod/` is populated
- [ ] `.gitmodules` includes PaperMod reference

## Deployment Process

### Step 1: Commit All Changes

```bash
# Check status
git status

# Add all files
git add .

# Commit
git commit -m "feat: Initial Hugo portfolio setup"

# Push to GitHub
git push origin main
```

**Verify**:
- [ ] All files pushed successfully
- [ ] GitHub shows latest commit

### Step 2: Enable GitHub Pages

1. Go to your repository on GitHub
2. Click **Settings** (gear icon)
3. Click **Pages** in left sidebar
4. Under **Source**:
   - [ ] Select **GitHub Actions** (not "Deploy from a branch")
5. Click **Save**

**Verify**:
- [ ] Source shows "GitHub Actions"
- [ ] No error messages

### Step 3: Monitor Deployment

1. Go to **Actions** tab in your repository
2. You should see a workflow run starting
3. Wait for it to complete (usually 1-2 minutes)

**Verify**:
- [ ] Workflow shows green checkmark ✓
- [ ] No failed steps
- [ ] "Deploy Hugo site to Pages" completed successfully

### Step 4: Access Your Site

1. In repository settings → Pages, find your site URL
2. Visit `https://YOUR-USERNAME.github.io/`

**Verify**:
- [ ] Site loads without errors
- [ ] Homepage displays correctly
- [ ] Navigation menu works
- [ ] Articles are accessible
- [ ] Theme styling applied
- [ ] Search works
- [ ] Archives page works

## Post-Deployment Verification

### Content Checks
- [ ] All articles display properly
- [ ] Images load correctly
- [ ] Internal links work
- [ ] Tags page works
- [ ] Categories work
- [ ] About page displays

### Functionality Checks
- [ ] Search functionality works
- [ ] Light/Dark theme toggle works
- [ ] Mobile responsive design
- [ ] Table of contents displays (if enabled)
- [ ] Share buttons work
- [ ] RSS feed accessible (`/index.xml`)

### SEO Checks
- [ ] Visit `https://YOUR-SITE/sitemap.xml` - should load
- [ ] View page source - verify meta tags present
- [ ] Verify Open Graph tags
- [ ] Check that descriptions are correct

### Performance Checks
- [ ] Page loads quickly
- [ ] Images load without delay
- [ ] No console errors (F12 → Console)
- [ ] Links have no 404 errors

## Common Issues & Fixes

### ❌ Build Fails

**Check**:
- GitHub Actions logs (Actions tab → Click on failed run)
- YAML syntax in `config.yml` (use [YAML Lint](http://www.yamllint.com/))
- Front matter in all articles is valid YAML

**Fix**:
```bash
# Validate config
hugo --config config.yml --verbose

# Check for errors in output
```

### ❌ Theme Not Applied

**Check**:
- Theme submodule initialized
- `themes/PaperMod/` directory exists and has content

**Fix**:
```bash
git submodule update --init --recursive
git add themes/
git commit -m "Fix theme submodule"
git push
```

### ❌ 404 Error on Site

**Check**:
- GitHub Pages is enabled (Settings → Pages)
- Source is set to "GitHub Actions"
- Workflow completed successfully
- `baseURL` in config.yml matches your site URL

**Fix**:
```yaml
# config.yml
baseURL: "https://YOUR-USERNAME.github.io/"  # Must match exactly
```

### ❌ Articles Not Appearing

**Check each article**:
- `draft: false` in front matter
- Valid YAML front matter syntax
- File in correct category directory

**Fix**:
```yaml
---
draft: false  # Change from true to false
---
```

### ❌ Images Not Loading

**Check**:
- Images in `static/images/` directory
- Markdown uses `/images/filename.jpg` (with leading slash)
- File names match exactly (case-sensitive)
- Images committed to git

**Fix**:
```markdown
# Correct
![Alt text](/images/photo.jpg)

# Incorrect (missing leading slash)
![Alt text](images/photo.jpg)
```

### ❌ Search Not Working

**Check**:
- `content/search.md` exists
- `config.yml` includes JSON output format

**Fix** `config.yml`:
```yaml
outputs:
  home:
    - HTML
    - RSS
    - JSON  # Required for search
```

## Optimization After Deployment

### Performance
- [ ] Add compression for images (use tools like TinyPNG)
- [ ] Enable caching headers (GitHub Pages does this automatically)
- [ ] Consider CDN for images if many/large

### SEO
- [ ] Submit sitemap to Google Search Console
  - URL: `https://YOUR-SITE/sitemap.xml`
- [ ] Submit to Bing Webmaster Tools
- [ ] Add Google Analytics (optional)
  ```yaml
  params:
    analytics:
      google:
        SiteVerificationTag: "YOUR-TAG"
  ```

### Content
- [ ] Add meta descriptions to all articles
- [ ] Use descriptive alt text for images
- [ ] Internal link related articles
- [ ] Maintain consistent tagging

### Social
- [ ] Share on LinkedIn
- [ ] Add to resume/CV
- [ ] Link from GitHub profile
- [ ] Create Open Graph image (1200x630px)

## Regular Maintenance

### Weekly
- [ ] Check for broken links
- [ ] Review Analytics (if enabled)
- [ ] Respond to any feedback

### Monthly
- [ ] Update theme: `git submodule update --remote --merge`
- [ ] Review and update old articles if needed
- [ ] Check for Hugo updates

### Per Article
- [ ] Proofread before publishing
- [ ] Verify all links work
- [ ] Check images display
- [ ] Set appropriate weight for featured articles
- [ ] Add appropriate tags and category

## Final Pre-Launch Checklist

Before sharing your portfolio publicly:

- [ ] All placeholder text replaced with real content
- [ ] All URLs updated from "yourusername" to actual username
- [ ] About page complete and accurate
- [ ] At least 3-5 quality articles published
- [ ] All articles proofread
- [ ] Mobile view tested
- [ ] Shared with trusted friend for feedback
- [ ] Resume/CV updated with portfolio link
- [ ] LinkedIn profile updated
- [ ] GitHub profile README includes link

## Success Criteria

Your portfolio is successfully deployed when:

✅ Site loads at your GitHub Pages URL
✅ All pages accessible (Home, Philosophy, Literature, Essays, About, Archives, Search)
✅ Articles display with correct formatting
✅ Theme styling applied correctly
✅ Navigation works on all pages
✅ Responsive on mobile devices
✅ Search returns results
✅ No console errors
✅ Fast page load times
✅ Professional appearance

## Next Steps After Deployment

1. **Content Strategy**
   - Plan regular posting schedule
   - Build content calendar
   - Identify topics to cover

2. **Promotion**
   - Share on social media
   - Add to professional profiles
   - Consider cross-posting on Medium
   - Engage with philosophy/literature communities

3. **Improvement**
   - Gather feedback
   - Iterate on design
   - Add features as needed
   - Keep content fresh and updated

4. **Analytics**
   - Monitor which articles get traffic
   - Understand your audience
   - Adjust content strategy accordingly

---

## Need Help?

- **Setup Issues**: See `QUICKSTART.md`
- **Configuration**: See `README.md`
- **Adding Content**: See `CONTRIBUTING.md`
- **Structure Questions**: See `PROJECT_STRUCTURE.md`
- **Post-Setup**: See `SETUP_COMPLETE.md`

## Verification Command

Run this to check everything:

```bash
bash verify-setup.sh
```

---

**Good luck with your deployment! 🚀**

Once live, don't forget to share your portfolio link!