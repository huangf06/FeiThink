const HUGO_ONLY_FIELDS = new Set([
  'weight',
  'showToc',
  'TocOpen',
  'categories',
  'author',
  'lastmod',
])

const ASTRO_PASSTHROUGH_FIELDS = [
  'title',
  'tags',
  'pin',
  'line',
  'standalone',
  'abbrlink',
  'toc',
  'lang',
] as const

function sameDate(a: unknown, b: unknown): boolean {
  if (a instanceof Date && b instanceof Date) return a.getTime() === b.getTime()
  return a === b
}

export function transformFrontmatter(hugo: Record<string, any>): Record<string, any> {
  const astro: Record<string, any> = {}

  for (const key of ASTRO_PASSTHROUGH_FIELDS) {
    if (key in hugo) astro[key] = hugo[key]
  }

  if ('date' in hugo) astro.published = hugo.date

  if ('lastmod' in hugo && !sameDate(hugo.lastmod, hugo.date)) {
    astro.updated = hugo.lastmod
  }

  if ('summary' in hugo && hugo.summary !== '' && hugo.summary != null) {
    astro.description = hugo.summary
  }

  astro.draft = hugo.draft ?? false

  return astro
}
