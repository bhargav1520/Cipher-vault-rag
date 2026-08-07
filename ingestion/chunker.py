from config import CHUNK_SIZE, CHUNK_OVERLAP


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """Sliding-window chunker over characters.

    Good enough for a demo project. If you want smarter splitting on
    sentence/paragraph boundaries later, swap this for LangChain's
    RecursiveCharacterTextSplitter — same function signature, drop-in
    replacement.
    """
    chunks = []
    start = 0
    text = text.strip()
    while start < len(text):
        end = start + chunk_size
        piece = text[start:end].strip()
        if piece:
            chunks.append(piece)
        start += chunk_size - overlap
    return chunks
