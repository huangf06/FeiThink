import { readFileSync, writeFileSync, readdirSync, mkdirSync, existsSync } from 'node:fs'
import { join, basename, resolve } from 'node:path'
import matter from 'gray-matter'
import { transformFrontmatter } from './transform'

const DEFAULT_SOURCE = resolve(process.cwd(), '..', 'FeiThink', 'content', 'posts')
const DEST = resolve(process.cwd(), 'src', 'content', 'posts')

const FILENAME_RE = /^(.+)\.(en|zh)\.md$/

function deriveAbbrlink(base: string): string {
  return base.replace(/^\d+-/, '')
}

function migrateFile(srcPath: string): { dest: string; lang: 'en' | 'zh'; slug: string } | null {
  const fname = basename(srcPath)
  const match = FILENAME_RE.exec(fname)
  if (!match) {
    console.warn(`skip (no .en.md/.zh.md suffix): ${fname}`)
    return null
  }
  const base = match[1]
  const lang = match[2] as 'en' | 'zh'

  const raw = readFileSync(srcPath, 'utf-8')
  const { data, content } = matter(raw)

  const abbrlink = deriveAbbrlink(base)
  const astroFront = {
    ...transformFrontmatter(data),
    lang,
    abbrlink,
  }

  const rebuilt = matter.stringify(content, astroFront)
  const dest = join(DEST, fname)
  writeFileSync(dest, rebuilt, 'utf-8')
  return { dest, lang, slug: abbrlink }
}

function main() {
  const source = process.argv[2] ?? DEFAULT_SOURCE
  if (!existsSync(source)) {
    console.error(`Source not found: ${source}`)
    process.exit(1)
  }
  if (!existsSync(DEST)) {
    mkdirSync(DEST, { recursive: true })
  }

  const files = readdirSync(source).filter(f => f.endsWith('.md'))
  let migrated = 0
  const slugsByLang: Record<string, Set<string>> = { en: new Set(), zh: new Set() }

  for (const f of files) {
    const result = migrateFile(join(source, f))
    if (result) {
      migrated++
      slugsByLang[result.lang]?.add(result.slug)
    }
  }

  console.log(`\nMigrated ${migrated} of ${files.length} files`)
  console.log(`  en: ${slugsByLang.en.size} unique abbrlinks`)
  console.log(`  zh: ${slugsByLang.zh.size} unique abbrlinks`)

  const onlyEn = [...slugsByLang.en].filter(s => !slugsByLang.zh.has(s))
  const onlyZh = [...slugsByLang.zh].filter(s => !slugsByLang.en.has(s))
  if (onlyEn.length) console.log(`  en-only: ${onlyEn.join(', ')}`)
  if (onlyZh.length) console.log(`  zh-only: ${onlyZh.join(', ')}`)
}

main()
