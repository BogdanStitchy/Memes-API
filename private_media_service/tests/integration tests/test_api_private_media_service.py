import pytest
from httpx import AsyncClient, ASGITransport

from private_media_service.main import app as private_media_app


@pytest.fixture(scope="function")
async def async_client():
    async with AsyncClient(transport=ASGITransport(app=private_media_app), base_url="http://test") as ac:
        yield ac


async def test_upload_get_file(async_client: AsyncClient):
    with open("private_media_service/tests/data_tests/test.png", "rb") as f:
        response = await async_client.post("/s3_memes/upload", files={"file": ("test.png", f, "image/jpeg")})
    assert response.status_code == 201

    response = await async_client.get("/s3_memes/files")
    assert response.status_code == 200
    response_data = response.json()
    files = response_data.get("files", [])

    assert 'test.png' in files

