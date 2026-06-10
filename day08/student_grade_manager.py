"""
student_grade_manager.py
========================
Day 8 - Task 1: Student Grade Manager
Week 2: Python Data Structures & Algorithms

Demonstrates core list operations: parallel lists, list methods,
sorting, list comprehensions, and finding min/max elements.

Author  : Sehar Andleeb
Mentor  : Mubashir Sir (Sr. Machine Learning Engineer)
Company : Xeven Solutions
Date    : 2026
"""

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
MIN_GRADE = 0
MAX_GRADE = 100
TOP_PERFORMERS_COUNT = 3


# ---------------------------------------------------------------------------
# Core Functions
# ---------------------------------------------------------------------------

def add_student(names: list, grades: list, name: str, grade: float) -> None:
    """Add a new student and their grade to the parallel lists.

    Args:
        names  : List of student names.
        grades : List of student grades (parallel to names).
        name   : Full name of the student to add.
        grade  : Numeric grade (0–100) for the student.

    Raises:
        ValueError: If grade is outside the valid 0–100 range.
    """
    if not (MIN_GRADE <= grade <= MAX_GRADE):
        raise ValueError(f"Grade must be between {MIN_GRADE} and {MAX_GRADE}. Got: {grade}")

    names.append(name)
    grades.append(grade)
    print(f"  ✓ Added '{name}' with grade {grade}")


def remove_student(names: list, grades: list, name: str) -> bool:
    """Remove a student by name from both parallel lists.

    Args:
        names  : List of student names.
        grades : List of student grades.
        name   : Name of the student to remove.

    Returns:
        True if student was found and removed, False otherwise.
    """
    if name in names:
        index = names.index(name)   # find position in names list
        names.pop(index)             # remove name at that index
        grades.pop(index)            # remove matching grade at same index
        print(f"  ✓ Removed '{name}'")
        return True

    print(f"  ✗ Student '{name}' not found.")
    return False


def update_grade(names: list, grades: list, name: str, new_grade: float) -> bool:
    """Update the grade for an existing student.

    Args:
        names     : List of student names.
        grades    : List of student grades.
        name      : Name of the student to update.
        new_grade : The replacement grade value.

    Returns:
        True if update was successful, False if student not found.

    Raises:
        ValueError: If new_grade is outside the valid 0–100 range.
    """
    if not (MIN_GRADE <= new_grade <= MAX_GRADE):
        raise ValueError(f"Grade must be between {MIN_GRADE} and {MAX_GRADE}.")

    if name in names:
        index = names.index(name)
        old_grade = grades[index]
        grades[index] = new_grade   # direct index assignment updates the list in-place
        print(f"  ✓ Updated '{name}': {old_grade} → {new_grade}")
        return True

    print(f"  ✗ Student '{name}' not found.")
    return False


def get_average(grades: list) -> float:
    """Calculate the mean grade across all students.

    Args:
        grades: List of numeric grade values.

    Returns:
        The average grade, or 0.0 if the list is empty.
    """
    if not grades:
        return 0.0
    return sum(grades) / len(grades)


def get_highest(names: list, grades: list) -> tuple:
    """Find the student with the highest grade.

    Args:
        names  : List of student names.
        grades : List of student grades.

    Returns:
        A tuple of (name, grade) for the top scorer, or (None, None) if empty.
    """
    if not grades:
        return (None, None)

    highest_grade = max(grades)
    highest_index = grades.index(highest_grade)
    return (names[highest_index], highest_grade)


def get_lowest(names: list, grades: list) -> tuple:
    """Find the student with the lowest grade.

    Args:
        names  : List of student names.
        grades : List of student grades.

    Returns:
        A tuple of (name, grade) for the lowest scorer, or (None, None) if empty.
    """
    if not grades:
        return (None, None)

    lowest_grade = min(grades)
    lowest_index = grades.index(lowest_grade)
    return (names[lowest_index], lowest_grade)


def sort_by_grade_descending(names: list, grades: list) -> tuple:
    """Return new lists sorted by grade from highest to lowest.

    Does NOT modify the original lists (returns sorted copies).

    Args:
        names  : List of student names.
        grades : List of student grades.

    Returns:
        A tuple of (sorted_names, sorted_grades) in descending grade order.
    """
    # zip pairs each name with its grade, sorted by grade (index 1) descending
    paired = sorted(zip(names, grades), key=lambda pair: pair[1], reverse=True)

    # unzip the sorted pairs back into two separate lists
    sorted_names, sorted_grades = zip(*paired) if paired else ([], [])
    return list(sorted_names), list(sorted_grades)


def get_top_performers(names: list, grades: list, count: int = TOP_PERFORMERS_COUNT) -> list:
    """Return the top N students sorted by grade descending.

    Args:
        names  : List of student names.
        grades : List of student grades.
        count  : Number of top performers to return (default: 3).

    Returns:
        List of (name, grade) tuples for the top performers.
    """
    sorted_names, sorted_grades = sort_by_grade_descending(names, grades)
    # list slicing: take only the first `count` items
    return list(zip(sorted_names[:count], sorted_grades[:count]))


def filter_above_average(names: list, grades: list) -> list:
    """Use list comprehension to find students scoring above the class average.

    Args:
        names  : List of student names.
        grades : List of student grades.

    Returns:
        List of (name, grade) tuples for students above the average.
    """
    average = get_average(grades)
    # list comprehension: build a new list by filtering (name, grade) pairs
    return [(name, grade) for name, grade in zip(names, grades) if grade > average]


def filter_below_average(names: list, grades: list) -> list:
    """Use list comprehension to find students scoring below the class average.

    Args:
        names  : List of student names.
        grades : List of student grades.

    Returns:
        List of (name, grade) tuples for students below the average.
    """
    average = get_average(grades)
    return [(name, grade) for name, grade in zip(names, grades) if grade < average]


# ---------------------------------------------------------------------------
# Display Helper
# ---------------------------------------------------------------------------

def display_all_students(names: list, grades: list) -> None:
    """Print a formatted table of all students and their grades.

    Args:
        names  : List of student names.
        grades : List of student grades.
    """
    if not names:
        print("  (No students enrolled)")
        return

    print(f"\n  {'Student':<20} {'Grade':>6}")
    print(f"  {'-'*20} {'-'*6}")
    for name, grade in zip(names, grades):
        print(f"  {name:<20} {grade:>6.1f}")
    print()


# ---------------------------------------------------------------------------
# Main Demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 55)
    print("   STUDENT GRADE MANAGER — Day 8, Task 1")
    print("=" * 55)

    # --- Initialize parallel lists (empty to start) ---
    student_names = []
    student_grades = []

    # --- Add students ---
    print("\n[1] Adding students...")
    add_student(student_names, student_grades, "Sehar Andleeb",   92.5)
    add_student(student_names, student_grades, "Ali Hassan",       78.0)
    add_student(student_names, student_grades, "Sara Khan",        88.5)
    add_student(student_names, student_grades, "Bilal Ahmed",      65.0)
    add_student(student_names, student_grades, "Zainab Malik",     95.0)
    add_student(student_names, student_grades, "Omar Farooq",      71.5)
    add_student(student_names, student_grades, "Hina Baig",        55.0)

    display_all_students(student_names, student_grades)

    # --- Update a grade ---
    print("[2] Updating a grade...")
    update_grade(student_names, student_grades, "Ali Hassan", 82.0)

    # --- Remove a student ---
    print("\n[3] Removing a student...")
    remove_student(student_names, student_grades, "Hina Baig")

    # --- Class statistics ---
    print("\n[4] Class Statistics")
    print("-" * 35)
    class_average = get_average(student_grades)
    top_name, top_grade = get_highest(student_names, student_grades)
    low_name, low_grade = get_lowest(student_names, student_grades)

    print(f"  Class Average : {class_average:.2f}")
    print(f"  Highest Grade : {top_name} ({top_grade})")
    print(f"  Lowest Grade  : {low_name}  ({low_grade})")

    # --- Top 3 performers ---
    print("\n[5] Top 3 Performers (sorted descending)")
    print("-" * 35)
    top_performers = get_top_performers(student_names, student_grades)
    for rank, (name, grade) in enumerate(top_performers, start=1):
        print(f"  #{rank}  {name:<20} {grade:.1f}")

    # --- List comprehension: above average ---
    print("\n[6] Students ABOVE Average (list comprehension)")
    print("-" * 35)
    above_avg = filter_above_average(student_names, student_grades)
    for name, grade in above_avg:
        print(f"  ✓  {name:<20} {grade:.1f}")

    # --- List comprehension: below average ---
    print("\n[7] Students BELOW Average (list comprehension)")
    print("-" * 35)
    below_avg = filter_below_average(student_names, student_grades)
    for name, grade in below_avg:
        print(f"  ✗  {name:<20} {grade:.1f}")

    print("\n" + "=" * 55)
    print("   student_grade_manager.py — COMPLETE")
    print("=" * 55)