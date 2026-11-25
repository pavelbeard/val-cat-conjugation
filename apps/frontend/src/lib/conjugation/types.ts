import type { MoodBlock } from '@/types'

export type Lang = 'ca' | 'es'

/** Overrides por verbo: { mood: { tense: forms[] } } — cada array son las 6 personas (o las formas no personales). */
export type VerbOverride = Record<string, Record<string, string[]>>

export type { MoodBlock }
