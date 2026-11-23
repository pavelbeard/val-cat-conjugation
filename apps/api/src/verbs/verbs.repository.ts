import { Verb } from '../models/verb.js'

/** Filtro de dominio para búsqueda de verbs (el BLL lo construye, aquí se traduce a Mongo). */
export interface VerbFilter {
  $or?: Array<Record<string, RegExp>>
  form?: string
  letter?: string
}

const escapeRegExp = (s: string) => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')

function toMongoQuery(filter: VerbFilter): Record<string, unknown> {
  const query: Record<string, unknown> = {}
  if (filter.$or) query.$or = filter.$or
  if (filter.form) query['moods.tenses.conjugation.forms'] = filter.form
  if (filter.letter) {
    query.infinitive = { $regex: `^${escapeRegExp(filter.letter)}`, $options: 'i' }
  }
  return query
}

/** Acceso a la BBDD para verbs. Toda query de Mongoose vive aquí. */
export const verbsRepository = {
  /** Búsqueda paginada: devuelve { data, total } para que mw.controller monte la metadata. */
  async searchVerbs(
    filter: VerbFilter,
    opts: { limit: number; skip: number; sort: Record<string, 1 | -1> },
  ) {
    const query = toMongoQuery(filter)
    const [data, total] = await Promise.all([
      Verb.find(query, { infinitive: 1, translation: 1, clicks: 1 })
        .sort(opts.sort)
        .skip(opts.skip)
        .limit(opts.limit)
        .lean(),
      Verb.countDocuments(query),
    ])
    return { data, total }
  },

  findByInfinitive(infinitive: string) {
    return Verb.findOne({ infinitive }).lean()
  },
}

export type VerbsRepository = typeof verbsRepository
