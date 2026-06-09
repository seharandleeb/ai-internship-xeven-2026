"""
Day 4 - Script 4: Login System
================================
Topic   : Logical operators, comparison operators, and type conversion
          applied in a real-world login and registration scenario
Author  : Sehar Andleeb
Internship: Xeven Solutions AI Internship 2026
"""


# -- Stored credentials (simulating a small user database) ------------------

VALID_USERNAME = "sehar"
VALID_PASSWORD = "xeven2026"
MAX_ATTEMPTS   = 3


def validate_username(username):
    """
    Check whether a username meets the required rules.

    Rules:
        - Must be at least 4 characters long
        - Must not contain spaces
        - Must not be empty

    Args:
        username (str): The username to validate.

    Returns:
        tuple[bool, str]: (is_valid, reason_message)
    """
    if len(username) == 0:
        return False, "Username cannot be empty."

    if " " in username:
        return False, "Username must not contain spaces."

    if len(username) < 4:
        return False, "Username must be at least 4 characters long."

    return True, "Username is valid."


def validate_password(password):
    """
    Check whether a password meets the required rules.

    Rules:
        - Must be at least 8 characters long
        - Must contain at least one digit
        - Must not be empty

    Args:
        password (str): The password to validate.

    Returns:
        tuple[bool, str]: (is_valid, reason_message)
    """
    if len(password) == 0:
        return False, "Password cannot be empty."

    if len(password) < 8:
        return False, "Password must be at least 8 characters long."

    # Check if any character in the password is a digit
    has_digit = any(char.isdigit() for char in password)
    if not has_digit:
        return False, "Password must contain at least one number."

    return True, "Password is valid."


def check_login(username, password):
    """
    Verify username and password against stored credentials.

    Uses logical AND — both must match for login to succeed.

    Args:
        username (str): Entered username.
        password (str): Entered password.

    Returns:
        bool: True if credentials match, False otherwise.
    """
    username_match = (username == VALID_USERNAME)    # comparison operator
    password_match = (password == VALID_PASSWORD)    # comparison operator

    return username_match and password_match          # logical AND


def login_system():
    """Run the login system with a maximum number of attempts."""
    print("=" * 40)
    print("       Login System — Day 4")
    print("=" * 40)

    attempts = 0

    while attempts < MAX_ATTEMPTS:
        remaining = MAX_ATTEMPTS - attempts
        print(f"\nAttempts remaining: {remaining}")

        username = input("Username : ").strip()    # strip() removes extra spaces
        password = input("Password : ").strip()

        # Validate format first
        user_valid, user_msg = validate_username(username)
        pass_valid, pass_msg = validate_password(password)

        if not user_valid:
            print(f"  [!] {user_msg}")
            attempts += 1
            continue

        if not pass_valid:
            print(f"  [!] {pass_msg}")
            attempts += 1
            continue

        # Check against stored credentials
        if check_login(username, password):
            print("\n  Access granted. Welcome, " + username + "!")
            print("  Login successful on attempt " + str(attempts + 1) + ".")
            return   # exit the function on success

        else:
            print("  [!] Incorrect username or password.")
            attempts += 1

    # Reaching here means all attempts were used
    print("\n  Account locked. Maximum attempts reached.")
    print("  Attempts used : " + str(attempts))


def demonstrate_logical_operators():
    """
    Show how and, or, not work with concrete examples.
    Runs before the interactive login so the logic is clear.
    """
    print("\n-- Logical Operator Demo --")

    age        = 20
    has_id     = True
    is_student = False

    # and — both conditions must be True
    can_enter  = age >= 18 and has_id
    print(f"  age >= 18 and has_id          = {can_enter}")

    # or — at least one condition must be True
    gets_discount = is_student or age < 25
    print(f"  is_student or age < 25        = {gets_discount}")

    # not — flips the boolean
    is_adult = not (age < 18)
    print(f"  not (age < 18)                = {is_adult}")

    # Chained comparison — Pythonic way
    valid_age = 18 <= age <= 65
    print(f"  18 <= age <= 65               = {valid_age}")

    # Combined complex condition
    full_access = (age >= 18 and has_id) and not is_student
    print(f"  (age>=18 and has_id) and not is_student = {full_access}")


def main():
    """Main entry point."""
    # Show logical operator theory first
    demonstrate_logical_operators()

    # Then run the interactive login
    print("\n" + "=" * 40)
    print("  Now entering interactive login...")
    print("  Hint — username: sehar | password: xeven2026")
    print("=" * 40)
    login_system()

    print("\nDay 4 | Script 4 complete — Login System")


if __name__ == "__main__":
    main()