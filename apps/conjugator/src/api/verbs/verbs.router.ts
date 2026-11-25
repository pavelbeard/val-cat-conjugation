import { Router } from 'express'
import { mw } from '@vcc/api-builder'
import { verbsController } from './verbs.controller.js'
import { verbsValidator } from './verbs.validator.js'

/**
 * Rutas del dominio verbs (montadas en /api/verbs desde src/router.ts):
 * - GET /search (paginado, con q/form/letter/sort/page/limit/skip) → { data, metadata }
 * - GET /:infinitive → verb completo
 * (No hay list-all: la paginación siempre va con la búsqueda para no cargar todos los verbs.)
 */
const router = Router()

router.get(
  '/search',
  mw.validator(verbsValidator.search),
  mw.controller(verbsController.search, { pagination: true }),
)
router.get('/:infinitive', mw.validator(verbsValidator.get), mw.controller(verbsController.get))

export default router
