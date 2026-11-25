import { error } from '@vcc/api-builder'
import {
  verbsRepository,
  type SearchOptions,
  type SearchQuery,
} from './verbs.repository.js'

export interface SearchParams {
  q?: string
  form?: string
  letter?: string
  sort?: string
  page?: number
  limit?: number
  skip?: number
}

/**
 * Lógica de negocio de verbs (funciones async planas con el repository importado).
 * Devuelve { data, count }; mw.controller({ pagination: true }) monta { data, metadata }.
 */
export async function search(params: SearchParams) {
  const query: SearchQuery = {
    q: params.q?.trim() || undefined,
    form: params.form?.trim() || undefined,
    letter: params.letter?.trim() || undefined,
  }
  const limit = Math.max(1, Math.floor(params.limit ?? 50))
  const options: SearchOptions = {
    limit,
    skip: Math.max(0, Math.floor(params.skip ?? (Math.max(1, params.page ?? 1) - 1) * limit)),
    sort: params.sort === 'clicks' ? { clicks: -1, infinitive: 1 } : { infinitive: 1 },
  }
  const [data, count] = await Promise.all([
    verbsRepository.search(query, options),
    verbsRepository.count(query),
  ])
  return { data, count }
}

export async function getVerb(infinitive: string) {
  const verb = await verbsRepository.findByInfinitive(infinitive)
  if (!verb) return error.notFound(`Verb not found: ${infinitive}`)
  return verb
}

export const verbsBll = { search, getVerb }
