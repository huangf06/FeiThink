# Deploy Your Portfolio NOW! 🚀

Follow these steps **exactly** to deploy your Hugo portfolio.

## Prerequisites

- GitHub account
- Git installed
- Repository created on GitHub

---

## Step 1: Add PaperMod Theme

Open your terminal (PowerShell, WSL, or Git Bash) and run:

```bash
cd /mnt/e/GitStack

git submodule add --depth=1 https://github.com/adityatelange/hugo-PaperMod.git themes/PaperMod

git submodule update --init --recursive
```

**Expected output**: "Cloning into..." and theme files downloaded.

---

## Step 2: Update Configuration

Open `config.yml` and change these lines:

### Line 1: Update baseURL
```yaml
# Change this:
baseURL: "https://yourusername.github.io/"

# To your actual URL (one of these):
baseURL: "https://YOUR-GITHUB-USERNAME.github.io/blog-portfolio/"
# OR if your repo is named YOUR-USERNAME.github.io:
baseURL: "https://YOUR-GITHUB-USERNAME.github.io/"
```

### Lines ~25-27: Update author
```yaml
params:
  author: "Your Real Name"  # Change this
```

### Lines ~85-92: Update social links
```yaml
socialIcons:
  - name: github
    url: "https://github.com/YOUR-ACTUAL-USERNAME"  # Change this
  - name: linkedin
    url: "https://linkedin.com/in/YOUR-LINKEDIN"    # Change this
  - name: email
    url: "mailto:your.actual.email@example.com"     # Change this
```

**Save the file!**

---

## Step 3: Verify Everything

Run the verification script:

```bash
cd /mnt/e/GitStack
bash verify-setup.sh
```

**Fix any errors** it reports before continuing.

---

## Step 4: Check Git Remote

Make sure you have a GitHub repository ready:

```bash
cd /mnt/e/GitStack

# Check if remote exists
git remote -v
```

### If NO remote shown:

**First, create a repository on GitHub:**
1. Go to https://github.com/new
2. Name it `blog-portfolio` (or `YOUR-USERNAME.github.io`)
3. Make it **Public**
4. **DON'T** initialize with README
5. Click "Create repository"

**Then add the remote:**
```bash
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPO-NAME.git
```

### If remote exists:
✓ You're good! Continue to next step.

---

## Step 5: Commit Everything

```bash
cd /mnt/e/GitStack

# Stage all files
git add .

# Check what will be committed
git status

# Commit
git commit -m "feat: Initial Hugo portfolio setup with PaperMod theme"
```

---

## Step 6: Push to GitHub

```bash
git push -u origin main
```

**If this fails** with "branch main doesn't exist", try:
```bash
git branch -M main
git push -u origin main
```

**Expected**: Progress bar showing files uploading, then "done".

---

## Step 7: Enable GitHub Pages

1. **Go to your repository** on GitHub:
   - `https://github.com/YOUR-USERNAME/YOUR-REPO-NAME`

2. **Click Settings** tab (top right)

3. **Click Pages** in left sidebar

4. **Under "Source"**:
   - Select: **GitHub Actions** (NOT "Deploy from a branch")
   - Click Save if needed

5. **Wait for deployment**:
   - Click **Actions** tab
   - You should see a workflow running
   - Wait for green checkmark ✓ (1-2 minutes)

---

## Step 8: Visit Your Site! 🎉

Your site is now live at:

**If repo name is `blog-portfolio`:**
```
https://YOUR-USERNAME.github.io/blog-portfolio/
```

**If repo name is `YOUR-USERNAME.github.io`:**
```
https://YOUR-USERNAME.github.io/
```

---

## Troubleshooting

### "Theme not found" error

```bash
cd /mnt/e/GitStack
git submodule update --init --recursive
git add themes/
git commit -m "Fix theme submodule"
git push
```

### "404 Page Not Found"

1. Check GitHub Pages is enabled (Settings → Pages → Source: GitHub Actions)
2. Verify `baseURL` in config.yml matches your actual URL exactly
3. Wait another minute - deployment can take time

### Build fails in Actions tab

1. Click on the failed workflow
2. Read the error message
3. Common issues:
   - Invalid YAML in `config.yml` - check indentation
   - Invalid front matter in articles - check `---` delimiters

### Site loads but no styling

```bash
cd /mnt/e/GitStack
git submodule update --init --recursive
git add .
git commit -m "Update theme"
git push
```

---

## Alternative: Use the Deployment Script

If you prefer, run the automated script:

```bash
cd /mnt/e/GitStack
bash deploy.sh
```

This script will guide you through all the steps interactively.

---

## After Deployment Checklist

Once your site is live:

- [ ] Visit site and verify it loads
- [ ] Check navigation menu works
- [ ] Test search functionality
- [ ] Verify articles display correctly
- [ ] Test on mobile device
- [ ] Update `content/about.md` with your info
- [ ] Remove or replace sample articles
- [ ] Add your own content

---

## Quick Reference Commands

```bash
# Add new article
hugo new philosophy/my-article.md

# Update and push
git add .
git commit -m "Add article: Title"
git push

# Check deployment status
# Go to: https://github.com/YOUR-USERNAME/YOUR-REPO/actions
```

---

## Need Help?

**Stuck on a step?** Check:
- `DEPLOYMENT_CHECKLIST.md` - Detailed checklist
- `QUICKSTART.md` - Quick start guide
- `README.md` - Full documentation

**Common issues:**
- Forgot to update config.yml → Edit and push again
- Theme not loading → Run submodule update command
- 404 error → Check baseURL matches your actual URL

---

## Success! 🎉

Once deployed:
1. Share your portfolio link
2. Add it to your resume/CV
3. Update LinkedIn profile
4. Start adding your articles!

**Your portfolio URL:**
```
https://YOUR-USERNAME.github.io/blog-portfolio/
```

(Replace with your actual username and repo name)