"""
Script Purpose: Enhanced Age Verification System
Author: Sehar Andleeb
Company: Xeven Solutions
Day: 3 of 30

This script prompts the user for their name and age,
classifies them into age categories, and prints a
personalized message for each category with proper
error handling for invalid inputs.
"""


# ─── CONSTANTS ─────────────────────────────────────
SEPARATOR  = "=" * 55
THIN_LINE  = "-" * 55
APP_NAME   = "Enhanced Age Verification System"


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


def get_user_name():
    """
    Prompt user to enter their name and validate it.

    Parameters: None
    Returns:
        str: Validated name entered by user
    """
    name = input("   Enter your name : ").strip()

    # ─── VALIDATE NAME ─────────────────────────────
    # Name cannot be empty or contain numbers
    if len(name) == 0:
        raise ValueError("Name cannot be empty")
    if any(char.isdigit() for char in name):
        raise ValueError("Name cannot contain numbers")

    return name


def get_user_age():
    """
    Prompt user to enter their age and convert to integer.

    Parameters: None
    Returns:
        int: Validated age entered by user
    """
    user_input = input("   Enter your age  : ").strip()

    # ─── CONVERT TO INTEGER ────────────────────────
    # input() always returns string so we convert it
    age = int(user_input)

    # ─── VALIDATE AGE RANGE ────────────────────────
    # Age cannot be negative or unrealistically high
    if age < 0:
        raise ValueError("Age cannot be negative")
    if age > 120:
        raise ValueError("Please enter a realistic age")

    return age


def classify_age(age):
    """
    Classify age into a category based on defined ranges.

    Parameters:
        age (int): Age of the person

    Returns:
        str: Age category label
    """
    # ─── AGE CATEGORY CONDITIONS ───────────────────
    # Each condition checks a specific age range
    # elif ensures only one category is matched

    if age < 13:
        # Children are below 13 years old
        category = "Child"

    elif age <= 17:
        # Teenagers are between 13 and 17 years old
        category = "Teenager"

    elif age <= 64:
        # Adults are between 18 and 64 years old
        category = "Adult"

    else:
        # Seniors are 65 years and above
        category = "Senior"

    return category


def get_personalized_message(user_name, category, age):
    """
    Generate a personalized message based on name and category.

    Parameters:
        user_name (str): Name of the user
        category  (str): Age category
        age       (int): Age of the person

    Returns:
        str: Personalized message
    """
    # ─── MESSAGE FOR EACH CATEGORY ─────────────────
    # Each category gets a unique encouraging message

    if category == "Child":
        # Encouraging message for children
        message = (f"Hello {user_name}! As a child, the world is full "
                   f"of wonder and learning. Enjoy every moment of "
                   f"growing up!")

    elif category == "Teenager":
        # Motivating message for teenagers
        message = (f"Hello {user_name}! As a teenager, you have many "
                   f"opportunities ahead. This is the best time to "
                   f"discover your passions and build your future!")

    elif category == "Adult":
        # Empowering message for adults
        message = (f"Hello {user_name}! As an adult, you have the "
                   f"experience and skills to achieve great things. "
                   f"Keep pushing forward and making an impact!")

    else:
        # Respectful message for seniors
        message = (f"Hello {user_name}! As a senior, your wisdom and "
                   f"life experience are invaluable. You have lived "
                   f"a remarkable journey and continue to inspire others!")

    return message


def check_permissions(user_name, age):
    """
    Check and display permissions based on age.

    Parameters:
        user_name (str): Name of the user
        age       (int): Age of the person

    Returns:
        None
    """
    print(f"\n{THIN_LINE}")
    print(f"   PERMISSIONS FOR {user_name.upper()}")
    print(THIN_LINE)

    # ─── VOTING CHECK ──────────────────────────────
    # Must be 18 or older to vote
    if age >= 18:
        print("   Voting          : Eligible")
    else:
        print(f"   Voting          : Not eligible ({18 - age} years remaining)")

    # ─── DRIVING CHECK ─────────────────────────────
    # Must be 18 or older to drive
    if age >= 18:
        print("   Driving         : Eligible")
    else:
        print(f"   Driving         : Not eligible ({18 - age} years remaining)")

    # ─── SENIOR DISCOUNT CHECK ─────────────────────
    # Must be 65 or older for senior discount
    if age >= 65:
        print("   Senior Discount : Eligible")
    else:
        print(f"   Senior Discount : Not eligible ({65 - age} years remaining)")

    # ─── SCHOOL CHECK ──────────────────────────────
    # School is required between ages 5 and 17
    if age < 5:
        print("   School          : Not yet required")
    elif age <= 17:
        print("   School          : Currently required")
    else:
        print("   School          : Completed")

    print(THIN_LINE)


def run_age_verification():
    """
    Main function to run the enhanced age verification system.

    Parameters: None
    Returns: None
    """
    display_header()

    while True:
        try:
            # ─── GET USER DETAILS ──────────────────
            user_name = get_user_name()
            age       = get_user_age()

            # ─── CLASSIFY AGE ──────────────────────
            category = classify_age(age)

            # ─── GET PERSONALIZED MESSAGE ──────────
            message = get_personalized_message(user_name, category, age)

            # ─── DISPLAY RESULTS ───────────────────
            print(f"\n{THIN_LINE}")
            print(f"   PROFILE SUMMARY")
            print(THIN_LINE)
            print(f"   Name     : {user_name}")
            print(f"   Age      : {age}")
            print(f"   Category : {category}")
            print(THIN_LINE)
            print(f"\n   {message}")

            # ─── SHOW PERMISSIONS ──────────────────
            check_permissions(user_name, age)

        except ValueError as error:
            # ─── HANDLE ALL INVALID INPUTS ─────────
            # Catches negative age, text input, empty name
            print(f"\n   Invalid input: {error}. Please try again.")

        # ─── ASK TO CONTINUE ───────────────────────
        again = input("\n   Check another person? (yes/no): ").strip().lower()
        if again != "yes":
            print(f"\n{SEPARATOR}")
            print("   Thank you for using the Age Verification System.")
            print(SEPARATOR)
            break


# ─── ENTRY POINT ───────────────────────────────────
if __name__ == "__main__":
    run_age_verification()