import type { NextFunction, Request, Response } from 'express'
import { HttpError, NotFoundError } from '../errors.js'

/** Cualquier ruta no registrada cae aquí como 404 JSON. */
export function notFoundHandler(req: Request, _res: Response, next: NextFunction) {
  next(new NotFoundError(`Route not found: ${req.method} ${req.originalUrl}`))
}

/** Middleware de errores centralizado: traduce errores a respuestas HTTP. */
export function errorHandler(err: unknown, _req: Request, res: Response, _next: NextFunction) {
  if (err instanceof HttpError) {
    res.status(err.status).json({ error: err.message })
    return
  }
  // Errores de Mongoose
  if (typeof err === 'object' && err !== null && 'code' in err && (err as { code: number }).code === 11000) {
    res.status(409).json({ error: 'Duplicate key' })
    return
  }
  if (err instanceof Error && err.name === 'ValidationError') {
    res.status(400).json({ error: err.message })
    return
  }
  console.error(err)
  res.status(500).json({ error: 'Internal server error' })
}
