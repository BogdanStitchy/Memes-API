from time import time

import sentry_sdk
from fastapi import FastAPI, Request
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from prometheus_fastapi_instrumentator import Instrumentator
from redis import asyncio as aioredis
from sqladmin import Admin

from public_memes_api.admin_panel.views import MemeAdmin
from public_memes_api.config.config import HOST_REDIS, SENTRY_DNS
from public_memes_api.db.db_base import engine
from public_memes_api.logger import logger
from public_memes_api.memes.router import router

app = FastAPI()

if SENTRY_DNS != "_":  # SENTRY_DNS - приватный днс
    sentry_sdk.init(
        dsn=SENTRY_DNS,
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
    )

app.include_router(router)

instrumentator = Instrumentator(
    should_group_status_codes=False,  # не группировать статусы ответа
    excluded_handlers=[".*admin.*", "/metrics"],  # игнорируемые эндпоинты
)
instrumentator.instrument(app).expose(app)  # Prometheus

admin = Admin(app, engine)  # Админка
admin.add_view(MemeAdmin)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time()
    response = await call_next(request)
    process_time = time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    logger.info("Request execution time", extra={
        "process_time": round(process_time, 4)
    })
    return response


@app.on_event("startup")
async def startup():
    redis = await aioredis.from_url(f"redis://{HOST_REDIS}", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="cache")
