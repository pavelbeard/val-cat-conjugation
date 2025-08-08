from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import RequestResponseEndpoint, BaseHTTPMiddleware
from utils.exceptions import AppException
from utils.logger import create_logger


logger = create_logger(__name__)


async def app_exception_handler(request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "error_type": exc.error_type},
    )


async def general_exception_handler(request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "detail": "An unexpected error occurred",
            "error_type": "Internal Server Error",
        },
    )


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        try:
            response = await call_next(request)
            return response
        except AppException as exc:
            return await app_exception_handler(request, exc)
        except Exception as exc:
            return await general_exception_handler(request, exc)


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        # Log the request details
        logger.info(f"Request: {request.method} {request.url}")

        response = await call_next(request)

        # Log the response details
        logger.info(f"Response: {response.status_code}")

        return response
