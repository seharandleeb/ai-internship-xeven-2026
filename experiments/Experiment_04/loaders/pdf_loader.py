"""
PDF document loader for Experiment 04.

This module provides functionality to load PDF documents using the
PyMuPDFLoader from LangChain. It returns the document contents as a list
of LangChain Document objects for downstream processing.
"""

from pathlib import Path

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_core.documents import Document


def load_pdf(pdf_path: str | Path) -> list[Document]:
    """
    Load a PDF document using PyMuPDF.

    Parameters
    ----------
    pdf_path : str | Path
        Path to the PDF document.

    Returns
    -------
    list[Document]
        List of LangChain Document objects.

    Raises
    ------
    FileNotFoundError
        If the specified PDF file does not exist.
    RuntimeError
        If an error occurs while loading the PDF.
    """
    pdf_path = Path(pdf_path)

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    try:
        loader = PyMuPDFLoader(str(pdf_path))
        documents = loader.load()
        return documents

    except Exception as exc:
        raise RuntimeError(
            f"Failed to load PDF '{pdf_path}': {exc}"
        ) from exc