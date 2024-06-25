from fastapi import FastAPI
from private_media_service.memes.router import router

app = FastAPI()

app.include_router(router)



