import { describe, expect, it } from 'vitest'
import { NotFoundError } from '../src/errors.js'
import { createVerbsBll } from '../src/verbs/verbs.bll.js'
import type { VerbsRepository, VerbFilter } from '../src/verbs/verbs.repository.js'

// El repo real devuelve Queries de Mongoose (thenables); el falso, Promises.
const calls: { filter: VerbFilter; opts: { limit: number; skip: number; sort: Record<string, 1 | -1> } }[] = []
const fakeRepo = {
  searchVerbs: async (filter: VerbFilter, opts: { limit: number; skip: number; sort: Record<string, 1 | -1> }) => {
    calls.push({ filter, opts })
    return { data: [{ infinitive: 'anar' }], total: 1 }
  },
  findByInfinitive: async (inf: string) => (inf === 'anar' ? { infinitive: 'anar' } : null),
} as unknown as VerbsRepository

describe('verbs.bll (unitario, repo falso)', () => {
  const bll = createVerbsBll(fakeRepo)

  it('search calcula skip desde page (page=3, limit=10 → skip=20)', async () => {
    await bll.search({ page: 3, limit: 10 })
    expect(calls.at(-1)?.opts).toMatchObject({ limit: 10, skip: 20 })
  })

  it('search usa skip directo si se da', async () => {
    await bll.search({ limit: 25, skip: 50 })
    expect(calls.at(-1)?.opts).toMatchObject({ limit: 25, skip: 50 })
  })

  it('search q → filtro $or con regex escapada (q="a.b")', async () => {
    await bll.search({ q: 'a.b', limit: 50 })
    const rx = calls.at(-1)?.filter.$or?.[0]?.infinitive
    expect(String(rx)).toBe('/a\\.b/i')
  })

  it('search form/letter → filtro de forma e inicial', async () => {
    await bll.search({ form: 'vaig', letter: 'a', limit: 50 })
    expect(calls.at(-1)?.filter).toMatchObject({ form: 'vaig', letter: 'a' })
  })

  it('sort=clicks → orden por clicks desc', async () => {
    await bll.search({ sort: 'clicks', limit: 10 })
    expect(calls.at(-1)?.opts.sort).toMatchObject({ clicks: -1 })
  })

  it('getVerb lanza NotFoundError (404) si no existe', async () => {
    await expect(bll.getVerb('noexiste')).rejects.toBeInstanceOf(NotFoundError)
    await expect(bll.getVerb('noexiste')).rejects.toMatchObject({ status: 404 })
  })
})
