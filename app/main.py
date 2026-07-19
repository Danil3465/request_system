from fastapi import FastAPI
from app.api.requests import router


app = FastAPI(title="Request System")

app.include_router(router)