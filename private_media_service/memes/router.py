import mimetypes
from typing import List

from fastapi import APIRouter, File, HTTPException, Response, UploadFile, status
from starlette.responses import StreamingResponse

from private_media_service.s3_storage.config_s3 import s3_client

router = APIRouter(
    prefix="/s3_memes",
    tags=["s3_мемы"]
)


@router.post("/upload", summary="Загрузить файл")
async def upload_file(file: UploadFile = File(...)):
    """
    Загружает файл в хранилище S3.

    - **file**: Файл для загрузки
    """
    try:
        s3_client.upload_fileobj(file.file, "memes", file.filename)
        return Response(status_code=status.HTTP_201_CREATED)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/download/{filename}", summary="Скачать файл")
async def download_file(filename: str) -> StreamingResponse:
    """
    Скачивает файл из хранилища S3 по его имени.

    - **filename**: Имя файла для скачивания
    """

    def get_mime_type(filename: str):
        mime_type, _ = mimetypes.guess_type(filename)
        return mime_type

    try:
        media_type = get_mime_type(filename)
        file_obj = s3_client.get_object(Bucket="memes", Key=filename)
        return StreamingResponse(file_obj['Body'], media_type=media_type)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/files", summary="Список файлов")
async def get_list_files() -> List[str]:
    """
    Возвращает список файлов в хранилище S3.
    """
    try:
        response = s3_client.list_objects_v2(Bucket="memes")
        files = [item["Key"] for item in response.get("Contents", [])]
        return files
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/delete/{filename}", summary="Удалить файл")
async def delete_file(filename: str):
    """
    Удаляет файл из хранилища S3 по его имени.

    - **filename**: Имя файла для удаления
    """
    try:
        s3_client.delete_object(Bucket="memes", Key=filename)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
