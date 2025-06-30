"""
Unit tests for ai/reply_predictor.py
"""

import unittest
from ai.reply_predictor import generate_reply

class TestReplyPredictor(unittest.TestCase):
    def test_generate_reply_local(self):
        # Simulate a local LLM reply
        user = "testuser"
        message = "Hello!"
        reply = generate_reply(message, user)
        self.assertIsInstance(reply, str)
        self.assertTrue(len(reply) > 0)

if __name__ == "__main__":
    unittest.main()