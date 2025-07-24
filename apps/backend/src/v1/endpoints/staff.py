from fastapi import APIRouter

from src.core.config import settings
from src.utils.exceptions import AppException, HttpStatus
from src.utils.queries import staff as staff_queries

router = APIRouter(tags=["System"])


@router.get("/health")
async def health_check():
    return {"collections": staff_queries.list_collections()}


@router.get("/error-test")
async def error_test():
    raise AppException(HttpStatus.BAD_REQUEST, "This is a test error")
