import type { NextFunction, Request, RequestHandler, Response } from 'express'
import { HttpError } from '../errors.js'
import { toAppRequest, type AppRequest } from '../validator/index.js'
import { sendNoContent, sendOk } from './response.js'

/**
 * Método de controller: async function (request) => result.
 * Recibe el AppRequest { params, query, body } ya validado por mw.validator
 * y DEVUELVE el resultado; mw.controller se encarga de la respuesta y los errores.
 */
export type ControllerMethod = (request: AppRequest) => Promise<unknown> | unknown

export interface ControllerOptions {
  status?: number
  /**
   * pagination: true → el método devuelve { data, total } y el middleware responde
   * { data, metadata: { total, limit, skip, page, totalPages } } usando el query validado.
   */
  pagination?: boolean
}

/**
 * Middleware que ejecuta un método de controller y centraliza la respuesta:
 * - pagination: true → { data, metadata } con limit/skip/page del query
 * - result === undefined → 204 No Content
 * - opts.status (p. ej. 201 en creates) → ese status
 * - si no, 200 con el resultado en JSON
 * Cualquier error va a next() → errorHandler.
 */
export function controller(fn: ControllerMethod, opts: ControllerOptions = {}): RequestHandler {
  return async (req: Request, res: Response, next: NextFunction) => {
    try {
      const request = toAppRequest(req)
      const result = await fn(request)

      // estilo BLL: `return error.notFound(...)` → se trata como error HTTP
      if (result instanceof HttpError) {
        next(result)
        return
      }

      if (opts.pagination) {
        const { data, count, total } = result as { data: unknown; count?: number; total?: number }
        const totalCount = Number(count ?? total) || 0
        const q = request.query
        const limit = Math.max(1, Number(q.limit) || 50)
        const page = Math.max(1, Number(q.page) || 1)
        // skip explícito o derivado de page (igual que en el BLL)
        const skip = Math.max(0, q.skip !== undefined && q.skip !== '' ? Number(q.skip) : (page - 1) * limit)
        sendOk(res, {
          data,
          metadata: {
            total: totalCount,
            limit,
            skip,
            page: Math.floor(skip / limit) + 1,
            totalPages: Math.max(1, Math.ceil(totalCount / limit)),
          },
        })
        return
      }

      if (result === undefined) sendNoContent(res)
      else sendOk(res, result, opts.status ?? 200)
    } catch (err) {
      next(err)
    }
  }
}
