import pytest
from httpx import AsyncClient, ASGITransport

from private_media_service.main import app as private_media_app


@pytest.fixture(scope="function")
async def async_client():
    async with AsyncClient(transport=ASGITransport(app=private_media_app), base_url="http://test") as ac:
        yield ac
