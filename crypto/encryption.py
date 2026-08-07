import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

NONCE_SIZE = 12  # 96-bit nonce, standard for AES-GCM


def encrypt_chunk(plaintext: str, key: bytes) -> bytes:
    """Encrypt plaintext with AES-GCM. Returns nonce + ciphertext (+ auth tag).

    A fresh random nonce is generated on every call — never reuse a nonce
    with the same key, that's the one AES-GCM rule that actually matters.
    """
    aesgcm = AESGCM(key)
    nonce = os.urandom(NONCE_SIZE)
    ciphertext = aesgcm.encrypt(nonce, plaintext.encode("utf-8"), associated_data=None)
    return nonce + ciphertext


def decrypt_chunk(blob: bytes, key: bytes) -> str:
    """Reverse of encrypt_chunk. Raises if the blob was tampered with
    (that's the 'authenticated' part of AES-GCM working as intended)."""
    aesgcm = AESGCM(key)
    nonce, ciphertext = blob[:NONCE_SIZE], blob[NONCE_SIZE:]
    plaintext = aesgcm.decrypt(nonce, ciphertext, associated_data=None)
    return plaintext.decode("utf-8")
