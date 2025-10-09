#!/usr/bin/env python3
"""
为文章自动添加标签
Auto-add tags to posts based on title and content
"""

import os
import re
from pathlib import Path

POSTS_DIR = Path("/mnt/e/FeiThink/content/posts")

# 定义关键词到标签的映射
TAG_KEYWORDS = {
    # 哲学相关
    "philosophy": ["kant", "康德", "moral", "道德", "ethics", "伦理", "existential", "存在",
                   "nietzsche", "尼采", "plato", "柏拉图", "思想史", "history of thought"],
    "literature": ["dostoevsky", "陀思妥耶夫斯基", "karamazov", "卡拉马佐夫", "idiot", "白痴",
                   "solitude", "孤独", "vagabond", "浪客"],
    "psychology": ["emotion", "情绪", "psychotherapy", "心理", "intj", "幸福", "happiness"],
    "politics": ["political", "政治", "democracy", "民主", "human nature", "人性", "protest"],
    "personal-growth": ["growth", "成长", "development", "self", "自我", "integrity", "正直",
                       "subjectivity", "主体性", "protagonist", "主角"],
    "reading": ["read", "读", "book", "书", "review", "书评", "notes", "笔记"],
    "writing": ["writing", "写作", "write", "写"],
    "education": ["education", "教育", "liberal", "博雅", "student", "学生"],
    "life": ["life", "生活", "daily", "日常", "memory", "回忆"],
    "society": ["society", "社会", "culture", "文化", "immigration", "移民"],
    "film": ["电影", "film", "movie", "观后感", "12.12", "首尔"],
    "covid": ["covid", "新冠", "疫情", "pandemic"],
    "feminism": ["feminism", "女性主义", "gender", "性别", "厌女"],
    "economics": ["economics", "经济", "股票", "stock", "trade"],
    "german": ["german", "德语", "deutschland"],
}

def extract_tags_from_title(title):
    """从标题提取标签"""
    tags = set()
    title_lower = title.lower()

    for tag, keywords in TAG_KEYWORDS.items():
        for keyword in keywords:
            if keyword.lower() in title_lower:
                tags.add(tag)
                break

    return list(tags)

def extract_tags_from_content(content, limit=200):
    """从内容前200字符提取标签"""
    tags = set()
    content_lower = content[:limit].lower()

    for tag, keywords in TAG_KEYWORDS.items():
        for keyword in keywords:
            if keyword.lower() in content_lower:
                tags.add(tag)
                break

    return list(tags)

def update_post_tags(file_path):
    """更新文章标签"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 提取front matter
    match = re.match(r'^---\n(.*?)\n---\n(.*)$', content, re.DOTALL)
    if not match:
        return False

    front_matter = match.group(1)
    body = match.group(2)

    # 提取标题
    title_match = re.search(r'^title:\s*["\']?(.+?)["\']?$', front_matter, re.MULTILINE)
    if not title_match:
        return False

    title = title_match.group(1)

    # 从标题和内容提取标签
    tags_from_title = extract_tags_from_title(title)
    tags_from_content = extract_tags_from_content(body, 300)

    # 合并标签
    all_tags = list(set(tags_from_title + tags_from_content))

    # 如果没有标签，根据分类添加通用标签
    if not all_tags:
        if '.zh.md' in str(file_path):
            all_tags = ['随笔']
        else:
            all_tags = ['essay']

    # 限制标签数量
    all_tags = all_tags[:5]

    # 更新front matter中的tags
    if '.zh.md' in str(file_path):
        tags_str = f'tags: {all_tags}'
    else:
        tags_str = f'tags: {all_tags}'

    new_front_matter = re.sub(
        r'^tags:\s*\[.*?\]$',
        tags_str,
        front_matter,
        flags=re.MULTILINE
    )

    # 写回文件
    new_content = f"---\n{new_front_matter}\n---\n{body}"

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    return True, title, all_tags

def main():
    md_files = list(POSTS_DIR.glob("*.md"))

    print(f"找到 {len(md_files)} 个文件")
    print(f"Found {len(md_files)} files\n")

    updated_count = 0

    for md_file in md_files:
        result = update_post_tags(md_file)
        if result and result[0]:
            _, title, tags = result
            print(f"✅ {md_file.name[:50]}: {tags}")
            updated_count += 1

    print(f"\n========================================")
    print(f"更新完成！Updated complete!")
    print(f"成功更新: {updated_count} 个文件")
    print(f"Successfully updated: {updated_count} files")
    print(f"========================================")

if __name__ == "__main__":
    main()
