#!/usr/bin/env python3
"""
将 Substack HTML 文章转换为 Hugo 双语 Markdown 格式
Convert Substack HTML posts to Hugo bilingual Markdown format
"""

import os
import csv
import re
from pathlib import Path
from html import unescape
from datetime import datetime

# 配置路径
SUBSTACK_DIR = Path("/mnt/e/FeiThink/substack/posts")
POSTS_CSV = Path("/mnt/e/FeiThink/substack/posts.csv")
OUTPUT_DIR = Path("/mnt/e/FeiThink/content/posts")

def clean_html_to_markdown(html_content):
    """简单的 HTML 到 Markdown 转换"""
    if not html_content:
        return ""

    # 解码 HTML 实体
    text = unescape(html_content)

    # 转换标题
    text = re.sub(r'<h1[^>]*>(.*?)</h1>', r'# \1', text, flags=re.DOTALL)
    text = re.sub(r'<h2[^>]*>(.*?)</h2>', r'## \1', text, flags=re.DOTALL)
    text = re.sub(r'<h3[^>]*>(.*?)</h3>', r'### \1', text, flags=re.DOTALL)
    text = re.sub(r'<h4[^>]*>(.*?)</h4>', r'#### \1', text, flags=re.DOTALL)
    text = re.sub(r'<h5[^>]*>(.*?)</h5>', r'##### \1', text, flags=re.DOTALL)

    # 转换段落
    text = re.sub(r'<p[^>]*>(.*?)</p>', r'\1\n\n', text, flags=re.DOTALL)

    # 转换粗体和斜体
    text = re.sub(r'<strong[^>]*>(.*?)</strong>', r'**\1**', text, flags=re.DOTALL)
    text = re.sub(r'<em[^>]*>(.*?)</em>', r'*\1*', text, flags=re.DOTALL)
    text = re.sub(r'<b[^>]*>(.*?)</b>', r'**\1**', text, flags=re.DOTALL)
    text = re.sub(r'<i[^>]*>(.*?)</i>', r'*\1*', text, flags=re.DOTALL)

    # 转换链接
    text = re.sub(r'<a[^>]*href=["\']([^"\']*)["\'][^>]*>(.*?)</a>', r'[\2](\1)', text, flags=re.DOTALL)

    # 转换列表
    text = re.sub(r'<ul[^>]*>', '\n', text)
    text = re.sub(r'</ul>', '\n', text)
    text = re.sub(r'<ol[^>]*>', '\n', text)
    text = re.sub(r'</ol>', '\n', text)
    text = re.sub(r'<li[^>]*>(.*?)</li>', r'- \1\n', text, flags=re.DOTALL)

    # 转换换行
    text = re.sub(r'<br\s*/?>', '\n', text)

    # 删除所有剩余的 HTML 标签
    text = re.sub(r'<[^>]+>', '', text)

    # 清理多余的空行
    text = re.sub(r'\n{3,}', '\n\n', text)

    return text.strip()

def is_chinese_title(title):
    """判断标题是否主要是中文"""
    if not title:
        return False
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', title))
    return chinese_chars > len(title) * 0.3

def sanitize_filename(title):
    """将标题转换为安全的文件名"""
    # 移除或替换非法字符
    filename = re.sub(r'[<>:"/\\|?*]', '', title)
    filename = filename.replace(' ', '-').lower()
    # 限制长度
    filename = filename[:100]
    return filename

def create_front_matter(title, date_str, categories, tags, is_draft=False):
    """创建 Hugo front matter"""
    # 解析日期
    try:
        date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        date = date_obj.strftime('%Y-%m-%d')
    except:
        date = datetime.now().strftime('%Y-%m-%d')

    front_matter = f"""---
title: "{title}"
date: {date}
lastmod: {date}
draft: {str(is_draft).lower()}
categories: {categories}
tags: {tags}
summary: ""
author: "Huang Fei"
showToc: true
TocOpen: false
---

"""
    return front_matter

def process_posts():
    """处理所有文章"""

    # 确保输出目录存在
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # 读取 CSV
    with open(POSTS_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        posts = list(reader)

    print(f"找到 {len(posts)} 篇文章")
    print(f"Found {len(posts)} posts\n")

    converted_count = 0
    skipped_count = 0

    for post in posts:
        post_id = post['post_id'].split('.')[0]
        title_en = post['title'].strip()
        title_zh = post['subtitle'].strip() if post['subtitle'] else ""
        post_date = post['post_date']

        # 查找对应的 HTML 文件
        html_files = list(SUBSTACK_DIR.glob(f"{post_id}.*.html"))
        if not html_files:
            print(f"⚠️  未找到 HTML 文件: {post_id}")
            skipped_count += 1
            continue

        html_file = html_files[0]

        # 读取 HTML 内容
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()

        # 转换为 Markdown
        markdown_content = clean_html_to_markdown(html_content)

        # 生成文件名
        if title_en and title_zh:
            # 双语文章
            filename_base = sanitize_filename(title_en)
        elif title_en:
            # 仅英文
            filename_base = sanitize_filename(title_en)
        elif title_zh:
            # 仅中文
            filename_base = sanitize_filename(title_zh)
        else:
            filename_base = post_id

        # 判断文章语言
        content_is_chinese = is_chinese_title(markdown_content[:200])

        # 创建文件
        if title_en and title_zh:
            # 双语：创建两个文件
            # 英文文件
            en_file = OUTPUT_DIR / f"{filename_base}.en.md"
            en_front_matter = create_front_matter(
                title_en, post_date,
                '["Essays"]',
                '[]'
            )
            with open(en_file, 'w', encoding='utf-8') as f:
                f.write(en_front_matter + markdown_content)

            # 中文文件
            zh_file = OUTPUT_DIR / f"{filename_base}.zh.md"
            zh_front_matter = create_front_matter(
                title_zh, post_date,
                '["随笔"]',
                '[]'
            )
            with open(zh_file, 'w', encoding='utf-8') as f:
                f.write(zh_front_matter + markdown_content)

            print(f"✅ 双语: {title_en} | {title_zh}")
            converted_count += 2

        elif content_is_chinese or is_chinese_title(title_en):
            # 纯中文
            zh_file = OUTPUT_DIR / f"{filename_base}.zh.md"
            zh_front_matter = create_front_matter(
                title_zh if title_zh else title_en, post_date,
                '["随笔"]',
                '[]'
            )
            with open(zh_file, 'w', encoding='utf-8') as f:
                f.write(zh_front_matter + markdown_content)

            print(f"✅ 中文: {title_zh if title_zh else title_en}")
            converted_count += 1

        else:
            # 纯英文
            en_file = OUTPUT_DIR / f"{filename_base}.en.md"
            en_front_matter = create_front_matter(
                title_en, post_date,
                '["Essays"]',
                '[]'
            )
            with open(en_file, 'w', encoding='utf-8') as f:
                f.write(en_front_matter + markdown_content)

            print(f"✅ 英文: {title_en}")
            converted_count += 1

    print(f"\n========================================")
    print(f"转换完成！Conversion complete!")
    print(f"成功转换: {converted_count} 个文件")
    print(f"Successfully converted: {converted_count} files")
    print(f"跳过: {skipped_count} 篇")
    print(f"Skipped: {skipped_count} posts")
    print(f"========================================")

if __name__ == "__main__":
    process_posts()
