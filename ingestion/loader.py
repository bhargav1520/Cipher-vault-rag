import os


def load_documents(folder: str) -> list[dict]:
    """Read every .txt file in folder. Returns list of {doc_id, text}."""
    docs = []
    for filename in sorted(os.listdir(folder)):
        if not filename.endswith(".txt"):
            continue
        path = os.path.join(folder, filename)
        with open(path, "r", encoding="utf-8") as f:
            docs.append({"doc_id": filename, "text": f.read()})
    return docs
