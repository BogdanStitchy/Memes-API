from io import BytesIO
from typing import Optional, List

import asyncio
import httpx
from fastapi import APIRouter, UploadFile, File, Response, Request, status
from fastapi_cache.decorator import cache
from starlette.responses import StreamingResponse

from public_memes_api.logger import logger
from public_memes_api.memes.dao import MemesDAO
from public_memes_api.memes.dao_wrappers import MemesDAOWrappers
from public_memes_api.config.config import PRIVATE_MEDIA_SERVICE_URL
from public_memes_api.memes.exceptions import AddingMemeMetadataException, IncorrectMemeIdException, \
    MemeImageException, MemeMetadataException, MemeMetadataDeleteException, MemesNotFoundException, \
    DaoMethodException, EndPointException
from public_memes_api.memes.schemas import SMemeRead, SAddedId, SMemeReadWithUrl
from public_memes_api.memes.utils_s3 import upload_image_to_s3, delete_image_from_s3, download_image_from_s3
from public_memes_api.tasks.tasks import tasks_delete_image_from_s3

router = APIRouter(
    prefix="/memes",
    tags=["Мемы"]
)


@router.get("/")
@cache(expire=100)
async def get_memes(request: Request, skip: int = 0, limit: int = 10) -> List[SMemeReadWithUrl]:
    memes = await MemesDAOWrappers.get_with_pagination_with_error_handling(skip=skip, limit=limit)
    if memes is None:
        raise MemesNotFoundException

    base_url = request.url.scheme + "://" + request.headers['host']

    result = [
        SMemeReadWithUrl(
            id=meme.id,
            file_name=meme.file_name,
            text=meme.text,
            image_url=f"{base_url}{router.prefix}/{meme.id}"
        )
        for meme in memes
    ]

    return result


@router.get("/batch_images")
async def get_batch_images(skip: int = 0, limit: int = 10) -> StreamingResponse:
    # !!! Swagger UI не отображает корректно multipart/mixed ответы
    memes = await MemesDAOWrappers.get_with_pagination_with_error_handling(skip=skip, limit=limit)
    if memes is None:
        raise MemesNotFoundException

    async with httpx.AsyncClient() as client:
        tasks = [
            client.get(f"{PRIVATE_MEDIA_SERVICE_URL}/s3_memes/download/{meme.id}_{meme.file_name}")
            for meme in memes
        ]
        responses = await asyncio.gather(*tasks)

    # Генератор для потоковой передачи нескольких файлов
    async def file_stream():
        for resp in responses:
            if resp.status_code == 200:
                yield b"--boundary\r\n"
                yield b'Content-Type: %s\r\n' % resp.headers['content-type'].encode()
                yield b'Content-Disposition: form-data; filename="%s"\r\n\r\n' % (resp.url.path.split('/')[-1].encode())
                yield resp.content
                yield b"\r\n"

        yield b"--boundary--\r\n"

    headers = {
        'Content-Type': 'multipart/mixed; boundary=boundary',
    }

    return StreamingResponse(file_stream(), headers=headers)


@router.get("/{meme_id}")
async def get_meme(meme_id: int) -> StreamingResponse:
    meme = await MemesDAOWrappers.find_by_id_with_error_handling(meme_id)
    if meme is None:
        raise IncorrectMemeIdException
    image_name = f"{meme.id}_{meme.file_name}"

    response = await download_image_from_s3(image_name)  # добавить обработку ошибок

    content_type = response.headers.get("content-type", "application/octet-stream")

    return StreamingResponse(BytesIO(response.content), media_type=content_type)


@router.get("/{meme_id}/metadata")
@cache(expire=100)
async def get_metadata_meme(meme_id: int) -> SMemeRead:
    meme = await MemesDAOWrappers.find_by_id_with_error_handling(meme_id)
    if meme is None:
        raise IncorrectMemeIdException
    return meme


@router.post("/")
async def add_meme(text: Optional[str], file: UploadFile = File(...)) -> SAddedId:
    id_added_meme: int = await MemesDAOWrappers.add_with_error_handling(file_name=file.filename,
                                                                        text=text)  # await MemesDAO.add(file_name=file.filename, text=text)
    new_name = f"{id_added_meme}_{file.filename}"
    await upload_image_to_s3(new_name, file)

    return SAddedId(id_added_meme=id_added_meme)


@router.put("/{meme_id}")
async def update_meme(
        meme_id: int,
        text: Optional[str] = None,
        file: UploadFile = File(None)
):
    meme = await MemesDAOWrappers.find_by_id_with_error_handling(meme_id)  # MemesDAO.find_by_id(meme_id)
    if meme is None:
        raise IncorrectMemeIdException

    if file:
        old_image_name = f"{meme.id}_{meme.file_name}"
        new_image_name = f"{meme.id}_{file.filename}"

        # чтобы не удалить новый мем, если имена обновленного и старого мема совпадают
        await upload_image_to_s3(new_image_name, file)
        if old_image_name != new_image_name:
            tasks_delete_image_from_s3.delay(old_image_name)  # Удалить изображение в фоне

        meme.file_name = file.filename

    if text is not None:
        meme.text = text

    await MemesDAOWrappers.update_with_error_handling(meme_id, file_name=meme.file_name, text=meme.text)

    return Response(status_code=status.HTTP_200_OK)


@router.delete("/{meme_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_meme(meme_id: int):
    meme = await MemesDAOWrappers.find_by_id_with_error_handling(meme_id)
    if meme is None:
        raise IncorrectMemeIdException

    image_name = f"{meme.id}_{meme.file_name}"

    tasks_delete_image_from_s3.delay(image_name)  # Удалить изображение в фоне

    result = await MemesDAOWrappers.delete_with_error_handling(id=meme_id)
    if result is None:
        raise MemeMetadataDeleteException

    return Response(status_code=status.HTTP_204_NO_CONTENT)
