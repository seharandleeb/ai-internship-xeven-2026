"""
Utility functions for printing Experiment 04 results.

This module contains helper functions for displaying the comparison
results between FAISS and ChromaDB in a clean and readable format.
"""

from config.settings import (
    EMBEDDING_MODEL_NAME,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    TOP_K,
    NUM_RETRIEVAL_RUNS,
)


def print_experiment_header() -> None:
    """
    Print the experiment title.
    """
    print("\n" + "=" * 70)
    print("EXPERIMENT 04: VECTOR DATABASE COMPARISON")
    print("FAISS vs ChromaDB")
    print("=" * 70)


def print_experiment_configuration(total_chunks: int) -> None:
    """
    Print the experiment configuration.

    Parameters
    ----------
    total_chunks : int
        Total number of document chunks generated.
    """
    print("\nExperiment Configuration")
    print("-" * 70)
    print(f"Embedding Model : {EMBEDDING_MODEL_NAME}")
    print(f"Chunk Size      : {CHUNK_SIZE}")
    print(f"Chunk Overlap   : {CHUNK_OVERLAP}")
    print(f"Top-K           : {TOP_K}")
    print(f"Benchmark Runs  : {NUM_RETRIEVAL_RUNS}")
    print(f"Total Chunks    : {total_chunks}")


def print_vectorstore_results(
    vectorstore_name: str,
    results: dict,
) -> None:
    """
    Print evaluation results for a single vector database.

    Parameters
    ----------
    vectorstore_name : str
        Name of the vector database.
    results : dict
        Evaluation metrics.
    """
    print(f"\n{vectorstore_name}")
    print("-" * 50)

    print(
        f"Index Creation Time      : "
        f"{results['index_creation_time_seconds']:.4f} seconds"
    )

    print(
        f"Average Retrieval Time   : "
        f"{results['retrieval_time_seconds']:.4f} seconds"
    )

    print(
        f"Retrieved Documents      : "
        f"{results['retrieved_documents']}"
    )


def print_engineering_decision(
    faiss_results: dict,
    chroma_results: dict,
) -> None:
    """
    Print an engineering decision based on experimental results.

    Parameters
    ----------
    faiss_results : dict
        FAISS evaluation metrics.
    chroma_results : dict
        ChromaDB evaluation metrics.
    """
    print("\n" + "=" * 70)
    print("ENGINEERING DECISION")
    print("=" * 70)

    indexing_winner = (
        "FAISS"
        if faiss_results["index_creation_time_seconds"]
        < chroma_results["index_creation_time_seconds"]
        else "ChromaDB"
    )

    retrieval_winner = (
        "FAISS"
        if faiss_results["retrieval_time_seconds"]
        < chroma_results["retrieval_time_seconds"]
        else "ChromaDB"
    )

    print(f"✓ Faster Index Creation   : {indexing_winner}")
    print(f"✓ Faster Retrieval        : {retrieval_winner}")

    print("\nProduction Considerations:")
    print("- FAISS: Excellent retrieval speed and lightweight deployment.")
    print("- ChromaDB: Built-in persistence and easier long-term management.")

    print(
        "\nFinal Recommendation:"
        "\nChoose the vector database based on your production "
        "requirements, considering indexing speed, average retrieval "
        "performance, persistence, scalability, and maintainability."
    )


def print_summary(
    results: dict,
    total_chunks: int,
) -> None:
    """
    Print the complete experiment summary.

    Parameters
    ----------
    results : dict
        Comparison results.
    total_chunks : int
        Total number of generated chunks.
    """
    print_experiment_header()

    print_experiment_configuration(total_chunks)

    print_vectorstore_results(
        "FAISS",
        results["FAISS"],
    )

    print_vectorstore_results(
        "ChromaDB",
        results["ChromaDB"],
    )

    print_engineering_decision(
        results["FAISS"],
        results["ChromaDB"],
    )

    print("\n" + "=" * 70)