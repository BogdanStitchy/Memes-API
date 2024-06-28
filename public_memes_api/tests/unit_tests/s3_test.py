import pytest
from unittest.mock import patch
from fastapi import UploadFile
from httpx import Response

from public_memes_api.memes.exceptions import MemeImageDeleteException, AddingMemePictureException, MemeImageException
from public_memes_api.memes.utils_s3 import delete_image_from_s3, upload_image_to_s3, download_image_from_s3


@pytest.mark.asyncio
@pytest.mark.parametrize("status_code,exception",
                         [
                             (204, None),
                             (404, MemeImageDeleteException)
                         ])
async def test_delete_image_from_s3(status_code, exception):
    with patch('httpx.AsyncClient.delete') as mock_delete:
        mock_delete.return_value = Response(status_code)
        if exception:
            with pytest.raises(exception):
                await delete_image_from_s3('test_image.png')
        else:
            await delete_image_from_s3('test_image.png')


@pytest.mark.asyncio
@pytest.mark.parametrize("status_code,exception",
                         [
                             (201, None),
                             (500, AddingMemePictureException)
                         ])
async def test_upload_image_to_s3(status_code, exception):
    with patch('httpx.AsyncClient.post') as mock_post:
        mock_post.return_value = Response(status_code)
        if exception:
            with pytest.raises(exception):
                await upload_image_to_s3('test_image.png', UploadFile('test_image.png'))
        else:
            await upload_image_to_s3('test_image.png', UploadFile('test_image.png'))


@pytest.mark.asyncio
@pytest.mark.parametrize("status_code,exception",
                         [
                             (200, None),
                             (500, MemeImageException)
                         ])
async def test_download_image_from_s3(status_code, exception):
    with patch('httpx.AsyncClient.get') as mock_get:
        mock_get.return_value = Response(status_code)
        if exception:
            with pytest.raises(exception):
                await download_image_from_s3('test_image.png')
        else:
            await download_image_from_s3('test_image.png')
