from fastapi import Request
from fastapi.responses import HTMLResponse

from .router import router
from src.settings import templates


@router.get(
    '/',
    response_class=HTMLResponse,
    name='shop_index'
)
async def index(request: Request):
    return templates.TemplateResponse(
        'shop/thankyou.html',
        {'request': request}
    )
