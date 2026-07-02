"""
Comparison engine for Experiment 06.

This module compares:
1. MMR Retrieval (baseline)
2. MMR + Cross-Encoder Reranking

Both pipelines use the SAME retrieved documents to ensure
a fair comparison. The reranked pipeline only adds the
Cross-Encoder reranking step.
"""

from langchain_core.retrievers import BaseRetriever

from evaluation.metrics import (
    measure_execution_time,
    count_retrieved_documents,
    compute_unique_pages,
    compute_duplicate_chunks,
    compute_context_diversity,
)

from retrieval.retriever import retrieve_documents
from reranker.rerank import rerank_documents


def compare_retrieval_strategies(
    mmr_retriever: BaseRetriever,
    reranker,
    query: str,
    top_k: int,
) -> dict:
    """
    Compare baseline MMR retrieval against
    MMR + Cross-Encoder reranking.
    """

    # ---------------------------------------------------------
    # Retrieve ONCE
    # ---------------------------------------------------------

    retrieved_docs, retrieval_time = measure_execution_time(
        retrieve_documents,
        mmr_retriever,
        query,
    )

    # ---------------------------------------------------------
    # Baseline Metrics
    # ---------------------------------------------------------

    baseline_results = {
        "retrieval_time": retrieval_time,
        "retrieved_documents": count_retrieved_documents(retrieved_docs),
        "unique_pages": compute_unique_pages(retrieved_docs),
        "duplicate_chunks": compute_duplicate_chunks(retrieved_docs),
        "context_diversity": compute_context_diversity(retrieved_docs),
        "documents": retrieved_docs,
    }

    # ---------------------------------------------------------
    # Reranking
    # ---------------------------------------------------------

    reranked_docs, rerank_time = measure_execution_time(
        rerank_documents,
        query,
        retrieved_docs,
        reranker,
        top_k,
    )

    reranked_results = {
        "retrieval_time": retrieval_time,
        "rerank_time": rerank_time,
        "total_time": retrieval_time + rerank_time,
        "retrieved_documents": count_retrieved_documents(reranked_docs),
        "unique_pages": compute_unique_pages(reranked_docs),
        "duplicate_chunks": compute_duplicate_chunks(reranked_docs),
        "context_diversity": compute_context_diversity(reranked_docs),
        "documents": reranked_docs,
    }

    return {
        "MMR": baseline_results,
        "RERANKED": reranked_results,
    }