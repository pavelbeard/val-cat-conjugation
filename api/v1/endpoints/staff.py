from fastapi import APIRouter

from api.core.config import settings
from api.utils.exceptions import AppException, HttpStatus
from api.utils.queries import staff as staff_queries

router = APIRouter(tags=["System"])


@router.get("/health")
async def health_check():
    return {"collections": staff_queries.list_collections()}


@router.get("/env")
async def get_env():
    return {"env": settings.model_dump(mode="json")}


@router.get("/error-test")
async def error_test():
    raise AppException(HttpStatus.BAD_REQUEST, "This is a test error")
