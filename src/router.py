from fastapi import APIRouter

from .api.router import router as api_router

router = APIRouter()
router.include_router(router=api_router)
