export type Pronoun =
  | 'jo'
  | 'tu'
  | 'ell/(-a)/vostè'
  | 'nosaltres'
  | 'vosaltres'
  | 'ells/(-es)/vostès'
  | 'infinitiu'
  | 'infinitiu_compost'
  | 'gerundi'
  | 'gerundi_compost'
  | 'participi'

export interface ConjugationForm {
  pronoun: Pronoun
  forms: string[]
  variation_types?: (string | null)[] | null
  translation?: string
}

export interface TenseBlock {
  tense: string
  conjugation: ConjugationForm[]
}

export interface MoodBlock {
  mood: string
  tenses: TenseBlock[]
}

export interface Verb {
  _id: string
  infinitive: string
  moods?: MoodBlock[]
  translation: string
  created_at: string
  updated_at?: string
  clicks?: number
}

export interface PaginationMetadata {
  total: number
  limit: number
  skip: number
  page: number
  totalPages: number
}

export interface Paginated<T> {
  data: T[]
  metadata: PaginationMetadata
}
