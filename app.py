from fastapi import FastAPI

from src.router import router
from src.settings import static, media

app = FastAPI(title='BELHARD', description='PROF 11')
app.include_router(router=router)
app.mount(path='/static', app=static, name='static')
app.mount(path='/media', app=media, name='media')
