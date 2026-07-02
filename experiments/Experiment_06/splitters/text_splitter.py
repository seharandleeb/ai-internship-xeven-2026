"""
Text splitting utilities for Experiment 06.

We use recursive character splitting to ensure:
- consistent chunk sizes
- good semantic boundaries
- compatibility with embedding models
"""

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from config.settings import CHUNK_SIZE, CHUNK_OVERLAP


def split_documents(documents: list[Document]) -> list[Document]:
    """
    Split documents into smaller chunks for embedding.

    Parameters
    ----------
    documents : list[Document]
        Raw documents from PDF loader.

    Returns
    -------
    list[Document]
        Chunked documents ready for embedding.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )

    chunks = splitter.split_documents(documents)

    if not chunks:
        raise ValueError("No chunks created from documents.")

    return chunks