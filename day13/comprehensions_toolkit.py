"""List and dictionary comprehension utilities.

Demonstrates advanced comprehension patterns: flattening a nested
list, transposing a matrix, inverting a dictionary, and building a
word-frequency counter with a dictionary comprehension.
"""


def flatten(nested):
    """Flatten one level of a nested list using a comprehension.

    Args:
        nested (list[list]): A list whose items are themselves lists.

    Returns:
        list: A single flat list containing all inner items.

    Example:
        >>> flatten([[1, 2], [3, 4]])
        [1, 2, 3, 4]
    """
    return [item for sublist in nested for item in sublist]


def transpose(matrix):
    """Transpose a rectangular matrix using a nested comprehension.

    Args:
        matrix (list[list]): A rectangular 2D list (equal row lengths).

    Returns:
        list[list]: The transposed matrix (rows become columns).

    Example:
        >>> transpose([[1, 2, 3], [4, 5, 6]])
        [[1, 4], [2, 5], [3, 6]]
    """
    return [[row[i] for row in matrix] for i in range(len(matrix[0]))]


def invert_dict(mapping):
    """Swap keys and values of a dict using a comprehension.

    Args:
        mapping (dict): Source dictionary with hashable values.

    Returns:
        dict: A new dict where each value maps back to its key.

    Example:
        >>> invert_dict({"a": 1, "b": 2})
        {1: 'a', 2: 'b'}
    """
    return {value: key for key, value in mapping.items()}


def word_frequency(text):
    """Count word occurrences using a dictionary comprehension.

    Args:
        text (str): Input text. Words are split on whitespace and
            compared case-insensitively.

    Returns:
        dict[str, int]: Mapping of each unique word to its count.

    Example:
        >>> word_frequency("a A b") == {"a": 2, "b": 1}
        True
    """
    words = text.lower().split()
    return {word: words.count(word) for word in set(words)}


def main():
    """Demonstrate each comprehension utility with sample data."""
    print("Flatten:  ", flatten([[1, 2], [3, 4], [5]]))
    print("Transpose:", transpose([[1, 2, 3], [4, 5, 6]]))
    print("Invert:   ", invert_dict({"a": 1, "b": 2}))
    print("Frequency:", word_frequency("the cat the dog the bird"))


if __name__ == "__main__":
    main()
