"""
Script Purpose: Number Classification System
Author: Sehar Andleeb
Company: Xeven Solutions
Day: 3 of 30

This script demonstrates conditional statements by classifying
numbers into various categories including positive, negative,
zero, even, odd, and special number types.
"""


# ─── CONSTANTS ─────────────────────────────────────
SEPARATOR = "=" * 50
THIN_LINE = "-" * 50
APP_NAME  = "Number Classification System"


def display_header():
    """
    Display application header.

    Parameters: None
    Returns: None
    """
    print(f"\n{SEPARATOR}")
    print(f"   {APP_NAME}")
    print(f"   Day 3 — Conditional Statements")
    print(SEPARATOR)


def classify_sign(number):
    """
    Classify number as positive, negative, or zero.

    Parameters:
        number (float): Number to classify

    Returns:
        str: Classification label
    """
    if number > 0:
        return "Positive"
    elif number < 0:
        return "Negative"
    else:
        return "Zero"


def classify_even_odd(number):
    """
    Classify number as even or odd.
    Only applies to whole numbers.

    Parameters:
        number (float): Number to classify

    Returns:
        str: Even, Odd, or Decimal
    """
    # ─── CHECK IF WHOLE NUMBER FIRST ───────────────
    # Decimal numbers cannot be even or odd
    if number != int(number):
        return "Decimal — even/odd not applicable"
    elif int(number) % 2 == 0:
        return "Even"
    else:
        return "Odd"


def classify_special(number):
    """
    Check if number belongs to any special category.

    Parameters:
        number (float): Number to classify

    Returns:
        str: Special category or description
    """
    # ─── SPECIAL NUMBER CHECKS ─────────────────────
    # Order matters — check specific cases first

    if number == 0:
        return "Zero — additive identity"
    elif number == 1:
        return "One — multiplicative identity"
    elif number < 0 and number == int(number):
        return "Negative Integer"
    elif number > 0 and number == int(number):
        # ─── CHECK IF PERFECT SQUARE ───────────────
        square_root = number ** 0.5
        if square_root == int(square_root):
            return f"Positive Integer and Perfect Square (√{number} = {int(square_root)})"
        else:
            return "Positive Integer"
    else:
        return "Decimal Number"


def classify_range(number):
    """
    Classify number into a numeric range category.

    Parameters:
        number (float): Number to classify

    Returns:
        str: Range category
    """
    if number < -1000:
        return "Very Large Negative"
    elif number < -100:
        return "Large Negative"
    elif number < 0:
        return "Small Negative"
    elif number == 0:
        return "Zero"
    elif number <= 100:
        return "Small Positive"
    elif number <= 1000:
        return "Large Positive"
    else:
        return "Very Large Positive"


def display_classification(number):
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
    print(f"   Sign         : {classify_sign(number)}")
    print(f"   Even/Odd     : {classify_even_odd(number)}")
    print(f"   Special Type : {classify_special(number)}")
    print(f"   Range        : {classify_range(number)}")
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
            number = float(user_input)

            # ─── DISPLAY RESULTS ───────────────────
            display_classification(number)

        except ValueError:
            print("\n   Invalid input. Please enter a number.")

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