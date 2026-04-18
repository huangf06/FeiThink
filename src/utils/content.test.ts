import { beforeEach, describe, expect, it, vi } from 'vitest'

vi.mock('astro:content', () => ({
  getCollection: vi.fn(),
  render: vi.fn(async () => ({ remarkPluginFrontmatter: { minutes: 1 } })),
}))

vi.mock('@/config', () => ({
  defaultLocale: 'en',
}))

// Force production mode so _getPosts' draft filter runs
vi.stubEnv('DEV', false)
vi.stubEnv('PROD', true)

import { getCollection } from 'astro:content'
import { getEssays, getMoments, groupMomentsByYear } from './content'

function mockPost(overrides: { id?: string, data?: Record<string, any> } = {}) {
  return {
    id: overrides.id ?? 'x',
    data: {
      title: 't',
      published: new Date('2026-01-01'),
      description: '',
      tags: [],
      draft: false,
      pin: 0,
      toc: false,
      lang: 'en',
      abbrlink: '',
      type: 'essay',
      ...overrides.data,
    },
  }
}

function mockCollection(entries: any[]) {
  ;(getCollection as any).mockImplementation(
    async (_name: any, filter?: (p: any) => boolean) =>
      filter ? entries.filter(filter) : entries,
  )
}

describe('getEssays / getMoments', () => {
  beforeEach(() => vi.clearAllMocks())

  it('getEssays returns only type=essay, excluding drafts', async () => {
    mockCollection([
      mockPost({ id: 'a', data: { type: 'essay' } }),
      mockPost({ id: 'b', data: { type: 'moment' } }),
      mockPost({ id: 'c', data: { type: 'essay', draft: true } }),
    ])
    const result = await getEssays('en')
    expect(result.map(p => p.id)).toEqual(['a'])
  })

  it('getMoments returns only type=moment, excluding drafts, newest first', async () => {
    mockCollection([
      mockPost({ id: 'a', data: { type: 'essay' } }),
      mockPost({ id: 'b', data: { type: 'moment', published: new Date('2026-01-01') } }),
      mockPost({ id: 'c', data: { type: 'moment', published: new Date('2026-02-01') } }),
      mockPost({ id: 'd', data: { type: 'moment', draft: true, published: new Date('2026-03-01') } }),
    ])
    const result = await getMoments('en')
    expect(result.map(p => p.id)).toEqual(['c', 'b'])
  })
})

describe('groupMomentsByYear', () => {
  beforeEach(() => vi.clearAllMocks())

  it('groups moments by year, newest year first, newest moment first within a year', async () => {
    mockCollection([
      mockPost({ id: 'a', data: { type: 'moment', published: new Date('2024-06-01') } }),
      mockPost({ id: 'b', data: { type: 'moment', published: new Date('2026-03-01') } }),
      mockPost({ id: 'c', data: { type: 'moment', published: new Date('2026-01-15') } }),
    ])
    const result = await groupMomentsByYear('en')
    expect(result.map(g => g.year)).toEqual([2026, 2024])
    expect(result[0].moments.map(m => m.id)).toEqual(['b', 'c'])
    expect(result[1].moments.map(m => m.id)).toEqual(['a'])
  })
})
