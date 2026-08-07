# CipherVault RAG

A fully local, encrypted retrieval-augmented generation pipeline. Document
chunks are encrypted at rest with AES-GCM and only decrypted transiently
for the specific chunks retrieved at query time. No cloud calls, no API
keys — generation runs on a local model via Ollama.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate        # on Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Install Ollama (https://ollama.com), then pull a small local model:
ollama pull llama3.2:1b
```

## Usage

**Command line:**
```bash
# Encrypt and index everything in sample_docs/
python main.py ingest

# Ask a question
python main.py ask "How many remote work days are employees allowed?"
```

**Or via a simple web UI:**
```bash
streamlit run streamlit_app.py
```

## How it works

1. **Ingest**: documents are chunked, each chunk is embedded (plaintext, for
   semantic search) and then encrypted with AES-GCM before being written to
   disk. The vector store (ChromaDB) only ever holds embeddings + metadata —
   never raw text.
2. **Ask**: the query is embedded and matched against stored embeddings.
   Only the retrieved chunk IDs get decrypted, in memory, for that single
   query. A basic guardrail blocks verbatim-extraction attempts and
   low-confidence retrievals. The decrypted context plus the question go to
   a local LLM (Ollama) to generate the final answer.

## Notes on scope

- Key management uses a local keyfile (`.vault.key`, gitignored) — appropriate
  for a demo project, not a claim of production-grade key management.
- The guardrail is a heuristic first pass (a phrase check plus a distance
  threshold), not a full AI-safety evaluation system.
- Re-running `ingest` on the same documents currently appends new chunks
  rather than skipping duplicates. Clear `chroma_store/` and
  `encrypted_chunks.db` before re-ingesting the same files to avoid
  duplicate entries.

## Next steps (optional)

- Make `ingest` idempotent — skip or replace chunks for documents already indexed.
- Wrap `ingest`/`ask` in a FastAPI app for a proper `/ingest` and `/query` API.
- Swap the confidence threshold guardrail for a RAGAS-based groundedness score.