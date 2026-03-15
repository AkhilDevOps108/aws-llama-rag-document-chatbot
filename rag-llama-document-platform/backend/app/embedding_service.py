from functools import lru_cache

from sentence_transformers import SentenceTransformer


@lru_cache(maxsize=1)
def get_model() -> SentenceTransformer:
    return SentenceTransformer("BAAI/bge-small-en")


def create_embeddings(chunks: list[str]):
    vectors = get_model().encode(chunks)

    return vectors


def embed_text(text: str):
    return get_model().encode(text).tolist()
