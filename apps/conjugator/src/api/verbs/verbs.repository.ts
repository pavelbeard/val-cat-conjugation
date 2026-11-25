import { db, orRegex, startsWith, toMongoQuery } from '@vcc/api-builder'

const COLLECTION = 'verbs'

/** Query de dominio para búsqueda de verbs (el BLL la construye). */
export interface SearchQuery {
  q?: string
  form?: string
  letter?: string
}

export interface SearchOptions {
  limit: number
  skip: number
  sort: Record<string, 1 | -1>
}

/** Compone la query de Mongo a partir de la query de dominio usando helpers genéricos de lib/db. */
function buildQuery({ q, form, letter }: SearchQuery): Record<string, unknown> {
  return toMongoQuery({
    $or: q ? orRegex(['infinitive', 'translation'], q).$or : undefined,
    'moods.tenses.conjugation.forms': form,
    infinitive: letter ? startsWith(letter) : undefined,
  })
}

/**
 * Acceso a la BBDD para verbs. Toda query de Mongo pasa por db.getCollection(COLLECTION).
 */
export async function search(query: SearchQuery, options: SearchOptions) {
  return db
    .getCollection(COLLECTION)
    .find(buildQuery(query), { projection: { infinitive: 1, translation: 1, clicks: 1 } })
    .sort(options.sort)
    .skip(options.skip)
    .limit(options.limit)
    .toArray()
}

export async function count(query: SearchQuery) {
  return db.getCollection(COLLECTION).countDocuments(buildQuery(query))
}

export async function findByInfinitive(infinitive: string) {
  return db.getCollection(COLLECTION).findOne({ infinitive })
}

export const verbsRepository = { search, count, findByInfinitive }
export type VerbsRepository = typeof verbsRepository
