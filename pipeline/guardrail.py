from config import MAX_DISTANCE

# Heuristic phrase list — a first-pass implementation of the concept,
# not a production-grade AI-safety filter. Say so if asked in interview.
EXTRACTION_PHRASES = [
    "repeat exactly", "verbatim", "word for word", "full text of",
    "copy the document", "print the entire", "dump the",
]


def is_extraction_attempt(query: str) -> bool:
    q = query.lower()
    return any(phrase in q for phrase in EXTRACTION_PHRASES)


from config import MAX_DISTANCE

def is_low_confidence(distances: list[float]) -> bool:
    """Chroma returns raw L2 distances (lower = more similar, unbounded above 1)."""
    if not distances:
        return True
    return min(distances) > MAX_DISTANCE


