"""
Script Purpose: Number Classification System
Author: Sehar Andleeb
Company: Xeven Solutions
Day: 3 of 30

This script classifies numbers into multiple categories
including sign, even/odd, special types, and ranges.
It demonstrates nested conditionals and comparison operators.
"""


# ─── CONSTANTS ─────────────────────────────────────
SEPARATOR = "=" * 55
THIN_LINE = "-" * 55
APP_NAME  = "Number Classification System"


def display_header():
    """
    Display application header.

    Parameters: None
    Returns: None
    """
    print(f"\n{SEPARATOR}")
    print(f"   {APP_NAME}")
    print(f"   Day 3 — Conditional Statements and Logic")
    print(SEPARATOR)


def classify_sign(number):
    """
    Classify number as positive, negative, or zero.

    Parameters:
        number (float): Number to classify

    Returns:
        str: Sign classification
    """
    # ─── SIGN CLASSIFICATION ───────────────────────
    # Three possible cases: positive, negative, zero

    if number > 0:
        # Any number greater than zero is positive
        return "Positive"
    elif number < 0:
        # Any number less than zero is negative
        return "Negative"
    else:
        # Only zero reaches this condition
        return "Zero"


def classify_even_odd(number):
    """
    Classify whole number as even or odd.
    Decimal numbers cannot be classified as even or odd.

    Parameters:
        number (float): Number to classify

    Returns:
        str: Even, Odd, or not applicable
    """
    # ─── CHECK IF WHOLE NUMBER ─────────────────────
    # Decimal numbers cannot be even or odd
    if number != int(number):
        return "Not applicable — decimal number"

    # ─── EVEN OR ODD CHECK ─────────────────────────
    # A number is even if remainder when divided by 2 is 0
    elif int(number) % 2 == 0:
        return "Even"
    else:
        return "Odd"


def classify_special(number):
    """
    Identify any special properties of the number.

    Parameters:
        number (float): Number to classify

    Returns:
        str: Special property description
    """
    # ─── SPECIAL NUMBER CHECKS ─────────────────────
    # Check from most specific to most general

    if number == 0:
        # Zero is the additive identity
        return "Zero — additive identity"

    elif number == 1:
        # One is the multiplicative identity
        return "One — multiplicative identity"

    elif number == int(number) and number > 1:
        # ─── CHECK PERFECT SQUARE ──────────────────
        # A perfect square has a whole number square root
        square_root = number ** 0.5
        if square_root == int(square_root):
            return f"Perfect Square — square root is {int(square_root)}"
        else:
            return "Positive Integer"

    elif number == int(number) and number < 0:
        return "Negative Integer"

    else:
        return "Decimal Number"


def classify_magnitude(number):
    """
    Classify number based on its size or magnitude.

    Parameters:
        number (float): Number to classify

    Returns:
        str: Magnitude classification
    """
    # ─── MAGNITUDE RANGES ──────────────────────────
    # Use absolute value to check size regardless of sign

    if number == 0:
        return "Zero"
    elif -10 <= number <= 10:
        return "Single digit range"
    elif -100 <= number <= 100:
        return "Double digit range"
    elif -1000 <= number <= 1000:
        return "Triple digit range"
    else:
        return "Very large number"


def display_results(number):
    """
    Display complete classification results for a number.

    Parameters:
        number (float): Number to display results for

    Returns:
        None
    """
    print(f"\n{THIN_LINE}")
    print(f"   CLASSIFICATION RESULTS FOR: {number}")
    print(THIN_LINE)
    print(f"   Sign      : {classify_sign(number)}")
    print(f"   Even/Odd  : {classify_even_odd(number)}")
    print(f"   Special   : {classify_special(number)}")
    print(f"   Magnitude : {classify_magnitude(number)}")
    print(THIN_LINE)


def run_classifier():
    """
    Main function to run the number classification system.

    Parameters: None
    Returns: None
    """
    display_header()

    while True:
        try:
            # ─── GET USER INPUT ────────────────────
            user_input = input("   Enter a number: ").strip()

            # ─── CONVERT TO FLOAT ──────────────────
            # float() handles both integers and decimals
            number = float(user_input)

            # ─── DISPLAY CLASSIFICATION ────────────
            display_results(number)

        except ValueError:
            # ─── HANDLE NON-NUMERIC INPUT ──────────
            print("\n   Invalid input. Please enter a number only.")

        # ─── ASK TO CONTINUE ───────────────────────
        again = input("\n   Classify another number? (yes/no): ").strip().lower()
        if again != "yes":
            print(f"\n{SEPARATOR}")
            print("   Thank you for using Number Classification System.")
            print(SEPARATOR)
            break


# ─── ENTRY POINT ───────────────────────────────────
if __name__ == "__main__":
    run_classifier()