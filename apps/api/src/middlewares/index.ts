import { controller, type ControllerMethod } from './controller.js'
import { validatorMw, type Validator, type ValidatorFn } from '../validator/index.js'

export { sendOk, sendCreated, sendNoContent } from './response.js'
export { errorHandler, notFoundHandler } from './error-handler.js'
export { controller, type ControllerMethod }
export { validatorMw, type Validator, type ValidatorFn }

/** Punto único de entrada a los middlewares: mw.validator(...) / mw.controller(...) en los routers. */
export const mw = { validator: validatorMw, controller }
export default mw
