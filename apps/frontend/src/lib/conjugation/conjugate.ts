import type { MoodBlock } from '@/types'
import { buildRegular } from './endings'
import type { Lang, VerbOverride } from './types'
import irregularsCa from './irregulars.ca.json'
import irregularsEs from './irregulars.es.json'

const OVERRIDES: Record<Lang, Record<string, VerbOverride>> = {
  ca: irregularsCa as Record<string, VerbOverride>,
  es: irregularsEs as Record<string, VerbOverride>,
}

/** Funde los overrides sobre la conjugación regular: mood.tense.forms se reemplaza entero. */
function applyOverrides(base: MoodBlock[], override: VerbOverride): MoodBlock[] {
  return base.map((moodBlock) => {
    const moodOver = override[moodBlock.mood]
    if (!moodOver) return moodBlock
    return {
      ...moodBlock,
      tenses: moodBlock.tenses.map((t) => {
        const forms = moodOver[t.tense]
        if (!forms) return t
        return {
          ...t,
          conjugation: t.conjugation.map((c, i) =>
            forms[i] !== undefined ? { ...c, forms: [forms[i]] } : c,
          ),
        }
      }),
    }
  })
}

/**
 * Conjuga un verbo por reglas (grupo -ar / -er-re / -ir) aplicando después
 * la lista de overrides de irregulares. Lang 'ca' = valencià (AVL), 'es' = castellà.
 */
export function conjugate(infinitive: string, lang: Lang = 'ca'): MoodBlock[] {
  const base = buildRegular(infinitive, lang)
  const key = infinitive.toLowerCase().replace(/-se('n)?$/i, '')
  const override = OVERRIDES[lang][key] ?? OVERRIDES[lang][infinitive.toLowerCase()]
  return override ? applyOverrides(base, override) : base
}

/** Busca una forma concreta: formOf(moods, 'indicatiu', 'present', 0) → primera persona. */
export function formOf(moods: MoodBlock[], mood: string, tenseName: string, person: number): string {
  const t = moods.find((m) => m.mood === mood)?.tenses.find((t) => t.tense === tenseName)
  return t?.conjugation[person]?.forms[0] ?? ''
}
