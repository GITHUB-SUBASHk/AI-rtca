"""
AI Reply Predictor (Hybrid)

Routes between local transformer, hybrid mode, and remote LLM.
Uses privacy_guard settings to determine behavior.
Combines context-awareness, tone, fallback, and optional local refinement.
"""

from ai.local_small_llm import generate_local_reply, rewrite_tone
from server.llm_interface import get_llm_reply
from client.advanced_tone_model import analyze_tone
from server.logs.message_logger import MessageLogger
from client.privacy_guard import PrivacyGuard
from ai.filter_nlp import sanitize_message
from client.ai.context_vectorizer import get_context_vector

def generate_reply(message, user):
    """
    Generate a reply to a message using the configured AI backend.

    Args:
        message (str): The incoming user message.
        user (str): The username (for context/logging).

    Returns:
        str: The AI-generated reply.
    """
    config = PrivacyGuard().config

    # Gather recent context for smarter replies
    logger = MessageLogger(user)
    messages = logger._read_log().get("messages", [])
    context_vector = get_context_vector(messages)
    tone = analyze_tone(message)

    use_server = config.get("use_server_llm", False)
    use_local = config.get("use_local_llm", False)
    local_refine = config.get("local_refine", False)

    sanitized = sanitize_message(message)

    # Hybrid logic
    if use_server:
        try:
            server_reply = get_llm_reply(
                sanitized, backend="ollama", tone=tone, context_vector=context_vector
            )
            if local_refine:
                # Optionally refine server reply locally
                return rewrite_tone(server_reply, target_tone=tone)
            return server_reply
        except Exception as e:
            print(f"[ReplyPredictor] Server LLM failed: {e}")
            # Fallback to local reply if server fails
            return generate_local_reply(sanitized, tone=tone, context=messages)
    elif use_local:
        return generate_local_reply(sanitized, tone=tone, context=messages)
    else:
        # Default to local reply (safe fallback)
        return generate_local_reply(sanitized, tone=tone, context=messages)
