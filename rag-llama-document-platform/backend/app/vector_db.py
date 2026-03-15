from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams


client = QdrantClient(path="qdrant_db")

COLLECTION = "documents"


def init_collection() -> None:
    if COLLECTION not in [c.name for c in client.get_collections().collections]:
        client.create_collection(
            collection_name=COLLECTION,
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE,
            ),
        )


def store_vectors(vectors, chunks: list[str]) -> None:
    points = []

    for i, vector in enumerate(vectors):
        points.append(
            PointStruct(
                id=i,
                vector=vector.tolist(),
                payload={"text": chunks[i]},
            )
        )

    client.upsert(collection_name=COLLECTION, points=points)


def store_chunks(chunks: list[str], embeddings: list[list[float]]) -> None:
    points = []

    for i, vector in enumerate(embeddings):
        points.append(
            PointStruct(
                id=i,
                vector=vector,
                payload={"text": chunks[i]},
            )
        )

    client.upsert(
        collection_name=COLLECTION,
        points=points,
    )


def search(query_vector: list[float]) -> list[str]:
    results = client.query_points(
        collection_name=COLLECTION,
        query=query_vector,
        limit=5,
    )

    points = results.points if hasattr(results, "points") else results
    return [point.payload["text"] for point in points if point.payload and "text" in point.payload]
