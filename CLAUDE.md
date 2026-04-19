# CLAUDE.md

Guidance for Claude Code working in this repository.

## Project Overview

FeiThink (`feithink.org`) is a bilingual personal journal built on **Astro 6.x** with the **astro-theme-retypeset** theme. Deployed to Cloudflare Pages from the `main` branch.

Positioning: *思想 + 生活的持续记录* — essays on moral philosophy (primary) plus life moments (secondary). Not a curated philosophy column. Tagline: `Plain living, high thinking.` (Wordsworth, 1802).

Primary language: English, with Chinese footer entry. Substack (`https://feithink.substack.com`) is the first-publish channel; selected essays migrate here.

## Essential Commands

Package manager: **pnpm 10.33** on Node ≥ 22.12. Do **not** use npm or yarn.

```bash
pnpm install                 # install deps
pnpm dev                     # astro check + dev server (http://localhost:4321)
pnpm build                   # astro check + production build → dist/
pnpm preview                 # serve dist/ locally
pnpm test                    # vitest run (unit tests under src/**/*.test.ts, scripts/**/*.test.ts)
pnpm test:watch              # vitest in watch mode
pnpm lint                    # eslint
pnpm lint:fix                # eslint --fix
pnpm migrate                 # scripts/migrate/migrate.ts — Substack/Hugo → posts
pnpm curate                  # scripts/curate/curate.ts — apply line/pin/standalone metadata
```

Running a single test file: `pnpm vitest run path/to/file.test.ts`.

## Architecture

### Stack

- **Astro 6.1+** static site generator
- **astro-theme-retypeset** (vendored under `src/` — *not* a git submodule)
- **UnoCSS** for styling (`uno.config.ts`)
- **MDX** for rich content, **KaTeX** for math, **Mermaid** for diagrams
- **@astrojs/sitemap**, **astro-compress**, **astro-og-canvas** (OG images), **feed** (RSS)
- **Vitest** for unit tests, **Playwright** listed but not wired to tests

### Directory layout (`src/`)

```
src/
├── assets/          theme assets
├── components/      .astro components
├── content/
│   ├── posts/       all essays + moments, bilingual (*.en.md / *.zh.md)
│   └── about/       about-en.md, about-zh.md
├── content.config.ts    Zod schema for posts + about collections (source of truth for frontmatter)
├── config.ts        site config (title, author, url, colors, menu, comment, seo)
├── i18n/            locale config + UI strings
├── layouts/         page layouts
├── pages/           routes (index, posts/, moments/, zh/, about/, archive, tags, atom.xml, etc.)
├── plugins/         custom remark/rehype plugins (reading-time, directives, heading-anchor, image-processor)
├── styles/          global styles, fonts
├── types/
└── utils/           content.ts helpers: getEssays, getMoments, getPinned, etc.
```

### Content model

Single `posts` collection with a `type` discriminator:

- `type: 'essay'` (default) — the long-form writing
- `type: 'moment'` — low-frequency life markers; may include `image`, `images`, `relatedEssay`

Bilingual convention: posts use paired files `{slug}.en.md` + `{slug}.zh.md`. Where only one language exists, use the proper `.en.md` or `.zh.md` suffix anyway; `lang` frontmatter is derived.

### Post frontmatter (from `src/content.config.ts`)

```yaml
---
title: "Post title"          # required
published: 2026-04-18        # required, Date
description: ""              # optional
updated: 2026-04-19          # optional
tags: [tag-one, tag-two]     # optional, kebab-case
draft: false                 # default false
pin: 0                       # 0–99, higher pins higher on home
toc: true                    # defaults from themeConfig.global.toc
lang: en                     # '' | 'en' | 'zh'
abbrlink: ""                 # optional, [a-z0-9-]
# FeiThink curation
line: kant                   # one of: kant | dostoevsky-and-literature | existence-and-self | moral-life
standalone: false            # true to exclude from any line
# Journal redesign (moments)
type: essay                  # 'essay' (default) | 'moment'
image: "/path.jpg"           # moment-only
images: ["..."]              # moment-only
relatedEssay: "slug"         # moment-only
---
```

**Reading lines** (used as Essays-page tag bar):
- `kant` — Kantian moral philosophy
- `dostoevsky-and-literature` — Dostoevsky + broader literary essays
- `existence-and-self` — existential psychology, selfhood
- `moral-life` — applied ethics / lived practice

Use the `curate` script (`scripts/curate/curate.ts`) to attach `line` / `pin` / `standalone` — the mapping lives there; don't hand-edit frontmatter for curation.

### Home-page composition

`hero paragraph → 3 pinned essays → Latest moments (2) → Recent essays (5)`. Pin slots (as of 2026-04): 99 *Why We Read Kant* / 98 *Brothers Karamazov* / 97 *积极之爱* / 96 *Ikiru* / 95 *Dumbledore*.

### i18n

Default locale `en`; Chinese mounted under `/zh/`. Locale map in `src/i18n/config.ts`. UI strings in `src/i18n/ui.ts`. Trailing slash is always `'always'`.

### Deployment

- **Cloudflare Pages** project `feithink` auto-deploys `main` → `feithink.pages.dev` → alias to `feithink.org` (root + `www`). No GitHub Actions workflow.
- CF Pages **production branch = `main`** (was wrong until 2026-04-19; if you see builds succeed but production not updating, check this setting).
- DNS + domain registration both on Cloudflare.
- Historical anchors: tag `hugo-final-pre-astro` (pre-migration), tag `astro-launch-ready` (merge HEAD).

## Scripts

- `scripts/migrate/migrate.ts` (+ `transform.ts`, `transform.test.ts`) — one-off import of Substack/Hugo exports into `src/content/posts/`.
- `scripts/curate/curate.ts` — idempotent: writes `line` / `pin` / `standalone` frontmatter based on an in-file map.
- `scripts/approve-article.sh` — promotes a draft from `output/drafts/` to `src/content/posts/`. Header comment still says "Hugo" but operates on current paths.
- `scripts/translate_substack.py` + `scripts/requirements.txt` — Python translation helper (runs outside the Astro build).

## Reference Documents

Design and planning docs live under `docs/`:

- `docs/plans/2026-04-18-journal-redesign-design.md` — **current site positioning** (overrides earlier 04-17 design)
- `docs/plans/2026-04-18-journal-redesign-implementation.md` — journal redesign execution record
- `docs/plans/2026-04-18-astro-migration-implementation.md` — Hugo → Astro migration record
- `docs/plans/2026-04-17-hugo-redesign-design.md` — earlier "curated column" framing (superseded for positioning, but still relevant for IA details)
- `docs/plans/2026-04-18-multi-platform-publisher-design.md` — multi-channel publisher (not yet implemented)
- `docs/plans/2026-03-16-substack-translation-automation-design.md`
- `docs/plans/astro-migration-log.md`
- `docs/content-polish/translation-proofread-queue.md` — **active** bilingual proofread queue (Phase 1A–3)
- `docs/content-polish/essays-curation-matrix.md` — line/pin decisions
- `docs/content-polish/about-skeleton-questions.md` — About-page skeleton notes

## Conventions

- **Frontmatter**: match `src/content.config.ts` exactly — Astro's Zod schema will fail the build on drift. `tags` are kebab-case. `published` is a Date, not a string.
- **File naming**: `{numeric-id}-{kebab-slug}.{lang}.md`. Numeric prefix is the Substack post ID when migrated; pure slugs are fine for native posts.
- **Bilingual translation rule** (from user memory): when the ZH text quotes/alludes to a named work, the EN version must use the canonical English word-pair from the original, not a paraphrase. EN files must not contain CJK characters.
- **Theme is vendored, not submodule**: editing files under `src/` that come from retypeset is fine; no `git submodule update` needed.

## Do Not

- Re-create Hugo artifacts (`config.yml`, `themes/PaperMod/`, `content/`, `archetypes/`, `auto-deploy.sh`, `.github/workflows/hugo.yml`) — all intentionally removed.
- Use `npm` or `yarn` — this project uses `pnpm` and pinned lockfile.
- Commit `output/`, `dist/`, `.astro/`, `substack_export/`, `/wechat_draft_*.md`, screenshots, or zip files — all gitignored.
- Treat `redesign-astro` as live — that branch was deleted locally and remote after the 2026-04-18 merge.
