#!/usr/bin/env python3
"""
Article Formatter - Standardize all articles according to project standards
"""

import os
import re
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple
import yaml

# Project root
ROOT_DIR = Path("/mnt/e/FeiThink")
POSTS_DIR = ROOT_DIR / "content/posts"

# Standard categories
VALID_CATEGORIES = ["Essays", "Philosophy", "Literature"]

def extract_summary_from_content(content: str, max_length: int = 100) -> str:
    """Extract first 50-100 words from content as summary"""
    # Remove markdown formatting
    text = re.sub(r'[#*`\[\]()]', '', content)
    # Remove multiple spaces/newlines
    text = re.sub(r'\s+', ' ', text).strip()
    # Get first 150 characters as approximation
    words = text.split()
    summary = []
    char_count = 0
    for word in words:
        if char_count + len(word) > max_length:
            break
        summary.append(word)
        char_count += len(word) + 1
    return ' '.join(summary) + "..." if len(summary) < len(words) else ' '.join(summary)

def standardize_tags(tags: List[str]) -> List[str]:
    """Convert tags to kebab-case and ensure at least 3 tags"""
    standardized = []
    for tag in tags:
        # Remove quotes and convert to kebab-case
        tag = tag.strip().strip('"\'')
        # Convert to lowercase and replace spaces/underscores with hyphens
        tag = re.sub(r'[\s_]+', '-', tag.lower())
        # Remove any non-alphanumeric except hyphens
        tag = re.sub(r'[^a-z0-9\-]', '', tag)
        if tag:
            standardized.append(tag)

    # Ensure at least 3 tags
    if len(standardized) < 3:
        standardized = standardized[:3] if standardized else ["article", "essay", "writing"]

    return standardized[:5]  # Max 5 tags

def parse_article(filepath: Path) -> Tuple[Dict, str]:
    """Parse article file and return (front_matter, content)"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split front matter and content
    match = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
    if not match:
        raise ValueError(f"Invalid article format: {filepath}")

    fm_str, article_content = match.groups()

    try:
        front_matter = yaml.safe_load(fm_str)
    except yaml.YAMLError as e:
        print(f"YAML Parse Error in {filepath}: {e}")
        return {}, article_content

    return front_matter or {}, article_content

def standardize_front_matter(fm: Dict, filepath: Path, content: str) -> Dict:
    """Standardize and complete front matter"""

    # Get language from filename
    is_chinese = '.zh.md' in str(filepath)
    language = 'zh' if is_chinese else 'en'

    # Ensure all required fields
    standardized = {
        'title': fm.get('title', 'Untitled'),
        'date': fm.get('date', datetime.now().strftime('%Y-%m-%d')),
        'lastmod': fm.get('lastmod', fm.get('date', datetime.now().strftime('%Y-%m-%d'))),
        'draft': fm.get('draft', False),
        'categories': fm.get('categories', ['Essays']),
        'tags': standardize_tags(fm.get('tags', [])),
        'summary': fm.get('summary', '').strip() or extract_summary_from_content(content),
        'weight': fm.get('weight', 999),
        'author': fm.get('author', 'FeiThink'),
        'showToc': fm.get('showToc', True),
        'TocOpen': fm.get('TocOpen', False),
    }

    # Validate categories
    if not isinstance(standardized['categories'], list):
        standardized['categories'] = [standardized['categories']]
    standardized['categories'] = [c for c in standardized['categories'] if c in VALID_CATEGORIES] or ['Essays']

    return standardized

def write_article(filepath: Path, front_matter: Dict, content: str) -> None:
    """Write standardized article back to file with proper YAML format"""
    # Build YAML manually to match our standard format
    fm_lines = []

    # Define field order (fields must be in this order)
    field_order = ['title', 'date', 'lastmod', 'draft', 'categories', 'tags', 'summary', 'weight', 'author', 'showToc', 'TocOpen']
    field_formatters = {
        'title': lambda v: f'"{v}"',
        'date': lambda v: str(v),
        'lastmod': lambda v: str(v),
        'draft': lambda v: str(v).lower(),
        'categories': lambda v: '[' + ', '.join(f'"{c}"' for c in v) + ']',
        'tags': lambda v: '[' + ', '.join(v) + ']',
        'summary': lambda v: f'"{v.replace(chr(34), chr(92) + chr(34))}"',
        'weight': lambda v: str(v),
        'author': lambda v: f'"{v}"',
        'showToc': lambda v: str(v).lower(),
        'TocOpen': lambda v: str(v).lower(),
    }

    # Build YAML lines in defined order
    for field in field_order:
        if field in front_matter:
            value = front_matter[field]
            formatted = field_formatters[field](value)
            fm_lines.append(f"{field}: {formatted}")

    fm_yaml = '\n'.join(fm_lines)

    # Build file content
    output = f"---\n{fm_yaml}\n---\n{content}"

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(output)

def process_articles(dry_run: bool = True) -> None:
    """Process all articles"""
    articles = sorted(POSTS_DIR.glob('*.md'))
    articles = [a for a in articles if 'posts_backup' not in str(a)]

    stats = {
        'total': 0,
        'updated': 0,
        'errors': 0,
        'issues': []
    }

    for filepath in articles:
        stats['total'] += 1
        try:
            fm, content = parse_article(filepath)
            original_fm = dict(fm)

            # Standardize
            fm = standardize_front_matter(fm, filepath, content)

            # Check if changed
            if fm != original_fm:
                stats['updated'] += 1
                stats['issues'].append(str(filepath.name))

                if not dry_run:
                    write_article(filepath, fm, content)
                    print(f"✓ Updated: {filepath.name}")
                else:
                    print(f"→ Would update: {filepath.name}")

        except Exception as e:
            stats['errors'] += 1
            print(f"✗ Error in {filepath.name}: {e}")

    print(f"\n{'='*60}")
    print(f"Total articles: {stats['total']}")
    print(f"Would update: {stats['updated']}")
    print(f"Errors: {stats['errors']}")
    print(f"Mode: {'DRY RUN' if dry_run else 'WRITE'}")

    return stats

if __name__ == '__main__':
    dry_run = '--apply' not in sys.argv
    if dry_run:
        print("Running in DRY RUN mode. Use '--apply' to actually modify files.\n")
    else:
        print("Running in WRITE mode. Files will be modified!\n")

    stats = process_articles(dry_run=dry_run)
