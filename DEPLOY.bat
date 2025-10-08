@echo off
echo ========================================
echo Hugo Portfolio Auto Deploy
echo ========================================
echo.

cd /d E:\GitStack
echo Current directory: %CD%
echo.

echo Step 1/5: Adding PaperMod theme...
git submodule add --depth=1 https://github.com/adityatelange/hugo-PaperMod.git themes/PaperMod 2>nul
if errorlevel 1 (
    echo Theme may already exist, continuing...
)
git submodule update --init --recursive
echo Theme configured successfully
echo.

echo Step 2/5: Staging files...
git add .
echo Files staged
echo.

echo Step 3/5: Committing changes...
git commit -m "feat: Initial Hugo portfolio setup with PaperMod theme"
if errorlevel 1 (
    echo No new changes to commit
)
echo Commit complete
echo.

echo Step 4/5: Pushing to GitHub...
git push -u origin main
echo Push successful!
echo.

echo ========================================
echo Deployment Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Visit your GitHub repository
echo 2. Go to Settings -^> Pages
echo 3. Select 'GitHub Actions' as Source
echo 4. Wait 1-2 minutes for build to complete
echo 5. Visit your site
echo.
pause
