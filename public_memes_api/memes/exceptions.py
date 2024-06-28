from fastapi import HTTPException, status


class MemeException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class AddingMemeMetadataException(MemeException):
    detail = "Ошибка добавления метаданных"


class AddingMemePictureException(MemeException):
    detail = "Ошибка добавления картинки"


class IncorrectMemeIdException(MemeException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Мем с заданным id не найден"


class MemeImageException(MemeException):
    detail = "Ошибка получения изображения мема"


class MemeMetadataException(MemeException):
    detail = "Ошибка получения метаданных мема"


class MemeImageDeleteException(MemeException):
    detail = "Ошибка удаления изображения мема"


class MemeMetadataDeleteException(MemeException):
    detail = "Ошибка удаления метаданных мема"


class MemesNotFoundException(MemeException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Метаданные мемов не найдены"


class DaoMethodException(Exception):
    pass
