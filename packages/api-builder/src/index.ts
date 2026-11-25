/**
 * @vcc/api-builder — librería de backend reutilizable.
 * Punto único de entrada (este index)
 * con db, middlewares, validator, errors y axios.
 */
export * from './errors.js'
export * from './axios.js'
export * from './db/index.js'
export {
  controller,
  auth,
  errorHandler,
  notFoundHandler,
  sendOk,
  sendCreated,
  sendNoContent,
  type ControllerMethod,
} from './middlewares/index.js'
export { default as mw } from './middlewares/index.js'
export {
  validator,
  buildRequestSchema,
  isDescriptor,
  validateRequest,
  formatIssues,
  isSchema,
  toAppRequest,
  validatorMw,
  type AppRequest,
  type ValidatedRequest,
  type Validator,
  type ValidatorFn,
  type RequestDescriptor,
  type FieldBuilder,
} from './validator/index.js'
