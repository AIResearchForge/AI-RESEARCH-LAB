# src/memory.py (custom memory, no LangChain dependencies)


class SimpleMemory:
    """Simple memory for storing conversation history."""

    def __init__(self):
        self.history = []

    def add_message(self, role: str, content: str):
        """Adds a message to the history."""
        self.history.append({"role": role, "content": content})

    def get_history(self) -> list:
        """Returns the entire conversation history."""
        return self.history

    def clear(self):
        """Clears the history."""
        self.history = []

    def __str__(self):
        return f"SimpleMemory({len(self.history)} messages)"


def get_memory_base():
    """Creates and returns a simple memory."""
    return SimpleMemory()


__all__ = ["SimpleMemory", "get_memory_base"]
