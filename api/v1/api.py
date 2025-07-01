from fastapi import APIRouter
from api.v1.endpoints.seed import router as seed_router
from api.v1.endpoints.staff import router as staff_router
from api.v1.endpoints.verbs import router as verbs_router

api_router = APIRouter()

api_router.include_router(seed_router)
api_router.include_router(staff_router)
api_router.include_router(verbs_router)
