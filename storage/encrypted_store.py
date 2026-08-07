import sqlite3
from config import ENCRYPTED_DB


def _connect():
    conn = sqlite3.connect(ENCRYPTED_DB)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS chunks (chunk_id TEXT PRIMARY KEY, encrypted_blob BLOB)"
    )
    return conn


def save_encrypted_chunk(chunk_id: str, blob: bytes):
    conn = _connect()
    conn.execute(
        "INSERT OR REPLACE INTO chunks (chunk_id, encrypted_blob) VALUES (?, ?)",
        (chunk_id, blob),
    )
    conn.commit()
    conn.close()


def get_encrypted_chunk(chunk_id: str) -> bytes:
    conn = _connect()
    row = conn.execute(
        "SELECT encrypted_blob FROM chunks WHERE chunk_id = ?", (chunk_id,)
    ).fetchone()
    conn.close()
    if row is None:
        raise KeyError(f"No encrypted chunk found for {chunk_id}")
    return row[0]
