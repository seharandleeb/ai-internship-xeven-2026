"""Day 16 - Task 2: LangChain document loaders.

Demonstrates the four core loaders and a generic dispatcher that picks the
right loader from a file extension:

* ``TextLoader``  -> .txt
* ``PyPDFLoader`` -> .pdf  (multi-page aware)
* ``CSVLoader``   -> .csv  (one Document per row)
* ``WebBaseLoader`` -> http(s) URLs

All sample files (.txt, .csv, .pdf) are auto-created inside this script so it
runs with no external setup. Every loader returns a list of LangChain
``Document`` objects, each exposing ``page_content`` and ``metadata``.
"""

import os

# Identify our requests to websites (silences WebBaseLoader's USER_AGENT warning).
os.environ.setdefault("USER_AGENT", "xeven-day16-loader/1.0")

from langchain_community.document_loaders import (  # noqa: E402
    CSVLoader,
    PyPDFLoader,
    TextLoader,
    WebBaseLoader,
)
from langchain_core.documents import Document  # noqa: E402

SAMPLE_DIR = "samples"
SAMPLE_TXT = os.path.join(SAMPLE_DIR, "sample.txt")
SAMPLE_CSV = os.path.join(SAMPLE_DIR, "sample.csv")
SAMPLE_PDF = os.path.join(SAMPLE_DIR, "sample.pdf")


def create_sample_files() -> None:
    """Auto-create the .txt, .csv and .pdf sample files used below."""
    os.makedirs(SAMPLE_DIR, exist_ok=True)

    with open(SAMPLE_TXT, "w", encoding="utf-8") as handle:
        handle.write(
            "LangChain is a framework for building applications powered by "
            "large language models.\n"
            "It abstracts away raw API complexity behind reusable components: "
            "models, prompts, chains and memory.\n"
            "Document loaders turn many file formats into a standard Document "
            "object so the rest of the pipeline stays format-agnostic.\n"
        )

    with open(SAMPLE_CSV, "w", encoding="utf-8", newline="") as handle:
        handle.write("component,role\n")
        handle.write("Model,Wraps an LLM behind a common interface\n")
        handle.write("Prompt,Templates the text sent to the model\n")
        handle.write("Chain,Composes steps into a workflow with LCEL\n")
        handle.write("Memory,Persists state across turns\n")

    _create_sample_pdf()


def _create_sample_pdf() -> None:
    """Create a small two-page PDF with fpdf2 for the PDF loader demo."""
    from fpdf import FPDF

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Helvetica", size=12)

    pdf.add_page()
    pdf.multi_cell(
        0,
        10,
        "Day 16 - Sample PDF, Page 1\n\n"
        "LangChain document loaders read PDFs page by page. PyPDFLoader "
        "returns one Document per page, with the page number stored in "
        "metadata.",
    )

    pdf.add_page()
    pdf.multi_cell(
        0,
        10,
        "Day 16 - Sample PDF, Page 2\n\n"
        "Because every loader emits the same Document shape, a Q&A chain can "
        "consume text, PDF, CSV or web content without changing its logic.",
    )

    pdf.output(SAMPLE_PDF)


def load_text(path: str) -> list[Document]:
    """Load a plain-text file into Documents."""
    return TextLoader(path, encoding="utf-8").load()


def load_pdf(path: str) -> list[Document]:
    """Load a (possibly multi-page) PDF into one Document per page."""
    return PyPDFLoader(path).load()


def load_csv(path: str) -> list[Document]:
    """Load a CSV into one Document per row."""
    return CSVLoader(file_path=path).load()


def load_web(url: str) -> list[Document]:
    """Load and clean a webpage into Documents."""
    return WebBaseLoader(url).load()


def load_any(source: str) -> list[Document]:
    """Generic loader: detect the source type and dispatch.

    Args:
        source: A URL or a path ending in .txt / .pdf / .csv.

    Returns:
        A list of ``Document`` objects.

    Raises:
        ValueError: If the source type is not supported.
    """
    lowered = source.lower()
    if lowered.startswith(("http://", "https://")):
        return load_web(source)
    if lowered.endswith(".txt"):
        return load_text(source)
    if lowered.endswith(".pdf"):
        return load_pdf(source)
    if lowered.endswith(".csv"):
        return load_csv(source)
    raise ValueError(f"Unsupported source type: {source}")


def describe(docs: list[Document], label: str) -> None:
    """Print a short structural summary of loaded Documents."""
    print(f"[{label}] {len(docs)} document(s)")
    if docs:
        first = docs[0]
        preview = first.page_content.strip().replace("\n", " ")[:90]
        print(f"   page_content[:90]: {preview}")
        print(f"   metadata: {first.metadata}")
    print()


def main() -> None:
    """Create samples and exercise every loader (no API key required)."""
    print("=== Task 2: Document Loaders ===\n")
    create_sample_files()

    describe(load_any(SAMPLE_TXT), "TextLoader")
    describe(load_any(SAMPLE_CSV), "CSVLoader")
    describe(load_any(SAMPLE_PDF), "PyPDFLoader")

    print("WebBaseLoader is available via load_any('https://...').")
    print("Skipped live fetch here to keep the script offline-friendly.")


if __name__ == "__main__":
    main()
