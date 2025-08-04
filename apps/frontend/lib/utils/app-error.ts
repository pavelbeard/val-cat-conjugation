enum AppErrorTypes {
  BAD_REQUEST = 400,
  UNAUTHORIZED = 401,
  FORBIDDEN = 403,
  NOT_FOUND = 404,
  TOO_MANY_REQUESTS = 429,
  SERVER = 500,
}

export interface IAppError {
  type: AppErrorTypes;
  message: string;
}

export class AppError extends Error {
  statusCode = AppErrorTypes.BAD_REQUEST;

  constructor(type: keyof typeof AppErrorTypes, message: string) {
    super(message);
    Object.setPrototypeOf(this, new.target.prototype);
    this.name = Error.name;
    this.statusCode = AppErrorTypes[type];
    Error.captureStackTrace(this);
  }
}
