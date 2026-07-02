"""
Evaluation metrics for Experiment 06.

This module measures retrieval + reranking performance including:
- timing
- diversity
- duplicates
- basic quality indicators
"""

import time
from collections import Counter
from langchain_core.documents import Document


# -------------------------------------------------------------
# Timing Utility
# -------------------------------------------------------------
def measure_execution_time(func, *args, **kwargs):
    """
    Measure execution time of any function.
    """

    start = time.time()
    result = func(*args, **kwargs)
    end = time.time()

    return result, end - start


# -------------------------------------------------------------
# Document Analysis Metrics
# -------------------------------------------------------------
def count_retrieved_documents(documents: list[Document]) -> int:
    """
    Count number of retrieved documents.
    """
    return len(documents)


def compute_unique_pages(documents: list[Document]) -> int:
    """
    Count how many unique source pages are retrieved.
    """
    pages = []

    for doc in documents:
        if "page" in doc.metadata:
            pages.append(doc.metadata["page"])
        elif "source" in doc.metadata:
            pages.append(doc.metadata["source"])

    return len(set(pages))


def compute_duplicate_chunks(documents: list[Document]) -> int:
    """
    Estimate duplicate chunks based on repeated content.
    """
    contents = [doc.page_content.strip() for doc in documents]
    freq = Counter(contents)

    duplicates = sum(count - 1 for count in freq.values() if count > 1)
    return duplicates


def compute_context_diversity(documents: list[Document]) -> float:
    """
    Compute simple diversity score based on unique pages ratio.
    """

    if not documents:
        return 0.0

    unique_pages = compute_unique_pages(documents)
    total = len(documents)

    return round(unique_pages / total, 2)