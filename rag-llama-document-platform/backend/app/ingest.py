from embedding_service import embed_text
from pdf_processor import extract_text
from text_splitter import split_text
from vector_db import init_collection, store_chunks


def process_pdf(file_path: str) -> None:
    text = extract_text(file_path)
    chunks = split_text(text)
    embeddings = [embed_text(chunk) for chunk in chunks]

    init_collection()
    store_chunks(chunks, embeddings)

