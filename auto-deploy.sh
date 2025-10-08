#!/bin/bash

# 自动部署脚本
# Auto-deploy script for Hugo portfolio

set -e

echo "🚀 开始自动部署 Hugo 作品集..."
echo ""

# 进入项目目录
cd /mnt/e/GitStack
echo "✓ 工作目录: $(pwd)"

# 1. 添加 PaperMod 主题
echo ""
echo "📦 步骤 1/5: 添加 PaperMod 主题..."
if [ -d "themes/PaperMod/.git" ]; then
    echo "✓ 主题已存在"
else
    git submodule add --depth=1 https://github.com/adityatelange/hugo-PaperMod.git themes/PaperMod
    echo "✓ 主题添加成功"
fi

# 2. 初始化子模块
echo ""
echo "🔄 步骤 2/5: 初始化子模块..."
git submodule update --init --recursive
echo "✓ 子模块初始化完成"

# 3. 添加所有文件
echo ""
echo "📝 步骤 3/5: 添加文件..."
git add .
echo "✓ 文件已暂存"

# 4. 提交
echo ""
echo "💾 步骤 4/5: 提交更改..."
git commit -m "feat: Initial Hugo portfolio setup with PaperMod theme

- Add Hugo configuration
- Add PaperMod theme
- Add sample articles (Philosophy, Literature, Essays)
- Add documentation
- Configure GitHub Actions for deployment" || echo "没有新的更改需要提交"
echo "✓ 提交完成"

# 5. 推送到 GitHub
echo ""
echo "🌐 步骤 5/5: 推送到 GitHub..."
git push -u origin main
echo "✓ 推送成功！"

echo ""
echo "========================================"
echo "✅ 部署完成！"
echo "========================================"
echo ""
echo "📍 下一步操作："
echo "1. 访问你的 GitHub 仓库"
echo "2. 进入 Settings → Pages"
echo "3. 在 Source 下选择 'GitHub Actions'"
echo "4. 等待 1-2 分钟让 Actions 完成构建"
echo "5. 访问你的网站："
echo "   https://你的用户名.github.io/blog-portfolio/"
echo ""
echo "🎉 恭喜！你的作品集即将上线！"
