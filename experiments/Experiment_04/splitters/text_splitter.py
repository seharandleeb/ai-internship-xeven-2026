"""
Text splitter for Experiment 04.

This module provides functionality to split LangChain Document objects
into smaller chunks using the Recursive Character Text Splitter.
"""

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config.settings import CHUNK_SIZE, CHUNK_OVERLAP


def split_documents(documents: list[Document]) -> list[Document]:
    """
    Split documents into smaller chunks.

    Parameters
    ----------
    documents : list[Document]
        List of LangChain Document objects.

    Returns
    -------
    list[Document]
        List of chunked LangChain Document objects.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )

    chunks = text_splitter.split_documents(documents)

    return chunks