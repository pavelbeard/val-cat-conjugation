import { validator } from '../validator/index.js'

/**
 * Validadores del panel de administración (DSL de src/validator),
 * uno por método del controller.
 */
const infinitiveParams = {
  infinitive: validator.stringRequired,
}

export const adminValidator = {
  list: undefined, // sin validador

  create: {
    body: {
      infinitive: validator.string.required(),
      translation: validator.string.required(),
    },
  },

  update: {
    params: infinitiveParams,
    body: validator.object.required(), // body obligatorio y objeto (parcial)
  },

  remove: {
    params: infinitiveParams,
  },
}
