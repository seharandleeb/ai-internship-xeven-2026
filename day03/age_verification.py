"""
Script Purpose: Age Verification and Category System
Author: Sehar Andleeb
Company: Xeven Solutions
Day: 3 of 30

This script demonstrates conditional statements by categorizing
a person into different age groups and verifying access
permissions based on their age.
"""


# ─── CONSTANTS ─────────────────────────────────────
SEPARATOR = "=" * 50
THIN_LINE = "-" * 50
APP_NAME  = "Age Verification System"


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


def get_age():
    """
    Prompt user to enter age and validate the input.

    Parameters: None
    Returns:
        int: Validated age entered by user
    """
    user_input = input("   Enter your age: ").strip()
    return int(user_input)


def get_age_category(age):
    """
    Determine the age category based on the age provided.

    Parameters:
        age (int): Age of the person

    Returns:
        str: Age category label
    """
    # ─── AGE CATEGORY LOGIC ────────────────────────
    # Each category has a specific age range
    # elif chain ensures only one category is selected

    if age < 0:
        category = "Invalid"
    elif age == 0:
        category = "Newborn"
    elif age <= 2:
        category = "Infant"
    elif age <= 12:
        category = "Child"
    elif age <= 17:
        category = "Teenager"
    elif age <= 25:
        category = "Young Adult"
    elif age <= 64:
        category = "Adult"
    elif age <= 120:
        category = "Senior Citizen"
    else:
        category = "Invalid"

    return category


def check_permissions(age):
    """
    Check what the person is allowed to do based on age.

    Parameters:
        age (int): Age of the person

    Returns:
        None
    """
    print(f"\n{THIN_LINE}")
    print("   ACCESS PERMISSIONS")
    print(THIN_LINE)

    # ─── VOTING PERMISSION ─────────────────────────
    if age >= 18:
        print("   Voting          : Allowed")
    else:
        remaining = 18 - age
        print(f"  Voting          : Not allowed ({remaining} years remaining)")

    # ─── DRIVING PERMISSION ────────────────────────
    if age >= 18:
        print("   Driving         : Allowed")
    else:
        remaining = 18 - age
        print(f"  Driving         : Not allowed ({remaining} years remaining)")

    # ─── SENIOR DISCOUNT ───────────────────────────
    if age >= 60:
        print("   Senior Discount : Eligible")
    else:
        remaining = 60 - age
        print(f"   Senior Discount : Not eligible ({remaining} years remaining)")

    # ─── SCHOOL ────────────────────────────────────
    if 5 <= age <= 17:
        print("   School          : Required by law")
    elif age < 5:
        print("   School          : Not yet required")
    else:
        print("   School          : Completed")

    print(THIN_LINE)


def run_age_verification():
    """
    Main function to run the age verification system.

    Parameters: None
    Returns: None
    """
    display_header()

    while True:
        try:
            # ─── GET AND VALIDATE AGE ──────────────
            age = get_age()

            # ─── DISPLAY CATEGORY ──────────────────
            category = get_age_category(age)

            if category == "Invalid":
                print(f"\n   Invalid age: {age}. Please enter age between 0 and 120.")
            else:
                print(f"\n{THIN_LINE}")
                print(f"   AGE ANALYSIS")
                print(THIN_LINE)
                print(f"   Age entered  : {age}")
                print(f"   Category     : {category}")

                # ─── CHECK PERMISSIONS ─────────────
                check_permissions(age)

        except ValueError:
            # ─── HANDLE NON-NUMERIC INPUT ──────────
            print("\n   Invalid input. Please enter a number.")

        # ─── ASK TO CONTINUE ───────────────────────
        again = input("\n   Check another age? (yes/no): ").strip().lower()
        if again != "yes":
            print(f"\n{SEPARATOR}")
            print("   Thank you for using Age Verification System.")
            print(SEPARATOR)
            break


# ─── ENTRY POINT ───────────────────────────────────
if __name__ == "__main__":
    run_age_verification()