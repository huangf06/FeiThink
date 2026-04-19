import { readFileSync, writeFileSync, readdirSync } from 'node:fs'
import { join, resolve } from 'node:path'
import matter from 'gray-matter'

type Line = 'kant' | 'dostoevsky-and-literature' | 'existence-and-self' | 'moral-life'
interface Curation {
  line?: Line
  standalone?: true
  pin?: number
  /** Explicitly drafted even though listed (preserves line while hiding post). */
  draft?: true
}

const POSTS_DIR = resolve(process.cwd(), 'src', 'content', 'posts')

// Source of truth. Any abbrlink missing here is treated as draft, line/standalone/pin stripped.
// Keep in sync with src/content/posts/*.md frontmatter — running this script is a no-op when aligned.
const CURATION: Record<string, Curation> = {
  // Pinned (home page hero)
  'why-we-read-kant':                              { line: 'kant', pin: 99 },
  'rereading-the-brothers-karamazov':              { line: 'dostoevsky-and-literature', pin: 98 },
  'active-love-grounded-as-mountain':              { line: 'moral-life', pin: 97 },
  'ikiru':                                         { standalone: true, pin: 96 },
  'dumbledores-woolen-socks':                      { standalone: true, pin: 95 },

  // Kant line
  'groundwork-of-the-metaphysics-of-morals-i':     { line: 'kant' },
  'groundwork-of-the-metaphysics-of-morals-ii':    { line: 'kant' },
  'on-liberal-education-and-free-will':            { line: 'kant' },
  'what-is-morality':                              { line: 'kant' },
  'feminism-vs-kantianism':                        { line: 'kant' },
  'love-and-evil-by-the-measure-of-freedom':       { line: 'kant' },
  'the-dignity-of-man':                            { line: 'kant' },
  'the-sublime-suffering':                         { line: 'kant' },

  // Dostoevsky & Literature
  'vagabond-and-the-sublime':                      { line: 'dostoevsky-and-literature' },
  'reading-notes-on-the-idiot-christ-like-love':   { line: 'dostoevsky-and-literature' },
  'starting-from-one-hundred-years-of-solitude':   { line: 'dostoevsky-and-literature' },
  'humiliated-and-insulted':                       { line: 'dostoevsky-and-literature' },
  'vagabond-go-farm':                              { line: 'dostoevsky-and-literature' },

  // Existence & Self
  'essence-of-existential-psychotherapy':          { line: 'existence-and-self' },
  'wandering-and-belonging':                       { line: 'existence-and-self' },
  'how-to-take-care-of-your-emotions':             { line: 'existence-and-self' },
  'subjectivity-how-to-become-the-protagonist-of-your-own-life': { line: 'existence-and-self' },
  'reason-and-emotion':                            { line: 'existence-and-self' },
  'how-to-traverse-an-existential-crisis':         { line: 'existence-and-self' },
  'why-i-feel-homeless':                           { line: 'existence-and-self' },
  'elements-of-happiness-for-intjs':               { line: 'existence-and-self', draft: true },

  // Moral Life & Public
  'in-memory-of-an-ordinary-man-dr-li-wenliang':   { line: 'moral-life' },
  'twelve-angry-men-and-roberts-rules-of-order':   { line: 'moral-life' },
  'on-human-nature-what-the-white-paper-protests-taught-me': { line: 'moral-life' },
  'on-being-a-person-of-integrity':                { line: 'moral-life' },
  'do-not-lie':                                    { line: 'moral-life' },
  'luo-xiang-a-light-flickering-against-the-wind': { line: 'moral-life' },
  'why-discriminating-belittles-you':              { line: 'moral-life' },
  'skin-in-the-game':                              { line: 'moral-life' },
  'false-criticism-and-mediocrity-of-writers':     { line: 'moral-life' },
  'beyond-the-differential-pattern':               { line: 'moral-life' },

  // Standalone gems
  'the-scale-of-time':                             { standalone: true },
  'let-there-be-light':                            { standalone: true },
  'perfect-friendship-and-bitter-merit':           { standalone: true },

  // Uncategorized but published (archive only, no line/standalone)
  'prologue':                                      {},
  'to-high-school-students-written-to-my-sister':  {},
  'memories-of-college-life-on-pain-and-healing':  {},
  'history-of-thought-01-from-myth-to-reason':     {},
  'history-of-thought-02-is-there-universal-law':  {},
  'history-of-thought-03-how-to-be-happy':         {},
  'history-of-thought-04-overview-and-reflections':{},
}

function applyCuration(abbrlink: string, front: Record<string, any>): Record<string, any> {
  const curated = CURATION[abbrlink]
  const next: Record<string, any> = { ...front }

  // Map is authoritative — reset all curation-controlled fields every run.
  delete next.line
  delete next.standalone
  delete next.pin

  if (curated) {
    if (curated.line) next.line = curated.line
    if (curated.standalone) next.standalone = true
    if (curated.pin !== undefined) next.pin = curated.pin
    next.draft = curated.draft ?? false
  }
  else {
    next.draft = true
  }

  return next
}

function main() {
  const files = readdirSync(POSTS_DIR).filter(f => f.endsWith('.md'))
  const counts = { lined: 0, standalone: 0, pinned: 0, drafted: 0, published: 0 }

  for (const f of files) {
    const path = join(POSTS_DIR, f)
    const raw = readFileSync(path, 'utf-8')
    const parsed = matter(raw)
    const abbrlink = parsed.data.abbrlink as string
    const next = applyCuration(abbrlink, parsed.data)

    const rebuilt = matter.stringify(parsed.content, next)
    writeFileSync(path, rebuilt, 'utf-8')

    if (next.line) counts.lined++
    if (next.standalone) counts.standalone++
    if (next.pin) counts.pinned++
    if (next.draft) counts.drafted++
    else counts.published++
  }

  console.log(`Curated ${files.length} files:`)
  console.log(`  lined:     ${counts.lined}`)
  console.log(`  standalone:${counts.standalone}`)
  console.log(`  pinned:    ${counts.pinned}`)
  console.log(`  drafted:   ${counts.drafted}`)
  console.log(`  published: ${counts.published}`)
}

main()
