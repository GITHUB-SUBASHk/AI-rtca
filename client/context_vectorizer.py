"""
Context Vectorizer:
Encodes recent conversation into a compact vector or summary for smarter LLM prompts.
For now, this returns a joined recent message string — can be upgraded to use real embeddings.
"""

from typing import List

MAX_CONTEXT_MESSAGES = 6  # Adjustable: how many past messages to include

def get_context_vector(messages: List[dict]) -> str:
    """
    Generate a compact context string from recent messages.
    """
    if not messages:
        return ""

    relevant = messages[-MAX_CONTEXT_MESSAGES:]
    context = ""

    for msg in relevant:
        role = "You" if msg.get("type") == "sent" else "Them"
        content = msg.get("content", "")
        context += f"{role}: {content}\n"

    return context.strip()
