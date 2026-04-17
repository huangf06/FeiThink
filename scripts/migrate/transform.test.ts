import { describe, it, expect } from 'vitest'
import { transformFrontmatter } from './transform'

describe('transformFrontmatter', () => {
  it('maps Hugo date to Astro published and summary to description', () => {
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

  it('drops Hugo-specific fields (weight, showToc, TocOpen, categories, author, lastmod-as-key)', () => {
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
    expect(astro).not.toHaveProperty('lastmod')
  })

  it('sets default draft=false when Hugo draft unspecified', () => {
    const hugo = { title: 'Test', date: '2025-10-08' }
    const astro = transformFrontmatter(hugo)
    expect(astro.draft).toBe(false)
  })

  it('preserves Astro-specific fields we may have added manually', () => {
    const hugo = {
      title: 'Test',
      date: '2025-10-08',
      pin: 99,
      line: 'kant',
      standalone: true,
      abbrlink: 'why-kant',
    }
    const astro = transformFrontmatter(hugo)
    expect(astro.pin).toBe(99)
    expect(astro.line).toBe('kant')
    expect(astro.standalone).toBe(true)
    expect(astro.abbrlink).toBe('why-kant')
  })

  it('omits updated when lastmod equals date (avoids noisy "updated" display)', () => {
    const hugo = {
      title: 'Test',
      date: '2023-07-01',
      lastmod: '2023-07-01',
    }
    const astro = transformFrontmatter(hugo)
    expect(astro).not.toHaveProperty('updated')
    expect(astro.published).toBe('2023-07-01')
  })

  it('sets updated when lastmod differs from date', () => {
    const hugo = {
      title: 'Test',
      date: '2025-11-10',
      lastmod: '2025-12-25',
    }
    const astro = transformFrontmatter(hugo)
    expect(astro.updated).toBe('2025-12-25')
  })

  it('omits updated when lastmod is missing', () => {
    const hugo = { title: 'Test', date: '2025-10-08' }
    const astro = transformFrontmatter(hugo)
    expect(astro).not.toHaveProperty('updated')
  })

  it('omits description when summary is missing or empty', () => {
    const noSummary = transformFrontmatter({ title: 'T', date: '2025-10-08' })
    expect(noSummary).not.toHaveProperty('description')

    const emptySummary = transformFrontmatter({ title: 'T', date: '2025-10-08', summary: '' })
    expect(emptySummary).not.toHaveProperty('description')
  })

  it('preserves empty tags array as empty (retypeset default)', () => {
    const hugo = { title: 'T', date: '2025-10-08' }
    const astro = transformFrontmatter(hugo)
    // Not required, but if present should be an array — schema default is []
    if ('tags' in astro) expect(astro.tags).toEqual([])
  })

  it('handles Date objects (YAML parses dates natively)', () => {
    const d1 = new Date('2025-10-08T00:00:00Z')
    const d2 = new Date('2025-10-09T00:00:00Z')
    const astro = transformFrontmatter({ title: 'T', date: d1, lastmod: d2 })
    expect(astro.published).toBe(d1)
    expect(astro.updated).toBe(d2)
  })

  it('handles Date objects where lastmod equals date', () => {
    const d = new Date('2025-10-08T00:00:00Z')
    const astro = transformFrontmatter({ title: 'T', date: d, lastmod: new Date(d.getTime()) })
    expect(astro).not.toHaveProperty('updated')
  })
})
