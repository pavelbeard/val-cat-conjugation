from fastapi import APIRouter
from fastapi.responses import JSONResponse
from schemas.staff import AppSettingsOutput, AppSettingsUpdate

from src.utils.exceptions import AppException, HttpStatus
from src.db.queries import staff as staff_queries

router = APIRouter(tags=["System"])


@router.get("/health")
async def health_check():
    return JSONResponse(content={"status": "ok"}, status_code=200)


@router.get("/settings", response_model=AppSettingsOutput, response_class=JSONResponse)
async def get_settings():
    """
    Get the application settings.
    """
    settings = staff_queries.get_settings()
    if not settings:
        raise AppException(HttpStatus.NOT_FOUND, "Settings not found")

    validated_settings = AppSettingsOutput.model_validate(settings)

    return JSONResponse(content=validated_settings.model_dump(), status_code=200)


@router.put("/settings", response_model=AppSettingsOutput, response_class=JSONResponse)
async def update_settings(settings: AppSettingsUpdate):
    """
    Update the application settings.
    """
    if not settings:
        raise AppException(HttpStatus.BAD_REQUEST, "Settings data is required")

    updated_settings = staff_queries.update_settings(
        settings.model_dump(exclude_none=True)
    )

    if not updated_settings:
        raise AppException(HttpStatus.NOT_FOUND, "Settings not found")

    validated_settings = AppSettingsOutput.model_validate(updated_settings)

    return JSONResponse(content=validated_settings.model_dump(), status_code=200)
