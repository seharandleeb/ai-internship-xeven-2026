"""
Day 4 - Practical Task 2: Multi-Operation Calculator
======================================================
Topic   : Type conversion, arithmetic operators, error handling
Author  : Sehar Andleeb
Internship: Xeven Solutions AI Internship 2026

Logic Flow:
    1. Prompt user for two numbers — convert strings to float
    2. Prompt user for an operation
    3. Validate the operation is one of the six allowed
    4. Perform the calculation with appropriate error handling
    5. Display result formatted to 2 decimal places
"""


# -- Supported operations ---------------------------------------------------

VALID_OPERATIONS = ["+", "-", "*", "/", "%", "**"]


# -- Input Helpers ----------------------------------------------------------

def get_number(prompt):
    """
    Prompt the user for a number and return it as a float.

    Keeps asking until a valid number is entered.

    Args:
        prompt (str): Message shown to the user.

    Returns:
        float: The validated number.
    """
    while True:
        raw = input(prompt).strip()
        try:
            return float(raw)
        except ValueError:
            print(f"  ERROR: '{raw}' is not a valid number. Please try again.")


def get_operation():
    """
    Prompt the user for an operation and validate it.

    Keeps asking until one of the six valid operations is entered.

    Returns:
        str: A valid operation symbol.
    """
    allowed = ", ".join(VALID_OPERATIONS)

    while True:
        op = input(f"  Operation ({allowed}) : ").strip()

        if op in VALID_OPERATIONS:
            return op

        # Invalid operation — list what is accepted
        print(f"  ERROR: '{op}' is not a valid operation.")
        print(f"  Accepted operations are: {allowed}")


# -- Calculation ------------------------------------------------------------

def calculate(a, b, operation):
    """
    Perform the selected arithmetic operation on two numbers.

    Args:
        a         (float): First operand.
        b         (float): Second operand.
        operation (str)  : One of +, -, *, /, %, **

    Returns:
        tuple[bool, str, float]: (success, message, result)
    """
    if operation == "+":
        return True, "OK", a + b

    elif operation == "-":
        return True, "OK", a - b

    elif operation == "*":
        return True, "OK", a * b

    elif operation == "/":
        # Guard against division by zero
        if b == 0:
            return False, "ERROR: Cannot divide by zero.", 0.0
        return True, "OK", a / b

    elif operation == "%":
        # Modulo also fails on zero divisor
        if b == 0:
            return False, "ERROR: Cannot perform modulo with zero.", 0.0
        return True, "OK", a % b

    elif operation == "**":
        # 0 ** negative number is mathematically undefined
        if a == 0 and b < 0:
            return False, "ERROR: Cannot raise zero to a negative power.", 0.0
        return True, "OK", a ** b

    # Should never reach here — get_operation() already validated
    return False, f"ERROR: Unknown operation '{operation}'.", 0.0


# -- Display Result ---------------------------------------------------------

def display_result(a, b, operation, success, message, result):
    """
    Print the calculation result in the required format.

    Successful format : 5.0 + 3.0 = 8.00
    Failed format     : ERROR message

    Args:
        a         (float): First operand.
        b         (float): Second operand.
        operation (str)  : The operation symbol.
        success   (bool) : Whether calculation succeeded.
        message   (str)  : Error message if failed.
        result    (float): The result if successful.
    """
    print("\n" + "-" * 40)
    print("  Result")
    print("-" * 40)

    if success:
        # Format all three values to 2 decimal places
        print(f"  {a:.2f} {operation} {b:.2f} = {result:.2f}")
    else:
        print(f"  {message}")

    print("-" * 40)


# -- Main -------------------------------------------------------------------

def main():
    """Main entry point — runs the multi-operation calculator."""
    print("=" * 40)
    print("   Multi-Operation Calculator — Task 2")
    print("=" * 40)

    # Step 1: Get two numbers — type conversion from str to float
    print("\nEnter two numbers:\n")
    a = get_number("  First number  : ")
    b = get_number("  Second number : ")

    # Step 2: Get and validate operation
    print()
    operation = get_operation()

    # Step 3: Perform calculation
    success, message, result = calculate(a, b, operation)

    # Step 4: Display formatted result
    display_result(a, b, operation, success, message, result)

    print("\nDay 4 | Practical Task 2 complete — Multi-Operation Calculator")


if __name__ == "__main__":
    main()