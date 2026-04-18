# Migration Session Log

## Environment
- Node: v25.5.0
- pnpm: 10.33.0
- OS: Windows 11 Pro for Workstations
- Worktree: C:\Users\huang\github\FeiThink-astro
- Branch: redesign-astro
- Start date: 2026-04-18

## Retypeset Structure (Task 1.1 recon, commit 2025-xx current main of radishzzz/astro-theme-retypeset)

### Top-level files to copy
- `astro.config.ts`
- `package.json`, `pnpm-lock.yaml`
- `tsconfig.json`
- `uno.config.ts` (UnoCSS)
- `eslint.config.mjs` (optional, can drop)
- `src/` (all subdirs)
- `public/`
- `patches/` (pnpm patch for @qwik.dev/partytown — must keep or pnpm install fails)
- `scripts/` (new-post, apply-lqip, format-posts, update-theme — optional but useful)
- `assets/` (top-level assets referenced by theme)
- `LICENSE`, `README.md` — drop/replace

### Site config location
- `src/config.ts` — the site identity + theme config is here (NOT in astro.config.ts).
  Fields: `site.{title,subtitle,description,author,url,base,favicon}`, `site.i18nTitle`, `color.{mode,light,dark}`, `global.{locale,moreLocales,fontStyle,dateFormat,toc,katex,reduceMotion}`, `comment`, `seo`, `footer.{links,startYear}`, `preload`.
- `astro.config.ts` imports `site`, `base`, `defaultLocale` from `./src/config` and `langMap` from `./src/i18n/config`.

### Content collections — `src/content.config.ts`
```ts
posts: glob `**/*.{md,mdx}` base `./src/content/posts`
  schema: title (string, required), published (date, required),
          description, updated, tags[], draft, pin(0-99), toc, lang(enum), abbrlink
about: glob `**/*.{md,mdx}` base `./src/content/about`
  schema: lang
```

Content dirs:
- `src/content/posts/` — demo content has `examples/`, `guides/`, `_images/`, and a `Universal Post.md`
- `src/content/about/` — one file per locale: `about-en.md`, `about-es.md`, `about-ja.md`, `about-ru.md`, `about-zh.md`, `about-zh-tw.md`

### Pages directory layout
```
src/pages/
├─ index.astro              # default-locale home (= /)
├─ about.astro              # default-locale about (= /about/)
├─ atom.xml.ts, rss.xml.ts  # feeds
├─ robots.txt.ts
├─ 404.astro
├─ config.ts, lang.ts, path.ts, ui.ts   # pages-level helpers
├─ posts/                   # post listing/detail
├─ tags/                    # tags index
├─ og/                      # OpenGraph image generation
└─ [...lang]/               # dynamic routing for non-default locales
   ├─ index.astro, about.astro, posts/, tags/, ...
```

**Critical insight:** Retypeset ALREADY puts the default locale at root (no prefix) and uses `[...lang]/` ONLY for non-default locales. To get "English at /, Chinese at /zh/" we just need to set:
- `global.locale: 'en'`
- `global.moreLocales: ['zh']`

No routing surgery needed (Task 2.1 approach A works trivially).

### i18n — `src/i18n/config.ts`
`langMap` maps path-segment (e.g. 'zh') → BCP-47 codes (e.g. ['zh-CN']). Our `zh` is valid.

### Dependencies to note
- pnpm patches `@qwik.dev/partytown@0.11.2` — must include `patches/` dir and `pnpm.patchedDependencies` in package.json.
- Heavy deps (sharp, canvaskit-wasm, mermaid) — these all compile; Cloudflare Pages build may need `NODE_VERSION=20` or `22`.
- `onlyBuiltDependencies: [esbuild, sharp, simple-git-hooks]` in package.json.

### Fields we need to add in our schema extension (Phase 4.1)
- `line` (enum): kant | dostoevsky-and-literature | existence-and-self | moral-life
- `standalone` (boolean)

All other retypeset fields (`title`, `published`, `description`, `updated`, `tags`, `draft`, `pin`, `toc`, `lang`, `abbrlink`) stay as-is. Our migration script output must match these names. Note:
- Retypeset `published` expects a `z.date()` (parsed from YAML date). Hugo `date: 2025-10-08` (ISO string or YAML date) will coerce correctly.
- `lang` is an enum including `''` (empty = no lang filter). We'll set explicit `'en'` or `'zh'`.
- `pin` is 0-99 (not arbitrary). Plan uses `pin: 99, 98, 97` — all within range.

