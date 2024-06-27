from sqlalchemy import select, update
from sqlalchemy.exc import SQLAlchemyError

from public_memes_api.dao.base_dao import BaseDAO
from public_memes_api.db.db_base import async_session_maker
from public_memes_api.logger import logger
from public_memes_api.memes.model import Meme


class MemesDAO(BaseDAO):
    model = Meme

    @classmethod
    async def get_memes_with_pagination(cls, skip: int, limit: int):
        try:
            async with async_session_maker() as session:
                query = select(cls.model.__table__).offset(skip).limit(limit)
                result_query = await session.execute(query)
                memes = result_query.mappings().all()
                return memes
        except (SQLAlchemyError, Exception) as error:
            if isinstance(error, SQLAlchemyError):
                msg = "Database Exc"
            if isinstance(error, Exception):
                msg = "Unknown Exc"
            msg += ": Cannot get meme with pagination"
            extra = {
                "skip": skip,
                "limit": limit
            }
            logger.error(msg, extra=extra, exc_info=True)
            return {"error": error.__str__()}

    @classmethod
    async def update(cls, meme_id: int, file_name: str, text: str):
        try:
            async with async_session_maker() as session:
                query = (
                    update(cls.model)
                        .where(cls.model.id == meme_id)
                        .values(file_name=file_name, text=text)
                        .returning(cls.model)
                )
                result = await session.execute(query)
                await session.commit()
                return result.mappings().one()
        except (SQLAlchemyError, Exception) as error:
            if isinstance(error, SQLAlchemyError):
                msg = "Database Exc"
            if isinstance(error, Exception):
                msg = "Unknown Exc"
            msg += ": Cannot update meme"
            extra = {
                "meme_id": meme_id,
                "file_name": file_name,
                "text": text
            }
            logger.error(msg, extra=extra, exc_info=True)
            return {"error": error.__str__()}
