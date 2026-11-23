import { Router } from 'express'
import mw from '../middlewares/index.js'
import { adminController, createAdminController, type AdminController } from './admin.controller.js'
import { adminValidator } from './admin.validator.js'

// TODO: proteger con auth de staff (Bearer token / sesión) antes de producción

/** Rutas de /api/admin: mw.validator(validator.x) -> mw.controller(controller.x). */
export function createAdminRouter(
  controller: AdminController = adminController,
  validator = adminValidator,
) {
  const router = Router()
  router.get('/verbs', mw.validator(validator.list), mw.controller(controller.list))
  router.post('/verbs', mw.validator(validator.create), mw.controller(controller.create, { status: 201 }))
  router.put('/verbs/:infinitive', mw.validator(validator.update), mw.controller(controller.update))
  router.delete('/verbs/:infinitive', mw.validator(validator.remove), mw.controller(controller.remove))
  return router
}
