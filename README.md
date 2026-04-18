# FeiThink

Bilingual personal journal of Fei Huang — essays on moral philosophy and life moments.

Live site: [feithink.org](https://feithink.org) · Substack: [feithink.substack.com](https://feithink.substack.com)

Tagline: *Plain living, high thinking.* (Wordsworth, 1802)

## Stack

- [Astro](https://astro.build/) 6.1+ (static)
- [astro-theme-retypeset](https://github.com/radishzzz/astro-theme-retypeset) (vendored)
- [UnoCSS](https://unocss.dev/), MDX, KaTeX, Mermaid
- pnpm 10 · Node ≥ 22.12
- Deployed on Cloudflare Pages, auto-deploys `main`

## Running locally

```bash
pnpm install
pnpm dev        # http://localhost:4321
pnpm build      # production build → dist/
pnpm preview    # serve the built site
pnpm test       # vitest
pnpm lint       # eslint
```

## Content

All writing lives under `src/content/posts/` as paired bilingual markdown files (`{slug}.en.md` + `{slug}.zh.md`). About pages are under `src/content/about/`.

Posts use an `essay | moment` type discriminator and an optional `line` curation tag (`kant`, `dostoevsky-and-literature`, `existence-and-self`, `moral-life`). See `src/content.config.ts` for the full frontmatter schema.

Helper scripts:
- `pnpm migrate` — import Substack/Hugo exports
- `pnpm curate` — apply line/pin/standalone metadata

See [CLAUDE.md](CLAUDE.md) for the full architecture, frontmatter schema, and authoring conventions.

## License

Content (text, translations, personal essays): © Fei Huang. All rights reserved.

Theme code (astro-theme-retypeset) is MIT-licensed — see upstream repo.
