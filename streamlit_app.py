import streamlit as st
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

st.set_page_config(page_title="CipherVault RAG", page_icon="🔒")
st.title("🔒 CipherVault RAG")
st.caption("A fully local, encrypted retrieval-augmented generation pipeline")

with st.sidebar:
    st.header("1. Index documents")
    st.write("Encrypts and indexes every .txt file in sample_docs/")
    if st.button("Run ingest"):
        with st.spinner("Encrypting and indexing..."):
            key = get_or_create_key()
            docs = load_documents(SAMPLE_DOCS_DIR)
            total_chunks = 0
            for doc in docs:
                for piece in chunk_text(doc["text"]):
                    chunk_id = str(uuid.uuid4())
                    embedding = embed_text(piece)
                    add_embedding(chunk_id, embedding, {"doc_id": doc["doc_id"]})
                    blob = encrypt_chunk(piece, key)
                    save_encrypted_chunk(chunk_id, blob)
                    total_chunks += 1
        st.success(f"Ingested {len(docs)} document(s) into {total_chunks} encrypted chunks.")

st.header("2. Ask a question")
query = st.text_input("Your question", placeholder="e.g. What's the rate limit for the API?")

if st.button("Ask") and query:
    key = get_or_create_key()

    if is_extraction_attempt(query):
        st.warning("I can summarize relevant content, but I won't reproduce raw document text verbatim.")
    else:
        with st.spinner("Retrieving and generating..."):
            chunk_ids, distances = retrieve_chunk_ids(query)

            if is_low_confidence(distances):
                st.warning("I don't have enough relevant information to answer that confidently.")
            else:
                decrypted_chunks = [decrypt_chunk(get_encrypted_chunk(cid), key) for cid in chunk_ids]
                answer = generate_answer(query, decrypted_chunks)
                st.success(answer)

                with st.expander("Show retrieved context (decrypted only for this query)"):
                    for i, chunk in enumerate(decrypted_chunks):
                        st.caption(f"Chunk {i+1} — similarity distance: {distances[i]:.3f}")
                        st.code(chunk)