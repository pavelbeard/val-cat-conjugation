import express from 'express'
import cors from 'cors'
import { errorHandler, notFoundHandler } from './middlewares/index.js'
import { createVerbsRouter } from './verbs/verbs.router.js'
import { createAdminRouter } from './admin/admin.router.js'

/** App Express montada por separado del listen, para poder testearla con supertest. */
export function createApp() {
  const app = express()
  app.use(cors())
  app.use(express.json({ limit: '5mb' }))

  app.get('/api/health', (_req, res) => res.json({ status: 'ok' }))
  app.use('/api/verbs', createVerbsRouter())
  app.use('/api/admin', createAdminRouter())

  // Cadena global: rutas desconocidas → 404; cualquier error → errorHandler
  app.use(notFoundHandler)
  app.use(errorHandler)

  return app
}

export const app = createApp()
