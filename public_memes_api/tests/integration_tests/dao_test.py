import pytest

from public_memes_api.memes.dao import MemesDAO
from public_memes_api.memes.exceptions import DaoMethodException


@pytest.mark.parametrize("skip,limit", [(0, 10), (10, 20)])
async def test_add_get_memes_with_pagination(skip, limit):
    # Добавление тестовых данных
    for i in range(15):
        await MemesDAO.add(file_name=f"test_image_{i}.png", text=f"Sample meme {i}")

    result = await MemesDAO.get_memes_with_pagination(skip=skip, limit=limit)
    for meme in result:
        isinstance(meme, dict)
    assert len(result) <= limit


async def test_update_meme():
    meme_id = await MemesDAO.add(file_name=f"test_image.png", text=f"Sample meme")

    # Обновление мема
    updated_meme = await MemesDAO.update(meme_id, file_name="updated_image.png", text="Updated meme")
    assert updated_meme.file_name == "updated_image.png"
    assert updated_meme.text == "Updated meme"


@pytest.mark.asyncio
async def test_find_by_id():
    meme_id = await MemesDAO.add(file_name=f"test_image.png", text=f"Sample meme")
    # Поиск мема по ID
    result = await MemesDAO.find_by_id(meme_id)
    assert result.file_name == "test_image.png"
    assert result.text == "Sample meme"


@pytest.mark.asyncio
async def test_find_one_or_none():
    await MemesDAO.add(file_name=f"unic_image.png", text=f"Sample meme")

    # Поиск мема по фильтру
    result = await MemesDAO.find_one_or_none(file_name="unic_image.png")

    assert result.file_name == "unic_image.png"
    assert result.text == "Sample meme"


@pytest.mark.asyncio
async def test_get_all(clear_db_table_meme):
    await MemesDAO.add(file_name=f"test_image.png", text=f"Sample meme")

    result = await MemesDAO.get_all()
    assert len(result) == 1
    assert result[0]["file_name"] == "test_image.png"
    assert result[0]["text"] == "Sample meme"


@pytest.mark.asyncio
async def test_delete_meme():
    meme_id = await MemesDAO.add(file_name=f"test_image.png", text=f"Sample meme")

    rows_deleted = await MemesDAO.delete(id=meme_id)
    assert rows_deleted == 1

    # Проверка, что мем удален
    with pytest.raises(DaoMethodException):
        await MemesDAO.find_by_id(meme_id)
