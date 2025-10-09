#!/usr/bin/env python3
"""
只保留 selection.csv 中列出的文章
Only keep posts listed in selection.csv
"""

import os
import csv
import re
from pathlib import Path

POSTS_DIR = Path("/mnt/e/FeiThink/content/posts")
SELECTION_CSV = Path("/mnt/e/FeiThink/substack/selection.csv")

def sanitize_title_to_filename(title):
    """将标题转换为可能的文件名"""
    # 移除特殊字符，转小写，替换空格
    filename = title.lower()
    filename = re.sub(r'[:\[\]()]', '', filename)
    filename = re.sub(r'[?!.,;]', '', filename)
    filename = re.sub(r'\s+', '-', filename)
    filename = re.sub(r'[-]+', '-', filename)
    filename = filename.strip('-')
    return filename

def main():
    # 读取选择列表
    selected_titles = []
    with open(SELECTION_CSV, 'r', encoding='utf-8', errors='ignore') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('title'):
                selected_titles.append(row['title'].strip())

    print(f"选择列表中有 {len(selected_titles)} 篇文章")
    print(f"Selection list has {len(selected_titles)} posts\n")

    # 获取所有现有文章
    all_en_files = list(POSTS_DIR.glob("*.en.md"))

    # 将选择的标题转换为可能的文件名模式
    selected_patterns = []
    for title in selected_titles:
        pattern = sanitize_title_to_filename(title)
        selected_patterns.append(pattern)

    print("选择的文章:")
    for title in selected_titles:
        print(f"  - {title}")
    print()

    # 检查每个文件是否在选择列表中
    to_keep = []
    to_remove = []

    for en_file in all_en_files:
        # 读取文件获取标题
        with open(en_file, 'r', encoding='utf-8') as f:
            content = f.read()

        title_match = re.search(r'^title:\s*["\']?(.+?)["\']?$', content, re.MULTILINE)
        if not title_match:
            to_remove.append(en_file)
            continue

        title = title_match.group(1)
        filename_base = en_file.stem.replace('.en', '')

        # 检查是否匹配选择列表
        matched = False
        for selected_title, pattern in zip(selected_titles, selected_patterns):
            # 检查标题是否匹配
            if title.strip() == selected_title.strip():
                matched = True
                break
            # 检查文件名是否包含模式
            if pattern in filename_base:
                matched = True
                break

        if matched:
            to_keep.append(en_file)
        else:
            to_remove.append(en_file)

    print(f"✅ 保留: {len(to_keep)} 篇")
    print(f"❌ 删除: {len(to_remove)} 篇\n")

    # 删除不在列表中的文章
    for en_file in to_remove:
        zh_file = POSTS_DIR / en_file.name.replace('.en.md', '.zh.md')

        if en_file.exists():
            en_file.unlink()
            print(f"  删除: {en_file.name}")
        if zh_file.exists():
            zh_file.unlink()
            print(f"  删除: {zh_file.name}")

    print(f"\n========================================")
    print(f"处理完成！Processing complete!")
    print(f"保留文章: {len(to_keep)} 篇")
    print(f"Kept posts: {len(to_keep)} posts")
    print(f"删除文章: {len(to_remove)} 篇")
    print(f"Removed posts: {len(to_remove)} posts")
    print(f"========================================")

if __name__ == "__main__":
    main()
