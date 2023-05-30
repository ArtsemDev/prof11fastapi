from fastapi import FastAPI

from src.router import router


app = FastAPI(title='BELHARD', description='PROF 11')
app.include_router(router=router)
