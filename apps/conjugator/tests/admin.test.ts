import { afterAll, beforeAll, describe, expect, it } from 'vitest'
import request from 'supertest'
import { app } from '../src/app.js'
import { setupTestDb, teardownTestDb } from './helpers.js'

const TOKEN = 'test-token'
process.env.ADMIN_TOKEN = TOKEN
const asAdmin = (r: request.Test) => r.set('Authorization', `Bearer ${TOKEN}`)

beforeAll(setupTestDb)
afterAll(teardownTestDb)

describe('CRUD /api/admin/verbs', () => {
  it('POST sin token → 401 (mw.auth)', async () => {
    const res = await request(app).post('/api/admin/verbs').send({ infinitive: 'x', translation: 'x' })
    expect(res.status).toBe(401)
  })

  it('POST con token inválido → 401', async () => {
    const res = await request(app)
      .post('/api/admin/verbs')
      .set('Authorization', 'Bearer mal')
      .send({ infinitive: 'x', translation: 'x' })
    expect(res.status).toBe(401)
  })

  it('POST crea un verb (201)', async () => {
    const res = await asAdmin(request(app).post('/api/admin/verbs')).send({
      infinitive: 'parlar',
      translation: 'hablar',
    })
    expect(res.status).toBe(201)
    expect(res.body.infinitive).toBe('parlar')
  })

  it('POST valida campos obligatorios (400, middleware validate)', async () => {
    const res = await asAdmin(request(app).post('/api/admin/verbs')).send({ infinitive: 'x' })
    expect(res.status).toBe(400)
    expect(res.body.error).toMatch(/translation/)
  })

  it('POST duplicado → 409 (índice único, errorHandler centralizado)', async () => {
    await asAdmin(request(app).post('/api/admin/verbs')).send({ infinitive: 'duplicat', translation: 'x' })
    const res = await asAdmin(request(app).post('/api/admin/verbs')).send({
      infinitive: 'duplicat',
      translation: 'y',
    })
    expect(res.status).toBe(409)
    expect(res.body.error).toMatch(/duplicate/i)
  })

  it('GET lista todos los verbs (público, sin auth)', async () => {
    const res = await request(app).get('/api/admin/verbs')
    expect(res.status).toBe(200)
    expect(res.body.map((v: { infinitive: string }) => v.infinitive)).toContain('parlar')
  })

  it('PUT con body que no es objeto → 400 (zod)', async () => {
    const res = await asAdmin(request(app).put('/api/admin/verbs/parlar')).send([1, 2])
    expect(res.status).toBe(400)
  })

  it('PUT actualiza (200) y 404 si no existe', async () => {
    const ok = await asAdmin(request(app).put('/api/admin/verbs/parlar')).send({
      translation: 'hablar (val.)',
    })
    expect(ok.status).toBe(200)
    expect(ok.body.translation).toBe('hablar (val.)')

    const ko = await asAdmin(request(app).put('/api/admin/verbs/noexiste')).send({ translation: 'x' })
    expect(ko.status).toBe(404)
  })

  it('DELETE borra (204) y 404 si no existe', async () => {
    const ok = await asAdmin(request(app).delete('/api/admin/verbs/parlar'))
    expect(ok.status).toBe(204)

    const ko = await asAdmin(request(app).delete('/api/admin/verbs/parlar'))
    expect(ko.status).toBe(404)
  })
})
