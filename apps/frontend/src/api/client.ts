import type { Paginated, Verb } from '@/types'

const BASE = import.meta.env.VITE_API_URL ?? '/api'

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...init,
  })
  if (!res.ok) throw new Error(`API error ${res.status}: ${await res.text()}`)
  return res.json() as Promise<T>
}

export interface SearchVerbsParams {
  q?: string
  form?: string
  translation?: string
  letter?: string
  sort?: 'infinitive' | 'clicks'
  page?: number
  limit?: number
  skip?: number
}

/** Búsqueda paginada de verbs: GET /api/verbs/search → { data, metadata }. */
export const searchVerbs = (params: SearchVerbsParams) => {
  const usp = new URLSearchParams()
  for (const [k, v] of Object.entries(params)) {
    if (v !== undefined && v !== '') usp.set(k, String(v))
  }
  return request<Paginated<Verb>>(`/verbs/search?${usp.toString()}`)
}

export const getVerb = (infinitive: string) =>
  request<Verb>(`/verbs/${encodeURIComponent(infinitive)}`)
