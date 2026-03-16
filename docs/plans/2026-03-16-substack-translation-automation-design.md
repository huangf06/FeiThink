# Substack Translation Automation System Design

**Date:** 2026-03-16
**Author:** Claude (Opus 4.6)
**Status:** Approved

## Overview

Automated system to translate Chinese articles from Substack export into publication-quality English for Hugo bilingual blog, with staged review workflow.

## Requirements

- Source: Substack export file (mr5GIyBeQdKuigbguBqPBg.zip)
- Target: Hugo static site with bilingual content (EN/ZH)
- Quality: Top-tier essay translation with editorial rigor
- Workflow: Hybrid auto-translate + staged review

## System Architecture

### Core Components

1. **Substack Parser Module**
   - Reads exported Substack data
   - Extracts: title, date, content, URL, ID
   - Identifies new articles by comparing with existing content/posts/*.zh.md

2. **Translation Engine**
   - Applies full editorial workflow per article
   - Outputs: diagnosis, title options, translation, editorial notes
   - Generates Hugo-compatible markdown

3. **Complexity Classifier**
   - Assigns: Simple / Medium / Complex
   - Criteria: length, philosophical density, cultural references
   - Generates prioritized review checklist

4. **Output Structure**
   ```
   output/
   ├── drafts/
   │   ├── {id}-{slug}.en.md
   │   └── {id}-{slug}.zh.md
   ├── reports/
   │   ├── {id}-{slug}-editorial.md
   │   └── comparison-{id}.md
   ├── review-checklist.md
   └── translation-summary.md
   ```

5. **Approval Script**
   - Command: `approve-article.sh {id}`
   - Moves from output/drafts/ to content/posts/
   - Updates review checklist

## Translation Workflow

For each new article:

1. Article diagnosis (status, theme, tone, complexity)
2. Title generation (recommended + alternatives)
3. Full translation (editorial principles applied)
4. Editorial notes (assessment, improvements, decisions)
5. Output generation (Hugo markdown + reports)

## Complexity Classification

- **Simple**: Straightforward narrative, <1500 words, minimal cultural references
- **Medium**: Some philosophy, 1500-3000 words, moderate cultural depth
- **Complex**: Dense philosophy, >3000 words or high conceptual density

Review priority: Complex → Medium → Simple

## Data Flow

```
Substack ZIP → Extract → Parse → Compare with Hugo
    → Identify NEW articles
    → Classify complexity
    → Apply editorial workflow
    → Generate translations + reports
    → Output to drafts/
    → Generate master documents
    → Notify for staged review
```

## Implementation Plan

See: 2026-03-16-substack-translation-automation-plan.md
