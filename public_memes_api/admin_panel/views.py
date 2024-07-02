from sqladmin import ModelView

from public_memes_api.memes.model import Meme


class MemeAdmin(ModelView, model=Meme):
    column_list = [Meme.id, Meme.file_name] + [Meme.text]
    can_delete = False
    name = "Мем"
    name_plural = "Мемы"
    icon = "fa-solid fa-laugh"
