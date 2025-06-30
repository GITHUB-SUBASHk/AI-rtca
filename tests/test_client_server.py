"""
Integration test for client/server communication.
"""

import unittest
import socket
import threading
import time

HOST = "127.0.0.1"
PORT = 5000

class TestClientServerIntegration(unittest.TestCase):
    def setUp(self):
        # Start the server in a background thread
        from server.main_server import receive
        self.server_thread = threading.Thread(target=receive, daemon=True)
        self.server_thread.start()
        time.sleep(1)  # Give server time to start

    def test_client_connection(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST, PORT))
        client.send(b"testuser")
        client.close()

if __name__ == "__main__":
    unittest.main()