from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer


client = QdrantClient(path="qdrant_db")
model = SentenceTransformer("BAAI/bge-small-en")

COLLECTION = "documents"


def search(query: str) -> list[str]:
    vector = model.encode(query).tolist()

    results = client.search(
        collection_name=COLLECTION,
        query_vector=vector,
        limit=5,
    )

    return [result.payload["text"] for result in results]

