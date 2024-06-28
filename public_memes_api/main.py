from fastapi import FastAPI, Request
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from time import time
from redis import asyncio as aioredis

from public_memes_api.memes.router import router
from public_memes_api.logger import logger
from public_memes_api.config.config import HOST_REDIS

app = FastAPI()

app.include_router(router)


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
