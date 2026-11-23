import { describe, expect, it } from 'vitest'
import { conjugate, formOf } from './conjugate'

describe('motor de conjugació (valencià)', () => {
  const parlar = conjugate('parlar', 'ca')

  it('present amb -e en primera persona (AVL)', () => {
    expect(formOf(parlar, 'indicatiu', 'present', 0)).toBe('parle')
    expect(formOf(parlar, 'indicatiu', 'present', 2)).toBe('parla')
    expect(formOf(parlar, 'indicatiu', 'present', 3)).toBe('parlem')
  })

  it('passat perifràstic: vaig parlar (normatiu en valencià)', () => {
    expect(formOf(parlar, 'indicatiu', 'passat_perifràstic', 0)).toBe('vaig parlar')
    expect(formOf(parlar, 'indicatiu', 'passat_perifràstic', 2)).toBe('va parlar')
  })

  it('passat simple, futur, condicional, subjuntiu, imperatiu', () => {
    expect(formOf(parlar, 'indicatiu', 'passat_simple', 0)).toBe('parlí')
    expect(formOf(parlar, 'indicatiu', 'futur', 0)).toBe('parlaré')
    expect(formOf(parlar, 'indicatiu', 'condicional', 0)).toBe('parlaria')
    expect(formOf(parlar, 'subjuntiu', 'present', 0)).toBe('parle')
    expect(formOf(parlar, 'subjuntiu', 'imperfet', 0)).toBe('parlara')
    expect(formOf(parlar, 'imperatiu', 'present', 1)).toBe('parla')
    expect(formOf(parlar, 'imperatiu', 'present', 2)).toBe('parle')
  })

  it('formes no personals', () => {
    expect(formOf(parlar, 'formes_no_personals', 'infinitiu', 0)).toBe('parlar')
    expect(formOf(parlar, 'formes_no_personals', 'gerundi', 0)).toBe('parlant')
    expect(formOf(parlar, 'formes_no_personals', 'participi', 0)).toBe('parlat')
  })

  it('irregular anar: vaig / va', () => {
    const anar = conjugate('anar', 'ca')
    expect(formOf(anar, 'indicatiu', 'present', 0)).toBe('vaig')
    expect(formOf(anar, 'indicatiu', 'present', 2)).toBe('va')
    expect(formOf(anar, 'imperatiu', 'present', 1)).toBe('vés')
  })

  it('irregular ser: sóc', () => {
    expect(formOf(conjugate('ser', 'ca'), 'indicatiu', 'present', 0)).toBe('sóc')
  })

  it('irregular córrer: corr (apòcope)', () => {
    expect(formOf(conjugate('córrer', 'ca'), 'indicatiu', 'present', 0)).toBe('corr')
  })
})

describe('motor de conjugación (español)', () => {
  const hablar = conjugate('hablar', 'es')

  it('present: hablo', () => {
    expect(formOf(hablar, 'indicatiu', 'present', 0)).toBe('hablo')
    expect(formOf(hablar, 'indicatiu', 'present', 3)).toBe('hablamos')
  })

  it('pretérito indefinido: hablé', () => {
    expect(formOf(hablar, 'indicatiu', 'pretérito_indefinido', 0)).toBe('hablé')
  })

  it('perífrasis: he hablado', () => {
    expect(formOf(hablar, 'indicatiu', 'pretérito_perfecto_compuesto', 0)).toBe('he hablado')
  })

  it('futuro, condicional, subjuntivo, imperativo, no personales', () => {
    expect(formOf(hablar, 'indicatiu', 'futur', 0)).toBe('hablaré')
    expect(formOf(hablar, 'indicatiu', 'condicional', 0)).toBe('hablaría')
    expect(formOf(hablar, 'subjuntiu', 'present', 0)).toBe('hable')
    expect(formOf(hablar, 'imperatiu', 'present', 1)).toBe('habla')
    expect(formOf(hablar, 'formes_no_personals', 'gerundi', 0)).toBe('hablando')
    expect(formOf(hablar, 'formes_no_personals', 'participi', 0)).toBe('hablado')
  })

  it('irregular ir: voy / voy a… (perífrasis con infinitivo no, con participio: he ido)', () => {
    const ir = conjugate('ir', 'es')
    expect(formOf(ir, 'indicatiu', 'present', 0)).toBe('voy')
    expect(formOf(ir, 'imperatiu', 'present', 1)).toBe('ve')
  })

  it('irregular hacer: hago / hecho', () => {
    const hacer = conjugate('hacer', 'es')
    expect(formOf(hacer, 'indicatiu', 'present', 0)).toBe('hago')
    expect(formOf(hacer, 'formes_no_personals', 'participi', 0)).toBe('hecho')
  })

  it('irregular poder: puedo', () => {
    expect(formOf(conjugate('poder', 'es'), 'indicatiu', 'present', 0)).toBe('puedo')
  })
})
