from fastapi import APIRouter, Depends

from .dependencies import headers_validator


router = APIRouter(
    prefix='/v1',
    # dependencies=(Depends(headers_validator), )
)
