from public_memes_API.dao.base_dao import BaseDAO
from public_memes_API.memes.model import Meme


class MemesDAO(BaseDAO):
    model = Meme
