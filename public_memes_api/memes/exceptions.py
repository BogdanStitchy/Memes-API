from fastapi import HTTPException, status


class MemeHTTTPException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class AddingMemeMetadataHTTTPException(MemeHTTTPException):
    detail = "Ошибка добавления метаданных"


class AddingMemePictureHTTTPException(MemeHTTTPException):
    detail = "Ошибка добавления картинки"


class IncorrectMemeIdHTTTPException(MemeHTTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Мем с заданным id не найден"


class MemeImageHTTTPException(MemeHTTTPException):
    detail = "Ошибка получения изображения мема"


class MemeMetadataHTTTPException(MemeHTTTPException):
    detail = "Ошибка получения метаданных мема"


class MemeImageDeleteHTTTPException(MemeHTTTPException):
    detail = "Ошибка удаления изображения мема"


class MemeMetadataDeleteHTTTPException(MemeHTTTPException):
    detail = "Ошибка удаления метаданных мема"


class MemesNotFoundHTTTPException(MemeHTTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Метаданные мемов не найдены"


class DaoMethodException(Exception):
    pass


class EndPointException(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Ошибка сервера"
