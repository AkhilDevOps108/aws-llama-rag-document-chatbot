from document_processor import extract_text, split_text
from embedding_service import create_embeddings
from vector_service import init_collection, store_vectors


def process_document(pdf_path: str) -> None:
    print("Extracting text...")
    text = extract_text(pdf_path)

    print("Splitting text...")
    chunks = split_text(text)

    print("Creating embeddings...")
    vectors = create_embeddings(chunks)

    print("Saving vectors...")
    init_collection()
    store_vectors(vectors, chunks)

    print("Document indexed successfully")

