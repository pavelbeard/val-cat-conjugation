import type { Request, RequestHandler } from 'express'
import {
  buildRequestSchema,
  isDescriptor,
  validator,
  type RequestDescriptor,
} from './dsl.js'
import { getValidatedQuery, isSchema, validateRequest, type ValidatedRequest, type Validator, type ValidatorFn } from './request.js'

export { validator, buildRequestSchema, isDescriptor, type FieldBuilder, type RequestDescriptor } from './dsl.js'
export {
  validateRequest,
  formatIssues,
  isSchema,
  getValidatedQuery,
  type ValidatedRequest,
  type Validator,
  type ValidatorFn,
} from './request.js'

/**
 * Middleware validador (expuesto como mw.validator en middlewares):
 * - undefined → sin validación (p. ej. list)
 * - descriptor DSL { params, query, body } → se convierte a zod y se valida
 * - schema zod → validateRequest directo
 * - función legacy → se ejecuta
 * Los errores van a errorHandler.
 */
export function validatorMw(validate?: Validator): RequestHandler {
  return (req: Request, _res, next) => {
    try {
      if (!validate) {
        next()
        return
      }
      if (isSchema(validate)) {
        ;(req as ValidatedRequest).validated = validateRequest(validate, req) as ValidatedRequest['validated']
      } else if (typeof validate === 'function') (validate as ValidatorFn)(req)
      else if (isDescriptor(validate)) {
        ;(req as ValidatedRequest).validated = validateRequest(buildRequestSchema(validate), req) as ValidatedRequest['validated']
      } else next(new Error('Invalid validator'))
      next()
    } catch (err) {
      next(err)
    }
  }
}
