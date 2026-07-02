"""
Evaluation metrics for Experiment 05.

This module provides reusable utility functions for benchmarking
retrieval strategies and measuring retrieval quality.
"""

from time import perf_counter
from typing import Any, Callable

from langchain_core.documents import Document


def measure_execution_time(
    function: Callable,
    *args: Any,
    **kwargs: Any,
) -> tuple[Any, float]:
    """
    Measure the execution time of a function.

    Parameters
    ----------
    function : Callable
        Function to benchmark.

    Returns
    -------
    tuple[Any, float]
        Function output and execution time in seconds.
    """
    start_time = perf_counter()

    result = function(*args, **kwargs)

    end_time = perf_counter()

    execution_time = end_time - start_time

    return result, execution_time


def count_retrieved_documents(
    documents: list[Document],
) -> int:
    """
    Count the number of retrieved documents.

    Parameters
    ----------
    documents : list[Document]
        Retrieved LangChain documents.

    Returns
    -------
    int
        Number of retrieved documents.
    """
    return len(documents)


def count_unique_pages(
    documents: list[Document],
) -> int:
    """
    Count the number of unique PDF pages represented in the
    retrieved documents.

    Parameters
    ----------
    documents : list[Document]
        Retrieved LangChain documents.

    Returns
    -------
    int
        Number of unique pages.
    """
    pages = {
        document.metadata.get("page", -1)
        for document in documents
    }

    return len(pages)


def count_duplicate_chunks(
    documents: list[Document],
) -> int:
    """
    Count duplicate retrieved chunks.

    Parameters
    ----------
    documents : list[Document]
        Retrieved LangChain documents.

    Returns
    -------
    int
        Number of duplicate chunks.
    """
    contents = [
        document.page_content
        for document in documents
    ]

    return len(contents) - len(set(contents))


def calculate_context_diversity(
    documents: list[Document],
) -> float:
    """
    Calculate a simple context diversity score.

    Diversity Score =
    Unique Chunks / Retrieved Chunks

    Parameters
    ----------
    documents : list[Document]
        Retrieved LangChain documents.

    Returns
    -------
    float
        Context diversity score between 0 and 1.
    """
    if not documents:
        return 0.0

    unique_chunks = len(
        {
            document.page_content
            for document in documents
        }
    )

    return unique_chunks / len(documents)