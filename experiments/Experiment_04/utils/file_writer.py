"""
Utility functions for saving Experiment 04 results.

This module provides functionality to save the comparison
results to a text file for future reference.
"""

from pathlib import Path


def save_results(
    results: dict,
    output_file: str | Path,
) -> None:
    """
    Save experiment results to a text file.

    Parameters
    ----------
    results : dict
        Comparison results.
    output_file : str | Path
        Output file path.
    """
    output_file = Path(output_file)

    output_file.parent.mkdir(parents=True, exist_ok=True)

    with output_file.open("w", encoding="utf-8") as file:
        file.write("=" * 70 + "\n")
        file.write("EXPERIMENT 04: VECTOR DATABASE COMPARISON\n")
        file.write("=" * 70 + "\n\n")

        for vectorstore_name, metrics in results.items():
            file.write(f"{vectorstore_name}\n")
            file.write("-" * 50 + "\n")

            file.write(
                f"Index Creation Time : "
                f"{metrics['index_creation_time_seconds']:.4f} seconds\n"
            )

            file.write(
                f"Retrieval Time      : "
                f"{metrics['retrieval_time_seconds']:.4f} seconds\n"
            )

            file.write(
                f"Retrieved Documents : "
                f"{metrics['retrieved_documents']}\n\n"
            )