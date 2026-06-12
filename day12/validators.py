"""User input validation suite.

Day 12 - Functions Fundamentals (Task 3).

Each validator returns a (is_valid, error_message) tuple. A
wrapper dispatches to the correct validator by field type.
"""

import re
from datetime import datetime


def validate_email(value):
    """Validate an email address.

    Args:
        value (str): The email to validate.

    Returns:
        tuple[bool, str]: (is_valid, error_message). The message
            is empty when valid.

    Example:
        >>> validate_email("a@b.com")
        (True, '')
    """
    if not isinstance(value, str) or not value:
        return False, "Email must be a non-empty string."
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if re.match(pattern, value):
        return True, ""
    return False, "Invalid email format."


def validate_phone(value):
    """Validate a phone number (10-15 digits, optional '+').

    Spaces, dashes, and parentheses are ignored before checking.

    Args:
        value (str): The phone number to validate.

    Returns:
        tuple[bool, str]: (is_valid, error_message).

    Example:
        >>> validate_phone("+1 (555) 123-4567")
        (True, '')
    """
    if not isinstance(value, str) or not value:
        return False, "Phone must be a non-empty string."
    cleaned = re.sub(r"[\s\-()]", "", value)
    if re.match(r"^\+?\d{10,15}$", cleaned):
        return True, ""
    return False, "Phone must have 10-15 digits."


def validate_date(value, date_format="%Y-%m-%d"):
    """Validate a date string against a format.

    Args:
        value (str): The date string to validate.
        date_format (str, optional): Expected strptime format.
            Defaults to "%Y-%m-%d".

    Returns:
        tuple[bool, str]: (is_valid, error_message).

    Example:
        >>> validate_date("2026-06-12")
        (True, '')
    """
    if not isinstance(value, str) or not value:
        return False, "Date must be a non-empty string."
    try:
        datetime.strptime(value, date_format)
        return True, ""
    except ValueError:
        return False, f"Date must match format {date_format}."


def validate_password(value, min_length=8):
    """Validate password strength.

    Requires at least `min_length` chars, plus an uppercase
    letter, a lowercase letter, a digit, and a special char.

    Args:
        value (str): The password to validate.
        min_length (int, optional): Minimum length. Defaults to 8.

    Returns:
        tuple[bool, str]: (is_valid, error_message).

    Example:
        >>> validate_password("Weak1!")[0]
        False
    """
    if not isinstance(value, str):
        return False, "Password must be a string."
    if len(value) < min_length:
        return False, (
            f"Password must be at least {min_length} chars."
        )
    if not re.search(r"[A-Z]", value):
        return False, "Password needs an uppercase letter."
    if not re.search(r"[a-z]", value):
        return False, "Password needs a lowercase letter."
    if not re.search(r"\d", value):
        return False, "Password needs a digit."
    if not re.search(r"[^A-Za-z0-9]", value):
        return False, "Password needs a special character."
    return True, ""


def validate_user_input(field_type, value):
    """Dispatch validation to the correct validator by type.

    Args:
        field_type (str): One of "email", "phone", "date",
            or "password".
        value (str): The value to validate.

    Returns:
        tuple[bool, str]: (is_valid, error_message).

    Raises:
        ValueError: If `field_type` is not supported.

    Example:
        >>> validate_user_input("email", "a@b.com")
        (True, '')
    """
    validators = {
        "email": validate_email,
        "phone": validate_phone,
        "date": validate_date,
        "password": validate_password,
    }
    field_type = field_type.lower()
    if field_type not in validators:
        raise ValueError(f"Unsupported field type: {field_type!r}")
    return validators[field_type](value)


def main():
    """Run a quick demonstration of the validation suite."""
    checks = [
        ("email", "umar@xeven.com"),
        ("email", "bad-email"),
        ("phone", "+1 (555) 123-4567"),
        ("date", "2026-06-12"),
        ("password", "Str0ng!Pass"),
        ("password", "weak"),
    ]
    for field, val in checks:
        ok, msg = validate_user_input(field, val)
        status = "PASS" if ok else f"FAIL ({msg})"
        print(f"{field:9} {val:22} -> {status}")


if __name__ == "__main__":
    main()