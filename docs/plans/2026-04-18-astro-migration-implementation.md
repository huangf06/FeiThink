# FeiThink Hugo→Astro Migration Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Migrate `feithink.org` from Hugo+PaperMod to Astro+retypeset, deploy to Cloudflare Pages, retire GitHub Pages.

**Architecture:** Fresh Astro project in an isolated worktree on branch `redesign-astro`. Replace Hugo at repo root (don't subfolder). Retypeset as starting theme, customize homepage/line pages/work/about. Content migrated via a TDD-tested frontmatter transform script. Cutover in one commit that deletes Hugo and merges Astro to main. Cloudflare Pages auto-deploys from main.

**Tech Stack:** Astro 6.x · astro-theme-retypeset (MIT) · pnpm · TypeScript · Content Collections · MDX · Cloudflare Pages · Cloudflare Registrar DNS

**Design source of truth:** `docs/plans/2026-04-17-hugo-redesign-design.md` (§7 tech/theme, §8 workload).

---

## Phase 0: Isolation & Prerequisites

### Task 0.1: Create isolated worktree

**Rationale:** Big destructive refactor (deleting Hugo scaffolding). Worktree keeps main intact for rollback.

**Step 1: Create worktree on new branch**

```bash
git worktree add ../FeiThink-astro -b redesign-astro
cd ../FeiThink-astro
```

**Step 2: Verify clean state**

Run: `git status`
Expected: `On branch redesign-astro`, working tree clean (same tracked files as main).

**Step 3: Verify design doc is present**

Run: `ls docs/plans/`
Expected: `2026-04-17-hugo-redesign-design.md` and `2026-04-18-astro-migration-implementation.md` (this file) both exist.

---

### Task 0.2: Verify Node & pnpm

**Step 1: Check versions**

Run: `node --version && pnpm --version`
Expected: Node ≥ 20.x, pnpm ≥ 9.x. If pnpm missing: `npm install -g pnpm`.

**Step 2: Write down versions to plan log**

Create `docs/plans/astro-migration-log.md` (session log):

```markdown
# Migration Session Log

## Environment
- Node: <version>
- pnpm: <version>
- OS: Windows 11
- Worktree: ../FeiThink-astro
- Branch: redesign-astro
- Start date: 2026-04-18
```

**Step 3: Commit log skeleton**

```bash
git add docs/plans/astro-migration-log.md
git commit -m "chore: start astro migration session log"
```

---

## Phase 1: Astro Scaffolding

### Task 1.1: Study retypeset structure before copying

**Rationale:** Don't guess the file layout. Read the actual repo once.

**Step 1: Clone retypeset to a scratch directory (outside the worktree)**

```bash
cd /tmp  # or any scratch path
git clone --depth 1 https://github.com/radishzzz/astro-theme-retypeset.git retypeset-ref
cd retypeset-ref
```

**Step 2: Inspect structure**

Run: `ls src/ && cat package.json && cat astro.config.ts 2>/dev/null || cat astro.config.mjs`

**Step 3: Record key paths in the log**

Write to `docs/plans/astro-migration-log.md` under "## Retypeset Structure":
- Config file name + path
- Content collections location (`src/content/posts/` or similar)
- Pages directory structure (look for `[...lang]/` routing)
- Theme config location (fontStyle, accentColor, etc.)
- Default index.astro location (this is what we'll override)
- i18n config location and default languages

**Step 4: Note the frontmatter schema**

Run: `cat src/content/config.ts` (or wherever `defineCollection` is)
Copy the schema to log — we need to match field names in the migration script.

**Step 5: Return to worktree**

```bash
cd ../../github/FeiThink-astro  # back to worktree
```

**Step 6: No commit yet — only recon.**

---

### Task 1.2: Initialize Astro project from retypeset

**Step 1: Remove Hugo scaffolding (inside worktree, this is the destructive step — tell the user)**

ASK USER: "About to delete Hugo files: `config.yml`, `themes/`, `content/posts/`, `.github/workflows/hugo.yml`, `auto-deploy.sh`, `deploy.sh`, `deploy-simple.sh`, and any `.bat` equivalents. Confirm?"

After confirmation:

```bash
rm -rf themes/ content/posts/ .github/workflows/hugo.yml \
       config.yml auto-deploy.sh deploy.sh deploy-simple.sh \
       archetypes/
# Keep: docs/, substack_export/, .claude/, CLAUDE.md, ARTICLE_FORMAT.md,
#       README.md, wechat_draft_*.md, output/, mr5*.zip (those are user's
#       personal artifacts, leave alone).
```

**Step 2: Remove submodule registration**

```bash
git rm -f .gitmodules 2>/dev/null || true
git config --remove-section submodule.themes/PaperMod 2>/dev/null || true
```

**Step 3: Copy retypeset scaffold into repo root**

```bash
cp -r /tmp/retypeset-ref/src ./src
cp -r /tmp/retypeset-ref/public ./public
cp /tmp/retypeset-ref/package.json ./package.json
cp /tmp/retypeset-ref/pnpm-lock.yaml ./pnpm-lock.yaml 2>/dev/null || true
cp /tmp/retypeset-ref/astro.config.* ./
cp /tmp/retypeset-ref/tsconfig.json ./tsconfig.json 2>/dev/null || true
cp /tmp/retypeset-ref/.gitignore ./.gitignore.new
# merge .gitignore.new into existing .gitignore
cat .gitignore.new >> .gitignore
rm .gitignore.new
# Copy any other top-level config files retypeset needs (eslint, prettier, etc.)
# Check /tmp/retypeset-ref/ root for missing configs.
```

**Step 4: Install dependencies**

```bash
pnpm install
```

Expected: All deps resolve, no errors.

**Step 5: Run dev server to verify default retypeset works**

```bash
pnpm dev
```

Expected: Dev server starts on `http://localhost:4321` (or similar). Visit it — should see retypeset's default demo posts.

**Step 6: Stop dev server (Ctrl-C)**

**Step 7: Commit scaffold**

```bash
git add -A
git commit -m "feat(scaffold): replace Hugo with Astro+retypeset base"
```

---

### Task 1.3: Minimal site identity config

**Step 1: Identify retypeset's site config file**

From log Task 1.1 recon, open the site config (likely `src/config.ts` or `astro.config.ts`). Update:
- `site: 'https://feithink.org'`
- `title: 'FeiThink'`
- `description: 'Essays on moral philosophy, from a reader of Kant.'` (placeholder, finalized in Phase 6)
- `author: 'Fei Huang'`
- Locale: `en` as default

**Step 2: Update `astro.config.*`**

Ensure `site: 'https://feithink.org'` is set at top of Astro config.

**Step 3: Verify dev server still runs**

```bash
pnpm dev
```

Check localhost — title should now be "FeiThink".

**Step 4: Commit**

```bash
git add -A
git commit -m "feat(config): set site identity for feithink.org"
```

---

### Task 1.4: Remove retypeset's default demo content

**Step 1: List demo posts**

Run: `ls src/content/posts/` (or wherever posts live — from Task 1.1 recon).

**Step 2: Delete all demo posts**

```bash
rm -rf src/content/posts/*
```

Keep the directory structure (just empty it).

**Step 3: Verify dev server still builds (will show empty post list, that's fine)**

```bash
pnpm dev
```

Expected: No errors, post list page is empty.

**Step 4: Commit**

```bash
git add -A
git commit -m "chore: remove retypeset demo content"
```

---

## Phase 2: i18n Routing Decision

### Task 2.1: Flatten English to root, keep `/zh/` for Chinese

**Rationale:** Per design §6, English is primary. Retypeset default `[...lang]` routing puts English at `/en/...` which is wrong for us.

**Step 1: Read retypeset's i18n docs in its README**

Find in `/tmp/retypeset-ref/README.md` or `docs/` section on i18n and `defaultLocale` behavior.

**Step 2: Decide implementation approach**

Two options:
- **A. Configure `defaultLocale: 'en'` with `prefixDefaultLocale: false`** (Astro i18n native flag — this makes English URLs not have `/en/` prefix while other locales keep their prefix). Preferred if retypeset exposes this.
- **B. Restructure the `[...lang]` dynamic routes** to use static `index.astro` at root for English and `/zh/index.astro` for Chinese. More surgery but more explicit.

Try A first. In `astro.config.*`:

```js
i18n: {
  defaultLocale: 'en',
  locales: ['en', 'zh'],
  routing: {
    prefixDefaultLocale: false,
  },
},
```

**Step 3: Test**

```bash
pnpm dev
```

Visit `localhost:4321/` (should be English) and `localhost:4321/zh/` (should be Chinese). If retypeset's `[...lang]` pages fight this, switch to approach B.

**Step 4: Commit**

```bash
git add -A
git commit -m "feat(i18n): English at root, /zh/ for Chinese"
```

---

## Phase 3: Content Migration Script (TDD)

### Task 3.1: Write failing test for Hugo→Astro frontmatter transform

**Files:**
- Create: `scripts/migrate/transform.test.ts`
- Create: `scripts/migrate/transform.ts` (placeholder)

**Step 1: Install test runner if not already**

Check `package.json` — does retypeset ship vitest? If yes, skip install. Otherwise:

```bash
pnpm add -D vitest
```

Add to `package.json`:
```json
"scripts": {
  "test": "vitest run",
  "test:watch": "vitest"
}
```

**Step 2: Write failing test**

Create `scripts/migrate/transform.test.ts`:

```typescript
import { describe, it, expect } from 'vitest'
import { transformFrontmatter } from './transform'

describe('transformFrontmatter', () => {
  it('maps Hugo date to Astro published', () => {
    const hugo = {
      title: 'Test',
      date: '2025-10-08',
      lastmod: '2025-10-09',
      draft: false,
      tags: ['kant', 'morality'],
      summary: 'A test essay.',
    }
    const astro = transformFrontmatter(hugo)
    expect(astro.published).toBe('2025-10-08')
    expect(astro.updated).toBe('2025-10-09')
    expect(astro.title).toBe('Test')
    expect(astro.description).toBe('A test essay.')
    expect(astro.tags).toEqual(['kant', 'morality'])
    expect(astro.draft).toBe(false)
  })

  it('drops Hugo-specific fields (weight, showToc, TocOpen, categories, author)', () => {
    const hugo = {
      title: 'Test',
      date: '2025-10-08',
      weight: 999,
      showToc: true,
      TocOpen: false,
      categories: ['Philosophy'],
      author: 'FeiThink',
    }
    const astro = transformFrontmatter(hugo)
    expect(astro).not.toHaveProperty('weight')
    expect(astro).not.toHaveProperty('showToc')
    expect(astro).not.toHaveProperty('TocOpen')
    expect(astro).not.toHaveProperty('categories')
    expect(astro).not.toHaveProperty('author')
  })

  it('sets default draft=false when Hugo draft unspecified', () => {
    const hugo = { title: 'Test', date: '2025-10-08' }
    const astro = transformFrontmatter(hugo)
    expect(astro.draft).toBe(false)
  })

  it('preserves unknown fields we may add manually (pin, line)', () => {
    const hugo = {
      title: 'Test',
      date: '2025-10-08',
      pin: 99,
      line: 'kant',
    }
    const astro = transformFrontmatter(hugo)
    expect(astro.pin).toBe(99)
    expect(astro.line).toBe('kant')
  })
})
```

Create `scripts/migrate/transform.ts` as empty placeholder:

```typescript
export function transformFrontmatter(hugo: any): any {
  throw new Error('not implemented')
}
```

**Step 3: Run test to confirm failure**

Run: `pnpm test scripts/migrate/transform.test.ts`
Expected: All 4 tests FAIL with "not implemented".

**Step 4: Commit failing test**

```bash
git add scripts/migrate/
git commit -m "test(migrate): add failing tests for frontmatter transform"
```

---

### Task 3.2: Implement minimal transform to pass tests

**Files:**
- Modify: `scripts/migrate/transform.ts`

**Step 1: Implement**

```typescript
const HUGO_ONLY_FIELDS = new Set([
  'weight', 'showToc', 'TocOpen', 'categories', 'author', 'lastmod'
])

export function transformFrontmatter(hugo: Record<string, any>): Record<string, any> {
  const astro: Record<string, any> = {}

  // title: passthrough
  if ('title' in hugo) astro.title = hugo.title

  // date → published
  if ('date' in hugo) astro.published = hugo.date

  // lastmod → updated (only if present and different from date)
  if ('lastmod' in hugo) astro.updated = hugo.lastmod

  // summary → description
  if ('summary' in hugo) astro.description = hugo.summary

  // tags: passthrough
  if ('tags' in hugo) astro.tags = hugo.tags

  // draft: default false
  astro.draft = hugo.draft ?? false

  // Preserve manually-added Astro fields (pin, line, fontStyle, lang)
  for (const key of ['pin', 'line', 'fontStyle', 'lang', 'standalone']) {
    if (key in hugo) astro[key] = hugo[key]
  }

  return astro
}
```

**Step 2: Run tests to confirm pass**

Run: `pnpm test scripts/migrate/transform.test.ts`
Expected: All 4 tests PASS.

**Step 3: Commit**

```bash
git add scripts/migrate/transform.ts
git commit -m "feat(migrate): implement Hugo→Astro frontmatter transform"
```

---

### Task 3.3: Write the file migration driver

**Files:**
- Create: `scripts/migrate/migrate.ts`
- Create: `scripts/migrate/migrate.test.ts` (optional smoke test)

**Step 1: Implement driver**

```typescript
import { readFileSync, writeFileSync, readdirSync, mkdirSync, existsSync } from 'node:fs'
import { join, basename } from 'node:path'
import matter from 'gray-matter'
import { transformFrontmatter } from './transform'

// Paths — adjust if Hugo source has been archived elsewhere
const HUGO_SOURCE = 'substack_export/posts' // or wherever original .md lives
const ASTRO_DEST_EN = 'src/content/posts'
const ASTRO_DEST_ZH = 'src/content/posts' // same collection, distinguished by lang field

function migrateFile(srcPath: string) {
  const raw = readFileSync(srcPath, 'utf-8')
  const { data, content } = matter(raw)
  const lang = srcPath.endsWith('.zh.md') ? 'zh' : 'en'
  const newFrontmatter = { ...transformFrontmatter(data), lang }
  const rebuilt = matter.stringify(content, newFrontmatter)

  const fname = basename(srcPath)
  const dest = join(ASTRO_DEST_EN, fname)
  writeFileSync(dest, rebuilt, 'utf-8')
  console.log(`migrated: ${srcPath} → ${dest}`)
}

function main() {
  // Hugo content was removed in Task 1.2; if user wants to migrate,
  // they must first restore content/posts/ from git history:
  //   git show main:content/posts/<slug>.en.md > /tmp/<slug>.en.md
  // Or cleaner: check out content/posts/ from main branch into a scratch dir.
  const source = process.argv[2] ?? HUGO_SOURCE
  if (!existsSync(source)) {
    console.error(`Source not found: ${source}`)
    process.exit(1)
  }
  if (!existsSync(ASTRO_DEST_EN)) {
    mkdirSync(ASTRO_DEST_EN, { recursive: true })
  }

  const files = readdirSync(source).filter(f => f.endsWith('.md'))
  for (const f of files) {
    migrateFile(join(source, f))
  }
  console.log(`Done: ${files.length} files migrated`)
}

main()
```

**Step 2: Install gray-matter**

```bash
pnpm add -D gray-matter
```

**Step 3: Prepare Hugo source**

The Hugo `content/posts/` was deleted in Task 1.2. Restore it to a scratch dir for migration:

```bash
mkdir -p /tmp/hugo-posts
git show main:content/posts 2>/dev/null || \
  git --git-dir=../FeiThink/.git worktree add /tmp/hugo-source main
# Alternatively, just checkout the files from main:
git checkout main -- content/posts/
# (this adds them back temporarily; we'll delete again after migration)
```

**Step 4: Dry-run on one file first**

```bash
pnpm tsx scripts/migrate/migrate.ts content/posts
```

Expected: Script processes 96 files, outputs to `src/content/posts/`. Inspect 2-3 output files manually — check frontmatter looks right.

**Step 5: If output looks right, commit migration**

```bash
git add src/content/posts/ scripts/migrate/migrate.ts package.json pnpm-lock.yaml
git commit -m "feat(content): migrate 48 bilingual Hugo posts to Astro collection"
```

**Step 6: Remove Hugo source again**

```bash
git rm -rf content/posts/
git commit -m "chore: remove Hugo content directory (migrated to src/content)"
```

---

### Task 3.4: Verify Astro builds with migrated content

**Step 1: Run dev server**

```bash
pnpm dev
```

**Step 2: Visit `/posts/` (or wherever retypeset lists posts)**

Expected: 48 English posts appear (retypeset will filter by lang). If build errors, inspect schema mismatch — likely some field the retypeset schema requires but transform didn't set. Add to transform, re-run migration.

**Step 3: Fix any schema errors iteratively**

Common issues:
- Missing `description` for some posts → backfill with first 120 chars of body
- Invalid date format → normalize to ISO 8601 in transform
- Required `lang` missing on some posts → default to `en` based on filename suffix

Each fix = add a test in `transform.test.ts`, make it pass, re-run migration.

**Step 4: Commit any fixes**

```bash
git add -A
git commit -m "fix(migrate): address <specific schema issue>"
```

---

## Phase 4: Content Schema Extension & Curation

### Task 4.1: Extend content collection schema with `line` and `standalone`

**Files:**
- Modify: `src/content/config.ts` (or `src/content.config.ts`)

**Step 1: Inspect current schema**

```bash
cat src/content/config.ts
```

**Step 2: Add optional fields**

Add to the posts schema:

```typescript
line: z.enum(['kant', 'dostoevsky-and-literature', 'existence-and-self', 'moral-life']).optional(),
standalone: z.boolean().optional(),
```

Keep all existing fields from retypeset (pin, published, etc.).

**Step 3: Run build to verify schema still validates existing content**

```bash
pnpm build
```

Expected: Build succeeds. If some essays have unexpected fields causing validation errors, fix them manually or in a follow-up migration pass.

**Step 4: Commit**

```bash
git add src/content/config.ts
git commit -m "feat(schema): add line and standalone fields"
```

---

### Task 4.2: Assign 20 essays to their 4 lines

**Rationale:** 5 essays per line × 4 lines. Final selection below is the design-doc candidate pool; adjust after rereading if needed during execution.

**Step 1: Tag Kant line (5 essays)**

Edit frontmatter of these `.en.md` files under `src/content/posts/` to add `line: kant`:

- `132322761-groundwork-of-the-metaphysics-of-morals-i.en.md`
- `136922186-groundwork-of-the-metaphysics-of-morals-ii.en.md`
- `149999960-why-we-read-kant.en.md`
- `the-dignity-of-man.en.md`
- `137280827-what-is-morality.en.md`

**Step 2: Tag Dostoevsky & Literature line (5)**

Add `line: dostoevsky-and-literature`:

- `167521111-rereading-the-brothers-karamazov.en.md`
- `149286461-reading-notes-on-the-idiot-christ-like-love.en.md`
- `167520908-humiliated-and-insulted.en.md`
- `137573845-vagabond-and-the-sublime.en.md`
- `153473895-starting-from-one-hundred-years-of-solitude.en.md`

**Step 3: Tag Existence & Self line (5)**

Add `line: existence-and-self`:

- `143075712-essence-of-existential-psychotherapy.en.md`
- `155013311-subjectivity-how-to-become-the-protagonist-of-your-own-life.en.md`
- `155013391-reason-and-emotion.en.md`
- `149286325-wandering-and-belonging.en.md`
- `140429780-elements-of-happiness-for-intjs.en.md`

**Step 4: Tag Moral Life & Public line (5)**

Add `line: moral-life`:

- `137281163-on-being-a-person-of-integrity.en.md`
- `139089803-do-not-lie.en.md`
- `150375922-why-discriminating-belittles-you.en.md`
- `137281107-on-human-nature-what-the-white-paper-protests-taught-me.en.md`
- `149437568-luo-xiang-a-light-flickering-against-the-wind.en.md`

**Step 5: Verify build**

```bash
pnpm build
```

Expected: No schema errors.

**Step 6: Commit**

```bash
git add src/content/posts/
git commit -m "feat(curation): tag 20 essays with line assignment"
```

---

### Task 4.3: Mark 5 standalone gems

**Step 1: Add `standalone: true` to these `.en.md` files**

- `159302102-ikiru.en.md`
- `172314779-the-scale-of-time.en.md`
- `173845261-dumbledores-woolen-socks.en.md`
- `202512230001-let-there-be-light.en.md`
- `perfect-friendship-and-bitter-merit.en.md`

**Step 2: Commit**

```bash
git add src/content/posts/
git commit -m "feat(curation): mark 5 standalone gems"
```

---

### Task 4.4: Pick 3 pinned essays for homepage

**Step 1: Choose 3 essays to represent the site's identity (design §5)**

Candidate logic: one from Kant line, one from Dostoevsky/literature line, one standalone gem. Tentative:

- `149999960-why-we-read-kant.en.md` → `pin: 99`
- `167521111-rereading-the-brothers-karamazov.en.md` → `pin: 98`
- `159302102-ikiru.en.md` → `pin: 97`

**Step 2: Add `pin` field to those 3 `.en.md` files**

**Step 3: Verify build**

```bash
pnpm build
```

**Step 4: Commit**

```bash
git add src/content/posts/
git commit -m "feat(curation): pin 3 homepage essays"
```

---

### Task 4.5: Mark 23 non-curated essays as draft

**Step 1: Identify non-curated essays**

Non-curated = not in lines (Tasks 4.2), not standalone (4.3), not pinned (4.4). That's 48 - 25 = 23 essays.

**Step 2: Add `draft: true` to their `.en.md` and `.zh.md` frontmatter**

Rationale: Astro with `draft: true` excludes from production build. These remain in the repo as archive but don't appear on the live site.

**Step 3: Verify build excludes drafts**

```bash
pnpm build
```

Expected: Generated `dist/` has 25 essay pages (not 48). Verify by counting HTML files under `dist/posts/`.

**Step 4: Commit**

```bash
git add src/content/posts/
git commit -m "feat(curation): mark 23 non-curated essays as draft"
```

---

### Task 4.6: Keep 25 Chinese essays for `/zh/` archive

**Step 1: Of the 25 curated English essays, their paired `.zh.md` stays published**

All `.zh.md` counterparts of the 25 curated `.en.md` files should have `draft: false` (default).

**Step 2: The 23 non-curated `.zh.md` files also get `draft: true` (from step 4.5)**

Already done if the migration script propagated.

**Step 3: Verify `/zh/posts/` shows ~25 posts in build**

```bash
pnpm build
ls dist/zh/posts/ | wc -l
```

Expected: ~25.

**Step 4: Commit**

```bash
git add src/content/posts/
git commit -m "feat(curation): align Chinese archive with English curation"
```

---

## Phase 5: Custom Layouts

### Task 5.1: Create line metadata file

**Files:**
- Create: `src/data/lines.ts`

**Step 1: Write line data**

```typescript
export type Line = {
  slug: 'kant' | 'dostoevsky-and-literature' | 'existence-and-self' | 'moral-life'
  title: string
  tagline: string         // one-liner for card on /essays/
  intro: string           // longer paragraph for line page (fill in Phase 6)
  readingOrder: string[]  // slugs of essays in recommended reading order
}

export const LINES: Line[] = [
  {
    slug: 'kant',
    title: 'Kant',
    tagline: 'Moral law, rational freedom, and why duty matters.',
    intro: 'PLACEHOLDER — fill in Phase 6.',
    readingOrder: [
      '149999960-why-we-read-kant',
      '132322761-groundwork-of-the-metaphysics-of-morals-i',
      '136922186-groundwork-of-the-metaphysics-of-morals-ii',
      '137280827-what-is-morality',
      'the-dignity-of-man',
    ],
  },
  {
    slug: 'dostoevsky-and-literature',
    title: 'Dostoevsky & Literature',
    tagline: 'Entering moral philosophy through the novel.',
    intro: 'PLACEHOLDER — fill in Phase 6.',
    readingOrder: [
      '167521111-rereading-the-brothers-karamazov',
      '149286461-reading-notes-on-the-idiot-christ-like-love',
      '167520908-humiliated-and-insulted',
      '137573845-vagabond-and-the-sublime',
      '153473895-starting-from-one-hundred-years-of-solitude',
    ],
  },
  {
    slug: 'existence-and-self',
    title: 'Existence & Self',
    tagline: 'On authenticity, subjectivity, and the life worth living.',
    intro: 'PLACEHOLDER — fill in Phase 6.',
    readingOrder: [
      '143075712-essence-of-existential-psychotherapy',
      '155013311-subjectivity-how-to-become-the-protagonist-of-your-own-life',
      '155013391-reason-and-emotion',
      '149286325-wandering-and-belonging',
      '140429780-elements-of-happiness-for-intjs',
    ],
  },
  {
    slug: 'moral-life',
    title: 'Moral Life & Public Sphere',
    tagline: 'Integrity, honesty, and courage under pressure.',
    intro: 'PLACEHOLDER — fill in Phase 6.',
    readingOrder: [
      '137281163-on-being-a-person-of-integrity',
      '139089803-do-not-lie',
      '150375922-why-discriminating-belittles-you',
      '137281107-on-human-nature-what-the-white-paper-protests-taught-me',
      '149437568-luo-xiang-a-light-flickering-against-the-wind',
    ],
  },
]
```

**Step 2: Commit**

```bash
git add src/data/lines.ts
git commit -m "feat(lines): add reading line metadata"
```

---

### Task 5.2: Custom homepage `/` (Hero + 3 pinned + 4 lines + footer)

**Files:**
- Modify or create: `src/pages/index.astro` (root English index)

**Step 1: Determine target file path**

From Task 2.1, English index should be at root. Retypeset's original may be `src/pages/[...lang]/index.astro` — either override at `src/pages/index.astro` (wins over dynamic) or edit the dynamic with conditional. Pick whichever Astro resolves to `/` cleanly.

**Step 2: Write index**

```astro
---
import Layout from '../layouts/BaseLayout.astro'  // adjust import to actual
import { getCollection } from 'astro:content'
import { LINES } from '../data/lines'

const posts = await getCollection('posts', ({ data }) =>
  data.lang === 'en' && !data.draft && data.pin !== undefined
)
const pinned = posts
  .sort((a, b) => (b.data.pin ?? 0) - (a.data.pin ?? 0))
  .slice(0, 3)
---

<Layout title="FeiThink" description="Essays on moral philosophy, from a reader of Kant.">
  <section class="hero">
    <h1>PLACEHOLDER Hero Line (finalize Phase 6)</h1>
    <p class="subtitle">
      Longform essays on Kant, Dostoevsky, and the moral life. Curated from years of writing at
      <a href="https://feihuang.substack.com">FeiThink on Substack</a>. New work goes there first.
    </p>
  </section>

  <section class="pinned">
    <h2 class="section-label">Start here</h2>
    <ul class="pinned-list">
      {pinned.map(p => (
        <li>
          <a href={`/posts/${p.slug}/`}>
            <h3>{p.data.title}</h3>
            <p class="hook">{p.data.description}</p>
            <span class="read-more">Read →</span>
          </a>
        </li>
      ))}
    </ul>
  </section>

  <section class="lines">
    <h2 class="section-label">By reading line</h2>
    <ul class="lines-list">
      {LINES.map(line => (
        <li>
          <a href={`/essays/lines/${line.slug}/`}>
            <h3>{line.title}</h3>
            <p>{line.tagline}</p>
          </a>
        </li>
      ))}
    </ul>
  </section>

  <footer class="identity">
    <p class="bio">
      Fei Huang. Based in Amsterdam. Writes on moral philosophy; works in AI.
    </p>
    <p class="cta">
      New essays land first on <a href="https://feihuang.substack.com">Substack</a>.
    </p>
    <ul class="social">
      <li><a href="https://github.com/huangf06">GitHub</a></li>
      <li><a href="https://www.linkedin.com/in/huangf06/">LinkedIn</a></li>
      <li><a href="https://feihuang.substack.com">Substack</a></li>
      <li><a href="/rss.xml">RSS</a></li>
      <li><a href="mailto:huangf06@gmail.com">Email</a></li>
    </ul>
  </footer>
</Layout>

<style>
  /* Match retypeset's typographic scale. No decorative gradients, no button CTAs.
     Keep all sections single-column, generous vertical rhythm.
     Pinned list: 3 items, each a full-width card with hairline border-top only.
     Lines list: 4 items, small text links with tagline below. */
  .hero h1 { font-size: 2rem; font-weight: 600; margin-bottom: 1rem; }
  .subtitle { font-size: 1.05rem; line-height: 1.6; color: var(--fg-subtle); }
  .section-label { font-size: 0.875rem; text-transform: uppercase; letter-spacing: 0.1em; color: var(--fg-subtle); margin-top: 3rem; }
  .pinned-list li + li, .lines-list li + li { border-top: 1px solid var(--border-subtle); padding-top: 1.5rem; margin-top: 1.5rem; }
  .cta { font-size: 0.95rem; }
  .social { list-style: none; padding: 0; display: flex; gap: 1.5rem; font-size: 0.9rem; }
</style>
```

Adjust class names/CSS vars to match retypeset's existing design tokens (inspect its base layout CSS).

**Step 3: Run dev server, check `/`**

```bash
pnpm dev
```

Expected: Homepage shows Hero placeholder + 3 pinned essays (if tags applied correctly) + 4 line entries + footer.

**Step 4: Commit**

```bash
git add src/pages/index.astro
git commit -m "feat(home): custom homepage layout per design §5"
```

---

### Task 5.3: Line page `src/pages/essays/lines/[line].astro`

**Files:**
- Create: `src/pages/essays/lines/[line].astro`

**Step 1: Write dynamic route**

```astro
---
import Layout from '../../../layouts/BaseLayout.astro'
import { getCollection, getEntry } from 'astro:content'
import { LINES } from '../../../data/lines'

export async function getStaticPaths() {
  return LINES.map(line => ({ params: { line: line.slug }, props: { line } }))
}

const { line } = Astro.props

// Fetch posts in reading order
const posts = await Promise.all(
  line.readingOrder.map(slug =>
    getEntry('posts', slug) // or wherever slug resolves
  )
)
---

<Layout title={`${line.title} — FeiThink`} description={line.tagline}>
  <article class="line">
    <h1>{line.title}</h1>
    <p class="tagline">{line.tagline}</p>
    <section class="intro">
      <p>{line.intro}</p>
    </section>
    <ol class="reading">
      {posts.filter(Boolean).map((p, i) => (
        <li>
          <span class="n">{i + 1}</span>
          <a href={`/posts/${p.slug}/`}>
            <h3>{p.data.title}</h3>
            <p>{p.data.description}</p>
          </a>
        </li>
      ))}
    </ol>
    <section class="further">
      <h2>Further reading</h2>
      <p>
        More at <a href="https://feihuang.substack.com">Substack</a>.
      </p>
    </section>
  </article>
</Layout>
```

**Step 2: Run dev server, test each line**

Visit `/essays/lines/kant/`, `/essays/lines/dostoevsky-and-literature/`, etc.

**Step 3: Commit**

```bash
git add src/pages/essays/lines/
git commit -m "feat(lines): line page dynamic route"
```

---

### Task 5.4: `/essays/` index with lines on top + chronological below

**Files:**
- Create or modify: `src/pages/essays/index.astro`

**Step 1: Write page**

```astro
---
import Layout from '../../layouts/BaseLayout.astro'
import { getCollection } from 'astro:content'
import { LINES } from '../../data/lines'

const all = await getCollection('posts', ({ data }) =>
  data.lang === 'en' && !data.draft
)
const chronological = all.sort((a, b) =>
  new Date(b.data.published).getTime() - new Date(a.data.published).getTime()
)
---

<Layout title="Essays — FeiThink" description="All curated essays.">
  <section class="lines-overview">
    <h2>Reading lines</h2>
    <ul>
      {LINES.map(line => (
        <li>
          <a href={`/essays/lines/${line.slug}/`}>
            <h3>{line.title}</h3>
            <p>{line.tagline}</p>
          </a>
        </li>
      ))}
    </ul>
  </section>

  <section class="archive">
    <h2>All essays</h2>
    <ul class="post-list">
      {chronological.map(p => (
        <li>
          <time>{new Date(p.data.published).toISOString().slice(0,10)}</time>
          <a href={`/posts/${p.slug}/`}>{p.data.title}</a>
          <p>{p.data.description}</p>
        </li>
      ))}
    </ul>
  </section>
</Layout>
```

**Step 2: Test**

Visit `/essays/` — top should show 4 lines, below should show 25 posts chronologically.

**Step 3: Commit**

```bash
git add src/pages/essays/index.astro
git commit -m "feat(essays): essays index with lines + chronological archive"
```

---

### Task 5.5: `/work/` page

**Files:**
- Create: `src/pages/work.astro`

**Step 1: Write page**

```astro
---
import Layout from '../layouts/BaseLayout.astro'
---

<Layout title="Work — FeiThink" description="Academic work, projects, credentials.">
  <article class="work">
    <h1>Work</h1>

    <section>
      <h2>Academic</h2>
      <ul>
        <li>
          <strong>M.Sc. Artificial Intelligence</strong>, Vrije Universiteit Amsterdam (2025).
          Thesis: <em>PLACEHOLDER: Uncertainty Quantification in Deep Reinforcement Learning</em>.
        </li>
      </ul>
    </section>

    <section>
      <h2>Projects</h2>
      <ul>
        <li>PLACEHOLDER — fill Phase 6: public repos, small demos.</li>
      </ul>
    </section>

    <section>
      <h2>Credentials</h2>
      <ul>
        <li>Databricks Certified Data Engineer Professional.</li>
      </ul>
    </section>

    <section>
      <h2>Experience</h2>
      <p>
        Henan Energy Group → Ele.me → BQ Investment → GLP Technology → Independent Quant → VU Amsterdam M.Sc. AI. Full timeline on <a href="https://www.linkedin.com/in/huangf06/">LinkedIn</a>.
      </p>
    </section>
  </article>
</Layout>
```

**Step 2: Test**

**Step 3: Commit**

```bash
git add src/pages/work.astro
git commit -m "feat(work): work page skeleton"
```

---

### Task 5.6: Rewrite `/about/`

**Files:**
- Modify: existing about source (likely `src/pages/about.astro` or `src/content/pages/about.md`)

**Step 1: Locate and replace**

Structure per design §2.2:

```markdown
# About

## Who I am

Fei Huang. Writes on moral philosophy — primarily Kant and Dostoevsky. Works in AI. Lives in Amsterdam.

## What I write about

PLACEHOLDER (fill Phase 6) — four short paragraphs, one per reading line, each linking to its line page.

## Professional

M.Sc. AI, Vrije Universiteit Amsterdam (2025). Databricks Certified Data Engineer Professional. Ten years in data science and machine learning; seven in quantitative trading.

## Why English

Chinese by birth, but this site is for an international audience. Writing in Chinese continues on Substack.

## Contact

- Email: huangf06@gmail.com
- GitHub: [huangf06](https://github.com/huangf06)
- LinkedIn: [Fei Huang](https://www.linkedin.com/in/huangf06/)
- Substack: [feihuang.substack.com](https://feihuang.substack.com)
```

**Step 2: Commit**

```bash
git add <about-path>
git commit -m "feat(about): rewrite per design §2.2"
```

---

### Task 5.7: Menu configuration — 4 items

**Files:**
- Modify: retypeset's menu config (likely `src/config.ts` or `src/data/menu.ts`)

**Step 1: Update menu to: Home · Essays · Work · About**

Remove any retypeset defaults (Tags, Categories, Archive, etc. unless they map cleanly).

**Step 2: Test navigation**

**Step 3: Commit**

```bash
git add <menu-config-path>
git commit -m "feat(nav): 4-item menu (Home/Essays/Work/About)"
```

---

## Phase 6: Writing Content (User Task)

These tasks produce text, not code. User writes; Claude can assist with drafts.

### Task 6.1: Finalize Hero positioning line + subtitle

**Deliverable:** Update `src/pages/index.astro` with final Hero text.

**Process:**
1. Brainstorm 3–5 candidates for the one-line Hero (per design §2.1).
2. User picks one or synthesizes.
3. Write 2–3 sentence subtitle.
4. Update `index.astro`.
5. Commit: `content: finalize hero positioning line`.

---

### Task 6.2: Rewrite About page content

**Deliverable:** Final About page text replacing PLACEHOLDER in Task 5.6.

**Process:**
1. Write all sections per design §2.2 structure.
2. No "wanderer", no "seeker", no closing literary quote.
3. Commit: `content: finalize about page`.

---

### Task 6.3: Write 4 line introductions

**Deliverable:** Replace `intro: 'PLACEHOLDER ...'` in `src/data/lines.ts` with real text.

**Process:**
1. Each intro: ~150 words. Say why this line exists, what reading it gets you, the recommended starting point.
2. Edit `src/data/lines.ts`.
3. Commit: `content: write line introductions`.

---

### Task 6.4: Finalize 25 essay selection

**Deliverable:** Reread each of the 25 selected essays on Substack. Confirm selections; swap any that don't hold up; adjust `line` / `standalone` / `pin` tags in content files.

**Process:**
1. Read through Substack archive.
2. For any swap, update frontmatter of in/out essays.
3. Commit: `content: finalize essay curation`.

---

### Task 6.5: Fill in Work page content

**Deliverable:** Replace PLACEHOLDER in `src/pages/work.astro`.

**Process:**
1. Write real thesis abstract (1–2 sentences).
2. List 2–3 public projects (GitHub repos or demos). If nothing suitable public, leave Projects section minimal or drop.
3. Commit: `content: finalize work page`.

---

## Phase 7: Deployment

### Task 7.1: Pre-deploy build verification

**Step 1: Full production build**

```bash
pnpm build
```

Expected: `dist/` generated with no errors. Manually spot-check 2–3 HTML files.

**Step 2: Preview locally**

```bash
pnpm preview
```

Visit localhost — verify homepage, /essays/, /essays/lines/kant/, /work/, /about/, /zh/ all render.

**Step 3: Commit any last fixes**

---

### Task 7.2: Push branch to GitHub

**Step 1: Push**

```bash
git push -u origin redesign-astro
```

**Step 2: Verify on GitHub**

Visit `https://github.com/huangf06/FeiThink/tree/redesign-astro` — confirm all files present.

---

### Task 7.3: Create Cloudflare Pages project

**NOTE: This is a shared-state action. Ask user to perform in Cloudflare dashboard; Claude cannot reach CF API without credentials.**

**Instructions for user:**
1. Go to `https://dash.cloudflare.com/` → Workers & Pages → Create → Pages → Connect to Git.
2. Authorize GitHub, select `huangf06/FeiThink`.
3. Production branch: `main` (not yet — we'll merge later; for now, deploy from `redesign-astro` as preview).
4. Build settings:
   - Framework preset: Astro
   - Build command: `pnpm build`
   - Build output: `dist`
   - Root directory: `/` (repo root)
   - Environment variable: `NODE_VERSION=20` (or 22, whichever matches Task 0.2)
5. Save and deploy preview.

**Step 2: Verify preview URL works**

Expected: `*.pages.dev` preview URL shows the site.

---

### Task 7.4: Attach custom domain `feithink.org`

**NOTE: DNS change — ask user.**

**Instructions for user:**
1. In the Cloudflare Pages project → Custom domains → Set up a custom domain → `feithink.org`.
2. Cloudflare auto-detects the DNS since the domain is already in Cloudflare Registrar. Approve the DNS records.
3. Add `www.feithink.org` as a second custom domain if desired (or 301 redirect in a later step).
4. Wait ~1 min for propagation.

**Step 2: Verify HTTPS works**

Visit `https://feithink.org/` — should serve the Astro site.

---

### Task 7.5: Add `_redirects` for old GitHub Pages URLs

**Files:**
- Create: `public/_redirects`

**Step 1: Inspect Substack export to identify live URLs that might be linked externally**

Most likely external links point to:
- `huangf06.github.io/GitStack/posts/<slug>/`
- `huangf06.github.io/GitStack/zh/posts/<slug>/`

The new URLs:
- `feithink.org/posts/<slug>/`
- `feithink.org/zh/posts/<slug>/`

**Step 2: Write `_redirects`**

Cloudflare Pages `_redirects` syntax (Netlify-compatible):

```
# Old GitHub Pages URLs → new site
/GitStack/*            https://feithink.org/:splat  301
/GitStack/posts/*      https://feithink.org/posts/:splat  301
/GitStack/zh/posts/*   https://feithink.org/zh/posts/:splat  301
```

(The old GitHub Pages URLs are on `huangf06.github.io/GitStack/` — these redirects will only take effect if `huangf06.github.io/GitStack/` also ends up served by CF Pages, which it won't. Instead, we'll disable GitHub Pages in Task 8.2 — external links to the old URL will 404 cleanly rather than redirect. If external-link preservation matters, configure GitHub Pages itself to redirect via a `_config.yml` meta refresh as a separate step.)

**Step 3: Commit and deploy**

```bash
git add public/_redirects
git commit -m "feat(redirects): add placeholder redirects for old URLs"
git push
```

---

## Phase 8: Cutover & Cleanup

### Task 8.1: Merge redesign-astro to main

**ASK USER: Confirm ready to cut over to production.**

**Step 1: From the main worktree (not the astro worktree)**

```bash
cd ../FeiThink  # original main worktree
git checkout main
git pull
```

**Step 2: Merge**

```bash
git merge redesign-astro --no-ff -m "feat: migrate feithink.org from Hugo to Astro+retypeset"
```

Resolve any conflicts (shouldn't be any since redesign-astro deleted all Hugo files and added Astro files from a clean state).

**Step 3: Push main**

```bash
git push origin main
```

**Step 4: Cloudflare Pages auto-deploys from main (if Task 7.3 set production branch to main)**

Wait for deploy, verify `feithink.org` shows the Astro site.

---

### Task 8.2: Disable old GitHub Pages deployment

**NOTE: Ask user — this is a production change.**

**Instructions for user:**
1. Go to `https://github.com/huangf06/FeiThink/settings/pages`
2. Under "Build and deployment", set Source to "None" (disable Pages).
3. Confirm.

Result: `huangf06.github.io/GitStack/` will 404. Acceptable per design — external links to old URLs are rare, and `feithink.org` is now the canonical home.

---

### Task 8.3: Remove the worktree

**Step 1: From anywhere outside the worktree**

```bash
cd ~/github/FeiThink
git worktree remove ../FeiThink-astro
# Branch redesign-astro can be deleted or kept for history:
git branch -D redesign-astro  # optional, after confirming merge
git push origin --delete redesign-astro  # optional
```

---

### Task 8.4: Smoke test live site

**Step 1: Visit and verify each page on `https://feithink.org/`**

- `/` — Hero + 3 pinned + 4 lines + footer
- `/essays/` — lines top + 25-post archive below
- `/essays/lines/kant/` — Kant line
- `/essays/lines/dostoevsky-and-literature/`
- `/essays/lines/existence-and-self/`
- `/essays/lines/moral-life/`
- `/work/` — academic, projects, credentials
- `/about/` — rewritten bio
- `/zh/` — Chinese home
- Pick 3 random essay URLs and verify they load
- Dark mode toggle works
- RSS feed at `/rss.xml`
- `/404` page looks right

**Step 2: Lighthouse audit**

Run Chrome DevTools Lighthouse on `/` and `/posts/<sample>/`:
- Performance ≥ 95
- Accessibility ≥ 95
- Best Practices ≥ 95
- SEO ≥ 95

**Step 3: Check mobile viewport**

Resize browser to 375px width. Verify layout holds.

**Step 4: Record results in session log**

---

### Task 8.5: Update memory — mark migration complete

**Files:**
- Modify: `~/.claude/projects/C--Users-huang-github-FeiThink/memory/project_blog_redesign.md`

**Step 1: Update memory**

Change status from "brainstorming done, implementation pending" to "live at feithink.org on Astro+retypeset as of <date>".

**Step 2: No commit needed — memory is outside repo.**

---

## Rollback Plan

If anything goes wrong after cutover:

1. Revert the merge commit:
   ```bash
   git revert -m 1 <merge-sha>
   git push origin main
   ```
2. Cloudflare Pages redeploys. But `dist/` won't exist in reverted main (it was the Hugo state) — **this won't work cleanly if main no longer has Hugo setup either**.
3. Safer: before Task 8.1 merge, tag main's last Hugo commit: `git tag hugo-final main` and push the tag. Rollback = checkout that tag, force push to main.

**Pre-merge safety step**: In Task 8.1, before merging, run:

```bash
git tag hugo-final-pre-astro main
git push origin hugo-final-pre-astro
```

This preserves an escape hatch.

---

## Appendix: Risk Register

| Risk | Mitigation |
|---|---|
| retypeset structure differs from what's assumed here | Task 1.1 recon step reads actual repo before committing decisions |
| Migration script schema mismatch after 48 files processed | TDD (Phase 3) + iterative schema fixes in Task 3.4 |
| Custom homepage fights with retypeset's `[...lang]` routing | Task 2.1 handles this; fallback to static pages if dynamic routing is sticky |
| Cloudflare Pages build fails on Windows-specific line endings | `.gitattributes` should already normalize; set `* text=auto eol=lf` if issues |
| External old-URL 404s cause traffic loss | Design accepts this as acceptable (most old URLs are low-traffic) |
| DNS propagation delay | Cloudflare Registrar + CF Pages is same-vendor, near-instant |

---

## Plan Execution Summary

- **Phases 0–5**: Pure engineering, can be executed autonomously by a subagent with user check-ins at destructive steps (Task 1.2 deletion, Task 8.1 merge, Task 8.2 GitHub Pages disable).
- **Phase 6**: Writing tasks — user-driven, Claude assists with drafts.
- **Phases 7–8**: Deployment — user must perform Cloudflare dashboard actions; Claude drives file-level work.
- **Commits**: 25+ small commits across the plan. Each task ends with a commit.
- **Estimated total**: 4–5 half-days engineering + 2 days writing (matches design §8).
