"""
Similarity Search retrieval strategy for Experiment 05.

This module creates a retriever that performs standard semantic
similarity search on the ChromaDB vector store.
"""

from langchain_chroma import Chroma
from langchain_core.retrievers import BaseRetriever

from config.settings import TOP_K


def get_similarity_retriever(
    vectorstore: Chroma,
) -> BaseRetriever:
    """
    Create a Similarity Search retriever.

    Parameters
    ----------
    vectorstore : Chroma
        Initialized ChromaDB vector store.

    Returns
    -------
    BaseRetriever
        Retriever configured for similarity search.
    """
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": TOP_K,
        },
    )

    return retriever