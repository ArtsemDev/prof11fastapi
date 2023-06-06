from fastapi import APIRouter

from .api.router import router as api_router
from .shop.views import router as shop_router

router = APIRouter()
router.include_router(router=api_router)
router.include_router(router=shop_router)
