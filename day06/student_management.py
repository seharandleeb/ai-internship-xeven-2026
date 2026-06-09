"""
Script Purpose: Student Management System Using Lists
Author: Sehar Andleeb
Company: Xeven Solutions
Day: 6 of 30

This script builds a complete student management system
using Python lists. It demonstrates real world application
of list operations including adding, removing, searching,
and sorting student records.
"""


# ─── CONSTANTS ─────────────────────────────────────
SEPARATOR    = "=" * 55
THIN_LINE    = "-" * 55
APP_NAME     = "Student Management System"
PASS_MARKS   = 50


def display_header():
    """
    Display application header.

    Parameters: None
    Returns: None
    """
    print(f"\n{SEPARATOR}")
    print(f"   {APP_NAME}")
    print(f"   Day 6 — Python Lists")
    print(SEPARATOR)


def display_menu():
    """
    Display main menu options.

    Parameters: None
    Returns: None
    """
    print(f"\n{THIN_LINE}")
    print("   MAIN MENU")
    print(THIN_LINE)
    print("   1. Add Student")
    print("   2. Remove Student")
    print("   3. View All Students")
    print("   4. Search Student")
    print("   5. Sort Students by Marks")
    print("   6. View Top 3 Students")
    print("   7. View Failed Students")
    print("   8. Class Statistics")
    print("   9. Exit")
    print(THIN_LINE)


def add_student(student_names, student_marks):
    """
    Add a new student to the system.

    Parameters:
        student_names (list): List of student names
        student_marks (list): List of student marks

    Returns:
        None
    """
    try:
        name  = input("   Enter student name  : ").strip()
        marks = float(input("   Enter student marks : "))

        # ─── VALIDATE MARKS RANGE ──────────────────
        if marks < 0 or marks > 100:
            print("   Invalid marks. Must be between 0 and 100.")
            return

        # ─── CHECK IF STUDENT EXISTS ───────────────
        if name.lower() in [n.lower() for n in student_names]:
            print(f"   Student {name} already exists.")
            return

        # ─── ADD TO BOTH LISTS ─────────────────────
        student_names.append(name)
        student_marks.append(marks)
        print(f"\n   Student {name} added successfully.")

    except ValueError:
        print("   Invalid input. Please enter correct values.")


def remove_student(student_names, student_marks):
    """
    Remove a student from the system by name.

    Parameters:
        student_names (list): List of student names
        student_marks (list): List of student marks

    Returns:
        None
    """
    name = input("   Enter student name to remove: ").strip()

    # ─── SEARCH FOR STUDENT ────────────────────────
    for index, student in enumerate(student_names):
        if student.lower() == name.lower():
            # ─── REMOVE FROM BOTH LISTS ────────────
            removed_name  = student_names.pop(index)
            removed_marks = student_marks.pop(index)
            print(f"\n   Removed: {removed_name} "
                  f"with marks {removed_marks}")
            return

    print(f"   Student {name} not found.")


def view_all_students(student_names, student_marks):
    """
    Display all students with their marks and status.

    Parameters:
        student_names (list): List of student names
        student_marks (list): List of student marks

    Returns:
        None
    """
    print(f"\n{THIN_LINE}")
    print("   ALL STUDENTS")
    print(THIN_LINE)

    # ─── CHECK IF LIST IS EMPTY ────────────────────
    if len(student_names) == 0:
        print("   No students registered yet.")
        return

    print(f"   {'No.':<5} {'Name':<20} {'Marks':<10} {'Status'}")
    print(f"   {'-'*5} {'-'*20} {'-'*10} {'-'*10}")

    for index in range(len(student_names)):
        status = "Pass" if student_marks[index] >= PASS_MARKS else "Fail"
        print(f"   {index + 1:<5} "
              f"{student_names[index]:<20} "
              f"{student_marks[index]:<10} "
              f"{status}")

    print(THIN_LINE)


def search_student(student_names, student_marks):
    """
    Search for a student by name and display their details.

    Parameters:
        student_names (list): List of student names
        student_marks (list): List of student marks

    Returns:
        None
    """
    name = input("   Enter student name to search: ").strip()

    # ─── LINEAR SEARCH THROUGH LIST ────────────────
    for index, student in enumerate(student_names):
        if student.lower() == name.lower():
            status = ("Pass" if student_marks[index] >= PASS_MARKS
                      else "Fail")
            print(f"\n{THIN_LINE}")
            print(f"   STUDENT FOUND")
            print(THIN_LINE)
            print(f"   Name     : {student_names[index]}")
            print(f"   Marks    : {student_marks[index]}")
            print(f"   Position : {index + 1} of "
                  f"{len(student_names)}")
            print(f"   Status   : {status}")
            print(THIN_LINE)
            return

    print(f"   Student {name} not found.")


def sort_students(student_names, student_marks):
    """
    Sort students by marks in descending order.

    Parameters:
        student_names (list): List of student names
        student_marks (list): List of student marks

    Returns:
        None
    """
    if len(student_names) == 0:
        print("   No students to sort.")
        return

    # ─── COMBINE AND SORT ──────────────────────────
    # Zip names and marks together for sorting
    combined = list(zip(student_names, student_marks))
    combined.sort(key=lambda x: x[1], reverse=True)

    # ─── UNPACK BACK TO SEPARATE LISTS ────────────
    for index, (name, marks) in enumerate(combined):
        student_names[index] = name
        student_marks[index] = marks

    print("\n   Students sorted by marks successfully.")
    view_all_students(student_names, student_marks)


def view_top_students(student_names, student_marks):
    """
    Display top 3 students by marks.

    Parameters:
        student_names (list): List of student names
        student_marks (list): List of student marks

    Returns:
        None
    """
    if len(student_names) == 0:
        print("   No students registered yet.")
        return

    # ─── COMBINE AND SORT ──────────────────────────
    combined = list(zip(student_names, student_marks))
    combined.sort(key=lambda x: x[1], reverse=True)

    # ─── SLICE TOP 3 ───────────────────────────────
    top_students = combined[:3]

    print(f"\n{THIN_LINE}")
    print("   TOP 3 STUDENTS")
    print(THIN_LINE)

    medals = ["Gold", "Silver", "Bronze"]

    for index, (name, marks) in enumerate(top_students):
        medal = medals[index] if index < len(medals) else ""
        print(f"   {index + 1}. {name:<20} {marks}  {medal}")

    print(THIN_LINE)


def view_failed_students(student_names, student_marks):
    """
    Display all students who failed.

    Parameters:
        student_names (list): List of student names
        student_marks (list): List of student marks

    Returns:
        None
    """
    # ─── FILTER FAILED STUDENTS ────────────────────
    failed_names  = []
    failed_marks  = []

    for index in range(len(student_names)):
        if student_marks[index] < PASS_MARKS:
            failed_names.append(student_names[index])
            failed_marks.append(student_marks[index])

    print(f"\n{THIN_LINE}")
    print("   FAILED STUDENTS")
    print(THIN_LINE)

    if len(failed_names) == 0:
        print("   All students passed.")
    else:
        for index in range(len(failed_names)):
            print(f"   {failed_names[index]:<20} "
                  f"{failed_marks[index]}")

    print(THIN_LINE)


def class_statistics(student_names, student_marks):
    """
    Display overall class statistics.

    Parameters:
        student_names (list): List of student names
        student_marks (list): List of student marks

    Returns:
        None
    """
    if len(student_names) == 0:
        print("   No students registered yet.")
        return

    # ─── CALCULATE STATISTICS ──────────────────────
    total_students  = len(student_names)
    average_marks   = sum(student_marks) / total_students
    highest_marks   = max(student_marks)
    lowest_marks    = min(student_marks)
    passed          = sum(1 for m in student_marks
                         if m >= PASS_MARKS)
    failed          = total_students - passed

    print(f"\n{THIN_LINE}")
    print("   CLASS STATISTICS")
    print(THIN_LINE)
    print(f"   Total Students  : {total_students}")
    print(f"   Average Marks   : {round(average_marks, 2)}")
    print(f"   Highest Marks   : {highest_marks}")
    print(f"   Lowest Marks    : {lowest_marks}")
    print(f"   Passed          : {passed}")
    print(f"   Failed          : {failed}")
    print(f"   Pass Rate       : "
          f"{round(passed / total_students * 100, 1)}%")
    print(THIN_LINE)


def run_student_management():
    """
    Main function to run the student management system.

    Parameters: None
    Returns: None
    """
    display_header()

    # ─── INITIALIZE EMPTY LISTS ────────────────────
    student_names = []
    student_marks = []

    while True:
        display_menu()
        choice = input("   Enter choice (1-9): ").strip()

        if choice == "1":
            add_student(student_names, student_marks)
        elif choice == "2":
            remove_student(student_names, student_marks)
        elif choice == "3":
            view_all_students(student_names, student_marks)
        elif choice == "4":
            search_student(student_names, student_marks)
        elif choice == "5":
            sort_students(student_names, student_marks)
        elif choice == "6":
            view_top_students(student_names, student_marks)
        elif choice == "7":
            view_failed_students(student_names, student_marks)
        elif choice == "8":
            class_statistics(student_names, student_marks)
        elif choice == "9":
            print(f"\n{SEPARATOR}")
            print("   Thank you for using Student Management System.")
            print(SEPARATOR)
            break
        else:
            print("   Invalid choice. Please enter 1 to 9.")


# ─── ENTRY POINT ───────────────────────────────────
if __name__ == "__main__":
    run_student_management()