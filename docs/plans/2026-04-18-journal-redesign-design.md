# FeiThink Journal Redesign — Design Document

Date: 2026-04-18
Status: Approved
Supersedes parts of `docs/plans/2026-04-17-hugo-redesign-design.md`

## Context

The Hugo→Astro migration (see `2026-04-18-astro-migration-implementation.md`) built a curated philosophy column: 25 English essays organized into 4 reading lines, 3 pinned posts, "Essays on moral philosophy" tagline hammered across header/hero/lines.

After seeing it live, the owner reframed the project: the site should stop repeatedly asserting intellectual depth. He wants to show himself more fully — "a three-dimensional place that records the moments worth remembering." Not a philosophy column. A place on the internet that is his.

This document redesigns the site around that reframe. It preserves Astro + retypeset + Cloudflare Pages; it preserves the 25 + 48 existing essays; it changes what the site *is* and how it's organized.

## What Supersedes What

From the 2026-04-17 design, these locked decisions are revised:

| # | Old | New |
|---|-----|-----|
| 1 | Brand imprint = "Kant reader" | Brand imprint = "a person living and thinking" — expressed by content mix, not by repeating the label |
| 3 | Essays page leads with 4 curation lines | Lines demoted to tag filter on Essays page |
| 4 | ~25 curated essays, closed set | Essays grow over time; no cap |
| 5 | Home: Hero → 3 pinned → 4 lines → identity footer | Home: minimal hero → 3 pinned essays → Latest moments (2) → Recent essays (5) |

These stay:

- Decision 2 (4 menu items) — revised to 5 below
- Decision 6 (English main, Chinese footer entry)
- Decision 7 (Astro + retypeset)

## Identity

FeiThink is Fei Huang's place on the internet — a continuous record of thinking and living. Not a philosophy column. Not a blog. A home.

Tagline (provisional, final text owner-written): `"Thinking and living — mostly in prose, occasionally in photos."`

The "three-dimensional impression" doesn't come from a louder hero or a longer bio. It comes from the home page surfacing two different life frequencies simultaneously: intellectual output (essays) and life peaks (moments).

## Information Architecture

Nav expands from 4 to 5 items:

**Home · Essays · Moments · Work · About**

- **Home** — hero + pinned essays + latest moments + recent essays
- **Essays** — essay listing with 4 reading-line tag bar on top
- **Moments** — new; memory wall (see §Moments Page)
- **Work** — unchanged
- **About** — unchanged IA; content to be rewritten by owner

Footer preserves the low-key Chinese entry.

## Content Model

One `posts` collection, discriminated by `type`:

```ts
// src/content.config.ts
const posts = defineCollection({
  schema: z.object({
    title: z.string().optional(),    // optional for moment; required for essay
    description: z.string().optional(),
    published: z.date(),
    lang: z.enum(['en', 'zh']),

    // NEW
    type: z.enum(['essay', 'moment']).default('essay'),
    image: z.string().optional(),              // single hero image
    images: z.array(z.string()).optional(),    // moment multi-image
    relatedEssay: z.string().optional(),       // moment can link to essay

    // existing
    line: z.enum([...]).optional(),     // essay only
    pinned: z.boolean().default(false), // essay only
    draft: z.boolean().default(false),
    tags: z.array(z.string()).default([]),
    abbrlink: z.string().optional(),
  }),
})
```

Two types only:

- **essay** — longform. Existing 25 English + 48 Chinese get `type: essay`. Default value so no migration change to frontmatter is strictly needed.
- **moment** — rare life marker (achievements, proud essays published, genuine happiness, belonging). Text + optional 1-to-N images. May link to a related essay.

Notes / photos as a separate type were considered and rejected: owner's honest cadence is sparse, so daily-post patterns would have been dead-on-arrival.

## Home Page Layout

```
┌──────────────────────────────┐
│  FeiThink                     │  ← site title
│  Thinking and living — …      │  ← tagline (new)
├──────────────────────────────┤
│  Pinned essays                │  ← 3 pinned essays (unchanged)
│  [essay card × 3]             │
├──────────────────────────────┤
│  Latest moments   See all →   │  ← latest 2 moments, visually rich
│  [moment card × 2]            │
├──────────────────────────────┤
│  Recent essays    See all →   │  ← latest 5 essays, list view
│  [essay list × 5]             │
└──────────────────────────────┘
```

The `Latest moments` section is the critical new element. Two recent moment cards, each with image (if any) + title + date + short text. Visual weight closer to pinned-essay cards than to essay-list items.

`See all →` links go to `/moments/` and `/essays/` respectively.

Skipped intentionally:
- No mixed-stream timeline (rejected: wouldn't be 立体 with sparse moments)
- No infinite scroll
- No type-filter toggles on home (that's what Essays / Moments pages are for)
- No large hero image (imprint comes from content, not visual shout)

## Moments Page

Not a reverse-chronological feed. A memory wall, grouped by year:

```
Moments
Things I want to remember.

2026
  [moment × N]

2025
  [moment × N]

2024
  [moment × N]
```

Each card: image (if any) + title + date + short text preview (1–2 lines). Clicking opens the full moment page at `/moments/{slug}/`.

No pagination initially (expected total <20 items per year, possibly <50 total ever). If density grows beyond comfortable single-page loading, revisit.

## Essays Page

Kept largely from prior design. Minor changes:

- Top of page shows 4 reading-line tag buttons (Kant, Dostoevsky & Literature, Existence & Self, Moral Life)
- Below: chronological essay list (replaces the previous "lines first, then chronological" two-tier layout)
- Clicking a line tag filters to that line's essays (reuse existing `/essays/lines/{line}/` routes)

Decision deferred (see §Open Items): whether to keep 4 lines or consolidate to 3.

## URL Structure

- Essay: `/posts/{abbrlink}/` (unchanged)
- Moment: `/moments/{slug}/`
- Moment index: `/moments/`
- Line filter: `/essays/lines/{line}/` (unchanged)

For Chinese versions, `/zh/` prefix applies uniformly.

## Bilingual Handling

Unchanged from decision 6. English primary, Chinese low-key footer entry.

Implication for moments: each moment is single-language. English moments appear in `/` home and `/moments/` index. Chinese moments appear in `/zh/` home and `/zh/moments/` index. Not translated piece-by-piece.

Expected content skew: English feed tilts toward essays (less everyday life); Chinese feed tilts toward moments (daily life feels natural in Chinese). This asymmetry is a feature.

## Risks

The original "you won't post daily" risk is no longer a risk — moments are designed to be sparse.

The real risk now:

**Owner under-claims milestones.** Many introspective people feel their achievements "aren't big enough to mark yet" and the Moments page stays at 0–1 entries permanently. The Moments wall's life is not a code problem; it's the owner's willingness to publicly acknowledge his own peaks in real time. This design cannot mitigate that.

Mitigation at design level (all we can do): Moments page text encourages the owner himself — `"Things I want to remember"` — frames the page as self-addressed, not performative. Removes the "is this worth broadcasting" mental tax.

Secondary observation: moments and essays can reinforce each other. When a proud essay is published, a moment can mark the day of writing/finishing (with place, photo, mood, and a link to the essay). Each reinforces the other.

## Division of Labor

**Implemented in code:**
- Schema extension (`type`, `image`, `images`, `relatedEssay`)
- Moments index page (`/moments/`)
- Moment detail page (`/moments/[slug]`)
- Moment card component (home + moments index variants)
- Home page rewrite (new sections)
- Essays page adjustment (tag bar on top, chronological below)
- Navbar: add `Moments` as 3rd item between Essays and Work
- Tagline / config.ts site subtitle updated

**Owner-written content (not implementation):**
- Final tagline text
- About rewrite
- Any seed moments (not required — empty Moments wall is fine for launch)

## Open Items

1. **Reading lines count** — keep 4 (Kant, Dostoevsky & Literature, Existence & Self, Moral Life) or consolidate to 3 / 2? Deferred to implementation-time decision with owner.

2. **Moment slug format** — auto-generated from date + short title, or hand-authored? Defer: default to hand-authored (matches essay `abbrlink` pattern).

3. **Moment detail page layout** — open question whether it should look like an essay page or have a distinct layout (image-forward, less text chrome). Default: lightweight variant of essay page; adjust if it feels wrong when first real moment is posted.

## Related Documents

- Prior design: `docs/plans/2026-04-17-hugo-redesign-design.md` (partially superseded above)
- Astro migration implementation: `docs/plans/2026-04-18-astro-migration-implementation.md` (base architecture, still in force)
- Handoff notes: `docs/plans/2026-04-17-hugo-redesign-handoff.md`

## Next Step

This design is approved by owner (2026-04-18). Next: use the `superpowers:writing-plans` skill to produce an implementation plan `docs/plans/2026-04-18-journal-redesign-implementation.md` broken into bite-sized tasks, then execute via `superpowers:executing-plans`.
