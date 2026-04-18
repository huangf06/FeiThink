# Multi-Platform Publisher — Design Document

Date: 2026-04-18
Status: Approved (via brainstorming session 2026-04-18)
Next step: writing-plans skill in a fresh session → `docs/plans/2026-04-18-multi-platform-publisher-implementation.md`

## Context

Owner writes essays in Markdown locally (Chinese first, English translation later). Currently distribution to non-feithink platforms is fully manual: log into Substack web editor, paste, click publish; same for WeChat 公众号; same for Twitter. The feithink.org side is already automated (git push → Cloudflare Pages build).

Goal: write once in Markdown → one CLI command dispatches to every platform the essay declares, with per-post override control over where it goes.

## Locked Decisions

### 1. Target platforms (real, current)

- **feithink.org** (Astro + Cloudflare Pages) — owner's sovereign home. Already automated via `git push`; a publisher adapter is optional (the git workflow is already fine).
- **Substack** (`feithink.substack.com`) — primary long-form distribution, newsletter.
- **WeChat 公众号** — Chinese-speaking reader surface. Owner holds a **personal (unverified) subscription account**. See decision 5.
- **Twitter/X** — presence + existence; no illusions about growth via automation.
- **LinkedIn** — added in this design. High ROI given owner's EU Data/AI job hunt; official API supports personal-post writes.

Not in scope (explicitly declined): 小红书, 即刻, 微博, Hacker News, Reddit, Medium, Bluesky, Mastodon, Dev.to. May revisit individually later; YAGNI now.

### 2. Publish posture per platform (the crucial per-platform policy)

| Platform | Posture | Rationale |
|---|---|---|
| feithink.org | auto (already via CF Pages) | Owner's own infra; zero risk |
| Substack | **push DRAFT only**, owner clicks publish | No official API. Reverse-engineered session cookie is fragile; a direct-publish misfire sends broken emails to subscribers, irreversible. 10s of manual click buys a last look. |
| WeChat | **MD → WeChat-styled HTML + clipboard copy**, owner pastes in editor | Personal account has no API publish rights; verifying via a Dutch company costs ~600-800 EUR/yr + admin with negative ROI given owner's monthly cadence and stated desire to not grow the Chinese social footprint. Half-auto is the right level. |
| LinkedIn | **auto direct publish** (excerpt + link back) | Official API, stable, short content; errors are cheap to edit. |
| Twitter | **auto direct publish** (excerpt + link; auto-thread if long) | Official API; errors are cheap to edit. Automation buys existence, not influence — understood and accepted. |

### 3. Per-post routing — frontmatter white-list

Every essay file (`<slug>.{zh,en}.md`) declares its destinations explicitly:

```yaml
---
title: 武藏，去种田吧
slug: musashi-go-farm
lang: zh                         # zh | en
date: 2026-02-12
platforms: [feithink, substack, wechat]   # white-list; CLI only dispatches to these
excerpt: |                        # used by twitter/linkedin; auto-extracted from body if absent
  武藏扛着锄头走向田埂时...
status: ready                    # draft | ready | published — CLI refuses non-ready
translation_of: musashi-go-farm  # EN file only; points to ZH source slug for hreflang/canonical
---
```

**Default routing** when `platforms:` is absent:

- `lang: zh` → `[feithink, substack, wechat]`
- `lang: en` → `[feithink, substack, linkedin, twitter]`

Owner can override either direction, per post. Substack takes both languages (existing behavior). LinkedIn and Twitter only receive curated EN pieces (owner decides via frontmatter).

### 4. Content model — one file per language

Owner writes ZH first, EN later (asynchronous). Two independent files share a slug:

```
essays/musashi-go-farm.zh.md       # ZH source, self-contained
essays/musashi-go-farm.en.md       # EN translation, frontmatter has translation_of: musashi-go-farm
```

Each file has its own `platforms:` and its own publish lifecycle. Publishing ZH does not block EN; the EN file can land weeks later.

### 5. WeChat — stay on personal (unverified) account

Owner considered opening a Dutch entity to verify the WeChat account for API access. Rejected:

- Annual cost: ~600-800 EUR (KVK eenmanszaak + bookkeeping + USD 300 WeChat verification fee/yr) + ongoing compliance admin.
- Capability unlocked: only "push to 草稿箱" — owner still taps Send on phone.
- Cadence mismatch: owner posts to WeChat ~1-2×/month. Half-auto (MD → styled HTML + clipboard, paste into editor) costs 30-60s per post, i.e. ~10 min/yr.
- Strategic mismatch: owner is deliberately reducing Chinese social media footprint (CLAUDE.md). Verifying ≈ building infra in the direction he is walking away from.

Keep personal account. Adapter ships the content as paste-ready HTML.

### 6. Trigger — local CLI, no CI

Decided against GitHub Actions. Reasons:

- Solo user — the CI value prop (multi-contributor auditability, reproducibility across machines) does not apply.
- Feedback loop: local CLI returns in ~5s; Actions round-trip is 30-60s.
- Accidental triggers: owner pushes for unrelated reasons (typo fixes, style tweaks). `status: ready` gating mitigates but doesn't remove friction.
- Debugging: terminal scrollback > Actions web UI.

Local CLI with `.env` credentials. Append-only log at `output/publish-log.jsonl` for local audit.

### 7. Twitter honesty

Owner asked whether automation buys Twitter influence. It does not — the platform rewards native content and engagement. Automation buys existence: excerpt + link-back on publish. If owner later decides to invest in Twitter as a growth channel, that is a separate project (manual native writing, threads, reply loops); it is not in scope here.

## Architecture

### Tool layout

Python CLI, lives in the FeiThink repo under `tools/publish/`:

```
tools/publish/
├── publish.py              # CLI entry: `publish <path-to-md> [--dry-run] [--only platform] [--skip platform]`
├── core/
│   ├── post.py             # Post dataclass; frontmatter parser; validation
│   ├── log.py              # jsonl appender → output/publish-log.jsonl
│   ├── render.py           # MD → HTML (platform-agnostic); excerpt extraction fallback
│   └── clipboard.py        # Windows clipboard helper
├── adapters/
│   ├── base.py             # Adapter protocol: publish(post: Post) -> PublishResult
│   ├── feithink.py         # optional: move file to content/posts/ and stage git commit
│   ├── substack.py         # reverse API via substack-api lib; create DRAFT; return edit URL
│   ├── wechat.py           # MD → WeChat-styled HTML; write output/wechat-html/<slug>.html; clipboard copy
│   ├── linkedin.py         # LinkedIn API v2; create UGC post with excerpt + canonical link
│   └── twitter.py          # X API v2; single tweet or auto-thread with excerpt + link
├── .env.example
└── README.md
```

### Runtime flow

1. `publish essays/musashi-go-farm.zh.md`
2. CLI parses frontmatter → `Post` dataclass.
3. Validation: `status == ready`, `slug` present, `lang` valid, declared platforms all have adapters + credentials loaded.
4. For each platform in `platforms:`:
   - Call `adapter.publish(post)`.
   - Capture `PublishResult(platform, ok, url|draft_url|message, error)`.
   - Append to `output/publish-log.jsonl` with timestamp.
5. Print summary table.
6. Exit non-zero if any adapter failed; owner can re-run with `--only <platform>` to retry.

### Example terminal output

```
$ publish essays/musashi-go-farm.zh.md
essays/musashi-go-farm.zh.md  →  lang=zh, 3 platforms, status=ready

  ✓ feithink    staged in content/posts/ (CF Pages will build after git push)
  ✓ substack    DRAFT created — https://substack.com/home/post/p-132322761/edit
                (open → click Publish to send to subscribers)
  ✓ wechat      output/wechat-html/musashi-go-farm.html (3.2 KB, copied to clipboard)
                → open 公众号后台 → 新建图文 → 粘贴

Log → output/publish-log.jsonl
```

If Substack cookie expired:

```
  ✗ substack    auth failed — session cookie expired
                → update SUBSTACK_SESSION in .env (see docs/publish-setup.md §Substack)
                → re-run: publish essays/musashi-go-farm.zh.md --only substack
```

## Frontmatter Schema

```yaml
title: string, required
slug: string, required, kebab-case, unique across lang pair
lang: "zh" | "en", required
date: YYYY-MM-DD, required
platforms: array<"feithink"|"substack"|"wechat"|"linkedin"|"twitter">, optional (defaults per lang)
excerpt: string, optional (auto-extracted from first paragraph if absent)
status: "draft" | "ready" | "published", required, CLI refuses non-ready
translation_of: string (slug), optional, EN files pointing to ZH source
canonical: URL, optional (override for cross-posted content)
```

Validation is strict — any malformed field fails fast before any adapter runs.

## Credentials & Security

All secrets in `.env` at repo root (already in `.gitignore`):

```env
# Substack — reverse API via extracted browser session cookie
SUBSTACK_SESSION=eyJ...           # update periodically when expires

# Twitter/X — Developer app credentials
TWITTER_CONSUMER_KEY=...
TWITTER_CONSUMER_SECRET=...
TWITTER_ACCESS_TOKEN=...
TWITTER_ACCESS_SECRET=...

# LinkedIn — OAuth 2.0 access token with w_member_social scope
LINKEDIN_ACCESS_TOKEN=...
LINKEDIN_PERSON_URN=urn:li:person:...
```

Ship `.env.example` with placeholders. Document one-time platform setup in `docs/publish-setup.md` (per-platform walkthrough: where to register app, which scopes, where cookies live, how to refresh).

## Implementation Phasing

Each phase ships an end-to-end slice. Phases are independent after Phase 0.

- **Phase 0 — Skeleton + core**: `Post` dataclass, frontmatter parser + validator, CLI entry with `--dry-run`, `--only`, `--skip`, jsonl log writer. No real adapters — dry-run prints what would happen.
- **Phase 1 — LinkedIn**: official API, lowest-risk path, validates the full loop end-to-end (auth → post → log → verify URL).
- **Phase 2 — Twitter**: official API, similar shape to LinkedIn. Decide single-tweet vs auto-thread strategy.
- **Phase 3 — WeChat**: MD → WeChat-styled HTML (use `doocs/md` logic or equivalent), write to disk + clipboard.
- **Phase 4 — Substack**: reverse API. Ship last because it is the most fragile; failure modes documented in `docs/publish-setup.md`.
- **Phase 5 — feithink adapter** *(optional)*: probably a plain `git add content/posts/... && git commit` wrapper is sufficient. Evaluate after Phase 4 whether it earns its keep.
- **Phase 6 — Docs**: `docs/publish-setup.md` (per-platform one-time setup), `tools/publish/README.md` (daily usage), `.env.example`.

If any platform proves unreliable in practice, the `--skip` flag lets the workflow continue without blocking on it.

## Out of Scope

- Multi-tenant / multi-author (this is Fei's personal tool).
- Automatic LLM translation — owner rejected explicitly; translation remains human.
- Image pipeline across platforms — initial version handles plain MD with image URLs pointing to feithink.org-hosted assets. WeChat's "永久素材" image upload and Twitter card OG image are Phase-7+ if ever needed.
- Cross-platform analytics aggregation — owner can check each platform's native dashboard.
- Scheduling / queueing — MVP runs synchronously when invoked.
- Automated publish to Substack (direct, no draft) — explicitly rejected on risk grounds.
- Any Chinese social platform beyond WeChat.
- Mirroring to Bluesky / Mastodon / Medium. Deferred until there is evidence they pay off.

## Success Criteria

1. Owner writes `essays/<slug>.zh.md` with `status: ready`, runs `publish essays/<slug>.zh.md`, and within 10 seconds the terminal confirms: (a) feithink file staged, (b) Substack draft URL returned, (c) WeChat HTML copied to clipboard. Total manual work remaining per ZH post: one click in Substack + one paste in WeChat editor.
2. Owner writes `essays/<slug>.en.md`, runs `publish essays/<slug>.en.md`, and within 10 seconds: feithink staged, Substack draft, LinkedIn post live, Twitter post live. Total manual work remaining per EN post: one click in Substack.
3. `output/publish-log.jsonl` contains one row per adapter invocation, enough to answer "when did I post X to Y, and what's the URL."
4. A failure in any single adapter does not prevent the others from publishing; re-running with `--only <platform>` retries cleanly.
5. Each credential failure produces a terminal message pointing at the specific `docs/publish-setup.md` section for recovery.

## Open Items (tracked but not blocking)

- Decide single-tweet vs auto-thread for Twitter at Phase 2 — may depend on length heuristic.
- Excerpt quality: auto-extract first paragraph vs require frontmatter `excerpt:` — provisional default is auto-extract with frontmatter override; revisit after a month of use.
- Whether feithink adapter is worth building (Phase 5) or whether `git` directly is simpler forever.

## Handoff

Next step: in a fresh session, invoke `superpowers:writing-plans` with this design document as context. Target output:
`docs/plans/2026-04-18-multi-platform-publisher-implementation.md`.
