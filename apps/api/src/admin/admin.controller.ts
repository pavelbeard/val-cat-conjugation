import type { Request } from 'express'
import { createAdminBll, type AdminBll } from './admin.bll.js'

/**
 * Controller del admin: métodos async que DEVUELVEN el resultado.
 * mw.controller envía la respuesta (create → 201 vía opts, remove → 204 si devuelve undefined).
 */
export function createAdminController(bll: AdminBll = createAdminBll()) {
  return {
    list: async () => bll.listVerbs(),

    create: async (req: Request) => bll.createVerb(req.body as Record<string, unknown>),

    update: async (req: Request) =>
      bll.updateVerb(decodeURIComponent(req.params.infinitive), req.body as Record<string, unknown>),

    remove: async (req: Request) => {
      await bll.deleteVerb(decodeURIComponent(req.params.infinitive))
      // devolver undefined → 204 No Content
    },
  }
}

export const adminController = createAdminController()
export type AdminController = ReturnType<typeof createAdminController>
