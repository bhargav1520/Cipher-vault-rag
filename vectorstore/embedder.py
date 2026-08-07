from sentence_transformers import SentenceTransformer
from config import EMBEDDING_MODEL

_model = None  # loaded once, reused across calls


def get_embedder() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer(EMBEDDING_MODEL)
    return _model


def embed_text(text: str) -> list[float]:
    model = get_embedder()
    return model.encode(text).tolist()
