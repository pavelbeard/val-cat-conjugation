from enum import Enum

from fastapi import HTTPException

class HttpStatus(Enum):
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    CONFLICT = 409
    INTERNAL_SERVER_ERROR = 500



class AppException(HTTPException):
    status_code: HttpStatus.BAD_REQUEST

    def __init__(self, type: HttpStatus, message: str):
        super().__init__(status_code=type.value, detail=message)
        self.status_code = type.value
        self.error_type = type.name