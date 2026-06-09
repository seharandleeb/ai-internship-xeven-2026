"""
Script Purpose: Grade Calculator with Letter Grades and Messages
Author: Sehar Andleeb
Company: Xeven Solutions
Day: 3 of 30

This script takes student name and marks for multiple subjects,
calculates letter grades, GPA points, and provides personalized
feedback using nested conditional statements.
"""


# ─── CONSTANTS ─────────────────────────────────────
SEPARATOR    = "=" * 55
THIN_LINE    = "-" * 55
APP_NAME     = "Student Grade Calculator"
TOTAL_MARKS  = 100
PASS_MARKS   = 50


def display_header():
    """
    Display application header.

    Parameters: None
    Returns: None
    """
    print(f"\n{SEPARATOR}")
    print(f"   {APP_NAME}")
    print(f"   Day 3 — Nested Conditionals and Logic")
    print(SEPARATOR)


def get_student_name():
    """
    Prompt user to enter student name and validate.

    Parameters: None
    Returns:
        str: Validated student name
    """
    name = input("   Enter student name : ").strip()

    # ─── VALIDATE NAME IS NOT EMPTY ────────────────
    if len(name) == 0:
        raise ValueError("Name cannot be empty")

    return name


def get_marks(subject_name):
    """
    Prompt user to enter marks for a subject and validate range.

    Parameters:
        subject_name (str): Name of the subject

    Returns:
        float: Validated marks between 0 and 100
    """
    user_input = input(f"   Enter marks for {subject_name} (0-100): ").strip()

    # ─── CONVERT STRING TO FLOAT ───────────────────
    marks = float(user_input)

    # ─── VALIDATE MARKS ARE WITHIN RANGE ──────────
    # Marks cannot be less than 0 or more than 100
    if marks < 0 or marks > TOTAL_MARKS:
        raise ValueError(f"Marks must be between 0 and {TOTAL_MARKS}")

    return marks


def get_letter_grade(marks):
    """
    Convert numeric marks to letter grade using grade boundaries.

    Parameters:
        marks (float): Marks obtained out of 100

    Returns:
        str: Letter grade
    """
    # ─── GRADE BOUNDARY CONDITIONS ─────────────────
    # Each elif checks the next lower boundary
    # Order matters — check highest first

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
        # Anything below 45 is a failing grade
        return "F"


def get_gpa_points(letter_grade):
    """
    Convert letter grade to GPA points on a 4.0 scale.

    Parameters:
        letter_grade (str): Letter grade

    Returns:
        float: GPA points
    """
    # ─── GPA POINT MAPPING ─────────────────────────
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
        # F grade gets zero GPA points
        return 0.0


def get_feedback(student_name, marks, letter_grade):
    """
    Generate personalized feedback using nested conditionals.

    Parameters:
        student_name (str): Name of the student
        marks        (float): Marks obtained
        letter_grade (str): Letter grade

    Returns:
        str: Personalized feedback message
    """
    # ─── NESTED CONDITIONAL FEEDBACK ──────────────
    # Outer condition checks grade category
    # Inner condition gives more specific feedback

    if letter_grade in ("A+", "A", "A-"):
        # ─── EXCELLENT PERFORMANCE ─────────────────
        if marks == 100:
            message = (f"Perfect score {student_name}! "
                       f"Absolutely flawless performance.")
        elif marks >= 90:
            message = (f"Outstanding {student_name}! "
                       f"You have truly mastered this subject.")
        else:
            message = (f"Excellent work {student_name}! "
                       f"You are performing at the highest level.")

    elif letter_grade in ("B+", "B", "B-"):
        # ─── GOOD PERFORMANCE ──────────────────────
        if marks >= 75:
            message = (f"Great job {student_name}! "
                       f"Just a little more effort to reach an A.")
        else:
            message = (f"Good work {student_name}. "
                       f"Focus on your weak areas to move up.")

    elif letter_grade in ("C+", "C", "C-"):
        # ─── AVERAGE PERFORMANCE ───────────────────
        if marks >= 55:
            message = (f"Keep going {student_name}. "
                       f"More consistent studying will improve your grade.")
        else:
            message = (f"You are passing {student_name}, but barely. "
                       f"Please put in extra effort this week.")

    elif letter_grade == "D":
        # ─── AT RISK ───────────────────────────────
        message = (f"{student_name}, you are at risk of failing. "
                   f"Attend extra classes and revise thoroughly.")

    else:
        # ─── FAILED ────────────────────────────────
        message = (f"{student_name}, unfortunately you have not passed. "
                   f"Please retake the exam and seek academic support.")

    return message


def display_subject_result(subject_name, marks, letter_grade,
                           gpa_points, feedback):
    """
    Display result for a single subject.

    Parameters:
        subject_name (str): Name of the subject
        marks        (float): Marks obtained
        letter_grade (str): Letter grade
        gpa_points   (float): GPA points
        feedback     (str): Personalized feedback

    Returns:
        None
    """
    # ─── DETERMINE PASS OR FAIL ────────────────────
    status = "Pass" if marks >= PASS_MARKS else "Fail"

    print(f"\n{THIN_LINE}")
    print(f"   RESULT — {subject_name.upper()}")
    print(THIN_LINE)
    print(f"   Marks        : {marks} / {TOTAL_MARKS}")
    print(f"   Percentage   : {marks}%")
    print(f"   Letter Grade : {letter_grade}")
    print(f"   GPA Points   : {gpa_points}")
    print(f"   Status       : {status}")
    print(THIN_LINE)
    print(f"   Feedback     : {feedback}")
    print(THIN_LINE)


def display_overall_summary(student_name, total_marks,
                            subject_count, average_gpa):
    """
    Display overall academic summary for the student.

    Parameters:
        student_name  (str): Name of the student
        total_marks   (float): Total marks across all subjects
        subject_count (int): Number of subjects
        average_gpa   (float): Average GPA points

    Returns:
        None
    """
    # ─── CALCULATE AVERAGES ────────────────────────
    average_marks  = total_marks / subject_count
    overall_grade  = get_letter_grade(average_marks)
    overall_status = "PASS" if average_marks >= PASS_MARKS else "FAIL"

    print(f"\n{SEPARATOR}")
    print(f"   OVERALL SUMMARY — {student_name.upper()}")
    print(SEPARATOR)
    print(f"   Total Marks   : {total_marks} / {subject_count * TOTAL_MARKS}")
    print(f"   Average Marks : {round(average_marks, 2)}%")
    print(f"   Overall Grade : {overall_grade}")
    print(f"   Average GPA   : {round(average_gpa, 2)}")
    print(f"   Final Status  : {overall_status}")

    # ─── FINAL MOTIVATIONAL MESSAGE ────────────────
    # Message changes based on overall performance
    if average_marks >= 85:
        print(f"\n   Congratulations {student_name}! Truly impressive results.")
    elif average_marks >= 70:
        print(f"\n   Well done {student_name}! Solid performance overall.")
    elif average_marks >= 50:
        print(f"\n   You passed {student_name}. Keep working hard.")
    else:
        print(f"\n   {student_name}, do not give up. Work harder next time.")

    print(SEPARATOR)


def run_grade_calculator():
    """
    Main function to run the grade calculator.

    Parameters: None
    Returns: None
    """
    display_header()

    # ─── SUBJECT LIST ──────────────────────────────
    subjects = [
        "Mathematics",
        "English",
        "Physics",
        "Computer Science"
    ]

    while True:
        try:
            # ─── GET STUDENT NAME ──────────────────
            student_name  = get_student_name()
            total_marks   = 0
            total_gpa     = 0
            subject_count = len(subjects)

            print(f"\n   Calculating grades for {student_name}.\n")

            for subject_name in subjects:
                while True:
                    try:
                        # ─── GET MARKS ─────────────
                        marks = get_marks(subject_name)

                        # ─── CALCULATE GRADE ───────
                        letter_grade = get_letter_grade(marks)
                        gpa_points   = get_gpa_points(letter_grade)
                        feedback     = get_feedback(
                            student_name, marks, letter_grade
                        )

                        # ─── DISPLAY RESULT ────────
                        display_subject_result(
                            subject_name,
                            marks,
                            letter_grade,
                            gpa_points,
                            feedback
                        )

                        # ─── ADD TO TOTALS ─────────
                        total_marks += marks
                        total_gpa   += gpa_points
                        break

                    except ValueError as error:
                        print(f"\n   Invalid input: {error}. Try again.")

            # ─── DISPLAY OVERALL SUMMARY ───────────
            display_overall_summary(
                student_name,
                total_marks,
                subject_count,
                total_gpa / subject_count
            )

        except ValueError as error:
            print(f"\n   Invalid input: {error}. Please try again.")

        # ─── ASK TO CONTINUE ───────────────────────
        again = input("\n   Calculate for another student? (yes/no): ").strip().lower()
        if again != "yes":
            print(f"\n{SEPARATOR}")
            print("   Thank you for using the Grade Calculator.")
            print(SEPARATOR)
            break


# ─── ENTRY POINT ───────────────────────────────────
if __name__ == "__main__":
    run_grade_calculator()