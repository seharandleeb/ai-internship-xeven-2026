"""
Script Purpose: List Operations — Sorting, Searching,
                and Error Handling
Author: Sehar Andleeb
Company: Xeven Solutions
Day: 6 of 30

This script demonstrates advanced list operations including
sorting algorithms, searching techniques, and graceful
handling of IndexError and ValueError exceptions.
"""


# ─── CONSTANTS ─────────────────────────────────────
SEPARATOR = "=" * 55
THIN_LINE = "-" * 55


def demonstrate_sorting():
    """
    Demonstrate different sorting techniques on lists.

    Parameters: None
    Returns: None
    """
    print(f"\n{THIN_LINE}")
    print("   SORTING")
    print(THIN_LINE)

    numbers = [64, 34, 25, 12, 22, 11, 90]
    print(f"   Original         : {numbers}")

    # ─── SORT IN PLACE ─────────────────────────────
    # sort() modifies the original list
    numbers.sort()
    print(f"   Ascending        : {numbers}")

    numbers.sort(reverse=True)
    print(f"   Descending       : {numbers}")

    # ─── SORTED FUNCTION ───────────────────────────
    # sorted() returns new list, original unchanged
    original = [64, 34, 25, 12, 22, 11, 90]
    sorted_list = sorted(original)
    print(f"\n   Original (same)  : {original}")
    print(f"   sorted()         : {sorted_list}")

    # ─── SORT STRINGS ──────────────────────────────
    names = ["Zara", "Ali", "Sara", "Ahmed", "Fatima"]
    print(f"\n   Names original   : {names}")
    names.sort()
    print(f"   Names sorted     : {names}")


def demonstrate_searching():
    """
    Demonstrate linear search and in operator in lists.

    Parameters: None
    Returns: None
    """
    print(f"\n{THIN_LINE}")
    print("   SEARCHING")
    print(THIN_LINE)

    numbers = [10, 25, 36, 47, 58, 69, 70, 81, 92]
    print(f"   List             : {numbers}")

    # ─── IN OPERATOR ───────────────────────────────
    # Fastest way to check if item exists
    print(f"\n   58 in list       : {58 in numbers}")
    print(f"   100 in list      : {100 in numbers}")

    # ─── INDEX METHOD ──────────────────────────────
    # Returns position of first occurrence
    if 58 in numbers:
        position = numbers.index(58)
        print(f"   index of 58      : {position}")

    # ─── LINEAR SEARCH ─────────────────────────────
    # Manual search through each element
    search_value = 69
    found        = False

    for index, value in enumerate(numbers):
        if value == search_value:
            print(f"\n   Linear search for {search_value}:")
            print(f"   Found at index   : {index}")
            found = True
            break

    if not found:
        print(f"   {search_value} not found in list")


def demonstrate_error_handling():
    """
    Demonstrate graceful handling of list errors.

    Parameters: None
    Returns: None
    """
    print(f"\n{THIN_LINE}")
    print("   ERROR HANDLING")
    print(THIN_LINE)

    numbers = [10, 20, 30, 40, 50]
    print(f"   List             : {numbers}")
    print(f"   Length           : {len(numbers)}")

    # ─── INDEX ERROR ───────────────────────────────
    # Accessing index that does not exist
    print(f"\n   Accessing index 10 (out of range):")
    try:
        value = numbers[10]
        print(f"   Value            : {value}")
    except IndexError as error:
        print(f"   IndexError caught: {error}")
        print(f"   Valid range      : 0 to {len(numbers) - 1}")

    # ─── NEGATIVE INDEX ERROR ──────────────────────
    print(f"\n   Accessing index -10 (out of range):")
    try:
        value = numbers[-10]
        print(f"   Value            : {value}")
    except IndexError as error:
        print(f"   IndexError caught: {error}")

    # ─── REMOVE NON EXISTENT VALUE ─────────────────
    print(f"\n   Removing value 999 (not in list):")
    try:
        numbers.remove(999)
    except ValueError as error:
        print(f"   ValueError caught: {error}")

    # ─── SAFE ACCESS FUNCTION ──────────────────────
    print(f"\n   Safe access with default value:")
    print(f"   Index 2  : {safe_get(numbers, 2)}")
    print(f"   Index 10 : {safe_get(numbers, 10, 'Not found')}")


def safe_get(lst, index, default=None):
    """
    Safely access list item without raising IndexError.

    Parameters:
        lst     (list): The list to access
        index   (int): Index to access
        default: Value to return if index not found

    Returns:
        Value at index or default if IndexError occurs
    """
    try:
        return lst[index]
    except IndexError:
        return default


def demonstrate_list_comprehension():
    """
    Demonstrate list comprehension for creating lists.

    Parameters: None
    Returns: None
    """
    print(f"\n{THIN_LINE}")
    print("   LIST COMPREHENSION")
    print(THIN_LINE)

    # ─── BASIC COMPREHENSION ───────────────────────
    # Create list of squares
    squares = [x ** 2 for x in range(1, 6)]
    print(f"   Squares 1-5      : {squares}")

    # ─── WITH CONDITION ────────────────────────────
    # Only even numbers
    evens = [x for x in range(1, 11) if x % 2 == 0]
    print(f"   Even numbers     : {evens}")

    # ─── STRING COMPREHENSION ──────────────────────
    names  = ["sehar", "ali", "sara", "ahmed"]
    upper  = [name.upper() for name in names]
    print(f"   Names upper      : {upper}")

    # ─── FILTER WITH CONDITION ─────────────────────
    marks  = [45, 78, 92, 38, 65, 88, 23, 71]
    passed = [m for m in marks if m >= 50]
    print(f"   All marks        : {marks}")
    print(f"   Passing marks    : {passed}")


def run_list_operations():
    """
    Main function to run all list operation demonstrations.

    Parameters: None
    Returns: None
    """
    print(f"\n{SEPARATOR}")
    print("   List Operations — Sorting, Searching, Errors")
    print("   Day 6 — Data Structures")
    print(SEPARATOR)

    demonstrate_sorting()
    demonstrate_searching()
    demonstrate_error_handling()
    demonstrate_list_comprehension()

    print(f"\n{SEPARATOR}")
    print("   All list operations demonstrated successfully.")
    print(SEPARATOR)


# ─── ENTRY POINT ───────────────────────────────────
if __name__ == "__main__":
    run_list_operations()