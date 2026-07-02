"""
Maximal Marginal Relevance (MMR) retrieval strategy for Experiment 05.

This module creates a retriever that performs Maximal Marginal
Relevance (MMR) search on the ChromaDB vector store. MMR balances
semantic relevance with result diversity to reduce redundant
document retrieval.
"""

from langchain_chroma import Chroma
from langchain_core.retrievers import BaseRetriever

from config.settings import (
    TOP_K,
    MMR_FETCH_K,
    MMR_LAMBDA_MULT,
)


def get_mmr_retriever(
    vectorstore: Chroma,
) -> BaseRetriever:
    """
    Create an MMR retriever.

    Parameters
    ----------
    vectorstore : Chroma
        Initialized ChromaDB vector store.

    Returns
    -------
    BaseRetriever
        Retriever configured for Maximal Marginal Relevance (MMR).
    """
    retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": TOP_K,
            "fetch_k": MMR_FETCH_K,
            "lambda_mult": MMR_LAMBDA_MULT,
        },
    )

    return retriever