import { afterAll, beforeAll, describe, expect, it } from 'vitest'
import request from 'supertest'
import { app } from '../src/app.js'
import { Verb } from '../src/models/verb.js'
import { ANAR_FIXTURE, setupTestDb, teardownTestDb } from './helpers.js'

beforeAll(async () => {
  await setupTestDb()
  await Verb.create(ANAR_FIXTURE)
  await Verb.create({ infinitive: 'parlar', translation: 'hablar', clicks: 5 })
  await Verb.insertMany(
    Array.from({ length: 30 }, (_, i) => ({
      infinitive: `verb${String(i + 1).padStart(2, '0')}`,
      translation: `trad${i + 1}`,
    })),
  )
})

afterAll(teardownTestDb)

describe('GET /api/verbs (list-all eliminado)', () => {
  it('→ 404', async () => {
    const res = await request(app).get('/api/verbs')
    expect(res.status).toBe(404)
  })
})

describe('GET /api/verbs/search → { data, metadata }', () => {
  it('form=vaig encuentra anar con metadata por defecto', async () => {
    const res = await request(app).get('/api/verbs/search').query({ form: 'vaig' })
    expect(res.status).toBe(200)
    expect(res.body.data.map((v: { infinitive: string }) => v.infinitive)).toContain('anar')
    expect(res.body.metadata).toMatchObject({ total: 1, limit: 50, skip: 0, page: 1, totalPages: 1 })
  })

  it('q busca en infinitivo y traducción', async () => {
    const res = await request(app).get('/api/verbs/search').query({ q: 'hablar' })
    expect(res.status).toBe(200)
    expect(res.body.data.map((v: { infinitive: string }) => v.infinitive)).toEqual(['parlar'])
    expect(res.body.metadata.total).toBe(1)
  })

  it('letter=v filtra por inicial (30 verbXX)', async () => {
    const res = await request(app).get('/api/verbs/search').query({ letter: 'v' })
    expect(res.status).toBe(200)
    expect(res.body.metadata.total).toBe(30)
    expect(res.body.data.every((v: { infinitive: string }) => v.infinitive.startsWith('verb'))).toBe(true)
  })

  it('paginación con limit/skip', async () => {
    const res = await request(app).get('/api/verbs/search').query({ limit: 10, skip: 10 })
    expect(res.status).toBe(200)
    expect(res.body.data).toHaveLength(10)
    expect(res.body.metadata).toMatchObject({ total: 32, limit: 10, skip: 10, page: 2, totalPages: 4 })
  })

  it('paginación con page (page=3, limit=10 → skip=20)', async () => {
    const res = await request(app).get('/api/verbs/search').query({ page: 3, limit: 10 })
    expect(res.status).toBe(200)
    expect(res.body.metadata).toMatchObject({ total: 32, limit: 10, skip: 20, page: 3, totalPages: 4 })
    expect(res.body.data).toHaveLength(10)
  })

  it('sort=clicks ordena por clicks desc', async () => {
    await Verb.updateOne({ infinitive: 'anar' }, { clicks: 999 })
    const res = await request(app).get('/api/verbs/search').query({ sort: 'clicks', limit: 5 })
    expect(res.status).toBe(200)
    expect(res.body.data[0].infinitive).toBe('anar')
  })

  it('sin params → primera página (limit 50) de todos', async () => {
    const res = await request(app).get('/api/verbs/search')
    expect(res.status).toBe(200)
    expect(res.body.data).toHaveLength(32)
    expect(res.body.metadata).toMatchObject({ total: 32, limit: 50, skip: 0, page: 1, totalPages: 1 })
  })

  it('limit inválido → 400 (zod)', async () => {
    const res = await request(app).get('/api/verbs/search').query({ limit: 'abc' })
    expect(res.status).toBe(400)
    expect(res.body.error).toMatch(/limit/)
  })
})

describe('GET /api/verbs/:infinitive', () => {
  it('devuelve el verbo con sus moods', async () => {
    const res = await request(app).get('/api/verbs/anar')
    expect(res.status).toBe(200)
    expect(res.body.infinitive).toBe('anar')
    expect(res.body.moods[0].tenses[0].conjugation[0].forms).toEqual(['vaig'])
  })

  it('404 si no existe', async () => {
    const res = await request(app).get('/api/verbs/noexiste')
    expect(res.status).toBe(404)
    expect(res.body.error).toMatch(/not found/i)
  })
})
