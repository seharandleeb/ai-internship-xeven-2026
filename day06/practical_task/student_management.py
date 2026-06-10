"""
Script Purpose: Student Management System Using Lists
Author: Sehar Andleeb
Company: Xeven Solutions
Day: 6 of 30 — Practical Task 1

This script demonstrates list operations including append,
insert, remove, pop, slicing, and sorting using a student
management system as a real world example.
"""


# ─── CONSTANTS ─────────────────────────────────────
SEPARATOR = "=" * 55
THIN_LINE = "-" * 55


def display_list(label, students):
    """
    Display list with a clear label.

    Parameters:
        label    (str): Label to display above list
        students (list): List of student names

    Returns:
        None
    """
    print(f"\n   {label}")
    print(f"   {THIN_LINE[:40]}")
    for index, name in enumerate(students):
        print(f"   {index + 1}. {name}")
    print(f"   Total: {len(students)} students")


def run_student_management():
    """
    Main function demonstrating all list operations.

    Parameters: None
    Returns: None
    """
    print(f"\n{SEPARATOR}")
    print("   Student Management System")
    print("   Day 6 — Practical Task 1")
    print(SEPARATOR)

    # ─── INITIAL STUDENT LIST ──────────────────────
    # Create list with 5 students
    student_names = [
        "Ali Hassan",
        "Sara Ahmed",
        "Usman Khan",
        "Fatima Malik",
        "Ahmed Raza"
    ]

    display_list("INITIAL STUDENT LIST", student_names)

    # ─── APPEND ────────────────────────────────────
    # append() adds single item at the end of list
    student_names.append("Zara Siddiqui")
    display_list("AFTER append('Zara Siddiqui')", student_names)

    # ─── INSERT ────────────────────────────────────
    # insert(index, value) adds item at specific position
    student_names.insert(2, "Bilal Hussain")
    display_list("AFTER insert(2, 'Bilal Hussain')", student_names)

    # ─── REMOVE ────────────────────────────────────
    # remove() deletes first occurrence of given value
    student_names.remove("Usman Khan")
    display_list("AFTER remove('Usman Khan')", student_names)

    # ─── POP ───────────────────────────────────────
    # pop() removes and returns item at given index
    popped = student_names.pop(0)
    display_list(f"AFTER pop(0) — removed '{popped}'",
                 student_names)

    # ─── SLICING ───────────────────────────────────
    # Slice first 3 students using [0:3]
    first_three = student_names[:3]
    display_list("FIRST 3 STUDENTS (sliced)", first_three)

    # ─── SORT ──────────────────────────────────────
    # sort() sorts list alphabetically in place
    student_names.sort()
    display_list("AFTER sort() — Alphabetical Order",
                 student_names)

    print(f"\n{SEPARATOR}")
    print("   Task 1 completed successfully.")
    print(SEPARATOR)


# ─── ENTRY POINT ───────────────────────────────────
if __name__ == "__main__":
    run_student_management()