import pytest
from httpx import AsyncClient, ASGITransport

from public_memes_api.main import app as public_media_app
from public_memes_api.config import config
from public_memes_api.db.db_base import engine, Base, async_session_maker
from public_memes_api.memes.model import Meme


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    assert config.MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    print("Database created sdfsdf")

    # def open_mock_json(model: str):
    #     with open(f"app/tests/mock_{model}.json", encoding="utf-8") as file:
    #         return json.load(file)
    #
    # hotels = open_mock_json("hotels")
    # rooms = open_mock_json("rooms")
    # users = open_mock_json("users")
    # bookings = open_mock_json("bookings")
    #
    # for booking in bookings:
    #     booking["date_from"] = datetime.strptime(booking["date_from"], "%Y-%m-%d")
    #     booking["date_to"] = datetime.strptime(booking["date_to"], "%Y-%m-%d")
    #
    # async with async_session_maker() as session:
    #     add_hotels = insert(Hotels).values(hotels)
    #     add_rooms = insert(Rooms).values(rooms)
    #     add_users = insert(Users).values(users)
    #     add_bookings = insert(Bookings).values(bookings)
    #
    #     await session.execute(add_hotels)
    #     await session.execute(add_rooms)
    #     await session.execute(add_users)
    #     await session.execute(add_bookings)
    #
    #     await session.commit()


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
