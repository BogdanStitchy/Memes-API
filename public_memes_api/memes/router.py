from pathlib import Path
from typing import Optional

import httpx
from fastapi import APIRouter, HTTPException, UploadFile, File, Response, status

from public_memes_api.memes.dao import MemesDAO
from public_memes_api.config.config import PRIVATE_MEDIA_SERVICE_URL
from public_memes_api.memes.exceptions import AddingMemePictureException, AddingMemeMetadataException
from public_memes_api.memes.schemas import SMemeCreate

router = APIRouter(
    prefix="/memes",
    tags=["Мемы"]
)


# @router.get("/memes")
# async def get_memes(skip: int = 0, limit: int = 10):
#     memes = await MemesDAO.get_memes_with_pagination(skip, limit)
#     return memes


# @router.get("/memes/{meme_id}")
# async def get_meme(meme_id: int):
#     meme = MemesDAO.find_by_id(meme_id)
#     if meme is None:
#         raise HTTPException(status_code=404, detail="Meme not found")
#     return meme


@router.post("/memes")
async def create_meme(meme_name: str, text: Optional[str], file: UploadFile = File(...)) -> int:  # meme: SMemeCreate
    id_added_meme: int = await MemesDAO.add(file_name=meme_name, text=text)

    if not isinstance(id_added_meme, int):
        raise AddingMemeMetadataException

    file_extension = Path(file.filename).suffix[1:]
    new_name = f"{meme_name}_{id_added_meme}.{file_extension}"

    async with httpx.AsyncClient() as client:  # Загрузка файла на приватный сервис
        response = await client.post(
            f"{PRIVATE_MEDIA_SERVICE_URL}/s3_memes/upload",
            files={"file": (new_name, file.file, file.content_type)}
        )
        if response.status_code != 201:
            raise AddingMemePictureException

    return id_added_meme
