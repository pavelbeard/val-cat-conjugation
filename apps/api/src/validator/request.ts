import type { Request } from 'express'
import { z } from 'zod'
import { BadRequestError } from '../errors.js'
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

/** Parsea el request contra el schema; lanza BadRequestError (400) con el detalle si falla. Devuelve los datos parseados. */
export function validateRequest(schema: z.ZodTypeAny, req: Request) {
  const result = schema.safeParse({ params: req.params, query: req.query, body: req.body })
  if (!result.success) throw new BadRequestError(formatIssues(result.error))
  return result.data
}

/** Query ya validada (con defaults), o la cruda si no pasó por validador. */
export function getValidatedQuery(req: Request): Record<string, unknown> {
  return ((req as ValidatedRequest).validated?.query ?? req.query) as Record<string, unknown>
}
