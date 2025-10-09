# 双语博客使用指南 | Bilingual Blog Guide

## 概述 | Overview

你的 FeiThink 博客现在已配置为中英双语模式。每篇文章都有独立的中英文版本，读者可以通过语言切换器在两种语言间切换。

Your FeiThink blog is now configured for bilingual (Chinese/English) content. Each post has separate Chinese and English versions, and readers can switch between languages using the language switcher.

---

## 文件命名规范 | File Naming Convention

每篇文章需要创建**两个文件**，使用语言后缀区分：

Each article requires **two files** with language suffixes:

```
content/posts/your-article-name.en.md  # 英文版 | English version
content/posts/your-article-name.zh.md  # 中文版 | Chinese version
```

### 示例 | Examples

```
philosophy/plato-republic.en.md
philosophy/plato-republic.zh.md

literature/poem-translation.en.md
literature/poem-translation.zh.md

essays/technology-thoughts.en.md
essays/technology-thoughts.zh.md
```

---

## Front Matter 模板 | Front Matter Template

### 英文版 | English Version

```yaml
---
title: "Your Article Title"
date: 2025-01-15
lastmod: 2025-01-15
draft: false
categories: ["Philosophy"]  # or ["Literature"], ["Essays"]
tags: ["tag1", "tag2", "tag3"]
summary: "Brief English summary of the article"
weight: 100
author: "Huang Fei"
showToc: true
TocOpen: false
---

Your English content here...
```

### 中文版 | Chinese Version

```yaml
---
title: "你的文章标题"
date: 2025-01-15
lastmod: 2025-01-15
draft: false
categories: ["哲学"]  # 或 ["文学"], ["随笔"]
tags: ["标签1", "标签2", "标签3"]
summary: "文章的中文简要说明"
weight: 100
author: "黄飞"
showToc: true
TocOpen: false
---

你的中文内容...
```

---

## URL 结构 | URL Structure

双语网站的 URL 结构：

Bilingual site URL structure:

```
英文 | English:
https://huangf06.github.io/FeiThink/en/
https://huangf06.github.io/FeiThink/en/posts/
https://huangf06.github.io/FeiThink/en/posts/your-article/

中文 | Chinese:
https://huangf06.github.io/FeiThink/zh/
https://huangf06.github.io/FeiThink/zh/posts/
https://huangf06.github.io/FeiThink/zh/posts/your-article/
```

---

## 创建新文章 | Creating New Posts

### 方法 1: 手动创建 | Method 1: Manual Creation

直接创建两个文件：

Create two files directly:

```bash
# 创建英文版
touch content/posts/my-new-post.en.md

# 创建中文版
touch content/posts/my-new-post.zh.md
```

### 方法 2: 使用 Hugo 命令 | Method 2: Using Hugo Commands

如果你安装了 Hugo：

If you have Hugo installed:

```bash
# 创建英文版
hugo new posts/my-new-post.en.md

# 创建中文版
hugo new posts/my-new-post.zh.md
```

---

## 语言特定的分类和标签 | Language-Specific Categories and Tags

### 英文分类 | English Categories
- `Philosophy`
- `Literature`
- `Essays`

### 中文分类 | Chinese Categories
- `哲学`
- `文学`
- `随笔`

**重要**: 使用各自语言的分类名称，以便正确分类和显示。

**Important**: Use category names in the respective language for proper categorization and display.

---

## 部署工作流 | Deployment Workflow

### 使用部署脚本 | Using Deployment Script

```bash
# 使用默认提交信息
./deploy-bilingual.sh

# 使用自定义提交信息
./deploy-bilingual.sh "feat: Add new philosophy article on Plato"
```

### 手动部署 | Manual Deployment

```bash
git add .
git commit -m "feat: Add new bilingual content"
git push
```

部署后 1-2 分钟，GitHub Actions 会自动构建并发布网站。

After deployment, GitHub Actions will automatically build and publish the site in 1-2 minutes.

---

## 最佳实践 | Best Practices

### 1. 内容对应 | Content Correspondence

确保中英文版本内容对应，但**不需要逐字翻译**。根据语言特点调整表达。

Ensure Chinese and English versions correspond, but **don't translate word-for-word**. Adapt expression to each language's characteristics.

### 2. 文件名一致 | Consistent File Names

除了语言后缀外，文件名应完全相同：
- ✅ `article.en.md` 和 `article.zh.md`
- ❌ `article-en.en.md` 和 `article-zh.zh.md`

Aside from language suffix, file names should be identical:
- ✅ `article.en.md` and `article.zh.md`
- ❌ `article-en.en.md` and `article-zh.zh.md`

### 3. 同步发布 | Synchronized Publishing

同时创建和发布中英文版本，保持两个版本的 `date` 和 `lastmod` 字段一致。

Create and publish both versions simultaneously, keeping `date` and `lastmod` fields consistent.

### 4. Draft 管理 | Draft Management

在完成两个版本前，都设置为 `draft: true`，完成后一起发布。

Set both versions to `draft: true` until both are complete, then publish together.

---

## 示例文章结构 | Example Article Structure

```
content/
├── posts/
│   ├── example-post.en.md       ✅ 示例文章
│   └── example-post.zh.md       ✅ 示例文章
├── philosophy/
│   ├── article1.en.md
│   └── article1.zh.md
├── literature/
│   ├── poem1.en.md
│   └── poem1.zh.md
├── essays/
│   ├── essay1.en.md
│   └── essay1.zh.md
├── about.en.md
├── about.zh.md
├── archives.en.md
├── archives.zh.md
├── search.en.md
└── search.zh.md
```

---

## 语言切换功能 | Language Switching Feature

PaperMod 主题会自动在页面右上角添加语言切换器，允许读者在中英文版本间切换。

The PaperMod theme automatically adds a language switcher in the top-right corner, allowing readers to switch between Chinese and English versions.

---

## 故障排查 | Troubleshooting

### 语言切换器不显示 | Language Switcher Not Showing

确保两个语言版本的文件名（除后缀外）完全相同。

Ensure both language versions have identical file names (except for the suffix).

### 文章不显示 | Posts Not Showing

检查：
1. `draft: false` 已设置
2. 文件扩展名为 `.md`
3. Front matter 格式正确（YAML）
4. 分类名称使用了正确的语言

Check:
1. `draft: false` is set
2. File extension is `.md`
3. Front matter format is correct (YAML)
4. Category names use the correct language

### 部署失败 | Deployment Failed

访问 GitHub Actions 页面查看构建日志：
`https://github.com/huangf06/FeiThink/actions`

Visit GitHub Actions page to check build logs:
`https://github.com/huangf06/FeiThink/actions`

---

## 需要帮助？| Need Help?

如有问题，可以：
1. 查看 Hugo 官方文档：https://gohugo.io/content-management/multilingual/
2. 查看 PaperMod 主题文档：https://github.com/adityatelange/hugo-PaperMod
3. 检查 GitHub Issues：https://github.com/huangf06/FeiThink/issues

For questions:
1. Check Hugo official docs: https://gohugo.io/content-management/multilingual/
2. Check PaperMod theme docs: https://github.com/adityatelange/hugo-PaperMod
3. Check GitHub Issues: https://github.com/huangf06/FeiThink/issues

---

祝写作愉快！| Happy writing!
