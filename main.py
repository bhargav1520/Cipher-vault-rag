import argparse
import uuid

from config import SAMPLE_DOCS_DIR
from crypto.keymanager import get_or_create_key
from crypto.encryption import encrypt_chunk, decrypt_chunk
from ingestion.loader import load_documents
from ingestion.chunker import chunk_text
from vectorstore.embedder import embed_text
from vectorstore.store import add_embedding
from storage.encrypted_store import save_encrypted_chunk, get_encrypted_chunk
from pipeline.retriever import retrieve_chunk_ids
from pipeline.guardrail import is_extraction_attempt, is_low_confidence
from pipeline.generator import generate_answer


def ingest():
    key = get_or_create_key()
    docs = load_documents(SAMPLE_DOCS_DIR)
    total_chunks = 0
    for doc in docs:
        for piece in chunk_text(doc["text"]):
            chunk_id = str(uuid.uuid4())
            embedding = embed_text(piece)                    # embed plaintext
            add_embedding(chunk_id, embedding, {"doc_id": doc["doc_id"]})  # store embedding only
            blob = encrypt_chunk(piece, key)                  # encrypt for storage
            save_encrypted_chunk(chunk_id, blob)
            total_chunks += 1
    print(f"Ingested {len(docs)} document(s) into {total_chunks} encrypted chunks.")


def ask(query: str):
    key = get_or_create_key()

    if is_extraction_attempt(query):
        print("I can summarize relevant content, but I won't reproduce raw document text verbatim.")
        return

    chunk_ids, distances = retrieve_chunk_ids(query)

    if is_low_confidence(distances):
        print("I don't have enough relevant information to answer that confidently.")
        return

    decrypted_chunks = [decrypt_chunk(get_encrypted_chunk(cid), key) for cid in chunk_ids]
    answer = generate_answer(query, decrypted_chunks)
    print(answer)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CipherVault RAG CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("ingest", help="Encrypt and index all docs in sample_docs/")

    ask_parser = sub.add_parser("ask", help="Ask a question against the indexed docs")
    ask_parser.add_argument("query")

    args = parser.parse_args()

    if args.command == "ingest":
        ingest()
    elif args.command == "ask":
        ask(args.query)
