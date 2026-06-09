"""
Script Purpose: Simple Grade Calculator with Feedback
Author: Sehar Andleeb
Company: Xeven Solutions
Day: 3 of 30

This script accepts a numeric grade from the user,
assigns a letter grade using elif statements, validates
input, and prints a personalized encouraging message.
"""


# ─── CONSTANTS ─────────────────────────────────────
SEPARATOR = "=" * 50
THIN_LINE = "-" * 50
APP_NAME  = "Grade Calculator with Feedback"


def display_header():
    """
    Display application header.

    Parameters: None
    Returns: None
    """
    print(f"\n{SEPARATOR}")
    print(f"   {APP_NAME}")
    print(f"   Day 3 — elif Statements and Logic")
    print(SEPARATOR)


def get_student_name():
    """
    Prompt user to enter their name.

    Parameters: None
    Returns:
        str: Student name
    """
    name = input("   Enter your name  : ").strip()

    # ─── NAME CANNOT BE EMPTY ──────────────────────
    if len(name) == 0:
        raise ValueError("Name cannot be empty")

    return name


def get_numeric_grade():
    """
    Prompt user to enter a numeric grade and validate range.

    Parameters: None
    Returns:
        float: Validated grade between 0 and 100
    """
    user_input = input("   Enter your grade (0-100): ").strip()

    # ─── CONVERT STRING TO FLOAT ───────────────────
    grade = float(user_input)

    # ─── VALIDATE GRADE IS WITHIN RANGE ───────────
    # Grade must be between 0 and 100 inclusive
    if grade < 0 or grade > 100:
        raise ValueError("Grade must be between 0 and 100")

    return grade


def get_letter_grade(grade):
    """
    Assign letter grade based on numeric grade using elif chain.
    Avoids unnecessary nesting by using flat elif statements.

    Parameters:
        grade (float): Numeric grade between 0 and 100

    Returns:
        str: Letter grade
    """
    # ─── LETTER GRADE ASSIGNMENT ───────────────────
    # Each elif checks the next lower boundary
    # Only one condition will ever be True

    if grade >= 90:
        # 90 and above is an A
        return "A"
    elif grade >= 80:
        # 80 to 89 is a B
        return "B"
    elif grade >= 70:
        # 70 to 79 is a C
        return "C"
    elif grade >= 60:
        # 60 to 69 is a D
        return "D"
    else:
        # Anything below 60 is a failing grade
        return "F"


def get_grade_interpretation(letter_grade):
    """
    Provide a descriptive interpretation of the letter grade.

    Parameters:
        letter_grade (str): Letter grade

    Returns:
        str: Grade interpretation
    """
    # ─── GRADE INTERPRETATION ──────────────────────
    if letter_grade == "A":
        return "Outstanding — top of the class"
    elif letter_grade == "B":
        return "Above average — strong performance"
    elif letter_grade == "C":
        return "Average — meets expectations"
    elif letter_grade == "D":
        return "Below average — needs improvement"
    else:
        return "Failing — did not meet requirements"


def get_message(student_name, letter_grade):
    """
    Generate a personalized encouraging message based on grade.

    Parameters:
        student_name (str): Name of the student
        letter_grade (str): Letter grade

    Returns:
        str: Personalized message
    """
    # ─── PERSONALIZED MESSAGES ─────────────────────
    # Each grade gets a unique encouraging message
    # Using elif keeps the code flat and readable

    if letter_grade == "A":
        message = (f"Excellent work {student_name}! "
                   f"You have shown exceptional dedication "
                   f"and mastery of the subject.")

    elif letter_grade == "B":
        message = (f"Good job {student_name}! "
                   f"You are performing well above average. "
                   f"Keep pushing and an A is within reach.")

    elif letter_grade == "C":
        message = (f"Not bad {student_name}. "
                   f"You are meeting expectations but there is "
                   f"room to grow. A little more effort goes a long way.")

    elif letter_grade == "D":
        message = (f"Keep trying {student_name}. "
                   f"You are passing but only just. "
                   f"Focus on your weak areas and seek help if needed.")

    else:
        message = (f"Do not give up {student_name}. "
                   f"Failure is not the end — it is a chance to "
                   f"learn, reset, and come back stronger.")

    return message


def display_result(student_name, grade, letter_grade,
                   interpretation, message):
    """
    Display the complete grade result and feedback.

    Parameters:
        student_name    (str): Name of the student
        grade           (float): Numeric grade
        letter_grade    (str): Letter grade
        interpretation  (str): Grade interpretation
        message         (str): Personalized message

    Returns:
        None
    """
    print(f"\n{THIN_LINE}")
    print(f"   GRADE REPORT — {student_name.upper()}")
    print(THIN_LINE)
    print(f"   Numeric Grade  : {grade} / 100")
    print(f"   Letter Grade   : {letter_grade}")
    print(f"   Interpretation : {interpretation}")
    print(f"   Status         : {'Pass' if grade >= 60 else 'Fail'}")
    print(THIN_LINE)
    print(f"   Message: {message}")
    print(THIN_LINE)


def run_grade_calculator():
    """
    Main function to run the simple grade calculator.

    Parameters: None
    Returns: None
    """
    display_header()

    while True:
        try:
            # ─── GET STUDENT DETAILS ───────────────
            student_name = get_student_name()
            grade        = get_numeric_grade()

            # ─── CALCULATE GRADE AND MESSAGE ───────
            letter_grade    = get_letter_grade(grade)
            interpretation  = get_grade_interpretation(letter_grade)
            message         = get_message(student_name, letter_grade)

            # ─── DISPLAY RESULT ────────────────────
            display_result(
                student_name,
                grade,
                letter_grade,
                interpretation,
                message
            )

        except ValueError as error:
            # ─── HANDLE INVALID INPUT ──────────────
            print(f"\n   Invalid input: {error}. Please try again.")

        # ─── ASK TO CONTINUE ───────────────────────
        again = input("\n   Calculate another grade? (yes/no): ").strip().lower()
        if again != "yes":
            print(f"\n{SEPARATOR}")
            print("   Thank you for using the Grade Calculator.")
            print(SEPARATOR)
            break


# ─── ENTRY POINT ───────────────────────────────────
if __name__ == "__main__":
    run_grade_calculator()