"""
PDF loading utilities for Experiment 05.

This module loads PDF documents using PyMuPDF, the PDF loader
selected in Experiment 01. Keeping the same loader ensures that
only the retrieval strategy changes during this experiment.
"""

from pathlib import Path

from langchain_core.documents import Document
from langchain_community.document_loaders import PyMuPDFLoader


def load_pdf(pdf_path: Path) -> list[Document]:
    """
    Load a PDF document using PyMuPDF.

    Parameters
    ----------
    pdf_path : Path
        Path to the PDF document.

    Returns
    -------
    list[Document]
        List of LangChain Document objects.
    """
    loader = PyMuPDFLoader(str(pdf_path))
    documents = loader.load()

    return documents