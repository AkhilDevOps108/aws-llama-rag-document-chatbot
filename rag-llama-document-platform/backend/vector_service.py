from qdrant_client import QdrantClient


# Local embedded Qdrant database for simple testing without Docker.
client = QdrantClient(path="qdrant_db")

print("Qdrant initialized")
