#!/bin/bash
cd /e/GitStack
git add config.yml
git commit -m "fix: Update baseURL to correct GitHub Pages URL"
git push origin main
echo "Updated! Wait 1-2 minutes then check: https://huangf06.github.io/GitStack/"
