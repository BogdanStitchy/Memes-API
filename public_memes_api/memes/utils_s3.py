import httpx
from fastapi import UploadFile

from public_memes_api.config.config import PRIVATE_MEDIA_SERVICE_URL
from public_memes_api.memes.exceptions import MemeImageDeleteException, AddingMemePictureException


async def delete_image_from_s3(image_name: str):
    print("Task Start")
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{PRIVATE_MEDIA_SERVICE_URL}/s3_memes/delete/{image_name}")
        print("Task Finish", response.status_code)
        if response.status_code != 204:
            raise MemeImageDeleteException


async def upload_image_to_s3(image_name: str, file: UploadFile):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{PRIVATE_MEDIA_SERVICE_URL}/s3_memes/upload",
            files={"file": (image_name, file.file, file.content_type)}
        )
        if response.status_code != 201:
            raise AddingMemePictureException
