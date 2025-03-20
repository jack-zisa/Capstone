import hashlib

def hash(s: str) -> str:
    """Hashes a username for storage."""
    return hashlib.sha256(s.encode()).hexdigest()