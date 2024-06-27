from fastapi import FastAPI, Request
from time import time

from public_memes_api.memes.router import router

from public_memes_api.logger import logger

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
