from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# If your AI reply logic exists:
# from ai.reply_predictor import generate_reply

app = FastAPI()

# Enable CORS (for safety with frontend requests)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve the frontend static files
app.mount("/", StaticFiles(directory="web/static", html=True), name="static")

@app.post("/generate-reply")
async def generate_reply_endpoint(request: Request):
    data = await request.json()
    user_message = data.get("message", "")
    
    # Replace this with your AI logic
    # reply = generate_reply(user_message)
    reply = f"You said: {user_message}"  # Stub for testing

    return JSONResponse(content={"reply": reply})
