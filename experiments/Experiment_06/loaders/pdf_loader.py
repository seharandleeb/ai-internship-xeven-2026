"""
PDF loader for Experiment 06.

Loads PDF documents and converts them into LangChain Documents
for downstream chunking and embedding.
"""

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_core.documents import Document


def load_pdf(pdf_path: str) -> list[Document]:
    """
    Load PDF file and return list of documents.

    Parameters
    ----------
    pdf_path : str
        Path to PDF file.

    Returns
    -------
    list[Document]
        Extracted documents from PDF.
    """

    loader = PyMuPDFLoader(pdf_path)
    documents = loader.load()

    if not documents:
        raise ValueError("No content extracted from PDF.")

    return documents