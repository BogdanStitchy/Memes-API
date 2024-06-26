import pytest
from httpx import AsyncClient


async def test_upload_file(async_client: AsyncClient):
    with open("private_media_service/tests/data_tests/test.png", "rb") as f:
        response = await async_client.post("/s3_memes/upload", files={"file": ("test.png", f, "image/jpeg")})
    assert response.status_code == 201


async def test_download_file(async_client: AsyncClient):
    response = await async_client.get("/s3_memes/download/test.png")
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"


async def test_get_list_files(async_client: AsyncClient):
    response = await async_client.get("/s3_memes/files")
    assert response.status_code == 200
    response_data = response.json()
    files = response_data.get("files", [])
    assert 'test.png' in files


async def test_delete_file(async_client: AsyncClient):
    response = await async_client.delete("/s3_memes/delete/test.png")
    assert response.status_code == 204

    response = await async_client.get("/s3_memes/files")
    assert response.status_code == 200
    response_data = response.json()
    files = response_data.get("files", [])
    assert 'test.png' not in files
