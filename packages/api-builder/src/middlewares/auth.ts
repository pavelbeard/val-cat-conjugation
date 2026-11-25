import type { Request, RequestHandler } from 'express'
import { error } from '../errors.js'

/**
 * Autorización (de momento solo para /api/admin de escritura):
 * exige cabecera `Authorization: Bearer <ADMIN_TOKEN>` (env).
 * Si es válida, deja el payload en `request.auth` para los controllers:
 *   const { auth } = request
 */
export const auth: RequestHandler = (req: Request, _res, next) => {
  const expected = process.env.ADMIN_TOKEN
  if (!expected) {
    next(error.http(500, 'ADMIN_TOKEN is not set'))
    return
  }
  const header = req.headers.authorization
  const token = header?.startsWith('Bearer ') ? header.slice('Bearer '.length) : undefined
  if (!token || token !== expected) {
    next(error.unauthorized('Missing or invalid Bearer token'))
    return
  }
  ;(req as Request & { auth?: unknown }).auth = { token }
  next()
}
