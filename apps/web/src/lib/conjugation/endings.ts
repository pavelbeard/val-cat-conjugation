import type { MoodBlock, Pronoun, TenseBlock } from '@/types'
import type { Lang } from './types'

/**
 * Tablas de terminaciones por grupo (-ar, -er/-re, -ir) e idioma.
 * Son datos: revisar contra la normativa AVL (valencià) y RAE (castellà).
 * `stem` = raíz del infinitivo; las formas se construyen como stem + sufijo.
 */

export const PRONOUNS: Record<Lang, string[]> = {
  ca: ['jo', 'tu', 'ell/ella/vostè', 'nosaltres', 'vosaltres', 'ells/elles/vostès'],
  es: ['yo', 'tú', 'él/ella/usted', 'nosotros', 'vosotros', 'ellos/ellas/ustedes'],
}

type Group = 'ar' | 'er' | 'ir'

export function groupOf(infinitive: string): Group {
  const base = infinitive.replace(/-se('n)?$/i, '')
  if (base.endsWith('ar')) return 'ar'
  if (base.endsWith('er') || base.endsWith('re')) return 'er'
  return 'ir'
}

function stemOf(infinitive: string, group: Group): string {
  const base = infinitive.replace(/-se('n)?$/i, '')
  if (group === 'ar') return base.slice(0, -2)
  if (group === 'er') return base.slice(0, -2)
  return base.slice(0, -2) // -ir
}

function tense(tenseName: string, forms: string[], pronouns: string[]): TenseBlock {
  return {
    tense: tenseName,
    conjugation: pronouns.map((pronoun, i) => ({
      pronoun: pronoun as Pronoun,
      forms: forms[i] ? [forms[i]] : [],
    })),
  }
}

function nonPersonal(name: string, forms: string[]): TenseBlock {
  return {
    tense: name,
    conjugation: [{ pronoun: name as Pronoun, forms }],
  }
}

/** Formas perifràsticas del passat (vaig parlar / hube hablado): auxiliar + infinitiu/participi. */
function periphrasticPast(aux: string[], participle: string, infinitive: string, lang: Lang): string[] {
  return aux.map((a) => (lang === 'ca' ? `${a} ${infinitive}` : `${a} ${participle}`))
}

const CA_AUX_PAST = ['vaig', 'vas', 'va', 'vam', 'vau', 'van']
const ES_AUX_PAST = ['he', 'has', 'ha', 'hemos', 'habéis', 'han']

interface GroupTable {
  present: (s: string, inf: string) => string[]
  imperfet: (s: string) => string[]
  passatSimple: (s: string) => string[]
  futur: (s: string, inf: string) => string[]
  condicional: (s: string, inf: string) => string[]
  subjPresent: (s: string) => string[]
  subjImperfet: (s: string) => string[]
  imperatiu: (s: string) => string[]
  gerundi: (s: string) => string
  participi: (s: string) => string[]
}

const CA_TABLES: Record<Group, GroupTable> = {
  ar: {
    present: (s) => [s + 'e', s + 'es', s + 'a', s + 'em', s + 'eu', s + 'en'],
    imperfet: (s) => [s + 'ava', s + 'aves', s + 'ava', s + 'àvem', s + 'àveu', s + 'aven'],
    passatSimple: (s) => [s + 'í', s + 'ares', s + 'à', s + 'àrem', s + 'àreu', s + 'aren'],
    futur: (_s, inf) => [inf + 'é', inf + 'às', inf + 'à', inf + 'em', inf + 'eu', inf + 'an'],
    condicional: (_s, inf) => [inf + 'ia', inf + 'ies', inf + 'ia', inf + 'íem', inf + 'íeu', inf + 'ien'],
    subjPresent: (s) => [s + 'e', s + 'es', s + 'e', s + 'em', s + 'eu', s + 'en'],
    subjImperfet: (s) => [s + 'ara', s + 'ares', s + 'ara', s + 'àrem', s + 'àreu', s + 'aren'],
    imperatiu: (s) => ['', s + 'a', s + 'e', s + 'em', s + 'eu', s + 'en'],
    gerundi: (s) => s + 'ant',
    participi: (s) => [s + 'at', s + 'ada', s + 'ats', s + 'ades'],
  },
  er: {
    present: (s) => [s, s + 's', s, s + 'em', s + 'eu', s + 'en'],
    imperfet: (s) => [s + 'ia', s + 'ies', s + 'ia', s + 'íem', s + 'íeu', s + 'ien'],
    passatSimple: (s) => [s + 'í', s + 'eres', s + 'é', s + 'érem', s + 'éreu', s + 'eren'],
    futur: (s) => [s + 'eré', s + 'eràs', s + 'erà', s + 'erem', s + 'ereu', s + 'eran'],
    condicional: (s) => [s + 'eria', s + 'eries', s + 'eria', s + 'eríem', s + 'eríeu', s + 'erien'],
    subjPresent: (s) => [s + 'a', s + 'es', s + 'a', s + 'am', s + 'au', s + 'an'],
    subjImperfet: (s) => [s + 'era', s + 'eres', s + 'era', s + 'érem', s + 'éreu', s + 'eren'],
    imperatiu: (s) => ['', s, s + 'a', s + 'em', s + 'eu', s + 'en'],
    gerundi: (s) => s + 'ent',
    participi: (s) => [s + 'ut', s + 'uda', s + 'uts', s + 'udes'],
  },
  ir: {
    present: (s) => [s + 'i', s + 'es', s + 'e', s + 'im', s + 'iu', s + 'en'],
    imperfet: (s) => [s + 'ia', s + 'ies', s + 'ia', s + 'íem', s + 'íeu', s + 'ien'],
    passatSimple: (s) => [s + 'í', s + 'ires', s + 'í', s + 'íem', s + 'íeu', s + 'iren'],
    futur: (s) => [s + 'iré', s + 'iràs', s + 'irà', s + 'irem', s + 'ireu', s + 'iran'],
    condicional: (s) => [s + 'iria', s + 'iries', s + 'iria', s + 'iríem', s + 'iríeu', s + 'irien'],
    subjPresent: (s) => [s + 'a', s + 'es', s + 'a', s + 'am', s + 'au', s + 'an'],
    subjImperfet: (s) => [s + 'ira', s + 'ires', s + 'ira', s + 'íem', s + 'íeu', s + 'iren'],
    imperatiu: (s) => ['', s + 'e', s + 'a', s + 'im', s + 'iu', s + 'en'],
    gerundi: (s) => s + 'int',
    participi: (s) => [s + 'it', s + 'ida', s + 'its', s + 'ides'],
  },
}

const ES_TABLES: Record<Group, GroupTable> = {
  ar: {
    present: (s) => [s + 'o', s + 'as', s + 'a', s + 'amos', s + 'áis', s + 'an'],
    imperfet: (s) => [s + 'aba', s + 'abas', s + 'aba', s + 'ábamos', s + 'abais', s + 'aban'],
    passatSimple: (s) => [s + 'é', s + 'aste', s + 'ó', s + 'amos', s + 'asteis', s + 'aron'],
    futur: (_s, inf) => [inf + 'é', inf + 'ás', inf + 'á', inf + 'emos', inf + 'éis', inf + 'án'],
    condicional: (_s, inf) => [inf + 'ía', inf + 'ías', inf + 'ía', inf + 'íamos', inf + 'íais', inf + 'ían'],
    subjPresent: (s) => [s + 'e', s + 'es', s + 'e', s + 'emos', s + 'éis', s + 'en'],
    subjImperfet: (s) => [s + 'ara', s + 'aras', s + 'ara', s + 'áramos', s + 'arais', s + 'aran'],
    imperatiu: (s) => ['', s + 'a', s + 'e', s + 'emos', s + 'ad', s + 'en'],
    gerundi: (s) => s + 'ando',
    participi: (s) => [s + 'ado', s + 'ada', s + 'ados', s + 'adas'],
  },
  er: {
    present: (s) => [s + 'o', s + 'es', s + 'e', s + 'emos', s + 'éis', s + 'en'],
    imperfet: (s) => [s + 'ía', s + 'ías', s + 'ía', s + 'íamos', s + 'íais', s + 'ían'],
    passatSimple: (s) => [s + 'í', s + 'iste', s + 'ió', s + 'imos', s + 'isteis', s + 'ieron'],
    futur: (s) => [s + 'eré', s + 'erás', s + 'erá', s + 'eremos', s + 'eréis', s + 'erán'],
    condicional: (s) => [s + 'ería', s + 'erías', s + 'ería', s + 'eríamos', s + 'eríais', s + 'erían'],
    subjPresent: (s) => [s + 'a', s + 'as', s + 'a', s + 'amos', s + 'áis', s + 'an'],
    subjImperfet: (s) => [s + 'iera', s + 'ieras', s + 'iera', s + 'iéramos', s + 'ierais', s + 'ieran'],
    imperatiu: (s) => ['', s + 'e', s + 'a', s + 'amos', s + 'ed', s + 'an'],
    gerundi: (s) => s + 'iendo',
    participi: (s) => [s + 'ido', s + 'ida', s + 'idos', s + 'idas'],
  },
  ir: {
    present: (s) => [s + 'o', s + 'es', s + 'e', s + 'imos', s + 'ís', s + 'en'],
    imperfet: (s) => [s + 'ía', s + 'ías', s + 'ía', s + 'íamos', s + 'íais', s + 'ían'],
    passatSimple: (s) => [s + 'í', s + 'iste', s + 'ió', s + 'imos', s + 'isteis', s + 'ieron'],
    futur: (s) => [s + 'iré', s + 'irás', s + 'irá', s + 'iremos', s + 'iréis', s + 'irán'],
    condicional: (s) => [s + 'iría', s + 'irías', s + 'iría', s + 'iríamos', s + 'iríais', s + 'irían'],
    subjPresent: (s) => [s + 'a', s + 'as', s + 'a', s + 'amos', s + 'áis', s + 'an'],
    subjImperfet: (s) => [s + 'iera', s + 'ieras', s + 'iera', s + 'iéramos', s + 'ierais', s + 'ieran'],
    imperatiu: (s) => ['', s + 'e', s + 'a', s + 'amos', s + 'id', s + 'an'],
    gerundi: (s) => s + 'iendo',
    participi: (s) => [s + 'ido', s + 'ida', s + 'idos', s + 'idas'],
  },
}

export function buildRegular(infinitive: string, lang: Lang): MoodBlock[] {
  const group = groupOf(infinitive)
  const stem = stemOf(infinitive, group)
  const t = (lang === 'ca' ? CA_TABLES : ES_TABLES)[group]
  const pronouns = PRONOUNS[lang]
  const participle = t.participi(stem)[0]

  const indicatiu: TenseBlock[] = [
    tense('present', t.present(stem, infinitive), pronouns),
    tense('imperfet', t.imperfet(stem), pronouns),
    tense(lang === 'ca' ? 'passat_perifràstic' : 'pretérito_perfecto_compuesto', periphrasticPast(lang === 'ca' ? CA_AUX_PAST : ES_AUX_PAST, participle, infinitive, lang), pronouns),
    tense(lang === 'ca' ? 'passat_simple' : 'pretérito_indefinido', t.passatSimple(stem), pronouns),
    tense('futur', t.futur(stem, infinitive), pronouns),
    tense('condicional', t.condicional(stem, infinitive), pronouns),
  ]
  const subjuntiu: TenseBlock[] = [
    tense('present', t.subjPresent(stem), pronouns),
    tense('imperfet', t.subjImperfet(stem), pronouns),
  ]
  const imperatiu: TenseBlock[] = [tense('present', t.imperatiu(stem), pronouns)]
  const noPersonals: TenseBlock[] = [
    nonPersonal('infinitiu', [infinitive]),
    nonPersonal('gerundi', [t.gerundi(stem)]),
    nonPersonal('participi', t.participi(stem)),
  ]

  return [
    { mood: 'indicatiu', tenses: indicatiu },
    { mood: 'subjuntiu', tenses: subjuntiu },
    { mood: 'imperatiu', tenses: imperatiu },
    { mood: 'formes_no_personals', tenses: noPersonals },
  ]
}
