"""
Script Purpose: Grade Tracker Using Parallel Lists
Author: Sehar Andleeb
Company: Xeven Solutions
Day: 6 of 30 — Practical Task 2

This script uses two parallel lists to track student names
and grades. It demonstrates finding highest, lowest, average
grades and filtering students who passed using list methods.
"""


# ─── CONSTANTS ─────────────────────────────────────
SEPARATOR  = "=" * 55
THIN_LINE  = "-" * 55
PASS_MARKS = 50


def display_all_students(student_names, student_grades):
    """
    Display all students with their grades and status.

    Parameters:
        student_names  (list): List of student names
        student_grades (list): List of student grades

    Returns:
        None
    """
    print(f"\n{THIN_LINE}")
    print(f"   {'No.':<5} {'Name':<20} {'Grade':<8} {'Status'}")
    print(f"   {'-'*5} {'-'*20} {'-'*8} {'-'*8}")

    for index in range(len(student_names)):
        # ─── DETERMINE PASS OR FAIL ────────────────
        status = ("Pass" if student_grades[index] >= PASS_MARKS
        else "Fail")
        print(f"   {index + 1:<5} "
            f"{student_names[index]:<20} "
            f"{student_grades[index]:<8} "
            f"{status}")

    print(THIN_LINE)


def find_highest(student_names, student_grades):
    """
    Find student with highest grade.

    Parameters:
        student_names  (list): List of student names
        student_grades (list): List of student grades

    Returns:
        tuple: Name and grade of top student
    """
    # ─── FIND MAXIMUM GRADE ────────────────────────
    highest_grade = max(student_grades)
    highest_index = student_grades.index(highest_grade)
    highest_name  = student_names[highest_index]

    return highest_name, highest_grade


def find_lowest(student_names, student_grades):
    """
    Find student with lowest grade.

    Parameters:
        student_names  (list): List of student names
        student_grades (list): List of student grades

    Returns:
        tuple: Name and grade of lowest student
    """
    # ─── FIND MINIMUM GRADE ────────────────────────
    lowest_grade = min(student_grades)
    lowest_index = student_grades.index(lowest_grade)
    lowest_name  = student_names[lowest_index]

    return lowest_name, lowest_grade


def find_average(student_grades):
    """
    Calculate average grade of all students.

    Parameters:
        student_grades (list): List of student grades

    Returns:
        float: Average grade
    """
    # ─── CALCULATE AVERAGE ─────────────────────────
    return sum(student_grades) / len(student_grades)


def find_passed_students(student_names, student_grades):
    """
    Find all students who passed.

    Parameters:
        student_names  (list): List of student names
        student_grades (list): List of student grades

    Returns:
        list: Names of students who passed
    """
    # ─── FILTER PASSED STUDENTS ────────────────────
    # Use list comprehension with condition
    passed = [
        student_names[i]
        for i in range(len(student_names))
        if student_grades[i] >= PASS_MARKS
    ]

    return passed


def run_grade_tracker():
    """
    Main function to run the grade tracker.

    Parameters: None
    Returns: None
    """
    print(f"\n{SEPARATOR}")
    print("   Grade Tracker with Parallel Lists")
    print("   Day 6 — Practical Task 2")
    print(SEPARATOR)

    # ─── PARALLEL LISTS ────────────────────────────
    # Two lists where same index = same student
    student_names = [
        "Ali Hassan",
        "Sara Ahmed",
        "Usman Khan",
        "Fatima Malik",
        "Ahmed Raza",
        "Zara Siddiqui",
        "Bilal Hussain"
    ]

    student_grades = [78, 92, 45, 88, 34, 67, 55]

    # ─── DISPLAY ALL STUDENTS ──────────────────────
    print(f"\n{THIN_LINE}")
    print("   ALL STUDENTS AND GRADES")
    display_all_students(student_names, student_grades)

    # ─── HIGHEST GRADE ─────────────────────────────
    highest_name, highest_grade = find_highest(
        student_names, student_grades
    )

    # ─── LOWEST GRADE ──────────────────────────────
    lowest_name, lowest_grade = find_lowest(
        student_names, student_grades
    )

    # ─── AVERAGE GRADE ─────────────────────────────
    average_grade = find_average(student_grades)

    # ─── PASSED STUDENTS ───────────────────────────
    passed_students = find_passed_students(
        student_names, student_grades
    )

    # ─── DISPLAY STATISTICS ────────────────────────
    print(f"\n{THIN_LINE}")
    print("   GRADE STATISTICS")
    print(THIN_LINE)
    print(f"   Highest Grade  : {highest_grade} — {highest_name}")
    print(f"   Lowest Grade   : {lowest_grade} — {lowest_name}")
    print(f"   Average Grade  : {round(average_grade, 2)}")
    print(f"   Total Students : {len(student_names)}")
    print(f"   Passed         : {len(passed_students)}")
    print(f"   Failed         : "
        f"{len(student_names) - len(passed_students)}")
    print(THIN_LINE)

    # ─── DISPLAY PASSED STUDENTS ───────────────────
    print(f"\n{THIN_LINE}")
    print("   STUDENTS WHO PASSED")
    print(THIN_LINE)
    for index, name in enumerate(passed_students):
        print(f"   {index + 1}. {name}")
    print(THIN_LINE)

    print(f"\n{SEPARATOR}")
    print("   Task 2 completed successfully.")
    print(SEPARATOR)


# ─── ENTRY POINT ───────────────────────────────────
if __name__ == "__main__":
    run_grade_tracker()