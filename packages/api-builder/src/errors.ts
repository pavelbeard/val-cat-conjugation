export class HttpError extends Error {
  constructor(
    public status: number,
    message: string,
  ) {
    super(message)
    this.name = 'HttpError'
  }
}

export class NotFoundError extends HttpError {
  constructor(message = 'Not found') {
    super(404, message)
    this.name = 'NotFoundError'
  }
}

export class BadRequestError extends HttpError {
  constructor(message = 'Bad request') {
    super(400, message)
    this.name = 'BadRequestError'
  }
}

export class UnauthorizedError extends HttpError {
  constructor(message = 'Unauthorized') {
    super(401, message)
    this.name = 'UnauthorizedError'
  }
}

/** Factoría de errores de dominio: `return error.notFound('...')` en el BLL. */
export const error = {
  notFound: (message: string) => new NotFoundError(message),
  badRequest: (message: string) => new BadRequestError(message),
  unauthorized: (message: string) => new UnauthorizedError(message),
  http: (status: number, message: string) => new HttpError(status, message),
}
