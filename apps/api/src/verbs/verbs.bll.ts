import { NotFoundError } from '../errors.js'
import { verbsRepository, type VerbsRepository, type VerbFilter } from './verbs.repository.js'

const escapeRegExp = (s: string) => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')

export interface SearchParams {
  q?: string
  form?: string
  letter?: string
  sort?: string
  page?: number
  limit?: number
  skip?: number
}

/** Lógica de negocio de verbs. Recibe el repository por inyección (testeable). */
export function createVerbsBll(repo: VerbsRepository = verbsRepository) {
  return {
    /** Búsqueda + paginación. Devuelve { data, total }; mw.controller({ pagination: true }) monta { data, metadata }. */
    async search(params: SearchParams) {
      const filter: VerbFilter = {}

      const q = params.q?.trim()
      if (q) {
        const rx = new RegExp(escapeRegExp(q), 'i')
        filter.$or = [{ infinitive: rx }, { translation: rx }]
      }
      const form = params.form?.trim()
      if (form) filter.form = form
      const letter = params.letter?.trim()
      if (letter) filter.letter = letter

      const limit = Math.max(1, Math.floor(params.limit ?? 50))
      const skip = Math.max(0, Math.floor(params.skip ?? (Math.max(1, params.page ?? 1) - 1) * limit))
      const sort: Record<string, 1 | -1> =
        params.sort === 'clicks' ? { clicks: -1, infinitive: 1 } : { infinitive: 1 }

      return repo.searchVerbs(filter, { limit, skip, sort })
    },

    async getVerb(infinitive: string) {
      const verb = await repo.findByInfinitive(infinitive)
      if (!verb) throw new NotFoundError(`Verb not found: ${infinitive}`)
      return verb
    },
  }
}

export type VerbsBll = ReturnType<typeof createVerbsBll>
