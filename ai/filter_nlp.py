"""
filter_nlp.py

Handles privacy-preserving preprocessing and NLP sanitization of input.
This module focuses on:
- Masking PII (emails, phone numbers, IPs)
- Filtering profanity
- Cleaning malformed/hostile input (XSS, ANSI codes, etc.)
"""

import re

# Extendable list for profanity filtering
BAD_WORDS = {"damn", "shit", "crap", "fuck"}  # You can load this from file if needed

def mask_pii(text: str) -> str:
    """
    Mask email, phone numbers, and IP addresses.
    """
    text = re.sub(r'\b\d{10}\b', '[PHONE]', text)
    text = re.sub(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', '[EMAIL]', text)
    text = re.sub(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', '[IP]', text)
    return text

def mask_profanity(text: str) -> str:
    """
    Replace profane words with [CENSORED].
    """
    def censor(match):
        word = match.group()
        return "[CENSORED]" if word.lower() in BAD_WORDS else word

    return re.sub(r'\b\w+\b', censor, text, flags=re.IGNORECASE)

def sanitize_message(text: str) -> str:
    """
    Clean and normalize a user message:
    - Remove HTML, ANSI codes, newlines, and extra whitespace.
    - Apply profanity and PII masking.
    """
    text = text.strip()
    text = mask_pii(text)
    text = mask_profanity(text)
    text = re.sub(r'<[^>]+>', '', text)                      # Strip HTML
    text = re.sub(r'\x1b\[[0-9;]*[a-zA-Z]', '', text)        # Strip ANSI
    text = re.sub(r'[\r\n]+', ' ', text)                     # Normalize newlines
    text = re.sub(r'\s{2,}', ' ', text)                      # Collapse whitespace
    return text.strip()
