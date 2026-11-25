import { db, contains, escapeRegExp, orRegex, startsWith, toMongoQuery } from '@vcc/api-builder'

const COLLECTION = 'verbs'

/** Query de dominio para búsqueda de verbs (el BLL la construye). */
export interface SearchQuery {
  q?: string
  form?: string
  letter?: string
  translation?: string
}

export interface SearchOptions {
  limit: number
  skip: number
  sort: Record<string, 1 | -1>
  /** Si se indica, los infinitivos que empiezan por este término van primero (relevancia). */
  startsWithValue?: string
}

/** Compone la query de Mongo a partir de la query de dominio usando helpers genéricos de lib/db. */
function buildQuery({ q, form, letter, translation }: SearchQuery): Record<string, unknown> {
  return toMongoQuery({
    $or: q ? orRegex(['infinitive', 'translation'], q).$or : undefined,
    'moods.tenses.conjugation.forms': form,
    infinitive: letter ? startsWith(letter) : undefined,
    translation: translation ? contains(translation) : undefined,
  })
}

/**
 * Acceso a la BBDD para verbs. Toda query de Mongo pasa por db.getCollection(COLLECTION).
 * Con startsWithValue usa aggregate para rankear: primero los que empiezan por el término.
 */
export async function search(query: SearchQuery, options: SearchOptions) {
  const collection = db.getCollection(COLLECTION)
  const mongoQuery = buildQuery(query)

  if (options.startsWithValue) {
    return collection
      .aggregate([
        { $match: mongoQuery },
        {
          $addFields: {
            _relevance: {
              $cond: [
                {
                  $regexMatch: {
                    input: '$infinitive',
                    regex: `^${escapeRegExp(options.startsWithValue)}`,
                    options: 'i',
                  },
                },
                0,
                1,
              ],
            },
          },
        },
        { $sort: { _relevance: 1, ...options.sort } },
        { $skip: options.skip },
        { $limit: options.limit },
        { $project: { infinitive: 1, translation: 1, clicks: 1 } },
      ])
      .toArray()
  }

  return collection
    .find(mongoQuery, { projection: { infinitive: 1, translation: 1, clicks: 1 } })
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
