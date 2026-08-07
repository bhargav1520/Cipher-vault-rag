import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAMPLE_DOCS_DIR = os.path.join(BASE_DIR, "sample_docs")
KEY_FILE = os.path.join(BASE_DIR, ".vault.key")          # never commit this
ENCRYPTED_DB = os.path.join(BASE_DIR, "encrypted_chunks.db")
CHROMA_DIR = os.path.join(BASE_DIR, "chroma_store")
CHROMA_COLLECTION = "cipher_vault_chunks"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"   # small, local, no API key needed
OLLAMA_MODEL = "llama3.2:3b"           # pull with: ollama pull llama3.2:3b

CHUNK_SIZE = 400       # characters per chunk
CHUNK_OVERLAP = 60     # overlap between consecutive chunks
TOP_K = 3              # how many chunks to retrieve per query
MAX_DISTANCE = 1.0   # tune this based on real query results