from __future__ import annotations

from dataclasses import dataclass
from io import BytesIO

from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader
from transformers import AutoTokenizer

from app.config import get_settings


@dataclass
class DocumentChunk:
    text: str
    page_number: int | None


class DocumentProcessor:
    def __init__(self) -> None:
        settings = get_settings()
        tokenizer = AutoTokenizer.from_pretrained(settings.embedding_model)
        self.splitter = RecursiveCharacterTextSplitter.from_huggingface_tokenizer(
            tokenizer=tokenizer,
            chunk_size=500,
            chunk_overlap=50,
            separators=["\n\n", "\n", ". ", " ", ""],
        )

    def extract_chunks(self, pdf_bytes: bytes) -> list[DocumentChunk]:
        reader = PdfReader(BytesIO(pdf_bytes))
        chunks: list[DocumentChunk] = []

        for page_index, page in enumerate(reader.pages, start=1):
            text = (page.extract_text() or "").strip()
            if not text:
                continue

            for piece in self.splitter.split_text(text):
                cleaned = piece.strip()
                if cleaned:
                    chunks.append(DocumentChunk(text=cleaned, page_number=page_index))

        return chunks
