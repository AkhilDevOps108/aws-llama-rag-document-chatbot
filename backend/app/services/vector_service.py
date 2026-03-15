from __future__ import annotations

from uuid import uuid4

from qdrant_client import QdrantClient
from qdrant_client.http import models as qdrant

from app.config import get_settings


class VectorService:
    def __init__(self) -> None:
        settings = get_settings()
        self.collection = settings.qdrant_collection
        self.client = QdrantClient(url=settings.qdrant_url)

    def ensure_collection(self, vector_size: int) -> None:
        collections = self.client.get_collections().collections
        if any(item.name == self.collection for item in collections):
            return

        self.client.create_collection(
            collection_name=self.collection,
            vectors_config=qdrant.VectorParams(size=vector_size, distance=qdrant.Distance.COSINE),
        )

    def upsert_chunks(self, embeddings: list[list[float]], chunks: list[dict[str, object]]) -> None:
        if not embeddings:
            return

        self.ensure_collection(len(embeddings[0]))
        points = [
            qdrant.PointStruct(id=str(uuid4()), vector=vector, payload=payload)
            for vector, payload in zip(embeddings, chunks, strict=True)
        ]
        self.client.upsert(collection_name=self.collection, points=points)

    def search(self, query_embedding: list[float], top_k: int) -> list[dict[str, object]]:
        if not self.client.collection_exists(self.collection):
            return []

        results = self.client.search(
            collection_name=self.collection,
            query_vector=query_embedding,
            limit=top_k,
            with_payload=True,
        )
        matches: list[dict[str, object]] = []

        for item in results:
            payload = item.payload or {}
            matches.append(
                {
                    "score": item.score,
                    "text": payload.get("text", ""),
                    "document_name": payload.get("document_name", "Unknown"),
                    "page_number": payload.get("page_number"),
                }
            )

        return matches

