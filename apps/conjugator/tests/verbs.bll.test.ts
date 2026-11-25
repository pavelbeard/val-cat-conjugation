import { describe, expect, it, vi } from 'vitest'
import { NotFoundError } from '@vcc/api-builder'
import type { SearchOptions, SearchQuery } from '../src/api/verbs/verbs.repository.js'

const calls: { query: SearchQuery; options: SearchOptions }[] = []

vi.mock('../src/api/verbs/verbs.repository.js', () => ({
  verbsRepository: {
    search: async (query: SearchQuery, options: SearchOptions) => {
      calls.push({ query, options })
      return [{ infinitive: 'anar' }]
    },
    count: async () => 1,
    findByInfinitive: async (inf: string) => (inf === 'anar' ? { infinitive: 'anar' } : null),
  },
}))

const { search, getVerb } = await import('../src/api/verbs/verbs.bll.js')

describe('verbs.bll (unitario, repository mockeado)', () => {
  it('search calcula skip desde page (page=3, limit=10 → skip=20)', async () => {
    await search({ page: 3, limit: 10 })
    expect(calls.at(-1)?.options).toMatchObject({ limit: 10, skip: 20 })
  })

  it('search usa skip directo si se da', async () => {
    await search({ limit: 25, skip: 50 })
    expect(calls.at(-1)?.options).toMatchObject({ limit: 25, skip: 50 })
  })

  it('search devuelve { data, count }', async () => {
    const res = await search({ limit: 50 })
    expect(res).toMatchObject({ data: [{ infinitive: 'anar' }], count: 1 })
  })

  it('search q → query de dominio q (el repository monta el $or con helpers de lib/db)', async () => {
    await search({ q: 'a.b', limit: 50 })
    expect(calls.at(-1)?.query).toMatchObject({ q: 'a.b' })
  })

  it('search form/letter → query de forma e inicial', async () => {
    await search({ form: 'vaig', letter: 'a', limit: 50 })
    expect(calls.at(-1)?.query).toMatchObject({ form: 'vaig', letter: 'a' })
  })

  it('sort=clicks → orden por clicks desc', async () => {
    await search({ sort: 'clicks', limit: 10 })
    expect(calls.at(-1)?.options.sort).toMatchObject({ clicks: -1 })
  })

  it('getVerb devuelve error.notFound (404) si no existe', async () => {
    const res = await getVerb('noexiste')
    expect(res).toBeInstanceOf(NotFoundError)
    expect((res as NotFoundError).status).toBe(404)
  })

  it('getVerb devuelve el verb si existe', async () => {
    const res = await getVerb('anar')
    expect(res).toMatchObject({ infinitive: 'anar' })
  })
})
