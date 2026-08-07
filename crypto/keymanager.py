import os
from config import KEY_FILE


def get_or_create_key() -> bytes:
    """Load the local AES key, generating one on first run.

    This is intentionally simple: a 256-bit key stored in a local file.
    Fine for a student/demo project. For production you'd use a proper
    KMS/HSM instead of a flat keyfile — worth saying out loud if asked
    about this in an interview, rather than overclaiming it.
    """
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as f:
            return f.read()

    key = os.urandom(32)  # 256-bit AES key
    with open(KEY_FILE, "wb") as f:
        f.write(key)
    return key
