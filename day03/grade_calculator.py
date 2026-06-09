"""
Script Purpose: Grade Calculator with Letter Grades and Messages
Author: Sehar Andleeb
Company: Xeven Solutions
Day: 3 of 30

This script demonstrates nested conditional statements by
calculating letter grades, GPA points, and personalized
feedback messages based on student marks.
"""


# ─── CONSTANTS ─────────────────────────────────────
SEPARATOR  = "=" * 55
THIN_LINE  = "-" * 55
APP_NAME   = "Grade Calculator"
TOTAL_MARKS = 100


def display_header():
    """
    Display application header.

    Parameters: None
    Returns: None
    """
    print(f"\n{SEPARATOR}")
    print(f"   {APP_NAME}")
    print(f"   Day 3 — Conditional Statements and Logic")
    print(SEPARATOR)


def get_marks(subject_name):
    """
    Prompt user to enter marks for a subject and validate.

    Parameters:
        subject_name (str): Name of the subject

    Returns:
        float: Validated marks between 0 and 100
    """
    user_input = input(f"   Enter marks for {subject_name} (0-100): ").strip()
    marks = float(user_input)

    # ─── VALIDATE RANGE ────────────────────────────
    # Marks must be between 0 and 100
    if marks < 0 or marks > 100:
        raise ValueError("Marks must be between 0 and 100")

    return marks


def get_letter_grade(marks):
    """
    Convert numeric marks to letter grade.

    Parameters:
        marks (float): Marks obtained out of 100

    Returns:
        str: Letter grade
    """
    # ─── GRADE BOUNDARIES ──────────────────────────
    if marks >= 90:
        return "A+"
    elif marks >= 85:
        return "A"
    elif marks >= 80:
        return "A-"
    elif marks >= 75:
        return "B+"
    elif marks >= 70:
        return "B"
    elif marks >= 65:
        return "B-"
    elif marks >= 60:
        return "C+"
    elif marks >= 55:
        return "C"
    elif marks >= 50:
        return "C-"
    elif marks >= 45:
        return "D"
    else:
        return "F"


def get_gpa_points(letter_grade):
    """
    Convert letter grade to GPA points.

    Parameters:
        letter_grade (str): Letter grade

    Returns:
        float: GPA points
    """
    # ─── GPA MAPPING ───────────────────────────────
    if letter_grade == "A+":
        return 4.0
    elif letter_grade == "A":
        return 4.0
    elif letter_grade == "A-":
        return 3.7
    elif letter_grade == "B+":
        return 3.3
    elif letter_grade == "B":
        return 3.0
    elif letter_grade == "B-":
        return 2.7
    elif letter_grade == "C+":
        return 2.3
    elif letter_grade == "C":
        return 2.0
    elif letter_grade == "C-":
        return 1.7
    elif letter_grade == "D":
        return 1.0
    else:
        return 0.0


def get_feedback_message(marks, letter_grade):
    """
    Generate personalized feedback based on marks and grade.

    Parameters:
        marks (float): Marks obtained
        letter_grade (str): Letter grade

    Returns:
        str: Personalized feedback message
    """
    # ─── NESTED CONDITIONALS FOR FEEDBACK ──────────
    # First check grade category, then give specific message

    if letter_grade in ("A+", "A", "A-"):
        if marks == 100:
            message = "Perfect score! Absolutely outstanding performance."
        elif marks >= 90:
            message = "Excellent work! You have mastered this subject."
        else:
            message = "Great job! You are performing at a high level."

    elif letter_grade in ("B+", "B", "B-"):
        if marks >= 75:
            message = "Good performance. A little more effort for an A."
        else:
            message = "Decent work. Focus on weak areas to improve."

    elif letter_grade in ("C+", "C", "C-"):
        if marks >= 55:
            message = "Average performance. More consistent study needed."
        else:
            message = "Just passing. Seek help and put in extra effort."

    elif letter_grade == "D":
        message = "At risk. Attend extra classes and revise thoroughly."

    else:
        message = "Failed. Please retake the exam and seek academic support."

    return message


def display_result(subject_name, marks, letter_grade, gpa_points, message):
    """
    Display the complete result for a subject.

    Parameters:
        subject_name (str): Name of the subject
        marks        (float): Marks obtained
        letter_grade (str): Letter grade
        gpa_points   (float): GPA points
        message      (str): Feedback message

    Returns:
        None
    """
    print(f"\n{THIN_LINE}")
    print(f"   RESULT — {subject_name.upper()}")
    print(THIN_LINE)
    print(f"   Marks Obtained : {marks} / {TOTAL_MARKS}")
    print(f"   Percentage     : {marks}%")
    print(f"   Letter Grade   : {letter_grade}")
    print(f"   GPA Points     : {gpa_points}")
    print(f"   Status         : {'Pass' if marks >= 50 else 'Fail'}")
    print(THIN_LINE)
    print(f"   Feedback: {message}")
    print(THIN_LINE)


def run_grade_calculator():
    """
    Main function to run the grade calculator.

    Parameters: None
    Returns: None
    """
    display_header()

    # ─── SUBJECT LIST ──────────────────────────────
    subjects = ["Mathematics", "English", "Physics", "Computer Science"]

    total_marks_obtained = 0
    total_gpa_points     = 0
    subject_count        = len(subjects)

    print(f"\n   You will enter marks for {subject_count} subjects.\n")

    for subject_name in subjects:
        while True:
            try:
                # ─── GET MARKS ─────────────────────
                marks = get_marks(subject_name)

                # ─── CALCULATE GRADE ───────────────
                letter_grade = get_letter_grade(marks)
                gpa_points   = get_gpa_points(letter_grade)
                message      = get_feedback_message(marks, letter_grade)

                # ─── DISPLAY RESULT ────────────────
                display_result(
                    subject_name,
                    marks,
                    letter_grade,
                    gpa_points,
                    message
                )

                # ─── ADD TO TOTALS ─────────────────
                total_marks_obtained += marks
                total_gpa_points     += gpa_points
                break

            except ValueError as error:
                print(f"\n   Invalid input: {error}. Please try again.")

    # ─── OVERALL SUMMARY ───────────────────────────
    average_marks = total_marks_obtained / subject_count
    average_gpa   = total_gpa_points / subject_count
    overall_grade = get_letter_grade(average_marks)

    print(f"\n{SEPARATOR}")
    print(f"   OVERALL ACADEMIC SUMMARY")
    print(SEPARATOR)
    print(f"   Total Marks    : {total_marks_obtained} / {subject_count * 100}")
    print(f"   Average Marks  : {round(average_marks, 2)}%")
    print(f"   Overall Grade  : {overall_grade}")
    print(f"   Average GPA    : {round(average_gpa, 2)}")

    # ─── FINAL STATUS ──────────────────────────────
    # Student passes only if average is 50 or above
    if average_marks >= 50:
        print(f"   Final Status   : PASS")
    else:
        print(f"   Final Status   : FAIL")

    print(SEPARATOR)


# ─── ENTRY POINT ───────────────────────────────────
if __name__ == "__main__":
    run_grade_calculator()