export interface Database__ConjugationForm {
  pronoun:
    | 'jo'
    | 'tu'
    | 'ell/(-a)/vostè'
    | 'nosaltres'
    | 'vosaltres'
    | 'ells/(-es)/vostès'
    // Forms non personal
    | 'infinitiu'
    | 'infinitiu_compost'
    | 'gerundi'
    | 'gerundi_compost'
    | 'participi'
  forms: string[]
  variation_types?: (string | null)[] | null
  translation?: string
}

export interface Database__TenseBlock {
  tense: string
  conjugation: Database__ConjugationForm[]
}

export interface Database__MoodBlock {
  mood: string
  tenses: Database__TenseBlock[]
}

export interface Database__VerbOutput {
  _id: string
  infinitive: string
  moods?: Database__MoodBlock[]
  translation: string
  source?: string
  created_at: string
  updated_at: string
}

export type Conjugation = {
  pronoun:
    | 'jo'
    | 'tu'
    | 'ell/(-a)/vostè'
    | 'nosaltres'
    | 'vosaltres'
    | 'ells/(-es)/vostès'
  variation_types:
    | { word: string; dialect?: 'cent.' | 'val.' | 'bal.' }[]
    | string
  translation?: string
}

export type Mode = {
  tense: string
  conjugations: Conjugation[]
}

export type Tenses = {
  present: Mode
  imperfet: Mode
  perfet: Mode
  plusquamperfet: Mode
  passat_simple: Mode
  passat_perifràstic: Mode
  passat_anterior: Mode
  passat_anterior_perifràstic: Mode
  futur: Mode
  futur_perfet: Mode
  subjuntiu_present: Mode
  subjuntiu_imperfet: Mode
  subjuntiu_perfet: Mode
  subjuntiu_plusquamperfet: Mode
  condicional_simple: Mode
  condicional_perfet: Mode
  imperatiu: Imperatiu
}

export type TenseNames = {
  [key in keyof Tenses]: string
}

export type Imperatiu = Omit<Conjugation['pronoun'], 'jo'> & {
  variation: { word: string; dialect?: 'cent.' | 'val.' | 'bal.' }[] | string
  translation?: string
}
