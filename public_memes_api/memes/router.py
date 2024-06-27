from io import BytesIO
from typing import Optional

import httpx
from fastapi import APIRouter, HTTPException, UploadFile, File, BackgroundTasks, Response, status
from starlette.responses import StreamingResponse

from public_memes_api.memes.dao import MemesDAO
from public_memes_api.config.config import PRIVATE_MEDIA_SERVICE_URL
from public_memes_api.memes.exceptions import AddingMemePictureException, AddingMemeMetadataException, \
    IncorrectMemeIdException, MemeImageException, MemeMetadataException
from public_memes_api.memes.schemas import SMemeRead, SAddedId
from public_memes_api.memes.utils_s3 import upload_image_to_s3, delete_image_from_s3

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

    if meme is None:
        raise IncorrectMemeIdException
    if isinstance(meme, dict):
        if "error" in meme:
            raise MemeMetadataException

    image_name = f"{meme.id}_{meme.file_name}"

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{PRIVATE_MEDIA_SERVICE_URL}/s3_memes/download/{image_name}")

        if response.status_code != 200:
            raise MemeImageException

    content_type = response.headers.get("content-type", "application/octet-stream")

    return StreamingResponse(BytesIO(response.content), media_type=content_type)


@router.get("/{meme_id}/metadata")
async def get_metadata_meme(meme_id: int) -> SMemeRead:
    meme = await MemesDAO.find_by_id(meme_id)

    if meme is None:
        raise HTTPException(status_code=404, detail="Meme not found")
    if isinstance(meme, dict):
        if "error" in meme:
            raise MemeMetadataException

    return meme


@router.post("/")
async def add_meme(text: Optional[str], file: UploadFile = File(...)) -> SAddedId:
    id_added_meme: int = await MemesDAO.add(file_name=file.filename, text=text)

    if not isinstance(id_added_meme, int):
        raise AddingMemeMetadataException

    new_name = f"{id_added_meme}_{file.filename}"

    # async with httpx.AsyncClient() as client:  # Загрузка файла на приватный сервис
    #     response = await client.post(
    #         f"{PRIVATE_MEDIA_SERVICE_URL}/s3_memes/upload",
    #         files={"file": (new_name, file.file, file.content_type)}
    #     )
    #     if response.status_code != 201:
    #         raise AddingMemePictureException
    await upload_image_to_s3(new_name, file)

    return SAddedId(id_added_meme=id_added_meme)


@router.put("/{meme_id}")
async def update_meme(
        background_tasks: BackgroundTasks,
        meme_id: int,
        text: Optional[str] = None,
        file: UploadFile = File(None)
):
    meme = await MemesDAO.find_by_id(meme_id)

    if meme is None:
        raise IncorrectMemeIdException
    if isinstance(meme, dict):
        if "error" in meme:
            raise MemeMetadataException

    if file:
        old_image_name = f"{meme.id}_{meme.file_name}"
        new_image_name = f"{meme.id}_{file.filename}"

        # чтобы не удалить новый мем, если имена обновленного и старого мема совпадают
        await upload_image_to_s3(new_image_name, file)
        if old_image_name != new_image_name:
            background_tasks.add_task(delete_image_from_s3, old_image_name)  # Удаляем старое изображение в фоне

        meme.file_name = file.filename

    if text is not None:
        meme.text = text

    await MemesDAO.update(meme_id, file_name=meme.file_name, text=meme.text)

    return Response(status_code=status.HTTP_200_OK)
