from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from private_media_service.memes.router import router

app = FastAPI()

app.include_router(router)

origins = [
    "http://localhost:8000",
    "http://localhost:8001",
    "http://127.0.0.1:8001",
    "http://127.0.0.1:8001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Разрешенные источники
    allow_credentials=True,  # Разрешение на отправку cookie
    allow_methods=["GET", "POST", "DELETE"],  # Разрешенные методы
)
