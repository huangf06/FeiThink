# FeiThink Journal Redesign — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Implement the approved journal redesign: add `moment` as a new content type, build a Moments memory-wall page, rewrite the home page around essays + moments, and update navigation to 5 items.

**Architecture:** Single `posts` content collection discriminated by a new `type: 'essay' | 'moment'` field. New Astro routes at `/moments/` and `/moments/[slug]/` (plus `/zh/...` equivalents). New `MomentCard.astro` component with two variants (home-featured and index-grid). Home page restructures into pinned essays + latest moments + recent essays sections. Navbar grows from 4 to 5 items. All changes additive; existing 25 English + 48 Chinese essays need no frontmatter migration because `type` defaults to `'essay'`.

**Tech Stack:** Astro 6.1.5, astro-theme-retypeset, TypeScript, Zod, vitest (colocation pattern: `foo.ts` + `foo.test.ts`), UnoCSS, pnpm 10.33.0, Node 22.

**Branch / Worktree:** All work happens in `../FeiThink-astro` worktree on branch `redesign-astro`. No destructive steps in this plan — every push auto-deploys to the CF Pages temp URL (`feithink.pages.dev`), which is not yet bound to `feithink.org`, so there is no production risk. Final cutover to `feithink.org` is out of scope (Task 7.4 of the prior implementation plan).

**Design Source:** `docs/plans/2026-04-18-journal-redesign-design.md`

**Seed content:** The plan does NOT create real seed moments — owner decides when the first real moment is worth posting. Each page is tested with a minimal fixture moment that lives only in tests, so production ships with an empty Moments wall.

---

## Phase 1: Schema Extension

### Task 1.1: Extend posts schema with type/image/images/relatedEssay

**Files:**
- Modify: `src/content.config.ts`

**Step 1: Edit the schema**

Add these fields inside the `posts` collection `z.object({...})`, right after the `standalone` field (after the `// FeiThink curation` block):

```ts
    // FeiThink journal redesign (2026-04-18)
    type: z.enum(['essay', 'moment']).optional().default('essay'),
    image: z.string().optional(),
    images: z.array(z.string()).optional(),
    relatedEssay: z.string().optional(),
```

**Step 2: Verify existing content still validates**

Run: `pnpm astro check`
Expected: No errors. All 25 English + 48 Chinese essays continue to validate because `type` defaults to `'essay'`.

**Step 3: Run existing tests**

Run: `pnpm test`
Expected: 11/11 passing (nothing changed behaviorally).

**Step 4: Commit**

```bash
git add src/content.config.ts
git commit -m "feat(schema): add type/image/images/relatedEssay to posts collection"
```

---

## Phase 2: Content Helpers

### Task 2.1: Add `getEssays` and `getMoments` helpers (TDD)

**Files:**
- Modify: `src/utils/content.ts`
- Test: `src/utils/content.test.ts` (create)

**Step 1: Write the failing test**

Create `src/utils/content.test.ts`:

```ts
import { describe, it, expect, vi, beforeEach } from 'vitest'

vi.mock('astro:content', () => ({
  getCollection: vi.fn(),
  render: vi.fn(async () => ({ remarkPluginFrontmatter: { minutes: 1 } })),
}))

vi.mock('@/config', () => ({
  defaultLocale: 'en',
}))

import { getCollection } from 'astro:content'
import { getEssays, getMoments } from './content'

const mockPost = (overrides: any) => ({
  id: overrides.id ?? 'x',
  data: {
    title: 't',
    published: new Date('2026-01-01'),
    description: '',
    tags: [],
    draft: false,
    pin: 0,
    toc: false,
    lang: 'en',
    abbrlink: '',
    type: 'essay',
    ...overrides.data,
  },
})

describe('getEssays / getMoments', () => {
  beforeEach(() => vi.clearAllMocks())

  it('getEssays returns only type=essay, excluding drafts', async () => {
    ;(getCollection as any).mockResolvedValue([
      mockPost({ id: 'a', data: { type: 'essay' } }),
      mockPost({ id: 'b', data: { type: 'moment' } }),
      mockPost({ id: 'c', data: { type: 'essay', draft: true } }),
    ])
    const result = await getEssays('en')
    expect(result.map(p => p.id)).toEqual(['a'])
  })

  it('getMoments returns only type=moment, excluding drafts', async () => {
    ;(getCollection as any).mockResolvedValue([
      mockPost({ id: 'a', data: { type: 'essay' } }),
      mockPost({ id: 'b', data: { type: 'moment', published: new Date('2026-01-01') } }),
      mockPost({ id: 'c', data: { type: 'moment', published: new Date('2026-02-01') } }),
    ])
    const result = await getMoments('en')
    // sorted newest first
    expect(result.map(p => p.id)).toEqual(['c', 'b'])
  })
})
```

**Step 2: Run to confirm failure**

Run: `pnpm test src/utils/content.test.ts`
Expected: FAIL — `getEssays`/`getMoments` not exported.

**Step 3: Implement**

Append to `src/utils/content.ts` (before the existing `_getPostsByYear` if it helps, otherwise at bottom before the final memoized exports block — keep alphabetical-ish):

```ts
async function _getEssays(lang?: Language) {
  const posts = await _getPosts(lang)
  return posts.filter(p => (p.data.type ?? 'essay') === 'essay')
}

async function _getMoments(lang?: Language) {
  const posts = await _getPosts(lang)
  return posts
    .filter(p => p.data.type === 'moment')
    .sort((a, b) => b.data.published.getTime() - a.data.published.getTime())
}

export const getEssays = memoize(_getEssays)
export const getMoments = memoize(_getMoments)
```

Note: `_getPosts` already sorts by date descending and excludes drafts — we only need the extra filter. If `_getPosts` is not accessible (it may be scoped), thread through `getPosts` (the memoized version) instead.

**Step 4: Run test**

Run: `pnpm test src/utils/content.test.ts`
Expected: PASS.

**Step 5: Commit**

```bash
git add src/utils/content.ts src/utils/content.test.ts
git commit -m "feat(content): add getEssays and getMoments helpers"
```

---

### Task 2.2: Add `groupMomentsByYear` helper (TDD)

**Files:**
- Modify: `src/utils/content.ts`
- Modify: `src/utils/content.test.ts`

**Step 1: Add failing test**

Append to `src/utils/content.test.ts`:

```ts
import { groupMomentsByYear } from './content'

describe('groupMomentsByYear', () => {
  it('groups moments by year, newest year first, newest moment first within a year', async () => {
    ;(getCollection as any).mockResolvedValue([
      mockPost({ id: 'a', data: { type: 'moment', published: new Date('2024-06-01') } }),
      mockPost({ id: 'b', data: { type: 'moment', published: new Date('2026-03-01') } }),
      mockPost({ id: 'c', data: { type: 'moment', published: new Date('2026-01-15') } }),
    ])
    const result = await groupMomentsByYear('en')
    expect(result.map(g => g.year)).toEqual([2026, 2024])
    expect(result[0].moments.map(m => m.id)).toEqual(['b', 'c'])
  })
})
```

**Step 2: Run to fail**

Run: `pnpm test src/utils/content.test.ts`
Expected: FAIL — `groupMomentsByYear` not exported.

**Step 3: Implement**

Append to `src/utils/content.ts`:

```ts
async function _groupMomentsByYear(lang?: Language) {
  const moments = await _getMoments(lang)
  const map = new Map<number, typeof moments>()
  for (const m of moments) {
    const y = m.data.published.getFullYear()
    const arr = map.get(y) ?? []
    arr.push(m)
    map.set(y, arr)
  }
  return [...map.entries()]
    .sort(([a], [b]) => b - a)
    .map(([year, moments]) => ({ year, moments }))
}

export const groupMomentsByYear = memoize(_groupMomentsByYear)
```

**Step 4: Run**

Run: `pnpm test`
Expected: all tests pass.

**Step 5: Commit**

```bash
git add src/utils/content.ts src/utils/content.test.ts
git commit -m "feat(content): add groupMomentsByYear helper"
```

---

## Phase 3: i18n + Navbar

### Task 3.1: Add `moments` translation key

**Files:**
- Modify: `src/i18n/ui.ts`

**Step 1: Add `moments` field**

In the `Translation` interface (or the equivalent type), add:

```ts
moments: string
```

In the `en` object:

```ts
moments: 'Moments',
```

In the `zh` object:

```ts
moments: '时刻',
```

**Step 2: Verify types**

Run: `pnpm astro check`
Expected: no errors.

**Step 3: Commit**

```bash
git add src/i18n/ui.ts
git commit -m "feat(i18n): add moments translation key"
```

---

### Task 3.2: Add `isMomentsPage` to page utils

**Files:**
- Modify: `src/utils/page.ts`

**Step 1: Find the existing page helpers**

Open `src/utils/page.ts`. Locate `isEssaysPage` and `isWorkPage`.

**Step 2: Add parallel helper**

Add after `isWorkPage`:

```ts
export function isMomentsPage(pathname: string) {
  // Matches /moments, /moments/, /moments/slug, /zh/moments, etc.
  return /^\/(?:[a-z]{2}\/)?moments(?:\/.*)?$/.test(pathname)
}
```

Extend the `getPageInfo` function to include `isMoments`:

```ts
return {
  ...,
  isMoments: isMomentsPage(pathname),
}
```

**Step 3: Build check**

Run: `pnpm astro check`
Expected: no errors.

**Step 4: Commit**

```bash
git add src/utils/page.ts
git commit -m "feat(page): add isMomentsPage helper"
```

---

### Task 3.3: Add Moments to Navbar (5 items)

**Files:**
- Modify: `src/components/Navbar.astro`

**Step 1: Edit Navbar**

Insert the Moments link between Essays and Work. The anchor path is `/moments/` for English, `/${currentLang}/moments/` for non-default locales — use the existing `getLocalizedPath` helper.

Active-state logic: the Moments link highlights when `isMoments` is true.

**Step 2: Build**

Run: `pnpm build`
Expected: builds cleanly; 5-item nav shows on every page.

**Step 3: Commit**

```bash
git add src/components/Navbar.astro
git commit -m "feat(nav): add Moments as fifth nav item"
```

---

## Phase 4: Moment Card Component

### Task 4.1: Create MomentCard.astro with two variants

**Files:**
- Create: `src/components/MomentCard.astro`

**Step 1: Author the component**

```astro
---
import type { CollectionEntry } from 'astro:content'
import { getLocalizedPath } from '@/utils/path' // adjust import to the project's existing helper
import PostDate from '@/components/PostDate.astro'

interface Props {
  moment: CollectionEntry<'posts'>
  variant: 'home' | 'index'
}

const { moment, variant } = Astro.props
const slug = moment.data.abbrlink || moment.id.split('/').pop()?.replace(/\.mdx?$/, '') || moment.id
const lang = moment.data.lang || 'en'
const href = lang === 'en' ? `/moments/${slug}/` : `/${lang}/moments/${slug}/`
const cover = moment.data.image ?? moment.data.images?.[0]
---

<article class:list={['moment-card', variant === 'home' ? 'moment-card--home' : 'moment-card--index', 'mb-6']}>
  <a href={href} class="block">
    {cover && (
      <img src={cover} alt="" class:list={['moment-card__img rounded', variant === 'home' ? 'aspect-16/9 w-full object-cover' : 'aspect-16/9 w-full object-cover']} loading="lazy" />
    )}
    <div class="mt-3">
      {moment.data.title && (
        <h3 class="text-4.5 font-medium leading-tight cjk:tracking-wide lg:text-5 hover:c-primary transition-colors">
          {moment.data.title}
        </h3>
      )}
      <div class="mt-1 text-3.2 c-secondary lg:text-3.4">
        <PostDate date={moment.data.published} />
      </div>
      {moment.data.description && (
        <p class="mt-2 heti text-3.6 leading-1.6 lg:text-3.8 line-clamp-2">
          {moment.data.description}
        </p>
      )}
    </div>
  </a>
</article>
```

Adjust import paths to match the actual project (especially `getLocalizedPath`; fall back to constructing the href manually as shown if that helper isn't there).

**Step 2: Build check**

Run: `pnpm build`
Expected: component is unused yet so no visible change; build passes.

**Step 3: Commit**

```bash
git add src/components/MomentCard.astro
git commit -m "feat(component): add MomentCard with home/index variants"
```

---

## Phase 5: Moment Detail Page

### Task 5.1: Create moment detail route (English)

**Files:**
- Create: `src/pages/moments/[slug].astro`

**Step 1: Scaffold**

Look at how `src/pages/posts/[slug].astro` (or equivalent existing essay detail page) is structured. Copy that structure, then:

- In `getStaticPaths`: use `getMoments('en')` instead of `getEssays('en')` / `getPosts`.
- Pass the moment entry to the same `Layout` or a new `MomentLayout` if the essay layout feels wrong.
- Keep markdown rendering. Add a small image gallery at the top if `moment.data.images` exists (one image full width, multiple images grid).

Start with the simplest version: reuse essay layout with title + date + rendered markdown. Refine visuals in a later task if they feel wrong.

**Step 2: Add one test fixture moment**

Create `src/content/posts/en/moments/test-fixture.md` — **but prefix with `draft: true` in frontmatter** so it never ships:

```md
---
title: Test Fixture Moment
published: 2026-04-18
lang: en
type: moment
draft: true
description: Test fixture; do not ship.
abbrlink: test-fixture-moment
---

Fixture body for build-time verification.
```

This lets us exercise `getStaticPaths` and the detail page template during dev without polluting production. Remove this file at the end of Phase 10 (Task 10.3).

**Step 3: Dev build check**

Run: `pnpm dev` briefly (or `pnpm build` — drafts appear in dev, are excluded from production build). To test the route exists, temporarily flip `draft: false`, build, confirm `dist/moments/test-fixture-moment/index.html` exists, then flip back.

**Step 4: Commit**

```bash
git add src/pages/moments/[slug].astro src/content/posts/en/moments/test-fixture.md
git commit -m "feat(page): moment detail route (en)"
```

---

### Task 5.2: Create moment detail route (Chinese + other locales)

**Files:**
- Create: `src/pages/[...lang]/moments/[slug].astro`

**Step 1: Mirror Task 5.1 for non-default locales**

Same structure. `getStaticPaths` returns `[lang, slug]` pairs across `moreLocales`. Use `getMoments(lang)` for each.

**Step 2: Build check**

Run: `pnpm build`
Expected: builds clean. No moment pages in dist yet (only the draft fixture, which is excluded).

**Step 3: Commit**

```bash
git add src/pages/[...lang]/moments/[slug].astro
git commit -m "feat(page): moment detail route (non-default locales)"
```

---

## Phase 6: Moments Index Page

### Task 6.1: Create Moments index (English)

**Files:**
- Create: `src/pages/moments/index.astro`

**Step 1: Scaffold**

```astro
---
import Layout from '@/layouts/Layout.astro'
import MomentCard from '@/components/MomentCard.astro'
import { groupMomentsByYear } from '@/utils/content'

const groups = await groupMomentsByYear('en')
---

<Layout postTitle="Moments" postDescription="Things I want to remember.">
  <header class="mb-8">
    <h1 class="mb-2 text-5.5 font-bold leading-tight cjk:tracking-wide lg:text-6">
      Moments
    </h1>
    <p class="text-3.8 leading-1.6 c-secondary lg:text-4">
      Things I want to remember.
    </p>
  </header>

  {groups.length === 0 && (
    <p class="c-secondary text-3.8 lg:text-4">
      Nothing here yet.
    </p>
  )}

  {groups.map(({ year, moments }) => (
    <section class="mb-10">
      <h2 class="mb-4 text-4.5 font-semibold c-secondary lg:text-5">{year}</h2>
      <div class="grid gap-6 lg:grid-cols-2">
        {moments.map(moment => <MomentCard moment={moment} variant="index" />)}
      </div>
    </section>
  ))}
</Layout>
```

**Step 2: Build check**

Run: `pnpm build`
Expected: `/moments/index.html` exists. With fixture draft excluded, the page shows the "Nothing here yet" empty state. Confirm by opening the built HTML.

**Step 3: Commit**

```bash
git add src/pages/moments/index.astro
git commit -m "feat(page): Moments index (en)"
```

---

### Task 6.2: Create Moments index (non-default locales)

**Files:**
- Create: `src/pages/[...lang]/moments/index.astro`

**Step 1: Mirror Task 6.1**

Use `getStaticPaths` over `moreLocales`. Use `ui[lang].moments` for the page title and a localized empty-state string.

Add empty-state zh string in `src/i18n/ui.ts`:

```ts
// en
momentsEmpty: 'Nothing here yet.',
momentsSubtitle: 'Things I want to remember.',

// zh
momentsEmpty: '暂时还没有。',
momentsSubtitle: '那些值得记得的时刻。',
```

**Step 2: Build check**

Run: `pnpm build`
Expected: `/zh/moments/index.html` (and any other locale variant) exists.

**Step 3: Commit**

```bash
git add src/pages/[...lang]/moments/index.astro src/i18n/ui.ts
git commit -m "feat(page): Moments index (non-default locales)"
```

---

## Phase 7: Home Page Rewrite

### Task 7.1: Rewrite English home with new section structure

**Files:**
- Modify: `src/pages/index.astro`

**Step 1: Replace the "By reading line" section**

Current home has: hero → pinned (3) → "By reading line" (4 lines). Replace the "By reading line" section with two new sections:

```astro
---
import Layout from '@/layouts/Layout.astro'
import MomentCard from '@/components/MomentCard.astro'
import PostList from '@/components/PostList.astro' // or existing equivalent
import { getPinnedPosts, getEssays, getMoments } from '@/utils/content'
import { getPostPath } from '@/i18n/path'

const pinned = await getPinnedPosts('en')
const latestMoments = (await getMoments('en')).slice(0, 2)
const recentEssays = (await getEssays('en'))
  .filter(p => !p.data.pin) // exclude pinned to avoid double-listing
  .slice(0, 5)
---

<Layout>
  {/* --- hero: keep existing paragraph; it's fine --- */}
  <section class="hero mb-10">
    <p class="text-3.8 leading-1.7 lg:text-4">
      Longform writing on Kant, Dostoevsky, and the moral life. Curated from
      years at <a
        class="highlight-hover transition-colors hover:c-primary"
        href="https://feihuang.substack.com"
        target="_blank"
        rel="noopener noreferrer"
      >FeiThink on Substack</a>. New work goes there first.
    </p>
  </section>

  {/* --- Pinned (unchanged) --- */}
  {pinned.length > 0 && (
    <section class="mb-10">
      <div class="uno-decorative-line" />
      <p class="mb-4 text-3 font-semibold uppercase tracking-widest c-secondary lg:text-3.2">
        Start here
      </p>
      {/* keep existing pinned list rendering */}
      ...
    </section>
  )}

  {/* --- Latest moments (NEW) --- */}
  {latestMoments.length > 0 && (
    <section class="mb-10">
      <div class="uno-decorative-line" />
      <div class="mb-4 flex items-baseline justify-between">
        <p class="text-3 font-semibold uppercase tracking-widest c-secondary lg:text-3.2">
          Latest moments
        </p>
        <a href="/moments/" class="text-3.2 c-secondary hover:c-primary transition-colors">See all →</a>
      </div>
      <div class="grid gap-6 lg:grid-cols-2">
        {latestMoments.map(moment => <MomentCard moment={moment} variant="home" />)}
      </div>
    </section>
  )}

  {/* --- Recent essays (replaces "By reading line") --- */}
  <section class="mb-10">
    <div class="uno-decorative-line" />
    <div class="mb-4 flex items-baseline justify-between">
      <p class="text-3 font-semibold uppercase tracking-widest c-secondary lg:text-3.2">
        Recent essays
      </p>
      <a href="/essays/" class="text-3.2 c-secondary hover:c-primary transition-colors">See all →</a>
    </div>
    <PostList posts={recentEssays} />  {/* or reproduce the list markup from essays/index */}
  </section>
</Layout>
```

Notes:
- `PostList` is the existing component used on essays index; check its exact API and prop name and adjust.
- If `PostList` doesn't exist as a reusable component, lift the list markup from `src/pages/essays/index.astro` into a small component or inline.

**Step 2: Build check**

Run: `pnpm build`
Expected: 111+ pages; `/index.html` has the new three-section structure; Moments section is hidden (empty state) because no published moments exist.

**Step 3: Visual check on CF preview**

After push (Task 10.4) verify on `feithink.pages.dev`.

**Step 4: Commit**

```bash
git add src/pages/index.astro
git commit -m "feat(home): add Latest moments section, replace By-reading-line with Recent essays"
```

---

### Task 7.2: Update non-default locale home

**Files:**
- Modify: `src/pages/[...lang]/index.astro`

**Step 1: Parallel update**

Match the English home structure but localize strings via `ui[lang]`. Use `getMoments(lang)` and `getEssays(lang)` per-locale.

Add the missing i18n strings to `src/i18n/ui.ts`:

```ts
// en
latestMoments: 'Latest moments',
recentEssays: 'Recent essays',
seeAll: 'See all →',

// zh
latestMoments: '最近的时刻',
recentEssays: '最近的文章',
seeAll: '查看全部 →',
```

**Step 2: Build check**

Run: `pnpm build`
Expected: `/zh/index.html` has the new three-section structure.

**Step 3: Commit**

```bash
git add src/pages/[...lang]/index.astro src/i18n/ui.ts
git commit -m "feat(home): mirror new structure for non-default locales"
```

---

## Phase 8: Essays Page Adjustment

### Task 8.1: Update Essays index — tag bar on top, chronological list below

**Files:**
- Modify: `src/pages/essays/index.astro`

**Step 1: Restructure**

Current layout shows "lines overview + chronological archive". Flatten to: 4 line-tag buttons at top, chronological essay list below.

```astro
---
import Layout from '@/layouts/Layout.astro'
import { LINES } from '@/data/lines'
import { getEssays } from '@/utils/content'
import PostList from '@/components/PostList.astro' // or equivalent

const essays = await getEssays('en')
---

<Layout postTitle="Essays" postDescription="Longform on Kant, Dostoevsky, and the moral life.">
  <header class="mb-8">
    <h1 class="mb-2 text-5.5 font-bold leading-tight cjk:tracking-wide lg:text-6">
      Essays
    </h1>
    <p class="text-3.8 leading-1.6 c-secondary lg:text-4">
      Longform on Kant, Dostoevsky, and the moral life.
    </p>
  </header>

  <section class="mb-10 flex flex-wrap gap-3">
    {LINES.map(line => (
      <a
        href={`/essays/lines/${line.slug}/`}
        class="inline-block rounded-full border px-4 py-1.5 text-3.4 c-secondary hover:c-primary transition-colors"
      >
        {line.title}
      </a>
    ))}
  </section>

  <section>
    <PostList posts={essays} />
  </section>
</Layout>
```

**Step 2: Build check**

Run: `pnpm build`
Expected: `/essays/` renders with the tag bar and full chronological list.

**Step 3: Commit**

```bash
git add src/pages/essays/index.astro
git commit -m "feat(essays): flatten index to tag bar + chronological list"
```

---

## Phase 9: Tagline / Subtitle

### Task 9.1: Update site subtitle in config.ts

**Files:**
- Modify: `src/config.ts` (or `config.ts` at repo root — whichever the theme uses)

**Step 1: Change subtitle**

Locate `subtitle: 'Essays on moral philosophy',` and change to:

```ts
subtitle: 'Thinking and living — mostly in prose, occasionally in photos.',
```

Owner may later change this text; this is the default.

**Step 2: Build check**

Run: `pnpm build`
Expected: header subtitle updates across all pages.

**Step 3: Commit**

```bash
git add src/config.ts
git commit -m "feat(config): update site subtitle for journal redesign"
```

---

## Phase 10: Verify & Deploy

### Task 10.1: Run full test suite

Run: `pnpm test`
Expected: all tests pass (existing 11 + new content-helper tests = 13+).

### Task 10.2: Run full production build

Run: `pnpm build`
Expected:
- Build succeeds.
- Page count ≥ previous (111 before; new: 111 + `/moments/` + `/zh/moments/` = 113 minimum). Moment detail pages currently zero (fixture excluded).
- No unreferenced-key or missing-translation errors from `astro check`.

### Task 10.3: Remove the test fixture moment

**Files:**
- Delete: `src/content/posts/en/moments/test-fixture.md`

```bash
rm src/content/posts/en/moments/test-fixture.md
pnpm build  # verify still green
git add -A
git commit -m "chore: remove dev-only fixture moment"
```

### Task 10.4: Push to origin

```bash
git push origin redesign-astro
```

CF Pages auto-builds. Watch the deployment at `dash.cloudflare.com` → Pages → feithink → Deployments. First build after this push should succeed (Node 22, Astro build, ~113 pages).

### Task 10.5: Visual QA on the preview URL

Open the new `*.feithink.pages.dev` deployment URL and confirm:
- Home: hero paragraph → pinned essays (3) → "Latest moments" section shows empty or hidden (no moments yet) → "Recent essays" (5 items).
- Nav: 5 items, Moments link goes to `/moments/` and shows "Nothing here yet."
- Essays page: 4 line-tag buttons on top, full chronological list below.
- `/zh/` mirrors the structure with localized strings.
- Old `/GitStack/*` 301 redirects still work.

If anything looks wrong, fix with a follow-up task and re-push.

---

## Open Items (Post-Plan)

1. **Reading lines count** — still 4. Owner can decide later whether to consolidate to 3 or 2. Pure content decision; tag-bar UI handles any count.
2. **Moment detail page layout** — currently reuses essay layout. Revisit if it feels wrong with the first real moment posted.
3. **Archive page** — retypeset's built-in `/archive/` still shows all posts including moments mixed with essays. If that looks weird, add a follow-up task to filter by `type=essay`.
4. **About rewrite / tagline final text** — owner writing tasks; out of scope for this plan.
5. **CF Pages custom domain `feithink.org`** — still deferred (Task 7.4 of prior plan).

---

## Related Documents

- Design: `docs/plans/2026-04-18-journal-redesign-design.md`
- Prior design (partially superseded): `docs/plans/2026-04-17-hugo-redesign-design.md`
- Prior implementation (base architecture, still in force): `docs/plans/2026-04-18-astro-migration-implementation.md`
