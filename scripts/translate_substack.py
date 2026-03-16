#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Substack to Hugo Translation Automation
Translates new Chinese articles from Substack export to English for Hugo blog.
"""
import csv
import json
import re
import sys
from pathlib import Path
from bs4 import BeautifulSoup
import yaml
from datetime import datetime

# Fix Windows console encoding
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')


def parse_substack_export(export_dir: Path) -> list[dict]:
    """Parse Substack export and return list of articles."""
    posts_csv = export_dir / "posts.csv"
    articles = []

    print(f"  Reading {posts_csv}...")
    with open(posts_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if not row['is_published'] or row['is_published'].lower() != 'true':
                continue

            post_id = row['post_id'].split('.')[0]

            # Find HTML file for this post
            html_files = list(export_dir.glob(f"posts/{post_id}.*.html"))

            if html_files:
                html_path = html_files[0]
                with open(html_path, 'r', encoding='utf-8') as hf:
                    soup = BeautifulSoup(hf.read(), 'html.parser')

                    # Extract main content
                    content_div = soup.find('div', class_='body')
                    if content_div:
                        content = content_div.get_text(separator='\n\n', strip=True)
                    else:
                        content = soup.get_text(separator='\n\n', strip=True)

                articles.append({
                    'id': post_id,
                    'title': row['title'],
                    'subtitle': row.get('subtitle', ''),
                    'date': row['post_date'][:10] if row['post_date'] else '2020-01-01',
                    'content': content,
                    'html_path': str(html_path)
                })

    return articles


def get_existing_hugo_articles(content_dir: Path) -> set[str]:
    """Get set of article IDs already in Hugo."""
    existing = set()
    for zh_file in content_dir.glob("content/posts/*.zh.md"):
        # Extract ID from filename like "137279583-prologue.zh.md"
        article_id = zh_file.stem.split('-')[0].split('.')[0]
        existing.add(article_id)
    return existing


def identify_new_articles(substack_articles: list[dict], hugo_dir: Path) -> list[dict]:
    """Return articles that don't exist in Hugo yet."""
    existing_ids = get_existing_hugo_articles(hugo_dir)
    new_articles = [a for a in substack_articles if a['id'] not in existing_ids]
    return new_articles


def classify_complexity(article: dict) -> str:
    """Classify article as Simple, Medium, or Complex."""
    content = article['content']
    word_count = len(content)

    # Keywords indicating philosophical/cultural depth
    complex_keywords = ['康德', '陀思妥耶夫斯基', '道德', '哲学', '存在', '本质', '形而上', '伦理', '理性']
    medium_keywords = ['思考', '反思', '理解', '意义', '价值', '社会', '文化']

    complex_score = sum(1 for kw in complex_keywords if kw in content)
    medium_score = sum(1 for kw in medium_keywords if kw in content)

    if word_count > 3000 or complex_score >= 3:
        return "Complex"
    elif word_count > 1500 or medium_score >= 2 or complex_score >= 1:
        return "Medium"
    else:
        return "Simple"


def create_slug(title: str) -> str:
    """Create URL-friendly slug from title."""
    # Remove special characters, keep Chinese, English, numbers
    slug = re.sub(r'[^\w\s-]', '', title.lower())
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug[:60]


def translate_article_with_claude(article: dict) -> dict:
    """
    Apply editorial translation workflow to article.
    This is a placeholder - actual translation happens via Claude interaction.
    """

    # For now, create structured output for manual translation
    diagnosis = {
        'status': 'Chinese only - awaiting translation',
        'core_theme': 'To be analyzed during translation',
        'intended_tone': 'To be determined',
        'complexity': article['complexity'],
        'challenges': 'To be identified during translation process'
    }

    title_options = {
        'recommended': article['title'],  # Will be translated
        'alternatives': []
    }

    # Placeholder translation - will be done manually with Claude
    translated_content = f"""[TRANSLATION PENDING]

Original Title: {article['title']}
Subtitle: {article['subtitle']}
Date: {article['date']}
Complexity: {article['complexity']}
Word Count: {len(article['content'])} characters

---

ORIGINAL CHINESE CONTENT:

{article['content']}

---

TRANSLATION INSTRUCTIONS:
1. Apply full editorial workflow from guidelines
2. Maintain serious, reflective, intellectually ambitious voice
3. Remove Chinglish, ensure natural English prose
4. Preserve philosophical depth and emotional nuance
5. Provide title alternatives with tonal explanations
"""

    editorial_notes = {
        'assessment': 'Awaiting detailed translation and editorial review',
        'improvements': [],
        'key_decisions': [],
        'refinements': []
    }

    return {
        'original': article,
        'diagnosis': diagnosis,
        'title_options': title_options,
        'translated_content': translated_content,
        'editorial_notes': editorial_notes
    }


def generate_hugo_frontmatter(article: dict, translation: dict) -> dict:
    """Generate Hugo-compatible front matter dictionary."""
    frontmatter = {
        'title': translation['title_options']['recommended'],
        'date': article['date'],
        'lastmod': article['date'],
        'draft': True,  # Always draft for review
        'categories': ['Essays'],
        'tags': ['translation-pending', 'review-needed', article['complexity'].lower()],
        'summary': f"Translation pending. Original: {article['title']}",
        'weight': 999,
        'author': 'FeiThink',
        'showToc': True,
        'TocOpen': False
    }
    return frontmatter


def generate_markdown_file(article: dict, translation: dict, output_dir: Path) -> str:
    """Generate Hugo markdown files (EN + ZH)."""
    slug = create_slug(article['title'])
    en_filename = f"{article['id']}-{slug}.en.md"
    zh_filename = f"{article['id']}-{slug}.zh.md"

    # English draft
    en_path = output_dir / "drafts" / en_filename
    frontmatter = generate_hugo_frontmatter(article, translation)
    frontmatter_yaml = yaml.dump(frontmatter, allow_unicode=True, sort_keys=False)

    en_content = f"""---
{frontmatter_yaml}---

{translation['translated_content']}
"""
    en_path.write_text(en_content, encoding='utf-8')

    # Chinese reference
    zh_path = output_dir / "drafts" / zh_filename
    zh_frontmatter = {
        'title': article['title'],
        'date': article['date'],
        'lastmod': article['date'],
        'draft': True,
        'categories': ['Essays'],
        'tags': ['original-chinese'],
        'summary': article['subtitle'] if article['subtitle'] else article['title'],
        'weight': 999,
        'author': 'FeiThink',
        'showToc': True,
        'TocOpen': False
    }
    zh_frontmatter_yaml = yaml.dump(zh_frontmatter, allow_unicode=True, sort_keys=False)

    zh_content = f"""---
{zh_frontmatter_yaml}---

{article['content']}
"""
    zh_path.write_text(zh_content, encoding='utf-8')

    return en_filename


def generate_editorial_report(article: dict, translation: dict, output_dir: Path) -> str:
    """Generate detailed editorial report."""
    slug = create_slug(article['title'])
    report_filename = f"{article['id']}-{slug}-editorial.md"
    report_path = output_dir / "reports" / report_filename

    report = f"""# Editorial Report: {article['title']}

**Article ID:** {article['id']}
**Date:** {article['date']}
**Complexity:** {translation['diagnosis']['complexity']}
**Word Count:** {len(article['content'])} characters

---

## Article Diagnosis

- **Status:** {translation['diagnosis']['status']}
- **Core theme:** {translation['diagnosis']['core_theme']}
- **Intended tone:** {translation['diagnosis']['intended_tone']}
- **Complexity:** {translation['diagnosis']['complexity']}
- **Main challenges:** {translation['diagnosis']['challenges']}

## English Title Options

- **Recommended:** "{translation['title_options']['recommended']}"
- **Alternatives:** {translation['title_options']['alternatives'] if translation['title_options']['alternatives'] else 'To be determined during translation'}

## Translation Quality Assessment

{translation['editorial_notes']['assessment']}

## Key Translation Decisions

{translation['editorial_notes']['key_decisions'] if translation['editorial_notes']['key_decisions'] else 'To be documented during translation'}

## Recommended Review Actions

- [ ] Translate title with 2-4 alternatives
- [ ] Apply full editorial workflow
- [ ] Review for cultural references and philosophical terminology
- [ ] Proofread for natural English prose
- [ ] Verify tone matches original intent
- [ ] Check summary is 50-100 words

---

**Files:**
- English draft: `output/drafts/{article['id']}-{slug}.en.md`
- Chinese reference: `output/drafts/{article['id']}-{slug}.zh.md`
- Comparison: `output/reports/comparison-{article['id']}.md`

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

    report_path.write_text(report, encoding='utf-8')
    return report_filename


def generate_comparison(article: dict, translation: dict, output_dir: Path) -> str:
    """Generate side-by-side comparison document."""
    comp_filename = f"comparison-{article['id']}.md"
    comp_path = output_dir / "reports" / comp_filename

    preview_length = min(2000, len(article['content']))

    comparison = f"""# Translation Comparison: {article['title']}

**Article ID:** {article['id']}
**Complexity:** {article['complexity']}
**Total Length:** {len(article['content'])} characters

---

## Chinese Original (Preview)

{article['content'][:preview_length]}

{'...' if len(article['content']) > preview_length else ''}

---

## English Translation Status

**Status:** Translation pending
**Recommended approach:** {article['complexity']} article - requires careful attention to {'philosophical terminology and cultural references' if article['complexity'] == 'Complex' else 'tone and natural English flow'}

---

## Translation Notes

- Original title: {article['title']}
- Subtitle: {article['subtitle'] if article['subtitle'] else 'None'}
- Date: {article['date']}

**Next steps:**
1. Read full Chinese content carefully
2. Identify key themes and philosophical concepts
3. Draft English title with alternatives
4. Translate with editorial rigor
5. Review and refine

---

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

    comp_path.write_text(comparison, encoding='utf-8')
    return comp_filename


def generate_review_checklist(articles: list[dict], output_dir: Path):
    """Generate prioritized review checklist."""
    checklist_path = output_dir / "review-checklist.md"

    # Sort by complexity (Complex first)
    complexity_order = {'Complex': 0, 'Medium': 1, 'Simple': 2}
    sorted_articles = sorted(articles, key=lambda a: complexity_order[a['complexity']])

    checklist = f"""# Translation Review Checklist

**Total Articles:** {len(articles)}
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## Review Priority Order

Review articles in this order: Complex → Medium → Simple

### Complex Articles (High Priority - Review First)

"""

    for article in sorted_articles:
        if article['complexity'] == 'Complex':
            slug = create_slug(article['title'])
            checklist += f"- [ ] **{article['id']}** - {article['title']} ({len(article['content'])} chars)\n"
            checklist += f"      File: `output/drafts/{article['id']}-{slug}.en.md`\n"

    checklist += "\n### Medium Articles (Medium Priority)\n\n"
    for article in sorted_articles:
        if article['complexity'] == 'Medium':
            slug = create_slug(article['title'])
            checklist += f"- [ ] **{article['id']}** - {article['title']}\n"
            checklist += f"      File: `output/drafts/{article['id']}-{slug}.en.md`\n"

    checklist += "\n### Simple Articles (Lower Priority)\n\n"
    for article in sorted_articles:
        if article['complexity'] == 'Simple':
            slug = create_slug(article['title'])
            checklist += f"- [ ] **{article['id']}** - {article['title']}\n"
            checklist += f"      File: `output/drafts/{article['id']}-{slug}.en.md`\n"

    checklist += f"""

---

## Approval Process

For each reviewed and approved article:

```bash
./scripts/approve-article.sh <article-id>
```

This will:
1. Copy EN/ZH files to `content/posts/`
2. Set `draft: false`
3. Ready for commit and deployment

---

**Progress:** 0/{len(articles)} articles reviewed
"""

    checklist_path.write_text(checklist, encoding='utf-8')
    print(f"  [OK] Generated: {checklist_path.name}")


def generate_translation_summary(articles: list[dict], output_dir: Path):
    """Generate master translation summary."""
    summary_path = output_dir / "translation-summary.md"

    complexity_counts = {}
    for article in articles:
        c = article['complexity']
        complexity_counts[c] = complexity_counts.get(c, 0) + 1

    summary = f"""# Substack Translation Automation Summary

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Total New Articles:** {len(articles)}

---

## Complexity Breakdown

- **Complex:** {complexity_counts.get('Complex', 0)} articles (philosophical depth, cultural references)
- **Medium:** {complexity_counts.get('Medium', 0)} articles (moderate complexity)
- **Simple:** {complexity_counts.get('Simple', 0)} articles (straightforward prose)

---

## Output Structure

```
output/
├── drafts/              # {len(articles) * 2} files (EN + ZH pairs)
│   ├── {articles[0]['id']}-*.en.md
│   ├── {articles[0]['id']}-*.zh.md
│   └── ...
├── reports/             # {len(articles) * 2} files (editorial + comparison)
│   ├── {articles[0]['id']}-*-editorial.md
│   ├── comparison-{articles[0]['id']}.md
│   └── ...
├── review-checklist.md  # Prioritized review list
└── translation-summary.md  # This file
```

---

## Next Steps

1. **Review translations** in priority order (see `review-checklist.md`)
2. **For each article:**
   - Open `output/drafts/{{id}}-{{slug}}.en.md`
   - Read editorial report in `output/reports/{{id}}-{{slug}}-editorial.md`
   - Apply full translation workflow per editorial guidelines
   - Replace `[TRANSLATION PENDING]` section with polished English
3. **Approve completed articles:**
   ```bash
   ./scripts/approve-article.sh <article-id>
   ```
4. **Commit and deploy** approved translations

---

## Articles to Translate

"""

    for article in sorted(articles, key=lambda a: {'Complex': 0, 'Medium': 1, 'Simple': 2}[a['complexity']]):
        slug = create_slug(article['title'])
        summary += f"- **{article['id']}** ({article['complexity']}): {article['title']}\n"
        summary += f"  - {len(article['content'])} chars | {article['date']}\n"

    summary += f"""

---

## Translation Guidelines Reference

Apply these principles to every article:

1. **Accuracy first** - Preserve meaning, argument flow, emotional logic
2. **Strong English prose** - Remove Chinglish, use idiomatic English
3. **Keep author's voice** - Serious, reflective, intellectually ambitious
4. **Good taste** - Avoid melodrama, pompous phrasing, cliché self-help tone
5. **Signal difficult choices** - Provide title alternatives, note translation tradeoffs

**Quality bar:** Top-tier essay translation, serious magazine-level editing

---

**Status:** Ready for manual translation work
**Review checklist:** `output/review-checklist.md`
"""

    summary_path.write_text(summary, encoding='utf-8')
    print(f"  [OK] Generated: {summary_path.name}")


def main():
    """Main execution pipeline."""
    print("=" * 70)
    print("Substack Translation Automation")
    print("=" * 70)

    # Setup paths
    export_dir = Path("substack_export")
    hugo_dir = Path(".")
    output_dir = Path("output")

    # Ensure output directories exist
    (output_dir / "drafts").mkdir(parents=True, exist_ok=True)
    (output_dir / "reports").mkdir(parents=True, exist_ok=True)

    # Step 1: Parse Substack export
    print("\n[1/6] Parsing Substack export...")
    articles = parse_substack_export(export_dir)
    print(f"  [OK] Found {len(articles)} total published articles")

    # Step 2: Identify new articles
    print("\n[2/6] Identifying new articles...")
    new_articles = identify_new_articles(articles, hugo_dir)
    print(f"  [OK] Found {len(new_articles)} new articles to translate")

    if not new_articles:
        print("\n[OK] No new articles to translate!")
        return

    # Step 3: Classify complexity
    print("\n[3/6] Classifying article complexity...")
    for article in new_articles:
        article['complexity'] = classify_complexity(article)

    complexity_counts = {}
    for article in new_articles:
        c = article['complexity']
        complexity_counts[c] = complexity_counts.get(c, 0) + 1

    print(f"  [OK] Complex: {complexity_counts.get('Complex', 0)}")
    print(f"  [OK] Medium: {complexity_counts.get('Medium', 0)}")
    print(f"  [OK] Simple: {complexity_counts.get('Simple', 0)}")

    # Step 4: Process articles
    print(f"\n[4/6] Processing {len(new_articles)} articles...")
    translations = []
    for i, article in enumerate(new_articles, 1):
        title_preview = article['title'][:50] + ('...' if len(article['title']) > 50 else '')
        print(f"  [{i}/{len(new_articles)}] {title_preview}")
        translation = translate_article_with_claude(article)
        translations.append(translation)

    # Step 5: Generate outputs
    print(f"\n[5/6] Generating output files...")
    for translation in translations:
        article = translation['original']
        generate_markdown_file(article, translation, output_dir)
        generate_editorial_report(article, translation, output_dir)
        generate_comparison(article, translation, output_dir)
    print(f"  [OK] Generated {len(translations) * 4} files")

    # Step 6: Generate master documents
    print("\n[6/6] Generating master documents...")
    generate_review_checklist(new_articles, output_dir)
    generate_translation_summary(new_articles, output_dir)

    print("\n" + "=" * 70)
    print("[OK] Translation automation complete!")
    print("=" * 70)
    print(f"\n[DIR] Output location: {output_dir.absolute()}")
    print(f"[DOC] Review checklist: {output_dir / 'review-checklist.md'}")
    print(f"[CHART] Translation summary: {output_dir / 'translation-summary.md'}")
    print(f"\n[NOTE] Next steps:")
    print("   1. Review translations in priority order (Complex → Medium → Simple)")
    print("   2. Apply full editorial workflow to each article")
    print("   3. Approve: ./scripts/approve-article.sh <article-id>")
    print("   4. Commit and deploy approved translations")
    print()


if __name__ == "__main__":
    main()

