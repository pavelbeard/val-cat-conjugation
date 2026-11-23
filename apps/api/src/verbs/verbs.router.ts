import { Router } from 'express'
import mw from '../middlewares/index.js'
import { createVerbsController, verbsController, type VerbsController } from './verbs.controller.js'
import { verbsValidator } from './verbs.validator.js'

/**
 * Rutas de /api/verbs:
 * - GET /search (paginado, con q/form/letter/sort/page/limit/skip) → { data, metadata }
 * - GET /:infinitive → verb completo
 * (No hay list-all: la paginación siempre va con la búsqueda para no cargar todos los verbs.)
 */
export function createVerbsRouter(
  controller: VerbsController = verbsController,
  validator = verbsValidator,
) {
  const router = Router()
  router.get(
    '/search',
    mw.validator(validator.search),
    mw.controller(controller.search, { pagination: true }),
  )
  router.get('/:infinitive', mw.validator(validator.get), mw.controller(controller.get))
  return router
}
