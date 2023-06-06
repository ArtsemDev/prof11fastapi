from pathlib import Path
from datetime import datetime

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

from .schemas import Settings


def contact(request: Request):
    return {
        'request': request,
        'phone_number': '+375259145208',
        'email': 'prataye.a@gmail.com',
        'address': 'Минск, 4й Загородный переулок 56А'
    }


SETTINGS = Settings()
BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(
    directory=BASE_DIR / 'templates',
    context_processors=[contact]
)
templates.env.globals['datetime'] = datetime
static = StaticFiles(directory=BASE_DIR / 'static')
media = StaticFiles(directory=BASE_DIR / 'media')
