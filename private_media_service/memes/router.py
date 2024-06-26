from fastapi import APIRouter, HTTPException, UploadFile, File, Response, status
from starlette.responses import StreamingResponse
import mimetypes

from private_media_service.memes.config_s3 import s3_client

router = APIRouter(
    prefix="/s3_memes",
    tags=["s3_мемы"]
)


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        s3_client.upload_fileobj(file.file, "memes", file.filename)
        return Response(status_code=status.HTTP_201_CREATED)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/download/{filename}")
async def download_file(filename: str) -> StreamingResponse:
    def get_mime_type(filename: str):
        mime_type, _ = mimetypes.guess_type(filename)
        return mime_type

    try:
        media_type = get_mime_type(filename)
        file_obj = s3_client.get_object(Bucket="memes", Key=filename)
        return StreamingResponse(file_obj['Body'], media_type=media_type)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/files")
async def get_list_files():
    try:
        response = s3_client.list_objects_v2(Bucket="memes")
        files = [item["Key"] for item in response.get("Contents", [])]
        return {"files": files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/delete/{filename}")
async def delete_file(filename: str):
    try:
        s3_client.delete_object(Bucket="memes", Key=filename)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return {"error": str(e)}
