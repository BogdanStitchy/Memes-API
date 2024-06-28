from celery import Celery
from public_memes_api.config.config import HOST_REDIS

celery = Celery(
    "tasks",
    broker=f"redis://{HOST_REDIS}",
    include="public_memes_api.tasks.tasks"
)
