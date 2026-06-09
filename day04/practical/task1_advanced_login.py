"""
Day 4 - Practical Task 1: Advanced Login System
=================================================
Topic   : Logical operators and validation with specific error messages
Author  : Sehar Andleeb
Internship: Xeven Solutions AI Internship 2026

Logic Flow:
    1. Take username, password, and age from user
    2. Convert age from string to integer (type conversion)
    3. Validate each field individually with specific error messages
    4. Only grant access if ALL three conditions pass (logical and)
"""


# -- Validation Functions ---------------------------------------------------

def validate_username(username):
    """
    Validate that the username meets the required criteria.

    Rule: Must be at least 5 characters long.

    Args:
        username (str): The username entered by the user.

    Returns:
        tuple[bool, str]: (is_valid, error_message)
    """
    # Check if username is empty
    if len(username) == 0:
        return False, "ERROR: Username cannot be empty."

    # Check minimum length — must be 5 or more characters
    if len(username) < 5:
        return False, (
            f"ERROR: Username '{username}' is too short. "
            f"Must be at least 5 characters (entered {len(username)})."
        )

    # Check for spaces — usernames should not have spaces
    if " " in username:
        return False, "ERROR: Username must not contain spaces."

    # All checks passed
    return True, "Username is valid."


def validate_password(password):
    """
    Validate that the password meets the required criteria.

    Rule: Must be at least 8 characters long.

    Args:
        password (str): The password entered by the user.

    Returns:
        tuple[bool, str]: (is_valid, error_message)
    """
    # Check if password is empty
    if len(password) == 0:
        return False, "ERROR: Password cannot be empty."

    # Check minimum length — must be 8 or more characters
    if len(password) < 8:
        return False, (
            f"ERROR: Password is too short. "
            f"Must be at least 8 characters (entered {len(password)})."
        )

    # All checks passed
    return True, "Password is valid."


def validate_age(age_input):
    """
    Validate that the age is a valid integer and 18 or above.

    Args:
        age_input (str): The raw age string entered by the user.

    Returns:
        tuple[bool, str, int]: (is_valid, error_message, age_as_int)
    """
    # Step 1: Try to convert string input to integer
    try:
        age = int(age_input)
    except ValueError:
        # Input was not a number at all
        return False, f"ERROR: '{age_input}' is not a valid age. Please enter a number.", 0

    # Step 2: Age cannot be negative
    if age < 0:
        return False, f"ERROR: Age cannot be negative (entered {age}).", 0

    # Step 3: Age must be 18 or above
    if age < 18:
        return False, (
            f"ERROR: Access denied. You must be 18 or above. "
            f"(entered {age}, need {18 - age} more year(s))."
        ), 0

    # All checks passed
    return True, "Age is valid.", age


# -- Access Decision --------------------------------------------------------

def check_access(username_valid, password_valid, age_valid):
    """
    Decide whether to grant access based on all three validations.

    All three conditions must be True — uses logical AND.

    Args:
        username_valid (bool): Whether username passed validation.
        password_valid (bool): Whether password passed validation.
        age_valid      (bool): Whether age passed validation.

    Returns:
        bool: True if access is granted, False otherwise.
    """
    # logical and — every single condition must pass
    return username_valid and password_valid and age_valid


# -- Display Results --------------------------------------------------------

def display_validation_report(username, password, age_input):
    """
    Run all validations, print individual results, and show final decision.

    Args:
        username  (str): Username entered by user.
        password  (str): Password entered by user.
        age_input (str): Age entered by user (raw string).
    """
    print("\n" + "-" * 45)
    print("  Validation Report")
    print("-" * 45)

    # --- Validate each field and print result immediately ---

    # Username check
    u_valid, u_msg = validate_username(username)
    status = "PASS" if u_valid else "FAIL"
    print(f"  Username  [{status}] : {u_msg}")

    # Password check
    p_valid, p_msg = validate_password(password)
    status = "PASS" if p_valid else "FAIL"
    print(f"  Password  [{status}] : {p_msg}")

    # Age check
    a_valid, a_msg, age = validate_age(age_input)
    status = "PASS" if a_valid else "FAIL"
    print(f"  Age       [{status}] : {a_msg}")

    # --- Final decision using logical and across all three ---
    print("-" * 45)

    access_granted = check_access(u_valid, p_valid, a_valid)

    if access_granted:
        # not is used here to confirm no condition failed
        any_failed = not access_granted
        print(f"  Any condition failed? {any_failed}")
        print(f"\n  ACCESS GRANTED — Welcome, {username}!")
        print(f"  Logged in as: {username} | Age: {age}")
    else:
        # Use logical or to check if at least one failed (for the message)
        any_failed = not u_valid or not p_valid or not a_valid
        print(f"  Any condition failed? {any_failed}")
        print("\n  ACCESS DENIED — Please fix the errors above and try again.")

    print("-" * 45)


# -- Main -------------------------------------------------------------------

def main():
    """Main entry point — collect input and run validation."""
    print("=" * 45)
    print("    Advanced Login System — Practical Task 1")
    print("=" * 45)
    print("\nPlease enter your credentials:\n")

    # Collect raw input — everything comes in as string
    username  = input("  Username : ").strip()
    password  = input("  Password : ").strip()
    age_input = input("  Age      : ").strip()

    # Run full validation and display report
    display_validation_report(username, password, age_input)

    print("\nDay 4 | Practical Task 1 complete — Advanced Login System")


if __name__ == "__main__":
    main()