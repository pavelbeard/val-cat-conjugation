from db.client import db
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from api.core.config import settings
from api.utils.exceptions import AppException
from api.v1.api import api_router

app = FastAPI()


@app.exception_handler(AppException)
async def app_exception_handler(request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "error_type": exc.error_type},
    )


@app.get("/")
async def read_root():
    return {"message": "Welcome to the Val Cat Conjugation API"}


app.include_router(prefix=settings.API_V1_STR, router=api_router)
