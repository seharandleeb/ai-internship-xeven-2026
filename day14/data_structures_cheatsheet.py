"""Week 2 data-structures cheat sheet and live demonstrations.

Provides small demo functions for Python's four core built-in data
structures (list, tuple, set, dict) and prints a side-by-side summary
of their properties so they can be compared at a glance.
"""


def demo_list():
    """Demonstrate a list: ordered, mutable, allows duplicates.

    Returns:
        list: A sample list after an in-place mutation.

    Example:
        >>> demo_list()
        [1, 2, 2, 3, 99]
    """
    items = [1, 2, 2, 3]      # ordered, duplicates allowed
    items.append(99)          # mutable: grows in place
    return items


def demo_tuple():
    """Demonstrate a tuple: ordered, immutable, hashable.

    Returns:
        tuple: A fixed coordinate record.

    Example:
        >>> demo_tuple()
        (24.86, 67.0)
    """
    point = (24.86, 67.0)     # immutable: safe as a fixed record
    return point


def demo_set():
    """Demonstrate a set: unordered, unique, fast membership.

    Returns:
        set: The union of two sample tag sets.

    Example:
        >>> sorted(demo_set())
        ['ai', 'ml', 'python']
    """
    tags_a = {"python", "ai"}
    tags_b = {"ai", "ml"}     # duplicates collapse automatically
    return tags_a | tags_b    # set union operation


def demo_dict():
    """Demonstrate a dict: key-value map with fast lookup by key.

    Returns:
        dict: A sample contact record.

    Example:
        >>> demo_dict()["name"]
        'Sara'
    """
    contact = {"name": "Sara", "phone": "0300-1234567"}
    contact["email"] = "sara@example.com"   # mutable mapping
    return contact


def print_comparison():
    """Print a compact comparison of the four data structures."""
    rows = [
        ("Structure", "Ordered", "Mutable", "Duplicates"),
        ("List", "Yes", "Yes", "Yes"),
        ("Tuple", "Yes", "No", "Yes"),
        ("Set", "No", "Yes", "No"),
        ("Dict", "Yes*", "Yes", "Keys: No"),
    ]
    for cols in rows:
        print("{:<11}{:<10}{:<10}{:<12}".format(*cols))
    print("* dict preserves insertion order since Python 3.7")


def main():
    """Run every demo and print the comparison table."""
    print("List :", demo_list())
    print("Tuple:", demo_tuple())
    print("Set  :", demo_set())
    print("Dict :", demo_dict())
    print()
    print_comparison()


if __name__ == "__main__":
    main()
