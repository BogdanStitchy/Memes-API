import pytest
from httpx import AsyncClient, ASGITransport

from private_media_service.config import config
from private_media_service.main import app as private_media_app


@pytest.fixture(scope="session", autouse=True)
def check_mode():
    if config.MODE != "TEST":
        pytest.exit(f"Прерывание тестовой серии: MODE!=TEST\nMODE={config.MODE}")


@pytest.fixture(scope="function")
async def async_client():
    async with AsyncClient(transport=ASGITransport(app=private_media_app), base_url="http://test") as ac:
        yield ac
