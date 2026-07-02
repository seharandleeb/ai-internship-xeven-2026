"""
Document retrieval utilities for Experiment 05.

This module provides a common interface for retrieving documents
using any LangChain-compatible retriever. A shared retrieval
function ensures that Similarity Search and Maximal Marginal
Relevance (MMR) are evaluated under identical conditions.
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
        List of retrieved LangChain documents.
    """
    return retriever.invoke(query)