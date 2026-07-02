"""
Text splitting utilities for Experiment 05.

This module splits loaded documents into smaller chunks using the
Recursive Character Text Splitter selected in Experiment 02.
Keeping the chunking strategy unchanged ensures a fair comparison
between retrieval strategies.
"""

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config.settings import (
    CHUNK_OVERLAP,
    CHUNK_SIZE,
)


def split_documents(
    documents: list[Document],
) -> list[Document]:
    """
    Split documents into overlapping chunks.

    Parameters
    ----------
    documents : list[Document]
        List of loaded LangChain documents.

    Returns
    -------
    list[Document]
        List of chunked LangChain documents.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )

    chunks = text_splitter.split_documents(documents)

    return chunks