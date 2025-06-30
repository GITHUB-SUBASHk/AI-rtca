### File: server/main_server.py

import socket
import threading
import time
import re
from ai.filter_nlp import sanitize_message

from server.logs.message_logger import MessageLogger
from shared.encryption_utils import simple_sanitize 
 # Assumes a helper to strip risky input
from logs.message_logger import ServerMessageLogger
logger = ServerMessageLogger()

HOST = '127.0.0.1'
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
nicknames = []
last_message_time = {}  # rate limiting (addr -> last timestamp)

# Optional: Auth tokens (demo purposes)
AUTHORIZED_USERS = {
    "alice": "token123",
    "bob": "secure456"
}

def broadcast(message, sender=None):
    for client in clients:
        if client != sender:
            try:
                client.send(message.encode('utf-8'))
            except:
                pass

def handle(client, address):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            now = time.time()
            if now - last_message_time.get(address, 0) < 1:  # 1s throttle
                continue
            last_message_time[address] = now

            sanitized = simple_sanitize(message)
            broadcast(sanitized, sender=client)
        except:
            if client in clients:
                idx = clients.index(client)
                nickname = nicknames[idx]
                print(f"[-] {nickname} disconnected")
                broadcast(f"{nickname} left the chat.")
                clients.remove(client)
                nicknames.remove(nickname)
                client.close()
            break

def receive():
    print(f"[+] Server running on {HOST}:{PORT}...")
    while True:
        client, addr = server.accept()
        print(f"[+] Connected with {addr}")

        client.send("NICKNAME".encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')

        if nickname not in AUTHORIZED_USERS:
            client.send("[AUTH] Invalid user.".encode('utf-8'))
            client.close()
            continue

        clients.append(client)
        nicknames.append(nickname)
        broadcast(f"{nickname} joined the chat!")
        client.send("[✔] Connected to the server.".encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client, addr))
        thread.start()

receive()
message = client.recv(1024).decode('utf-8')
nickname = get_nickname_for_client(client)  # however you track nicknames
logger.log(nickname, message)
