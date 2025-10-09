#!/usr/bin/env python3
import re
from pathlib import Path
from html import unescape

SUBSTACK_DIR = Path("/mnt/e/FeiThink/substack/posts")
OUTPUT_DIR = Path("/mnt/e/FeiThink/content/posts")

def clean_html_to_markdown(html_content):
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
    text = re.sub(r'<br\s*/?>', '\n', text)
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def split_bilingual_content(content):
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

posts = [
    {'file': '139089803.do-not-lie.html', 'title_en': 'Do Not Lie', 'title_zh': '不要说谎', 'date': '2023-11-23', 'filename': 'do-not-lie'},
    {'file': '137279583.prologue.html', 'title_en': 'Prologue', 'title_zh': '序章', 'date': '2017-08-26', 'filename': 'prologue'}
]

for post in posts:
    html_file = SUBSTACK_DIR / post['file']
    if not html_file.exists():
        print(f"❌ Not found: {post['file']}")
        continue
    with open(html_file, 'r', encoding='utf-8') as f:
        html = f.read()
    markdown = clean_html_to_markdown(html)
    english, chinese = split_bilingual_content(markdown)

    en_file = OUTPUT_DIR / f"{post['filename']}.en.md"
    with open(en_file, 'w', encoding='utf-8') as f:
        f.write(f'''---
title: "{post['title_en']}"
date: {post['date']}
lastmod: {post['date']}
draft: false
categories: ["Essays"]
tags: ["philosophy", "personal-growth"]
summary: ""
author: "Huang Fei"
showToc: true
TocOpen: false
---

{english}
''')

    zh_file = OUTPUT_DIR / f"{post['filename']}.zh.md"
    with open(zh_file, 'w', encoding='utf-8') as f:
        f.write(f'''---
title: "{post['title_zh']}"
date: {post['date']}
lastmod: {post['date']}
draft: false
categories: ["随笔"]
tags: ["哲学", "个人成长"]
summary: ""
author: "Huang Fei"
showToc: true
TocOpen: false
---

{chinese}
''')
    print(f"✅ {post['title_en']} | {post['title_zh']}")

print("\nDone!")
