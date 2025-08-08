from core.middlewares import ErrorHandlingMiddleware
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from utils.logger import create_logger
from src.core.config import settings
from src.v1.api import api_router

app = FastAPI()

origins = [
    "http://localhost:3000",
    "https://catalan-conjugador.vercel.app",
]

logger = create_logger(__name__)


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(ErrorHandlingMiddleware)
# app.add_middleware(LoggingMiddleware)


@app.get("/")
async def read_root():
    return {"message": "Welcome to the Val Cat Conjugation API"}


app.include_router(prefix=settings.API_V1_STR, router=api_router)
