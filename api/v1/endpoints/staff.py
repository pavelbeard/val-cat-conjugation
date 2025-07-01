from fastapi import APIRouter

from api.core.config import settings
from api.db.client import db
from api.utils.exceptions import AppException, HttpStatus

router = APIRouter(tags=["System"])


@router.get("/health")
async def health_check():
    return {"collections": db.list_collection_names()}


@router.get("/env")
async def get_env():
    return {"env": settings.model_dump(mode="json")}


@router.get("/error-test")
async def error_test():
    raise AppException(HttpStatus.BAD_REQUEST, "This is a test error")
