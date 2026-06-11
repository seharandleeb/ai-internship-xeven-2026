"""
Script Purpose: Interactive Calculator with History and Statistics
Author: Sehar Andleeb
Company: Xeven Solutions
Day: 2 of 30

A professional calculator that performs arithmetic operations,
tracks calculation history, shows session statistics, and handles
all edge cases with proper error handling. Built using Python
basics: variables, data types, input/output, and type conversion.
"""


# ─── CONSTANTS ─────────────────────────────────────────────────
SEPARATOR     = "=" * 55
THIN_LINE     = "-" * 55
APP_NAME      = "SmartCalc Pro"
INTERN_NAME   = "Sehar Andleeb"
COMPANY       = "Xeven Solutions"


# ─── HISTORY STORAGE ───────────────────────────────────────────
# Lists store all calculations done in this session
calculation_history  = []     # stores each result as string
all_results          = []     # stores numeric results for stats
total_calculations   = 0      # counts total operations done


def display_header():
    """
    Display the application header with branding.

    Parameters: None
    Returns: None
    """
    print(f"\n{SEPARATOR}")
    print(f"   {APP_NAME} — Professional Python Calculator")
    print(f"   Built by {INTERN_NAME} | {COMPANY}")
    print(f"   Day 2 of 30 — Variables, Types, Input/Output")
    print(SEPARATOR)


def display_menu():
    """
    Display the main operation menu to the user.

    Parameters: None
    Returns: None
    """
    print(f"\n{THIN_LINE}")
    print("   SELECT OPERATION")
    print(THIN_LINE)
    print("   1. Basic Arithmetic  (+ - x /)")
    print("   2. Power             (x ^ y)")
    print("   3. Remainder         (x % y)")
    print("   4. View History      (past calculations)")
    print("   5. View Statistics   (session summary)")
    print("   6. Exit")
    print(THIN_LINE)


def get_number(prompt):
    """
    Prompt user to enter a number and return it as float.

    Parameters:
        prompt (str): Message shown to the user

    Returns:
        float: Validated number entered by user

    Raises:
        ValueError: If input cannot be converted to float
    """
    user_input = input(prompt).strip()
    return float(user_input)


def perform_basic_arithmetic(first_number, second_number):
    """
    Perform all four arithmetic operations and display results.

    Parameters:
        first_number  (float): First operand
        second_number (float): Second operand

    Returns:
        float: The sum result for history tracking
    """
    global total_calculations

    # ─── CALCULATIONS ──────────────────────────────
    sum_result        = first_number + second_number
    difference_result = first_number - second_number
    product_result    = first_number * second_number

    print(f"\n{THIN_LINE}")
    print(f"   RESULTS")
    print(THIN_LINE)
    print(f"   Sum        : {first_number} + {second_number} = {sum_result}")
    print(f"   Difference : {first_number} - {second_number} = {difference_result}")
    print(f"   Product    : {first_number} x {second_number} = {product_result}")

    # ─── SAFE DIVISION ─────────────────────────────
    # Dividing by zero is undefined in mathematics
    if second_number == 0:
        print(f"   Quotient   : Cannot divide {first_number} by zero")
    else:
        quotient_result = first_number / second_number
        print(f"   Quotient   : {first_number} / {second_number} = {round(quotient_result, 4)}")

    # ─── SAVE TO HISTORY ───────────────────────────
    record = (f"{first_number} + {second_number} = {sum_result} | "
            f"{first_number} - {second_number} = {difference_result} | "
            f"{first_number} x {second_number} = {product_result}")
    calculation_history.append(record)
    all_results.append(sum_result)
    total_calculations += 1

    return sum_result


def perform_power(first_number, second_number):
    """
    Calculate the power of first_number raised to second_number.

    Parameters:
        first_number  (float): Base number
        second_number (float): Exponent

    Returns:
        float: Result of first_number ^ second_number
    """
    global total_calculations

    power_result = first_number ** second_number

    print(f"\n{THIN_LINE}")
    print(f"   RESULT")
    print(THIN_LINE)
    print(f"   Power : {first_number} ^ {second_number} = {power_result}")

    # ─── SAVE TO HISTORY ───────────────────────────
    record = f"{first_number} ^ {second_number} = {power_result}"
    calculation_history.append(record)
    all_results.append(power_result)
    total_calculations += 1

    return power_result


def perform_remainder(first_number, second_number):
    """
    Calculate the remainder when first_number is divided by second_number.

    Parameters:
        first_number  (float): Dividend
        second_number (float): Divisor

    Returns:
        float: Remainder of the division
    """
    global total_calculations

    # ─── SAFE MODULO ───────────────────────────────
    if second_number == 0:
        print(f"\n   Cannot find remainder when dividing by zero")
        return None

    remainder_result = first_number % second_number

    print(f"\n{THIN_LINE}")
    print(f"   RESULT")
    print(THIN_LINE)
    print(f"   Remainder : {first_number} % {second_number} = {remainder_result}")

    # ─── SAVE TO HISTORY ───────────────────────────
    record = f"{first_number} % {second_number} = {remainder_result}"
    calculation_history.append(record)
    all_results.append(remainder_result)
    total_calculations += 1

    return remainder_result


def display_history():
    """
    Display all calculations performed in this session.

    Parameters: None
    Returns: None
    """
    print(f"\n{THIN_LINE}")
    print("   CALCULATION HISTORY")
    print(THIN_LINE)

    # ─── CHECK IF HISTORY IS EMPTY ─────────────────
    if len(calculation_history) == 0:
        print("   No calculations yet.")
    else:
        for index, record in enumerate(calculation_history):
            print(f"   {index + 1}. {record}")

    print(THIN_LINE)


def display_statistics():
    """
    Display session statistics including total calculations,
    highest result, lowest result, and average result.

    Parameters: None
    Returns: None
    """
    print(f"\n{THIN_LINE}")
    print("   SESSION STATISTICS")
    print(THIN_LINE)

    # ─── CHECK IF ANY CALCULATIONS DONE ────────────
    if total_calculations == 0:
        print("   No calculations performed yet.")
    else:
        average_result = sum(all_results) / len(all_results)

        print(f"   Total Calculations : {total_calculations}")
        print(f"   Highest Result     : {max(all_results)}")
        print(f"   Lowest Result      : {min(all_results)}")
        print(f"   Average Result     : {round(average_result, 4)}")

    print(THIN_LINE)


def run_calculator():
    """
    Main function to run the SmartCalc Pro calculator.
    Controls the main loop and routes user to correct operation.

    Parameters: None
    Returns: None
    """
    display_header()

    while True:
        display_menu()

        try:
            choice = input("   Enter your choice (1-6): ").strip()

            # ─── BASIC ARITHMETIC ──────────────────
            if choice == "1":
                first_number  = get_number("   Enter first number  : ")
                second_number = get_number("   Enter second number : ")
                perform_basic_arithmetic(first_number, second_number)

            # ─── POWER ─────────────────────────────
            elif choice == "2":
                first_number  = get_number("   Enter base number   : ")
                second_number = get_number("   Enter exponent      : ")
                perform_power(first_number, second_number)

            # ─── REMAINDER ─────────────────────────
            elif choice == "3":
                first_number  = get_number("   Enter first number  : ")
                second_number = get_number("   Enter second number : ")
                perform_remainder(first_number, second_number)

            # ─── HISTORY ───────────────────────────
            elif choice == "4":
                display_history()

            # ─── STATISTICS ────────────────────────
            elif choice == "5":
                display_statistics()

            # ─── EXIT ──────────────────────────────
            elif choice == "6":
                print(f"\n{SEPARATOR}")
                print(f"   Total calculations this session: {total_calculations}")
                print(f"   Thank you for using {APP_NAME}.")
                print(f"   Keep learning, keep building — {INTERN_NAME}")
                print(SEPARATOR)
                break

            else:
                print("   Invalid choice. Please enter a number from 1 to 6.")

        except ValueError:
            # ─── HANDLE INVALID NUMBER INPUT ───────
            print(f"\n   Invalid input. Please enter numbers only.")


# ─── ENTRY POINT ───────────────────────────────────
if __name__ == "__main__":
    run_calculator()