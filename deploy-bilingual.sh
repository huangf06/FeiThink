#!/bin/bash

# 双语博客部署脚本
# Bilingual blog deployment script

set -e

echo "🚀 开始部署双语博客 | Deploying bilingual blog..."
echo ""

# 获取当前目录
CURRENT_DIR=$(pwd)
echo "✓ 工作目录 | Working directory: $CURRENT_DIR"

# 1. 初始化子模块
echo ""
echo "🔄 步骤 1/4: 初始化主题子模块 | Initializing theme submodule..."
git submodule update --init --recursive
echo "✓ 子模块初始化完成 | Submodule initialized"

# 2. 添加所有文件
echo ""
echo "📝 步骤 2/4: 添加文件 | Adding files..."
git add .
echo "✓ 文件已暂存 | Files staged"

# 3. 提交
echo ""
echo "💾 步骤 3/4: 提交更改 | Committing changes..."
COMMIT_MSG="${1:-feat: Update bilingual content}"
git commit -m "$COMMIT_MSG" || echo "没有新的更改需要提交 | No changes to commit"
echo "✓ 提交完成 | Commit completed"

# 4. 推送到 GitHub
echo ""
echo "🌐 步骤 4/4: 推送到 GitHub | Pushing to GitHub..."
git push
echo "✓ 推送成功！| Push successful!"

echo ""
echo "========================================"
echo "✅ 部署完成！| Deployment complete!"
echo "========================================"
echo ""
echo "📍 网站将在 1-2 分钟后更新 | Site will be updated in 1-2 minutes"
echo "🌐 访问 | Visit: https://huangf06.github.io/FeiThink/"
echo ""
