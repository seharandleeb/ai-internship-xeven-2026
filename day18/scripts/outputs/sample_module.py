"""A tiny utility module used as a code-splitting sample."""


def greet(name):
    """Return a friendly greeting for the given name."""
    return "Hello, %s!" % name


def add(a, b):
    """Return the sum of two numbers."""
    return a + b


class Counter:
    """A minimal counter with increment and reset."""

    def __init__(self):
        self.value = 0

    def increment(self):
        """Add one to the current value."""
        self.value += 1
        return self.value

    def reset(self):
        """Reset the counter back to zero."""
        self.value = 0
