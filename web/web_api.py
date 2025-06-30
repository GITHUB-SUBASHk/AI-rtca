"""
FastAPI Web API for AI Chat
- POST /chat: Send a message and get an AI reply
- GET /health: Health check endpoint
"""

from fastapi import FastAPI, Request
from pydantic import BaseModel
from ai.reply_predictor import generate_reply

app = FastAPI(title="AI Chat API")

class ChatRequest(BaseModel):
    user: str
    message: str

class ChatResponse(BaseModel):
    reply: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(req: ChatRequest):
    reply = generate_reply(req.message, req.user)
    return {"reply": reply}

# To run: uvicorn web.web_api:app --reloads