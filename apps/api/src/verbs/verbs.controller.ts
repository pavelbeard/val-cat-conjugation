import type { Request } from 'express'
import { getValidatedQuery } from '../validator/index.js'
import { createVerbsBll, type VerbsBll, type SearchParams } from './verbs.bll.js'

const asString = (v: unknown) => (typeof v === 'string' && v !== '' ? v : undefined)
const asNumber = (v: unknown) => (typeof v === 'number' && Number.isFinite(v) ? v : undefined)

/**
 * Controller: métodos async que DEVUELVEN el resultado.
 * mw.controller (en el router) se encarga de la respuesta y los errores;
 * con { pagination: true } envuelve { data, total } en { data, metadata }.
 */
export function createVerbsController(bll: VerbsBll = createVerbsBll()) {
  return {
    search: async (req: Request): Promise<{ data: unknown; total: number }> => {
      const q = getValidatedQuery(req)
      const params: SearchParams = {
        q: asString(q.q),
        form: asString(q.form),
        letter: asString(q.letter),
        sort: asString(q.sort),
        page: asNumber(q.page),
        limit: asNumber(q.limit),
        skip: asNumber(q.skip),
      }
      return bll.search(params)
    },

    get: async (req: Request) => bll.getVerb(decodeURIComponent(req.params.infinitive)),
  }
}

export const verbsController = createVerbsController()
export type VerbsController = ReturnType<typeof createVerbsController>
