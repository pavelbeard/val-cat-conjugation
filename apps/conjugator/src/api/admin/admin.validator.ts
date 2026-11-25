import { validator } from '@vcc/api-builder';

/**
 * Validadores del panel de administración (DSL de src/validator),
 * uno por método del controller.
 */
const infinitiveParams = {
  infinitive: validator.stringRequired,
};

const create = {
  body: {
    infinitive: validator.string.required(),
    translation: validator.string.required(),
  },
};

const update = {
  params: infinitiveParams,
  body: validator.object.required(), // body obligatorio y objeto (parcial)
};

const remove = {
  params: infinitiveParams,
};

export const adminValidator = {
  create,
  update,
  remove,
};
