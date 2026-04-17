import { readFileSync, writeFileSync, readdirSync } from 'node:fs'
import { join, resolve } from 'node:path'
import matter from 'gray-matter'

type Line = 'kant' | 'dostoevsky-and-literature' | 'existence-and-self' | 'moral-life'
interface Curation { line?: Line; standalone?: true; pin?: number }

const POSTS_DIR = resolve(process.cwd(), 'src', 'content', 'posts')

const CURATION: Record<string, Curation> = {
  // Kant line
  'groundwork-of-the-metaphysics-of-morals-i': { line: 'kant' },
  'groundwork-of-the-metaphysics-of-morals-ii': { line: 'kant' },
  'why-we-read-kant': { line: 'kant', pin: 99 },
  'the-dignity-of-man': { line: 'kant' },
  'what-is-morality': { line: 'kant' },

  // Dostoevsky & Literature
  'rereading-the-brothers-karamazov': { line: 'dostoevsky-and-literature', pin: 98 },
  'reading-notes-on-the-idiot-christ-like-love': { line: 'dostoevsky-and-literature' },
  'humiliated-and-insulted': { line: 'dostoevsky-and-literature' },
  'vagabond-and-the-sublime': { line: 'dostoevsky-and-literature' },
  'starting-from-one-hundred-years-of-solitude': { line: 'dostoevsky-and-literature' },

  // Existence & Self
  'essence-of-existential-psychotherapy': { line: 'existence-and-self' },
  'subjectivity-how-to-become-the-protagonist-of-your-own-life': { line: 'existence-and-self' },
  'reason-and-emotion': { line: 'existence-and-self' },
  'wandering-and-belonging': { line: 'existence-and-self' },
  'elements-of-happiness-for-intjs': { line: 'existence-and-self' },

  // Moral Life & Public
  'on-being-a-person-of-integrity': { line: 'moral-life' },
  'do-not-lie': { line: 'moral-life' },
  'why-discriminating-belittles-you': { line: 'moral-life' },
  'on-human-nature-what-the-white-paper-protests-taught-me': { line: 'moral-life' },
  'luo-xiang-a-light-flickering-against-the-wind': { line: 'moral-life' },

  // Standalone gems
  'ikiru': { standalone: true, pin: 97 },
  'the-scale-of-time': { standalone: true },
  'dumbledores-woolen-socks': { standalone: true },
  'let-there-be-light': { standalone: true },
  'perfect-friendship-and-bitter-merit': { standalone: true },
}

function applyCuration(abbrlink: string, front: Record<string, any>): Record<string, any> {
  const curated = CURATION[abbrlink]
  const next: Record<string, any> = { ...front }

  // Reset curation-controlled fields (idempotent re-runs)
  delete next.line
  delete next.standalone
  if (next.pin === 0) delete next.pin

  if (curated) {
    if (curated.line) next.line = curated.line
    if (curated.standalone) next.standalone = true
    if (curated.pin !== undefined) next.pin = curated.pin
    next.draft = false
  }
  else {
    next.draft = true
    delete next.pin
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

  console.log(`Curated ${files.length} files (both en+zh):`)
  console.log(`  lined:     ${counts.lined}  (target 40 = 20×2)`)
  console.log(`  standalone:${counts.standalone}  (target 10 = 5×2)`)
  console.log(`  pinned:    ${counts.pinned}  (target 6 = 3×2)`)
  console.log(`  drafted:   ${counts.drafted}  (target 46 = 23×2)`)
  console.log(`  published: ${counts.published}  (target 50 = 25×2)`)
}

main()
