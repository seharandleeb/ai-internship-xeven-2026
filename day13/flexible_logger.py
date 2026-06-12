"""Flexible logging utility built with *args and **kwargs.

This module demonstrates variable positional arguments (*args) and
variable keyword arguments (**kwargs) by implementing a small logger
that accepts any number of message fragments and a flexible set of
formatting options (timestamp, file output, and text/JSON format).
"""

import json
from datetime import datetime


# ANSI color codes used to tint terminal output by severity level.
COLORS = {
    "ERROR": "\033[91m",    # red
    "WARNING": "\033[93m",  # yellow
    "INFO": "\033[0m",      # normal / default
}
RESET = "\033[0m"


def log(level, *messages, **options):
    """Log one or more messages with flexible formatting options.

    Joins every positional message fragment into a single line and
    formats it according to the keyword options provided. This shows
    how *args collects an arbitrary number of messages while **kwargs
    collects optional, named settings.

    Args:
        level (str): Severity label, e.g. "ERROR", "WARNING", "INFO".
        *messages: Any number of message fragments. They are joined
            with a single space to form the final message text.
        **options: Optional settings:
            timestamp (bool): Prepend an ISO timestamp. Default False.
            file (str): If given, append the line to this file path.
            format (str): "text" (default) or "json".

    Returns:
        str: The fully formatted log line (without color codes).

    Raises:
        ValueError: If an unsupported format option is supplied.

    Example:
        >>> log("INFO", "server", "started")
        'INFO: server started'
    """
    # Pull optional settings out of **options with safe defaults.
    use_timestamp = options.get("timestamp", False)
    file_path = options.get("file", None)
    output_format = options.get("format", "text")

    # Join all positional *messages into one text body.
    text = " ".join(str(part) for part in messages)
    stamp = datetime.now().isoformat(timespec="seconds")

    # Build a structured record once; reuse for both output formats.
    record = {"level": level, "message": text}
    if use_timestamp:
        record["timestamp"] = stamp

    if output_format == "json":
        line = json.dumps(record)
    elif output_format == "text":
        prefix = f"[{stamp}] " if use_timestamp else ""
        line = f"{prefix}{level}: {text}"
    else:
        raise ValueError(f"Unsupported format: {output_format!r}")

    # Tint the on-screen output based on the severity level.
    color = COLORS.get(level, "")
    print(f"{color}{line}{RESET}")

    # Persist to a file when a path is supplied via **options.
    if file_path:
        with open(file_path, "a", encoding="utf-8") as handle:
            handle.write(line + "\n")

    return line


def main():
    """Demonstrate the logger with varied arguments and options."""
    log("INFO", "Application", "started", timestamp=True)
    log("WARNING", "Disk", "space", "low", timestamp=True)
    log("ERROR", "Database connection failed", format="json",
        timestamp=True)
    log("INFO", "This line is also written to a file",
        file="day13_demo.log")


if __name__ == "__main__":
    main()
