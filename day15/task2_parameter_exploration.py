"""
task2_parameter_exploration.py
==============================
Day 15 - Task 2: API Parameter Exploration (using Groq - free tier)

Systematically tests three key parameters:
    1. temperature  - controls randomness (0.0 to 1.5)
    2. max_tokens   - hard cap on response length (observe truncation)
    3. top_p        - nucleus sampling (focused vs diverse)

For each parameter, a fixed prompt is tested at multiple values
and results are printed for comparison.

Usage:
    python task2_parameter_exploration.py

Requires:
    GROQ_API_KEY in a .env file.
    pip install groq python-dotenv
"""

import os
import textwrap

from dotenv import load_dotenv
from groq import Groq


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

MODEL = "llama-3.3-70b-versatile" 


# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------

def get_client() -> Groq:
    """Load API key and return an authenticated Groq client.

    Returns:
        Groq: Authenticated Groq client.

    Raises:
        EnvironmentError: If GROQ_API_KEY is missing from environment.
    """
    load_dotenv()
    key = os.getenv("GROQ_API_KEY")
    if not key:
        raise EnvironmentError(
            "GROQ_API_KEY not found. Add it to your .env file."
        )
    return Groq(api_key=key)


# ---------------------------------------------------------------------------
# Generic API call
# ---------------------------------------------------------------------------

def call_api(
    client: Groq,
    prompt: str,
    temperature: float = 0.7,
    max_tokens: int = 150,
    top_p: float = 1.0,
) -> dict:
    """Make a chat completion call with explicit parameter control.

    Args:
        client (Groq): Authenticated Groq client.
        prompt (str): User message to send.
        temperature (float): Randomness control (0.0-2.0). Default 0.7.
        max_tokens (int): Max output tokens. Default 150.
        top_p (float): Nucleus sampling threshold (0.0-1.0). Default 1.0.

    Returns:
        dict: Keys - 'text', 'prompt_tokens', 'completion_tokens',
              'total_tokens', 'finish_reason'.
              finish_reason is 'stop' (complete) or 'length' (truncated).

    Example:
        >>> r = call_api(client, "Hello!", temperature=0.0, max_tokens=10)
        >>> print(r['finish_reason'])
    """
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
    )
    choice = response.choices[0]
    return {
        "text": choice.message.content,
        "prompt_tokens": response.usage.prompt_tokens,
        "completion_tokens": response.usage.completion_tokens,
        "total_tokens": response.usage.total_tokens,
        "finish_reason": choice.finish_reason,
    }


# ---------------------------------------------------------------------------
# Experiment 1 - Temperature
# ---------------------------------------------------------------------------

def experiment_temperature(client: Groq) -> None:
    """Test the same creative prompt at temperatures 0.0, 0.7, and 1.5.

    Args:
        client (Groq): Authenticated Groq client.

    Returns:
        None
    """
    prompt = (
        "Write a two-sentence description of a robot learning to paint."
    )
    values = [0.0, 0.7, 1.5]

    print("\n" + "=" * 65)
    print("EXPERIMENT 1 - TEMPERATURE")
    print(f'Prompt: "{prompt}"')
    print("=" * 65)

    for temp in values:
        result = call_api(client, prompt, temperature=temp, max_tokens=80)
        short = textwrap.shorten(
            result["text"].strip(), width=60, placeholder="..."
        )
        print(f"\n  [temperature = {temp}]")
        print(f"  Response     : {short}")
        print(
            f"  finish_reason: {result['finish_reason']} | "
            f"tokens: {result['total_tokens']}"
        )


# ---------------------------------------------------------------------------
# Experiment 2 - max_tokens
# ---------------------------------------------------------------------------

def experiment_max_tokens(client: Groq) -> None:
    """Test how max_tokens truncates the response at 15, 50, and 200.

    finish_reason = 'length' means the response was cut off.
    finish_reason = 'stop'   means the response completed normally.

    Args:
        client (Groq): Authenticated Groq client.

    Returns:
        None
    """
    prompt = (
        "Explain the three main layers of a neural network: "
        "input, hidden, and output. Be detailed."
    )
    limits = [15, 50, 200]

    print("\n" + "=" * 65)
    print("EXPERIMENT 2 - MAX_TOKENS (truncation test)")
    print(f'Prompt: "{prompt}"')
    print("=" * 65)

    for limit in limits:
        result = call_api(
            client, prompt, temperature=0.3, max_tokens=limit
        )
        cut = result["finish_reason"] == "length"
        flag = " << TRUNCATED" if cut else " << COMPLETE"
        print(f"\n  [max_tokens = {limit}]{flag}")
        print(f"  finish_reason     : {result['finish_reason']}")
        print(f"  completion_tokens : {result['completion_tokens']}")
        print(f"  Response          : {result['text'].strip()}")


# ---------------------------------------------------------------------------
# Experiment 3 - top_p
# ---------------------------------------------------------------------------

def experiment_top_p(client: Groq) -> None:
    """Test top_p at 0.1 (focused), 0.5 (moderate), and 0.9 (diverse).

    Keep temperature at 1.0 when varying top_p, as recommended.

    Args:
        client (Groq): Authenticated Groq client.

    Returns:
        None
    """
    prompt = (
        "Describe the feeling of discovering a new idea for the first time."
    )
    values = [0.1, 0.5, 0.9]

    print("\n" + "=" * 65)
    print("EXPERIMENT 3 - TOP_P (nucleus sampling)")
    print(f'Prompt: "{prompt}"')
    print("temperature fixed at 1.0 during this test")
    print("=" * 65)

    for tp in values:
        result = call_api(
            client, prompt, temperature=1.0, max_tokens=80, top_p=tp
        )
        short = textwrap.shorten(
            result["text"].strip(), width=60, placeholder="..."
        )
        print(f"\n  [top_p = {tp}]")
        print(f"  Response : {short}")
        print(f"  Tokens   : {result['total_tokens']}")


# ---------------------------------------------------------------------------
# Summary table
# ---------------------------------------------------------------------------

def print_summary_table() -> None:
    """Print a static reference table: parameter, effect, best use case.

    Returns:
        None
    """
    print("\n" + "=" * 65)
    print("PARAMETER REFERENCE TABLE")
    print("=" * 65)
    print(f"{'Parameter':<22} | {'Effect':<20} | Best Use Case")
    print("-" * 65)
    rows = [
        ("temperature=0.0", "Deterministic",    "Factual Q&A, code"),
        ("temperature=0.7", "Balanced",          "General chat"),
        ("temperature=1.5", "Very creative",     "Brainstorming, fiction"),
        ("max_tokens=15",   "Hard cutoff",       "Cost testing"),
        ("max_tokens=200",  "Full answer",       "Detailed explanations"),
        ("top_p=0.1",       "Narrow vocabulary", "Precise output"),
        ("top_p=0.9",       "Broad vocabulary",  "Creative phrasing"),
    ]
    for param, effect, use in rows:
        print(f"  {param:<20} | {effect:<20} | {use}")
    print()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    """Run all three parameter experiments."""
    client = get_client()

    print("\nDAY 15 - TASK 2: PARAMETER EXPLORATION")

    experiment_temperature(client)
    experiment_max_tokens(client)
    experiment_top_p(client)
    print_summary_table()

    print("Task 2 complete!")


if __name__ == "__main__":
    main()
