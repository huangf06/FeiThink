#!/bin/bash
cd /mnt/e/GitStack
git pull origin main
git add config.yml
git commit -m "fix: Update config for Hugo 0.146.0 compatibility (pagination and privacy settings)"
git push origin main
echo "Done! Check https://huangf06.github.io/GitStack/ in 1-2 minutes"
