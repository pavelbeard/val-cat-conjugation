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
