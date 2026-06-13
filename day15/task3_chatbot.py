"""
task3_chatbot.py
================
Day 15 - Task 3: Conversational Chatbot (using Groq - free tier)

Features:
    - System message to define chatbot personality
    - Conversation history maintained across turns (multi-turn context)
    - Error handling for API failures and rate limits
    - Per-turn and cumulative token usage tracking
    - Type 'quit' or 'exit' to end session with summary

Usage:
    python task3_chatbot.py

Requires:
    GROQ_API_KEY in a .env file.
    pip install groq python-dotenv
"""

import os
import sys

from dotenv import load_dotenv
from groq import Groq


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

MODEL = "llama-3.3-70b-versatile" 
MAX_TOKENS_PER_TURN = 300
TEMPERATURE = 0.7

SYSTEM_PROMPT = (
    "You are Zara, a friendly and concise AI learning assistant "
    "specializing in Python and machine learning. "
    "Keep answers under 4 sentences unless the user asks for more. "
    "If you do not know something, say so honestly."
)

EXIT_COMMANDS = {"quit", "exit", "bye", "q"}


# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------

def get_client() -> Groq:
    """Load API key and return an authenticated Groq client.

    Returns:
        Groq: Authenticated Groq client.

    Raises:
        EnvironmentError: If GROQ_API_KEY is missing.
    """
    load_dotenv()
    key = os.getenv("GROQ_API_KEY")
    if not key:
        raise EnvironmentError(
            "GROQ_API_KEY not found. "
            "Create a .env file with: GROQ_API_KEY=gsk_..."
        )
    return Groq(api_key=key)


# ---------------------------------------------------------------------------
# Single turn
# ---------------------------------------------------------------------------

def send_message(
    client: Groq,
    history: list,
) -> tuple:
    """Send conversation history to API and return reply + token counts.

    The system message is prepended at call time and not stored in history.

    Args:
        client (Groq): Authenticated Groq client.
        history (list): List of dicts with 'role' and 'content' keys.
            The last entry should be the new user message.

    Returns:
        tuple: (reply_text: str, prompt_tokens: int,
                completion_tokens: int)

    Raises:
        Exception: On API failures (connection, rate limit, etc.).

    Example:
        >>> reply, p, c = send_message(client,
        ...     [{"role": "user", "content": "Hi!"}])
    """
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS_PER_TURN,
    )
    reply = response.choices[0].message.content
    return (
        reply,
        response.usage.prompt_tokens,
        response.usage.completion_tokens,
    )


# ---------------------------------------------------------------------------
# Chatbot loop
# ---------------------------------------------------------------------------

def run_chatbot(client: Groq) -> None:
    """Run the interactive chatbot session in the terminal.

    Maintains full conversation history so the model remembers
    previous turns. Tracks token usage and cost per turn.

    Args:
        client (Groq): Authenticated Groq client.

    Returns:
        None
    """
    history = []
    total_prompt_tokens = 0
    total_completion_tokens = 0
    turn = 0

    print("\n" + "=" * 60)
    print("  ZARA - AI Learning Assistant  (Powered by Groq/Llama3)")
    print("  Type 'quit' or 'exit' to end the session.")
    print("=" * 60 + "\n")

    while True:

        # --- Get user input ---
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\n[Session ended]")
            break

        # --- Skip empty input ---
        if not user_input:
            print("Zara: Please type something!\n")
            continue

        # --- Check exit command ---
        if user_input.lower() in EXIT_COMMANDS:
            total = total_prompt_tokens + total_completion_tokens
            print(
                f"\nZara: Goodbye! Here's your session summary:\n"
                f"  Turns completed : {turn}\n"
                f"  Total tokens    : {total}\n"
                f"  (Groq free tier - no cost!)\n"
            )
            break

        # --- Add user message to history ---
        history.append({"role": "user", "content": user_input})

        # --- Call API with error handling ---
        try:
            reply, p_tokens, c_tokens = send_message(client, history)

        except Exception as exc:
            error_msg = str(exc)
            if "rate" in error_msg.lower():
                print("Zara: [Rate limit hit - wait a moment!]\n")
            elif "connect" in error_msg.lower():
                print("Zara: [Connection error - check internet.]\n")
            else:
                print(f"Zara: [API error: {error_msg[:60]}]\n")
            # Remove the failed user message from history
            history.pop()
            continue

        # --- Update history and counters ---
        history.append({"role": "assistant", "content": reply})
        total_prompt_tokens += p_tokens
        total_completion_tokens += c_tokens
        turn += 1

        # --- Display reply ---
        print(f"\nZara: {reply.strip()}")
        print(
            f"  [Turn {turn} | tokens: {p_tokens} in / "
            f"{c_tokens} out | Groq free]\n"
        )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    """Entry point for the chatbot."""
    try:
        client = get_client()
    except EnvironmentError as exc:
        print(f"ERROR: {exc}")
        sys.exit(1)

    run_chatbot(client)


if __name__ == "__main__":
    main()
