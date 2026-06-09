"""
Script Purpose: Python Lists — Basics and Operations
Author: Sehar Andleeb
Company: Xeven Solutions
Day: 6 of 30

This script demonstrates Python list creation, indexing,
slicing, and all basic list methods with clear examples.
"""


# ─── CONSTANTS ─────────────────────────────────────
SEPARATOR = "=" * 55
THIN_LINE = "-" * 55


def demonstrate_list_creation():
    """
    Demonstrate different ways to create lists.

    Parameters: None
    Returns: None
    """
    print(f"\n{THIN_LINE}")
    print("   LIST CREATION")
    print(THIN_LINE)

    # ─── EMPTY LIST ────────────────────────────────
    empty_list = []
    print(f"   Empty list       : {empty_list}")

    # ─── INTEGER LIST ──────────────────────────────
    numbers = [1, 2, 3, 4, 5]
    print(f"   Integer list     : {numbers}")

    # ─── STRING LIST ───────────────────────────────
    fruits = ["apple", "banana", "cherry", "mango"]
    print(f"   String list      : {fruits}")

    # ─── MIXED DATA TYPES ──────────────────────────
    # Lists can hold any combination of data types
    mixed_list = [1, "hello", 3.14, True, None]
    print(f"   Mixed list       : {mixed_list}")

    # ─── NESTED LIST ───────────────────────────────
    nested_list = [[1, 2], [3, 4], [5, 6]]
    print(f"   Nested list      : {nested_list}")

    # ─── LIST LENGTH ───────────────────────────────
    print(f"\n   Length of fruits : {len(fruits)}")


def demonstrate_indexing():
    """
    Demonstrate positive and negative indexing in lists.

    Parameters: None
    Returns: None
    """
    print(f"\n{THIN_LINE}")
    print("   INDEXING")
    print(THIN_LINE)

    fruits = ["apple", "banana", "cherry", "mango", "orange"]

    print(f"   List             : {fruits}")
    print(f"\n   Positive Indexing:")

    # ─── POSITIVE INDEXING ─────────────────────────
    # Index starts from 0 at the beginning
    print(f"   fruits[0]        : {fruits[0]}")
    print(f"   fruits[1]        : {fruits[1]}")
    print(f"   fruits[4]        : {fruits[4]}")

    print(f"\n   Negative Indexing:")

    # ─── NEGATIVE INDEXING ─────────────────────────
    # Index starts from -1 at the end
    print(f"   fruits[-1]       : {fruits[-1]}")
    print(f"   fruits[-2]       : {fruits[-2]}")
    print(f"   fruits[-5]       : {fruits[-5]}")


def demonstrate_slicing():
    """
    Demonstrate list slicing with different patterns.

    Parameters: None
    Returns: None
    """
    print(f"\n{THIN_LINE}")
    print("   SLICING")
    print(THIN_LINE)

    numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    print(f"   List             : {numbers}")

    # ─── BASIC SLICING ─────────────────────────────
    # list[start:end] — end is not included
    print(f"\n   Basic Slicing:")
    print(f"   numbers[2:5]     : {numbers[2:5]}")
    print(f"   numbers[:4]      : {numbers[:4]}")
    print(f"   numbers[6:]      : {numbers[6:]}")
    print(f"   numbers[:]       : {numbers[:]}")

    # ─── STEP SLICING ──────────────────────────────
    # list[start:end:step]
    print(f"\n   Step Slicing:")
    print(f"   numbers[::2]     : {numbers[::2]}")
    print(f"   numbers[1::2]    : {numbers[1::2]}")
    print(f"   numbers[::-1]    : {numbers[::-1]}")
    print(f"   numbers[0:8:3]   : {numbers[0:8:3]}")


def demonstrate_adding_items():
    """
    Demonstrate append, insert, and extend methods.

    Parameters: None
    Returns: None
    """
    print(f"\n{THIN_LINE}")
    print("   ADDING ITEMS")
    print(THIN_LINE)

    fruits = ["apple", "banana", "cherry"]
    print(f"   Original list    : {fruits}")

    # ─── APPEND ────────────────────────────────────
    # Adds single item at the end
    fruits.append("mango")
    print(f"\n   After append()   : {fruits}")

    # ─── INSERT ────────────────────────────────────
    # Adds item at specific position
    fruits.insert(1, "orange")
    print(f"   After insert()   : {fruits}")

    # ─── EXTEND ────────────────────────────────────
    # Adds multiple items from another list
    fruits.extend(["grape", "kiwi"])
    print(f"   After extend()   : {fruits}")


def demonstrate_removing_items():
    """
    Demonstrate remove, pop, and clear methods.

    Parameters: None
    Returns: None
    """
    print(f"\n{THIN_LINE}")
    print("   REMOVING ITEMS")
    print(THIN_LINE)

    fruits = ["apple", "banana", "cherry", "mango", "banana"]
    print(f"   Original list    : {fruits}")

    # ─── REMOVE ────────────────────────────────────
    # Removes first occurrence of the value
    fruits.remove("banana")
    print(f"\n   After remove()   : {fruits}")

    # ─── POP ───────────────────────────────────────
    # Removes and returns item at index
    popped_item = fruits.pop()
    print(f"   After pop()      : {fruits}")
    print(f"   Popped item      : {popped_item}")

    popped_item = fruits.pop(0)
    print(f"   After pop(0)     : {fruits}")
    print(f"   Popped item      : {popped_item}")

    # ─── CLEAR ─────────────────────────────────────
    # Removes all items from list
    fruits.clear()
    print(f"   After clear()    : {fruits}")


def demonstrate_list_methods():
    """
    Demonstrate sort, reverse, count, and index methods.

    Parameters: None
    Returns: None
    """
    print(f"\n{THIN_LINE}")
    print("   LIST METHODS")
    print(THIN_LINE)

    numbers = [5, 2, 8, 1, 9, 3, 7, 4, 6, 2, 2]
    print(f"   Original list    : {numbers}")

    # ─── COUNT ─────────────────────────────────────
    # Counts occurrences of a value
    count = numbers.count(2)
    print(f"\n   count(2)         : {count}")

    # ─── INDEX ─────────────────────────────────────
    # Returns index of first occurrence
    index = numbers.index(9)
    print(f"   index(9)         : {index}")

    # ─── SORT ──────────────────────────────────────
    # Sorts list in place — ascending by default
    numbers.sort()
    print(f"\n   After sort()     : {numbers}")

    # ─── SORT DESCENDING ───────────────────────────
    numbers.sort(reverse=True)
    print(f"   Sort descending  : {numbers}")

    # ─── REVERSE ───────────────────────────────────
    # Reverses list in place
    numbers.reverse()
    print(f"   After reverse()  : {numbers}")


def run_list_basics():
    """
    Main function to run all list demonstrations.

    Parameters: None
    Returns: None
    """
    print(f"\n{SEPARATOR}")
    print("   Python Lists — Basics and Operations")
    print("   Day 6 — Data Structures")
    print(SEPARATOR)

    demonstrate_list_creation()
    demonstrate_indexing()
    demonstrate_slicing()
    demonstrate_adding_items()
    demonstrate_removing_items()
    demonstrate_list_methods()

    print(f"\n{SEPARATOR}")
    print("   All list operations demonstrated successfully.")
    print(SEPARATOR)


# ─── ENTRY POINT ───────────────────────────────────
if __name__ == "__main__":
    run_list_basics()