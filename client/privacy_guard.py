"""
PrivacyGuard: Handles privacy-related settings and logic for the chat client.
Loads configuration from config.json and provides access to privacy features.
"""

import json
import os

class PrivacyGuard:
    DEFAULT_CONFIG = {
        "enable_ai_assist": True,
        "enable_autoreply": False,
        "allow_anonymized_stats": False,
        "log_encrypted": True,
        "use_server_llm": True,
        "local_refine": True,
        "log_password": "defaultpassword"
    }

    def __init__(self, config_path="config.json"):
        self.config_path = config_path
        self.config = self.load_config()

    def load_config(self):
        """Load privacy config from file or use defaults."""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    config = json.load(f)
                # Fill in any missing keys with defaults
                for k, v in self.DEFAULT_CONFIG.items():
                    config.setdefault(k, v)
                return config
            except Exception as e:
                print(f"[PrivacyGuard] Error loading config: {e}. Using defaults.")
        return self.DEFAULT_CONFIG.copy()

    def save_config(self):
        """Save current config to file."""
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"[PrivacyGuard] Error saving config: {e}")

    def is_ai_assist_enabled(self):
        return self.config.get("enable_ai_assist", True)

    def is_autoreply_enabled(self):
        return self.config.get("enable_autoreply", False)

    def is_anonymized_stats_allowed(self):
        return self.config.get("allow_anonymized_stats", False)

    def is_log_encrypted(self):
        return self.config.get("log_encrypted", True)

    def get_log_password(self):
        return self.config.get("log_password", "defaultpassword")

    def update_setting(self, key, value):
        """Update a privacy setting and save."""
        self.config[key] = value
        self.save_config()

    # Add more privacy-related methods as needed

# Example usage:
# privacy = PrivacyGuard()
# if privacy.is_ai_assist_enabled():
#     ...