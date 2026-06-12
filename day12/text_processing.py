"""Text processing utilities with function chaining.

Day 12 - Functions Fundamentals (Task 2).

Demonstrates default parameters, function composition (chaining),
and returning multiple values via tuples.
"""

import re
import string


def count_words(text):
    """Count the number of words in a string.

    Args:
        text (str): The input text.

    Returns:
        int: Number of whitespace-separated words.

    Raises:
        TypeError: If `text` is not a string.

    Example:
        >>> count_words("hello world")
        2
    """
    if not isinstance(text, str):
        raise TypeError("Input must be a string.")
    return len(text.split())


def extract_emails(text):
    """Extract all email addresses from a string.

    Args:
        text (str): The input text to scan.

    Returns:
        list[str]: All email addresses found (empty if none).

    Raises:
        TypeError: If `text` is not a string.

    Example:
        >>> extract_emails("contact a@x.com or b@y.org")
        ['a@x.com', 'b@y.org']
    """
    if not isinstance(text, str):
        raise TypeError("Input must be a string.")
    pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    return re.findall(pattern, text)


def remove_punctuation(text):
    """Remove all punctuation characters from a string.

    Args:
        text (str): The input text.

    Returns:
        str: Text with punctuation removed.

    Raises:
        TypeError: If `text` is not a string.

    Example:
        >>> remove_punctuation("Hello, World!")
        'Hello World'
    """
    if not isinstance(text, str):
        raise TypeError("Input must be a string.")
    # str.translate with a table mapping punctuation to None.
    table = str.maketrans("", "", string.punctuation)
    return text.translate(table)


def title_case(text):
    """Convert a string to title case (each word capitalized).

    Args:
        text (str): The input text.

    Returns:
        str: Title-cased text.

    Raises:
        TypeError: If `text` is not a string.

    Example:
        >>> title_case("hello world")
        'Hello World'
    """
    if not isinstance(text, str):
        raise TypeError("Input must be a string.")
    return text.title()


def process_text(text, remove_punct=True, to_title=True):
    """Clean text and return summary statistics.

    Chains remove_punctuation() and title_case() based on the
    flags, then computes word/char/unique-word counts.

    Args:
        text (str): The input text.
        remove_punct (bool, optional): Strip punctuation if True.
            Defaults to True.
        to_title (bool, optional): Apply title case if True.
            Defaults to True.

    Returns:
        tuple: A 4-tuple of
            (processed_text, word_count, char_count,
             unique_words), where unique_words counts distinct
            lowercase words.

    Raises:
        TypeError: If `text` is not a string.

    Example:
        >>> process_text("hi, hi there!")
        ('Hi Hi There', 3, 11, 2)
    """
    if not isinstance(text, str):
        raise TypeError("Input must be a string.")
    processed = text
    if remove_punct:
        processed = remove_punctuation(processed)
    if to_title:
        processed = title_case(processed)
    word_count = count_words(processed)
    char_count = len(processed)
    unique_words = len({word.lower() for word in processed.split()})
    return processed, word_count, char_count, unique_words


def main():
    """Run a quick demonstration of the text utilities."""
    sample = "Hello, world! Email me at umar@xeven.com please."
    print("Emails:   ", extract_emails(sample))
    print("No punct: ", remove_punctuation(sample))

    result, words, chars, unique = process_text(sample)
    print("Processed:", result)
    print("Words:", words, "| Chars:", chars, "| Unique:", unique)


if __name__ == "__main__":
    main()