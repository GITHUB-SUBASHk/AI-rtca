"""
LLM Interface

Provides functions to interact with both remote and local language models (LLMs).
Supports:
- Remote LLMs (e.g., Ollama, Flask LLM server)
- Local tone/style rewriting
"""

import requests

# --- Remote LLM: Ollama Example ---
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "mistral"  # Change to "llama3" or your installed model

def get_ollama_reply(prompt, model=OLLAMA_MODEL):
    """
    Get a reply from a remote Ollama LLM server.
    """
    try:
        res = requests.post(OLLAMA_URL, json={
            "model": model,
            "prompt": prompt,
            "stream": False
        }, timeout=10)
        return res.json().get("response", "")
    except Exception as e:
        return f"[Ollama Error: {e}]"

# --- Remote LLM: Flask LLM Server Example ---
FLASK_LLM_URL = "http://localhost:8000/llm"

def get_flask_llm_reply(message):
    """
    Get a reply from a Flask-based LLM server (dummy or real).
    """
    try:
        res = requests.post(FLASK_LLM_URL, json={"message": message}, timeout=5)
        return res.json().get("reply", "")
    except Exception as e:
        return f"[Flask LLM Error: {e}]"

# --- Local LLM: Tone/Style Rewriting ---
def rewrite_tone(reply, target_tone="neutral"):
    """
    Rewrite the reply with the desired tone.
    """
    if target_tone == "positive":
        return reply + " 😊"
    elif target_tone == "negative":
        return reply + "..."
    elif target_tone == "neutral":
        return reply + "."
    else:
        return reply

# --- Unified Interface ---
def get_llm_reply(prompt, backend="ollama", tone=None):
    """
    Unified interface to get a reply from the chosen LLM backend.
    Args:
        prompt (str): The input prompt/message.
        backend (str): 'ollama', 'flask', or 'local'.
        tone (str): Optional tone for local rewriting.
    Returns:
        str: The LLM's reply.
    """
    if backend == "ollama":
        reply = get_ollama_reply(prompt)
    elif backend == "flask":
        reply = get_flask_llm_reply(prompt)
    elif backend == "local":
        reply = prompt  # Echo or implement your own logic
    else:
        reply = "[LLM Interface Error: Unknown backend]"
    if tone:
        reply = rewrite_tone(reply, tone)
    return reply

# Example usage:
# reply = get_llm_reply("Hello, how are you?", backend="ollama", tone="positive")