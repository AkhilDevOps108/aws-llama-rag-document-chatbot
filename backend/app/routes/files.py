from fastapi import APIRouter

from app.models.document import DocumentRecord
from app.services.s3_service import S3Service


router = APIRouter(tags=["files"])


@router.get("/files", response_model=list[DocumentRecord])
async def list_files() -> list[DocumentRecord]:
    return S3Service().list_documents()

