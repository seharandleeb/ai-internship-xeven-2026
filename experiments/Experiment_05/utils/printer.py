"""
Utility functions for printing Experiment 05 results.

This module formats and displays the comparison results between
Similarity Search and Maximal Marginal Relevance (MMR).
"""

from config.settings import (
    BENCHMARK_RUNS,
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    EMBEDDING_MODEL_NAME,
    TOP_K,
)


def print_experiment_header() -> None:
    """Print the experiment header."""
    print("\n" + "=" * 70)
    print("EXPERIMENT 05: RETRIEVAL STRATEGY COMPARISON")
    print("Similarity Search vs Maximal Marginal Relevance (MMR)")
    print("=" * 70)


def print_experiment_configuration(
    total_chunks: int,
) -> None:
    """
    Print experiment configuration.
    """
    print("\nExperiment Configuration")
    print("-" * 70)
    print(f"Embedding Model : {EMBEDDING_MODEL_NAME}")
    print(f"Chunk Size      : {CHUNK_SIZE}")
    print(f"Chunk Overlap   : {CHUNK_OVERLAP}")
    print(f"Top-K           : {TOP_K}")
    print(f"Benchmark Runs  : {BENCHMARK_RUNS}")
    print(f"Total Chunks    : {total_chunks}")


def print_retrieval_results(
    strategy_name: str,
    results: dict,
) -> None:
    """
    Print retrieval metrics for one strategy.
    """
    print(f"\n{strategy_name}")
    print("-" * 50)

    print(
        f"Average Retrieval Time : "
        f"{results['average_retrieval_time_seconds']:.4f} seconds"
    )

    print(
        f"Retrieved Documents    : "
        f"{results['retrieved_documents']}"
    )

    print(
        f"Unique Pages           : "
        f"{results['unique_pages']}"
    )

    print(
        f"Duplicate Chunks       : "
        f"{results['duplicate_chunks']}"
    )

    print(
        f"Context Diversity      : "
        f"{results['context_diversity_score']:.2f}"
    )


def print_retrieved_documents(
    strategy_name: str,
    documents: list,
    preview_length: int = 250,
) -> None:
    """
    Print retrieved documents for qualitative comparison.

    Parameters
    ----------
    strategy_name : str
        Retrieval strategy name.

    documents : list
        Retrieved LangChain documents.

    preview_length : int
        Maximum preview length.
    """
    print("\n" + "=" * 70)
    print(f"{strategy_name.upper()} - RETRIEVED DOCUMENTS")
    print("=" * 70)

    for index, document in enumerate(documents, start=1):

        page = document.metadata.get("page", "Unknown")

        preview = (
            document.page_content
            .replace("\n", " ")
            .strip()
        )

        if len(preview) > preview_length:
            preview = preview[:preview_length] + "..."

        print(f"\nResult {index}")
        print("-" * 50)
        print(f"Page: {page}\n")
        print(preview)


def _select_winner(
    similarity_value: float,
    mmr_value: float,
    higher_is_better: bool,
) -> str:
    """
    Determine the winner between Similarity Search and MMR.
    """
    if similarity_value == mmr_value:
        return "Tie"

    if higher_is_better:
        return (
            "Similarity Search"
            if similarity_value > mmr_value
            else "MMR"
        )

    return (
        "Similarity Search"
        if similarity_value < mmr_value
        else "MMR"
    )


def print_engineering_decision(
    similarity_results: dict,
    mmr_results: dict,
) -> None:
    """
    Print engineering decision.
    """
    print("\n" + "=" * 70)
    print("ENGINEERING DECISION")
    print("=" * 70)

    speed_winner = _select_winner(
        similarity_results["average_retrieval_time_seconds"],
        mmr_results["average_retrieval_time_seconds"],
        higher_is_better=False,
    )

    diversity_winner = _select_winner(
        similarity_results["context_diversity_score"],
        mmr_results["context_diversity_score"],
        higher_is_better=True,
    )

    duplicate_winner = _select_winner(
        similarity_results["duplicate_chunks"],
        mmr_results["duplicate_chunks"],
        higher_is_better=False,
    )

    print(f"✓ Faster Retrieval     : {speed_winner}")
    print(f"✓ Better Diversity     : {diversity_winner}")
    print(f"✓ Fewer Duplicates     : {duplicate_winner}")

    print("\nProduction Considerations:")
    print("- Similarity Search: Faster and computationally efficient.")
    print("- MMR: Produces more diverse context while reducing redundant retrieval.")

    print("\nFinal Recommendation:")
    print(
        "Choose Similarity Search when retrieval speed is the "
        "highest priority. Choose MMR when response quality "
        "benefits from more diverse contextual information."
    )


def print_summary(
    results: dict,
    total_chunks: int,
) -> None:
    """
    Print complete experiment summary.
    """
    print_experiment_header()

    print_experiment_configuration(
        total_chunks,
    )

    print_retrieval_results(
        "Similarity Search",
        results["Similarity Search"],
    )

    print_retrieval_results(
        "MMR",
        results["MMR"],
    )

    print_engineering_decision(
        results["Similarity Search"],
        results["MMR"],
    )

    print_retrieved_documents(
        "Similarity Search",
        results["Similarity Search"]["documents"],
    )

    print_retrieved_documents(
        "MMR",
        results["MMR"]["documents"],
    )

    print("\n" + "=" * 70)