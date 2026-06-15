"""Day 18 - Task 3: Smart document processor.

Auto-detects a document's type (plain text, markdown, or Python code)
and applies the splitter that best preserves its structure:

  * .md   -> MarkdownHeaderTextSplitter (keeps section headers)
  * .py   -> PythonCodeTextSplitter (keeps def/class blocks together)
  * other -> RecursiveCharacterTextSplitter (paragraph/sentence aware)

Overlap is chosen by content: technical content (code/markdown) gets a
larger overlap so definitions and steps survive boundaries; narrative
text gets a smaller overlap. Each chunk carries rich metadata: source,
detected type, section, and an estimated token count.

The script auto-creates three sample files and its output folder, so it
runs end to end with no manual setup.

Run from inside day18/scripts/:
    python task3_smart_processor.py
"""

# Dependencies (install once, do NOT run pip inside a notebook):
#   uv pip install langchain-text-splitters

import json
import os

from langchain_text_splitters import (
    MarkdownHeaderTextSplitter,
    PythonCodeTextSplitter,
    RecursiveCharacterTextSplitter,
)

OUTPUT_DIR = "outputs"

# Overlap ratios tuned by content type. Technical content benefits from
# more redundancy at boundaries; narrative prose needs less.
TECHNICAL_OVERLAP = 0.18
NARRATIVE_OVERLAP = 0.08

# Llama-3 / MiniLM tokenizers average ~4 characters per English token.
# This is an estimate; an exact count needs the model tokenizer.
CHARS_PER_TOKEN = 4

MD_HEADERS = [
    ("#", "h1"),
    ("##", "h2"),
    ("###", "h3"),
]

SAMPLE_TXT = """Morning Routines That Actually Stick

Most advice about morning routines fails because it asks for too much
change at once. The trick is to anchor one tiny new habit to something
you already do without thinking. If you always make coffee, stretch
while it brews. The existing habit becomes the trigger for the new one.

Consistency beats intensity. A two-minute routine you keep every day
shapes your behaviour more than an hour-long routine you abandon after
a week. Start small enough that skipping feels harder than doing it.
"""

SAMPLE_MD = """# Project Setup Guide

Welcome to the project. This guide gets you running locally.

## Installation

Create a virtual environment and install the dependencies. The project
uses UV for fast, reproducible installs.

### Requirements

You need Python 3.12 and a Groq API key in a local .env file.

## Usage

Run the main script from the project root. Outputs are written to the
outputs folder, which is created automatically on first run.
"""

SAMPLE_PY = '''"""A tiny utility module used as a code-splitting sample."""


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
'''


def estimate_tokens(text):
    """Rough token estimate from character length."""
    return max(1, round(len(text) / CHARS_PER_TOKEN))


def detect_type(path, text):
    """Detect document type from extension first, then content."""
    lower = path.lower()
    if lower.endswith(".md"):
        return "markdown"
    if lower.endswith(".py"):
        return "code"
    stripped = text.lstrip()
    if stripped.startswith("#") or "\n## " in text:
        return "markdown"
    if "def " in text or "class " in text or "import " in text:
        return "code"
    return "text"


def split_markdown(text, source):
    """Split markdown on headers, keeping the section in metadata."""
    splitter = MarkdownHeaderTextSplitter(headers_to_split_on=MD_HEADERS)
    docs = splitter.split_text(text)
    overlap = int(400 * TECHNICAL_OVERLAP)
    sizer = RecursiveCharacterTextSplitter(chunk_size=400,
                                           chunk_overlap=overlap)
    results = []
    for doc in docs:
        section = " > ".join(
            doc.metadata[key] for key in ("h1", "h2", "h3")
            if key in doc.metadata)
        for piece in sizer.split_text(doc.page_content):
            results.append({
                "text": piece,
                "source": source,
                "type": "markdown",
                "section": section or "(root)",
                "est_tokens": estimate_tokens(piece),
            })
    return results


def split_code(text, source):
    """Split Python code, recording contained def/class names."""
    overlap = int(400 * TECHNICAL_OVERLAP)
    splitter = PythonCodeTextSplitter(chunk_size=400, chunk_overlap=overlap)
    results = []
    for piece in splitter.split_text(text):
        defs = []
        for line in piece.splitlines():
            stripped = line.strip()
            if stripped.startswith("def ") or stripped.startswith("class "):
                name = stripped.split("(")[0].replace(":", "").strip()
                defs.append(name)
        results.append({
            "text": piece,
            "source": source,
            "type": "code",
            "section": ", ".join(defs) if defs else "(module-level)",
            "est_tokens": estimate_tokens(piece),
        })
    return results


def split_text(text, source):
    """Split narrative prose with a smaller overlap."""
    overlap = int(400 * NARRATIVE_OVERLAP)
    splitter = RecursiveCharacterTextSplitter(chunk_size=400,
                                              chunk_overlap=overlap)
    results = []
    for piece in splitter.split_text(text):
        results.append({
            "text": piece,
            "source": source,
            "type": "text",
            "section": "(none)",
            "est_tokens": estimate_tokens(piece),
        })
    return results


def smart_split(path, text):
    """Detect type and dispatch to the right splitter."""
    doc_type = detect_type(path, text)
    if doc_type == "markdown":
        return split_markdown(text, os.path.basename(path))
    if doc_type == "code":
        return split_code(text, os.path.basename(path))
    return split_text(text, os.path.basename(path))


def build_samples():
    """Write the three sample files and return their paths."""
    samples = {
        os.path.join(OUTPUT_DIR, "sample_note.txt"): SAMPLE_TXT,
        os.path.join(OUTPUT_DIR, "sample_guide.md"): SAMPLE_MD,
        os.path.join(OUTPUT_DIR, "sample_module.py"): SAMPLE_PY,
    }
    paths = []
    for path, content in samples.items():
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(content)
        paths.append(path)
    return paths


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    paths = build_samples()

    all_chunks = []
    for path in paths:
        with open(path, "r", encoding="utf-8") as handle:
            text = handle.read()
        chunks = smart_split(path, text)
        all_chunks.extend(chunks)
        print("%-18s -> %-9s -> %d chunks" % (
            os.path.basename(path),
            detect_type(path, text),
            len(chunks)))

    print("\nSample chunk metadata:")
    for chunk in all_chunks[:6]:
        preview = chunk["text"].replace("\n", " ")[:46]
        print("  [%s] section=%-22s tokens=%-3d | %s..." % (
            chunk["type"], chunk["section"][:22],
            chunk["est_tokens"], preview))

    out_path = os.path.join(OUTPUT_DIR, "task3_smart_chunks.json")
    with open(out_path, "w", encoding="utf-8") as handle:
        json.dump(all_chunks, handle, indent=2, ensure_ascii=False)
    print("\nTotal chunks: %d" % len(all_chunks))
    print("Saved chunks -> %s" % out_path)


if __name__ == "__main__":
    main()
