import chromadb
from config import CHROMA_DIR, CHROMA_COLLECTION

_client = None


def get_collection():
    global _client
    if _client is None:
        _client = chromadb.PersistentClient(path=CHROMA_DIR)
    return _client.get_or_create_collection(CHROMA_COLLECTION)


def add_embedding(chunk_id: str, embedding: list[float], metadata: dict):
    """Note: only the embedding + metadata go here. The actual chunk text
    is never passed to this function — it lives only in the encrypted store."""
    collection = get_collection()
    collection.add(ids=[chunk_id], embeddings=[embedding], metadatas=[metadata])


def query_embedding(embedding: list[float], top_k: int):
    collection = get_collection()
    return collection.query(query_embeddings=[embedding], n_results=top_k)
