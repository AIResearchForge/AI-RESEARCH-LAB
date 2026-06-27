"""Example topics for AI Research Lab tests."""

from pathlib import Path

EXAMPLE_TOPICS_FILE = Path(__file__).parent / "example_topics.txt"


def load_example_topics() -> list[str]:
    """Loads example topics from file."""

    if not EXAMPLE_TOPICS_FILE.exists():
        return [
            "LLM hallucinations and how to reduce them",
            "Quantum computing in drug discovery",
            "Impact of social media on mental health",
            "AI in medical diagnostics",
            "Climate change adaptation strategies",
            "Future of renewable energy storage",
            "Genetic engineering in crop improvement",
            "Dark matter and the structure of the universe",
        ]

    with open(EXAMPLE_TOPICS_FILE, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


__all__ = ["load_example_topics"]
