#!/bin/bash
cd /e/GitStack
git submodule add --depth=1 https://github.com/adityatelange/hugo-PaperMod.git themes/PaperMod
git submodule update --init --recursive
git add .
git commit -m "feat: Initial Hugo portfolio setup with PaperMod theme"
git push -u origin main
echo "Done! Now go to GitHub Settings -> Pages -> Select 'GitHub Actions'"
