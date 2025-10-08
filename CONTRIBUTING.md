# Contributing to the Portfolio

Thank you for considering contributing to this portfolio! This guide will help you add new articles and improve the site.

## Quick Start: Adding a New Article

### 1. Create the Article File

Navigate to the appropriate category directory and create a new markdown file:

```bash
# For philosophy articles
touch content/philosophy/your-article-name.md

# For literature articles
touch content/literature/your-article-name.md

# For essays
touch content/essays/your-article-name.md
```

Or use Hugo CLI (if installed):
```bash
hugo new philosophy/your-article-name.md
```

### 2. Add Front Matter

Every article must start with YAML front matter. Here's the standard template:

```yaml
---
title: "Your Article Title"
date: 2025-10-08
lastmod: 2025-10-08
draft: false
categories: ["Philosophy"]  # or ["Literature"], ["Essays"]
tags: ["tag1", "tag2", "tag3"]
summary: "A brief 1-2 sentence summary for SEO and card displays"
weight: 999
author: "Your Name"
showToc: true
TocOpen: false
hidemeta: false
comments: true
description: ""
disableShare: false
searchHidden: false
---
```

### 3. Write Your Content

After the front matter, write your article using Markdown:

```markdown
## Introduction

Your introduction here...

## Main Content

### Subsection

Your content here...

## Conclusion

Your conclusion here...

---

*Optional footer note or citation*
```

### 4. Preview Locally (Optional)

If you have Hugo installed:

```bash
hugo server -D
```

Then visit `http://localhost:1313` to preview.

### 5. Commit and Push

```bash
git add .
git commit -m "Add article: Your Article Title"
git push origin main
```

GitHub Actions will automatically build and deploy your changes within 1-2 minutes.

## Front Matter Field Reference

| Field | Required | Description | Example |
|-------|----------|-------------|---------|
| `title` | Yes | Article title | `"Understanding Kant"` |
| `date` | Yes | Publication date | `2025-10-08` |
| `lastmod` | No | Last modified date | `2025-10-08` |
| `draft` | Yes | Set to `false` to publish | `false` |
| `categories` | Yes | Category array | `["Philosophy"]` |
| `tags` | Yes | Tag array | `["Kant", "ethics"]` |
| `summary` | Yes | Brief description (SEO) | `"An exploration of..."` |
| `weight` | No | Sort order (lower = first) | `1` |
| `author` | Yes | Author name | `"Your Name"` |
| `showToc` | No | Show table of contents | `true` |
| `TocOpen` | No | Expand TOC by default | `false` |
| `hidemeta` | No | Hide metadata | `false` |
| `comments` | No | Enable comments | `true` |
| `disableShare` | No | Disable share buttons | `false` |
| `searchHidden` | No | Hide from search | `false` |

## Categories

Use exactly one of these categories:
- **Philosophy**: Philosophical translations, ethics, moral philosophy
- **Literature**: Literary analysis, translations of fiction, book reviews
- **Essays**: Personal reflections, opinion pieces, general writing

## Tagging Guidelines

Good tags are:
- **Specific**: Use proper names (Kant, Dostoevsky), specific concepts (categorical-imperative, existentialism)
- **Consistent**: Check existing tags first to maintain consistency
- **Moderate**: Use 3-6 relevant tags per article
- **Lowercase with hyphens**: `moral-philosophy` not `Moral Philosophy`

Common tags by category:

**Philosophy:**
- Ethics: `ethics`, `moral-philosophy`, `virtue-ethics`, `deontology`, `utilitarianism`
- Philosophers: `kant`, `aristotle`, `nietzsche`, `plato`
- Concepts: `free-will`, `consciousness`, `metaphysics`

**Literature:**
- Authors: `dostoevsky`, `tolstoy`, `kafka`, `shakespeare`
- Genres: `russian-literature`, `existential-fiction`, `tragedy`
- Themes: `freedom`, `suffering`, `redemption`, `identity`

**Essays:**
- Topics: `translation`, `writing`, `philosophy`, `personal-growth`
- Themes: `reflection`, `practice`, `learning`

## Weight System

The `weight` field controls article ordering:
- **Lower numbers appear first** in lists
- Default is `999`
- Use `1-10` for featured articles on homepage
- Use `11-99` for important but not featured content
- Use `999` for regular articles (chronological order)

## Markdown Tips

### Headings

```markdown
# H1 - Article Title (automatically added from front matter)
## H2 - Major sections
### H3 - Subsections
#### H4 - Minor points
```

### Emphasis

```markdown
*italic* or _italic_
**bold** or __bold__
***bold italic***
```

### Links

```markdown
[Link text](https://example.com)
[Internal link](/philosophy/kant-ethics/)
```

### Quotes

```markdown
> This is a blockquote
> Multiple lines
```

### Lists

```markdown
- Unordered item 1
- Unordered item 2
  - Nested item

1. Ordered item 1
2. Ordered item 2
```

### Code

```markdown
Inline `code` with backticks

```python
# Code block with syntax highlighting
def hello():
    print("Hello, world!")
```
```

### Images

```markdown
![Alt text](/images/filename.jpg)
```

Place images in the `static/images/` directory.

## Writing Style Guidelines

### Philosophy Articles
- **Define terms**: Don't assume readers know technical philosophical vocabulary
- **Use examples**: Illustrate abstract concepts with concrete cases
- **Cite sources**: Reference original texts when discussing philosophical ideas
- **Be charitable**: Present opposing views fairly before critiquing

### Literature Articles
- **Avoid spoilers** (or warn first): Give readers a chance to read the work first
- **Quote judiciously**: Use quotes to support your analysis
- **Contextualize**: Provide historical/biographical context when relevant
- **Analyze deeply**: Go beyond plot summary to thematic/symbolic analysis

### Essays
- **Be authentic**: Personal essays should reflect genuine experience and thought
- **Stay focused**: One main idea per essay
- **Show, don't tell**: Use specific examples and anecdotes
- **Revise**: Essays benefit from multiple drafts

## Translation Articles

When posting translations:

1. **Cite the original**: Include author, title, year, and edition
2. **Note translation choices**: Explain difficult translation decisions
3. **Preserve structure**: Maintain paragraph breaks and formatting
4. **Add translator's notes**: Use footnotes for necessary clarifications
5. **Copyright**: Ensure you have rights to translate and publish

Example format:

```markdown
---
title: "Title in English (Original Title in Source Language)"
date: 2025-10-08
categories: ["Philosophy"]
tags: ["translation", "author-name", "concept"]
summary: "Translation of Author's essay on Topic"
---

*Translated from [Source Language] by Your Name*

**Original**: Author Name, "Original Title," *Publication*, Year.

---

## [Start of Translation]

Your translation here...

---

### Translator's Notes

[1] Explanation of difficult term...
```

## SEO Best Practices

- **Title**: Clear, descriptive, under 60 characters
- **Summary**: Compelling, 150-160 characters, includes main keywords
- **Headings**: Use logical H2/H3 structure
- **Images**: Include descriptive alt text
- **Links**: Link to related articles when appropriate
- **Keywords**: Naturally incorporate relevant search terms

## Quality Checklist

Before publishing, verify:

- [ ] Front matter is complete and valid YAML
- [ ] Draft is set to `false`
- [ ] Title is clear and compelling
- [ ] Summary accurately describes content
- [ ] Categories and tags are appropriate and consistent
- [ ] Markdown formatting is correct
- [ ] Links work (no broken links)
- [ ] Images display correctly
- [ ] Content is proofread (spelling, grammar, clarity)
- [ ] Article adds value to the portfolio

## Getting Help

- **Hugo issues**: Check [Hugo documentation](https://gohugo.io/documentation/)
- **Theme features**: See [PaperMod wiki](https://github.com/adityatelange/hugo-PaperMod/wiki)
- **Markdown syntax**: See [CommonMark spec](https://commonmark.org/)
- **Build failures**: Check GitHub Actions logs in repository

## Workflow Tips

### Batch Writing
1. Write multiple articles in draft mode (`draft: true`)
2. Review and revise over several days
3. Publish by setting `draft: false` and pushing

### Scheduling
- Set `date` to future date for scheduled publishing
- Hugo won't render future-dated posts unless configured

### Revisions
- Update `lastmod` field when making significant revisions
- Commit with descriptive message: `"Update article: [title] - [change summary]"`

## Style Conventions

- **Dates**: Use ISO format `YYYY-MM-DD`
- **File names**: Use lowercase with hyphens: `kant-categorical-imperative.md`
- **Quotes**: Use proper typographic quotes (" ") not straight quotes (" ")
- **Em dashes**: Use `—` (or `---` in Markdown)
- **Citations**: Use consistent citation style (MLA, APA, or Chicago)

## Advanced: Custom Layouts

For special article types, you can create custom layouts:

1. Create layout file: `layouts/_default/custom-type.html`
2. Specify in front matter: `layout: "custom-type"`

Consult Hugo documentation for layout syntax.

---

Thank you for contributing! Your articles help make this portfolio valuable and engaging.