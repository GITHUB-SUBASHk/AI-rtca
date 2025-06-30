import random

GENERIC_RESPONSES = [
    "Got it!",
    "Okay, makes sense.",
    "Thanks for letting me know.",
    "Interesting, tell me more.",
    "That's helpful.",
]

TONE_REWRITE_RULES = {
    "friendly": lambda text: f"😊 Hey! {text}",
    "formal": lambda text: f"Kindly note: {text}",
    "sarcastic": lambda text: f"Oh wow, totally shocking… {text}",
    "excited": lambda text: f"🎉 Awesome!! {text}",
    "neutral": lambda text: text,
    "positive": lambda text: text + " 😊",
    "negative": lambda text: text + "...",
}

def rewrite_tone(message: str, target_tone: str = "neutral") -> str:
    rewriter = TONE_REWRITE_RULES.get(target_tone, lambda x: x)
    return rewriter(message)

def generate_local_reply(message: str, tone: str = "neutral", context: list = None) -> str:
    # Use context to slightly personalize the reply
    if context and any("hello" in m.get("content", "").lower() for m in context):
        base = "Hello again! How can I help you?"
    else:
        base = random.choice(GENERIC_RESPONSES)
    return rewrite_tone(base, tone)
