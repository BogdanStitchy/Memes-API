from fastapi import HTTPException, status


class MemeException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class AddingMemeMetadataException(MemeException):
    detail = "Ошибка добавления метаданных"


class AddingMemePictureException(MemeException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Ошибка добавления картинки"


