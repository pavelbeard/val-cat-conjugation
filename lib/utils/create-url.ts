import { BACKEND_URL } from '../constants'

export const createUrl = (...paths: string[]): string => {
  const sanitizedPath = paths.join('/').replace(/\/+/g, '/')
  return [BACKEND_URL].concat(sanitizedPath).join('/')
}
