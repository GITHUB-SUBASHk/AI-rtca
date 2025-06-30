import json
import os
from datetime import datetime
from client.utils.encryption_utils import generate_key_from_password, encrypt_message, decrypt_message
from client.privacy_guard import PrivacyGuard
from cryptography.fernet import Fernet

class MessageLogger:
    """
    Logs chat messages for a user, with optional encryption.
    Each log entry includes timestamp, type (sent/received), and content.
    """
    def __init__(self, user, password=None):
        self.user = user
        self.log_dir = "client/logs"
        self.filename = os.path.join(self.log_dir, f"{user}_logs.json")
        self.privacy = PrivacyGuard()
        self.fernet = None

        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

        # Setup encryption if enabled
        if self.privacy.config.get("log_encrypted", True):
            if password is None:
                password = self.privacy.config.get("log_password", "defaultpassword")
            key = generate_key_from_password(password)
            self.fernet = Fernet(key)

        # Initialize log file if missing
        if not os.path.exists(self.filename):
            self._write_log({"messages": []})

    def _read_log(self):
        with open(self.filename, "r", encoding="utf-8") as f:
            raw = f.read()
            if self.fernet:
                raw = decrypt_message(raw, self.fernet)
            return json.loads(raw)

    def _write_log(self, data):
        raw = json.dumps(data, indent=2)
        if self.fernet:
            raw = encrypt_message(raw, self.fernet)
        with open(self.filename, "w", encoding="utf-8") as f:
            f.write(raw)

    def log_message(self, content, direction):
        """
        Log a message with timestamp and direction ('sent' or 'received').
        """
        data = self._read_log()
        data["messages"].append({
            "timestamp": datetime.utcnow().isoformat(),
            "type": direction,
            "content": content
        })
        self._write_log(data)

# Example usage:
# logger = MessageLogger("alice")
# logger.log_message("Hello!", "sent")
# logger.log_message("Hi Alice!", "received")import json
import os
from datetime import datetime
from cryptography.fernet import Fernet
from client.utils.encryption_utils import generate_key_from_password, encrypt_message, decrypt_message
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

        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

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

# Example usage:
# logger = MessageLogger("alice")
# logger.log_message("Hello!", "sent")
# for msg in logger.read_messages():
#     print(msg)