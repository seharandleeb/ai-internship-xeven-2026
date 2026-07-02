"""
Evaluation metrics for Experiment 04.

This module provides reusable utility functions for measuring the
performance of vector database operations. These metrics are used
to compare FAISS and ChromaDB under identical conditions.
"""

from time import perf_counter
from typing import Any, Callable
from statistics import mean

def measure_execution_time(
    func: Callable,
    *args: Any,
    **kwargs: Any,
) -> tuple[Any, float]:
    """
    Measure the execution time of a function.

    Parameters
    ----------
    func : Callable
        Function to execute.
    *args : Any
        Positional arguments for the function.
    **kwargs : Any
        Keyword arguments for the function.

    Returns
    -------
    tuple[Any, float]
        A tuple containing:
        - The function result.
        - Execution time in seconds.
    """
    start_time = perf_counter()

    result = func(*args, **kwargs)

    end_time = perf_counter()

    execution_time = end_time - start_time

    return result, execution_time

def measure_average_execution_time(
    func: Callable,
    runs: int,
    *args: Any,
    **kwargs: Any,
) -> tuple[Any, float]:
    """
    Measure the average execution time of a function over multiple runs.

    Parameters
    ----------
    func : Callable
        Function to execute.
    runs : int
        Number of benchmark runs.
    *args : Any
        Positional arguments.
    **kwargs : Any
        Keyword arguments.

    Returns
    -------
    tuple[Any, float]
        Function result from the final run and average execution time.
    """
    execution_times = []
    result = None

    for _ in range(runs):
        start_time = perf_counter()

        result = func(*args, **kwargs)

        end_time = perf_counter()

        execution_times.append(end_time - start_time)

    return result, mean(execution_times)

def count_retrieved_documents(documents: list) -> int:
    """
    Count the number of retrieved documents.

    Parameters
    ----------
    documents : list
        Retrieved documents.

    Returns
    -------
    int
        Number of retrieved documents.
    """
    return len(documents)