"""
Unit tests for client/privacy_guard.py
"""

import unittest
from client.privacy_guard import PrivacyGuard

class TestPrivacyGuard(unittest.TestCase):
    def setUp(self):
        self.guard = PrivacyGuard()

    def test_ai_assist_enabled(self):
        self.assertIn(self.guard.is_ai_assist_enabled(), [True, False])

    def test_update_setting(self):
        self.guard.update_setting("enable_ai_assist", False)
        self.assertFalse(self.guard.is_ai_assist_enabled())

if __name__ == "__main__":
    unittest.main()