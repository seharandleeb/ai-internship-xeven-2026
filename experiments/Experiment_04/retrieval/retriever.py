"""
Document retrieval utilities for Experiment 04.

This module provides a common interface for retrieving documents from
any LangChain-compatible retriever. Using a shared retrieval function
ensures that FAISS and ChromaDB are evaluated under identical conditions.
"""

from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever


def retrieve_documents(
    retriever: BaseRetriever,
    query: str,
) -> list[Document]:
    """
    Retrieve the most relevant documents for a given query.

    Parameters
    ----------
    retriever : BaseRetriever
        Configured LangChain retriever.
    query : str
        User query.

    Returns
    -------
    list[Document]
        List of retrieved documents.
    """
    return retriever.invoke(query)