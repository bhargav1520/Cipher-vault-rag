from vectorstore.embedder import embed_text
from vectorstore.store import query_embedding
from config import TOP_K


def retrieve_chunk_ids(query: str, top_k: int = TOP_K):
    """Returns (chunk_ids, distances) for the top_k closest chunks.
    Lower distance = more similar."""
    query_vec = embed_text(query)
    results = query_embedding(query_vec, top_k)
    chunk_ids = results["ids"][0]
    distances = results["distances"][0]
    return chunk_ids, distances
