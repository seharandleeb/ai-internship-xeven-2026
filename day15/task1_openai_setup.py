"""
task1_openai_setup.py
=====================
Day 15 - Task 1: LLM API Setup & Basic Calls (using Groq - free tier)

Demonstrates:
    - Loading API key from .env file
    - Making a basic chat completion call
    - Printing response text and token usage
    - Comparing outputs at temperature 0.0, 0.7, and 1.5

Usage:
    python task1_openai_setup.py

Requires:
    GROQ_API_KEY set in a .env file in the project root.
    pip install groq python-dotenv
"""

import os

from dotenv import load_dotenv
from groq import Groq


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

MODEL = "llama-3.3-70b-versatile"  # Free model on Groq


# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------

def load_client() -> Groq:
    """Load API key from .env and return an authenticated Groq client.

    Returns:
        Groq: Authenticated Groq client instance.

    Raises:
        EnvironmentError: If GROQ_API_KEY is not found in the environment.

    Example:
        >>> client = load_client()
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
# Core API call
# ---------------------------------------------------------------------------

def get_completion(
    client: Groq,
    prompt: str,
    temperature: float = 0.7,
    max_tokens: int = 200,
) -> dict:
    """Send a prompt to the Groq API and return the response and usage.

    Args:
        client (Groq): Authenticated Groq client.
        prompt (str): The user message to send.
        temperature (float): Sampling temperature. 0.0 = deterministic,
            1.5 = highly creative. Defaults to 0.7.
        max_tokens (int): Maximum tokens in the response. Defaults to 200.

    Returns:
        dict: Keys:
            - 'text' (str): The model's response text.
            - 'prompt_tokens' (int): Input tokens used.
            - 'completion_tokens' (int): Output tokens used.
            - 'total_tokens' (int): Total tokens consumed.

    Example:
        >>> result = get_completion(client, "What is AI?")
        >>> print(result['text'])
    """
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return {
        "text": response.choices[0].message.content,
        "prompt_tokens": response.usage.prompt_tokens,
        "completion_tokens": response.usage.completion_tokens,
        "total_tokens": response.usage.total_tokens,
    }


# ---------------------------------------------------------------------------
# Temperature experiment
# ---------------------------------------------------------------------------

def temperature_experiment(client: Groq, prompt: str) -> None:
    """Run the same prompt at temperatures 0.0, 0.7, and 1.5.

    Prints a side-by-side comparison showing how temperature
    affects output randomness and creativity.

    Args:
        client (Groq): Authenticated Groq client.
        prompt (str): The prompt to test at each temperature.

    Returns:
        None

    Example:
        >>> temperature_experiment(client, "Write a one-sentence story.")
    """
    temperatures = [0.0, 0.7, 1.5]

    print("\n" + "=" * 65)
    print("TEMPERATURE EXPERIMENT")
    print(f'Prompt: "{prompt}"')
    print("=" * 65)

    for temp in temperatures:
        result = get_completion(client, prompt, temperature=temp)
        print(f"\n[Temperature = {temp}]")
        print(f"  Response : {result['text'].strip()}")
        print(
            f"  Tokens   : {result['prompt_tokens']} in / "
            f"{result['completion_tokens']} out / "
            f"{result['total_tokens']} total"
        )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    """Run basic API call then temperature experiment."""
    client = load_client()

    # --- Basic call ---
    print("\n" + "=" * 65)
    print("BASIC COMPLETION CALL")
    print("=" * 65)

    prompt = (
        "Explain what a Large Language Model is in two sentences, "
        "suitable for a beginner."
    )
    result = get_completion(client, prompt)

    print(f"Prompt  : {prompt}")
    print(f"Response: {result['text'].strip()}")
    print(
        f"Tokens  : {result['prompt_tokens']} in / "
        f"{result['completion_tokens']} out / "
        f"{result['total_tokens']} total"
    )

    # --- Temperature experiment ---
    temperature_experiment(
        client,
        prompt="Write a one-sentence creative tagline for an AI product.",
    )

    print("\nTask 1 complete!")


if __name__ == "__main__":
    main()
