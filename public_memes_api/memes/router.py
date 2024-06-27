from fastapi import APIRouter, HTTPException, UploadFile, File, Response, status

router = APIRouter(
    prefix="/memes",
    tags=["Мемы"]
)


@router.get("/memes")
def read_memes(skip: int = 0, limit: int = 10):
    memes = get_memes(db, skip=skip, limit=limit)
    return memes


@router.get("/memes/{meme_id}")
def read_meme(meme_id: int, db: Session = Depends(get_db)):
    meme = get_meme(db, meme_id=meme_id)
    if meme is None:
        raise HTTPException(status_code=404, detail="Meme not found")
    return meme


@router.post("/memes")
async def create_meme(meme: MemeCreate, file: UploadFile = File(...), db: Session = Depends(get_db)):
    async with httpx.AsyncClient() as client:
        # Загрузка файла на приватный сервис
        response = await client.post(
            f"{PRIVATE_MEDIA_SERVICE_URL}/upload",
            files={"file": (file.filename, file.file, file.content_type)}
        )
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to upload image to media service")

        file_url = response.json().get("filename")

    # Сохранение данных мема в базе данных
    meme.image_url = file_url
    return create_meme(db, meme=meme)


@router.put("/memes/{meme_id}")
async def update_meme(meme_id: int, meme: MemeUpdate, db: Session = Depends(get_db)):
    db_meme = update_meme(db, meme_id=meme_id, meme=meme)
    if db_meme is None:
        raise HTTPException(status_code=404, detail="Meme not found")
    return db_meme


@router.delete("/memes/{meme_id}")
async def delete_meme(meme_id: int, db: Session = Depends(get_db)):
    # Получение информации о меме перед удалением
    meme = get_meme(db, meme_id=meme_id)
    if meme is None:
        raise HTTPException(status_code=404, detail="Meme not found")

    async with httpx.AsyncClient() as client:
        # Удаление файла на приватном сервисе
        response = await client.delete(f"{PRIVATE_MEDIA_SERVICE_URL}/delete/{meme.image_url}")
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to delete image from media service")

    delete_meme(db, meme_id=meme_id)
    return {"message": "Meme deleted successfully"}
