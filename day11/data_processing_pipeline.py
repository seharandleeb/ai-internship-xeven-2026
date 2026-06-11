"""
Day 11 - Task 1: Data Processing Pipeline
==========================================
Demonstrates for loops, enumerate(), zip(), break, and continue
for processing 1000 records with multiple data sources.

Author: Sehar Andleeb
Date: 2026-06-11
Internship: Xeven Solutions AI Engineering Internship 2026
"""

import random
import time


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
TOTAL_RECORDS = 1000
CRITICAL_ERROR_THRESHOLD = 950   # Stop processing if record index exceeds this
INVALID_MARKER = -1               # Sentinel value marking an invalid record
MIN_VALID_SCORE = 0
MAX_VALID_SCORE = 100


# ---------------------------------------------------------------------------
# Data Generation Helpers
# ---------------------------------------------------------------------------

def generate_employee_records(count: int) -> list[dict]:
    """
    Generate a list of simulated employee records.

    Some records are intentionally invalid (score == INVALID_MARKER) to
    exercise the `continue` path in the processing loop.

    Args:
        count: Number of records to generate.

    Returns:
        List of employee dictionaries with keys:
        'id', 'name', 'department', 'score'.
    """
    departments = ["Engineering", "Marketing", "Sales", "HR", "Finance"]
    first_names = ["Ali", "Sara", "Umar", "Zara", "Hassan", "Fatima",
                   "Bilal", "Ayesha", "Kamran", "Nadia"]
    last_names  = ["Khan", "Ahmed", "Malik", "Hussain", "Sheikh",
                   "Qureshi", "Chaudhry", "Butt", "Mirza", "Iqbal"]

    records = []
    for i in range(1, count + 1):
        # ~5 % of records are invalid to trigger continue
        if random.random() < 0.05:
            score = INVALID_MARKER
        else:
            score = random.randint(MIN_VALID_SCORE, MAX_VALID_SCORE)

        records.append({
            "id":         i,
            "name":       f"{random.choice(first_names)} {random.choice(last_names)}",
            "department": random.choice(departments),
            "score":      score,
        })
    return records


def generate_performance_ratings(count: int) -> list[float]:
    """
    Generate a parallel list of performance-rating multipliers.

    Args:
        count: Number of ratings to generate (must match employee count).

    Returns:
        List of float multipliers in the range [0.8, 1.5].
    """
    return [round(random.uniform(0.8, 1.5), 2) for _ in range(count)]


# ---------------------------------------------------------------------------
# Core Processing
# ---------------------------------------------------------------------------

def calculate_grade(adjusted_score: float) -> str:
    """
    Convert a numeric score to a letter grade.

    Args:
        adjusted_score: Score after applying performance-rating multiplier.

    Returns:
        Letter grade string: 'A', 'B', 'C', 'D', or 'F'.
    """
    if adjusted_score >= 90:
        return "A"
    elif adjusted_score >= 80:
        return "B"
    elif adjusted_score >= 70:
        return "C"
    elif adjusted_score >= 60:
        return "D"
    return "F"


def process_records(
    employees: list[dict],
    ratings: list[float],
) -> tuple[list[dict], dict]:
    """
    Process employee records using for loop, enumerate(), zip(),
    break, and continue.

    Processing rules:
    - Skip records whose score equals INVALID_MARKER (continue).
    - Stop processing entirely if record index > CRITICAL_ERROR_THRESHOLD (break).
    - Combine employee data with performance ratings via zip().
    - Track progress with enumerate().

    Args:
        employees: List of employee record dictionaries.
        ratings:   Parallel list of performance-rating multipliers.

    Returns:
        Tuple of:
          - processed: List of enriched employee dictionaries.
          - stats:     Summary statistics dictionary.
    """
    if len(employees) != len(ratings):
        raise ValueError(
            f"Length mismatch: {len(employees)} employees vs "
            f"{len(ratings)} ratings. Lists must be the same length."
        )

    processed      = []
    skipped_count  = 0
    stopped_early  = False

    print(f"\n{'='*60}")
    print(f"  DATA PROCESSING PIPELINE — {len(employees):,} Records")
    print(f"{'='*60}")

    # enumerate() gives (index, value); zip() merges two iterables in lock-step
    for idx, (employee, rating) in enumerate(zip(employees, ratings), start=1):

        # --- progress heartbeat every 100 records ---
        if idx % 100 == 0:
            pct = (idx / len(employees)) * 100
            print(f"  [Progress] Record #{idx:>4} of {len(employees):,} "
                  f"processed — {pct:.0f}% complete")

        # --- break: critical-error guard ---
        if employee["id"] > CRITICAL_ERROR_THRESHOLD:
            print(f"\n  [BREAK] Critical threshold reached at record #{idx}. "
                  "Halting pipeline.")
            stopped_early = True
            break

        # --- continue: skip invalid records ---
        if employee["score"] == INVALID_MARKER:
            skipped_count += 1
            continue   # jump to the next iteration; no processing for this record

        # --- transformation: apply performance-rating multiplier ---
        adjusted_score = min(employee["score"] * rating, 100.0)
        grade          = calculate_grade(adjusted_score)

        processed.append({
            **employee,                           # spread original fields
            "rating":         rating,
            "adjusted_score": round(adjusted_score, 2),
            "grade":          grade,
        })

    # --- build summary stats ---
    scores = [r["adjusted_score"] for r in processed]
    stats = {
        "total_input":    len(employees),
        "total_processed": len(processed),
        "total_skipped":  skipped_count,
        "stopped_early":  stopped_early,
        "average_score":  round(sum(scores) / len(scores), 2) if scores else 0,
        "highest_score":  max(scores) if scores else 0,
        "lowest_score":   min(scores) if scores else 0,
        "grade_distribution": {
            grade: sum(1 for r in processed if r["grade"] == grade)
            for grade in ["A", "B", "C", "D", "F"]
        },
    }

    return processed, stats


def display_stats(stats: dict) -> None:
    """
    Pretty-print summary statistics after processing.

    Args:
        stats: Dictionary returned by process_records().
    """
    print(f"\n{'='*60}")
    print("  PROCESSING SUMMARY")
    print(f"{'='*60}")
    print(f"  Total input records   : {stats['total_input']:,}")
    print(f"  Records processed     : {stats['total_processed']:,}")
    print(f"  Records skipped       : {stats['total_skipped']:,}  (invalid data)")
    print(f"  Stopped early         : {stats['stopped_early']}")
    print(f"  Average adjusted score: {stats['average_score']}")
    print(f"  Highest score         : {stats['highest_score']}")
    print(f"  Lowest score          : {stats['lowest_score']}")
    print(f"\n  Grade Distribution:")
    for grade, count in stats["grade_distribution"].items():
        bar = "█" * (count // 10)   # simple text bar chart
        print(f"    {grade}  {bar}  ({count:,})")
    print(f"{'='*60}\n")


def demonstrate_zip_validation() -> None:
    """
    Demonstrate zip() length validation with a small example.

    zip() silently truncates to the shortest iterable, which can hide
    data-alignment bugs. This function shows how to detect that.
    """
    print("\n--- zip() Length-Validation Demo ---")
    names   = ["Sehar", "Ali", "Sara", "Umar"]
    scores  = [95, 87, 76]           # intentionally shorter

    # Detect mismatch BEFORE zip()
    if len(names) != len(scores):
        print(f"  WARNING: names({len(names)}) and scores({len(scores)}) "
              "differ in length — data may be misaligned!")

    # zip() still works but truncates to 3 pairs
    pairs = list(zip(names, scores))
    print(f"  zip() produced {len(pairs)} pairs (truncated): {pairs}")
    print("  Always validate lengths when combining data sources.\n")


# ---------------------------------------------------------------------------
# Entry Point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    random.seed(42)   # reproducible output

    # 1. Generate synthetic data
    print("Generating employee records and performance ratings...")
    employee_data = generate_employee_records(TOTAL_RECORDS)
    rating_data   = generate_performance_ratings(TOTAL_RECORDS)

    # 2. Run the pipeline
    try:
        processed_records, summary = process_records(employee_data, rating_data)
        display_stats(summary)
    except ValueError as e:
        print(f"[ERROR] Pipeline aborted: {e}")

    # 3. Show zip() safety demo
    demonstrate_zip_validation()

    # 4. Preview a few processed records
    print("Sample processed records (first 3):")
    for record in processed_records[:3]:
        print(f"  {record}")
