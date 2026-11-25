import type { Request } from 'express'
import type { AxiosInstance } from 'axios'
import { z } from 'zod'
import { BadRequestError } from '../errors.js'
import { AxiosBuilder } from '../axios.js'
import type { RequestDescriptor } from './dsl.js'

/** Validador como función legacy (req) => void que lanza HttpError. */
export type ValidatorFn = (req: Request) => void

/** Validador: descriptor DSL ({params, query, body}), schema zod o función legacy. */
export type Validator = ValidatorFn | z.ZodTypeAny | RequestDescriptor

export function isSchema(v: unknown): v is z.ZodTypeAny {
  return typeof (v as z.ZodTypeAny)?.safeParse === 'function'
}

/** Formatea los issues de zod como "path: mensaje; ...". */
export function formatIssues(error: z.ZodError): string {
  return error.issues.map((i) => `${i.path.join('.') || 'request'}: ${i.message}`).join('; ')
}

/** Request con los datos ya validados/parseados por mw.validator (con defaults aplicados). */
export interface ValidatedRequest extends Request {
  validated?: { params?: Record<string, unknown>; query?: Record<string, unknown>; body?: unknown }
}

/**
 * Request plano que reciben los controllers:
 *   const { query, headers, auth, params, axios } = request
 * - params/query/body: ya validados (con defaults) si pasó por mw.validator, crudos si no
 * - headers: cabeceras HTTP
 * - auth: payload de autenticación (lo poblará un middleware de auth; undefined de momento)
 * - axios: instancia axios con los headers de la petición entrante ya recogidos
 */
export interface AppRequest {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  params: Record<string, any>
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  query: Record<string, any>
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  body: any
  headers: Record<string, unknown>
  auth: unknown
  axios: AxiosInstance
}

/** Parsea el request contra el schema; lanza BadRequestError (400) con el detalle si falla. Devuelve los datos parseados. */
export function validateRequest(schema: z.ZodTypeAny, req: Request) {
  const result = schema.safeParse({ params: req.params, query: req.query, body: req.body })
  if (!result.success) throw new BadRequestError(formatIssues(result.error))
  return result.data
}

/** decodeURIComponent seguro (si falla, devuelve el valor crudo). */
function safeDecode(s: string): string {
  try {
    return decodeURIComponent(s)
  } catch {
    return s
  }
}

/** Decodifica los params de la ruta (p. ej. infinitive con caracteres escapados). */
function decodeParams(params: Record<string, unknown>): Record<string, unknown> {
  const out: Record<string, unknown> = {}
  for (const [key, value] of Object.entries(params)) {
    out[key] = typeof value === 'string' ? safeDecode(value) : value
  }
  return out
}

/** Construye el AppRequest a partir del req de Express (ya validado o no). */
export function toAppRequest(req: Request): AppRequest {
  const v = (req as ValidatedRequest).validated
  return {
    params: decodeParams((v?.params ?? req.params) as Record<string, string>),
    query: (v?.query ?? req.query) as Record<string, never>,
    body: v?.body ?? req.body,
    headers: req.headers as Record<string, unknown>,
    auth: (req as Request & { auth?: unknown }).auth,
    axios: AxiosBuilder.fromRequest(req).build(),
  }
}
