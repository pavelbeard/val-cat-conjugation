import type { Response } from 'express'

/** Respuestas centralizadas: un único sitio para códigos y formato JSON. */
export function sendOk<T>(res: Response, data: T, status = 200) {
  res.status(status).json(data)
}

export function sendCreated<T>(res: Response, data: T) {
  sendOk(res, data, 201)
}

export function sendNoContent(res: Response) {
  res.status(204).end()
}
