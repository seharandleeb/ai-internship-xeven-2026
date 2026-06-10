"""
Script Purpose: List Slicing Practice
Author: Sehar Andleeb
Company: Xeven Solutions
Day: 6 of 30 — Practical Task 3

This script demonstrates all slicing patterns on a list
of numbers from 1 to 20 with clear explanations for each.
"""


# ─── CONSTANTS ─────────────────────────────────────
SEPARATOR = "=" * 55
THIN_LINE = "-" * 55


def display_slice(label, explanation, sliced_list):
    """
    Display a slice with label and explanation.

    Parameters:
        label       (str): Slice syntax used
        explanation (str): What this slice does
        sliced_list (list): Result of the slice

    Returns:
        None
    """
    print(f"\n   Slice    : {label}")
    print(f"   What     : {explanation}")
    print(f"   Result   : {sliced_list}")
    print(f"   Length   : {len(sliced_list)} items")


def run_list_slicing():
    """
    Main function demonstrating all slicing patterns.

    Parameters: None
    Returns: None
    """
    print(f"\n{SEPARATOR}")
    print("   List Slicing Practice")
    print("   Day 6 — Practical Task 3")
    print(SEPARATOR)

    # ─── CREATE LIST 1 TO 20 ───────────────────────
    # range(1, 21) generates numbers from 1 to 20
    numbers = list(range(1, 21))

    print(f"\n{THIN_LINE}")
    print(f"   Original List")
    print(THIN_LINE)
    print(f"   {numbers}")
    print(f"   Length: {len(numbers)} items")
    print(THIN_LINE)

    # ─── FIRST 5 ELEMENTS ──────────────────────────
    # [:5] starts from 0, goes up to index 4
    display_slice(
        "numbers[:5]",
        "First 5 elements — start to index 4",
        numbers[:5]
    )

    # ─── LAST 5 ELEMENTS ───────────────────────────
    # [-5:] starts from 5th last item to end
    display_slice(
        "numbers[-5:]",
        "Last 5 elements — 5th from end to last",
        numbers[-5:]
    )

    # ─── EVERY 3RD ELEMENT ─────────────────────────
    # [::3] starts from 0, takes every 3rd item
    display_slice(
        "numbers[::3]",
        "Every 3rd element — step of 3",
        numbers[::3]
    )

    # ─── REVERSE ENTIRE LIST ───────────────────────
    # [::-1] starts from end, goes backwards
    display_slice(
        "numbers[::-1]",
        "Reverse entire list — step of -1",
        numbers[::-1]
    )

    # ─── MIDDLE 10 ELEMENTS ────────────────────────
    # [5:15] starts at index 5, ends at index 14
    display_slice(
        "numbers[5:15]",
        "Middle 10 elements — index 5 to 14",
        numbers[5:15]
    )

    # ─── BONUS SLICES ──────────────────────────────
    print(f"\n{THIN_LINE}")
    print("   BONUS SLICES")
    print(THIN_LINE)

    # Every 2nd element
    display_slice(
        "numbers[::2]",
        "Every 2nd element — all even indexed items",
        numbers[::2]
    )

    # First half
    display_slice(
        "numbers[:10]",
        "First half of the list",
        numbers[:10]
    )

    # Second half reversed
    display_slice(
        "numbers[10:][::-1]",
        "Second half reversed",
        numbers[10:][::-1]
    )

    print(f"\n{SEPARATOR}")
    print("   Task 3 completed successfully.")
    print(SEPARATOR)


# ─── ENTRY POINT ───────────────────────────────────
if __name__ == "__main__":
    run_list_slicing()