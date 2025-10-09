#!/usr/bin/env python3
"""
重新转换缺失的3篇文章
Re-convert the 3 missing articles
"""

import re
from pathlib import Path
from html import unescape

SUBSTACK_DIR = Path("/mnt/e/FeiThink/substack/posts")
OUTPUT_DIR = Path("/mnt/e/FeiThink/content/posts")

def clean_html_to_markdown(html_content):
    """简单的 HTML 到 Markdown 转换"""
    if not html_content:
        return ""

    text = unescape(html_content)
    text = re.sub(r'<h1[^>]*>(.*?)</h1>', r'# \1', text, flags=re.DOTALL)
    text = re.sub(r'<h2[^>]*>(.*?)</h2>', r'## \1', text, flags=re.DOTALL)
    text = re.sub(r'<h3[^>]*>(.*?)</h3>', r'### \1', text, flags=re.DOTALL)
    text = re.sub(r'<h4[^>]*>(.*?)</h4>', r'#### \1', text, flags=re.DOTALL)
    text = re.sub(r'<p[^>]*>(.*?)</p>', r'\1\n\n', text, flags=re.DOTALL)
    text = re.sub(r'<strong[^>]*>(.*?)</strong>', r'**\1**', text, flags=re.DOTALL)
    text = re.sub(r'<em[^>]*>(.*?)</em>', r'*\1*', text, flags=re.DOTALL)
    text = re.sub(r'<b[^>]*>(.*?)</b>', r'**\1**', text, flags=re.DOTALL)
    text = re.sub(r'<i[^>]*>(.*?)</i>', r'*\1*', text, flags=re.DOTALL)
    text = re.sub(r'<a[^>]*href=["\']([^"\']*)["\'][^>]*>(.*?)</a>', r'[\2](\1)', text, flags=re.DOTALL)
    text = re.sub(r'<ul[^>]*>', '\n', text)
    text = re.sub(r'</ul>', '\n', text)
    text = re.sub(r'<ol[^>]*>', '\n', text)
    text = re.sub(r'</ol>', '\n', text)
    text = re.sub(r'<li[^>]*>(.*?)</li>', r'- \1\n', text, flags=re.DOTALL)
    text = re.sub(r'<br\s*/?>', '\n', text)
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'\n{3,}', '\n\n', text)

    return text.strip()

def split_bilingual_content(content):
    """分离双语内容"""
    lines = content.split('\n')
    english_lines = []
    chinese_lines = []
    in_chinese_section = False

    for line in lines:
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', line))
        total_chars = len(line.strip())

        if total_chars > 0 and chinese_chars > total_chars * 0.3:
            in_chinese_section = True

        if in_chinese_section:
            chinese_lines.append(line)
        else:
            english_lines.append(line)

    return '\n'.join(english_lines).strip(), '\n'.join(chinese_lines).strip()

# 定义要转换的3篇文章
posts_to_convert = [
    {
        'file': '173845261.dunbledores-woolen-socks.html',
        'title_en': "Dumbledore's Woolen Socks",
        'title_zh': '邓布利多的羊毛袜',
        'date': '2025-09-10',
        'filename': 'dumbledores-woolen-socks'
    },
    {
        'file': '137279663.on-writing-well.html',
        'title_en': 'Reading On Writing Well',
        'title_zh': '读On Writing Well 有感',
        'date': '2021-03-10',
        'filename': 'reading-on-writing-well'
    },
    {
        'file': '137279657.12-angry-men.html',
        'title_en': "Twelve Angry Men and Robert's Rules of Order",
        'title_zh': '《十二怒汉》和罗伯特议事规则',
        'date': '2020-10-05',
        'filename': 'twelve-angry-men-and-roberts-rules-of-order'
    }
]

for post in posts_to_convert:
    html_file = SUBSTACK_DIR / post['file']

    if not html_file.exists():
        print(f"❌ 文件不存在: {post['file']}")
        continue

    # 读取 HTML
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # 转换为 Markdown
    markdown = clean_html_to_markdown(html_content)

    # 分离中英文
    english_part, chinese_part = split_bilingual_content(markdown)

    # 创建英文文件
    en_file = OUTPUT_DIR / f"{post['filename']}.en.md"
    en_content = f"""---
title: "{post['title_en']}"
date: {post['date']}
lastmod: {post['date']}
draft: false
categories: ["Essays"]
tags: ["reading", "literature", "philosophy"]
summary: ""
author: "Huang Fei"
showToc: true
TocOpen: false
---

{english_part}
"""

    with open(en_file, 'w', encoding='utf-8') as f:
        f.write(en_content)

    # 创建中文文件
    zh_file = OUTPUT_DIR / f"{post['filename']}.zh.md"
    zh_content = f"""---
title: "{post['title_zh']}"
date: {post['date']}
lastmod: {post['date']}
draft: false
categories: ["随笔"]
tags: ["阅读", "文学", "哲学"]
summary: ""
author: "Huang Fei"
showToc: true
TocOpen: false
---

{chinese_part}
"""

    with open(zh_file, 'w', encoding='utf-8') as f:
        f.write(zh_content)

    print(f"✅ 转换: {post['title_en']}")

print("\n========================================")
print("转换完成！3 篇文章已添加")
print("Conversion complete! 3 articles added")
print("========================================")
