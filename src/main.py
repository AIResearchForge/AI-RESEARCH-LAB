"""Main entry point for AI Research Lab."""

import os
import sys
from dotenv import load_dotenv
from .graph import run_research_lab

load_dotenv()

# Set USER_AGENT (silences the warning)
if not os.getenv("USER_AGENT"):
    os.environ["USER_AGENT"] = "AI-Research-Lab/1.0"


def main():
    """Main interactive function."""

    print("\n" + "=" * 60)
    print("🧠 AI RESEARCH LAB — Scientific Agent")
    print("=" * 60)
    print(f"📦 Model: {os.getenv('MODEL_NAME', 'gpt-4o-mini')}")
    print("=" * 60 + "\n")

    session_counter = 0

    while True:
        topic = input("🔬 Enter research topic: ")

        if topic.lower() in ["exit", "quit", "q"]:
            print("\n👋 Goodbye!")
            break

        if not topic.strip():
            print("⚠️ Please enter a topic.\n")
            continue

        session_counter += 1
        thread_id = f"research-session-{session_counter:03d}"

        try:
            result = run_research_lab(topic, thread_id=thread_id)

            print("\n" + "=" * 60)
            print("📋 RESEARCH PAPER:")
            print("=" * 60)
            print(result)
            print("=" * 60 + "\n")

        except KeyboardInterrupt:
            print("\n\n⏹️ Interrupted by user.")
            break

        except Exception as e:
            print(f"\n❌ Error: {str(e)}\n")
            print("💡 Try again with a different topic or check the logs.\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)

