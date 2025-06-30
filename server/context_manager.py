"""
Context Manager

Manages conversation context for each user or chat session.
Stores recent messages and provides context windows for AI modules.
"""

from collections import defaultdict, deque

class ContextManager:
    def __init__(self, window_size=5):
        """
        Args:
            window_size (int): Number of recent messages to keep per user/session.
        """
        self.window_size = window_size
        self.contexts = defaultdict(lambda: deque(maxlen=self.window_size))

    def add_message(self, user, message):
        """
        Add a message to the user's context.

        Args:
            user (str): User or session identifier.
            message (str): Message content.
        """
        self.contexts[user].append(message)

    def get_context(self, user):
        """
        Get the recent message context for a user.

        Args:
            user (str): User or session identifier.

        Returns:
            list: List of recent messages (oldest first).
        """
        return list(self.contexts[user])

    def clear_context(self, user):
        """
        Clear the context for a user.

        Args:
            user (str): User or session identifier.
        """
        self.contexts[user].clear()

    def clear_all(self):
        """Clear all contexts."""
        self.contexts.clear()

# Example usage:
# ctx_mgr = ContextManager(window_size=5)
# ctx_mgr.add_message("alice", "Hello!")
# ctx_mgr.add_message("alice", "How are you?")
# print(ctx_mgr.get_context("alice"))