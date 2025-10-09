#!/usr/bin/env python3
"""
1. 只保留主标题是英文的双语文章
2. 分离中英文内容：英文版只保留英文部分，中文版只保留中文部分
"""

import os
import re
from pathlib import Path

POSTS_DIR = Path("/mnt/e/FeiThink/content/posts")

def is_english_title(title):
    """判断标题是否主要是英文"""
    if not title:
        return False
    # 统计英文字母比例
    english_chars = len(re.findall(r'[a-zA-Z]', title))
    return english_chars > len(title) * 0.3

def split_bilingual_content(content):
    """
    分离双语内容
    假设格式：英文在前，中文在后，可能用分隔符分开
    """
    # 尝试找到中英文分界点
    # 常见模式：连续的中文段落出现
    lines = content.split('\n')

    english_lines = []
    chinese_lines = []
    in_chinese_section = False

    for line in lines:
        # 判断这一行是否主要是中文
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', line))
        total_chars = len(line.strip())

        if total_chars > 0 and chinese_chars > total_chars * 0.3:
            in_chinese_section = True

        if in_chinese_section:
            chinese_lines.append(line)
        else:
            english_lines.append(line)

    return '\n'.join(english_lines).strip(), '\n'.join(chinese_lines).strip()

def process_posts():
    """处理文章"""

    # 获取所有 .en.md 文件
    en_files = list(POSTS_DIR.glob("*.en.md"))

    bilingual_files = []
    single_lang_files = []

    print(f"检查 {len(en_files)} 个英文文件...")
    print(f"Checking {len(en_files)} English files...\n")

    for en_file in en_files:
        # 读取文件提取标题
        with open(en_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # 提取标题
        title_match = re.search(r'^title:\s*["\']?(.+?)["\']?$', content, re.MULTILINE)
        if not title_match:
            continue

        title = title_match.group(1)

        # 判断是否是英文标题
        if is_english_title(title):
            bilingual_files.append(en_file)
        else:
            single_lang_files.append(en_file)

    print(f"✅ 双语文章: {len(bilingual_files)} 篇")
    print(f"❌ 单语文章: {len(single_lang_files)} 篇\n")

    # 删除单语文章
    print("删除单语文章...")
    for file in single_lang_files:
        zh_file = POSTS_DIR / file.name.replace('.en.md', '.zh.md')
        if file.exists():
            file.unlink()
            print(f"  删除: {file.name}")
        if zh_file.exists():
            zh_file.unlink()
            print(f"  删除: {zh_file.name}")

    print(f"\n分离双语内容...")
    # 处理双语文章，分离中英文
    for en_file in bilingual_files:
        zh_file = POSTS_DIR / en_file.name.replace('.en.md', '.zh.md')

        # 读取英文文件
        with open(en_file, 'r', encoding='utf-8') as f:
            en_content = f.read()

        # 分离 front matter 和正文
        match = re.match(r'^---\n(.*?)\n---\n(.*)$', en_content, re.DOTALL)
        if not match:
            continue

        front_matter_en = match.group(1)
        body = match.group(2)

        # 分离中英文内容
        english_part, chinese_part = split_bilingual_content(body)

        # 更新英文文件（只保留英文部分）
        new_en_content = f"---\n{front_matter_en}\n---\n\n{english_part}\n"
        with open(en_file, 'w', encoding='utf-8') as f:
            f.write(new_en_content)

        # 更新中文文件
        if zh_file.exists():
            with open(zh_file, 'r', encoding='utf-8') as f:
                zh_content = f.read()

            match_zh = re.match(r'^---\n(.*?)\n---\n(.*)$', zh_content, re.DOTALL)
            if match_zh:
                front_matter_zh = match_zh.group(1)
                new_zh_content = f"---\n{front_matter_zh}\n---\n\n{chinese_part}\n"
                with open(zh_file, 'w', encoding='utf-8') as f:
                    f.write(new_zh_content)

                print(f"  ✅ 分离: {en_file.name[:40]}")

    print(f"\n========================================")
    print(f"处理完成！Processing complete!")
    print(f"保留双语文章: {len(bilingual_files)} 篇")
    print(f"Kept bilingual posts: {len(bilingual_files)} posts")
    print(f"删除单语文章: {len(single_lang_files)} 篇")
    print(f"Removed single-language posts: {len(single_lang_files)} posts")
    print(f"========================================")

if __name__ == "__main__":
    process_posts()
