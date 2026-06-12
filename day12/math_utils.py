"""Math utility library: average, median, standard deviation.

Day 12 - Functions Fundamentals (Task 1).

Demonstrates parameter validation, default parameters, and
comprehensive docstrings. All functions are pure (no side
effects) and follow the single-responsibility principle.
"""


def _validate_numbers(numbers):
    """Validate that input is a non-empty list/tuple of numbers.

    Args:
        numbers (list | tuple): The values to validate.

    Returns:
        None: Returns nothing if validation passes.

    Raises:
        TypeError: If `numbers` is not a list/tuple, or if any
            element is non-numeric (bool is rejected too).
        ValueError: If `numbers` is empty.
    """
    if not isinstance(numbers, (list, tuple)):
        raise TypeError("Input must be a list or tuple.")
    if len(numbers) == 0:
        raise ValueError("Input list must not be empty.")
    for value in numbers:
        # bool is a subclass of int, so reject it explicitly.
        if isinstance(value, bool) or not isinstance(
            value, (int, float)
        ):
            raise TypeError(f"Non-numeric value found: {value!r}")


def calculate_average(numbers, precision=2):
    """Calculate the arithmetic mean of a list of numbers.

    Args:
        numbers (list[float]): Non-empty list of numeric values.
        precision (int, optional): Decimal places to round to.
            Defaults to 2.

    Returns:
        float: The mean, rounded to `precision` decimals.

    Raises:
        ValueError: If `numbers` is empty.
        TypeError: If any element is non-numeric.

    Example:
        >>> calculate_average([10, 20, 30])
        20.0
    """
    _validate_numbers(numbers)
    mean = sum(numbers) / len(numbers)
    return round(mean, precision)


def find_median(numbers, precision=2):
    """Find the median (middle value) of a list of numbers.

    For an even count, returns the average of the two middle
    values.

    Args:
        numbers (list[float]): Non-empty list of numeric values.
        precision (int, optional): Decimal places to round to.
            Defaults to 2.

    Returns:
        float: The median, rounded to `precision` decimals.

    Raises:
        ValueError: If `numbers` is empty.
        TypeError: If any element is non-numeric.

    Example:
        >>> find_median([3, 1, 2])
        2.0
    """
    _validate_numbers(numbers)
    ordered = sorted(numbers)
    n = len(ordered)
    mid = n // 2
    if n % 2 == 1:                 # odd count -> single middle
        median = ordered[mid]
    else:                          # even count -> average of two
        median = (ordered[mid - 1] + ordered[mid]) / 2
    return round(median, precision)


def get_standard_deviation(numbers, precision=2, sample=True):
    """Calculate the standard deviation of a list of numbers.

    Args:
        numbers (list[float]): List of numeric values. Needs at
            least 2 values when `sample` is True.
        precision (int, optional): Decimal places to round to.
            Defaults to 2.
        sample (bool, optional): If True, use sample standard
            deviation (divide by n - 1). If False, use population
            standard deviation (divide by n). Defaults to True.

    Returns:
        float: The standard deviation, rounded to `precision`.

    Raises:
        ValueError: If `numbers` is empty, or has fewer than 2
            values while `sample` is True.
        TypeError: If any element is non-numeric.

    Example:
        >>> get_standard_deviation([2, 4, 4, 4, 5, 5, 7, 9],
        ...                        sample=False)
        2.0
    """
    _validate_numbers(numbers)
    n = len(numbers)
    if sample and n < 2:
        raise ValueError("Sample std dev needs at least 2 values.")
    mean = sum(numbers) / n
    squared_diffs = [(x - mean) ** 2 for x in numbers]
    divisor = (n - 1) if sample else n
    variance = sum(squared_diffs) / divisor
    std_dev = variance ** 0.5
    return round(std_dev, precision)


def main():
    """Run a quick demonstration of the math utilities."""
    data = [10, 20, 30, 40, 50]
    print("Average:", calculate_average(data))
    print("Median: ", find_median(data))
    print("Std Dev:", get_standard_deviation(data))
    print("Pop Std:", get_standard_deviation(data, sample=False))


if __name__ == "__main__":
    main()