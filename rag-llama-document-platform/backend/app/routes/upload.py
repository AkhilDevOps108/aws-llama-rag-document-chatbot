from fastapi import APIRouter, UploadFile, HTTPException, status, Depends
from app.services.s3_service import upload_file_to_s3
from app.config import get_settings
import uuid

router = APIRouter()

@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_document(file: UploadFile, settings=Depends(get_settings)):
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are allowed."
        )

    unique_filename = f"documents/{uuid.uuid4()}.pdf"

    try:
        upload_file_to_s3(file.file, unique_filename, settings)
        return {"message": "File uploaded successfully", "filename": unique_filename}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload file: {str(e)}"
        )