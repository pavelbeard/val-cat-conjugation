from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from src.core.config import settings
from src.utils.exceptions import AppException
from src.v1.api import api_router

app = FastAPI()

origins = [
    "http://localhost:3000",
    "https://catalan-conjugador.vercel.app",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
