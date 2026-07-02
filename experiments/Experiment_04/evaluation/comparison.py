"""
Comparison utilities for Experiment 04.

This module evaluates FAISS and ChromaDB using identical retrieval
queries and returns a structured comparison of their performance.
"""

from langchain_core.retrievers import BaseRetriever

from config.settings import NUM_RETRIEVAL_RUNS
from evaluation.metrics import (
    count_retrieved_documents,
    measure_average_execution_time,
)
from retrieval.retriever import retrieve_documents


def evaluate_vectorstore(
    retriever: BaseRetriever,
    query: str,
) -> dict:
    """
    Evaluate a vector store retriever.

    Parameters
    ----------
    retriever : BaseRetriever
        Configured LangChain retriever.
    query : str
        Query used for retrieval.

    Returns
    -------
    dict
        Dictionary containing retrieval metrics.
    """
    retrieved_documents, retrieval_time = (
        measure_average_execution_time(
            retrieve_documents,
            NUM_RETRIEVAL_RUNS,
            retriever,
            query,
        )
    )

    return {
        "retrieval_time_seconds": retrieval_time,
        "retrieved_documents": count_retrieved_documents(
            retrieved_documents
        ),
        "documents": retrieved_documents,
    }


def compare_vectorstores(
    faiss_retriever: BaseRetriever,
    chroma_retriever: BaseRetriever,
    query: str,
    faiss_index_time: float,
    chroma_index_time: float,
) -> dict:
    """
    Compare FAISS and ChromaDB using the same query.

    Parameters
    ----------
    faiss_retriever : BaseRetriever
        FAISS retriever.
    chroma_retriever : BaseRetriever
        ChromaDB retriever.
    query : str
        Retrieval query.
    faiss_index_time : float
        FAISS index creation time.
    chroma_index_time : float
        ChromaDB index creation time.

    Returns
    -------
    dict
        Structured comparison results.
    """
    faiss_results = evaluate_vectorstore(
        faiss_retriever,
        query,
    )

    chroma_results = evaluate_vectorstore(
        chroma_retriever,
        query,
    )

    return {
        "FAISS": {
            "index_creation_time_seconds": faiss_index_time,
            **faiss_results,
        },
        "ChromaDB": {
            "index_creation_time_seconds": chroma_index_time,
            **chroma_results,
        },
    }