"""
Utility functions for saving Experiment 05 results.

This module writes the retrieval strategy comparison results
to a text file for documentation and future reference.
"""

from pathlib import Path


def save_results(
    results: dict,
    output_file: Path,
) -> None:
    """
    Save experiment results to a text file.

    Parameters
    ----------
    results : dict
        Comparison results.
    output_file : Path
        Output file path.
    """
    output_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(
        output_file,
        "w",
        encoding="utf-8",
    ) as file:

        file.write(
            "EXPERIMENT 05: RETRIEVAL STRATEGY COMPARISON\n"
        )
        file.write(
            "=" * 70 + "\n\n"
        )

        for strategy, metrics in results.items():

            file.write(f"{strategy}\n")
            file.write("-" * 50 + "\n")

            file.write(
                f"Average Retrieval Time : "
                f"{metrics['average_retrieval_time_seconds']:.4f} seconds\n"
            )

            file.write(
                f"Retrieved Documents    : "
                f"{metrics['retrieved_documents']}\n"
            )

            file.write(
                f"Unique Pages           : "
                f"{metrics['unique_pages']}\n"
            )

            file.write(
                f"Duplicate Chunks       : "
                f"{metrics['duplicate_chunks']}\n"
            )

            file.write(
                f"Context Diversity      : "
                f"{metrics['context_diversity_score']:.2f}\n"
            )

            file.write("\n")