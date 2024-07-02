from public_memes_api.memes.dao import MemesDAO
from public_memes_api.memes.exceptions import (
    DaoMethodException,
    IncorrectMemeIdHTTTPException,
    AddingMemeMetadataHTTTPException,
    MemeMetadataHTTTPException,
    MemesNotFoundHTTTPException,
    MemeMetadataDeleteHTTTPException,
)
from typing import List, Dict, Any, Optional

from public_memes_api.memes.schemas import MemeInDB


class MemesDAOWrappers:
    @classmethod
    async def find_by_id_with_error_handling(cls, meme_id: int) -> Dict[str, Any]:
        try:
            return await MemesDAO.find_by_id(meme_id)
        except DaoMethodException:
            raise IncorrectMemeIdHTTTPException

    @classmethod
    async def add_with_error_handling(cls, file_name: str, text: str) -> int:
        try:
            return await MemesDAO.add(file_name=file_name, text=text)
        except DaoMethodException:
            raise AddingMemeMetadataHTTTPException

    @classmethod
    async def get_with_pagination_with_error_handling(cls, skip: int, limit: int) -> List[Dict[str, Any]]:
        try:
            return await MemesDAO.get_memes_with_pagination(skip=skip, limit=limit)
        except DaoMethodException:
            raise MemesNotFoundHTTTPException

    @classmethod
    async def update_with_error_handling(cls, meme_id: int, file_name: str, text: str) -> MemeInDB:
        try:
            return await MemesDAO.update(meme_id, file_name=file_name, text=text)
        except DaoMethodException:
            raise MemeMetadataHTTTPException

    @classmethod
    async def find_one_or_none_with_error_handling(cls, **filter_by) -> Optional[Dict[str, Any]]:
        try:
            return await MemesDAO.find_one_or_none(**filter_by)
        except DaoMethodException:
            raise MemeMetadataHTTTPException

    @classmethod
    async def get_all_with_error_handling(cls, **filter_by) -> List[Dict[str, Any]]:
        try:
            return await MemesDAO.get_all(**filter_by)
        except DaoMethodException:
            raise MemeMetadataHTTTPException

    @classmethod
    async def delete_with_error_handling(cls, **filter_by) -> int:
        try:
            return await MemesDAO.delete(**filter_by)
        except DaoMethodException:
            raise MemeMetadataDeleteHTTTPException
