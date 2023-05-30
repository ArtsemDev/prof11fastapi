from fastapi import APIRouter

from .v1.endpoints import router as api_v1_router


router = APIRouter(prefix='/api')
router.include_router(router=api_v1_router)
