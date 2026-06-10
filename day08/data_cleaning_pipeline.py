"""
data_cleaning_pipeline.py
=========================
Day 8 - Task 3: Data Cleaning Pipeline
Week 2: Python Data Structures & Algorithms

Takes a messy list (duplicates, None values, extra whitespace, mixed
case) and runs it through a step-by-step cleaning pipeline using list
comprehensions. Displays before/after comparison with data quality
metrics at each stage.

Author  : Sehar Andleeb
Mentor  : Mubashir Sir (Sr. Machine Learning Engineer)
Company : Xeven Solutions
Date    : 2026
"""

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
SEPARATOR_WIDTH = 55


# ---------------------------------------------------------------------------
# Cleaning Functions (one responsibility each)
# ---------------------------------------------------------------------------

def remove_none_values(data: list) -> list:
    """Filter out None and empty-string entries from the list.

    Args:
        data: Raw list that may contain None or '' values.

    Returns:
        New list with all None and empty-string entries removed.
    """
    # list comprehension: keep only items that are not None and not blank
    # .strip() here catches whitespace-only strings like "  " as well
    return [item for item in data if item is not None and str(item).strip() != ""]


def strip_whitespace(data: list) -> list:
    """Strip leading and trailing whitespace from every string entry.

    Args:
        data: List of strings (should have no None values at this stage).

    Returns:
        New list with each string stripped of surrounding whitespace.
    """
    # .strip() removes spaces, tabs, newlines from both ends
    return [item.strip() for item in data]


def normalize_case(data: list) -> list:
    """Normalize every string to Title Case for consistency.

    Args:
        data: List of strings.

    Returns:
        New list with every string converted to title case.
    """
    # .title() capitalizes the first letter of each word
    return [item.title() for item in data]


def remove_duplicates(data: list) -> list:
    """Remove duplicate entries while preserving original order.

    Uses a seen-set for O(1) lookup on each item, which is faster
    than checking `if item not in result_list` (O(n) per check).

    Args:
        data: List of strings (already normalized).

    Returns:
        New list with duplicates removed, order preserved.
    """
    seen = set()       # tracks which values we've already encountered
    unique = []        # builds the result in original order

    for item in data:
        if item not in seen:
            seen.add(item)
            unique.append(item)

    return unique


def run_pipeline(raw_data: list) -> dict:
    """Execute the full cleaning pipeline step by step.

    Pipeline order:
        1. Remove None / empty strings
        2. Strip whitespace
        3. Normalize to title case
        4. Remove duplicates

    Args:
        raw_data: The original messy list.

    Returns:
        A dictionary with a snapshot of the list after each stage,
        plus before/after quality metrics.
    """
    # --- Stage 1: remove nulls ---
    after_null_removal = remove_none_values(raw_data)

    # --- Stage 2: strip whitespace ---
    after_strip = strip_whitespace(after_null_removal)

    # --- Stage 3: normalize case ---
    after_normalize = normalize_case(after_strip)

    # --- Stage 4: remove duplicates ---
    after_dedup = remove_duplicates(after_normalize)

    # --- Compile metrics ---
    total_raw        = len(raw_data)
    null_count       = sum(1 for item in raw_data if item is None or item == "")
    duplicates_removed = len(after_normalize) - len(after_dedup)
    final_count      = len(after_dedup)
    completeness_pct = (final_count / total_raw * 100) if total_raw > 0 else 0.0

    return {
        "raw":            raw_data,
        "after_null":     after_null_removal,
        "after_strip":    after_strip,
        "after_normalize":after_normalize,
        "after_dedup":    after_dedup,
        "metrics": {
            "total_raw":           total_raw,
            "null_empty_removed":  null_count,
            "duplicates_removed":  duplicates_removed,
            "final_unique_count":  final_count,
            "completeness_pct":    completeness_pct,
        },
    }


# ---------------------------------------------------------------------------
# Display Helpers
# ---------------------------------------------------------------------------

def display_list_side_by_side(label: str, data: list) -> None:
    """Print a labeled list in a clean numbered format.

    Args:
        label : Section heading to display above the list.
        data  : The list to print.
    """
    print(f"\n  {label}  ({len(data)} items)")
    print(f"  {'-' * 40}")
    if not data:
        print("  (empty)")
    else:
        for i, item in enumerate(data, start=1):
            # repr() shows None and whitespace exactly as they are
            print(f"  {i:>3}. {repr(item)}")


def display_pipeline_stages(result: dict) -> None:
    """Print each pipeline stage snapshot so the transformation is visible.

    Args:
        result: The dictionary returned by run_pipeline().
    """
    display_list_side_by_side("RAW INPUT",                result["raw"])
    display_list_side_by_side("Stage 1 — Remove None/Empty", result["after_null"])
    display_list_side_by_side("Stage 2 — Strip Whitespace",  result["after_strip"])
    display_list_side_by_side("Stage 3 — Normalize Case",    result["after_normalize"])
    display_list_side_by_side("Stage 4 — Remove Duplicates", result["after_dedup"])


def display_metrics(metrics: dict) -> None:
    """Print a formatted data quality report.

    Args:
        metrics: The metrics sub-dictionary from run_pipeline().
    """
    print("\n" + "=" * SEPARATOR_WIDTH)
    print("   DATA QUALITY REPORT")
    print("=" * SEPARATOR_WIDTH)
    print(f"  {'Total raw entries':<35} {metrics['total_raw']:>5}")
    print(f"  {'None / empty entries removed':<35} {metrics['null_empty_removed']:>5}")
    print(f"  {'Duplicate entries removed':<35} {metrics['duplicates_removed']:>5}")
    print(f"  {'Final unique clean entries':<35} {metrics['final_unique_count']:>5}")
    print(f"  {'Data completeness':<35} {metrics['completeness_pct']:>4.1f}%")
    print("=" * SEPARATOR_WIDTH)


# ---------------------------------------------------------------------------
# Main Demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * SEPARATOR_WIDTH)
    print("   DATA CLEANING PIPELINE — Day 8, Task 3")
    print("=" * SEPARATOR_WIDTH)

    # --- Intentionally messy dataset ---
    # Contains: duplicates, None, empty strings,
    #           extra whitespace, and inconsistent casing
    messy_data = [
        "  sehar andleeb ",   # leading/trailing whitespace
        "ALI HASSAN",          # all caps
        "sara khan",           # all lowercase
        None,                  # null value
        "  SEHAR ANDLEEB  ",  # duplicate with whitespace + caps
        "bilal ahmed",
        "",                    # empty string
        "Sara Khan",           # duplicate (different case)
        "  zainab malik",      # leading space
        "BILAL AHMED",         # duplicate in caps
        None,                  # second null
        "Omar Farooq",
        "ali hassan",          # duplicate in lowercase
        "  ",                  # whitespace-only string (becomes "" after strip)
        "hina baig",
        "Omar Farooq",         # exact duplicate
        "HINA BAIG",           # duplicate in caps
        "mubashir khan",       # unique entry
    ]

    # --- Run the full pipeline ---
    result = run_pipeline(messy_data)

    # --- Show each transformation stage ---
    print("\n[PIPELINE STAGES — step by step transformation]\n")
    display_pipeline_stages(result)

    # --- Before vs After summary ---
    print("\n\n[BEFORE vs AFTER COMPARISON]")
    print("-" * SEPARATOR_WIDTH)
    print(f"  Before : {len(result['raw'])} entries  →  After : {len(result['after_dedup'])} clean unique entries")
    print(f"  Removed: {len(result['raw']) - len(result['after_dedup'])} total entries cleaned out")

    # --- Final clean list ---
    print("\n[FINAL CLEAN DATA]")
    print("-" * SEPARATOR_WIDTH)
    for i, name in enumerate(result["after_dedup"], start=1):
        print(f"  {i:>3}. {name}")

    # --- Data quality metrics ---
    display_metrics(result["metrics"])

    # --- Demonstrate individual functions independently ---
    print("\n[BONUS — List Comprehension Showcase]")
    print("-" * SEPARATOR_WIDTH)

    sample = ["  python  ", "  MACHINE LEARNING  ", None, "ai engineering", "Python", ""]

    only_valid  = remove_none_values(sample)
    stripped    = strip_whitespace(only_valid)
    normalized  = normalize_case(stripped)
    clean       = remove_duplicates(normalized)

    print(f"  Raw    : {sample}")
    print(f"  Clean  : {clean}")

    print("\n" + "=" * SEPARATOR_WIDTH)
    print("   data_cleaning_pipeline.py — COMPLETE")
    print("=" * SEPARATOR_WIDTH)
