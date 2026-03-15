from __future__ import annotations

from io import BytesIO

from fastapi import APIRouter, File, HTTPException, UploadFile, status

from app.models.document import UploadResponse
from app.services.document_processor import DocumentProcessor
from app.services.embedding_service import EmbeddingService
from app.services.s3_service import S3Service
from app.services.vector_service import VectorService


router = APIRouter(tags=["upload"])


@router.post("/upload", response_model=UploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(file: UploadFile = File(...)) -> UploadResponse:
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    file_bytes = await file.read()
    if not file_bytes:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    s3_service = S3Service()
    s3_key = s3_service.upload_file(
        file_name=file.filename,
        file_stream=BytesIO(file_bytes),
        content_type=file.content_type or "application/pdf",
    )

    processor = DocumentProcessor()
    stored_file_bytes = s3_service.download_file_bytes(s3_key)
    chunks = processor.extract_chunks(stored_file_bytes)
    if not chunks:
        raise HTTPException(status_code=400, detail="No readable text was found in the PDF.")

    embedding_service = EmbeddingService()
    vector_service = VectorService()
    embeddings = embedding_service.embed_documents([chunk.text for chunk in chunks])
    payloads = [
        {
            "text": chunk.text,
            "document_name": file.filename,
            "page_number": chunk.page_number,
            "s3_key": s3_key,
        }
        for chunk in chunks
    ]
    vector_service.upsert_chunks(embeddings=embeddings, chunks=payloads)

    return UploadResponse(
        message="Document uploaded and indexed successfully.",
        file_name=file.filename,
        s3_key=s3_key,
        chunks_indexed=len(chunks),
    )
