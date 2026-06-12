"""Data transformation suite using lambda, map, filter, and sorted.

Demonstrates anonymous (lambda) functions inside the three classic
higher-order helpers and benchmarks a lambda against a named function
and a list comprehension performing the same workload.
"""

import re
import time


# Reusable compiled patterns for the extraction filters.
EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
PHONE_RE = re.compile(r"\+?\d[\d\s-]{7,}\d")
URL_RE = re.compile(r"https?://\S+")


def clean_strings(raw_items):
    """Strip whitespace and uppercase strings using map + lambda.

    Args:
        raw_items (list[str]): Strings that may contain surrounding
            whitespace and mixed casing.

    Returns:
        list[str]: Cleaned, upper-cased strings.

    Example:
        >>> clean_strings(["  hi ", "bye"])
        ['HI', 'BYE']
    """
    return list(map(lambda s: s.strip().upper(), raw_items))


def extract_matches(text_items, pattern):
    """Keep only items matching a regex, using filter + lambda.

    Args:
        text_items (list[str]): Candidate strings to test.
        pattern (re.Pattern): A compiled regular expression.

    Returns:
        list[str]: Items containing at least one match.

    Example:
        >>> extract_matches(["a@b.com", "nope"], EMAIL_RE)
        ['a@b.com']
    """
    return list(filter(lambda item: pattern.search(item), text_items))


def sort_by_keys(records, keys):
    """Sort a list of dicts by multiple keys using sorted + lambda.

    Args:
        records (list[dict]): Rows to sort.
        keys (list[str]): Dictionary keys in priority order.

    Returns:
        list[dict]: A new, sorted list of records.

    Example:
        >>> rows = [{"age": 30, "name": "B"}, {"age": 30, "name": "A"}]
        >>> sort_by_keys(rows, ["age", "name"])[0]["name"]
        'A'
    """
    return sorted(records, key=lambda row: tuple(row[k] for k in keys))


def square_lambda(numbers):
    """Square each number using map + lambda (for benchmarking)."""
    return list(map(lambda n: n * n, numbers))


def square_named(numbers):
    """Square each number using a named function (for benchmarking)."""

    def square(value):
        return value * value

    return list(map(square, numbers))


def square_comprehension(numbers):
    """Square each number using a list comprehension (benchmarking)."""
    return [n * n for n in numbers]


def benchmark(func, data, repeats=5):
    """Time a function over several runs and return the fastest.

    Args:
        func (callable): Function taking the data as its only argument.
        data: Input passed to func on each repeat.
        repeats (int): Number of timed runs. Default 5.

    Returns:
        float: The fastest observed run time in seconds.
    """
    best = float("inf")
    for _ in range(repeats):
        start = time.perf_counter()
        func(data)
        best = min(best, time.perf_counter() - start)
    return best


def main():
    """Demonstrate each transformer and the performance comparison."""
    messy = ["  hello ", "World  ", " PyThOn"]
    print("Cleaned:", clean_strings(messy))

    blobs = ["mail me at a@b.com", "visit https://x.io", "plain text",
             "call +1 555 123 4567"]
    print("Emails:", extract_matches(blobs, EMAIL_RE))
    print("URLs:  ", extract_matches(blobs, URL_RE))
    print("Phones:", extract_matches(blobs, PHONE_RE))

    people = [
        {"name": "Ali", "age": 30},
        {"name": "Sara", "age": 25},
        {"name": "Bilal", "age": 30},
    ]
    print("Sorted:", sort_by_keys(people, ["age", "name"]))

    numbers = list(range(100_000))
    print("lambda + map:    %.5fs" % benchmark(square_lambda, numbers))
    print("named function:  %.5fs" % benchmark(square_named, numbers))
    print("comprehension:   %.5fs"
          % benchmark(square_comprehension, numbers))


if __name__ == "__main__":
    main()
