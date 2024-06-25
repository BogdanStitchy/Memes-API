from fastapi import APIRouter, HTTPException, UploadFile, File
from starlette.responses import StreamingResponse
from private_media_service.memes.config_s3 import s3_client

router = APIRouter(
    prefix="/s3_memes",
    tags=["s3_мемы"]
)


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        s3_client.upload_fileobj(file.file, "memes", file.filename)
        return {"filename": file.filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/download/{filename}")
async def download_file(filename: str):
    try:
        file_obj = s3_client.get_object(Bucket="memes", Key=filename)
        return StreamingResponse(file_obj['Body'], media_type='application/octet-stream')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
