"""
Comparison utilities for Experiment 05.

This module evaluates Similarity Search and Maximal Marginal
Relevance (MMR) using the same query and returns a structured
comparison of their performance.
"""

from langchain_core.retrievers import BaseRetriever

from config.settings import BENCHMARK_RUNS
from evaluation.metrics import (
    calculate_context_diversity,
    count_duplicate_chunks,
    count_retrieved_documents,
    count_unique_pages,
    measure_execution_time,
)
from retrieval.retriever import retrieve_documents


def evaluate_retriever(
    retriever: BaseRetriever,
    query: str,
) -> dict:
    """
    Evaluate a retrieval strategy.

    Parameters
    ----------
    retriever : BaseRetriever
        Configured LangChain retriever.
    query : str
        Retrieval query.

    Returns
    -------
    dict
        Retrieval evaluation metrics.
    """
    retrieval_times = []

    retrieved_documents = []

    for _ in range(BENCHMARK_RUNS):

        retrieved_documents, retrieval_time = measure_execution_time(
            retrieve_documents,
            retriever,
            query,
        )

        retrieval_times.append(retrieval_time)

    average_time = sum(retrieval_times) / BENCHMARK_RUNS

    return {
        "average_retrieval_time_seconds": average_time,
        "retrieved_documents": count_retrieved_documents(
            retrieved_documents
        ),
        "unique_pages": count_unique_pages(
            retrieved_documents
        ),
        "duplicate_chunks": count_duplicate_chunks(
            retrieved_documents
        ),
        "context_diversity_score": calculate_context_diversity(
            retrieved_documents
        ),
        "documents": retrieved_documents,
    }


def compare_retrieval_strategies(
    similarity_retriever: BaseRetriever,
    mmr_retriever: BaseRetriever,
    query: str,
) -> dict:
    """
    Compare Similarity Search and MMR.

    Parameters
    ----------
    similarity_retriever : BaseRetriever
        Similarity Search retriever.
    mmr_retriever : BaseRetriever
        MMR retriever.
    query : str
        Query used for evaluation.

    Returns
    -------
    dict
        Structured comparison results.
    """
    similarity_results = evaluate_retriever(
        similarity_retriever,
        query,
    )

    mmr_results = evaluate_retriever(
        mmr_retriever,
        query,
    )

    return {
        "Similarity Search": similarity_results,
        "MMR": mmr_results,
    }