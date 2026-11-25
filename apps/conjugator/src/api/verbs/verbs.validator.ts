import { validator } from '@vcc/api-builder'

/**
 * Validadores de verbs (DSL de src/validator), uno por método del controller.
 * mw.validator los convierte a zod y valida { params, query, body }.
 */
const search = {
  query: {
    q: validator.string.notRequired(), // busca en infinitivo y traducción
    form: validator.string.notRequired(), // busca por forma conjugada exacta
    letter: validator.string.notRequired(), // infinitivo empieza por letra
    sort: validator.string.notRequired(), // 'infinitive' (default) | 'clicks'
    page: validator.number.notRequired(), // 1-based; alternativa a skip
    limit: validator.number.notRequired().default(50),
    skip: validator.number.notRequired(), // si no se indica, se calcula desde page
  },
}

const get = {
  params: {
    infinitive: validator.stringRequired,
  },
}

export const verbsValidator = {
  search,
  get,
}
