import { controller, type ControllerMethod } from './controller.js'
import { auth } from './auth.js'
import { validatorMw, type AppRequest, type Validator, type ValidatorFn } from '../validator/index.js'

export { sendOk, sendCreated, sendNoContent } from './response.js'
export { errorHandler, notFoundHandler } from './error-handler.js'
export { controller, type ControllerMethod }
export { auth }
export { validatorMw, type AppRequest, type Validator, type ValidatorFn }

/** Punto único de entrada a los middlewares: mw.validator(...) / mw.controller(...) / mw.auth en los routers. */
export const mw = { validator: validatorMw, controller, auth }
export default mw
