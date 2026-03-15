from datetime import datetime

from pydantic import BaseModel, Field


class DocumentRecord(BaseModel):
    name: str
    size: int
    uploaded_at: datetime
    s3_key: str


class UploadResponse(BaseModel):
    message: str
    file_name: str
    s3_key: str
    chunks_indexed: int


class ChatRequest(BaseModel):
    question: str = Field(min_length=3, max_length=4000)


class ChatSource(BaseModel):
    document_name: str
    page_number: int | None = None
    score: float
    text: str


class ChatResponse(BaseModel):
    answer: str
    sources: list[ChatSource]

