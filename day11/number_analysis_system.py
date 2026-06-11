"""
Day 11 - Task 3: Number Analysis System
=========================================
While loops, mathematical optimisation, and an interactive game.

Covers:
  - Sieve of Eratosthenes (while loop + optimised inner loop)
  - Iterative factorial and Fibonacci with while loops
  - Number-guessing game with attempt limit and hint system

Author: Sehar Andleeb
Date: 2026-06-11
Internship: Xeven Solutions AI Engineering Internship 2026
"""

import random
import time


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
PRIME_LIMIT        = 100     # Find all primes up to this value
FACTORIAL_N        = 15      # Compute 15!
FIBONACCI_TERMS    = 20      # First N Fibonacci numbers
GAME_RANGE_MIN     = 1
GAME_RANGE_MAX     = 100
MAX_ATTEMPTS       = 7       # Limit for the guessing game


# ---------------------------------------------------------------------------
# Section 1 – Prime Numbers (while loop + optimisation)
# ---------------------------------------------------------------------------

def find_primes_trial_division(limit: int) -> list[int]:
    """
    Find all primes up to `limit` using trial division and a while loop.

    Optimisation: only test divisors up to √n (if n has a factor > √n,
    the paired factor must be < √n, so we would have found it already).

    Time complexity: O(n * √n).

    Args:
        limit: Upper bound (inclusive) for prime search.

    Returns:
        Sorted list of prime numbers up to `limit`.
    """
    primes = []

    candidate = 2                          # start testing from 2
    while candidate <= limit:              # outer while loop: each candidate

        is_prime = True
        divisor  = 2

        # Inner while loop: test divisors up to √candidate
        while divisor * divisor <= candidate:
            if candidate % divisor == 0:   # divisible → not prime
                is_prime = False
                break                      # break inner loop early (optimisation)
            divisor += 1

        if is_prime:
            primes.append(candidate)

        candidate += 1                     # move to next candidate

    return primes


def find_primes_sieve(limit: int) -> list[int]:
    """
    Find all primes up to `limit` using the Sieve of Eratosthenes.

    Much faster than trial division for large limits.
    Time complexity: O(n log log n).

    Args:
        limit: Upper bound (inclusive).

    Returns:
        Sorted list of prime numbers.
    """
    if limit < 2:
        return []

    # Boolean sieve: True means "still possibly prime"
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False    # 0 and 1 are not prime

    p = 2
    while p * p <= limit:               # only need to sieve up to √limit
        if is_prime[p]:
            # Mark all multiples of p as composite, starting from p²
            multiple = p * p
            while multiple <= limit:
                is_prime[multiple] = False
                multiple += p
        p += 1

    return [n for n in range(2, limit + 1) if is_prime[n]]


def demonstrate_primes() -> None:
    """Compare trial-division vs sieve and display results."""
    print(f"\n{'='*60}")
    print(f"  PRIME NUMBERS up to {PRIME_LIMIT}")
    print(f"{'='*60}")

    # Trial division
    start = time.perf_counter()
    primes_td = find_primes_trial_division(PRIME_LIMIT)
    td_time   = (time.perf_counter() - start) * 1_000

    # Sieve
    start      = time.perf_counter()
    primes_sv  = find_primes_sieve(PRIME_LIMIT)
    sieve_time = (time.perf_counter() - start) * 1_000

    print(f"  Trial division  : {len(primes_td)} primes  ({td_time:.4f} ms)")
    print(f"  Sieve           : {len(primes_sv)} primes  ({sieve_time:.4f} ms)")
    print(f"  Results match   : {primes_td == primes_sv}")
    print(f"\n  Primes: {primes_sv}\n")


# ---------------------------------------------------------------------------
# Section 2 – Factorial (iterative while loop)
# ---------------------------------------------------------------------------

def factorial_iterative(n: int) -> int:
    """
    Calculate n! using an iterative while loop (no recursion).

    Args:
        n: Non-negative integer.

    Returns:
        n! as an integer.

    Raises:
        ValueError: If n is negative.
    """
    if n < 0:
        raise ValueError(f"Factorial undefined for negative numbers (got {n}).")

    result = 1
    counter = 1               # start multiplying from 1

    while counter <= n:       # while loop replaces for-range
        result  *= counter
        counter += 1          # manual increment — essential in while loops!

    return result


def demonstrate_factorial() -> None:
    """Display factorial values up to FACTORIAL_N."""
    print(f"{'='*60}")
    print(f"  FACTORIAL  (iterative while loop)  —  1! to {FACTORIAL_N}!")
    print(f"{'='*60}")
    for i in range(1, FACTORIAL_N + 1):
        try:
            result = factorial_iterative(i)
            print(f"  {i:>2}!  =  {result:,}")
        except ValueError as e:
            print(f"  [ERROR] {e}")
    print()


# ---------------------------------------------------------------------------
# Section 3 – Fibonacci Sequence (iterative while loop)
# ---------------------------------------------------------------------------

def fibonacci_iterative(terms: int) -> list[int]:
    """
    Generate the first `terms` Fibonacci numbers using a while loop.

    Fibonacci definition:
      F(0) = 0,  F(1) = 1,  F(n) = F(n-1) + F(n-2)

    Args:
        terms: How many terms to generate.

    Returns:
        List of Fibonacci numbers.

    Raises:
        ValueError: If terms < 1.
    """
    if terms < 1:
        raise ValueError("Must request at least 1 Fibonacci term.")

    sequence = []
    a, b   = 0, 1             # seed values
    count  = 0

    while count < terms:      # while loop: keep going until we have enough terms
        sequence.append(a)
        a, b  = b, a + b      # simultaneous assignment — Pythonic swap
        count += 1

    return sequence


def demonstrate_fibonacci() -> None:
    """Display the first FIBONACCI_TERMS Fibonacci numbers."""
    print(f"{'='*60}")
    print(f"  FIBONACCI SEQUENCE  (iterative while loop)  —  first {FIBONACCI_TERMS} terms")
    print(f"{'='*60}")
    try:
        fib = fibonacci_iterative(FIBONACCI_TERMS)
        for idx, val in enumerate(fib):
            print(f"  F({idx:>2})  =  {val:,}")
    except ValueError as e:
        print(f"  [ERROR] {e}")
    print()


# ---------------------------------------------------------------------------
# Section 4 – Number Guessing Game (while loop + hint system)
# ---------------------------------------------------------------------------

def play_guessing_game(
    low: int  = GAME_RANGE_MIN,
    high: int = GAME_RANGE_MAX,
    max_attempts: int = MAX_ATTEMPTS,
    secret: int | None = None,   # injectable secret for automated tests
) -> dict:
    """
    Interactive number-guessing game with attempt limit and hint system.

    Loop structure:
    - Outer while loop: continue while attempts remain.
    - Break on correct guess.
    - Continue is implied via the loop's natural iteration.

    Args:
        low:          Lower bound of guessing range (inclusive).
        high:         Upper bound of guessing range (inclusive).
        max_attempts: Maximum allowed guesses.
        secret:       Pre-set secret number (None = random). Used for demos.

    Returns:
        Dictionary with keys: 'secret', 'attempts', 'won', 'guesses'.
    """
    # --- setup ---
    target   = secret if secret is not None else random.randint(low, high)
    attempts = 0
    guesses  = []
    won      = False

    print(f"\n{'='*60}")
    print(f"  NUMBER GUESSING GAME")
    print(f"  Range: {low}–{high}  |  Max attempts: {max_attempts}")
    print(f"{'='*60}")
    print("  (Running in demo mode — guesses are auto-generated)\n")

    # Simulate a binary-search strategy for the demo
    demo_low  = low
    demo_high = high

    while attempts < max_attempts:        # while loop: keep guessing

        # --- demo auto-guess (binary search) ---
        guess = (demo_low + demo_high) // 2
        guesses.append(guess)
        attempts += 1

        print(f"  Attempt {attempts}/{max_attempts}: Guessing {guess}")

        # --- evaluate guess ---
        if guess == target:
            print(f"  ✓ Correct! The number was {target}.")
            won = True
            break                          # break: no point guessing further

        elif guess < target:
            hint_range = f"higher than {guess}"
            demo_low   = guess + 1         # narrow the search window upward
        else:
            hint_range = f"lower than {guess}"
            demo_high  = guess - 1         # narrow the search window downward

        remaining = max_attempts - attempts
        print(f"  ✗ Wrong! The answer is {hint_range}. "
              f"{remaining} attempt(s) remaining.")

        # Hint: warm/cold proximity hint
        distance = abs(target - guess)
        if distance <= 5:
            print("  🔥 Very warm — you're very close!")
        elif distance <= 15:
            print("  ♨  Warm — getting closer.")
        elif distance <= 30:
            print("  ❄  Cold — still far away.")
        else:
            print("  🧊 Freezing — very far off!")

    # --- post-loop else block ---
    # The else clause of a while loop runs if the loop exits normally
    # (i.e., the condition became False) — NOT when break was used.
    else:
        print(f"\n  Out of attempts! The secret number was {target}.")

    return {
        "secret":   target,
        "attempts": attempts,
        "won":      won,
        "guesses":  guesses,
    }


def demonstrate_guessing_game() -> None:
    """Run three guessing-game scenarios with different secrets."""
    scenarios = [
        {"secret": 42, "label": "Mid-range number (42)"},
        {"secret": 1,  "label": "Edge case — minimum (1)"},
        {"secret": 99, "label": "Edge case — near maximum (99)"},
    ]

    for scenario in scenarios:
        print(f"\n  >>> Scenario: {scenario['label']}")
        result = play_guessing_game(secret=scenario["secret"])
        status = "WON ✓" if result["won"] else "LOST ✗"
        print(f"  Result: {status}  |  Guesses: {result['guesses']}")

    print()


# ---------------------------------------------------------------------------
# Bonus: While Loop Control Flow Demo
# ---------------------------------------------------------------------------

def demonstrate_loop_control() -> None:
    """
    Explicitly show break, continue, and while-else behaviour.
    """
    print(f"{'='*60}")
    print("  WHILE LOOP CONTROL FLOW DEMO")
    print(f"{'='*60}")

    # --- break demo ---
    print("\n  [break] Stop at first multiple of 7 above 20:")
    n = 1
    while n <= 50:
        if n > 20 and n % 7 == 0:
            print(f"  Found {n} — breaking loop.")
            break
        n += 1

    # --- continue demo ---
    print("\n  [continue] Print even numbers 1–20, skip odd:")
    n = 0
    evens = []
    while n < 20:
        n += 1
        if n % 2 != 0:
            continue       # skip odd numbers
        evens.append(n)
    print(f"  Even numbers: {evens}")

    # --- while-else demo ---
    print("\n  [while-else] Search for value 999 in a small list:")
    data   = [3, 14, 15, 92, 65, 35]
    target = 999
    idx    = 0
    while idx < len(data):
        if data[idx] == target:
            print(f"  Found {target} at index {idx}.")
            break
        idx += 1
    else:
        # else executes because while condition became False (no break hit)
        print(f"  {target} not found — while-else block executed.")

    print()


# ---------------------------------------------------------------------------
# Entry Point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    demonstrate_primes()
    demonstrate_factorial()
    demonstrate_fibonacci()
    demonstrate_loop_control()
    demonstrate_guessing_game()
