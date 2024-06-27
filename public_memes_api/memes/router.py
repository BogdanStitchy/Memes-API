from io import BytesIO
from pathlib import Path
from typing import Optional

import httpx
from fastapi import APIRouter, HTTPException, UploadFile, File, Response, status
from starlette.responses import StreamingResponse

from public_memes_api.memes.dao import MemesDAO
from public_memes_api.config.config import PRIVATE_MEDIA_SERVICE_URL
from public_memes_api.memes.exceptions import AddingMemePictureException, AddingMemeMetadataException, \
    IncorrectMemeIdException, MemeImageException
from public_memes_api.memes.schemas import SMemeCreate

router = APIRouter(
    prefix="/memes",
    tags=["Мемы"]
)


# @router.get("/memes")
# async def get_memes(skip: int = 0, limit: int = 10):
#     memes = await MemesDAO.get_memes_with_pagination(skip, limit)
#     return memes


@router.get("/{meme_id}")
async def get_meme(meme_id: int) -> StreamingResponse:
    meme = await MemesDAO.find_by_id(meme_id)
    print(f"{meme=}")
    print(f"{type(meme)=}")
    if meme is None:
        raise IncorrectMemeIdException

    image_name = f"{meme.id}_{meme.file_name}"

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{PRIVATE_MEDIA_SERVICE_URL}/s3_memes/download/{image_name}")

        if response.status_code != 200:
            raise MemeImageException

    content_type = response.headers.get("content-type", "application/octet-stream")

    return StreamingResponse(BytesIO(response.content), media_type=content_type)


@router.post("/meme")
async def create_meme(text: Optional[str], file: UploadFile = File(...)) -> int:
    id_added_meme: int = await MemesDAO.add(file_name=file.filename, text=text)

    if not isinstance(id_added_meme, int):
        raise AddingMemeMetadataException

    new_name = f"{id_added_meme}_{file.filename}"

    async with httpx.AsyncClient() as client:  # Загрузка файла на приватный сервис
        response = await client.post(
            f"{PRIVATE_MEDIA_SERVICE_URL}/s3_memes/upload",
            files={"file": (new_name, file.file, file.content_type)}
        )
        if response.status_code != 201:
            raise AddingMemePictureException

    return id_added_meme
