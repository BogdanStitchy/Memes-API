import pytest
from httpx import AsyncClient, ASGITransport

from public_memes_api.main import app as public_media_app
from public_memes_api.config import config
from public_memes_api.db.db_base import engine, Base, async_session_maker


@pytest.fixture(scope="session", autouse=True)
def check_mode():
    if config.MODE != "TEST":
        pytest.exit(f"Прерывание тестовой серии: MODE!=TEST\nMODE={config.MODE}")


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    assert config.MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    print("Database created")


@pytest.fixture(scope="function")
async def async_client():
    async with AsyncClient(transport=ASGITransport(app=public_media_app), base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="function")
async def clear_db_table_meme():
    async with async_session_maker() as session:
        memes_table = Base.metadata.tables['memes']
        await session.execute(memes_table.delete())
        await session.commit()
        print("Table Meme was clear")
