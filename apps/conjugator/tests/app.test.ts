import { describe, expect, it } from 'vitest'
import request from 'supertest'
import { app } from '../src/app.js'

describe('middlewares globales', () => {
  it('ruta desconocida → 404 JSON centralizado', async () => {
    const res = await request(app).get('/api/no-existe')
    expect(res.status).toBe(404)
    expect(res.body.error).toMatch(/not found/i)
  })

  it('health responde con formato estándar', async () => {
    const res = await request(app).get('/api/health')
    expect(res.status).toBe(200)
    expect(res.body).toEqual({ status: 'ok' })
  })
})
