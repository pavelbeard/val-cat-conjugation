import type { Request } from 'express'
import { describe, expect, it } from 'vitest'
import { BadRequestError } from '../src/errors.js'
import { buildRequestSchema, validateRequest, validator } from '../src/validator/index.js'

const fakeReq = (parts: { params?: object; query?: object; body?: object }) =>
  ({ params: {}, query: {}, body: {}, ...parts }) as unknown as Request

describe('DSL de validadores (src/validator)', () => {
  it('string.required() exige presencia y no vacío, con mensaje estándar', () => {
    const schema = buildRequestSchema({
      query: { form: validator.string.required() },
    })
    expect(() => validateRequest(schema, fakeReq({}))).toThrowError(/query param "form" is required/)
    expect(() => validateRequest(schema, fakeReq({ query: { form: '' } }))).toThrowError(/required/)
    expect(() => validateRequest(schema, fakeReq({ query: { form: 'vaig' } }))).not.toThrow()
  })

  it('stringRequired (shorthand) en params', () => {
    const schema = buildRequestSchema({
      params: { infinitive: validator.stringRequired },
    })
    expect(() => validateRequest(schema, fakeReq({}))).toThrowError(/param "infinitive" is required/)
    expect(() => validateRequest(schema, fakeReq({ params: { infinitive: 'anar' } }))).not.toThrow()
  })

  it('bool.notRequired().default(false) parsea "true" → true y ausente → false', () => {
    const schema = buildRequestSchema({
      query: { verbose: validator.bool.notRequired().default(false) },
    })
    expect(validateRequest(schema, fakeReq({ query: { verbose: 'true' } }))).toMatchObject({
      query: { verbose: true },
    })
    expect(validateRequest(schema, fakeReq({}))).toMatchObject({ query: { verbose: false } })
  })

  it('number en query llega como string y se coerce', () => {
    const schema = buildRequestSchema({
      query: { limit: validator.number.notRequired() },
    })
    expect(validateRequest(schema, fakeReq({ query: { limit: '25' } }))).toMatchObject({
      query: { limit: 25 },
    })
  })

  it('object.required() como body rechaza arrays y exige objeto', () => {
    const schema = buildRequestSchema({
      params: { infinitive: validator.stringRequired },
      body: validator.object.required(),
    })
    expect(() =>
      validateRequest(schema, fakeReq({ params: { infinitive: 'parlar' }, body: [1, 2] })),
    ).toThrowError(/body/)
    expect(() =>
      validateRequest(schema, fakeReq({ params: { infinitive: 'parlar' }, body: { translation: 'hablar' } })),
    ).not.toThrow()
  })

  it('el error es BadRequestError (400) con el path del issue', () => {
    const schema = buildRequestSchema({ query: { form: validator.string.required() } })
    try {
      validateRequest(schema, fakeReq({}))
      expect.unreachable()
    } catch (err) {
      expect(err).toBeInstanceOf(BadRequestError)
      expect((err as BadRequestError).status).toBe(400)
      expect((err as Error).message).toBe('query.form: query param "form" is required')
    }
  })

  it('los shapes parciales no rompen claves extra (loose)', () => {
    const schema = buildRequestSchema({ query: { form: validator.string.required() } })
    expect(() =>
      validateRequest(schema, fakeReq({ query: { form: 'vaig', extra: 1 }, params: { x: 'y' } })),
    ).not.toThrow()
  })
})
