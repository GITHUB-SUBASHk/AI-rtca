"""
Tone Model

Analyzes the emotional tone of a message using TextBlob.
Can be extended later to support transformer-based sentiment detection.
"""

from textblob import TextBlob

def analyze_tone(message: str) -> str:
    """
    Determine the tone of the message.

    Returns:
        One of: 'positive', 'neutral', 'negative'
    """
    if not message.strip():
        return "neutral"

    blob = TextBlob(message)
    polarity = blob.sentiment.polarity

    if polarity > 0.2:
        return "positive"
    elif polarity < -0.2:
        return "negative"
    else:
        return "neutral"

# Optional: Categorize into richer tones
def classify_emotion(message: str) -> str:
    tone = analyze_tone(message)
    if tone == "positive":
        if "!" in message or "great" in message.lower():
            return "excited"
        elif "thanks" in message.lower():
            return "friendly"
    elif tone == "negative":
        if "why" in message.lower() or "not" in message.lower():
            return "sarcastic"
        else:
            return "formal"
    return "neutral"

# Example:
# print(analyze_tone("I'm so happy this is working!"))
# print(classify_emotion("Thanks a lot for helping!"))