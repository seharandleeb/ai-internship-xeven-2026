"""
Day 10 - Task 1: Student Information System
============================================
Demonstrates nested dictionaries, JSON persistence, and data analysis functions.
Connection to AI Engineering: LLM training pipelines store per-sample metadata
(labels, splits, token counts) in exactly this nested dict -> JSON pattern.

Author: Sehar Andleeb
Internship: Xeven Solutions, Lahore — AI Engineering
Mentor: Mubashir Sir (Sr. Machine Learning Engineer)
Date: Day 10 of 30-Day AI Engineering Roadmap
"""

import json
import os
from typing import Optional

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
DATA_FILE = "students.json"
PASSING_GRADE = 50.0
GRADE_BOUNDARIES = {
    "A+": 95, "A": 90, "A-": 85,
    "B+": 80, "B": 75, "B-": 70,
    "C+": 65, "C": 60, "C-": 55,
    "D": 50, "F": 0,
}


# ---------------------------------------------------------------------------
# Persistence helpers
# ---------------------------------------------------------------------------

def load_students(filepath: str = DATA_FILE) -> dict:
    """
    Load student records from a JSON file.

    Args:
        filepath: Path to the JSON file containing student data.

    Returns:
        Dictionary of student records, or empty dict if file not found.
    """
    if not os.path.exists(filepath):
        return {}

    try:
        with open(filepath, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        print(f"[INFO] Loaded {len(data)} student(s) from '{filepath}'.")
        return data
    except (json.JSONDecodeError, OSError) as exc:
        print(f"[ERROR] Could not read '{filepath}': {exc}")
        return {}


def save_students(students: dict, filepath: str = DATA_FILE) -> bool:
    """
    Persist student records to a JSON file.

    Args:
        students: Dictionary mapping student IDs to their records.
        filepath: Destination file path.

    Returns:
        True if saved successfully, False otherwise.
    """
    try:
        with open(filepath, "w", encoding="utf-8") as fh:
            json.dump(students, fh, indent=4, ensure_ascii=False)
        print(f"[INFO] Saved {len(students)} student(s) to '{filepath}'.")
        return True
    except OSError as exc:
        print(f"[ERROR] Could not save to '{filepath}': {exc}")
        return False


# ---------------------------------------------------------------------------
# CRUD operations
# ---------------------------------------------------------------------------

def add_student(
    students: dict,
    student_id: str,
    name: str,
    age: int,
    grades: Optional[dict] = None,
) -> bool:
    """
    Add a new student record to the registry.

    Args:
        students: The in-memory student registry (modified in-place).
        student_id: Unique identifier string (e.g. "S001").
        name: Full name of the student.
        age: Age in years.
        grades: Optional dict mapping subject names to numeric scores (0-100).

    Returns:
        True if added successfully, False if the ID already exists.
    """
    if student_id in students:
        print(f"[WARN] Student ID '{student_id}' already exists. Use update functions.")
        return False

    students[student_id] = {
        "name": name,
        "age": age,
        "grades": grades if grades is not None else {},  # {subject: score}
    }
    print(f"[INFO] Added student: {name} (ID: {student_id}).")
    return True


def update_grade(
    students: dict,
    student_id: str,
    subject: str,
    score: float,
) -> bool:
    """
    Add or update a subject grade for an existing student.

    Args:
        students: The in-memory student registry.
        student_id: Target student's unique identifier.
        subject: Subject name (e.g. "Mathematics").
        score: Numeric score between 0 and 100.

    Returns:
        True on success, False if the student ID is not found or score invalid.
    """
    if student_id not in students:
        print(f"[ERROR] Student '{student_id}' not found.")
        return False

    if not (0 <= score <= 100):
        print(f"[ERROR] Score {score} is out of range (0-100).")
        return False

    # O(1) dict insert / update
    students[student_id]["grades"][subject] = score
    print(f"[INFO] Updated {students[student_id]['name']} — {subject}: {score}.")
    return True


# ---------------------------------------------------------------------------
# Analysis functions
# ---------------------------------------------------------------------------

def get_student_average(students: dict, student_id: str) -> Optional[float]:
    """
    Calculate the average grade for a single student.

    Args:
        students: The in-memory student registry.
        student_id: Target student's unique identifier.

    Returns:
        Average score as a float, or None if student not found / no grades.
    """
    if student_id not in students:
        print(f"[ERROR] Student '{student_id}' not found.")
        return None

    grades = students[student_id]["grades"]
    if not grades:
        print(f"[WARN] No grades recorded for '{student_id}'.")
        return None

    # sum() and len() on .values() — O(n) over subjects
    average = sum(grades.values()) / len(grades)
    return round(average, 2)


def find_top_student(students: dict) -> Optional[tuple]:
    """
    Identify the student with the highest average grade.

    Args:
        students: The in-memory student registry.

    Returns:
        Tuple of (student_id, name, average) or None if registry is empty.
    """
    if not students:
        print("[WARN] No students in registry.")
        return None

    best_id = None
    best_avg = -1.0

    # Iterate over all students — O(n * subjects)
    for sid, info in students.items():
        avg = get_student_average(students, sid)
        if avg is not None and avg > best_avg:
            best_avg = avg
            best_id = sid

    if best_id is None:
        return None

    return best_id, students[best_id]["name"], best_avg


def _letter_grade(score: float) -> str:
    """
    Convert a numeric score to a letter grade.

    Args:
        score: Numeric score (0-100).

    Returns:
        Letter grade string such as 'A+', 'B', 'F', etc.
    """
    for letter, threshold in GRADE_BOUNDARIES.items():
        if score >= threshold:
            return letter
    return "F"


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

def generate_report(students: dict) -> None:
    """
    Print a formatted performance report for all students, sorted by GPA.

    Args:
        students: The in-memory student registry.
    """
    if not students:
        print("No student data available for report.")
        return

    # Build a list of (avg, id, info) for sorting — O(n)
    ranked = []
    for sid, info in students.items():
        avg = get_student_average(students, sid)
        ranked.append((avg if avg is not None else 0.0, sid, info))

    # Sort descending by average
    ranked.sort(key=lambda x: x[0], reverse=True)

    # ── Header ──────────────────────────────────────────────────────────────
    print("\n" + "=" * 65)
    print(f"{'STUDENT PERFORMANCE REPORT':^65}")
    print("=" * 65)
    print(f"{'Rank':<5} {'Name':<20} {'ID':<8} {'GPA':>7} {'Grade':>6}")
    print("-" * 65)

    for rank, (avg, sid, info) in enumerate(ranked, start=1):
        letter = _letter_grade(avg)
        status = "✓" if avg >= PASSING_GRADE else "✗"
        print(
            f"{rank:<5} {info['name']:<20} {sid:<8} "
            f"{avg:>7.2f} {letter:>6}  {status}"
        )

    # ── Per-student subject breakdown ───────────────────────────────────────
    print("\n" + "-" * 65)
    print("SUBJECT BREAKDOWN")
    print("-" * 65)
    for _, sid, info in ranked:
        print(f"\n  {info['name']} (Age {info['age']}):")
        if info["grades"]:
            for subject, score in sorted(info["grades"].items()):
                bar = "█" * int(score // 10)
                print(f"    {subject:<20} {score:>6.1f}  {bar}")
        else:
            print("    No grades recorded.")

    print("\n" + "=" * 65 + "\n")


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("╔══════════════════════════════════════════╗")
    print("║   Day 10 — Student Information System    ║")
    print("╚══════════════════════════════════════════╝\n")

    # ── Load existing data (or start fresh) ─────────────────────────────────
    registry = load_students()

    # ── Seed demo data if registry is empty ─────────────────────────────────
    if not registry:
        print("[DEMO] Seeding sample student data...\n")

        add_student(registry, "S001", "Ayesha Khan", 20, {
            "Mathematics": 92, "Physics": 88, "AI Fundamentals": 95,
            "Python Programming": 97, "Data Structures": 90,
        })
        add_student(registry, "S002", "Bilal Ahmed", 21, {
            "Mathematics": 74, "Physics": 69, "AI Fundamentals": 78,
            "Python Programming": 82, "Data Structures": 71,
        })
        add_student(registry, "S003", "Sana Malik", 19, {
            "Mathematics": 55, "Physics": 60, "AI Fundamentals": 63,
            "Python Programming": 70, "Data Structures": 58,
        })
        add_student(registry, "S004", "Usman Tariq", 22, {
            "Mathematics": 98, "Physics": 95, "AI Fundamentals": 99,
            "Python Programming": 100, "Data Structures": 97,
        })
        add_student(registry, "S005", "Fatima Zahra", 20)  # no grades yet

    # ── Demonstrate CRUD ─────────────────────────────────────────────────────
    print("\n--- Updating grades ---")
    update_grade(registry, "S005", "Mathematics", 88)
    update_grade(registry, "S005", "Python Programming", 91)
    update_grade(registry, "S005", "AI Fundamentals", 85)

    # ── Query individual averages ─────────────────────────────────────────────
    print("\n--- Individual averages ---")
    for sid in list(registry.keys())[:3]:
        avg = get_student_average(registry, sid)
        print(f"  {registry[sid]['name']}: {avg}")

    # ── Find top student ─────────────────────────────────────────────────────
    print("\n--- Top student ---")
    top = find_top_student(registry)
    if top:
        tid, tname, tavg = top
        print(f"  🏆 {tname} (ID: {tid}) — Average: {tavg}")

    # ── Generate full report ─────────────────────────────────────────────────
    generate_report(registry)

    # ── Persist to JSON ──────────────────────────────────────────────────────
    save_students(registry)
    print("[DONE] student_information_system.py complete.\n")
