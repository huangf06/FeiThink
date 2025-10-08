@echo off
chcp 65001 >nul
echo ========================================
echo 🚀 Hugo 作品集自动部署
echo ========================================
echo.

cd /d E:\GitStack
echo ✓ 当前目录: %CD%
echo.

echo 📦 步骤 1/5: 添加 PaperMod 主题...
git submodule add --depth=1 https://github.com/adityatelange/hugo-PaperMod.git themes/PaperMod
if errorlevel 1 (
    echo   主题可能已存在，继续...
)
git submodule update --init --recursive
echo ✓ 主题配置完成
echo.

echo 📝 步骤 2/5: 添加所有文件...
git add .
echo ✓ 文件已暂存
echo.

echo 💾 步骤 3/5: 提交更改...
git commit -m "feat: Initial Hugo portfolio setup with PaperMod theme"
if errorlevel 1 (
    echo   没有新更改，跳过提交
)
echo ✓ 提交完成
echo.

echo 🌐 步骤 4/5: 推送到 GitHub...
git push -u origin main
echo ✓ 推送成功！
echo.

echo ========================================
echo ✅ 部署完成！
echo ========================================
echo.
echo 📍 下一步操作：
echo 1. 访问你的 GitHub 仓库
echo 2. 进入 Settings → Pages
echo 3. 在 Source 下选择 'GitHub Actions'
echo 4. 等待 1-2 分钟让 Actions 完成构建
echo 5. 访问你的网站
echo.
echo 🎉 恭喜！你的作品集即将上线！
echo.
pause
