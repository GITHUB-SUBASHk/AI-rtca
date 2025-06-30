import re
import base64
import hashlib
import os
from datetime import datetime, timedelta
from cryptography.fernet import Fernet

# --- Password-based Fernet (per-user/client) ---

def generate_key():
    return Fernet.generate_key()

def generate_key_from_password(password: str) -> bytes:
    sha = hashlib.sha256(password.encode()).digest()
    return base64.urlsafe_b64encode(sha)

def get_fernet(password: str) -> Fernet:
    return Fernet(generate_key_from_password(password))

# --- Rotating server-wide Fernet (for server logs) ---

KEY_ROTATION_DAYS = 7
KEY_FILE = "shared/rotating_key.key"
KEY_META_FILE = "shared/rotating_key_meta.json"

def get_rotating_fernet() -> Fernet:
    if not os.path.exists(KEY_FILE) or key_expired():
        new_key = generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(new_key)
        with open(KEY_META_FILE, "w", encoding="utf-8") as meta:
            meta.write(datetime.utcnow().isoformat())
    with open(KEY_FILE, "rb") as f:
        key = f.read()
    return Fernet(key)

def key_expired() -> bool:
    if not os.path.exists(KEY_META_FILE):
        return True
    with open(KEY_META_FILE, "r", encoding="utf-8") as meta:
        try:
            timestamp = datetime.fromisoformat(meta.read().strip())
            return datetime.utcnow() - timestamp > timedelta(days=KEY_ROTATION_DAYS)
        except Exception:
            return True

# --- Encryption/Decryption helpers ---

def encrypt_message(message: str, fernet: Fernet) -> str:
    return fernet.encrypt(message.encode()).decode()

def decrypt_message(token: str, fernet: Fernet) -> str:
    return fernet.decrypt(token.encode()).decode()

# --- Sanitization ---

def simple_sanitize(text: str) -> str:
    text = re.sub(r'<.*?>', '', text)  # Remove HTML tags
    text = re.sub(r'\x1b\[[0-9;]*[a-zA-Z]', '', text)  # Remove ANSI escape sequences
    text = re.sub(r'[\r\n]+', ' ', text)  # Normalize line breaks
    return text.strip()