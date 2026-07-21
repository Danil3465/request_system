from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.requests import router


app = FastAPI(title="Request System")

app.include_router(router)


app.mount("/static", StaticFiles(directory="app/static"), name="static")