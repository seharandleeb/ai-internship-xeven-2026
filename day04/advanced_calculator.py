"""
Day 4 - Script 3: Advanced Calculator
=======================================
Topic   : All arithmetic operators combined with user input,
          type conversion, and error handling
Author  : Sehar Andleeb
Internship: Xeven Solutions AI Internship 2026
"""


def get_number(prompt):
    """
    Prompt the user for a number and return it as a float.

    Keeps asking until a valid number is entered.

    Args:
        prompt (str): The message shown to the user.

    Returns:
        float: The validated number entered by the user.
    """
    while True:
        raw = input(prompt)
        try:
            return float(raw)      # convert string input to float
        except ValueError:
            print(f"  Invalid input '{raw}'. Please enter a number.")


def perform_operations(a, b):
    """
    Perform and display all arithmetic operations on two numbers.

    Args:
        a (float): First operand.
        b (float): Second operand.
    """
    print("\n-- Results --")
    print(f"  Numbers entered : {a} and {b}")

    # Basic operations
    print(f"\n  Addition        : {a} + {b}  = {a + b}")
    print(f"  Subtraction     : {a} - {b}  = {a - b}")
    print(f"  Multiplication  : {a} * {b}  = {a * b}")

    # Division — must guard against zero
    if b != 0:
        print(f"  True Division   : {a} / {b}  = {a / b}")
        print(f"  Floor Division  : {a} // {b} = {a // b}  (rounded down)")
        print(f"  Modulo          : {a} % {b}  = {a % b}   (remainder)")
    else:
        print("  Division        : Cannot divide by zero")
        print("  Floor Division  : Cannot divide by zero")
        print("  Modulo          : Cannot divide by zero")

    # Exponentiation
    print(f"  Exponentiation  : {a} ** {b} = {a ** b}")


def display_precedence_example(a, b):
    """
    Show how operator precedence affects a combined expression.

    Args:
        a (float): First operand.
        b (float): Second operand.
    """
    print("\n-- Precedence Demo with Your Numbers --")

    expr1 = a + b * 2          # b*2 runs first
    expr2 = (a + b) * 2        # addition forced first
    expr3 = a ** 2 + b ** 2    # both exponents before addition

    print(f"  {a} + {b} * 2       = {expr1}  (multiplication first)")
    print(f"  ({a} + {b}) * 2     = {expr2}  (parentheses first)")
    print(f"  {a}^2 + {b}^2       = {expr3}  (both exponents first)")


def check_integer_result(a, b):
    """
    Demonstrate int/float type conversion on results.

    Args:
        a (float): First operand.
        b (float): Second operand.
    """
    print("\n-- Type Conversion on Results --")

    product = a * b
    print(f"  {a} * {b}           = {product}  (type: {type(product).__name__})")
    print(f"  int({product})      = {int(product)}  (truncated to int)")
    print(f"  round({product}, 2) = {round(product, 2)}  (rounded to 2 decimal places)")


def main():
    """Main entry point — runs the advanced calculator."""
    print("=" * 45)
    print("      Advanced Calculator — Day 4")
    print("=" * 45)

    # Get two numbers from the user with validation
    a = get_number("\nEnter first number  : ")
    b = get_number("Enter second number : ")

    # Run all sections
    perform_operations(a, b)
    display_precedence_example(a, b)
    check_integer_result(a, b)

    print("\nDay 4 | Script 3 complete — Advanced Calculator")


if __name__ == "__main__":
    main()