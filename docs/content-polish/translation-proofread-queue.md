# Translation + Proofread Queue

> Built 2026-04-18 from `src/content/posts/` snapshot. Tracks every visible post through the **translate → proofread → done** workflow that owner locked: *"我所有的文章，都需要翻译+校对的流程"*.

## Decisions locked 2026-04-18

- **Translation voice: idiomatic EN with philosophical precision** — see "Translation discipline" below.
- **Only `why-we-read-kant` is owner-proofread upfront.** Every other EN row stays `en-mt` and goes through normal pass.
- **Order: storefront first, then chronological walk.** Phase 1A (pin posts, 5) runs first so the site face is right. After that, Phase 1B (ZH-only 6) and Phase 2 (31 bilingual) are merged into one chronological queue ordered by publish date (≈ ID), so owner re-reads the essays in the order they were written. See "Revised walk order" below.
- **Pin 97 still pulled** (active-love, awaiting owner final review before restore). **Pin 96 slot reassigned**: sublime-suffering permanently unpinned 2026-04-18 (owner: too heavy for storefront); `ikiru` picked as replacement, needs proofread before pin.

## Translation discipline (for new EN drafts)

Default mode: **idiomatic English sentence-level, philosophical density preserved**. Three hard rules:

1. **Kant / philosophy terms lock to canonical English.** Use Allen Wood or Mary Gregor for Kant (*Groundwork of the Metaphysics of Morals*, *Critique of Practical Reason*), Pevear & Volokhonsky or Garnett for Dostoevsky, standard English titles for Tolstoy, Yalom, etc. No ad-hoc retranslations of known terms. **When the ZH cites or paraphrases a famous book line, the EN must use the canonical source wording (word pairs, phrasing), not my own paraphrase** — even if the ZH compresses the line into an aphoristic imperative. E.g., `爱具体的人，不爱抽象的人` → `love people in particular, not humanity in general` (the `in particular / in general` pair from Zosima's doctor's confession, Book II Ch 4), **not** `concrete persons, humanity in the abstract` (invented paraphrase).
2. **No Chinese (or Japanese) characters in EN main text.** Owner finds them jarring in English prose. Replacement policy:
   - **Proper nouns** (people, account names, places): pinyin (Mandarin) or romaji (Japanese), no characters. E.g., `正十七` → `"Zheng Shiqi"`; `天下無双` → `"invincible under the sun"` or romaji `tenka musō` if the original term matters.
   - **Book/film/work titles**: English translation in italics. If no canonical English translation exists, use pinyin/romaji in italics. E.g., `《英雄志》` → `*Heroes' Record*`.
   - **Philosophical/cultural concepts with no clean English match**: *italicized pinyin* + short inline gloss on first mention, e.g., `*chaxu geju* (the differential pattern of relationships)`, `*xiangyuan* (Confucius's hollow conformist)`. On second mention, English gloss alone is fine.
   - **Exception — stroke-level etymology/puns**: when the character shape itself carries the meaning (e.g., the 少→小 one-stroke prop error in *The Fifth Republic*), preserve the characters, but **move them to a footnote** with explanation, not the main narrative.
3. **Do not flatten intellectual density.** If the ZH sentence is tight, the EN stays tight. Don't smooth out the argument to make it "read easier", that kills the Kantian register. Idiom may shift at the sentence level; the *argument* must not be diluted.
4. **No em-dashes (—) anywhere in translated EN.** Owner considers em-dashes an AI tell. Replace contextually: commas for light asides, colons for emphatic breaks, periods for hard stops, parentheses for parenthetical inserts, semicolons for tight contrast. For blockquote attribution use `*Name*` (italicized name) rather than `—Name`. This rule also applies retroactively when polishing `en-mt` rows.

Anti-patterns to avoid:
- Performative literary cadence mimicking Chinese rhythm in English (purple prose).
- Auto-translating 乡愿 → "Mr. Nice Guy" without the gloss — the concept is not the same.
- Turning short declarative Chinese beats into flowing multi-clause English.
- Over-explaining allusions (*Vagabond*, *Brighter Summer Day*, *Dream of the Red Chamber*). A short parenthetical is enough; readers who care will look it up.

## Revised walk order

1. **Phase 1A — storefront (5 essays).** Pins, in pin order. Translate 97 + 96 first so pins can be restored; proofread 98 + 95; 99 already done.
2. **Chronological walk (37 essays).** All remaining visible posts sorted by ID ascending. This mixes proofreading (Phase 2 bilingual) and translation (Phase 1B ZH-only) — whatever the essay needs, handled in publish order. Owner re-reads the intellectual journey from `prologue` forward.
3. **Phase 3 deferred.** Draft-only essays untouched unless owner promotes one.

Net work: 8 translations + ~34 proofreads. Batching per `Suggested batching` below.

## Workflow & status fields

```
[ status ]   meaning                                                  next action
─────────────────────────────────────────────────────────────────────────────────
todo         no work yet                                              translate (if EN missing) or queue for proofread
en-mt        EN exists but is unverified MT (default for old set)     proofread
en-draft     EN draft from this batch, awaiting first proofread       proofread
proofread    owner has read both versions side-by-side, edits done    publish (or already published)
done         owner final-signed                                       leave alone
skip         owner pulled from site                                   draft:true or delete
```

How to use this file: owner edits the **Status** column inline. When you change a row to `proofread` or `done`, that's the durable signal for me. I never assume a row is `done` without that mark.

---

## Phase 1 — pin set + new ZH-only (priority)

These are the **face of the site** + **freshest content**. Do these first.

### 1A. Pinned essays (5 — owner has read EN of pin:99 already)

| ID | Slug | Line | EN status | ZH status | Owner notes |
|----|------|------|-----------|-----------|-------------|
| 149999960 | why-we-read-kant | kant | **proofread** (owner has done this) | todo | pin:99 |
| 167521111 | rereading-the-brothers-karamazov | dostoevsky | **proofread** 2026-04-18 (owner signed off) | todo | pin:98 |
| 182970593 | active-love-grounded-as-mountain | moral-life | en-draft (owner-edited, em-dash-free, **awaiting final review**) | todo | pin:97 pulled |
| 187142537 | the-sublime-suffering | kant | **proofread** 2026-04-18 (10 polish edits applied, owner approved) | todo | **pin removed by owner 2026-04-18** (too heavy for storefront) |
| 159302102 | ikiru | (none) | en-mt | todo | **pin:96 candidate** (owner pick 2026-04-18, awaiting proofread before restore) |
| 173845261 | dumbledores-woolen-socks | (none) | **proofread** 2026-04-18 (owner signed off) | todo | pin:95 |

### 1B. ZH-only essays (6 remaining — need EN created, then proofread)

These are the recent Substack posts I imported in Batch 3. EN is missing entirely.

| ID | Slug | Line | EN status | ZH status |
|----|------|------|-----------|-----------|
| 168080169 | how-to-traverse-an-existential-crisis | existence-and-self | en-draft (this session) | todo |
| 170658812 | feminism-vs-kantianism | kant | missing | todo |
| 171758194 | why-i-feel-homeless | existence-and-self | missing | todo |
| 175381089 | false-criticism-and-mediocrity-of-writers | moral-life | missing | todo |
| 184936010 | beyond-the-differential-pattern | moral-life | missing | todo |
| 185294968 | love-and-evil-by-the-measure-of-freedom | kant | missing | todo |
| 187724996 | vagabond-go-farm | dostoevsky | missing | todo |

**Phase 1 totals:** 5 pinned (1 EN done, 4 to proofread, 2 to translate) + 7 ZH-only (1 EN drafted, 6 to translate). Net new EN translations: **8**. Proofreads: **4 + 8 = 12**.

---

## Phase 2 — bilingual visible essays, grouped by reading line

After phase 1, work line-by-line so the site reads coherently as each line settles. EN is `en-mt` by default — owner has never line-by-line proofread these.

### 2A. Kant (5 essays)

| ID | Slug | EN | ZH | Notes |
|----|------|----|----|-------|
| 132322761 | groundwork-of-the-metaphysics-of-morals-i | en-mt | todo | translation of Kant primary text — proofread carefully |
| 136922186 | groundwork-of-the-metaphysics-of-morals-ii | en-mt | todo | translation of Kant primary text |
| 137279640 | on-liberal-education-and-free-will | en-mt | todo | |
| 137280827 | what-is-morality | en-mt | todo | |
| the-dignity-of-man | (no ID) | en-mt | todo | early essay |

### 2B. Moral life (8 essays)

| ID | Slug | EN | ZH | Notes |
|----|------|----|----|-------|
| 137279609 | in-memory-of-an-ordinary-man-dr-li-wenliang | en-mt | todo | |
| 137279657 | twelve-angry-men-and-roberts-rules-of-order | en-mt | todo | |
| 137281107 | on-human-nature-what-the-white-paper-protests-taught-me | en-mt | todo | sensitive topic — careful tone |
| 137281163 | on-being-a-person-of-integrity | en-mt | todo | |
| 139089803 | do-not-lie | en-mt | todo | |
| 149437568 | luo-xiang-a-light-flickering-against-the-wind | en-mt | todo | |
| 150375922 | why-discriminating-belittles-you | en-mt | todo | |
| 167520604 | skin-in-the-game | en-mt | todo | |

### 2C. Dostoevsky & literature (5 essays)

| ID | Slug | EN | ZH | Notes |
|----|------|----|----|-------|
| 137573845 | vagabond-and-the-sublime | en-mt | todo | |
| 149286461 | reading-notes-on-the-idiot-christ-like-love | en-mt | todo | |
| 153473895 | starting-from-one-hundred-years-of-solitude | en-mt | todo | |
| 167520908 | humiliated-and-insulted | en-mt | todo | |

### 2D. Existence & self (5 essays)

| ID | Slug | EN | ZH | Notes |
|----|------|----|----|-------|
| 143075712 | essence-of-existential-psychotherapy | en-mt | todo | Yalom — terminology check |
| 149286325 | wandering-and-belonging | en-mt | todo | |
| 149286531 | how-to-take-care-of-your-emotions | en-mt | todo | |
| 155013311 | subjectivity-how-to-become-the-protagonist-of-your-own-life | en-mt | todo | |
| 155013391 | reason-and-emotion | en-mt | todo | |

### 2E. No line tag (8 essays)

These never got assigned a reading line. Most are stand-alone. Either assign a line during proofread or confirm they stay loose.

| ID | Slug | EN | ZH | Notes |
|----|------|----|----|-------|
| 137279583 | prologue | en-mt | todo | site origin essay |
| 137279595 | to-high-school-students-written-to-my-sister | en-mt | todo | |
| 137279611 | memories-of-college-life-on-pain-and-healing | en-mt | todo | |
| 137279658 | history-of-thought-01-from-myth-to-reason | en-mt | todo | series — consider line |
| 137279659 | history-of-thought-02-is-there-universal-law | en-mt | todo | series |
| 137279661 | history-of-thought-03-how-to-be-happy | en-mt | todo | series |
| 137279660 | history-of-thought-04-overview-and-reflections | en-mt | todo | series |
| 159302102 | ikiru | en-mt | todo | |
| 172314779 | the-scale-of-time | en-mt | todo | |
| 202512230001 | let-there-be-light | en-mt | todo | |
| perfect-friendship-and-bitter-merit | (no ID) | en-mt | todo | early essay |

**Phase 2 totals:** 31 bilingual pairs to proofread.

---

## Phase 3 — drafted essays (deferred)

These are `draft: true` in both languages. They're hidden from the site. Decision was: keep around but don't surface. Proofread only if/when promoting one.

| ID | Slug |
|----|------|
| 137279586 | rereading-shen-pangpang |
| 137279589 | inspired-by-matthew-pottinger |
| 137279596 | take-reality-for-a-ride |
| 137279598 | questions-about-a-recent-viral-article-i |
| 137279602 | questions-about-recent-viral-articles-ii |
| 137279603 | things-i-want-to-do |
| 137279663 | reading-on-writing-well |
| 137280893 | more-on-morality-unfinished-thoughts |
| 140402278 | from-chosin-reservoir-to-christmas |
| 140429780 | elements-of-happiness-for-intjs |
| 141718568 | reflections-on-1212-the-day |
| 149943314 | personal-development-for-smart-people |

---

## Suggested batching

Batch sizes I can hold in one session without losing precision:

- **Translation (ZH → EN):** 1 essay per batch — full attention to register, idiom, philosophical terms. 7 batches for Phase 1B (1 already drafted) + 2 for pin posts = **9 translation batches**.
- **Proofread (EN ↔ ZH):** 2-3 essays per batch when both are short personal essays; 1 per batch for Kant Groundwork or other long/dense pieces. ~**15 proofread batches** for everything visible.

How owner participates:
- **Translation drafts:** I produce; owner reads + edits. Marks `proofread` when satisfied.
- **Proofread of existing EN-MT:** I produce a side-by-side diff with proposed corrections; owner approves block-by-block.
- **Owner-already-checked rows:** owner marks `done` and they leave the queue.

---

## Open questions for owner

1. **Translation voice.** EN-MT today is fairly literal. For new translations, prefer (a) literal + footnote idioms, (b) idiomatic + slight rephrasing, or (c) freer literary register matching the ZH cadence?
2. **Owner's already-proofread EN rows.** Besides `why-we-read-kant`, any others I should mark `proofread` upfront so we don't re-do them? (Owner mentioned this is partial — fine to leave untouched and audit during normal pass.)
3. **Phase 2 ordering.** I default to kant → moral-life → dostoevsky → existence → no-line. Override if a different line should land first.
4. **Pin posts that lack EN (active-love, sublime-suffering).** Are they comfortable being pinned in ZH-only state for now (EN draft will fill within a couple of weeks), or pull pin until EN ships?
