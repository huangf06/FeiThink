# Translation Automation System

## Overview

Automated system to translate Chinese articles from Substack export into publication-quality English for the Hugo bilingual blog.

## System Status

✅ **Automation Complete** - 77 new articles processed and ready for translation

### Statistics
- **Total Substack articles:** 122
- **Existing Hugo articles:** 48
- **New articles to translate:** 77
  - Complex: 29 articles (philosophical depth, cultural references)
  - Medium: 35 articles (moderate complexity)
  - Simple: 13 articles (straightforward prose)

### Output Generated
- 154 draft files (EN + ZH pairs) in `output/drafts/`
- 154 report files (editorial + comparison) in `output/reports/`
- Prioritized review checklist: `output/review-checklist.md`
- Translation summary: `output/translation-summary.md`

## Quick Start

### 1. Install Dependencies

```bash
pip install -r scripts/requirements.txt
```

### 2. Run Translation Automation

```bash
python scripts/translate_substack.py
```

This will:
- Parse Substack export from `substack_export/`
- Identify articles not yet in Hugo
- Classify by complexity
- Generate structured drafts and reports

### 3. Review and Translate

Review articles in priority order (Complex → Medium → Simple):

1. Open `output/review-checklist.md` for prioritized list
2. For each article:
   - Read Chinese original in `output/drafts/{id}-{slug}.zh.md`
   - Read editorial report in `output/reports/{id}-{slug}-editorial.md`
   - Open English draft in `output/drafts/{id}-{slug}.en.md`
   - Replace `[TRANSLATION PENDING]` section with polished English translation
   - Apply full editorial workflow per guidelines

### 4. Approve Translated Articles

Once translation is complete and reviewed:

```bash
./scripts/approve-article.sh <article-id>
```

Example:
```bash
./scripts/approve-article.sh 190074339
```

This will:
- Copy EN/ZH files to `content/posts/`
- Set `draft: false` in both files
- Ready for commit and deployment

### 5. Commit and Deploy

```bash
git add content/posts/
git commit -m "feat: add translated article {id}"
git push origin main
```

## Output Structure

```
output/
├── drafts/                    # Translation workspace
│   ├── {id}-{slug}.en.md     # English draft (edit this)
│   ├── {id}-{slug}.zh.md     # Chinese reference
│   └── ...
├── reports/                   # Editorial materials
│   ├── {id}-{slug}-editorial.md    # Editorial report
│   ├── comparison-{id}.md          # Side-by-side comparison
│   └── ...
├── review-checklist.md        # Prioritized review list
└── translation-summary.md     # Overview and statistics
```

## Translation Guidelines

Apply these principles to every article:

### Core Principles

1. **Accuracy first** - Preserve meaning, argument flow, emotional logic
2. **Strong English prose** - Remove Chinglish, use idiomatic English
3. **Keep author's voice** - Serious, reflective, intellectually ambitious
4. **Good taste** - Avoid melodrama, pompous phrasing, cliché self-help tone
5. **Signal difficult choices** - Provide title alternatives, note translation tradeoffs

### Quality Bar

- Top-tier essay translation
- Serious magazine-level editing
- Elite bilingual editorial work

### Workflow for Each Article

1. **Diagnose** - Assess theme, tone, complexity, challenges
2. **Title** - Provide recommended English title + 2-4 alternatives
3. **Translate** - Apply full editorial rigor
4. **Review** - Check accuracy, tone, naturalness
5. **Document** - Note key decisions in editorial report

## Complexity Levels

### Complex (29 articles)
- Dense philosophical argumentation
- Heavy cultural/literary references
- Sophisticated rhetorical devices
- > 3000 chars or high conceptual density
- **Review priority: HIGH**

### Medium (35 articles)
- Some philosophical concepts
- Moderate cultural references
- Mixed prose styles
- 1500-3000 chars
- **Review priority: MEDIUM**

### Simple (13 articles)
- Straightforward narrative
- Minimal cultural-specific references
- Clear, direct prose
- < 1500 chars
- **Review priority: LOWER**

## Files and Scripts

### Main Scripts

- `scripts/translate_substack.py` - Main automation pipeline
- `scripts/approve-article.sh` - Approval and deployment script
- `scripts/requirements.txt` - Python dependencies

### Key Outputs

- `output/review-checklist.md` - Start here for translation work
- `output/translation-summary.md` - Overview and statistics
- `output/drafts/*.en.md` - Edit these files with translations
- `output/reports/*-editorial.md` - Editorial guidance per article

## Workflow Summary

```
Substack Export
    ↓
Parse & Identify New Articles (77 found)
    ↓
Classify Complexity (Complex/Medium/Simple)
    ↓
Generate Drafts + Reports
    ↓
Manual Translation Work (YOU ARE HERE)
    ↓
Approve Articles (./scripts/approve-article.sh)
    ↓
Commit & Deploy to Hugo
```

## Next Steps

1. **Start with Complex articles** - See `output/review-checklist.md`
2. **Apply editorial workflow** - Follow translation guidelines
3. **Approve completed work** - Use approval script
4. **Deploy incrementally** - Commit and push approved translations

## Notes

- All translations start as drafts (`draft: true`)
- Original Chinese saved for reference
- Side-by-side comparisons available in reports
- Approval script handles file movement and draft status
- System can be re-run to process additional Substack exports

## Support

For questions or issues with the automation system, check:
- `output/translation-summary.md` for overview
- `output/reports/{id}-{slug}-editorial.md` for per-article guidance
- Original editorial guidelines document

---

**Status:** ✅ Automation complete - Ready for manual translation work
**Generated:** 2026-03-16
**Articles pending translation:** 77
