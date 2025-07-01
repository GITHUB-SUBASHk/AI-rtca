# CHAT-AI

A modular, privacy-aware, and AI-powered chat system with both terminal and web interfaces.  
Supports local and server-based AI, context-aware replies, privacy controls, and robust logging.

---

## Features

- **AI Reply Prediction:** Local rule-based or server LLM (Ollama, Flask, etc.)
- **Privacy Controls:** Configurable privacy guard, encrypted logs
- **Context Awareness:** Recent message context for smarter AI
- **Web API & Demo:** FastAPI backend and browser chat demo
- **Logging:** Per-user logs, optional encryption
- **Extensible:** Modular codebase for easy upgrades

---

## Project Structure

```
ai/
    local_small_llm.py         # Local AI/tone logic
    reply_predictor.py         # AI reply prediction logic
client/
    advanced_tone_model.py     # Tone analysis/generation
    context_vectorizer.py      # Context embedding
    main_client.py             # Terminal chat client
    privacy_guard.py           # Privacy settings/logic
server/
    context_manager.py         # Tracks conversation context
    llm_interface.py           # Unified LLM API (local/remote)
    main_server.py             # Multi-client chat server
    logs/
        alice_logs.json        # Example user log
        message_logger.py      # Logging utility
shared/
    constants.py               # Shared constants
    encryption_utils.py        # Encryption helpers
    utils.py                   # Shared utilities
tests/
    test_client_server.py      # Integration tests
    test_privacy_guard.py      # Privacy guard tests
    test_reply_predictor.py    # AI reply tests
web/
    web_api.py                 # FastAPI REST API
    static
static.index.html
static.custom.css
static.app.js              # Browser chat demo
```

---

## Getting Started

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Start the server

```bash
python server/main_server.py
```

### 3. (Optional) Start the FastAPI web API

```bash
uvicorn web.web_api:app --reload
```

### 4. Run the terminal client

```bash
python client/main_client.py
```

### 5. (Optional) Open the web demo

Open `web/web_demo.html` in your browser.  
If running the API on a different host/port, adjust the fetch URL in the HTML.

---

## Configuration

Edit `client/config.json` (if present) or adjust settings in `privacy_guard.py` for:
- AI backend selection (local/server)
- Privacy features
- Log encryption

---

## Testing

Run all tests with:

```bash
python -m unittest discover tests
```

---

## Extending

- Add new AI models in `ai/`
- Add more endpoints or web features in `web/`
- Expand privacy and logging as needed

---

## License

MIT License (or your choice)
