import json
import os
from datetime import datetime
from cryptography.fernet import Fernet
from shared.encryption_utils import generate_key_from_password, encrypt_message, decrypt_message
from client.privacy_guard import PrivacyGuard

class MessageLogger:
    """
    Hybrid logger: Each message is a JSON line (JSONL), with optional per-message encryption.
    Fast, robust, and privacy-friendly.
    """
    def __init__(self, user, password=None):
        self.user = user
        self.log_dir = "client/logs"
        self.filename = os.path.join(self.log_dir, f"{user}_logs.jsonl")
        self.privacy = PrivacyGuard()
        self.fernet = None

        os.makedirs(self.log_dir, exist_ok=True)

        # Setup encryption if enabled
        if self.privacy.config.get("log_encrypted", True):
            if password is None:
                password = self.privacy.config.get("log_password", "defaultpassword")
            key = generate_key_from_password(password)
            self.fernet = Fernet(key)

    def log_message(self, content, direction):
        """
        Log a message as a JSON line with timestamp and direction ('sent' or 'received').
        Each line is a separate JSON object.
        """
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "type": direction,
            "content": encrypt_message(content, self.fernet) if self.fernet else content
        }
        with open(self.filename, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")

    def read_messages(self):
        """
        Generator: yields each log entry (decrypted if needed).
        """
        if not os.path.exists(self.filename):
            return
        with open(self.filename, "r", encoding="utf-8") as f:
            for line in f:
                entry = json.loads(line)
                if self.fernet and isinstance(entry["content"], str):
                    try:
                        entry["content"] = decrypt_message(entry["content"], self.fernet)
                    except Exception:
                        entry["content"] = "[DECRYPTION FAILED]"
                yield entry

# Example:
# logger = MessageLogger("alice")
# logger.log_message("Hello!", "sent")
# for msg in logger.read_messages():
#     print(msg)
