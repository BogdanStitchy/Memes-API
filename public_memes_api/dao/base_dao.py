from sqlalchemy import delete, insert, select
from sqlalchemy.exc import SQLAlchemyError

from public_memes_api.db.db_base import async_session_maker
from public_memes_api.logger import logger


class BaseDAO:
    model = None

    @classmethod
    async def find_by_id(cls, model_id: int):
        try:
            async with async_session_maker() as session:
                query = select(cls.model).filter_by(id=model_id)
                result = await session.execute(query)
                return result.scalar_one_or_none()
        except (SQLAlchemyError, Exception) as error:
            if isinstance(error, SQLAlchemyError):
                msg = "Database Exc"
            if isinstance(error, Exception):
                msg = "Unknown Exc"
            msg += ": Cannot find by id"
            extra = {
                "model": cls.model,
                "model_id": model_id
            }
            logger.error(msg, extra=extra, exc_info=True)
            return {"error": error.__str__()}

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        try:
            async with async_session_maker() as session:
                query = select(cls.model.__table__).filter_by(**filter_by)
                result = await session.execute(query)
                return result.mappings().first()
        except (SQLAlchemyError, Exception) as error:
            if isinstance(error, SQLAlchemyError):
                msg = "Database Exc"
            if isinstance(error, Exception):
                msg = "Unknown Exc"
            msg += ": Cannot find one or none by filter"
            extra = {
                "model": cls.model,
                "filter_by": filter_by
            }
            logger.error(msg, extra=extra, exc_info=True)
            return {"error": error.__str__()}

    @classmethod
    async def get_all(cls, **filter_by):
        try:
            async with async_session_maker() as session:
                query = select(cls.model.__table__).filter_by(**filter_by)
                result = await session.execute(query)
                result = result.mappings().all()
                return result
        except (SQLAlchemyError, Exception) as error:
            if isinstance(error, SQLAlchemyError):
                msg = "Database Exc"
            if isinstance(error, Exception):
                msg = "Unknown Exc"
            msg += ": Cannot get all objects by filter"
            extra = {
                "model": cls.model,
                "filter_by": filter_by
            }
            logger.error(msg, extra=extra, exc_info=True)
            return {"error": error.__str__()}

    @classmethod
    async def add(cls, **data) -> int:
        try:
            async with async_session_maker() as session:
                query = insert(cls.model).values(**data).returning(cls.model.id)
                result = await session.execute(query)
                await session.commit()
                id_added_record = result.scalar_one()
                return id_added_record
        except (SQLAlchemyError, Exception) as error:
            if isinstance(error, SQLAlchemyError):
                msg = "Database Exc"
            if isinstance(error, Exception):
                msg = "Unknown Exc"
            msg += ": Cannot add object"
            extra = {
                "model": cls.model,
                "data": data
            }
            logger.error(msg, extra=extra, exc_info=True)
            return {"error": error.__str__()}

    @classmethod
    async def delete(cls, **filter_by):
        try:
            async with async_session_maker() as session:
                query = delete(cls.model).filter_by(**filter_by)
                result = await session.execute(query)
                await session.commit()
                return result.rowcount
        except (SQLAlchemyError, Exception) as error:
            if isinstance(error, SQLAlchemyError):
                msg = "Database Exc"
            if isinstance(error, Exception):
                msg = "Unknown Exc"
            msg += ": Cannot delete object by filter"
            extra = {
                "model": cls.model,
                "filter_by": filter_by
            }
            logger.error(msg, extra=extra, exc_info=True)
            return {"error": error.__str__()}
