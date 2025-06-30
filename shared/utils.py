"""
Shared utility functions for the chat AI system.
"""

import re
from datetime import datetime
import hashlib
import base64

def strip_html_tags(text):
    """Remove HTML tags from a string."""
    return re.sub(r'<[^>]+>', '', text)

def is_valid_username(username):
    """Check if a username is valid (alphanumeric, 3-20 chars)."""
    return bool(re.match(r'^[a-zA-Z0-9_]{3,20}$', username))

def current_utc_timestamp():
    """Return the current UTC timestamp as an ISO string."""
    return datetime.utcnow().isoformat()

def hash_text(text):
    """Return a SHA-256 hash of the given text."""
    return hashlib.sha256(text.encode()).hexdigest()

def base64_encode(text):
    """Base64-encode a string."""
    return base64.b64encode(text.encode()).decode()

def base64_decode(text):
    """Base64-decode a string."""
    return base64.b64decode(text.encode()).decode()