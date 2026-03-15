from sentence_transformers import SentenceTransformer


model = SentenceTransformer("BAAI/bge-small-en")


def create_embeddings(chunks: list[str]):
    vectors = model.encode(chunks)

    return vectors

