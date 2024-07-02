import requests

from public_memes_api.config.config import PRIVATE_MEDIA_SERVICE_URL
from public_memes_api.memes.exceptions import MemeImageDeleteHTTTPException
from public_memes_api.tasks.celery import celery


@celery.task
def tasks_delete_image_from_s3(image_name: str) -> None:
    response = requests.delete(f"{PRIVATE_MEDIA_SERVICE_URL}/s3_memes/delete/{image_name}")
    if response.status_code != 204:
        raise MemeImageDeleteHTTTPException
