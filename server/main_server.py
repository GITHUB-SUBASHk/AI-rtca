"""
Main server for the AI chat application.
- Handles multiple clients using threads.
- Broadcasts messages to all clients.
- Optionally integrates with an AI backend for reply prediction or moderation.
"""

import socket
import threading
import requests  # For AI backend integration (optional)

HOST = '127.0.0.1'
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
nicknames = []

# Optional: Set to your AI backend URL if using AI features
AI_BACKEND_URL = "http://127.0.0.1:8080/chat"

def broadcast(message, sender=None):
    """Send a message to all connected clients except the sender."""
    for client in clients:
        if client != sender:
            try:
                client.send(message)
            except Exception as e:
                print(f"Error sending message: {e}")

def handle(client):
    """Handle communication with a single client."""
    while True:
        try:
            message = client.recv(1024)
            if not message:
                break

            # Optionally, send message to AI backend for moderation or reply
            # Uncomment below to enable AI reply suggestion to all
            # ai_reply = get_ai_reply(message.decode('utf-8'))
            # if ai_reply:
            #     broadcast(f"[AI]: {ai_reply}".encode('utf-8'))

            broadcast(message, sender=client)
        except Exception as e:
            print(f"Error: {e}")
            break

    # Remove client on disconnect
    if client in clients:
        index = clients.index(client)
        clients.remove(client)
        nickname = nicknames[index]
        broadcast(f"{nickname} left the chat.".encode('utf-8'))
        nicknames.remove(nickname)
        client.close()

def receive():
    """Accept new clients and start their handler threads."""
    print(f"Server running on {HOST}:{PORT}...")
    while True:
        client, address = server.accept()
        print(f"Connected with {address}")

        client.send("NICKNAME".encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)

        print(f"{nickname} joined. Total users: {len(clients)}")
        broadcast(f"{nickname} joined the chat!".encode('utf-8'))
        client.send("Connected to the server.".encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

def get_ai_reply(message, user="anon", context=None, tone="neutral"):
    """
    Sends a message to the AI backend and returns the AI's reply.
    """
    if context is None:
        context = []
    try:
        response = requests.post(
            AI_BACKEND_URL,
            json={
                "user": user,
                "message": message,
                "context": context,
                "tone": tone
            },
            timeout=5
        )
        if response.status_code == 200:
            return response.json().get("reply", "")
    except Exception as e:
        print(f"AI backend error: {e}")
    return None

if __name__ == "__main__":
    receive()