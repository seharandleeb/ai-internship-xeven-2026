"""
File writing utilities for Experiment 06.

Saves experiment results to a text file for documentation
and future reference.
"""

from pathlib import Path


def _write_documents(file, title: str, documents: list) -> None:
    """
    Write retrieved document previews.
    """

    file.write("\n" + "=" * 70 + "\n")
    file.write(title + "\n")
    file.write("=" * 70 + "\n")

    for index, document in enumerate(documents, start=1):

        page = document.metadata.get("page", "Unknown")

        preview = document.page_content.replace("\n", " ")
        preview = " ".join(preview.split())
        preview = preview[:300]

        file.write(f"\nResult {index}\n")
        file.write("-" * 50 + "\n")
        file.write(f"Page: {page}\n\n")
        file.write(preview + "...\n")


def save_results(
    results: dict,
    output_file: str | Path,
) -> None:
    """
    Save experiment results to a text file.
    """

    output_file = Path(output_file)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    baseline = results["MMR"]
    reranked = results["RERANKED"]

    with open(output_file, "w", encoding="utf-8") as file:

        file.write("=" * 70 + "\n")
        file.write("EXPERIMENT 06: RERANKER COMPARISON\n")
        file.write("MMR vs MMR + Cross-Encoder Reranker\n")
        file.write("=" * 70 + "\n\n")

        file.write("MMR RETRIEVAL\n")
        file.write("-" * 50 + "\n")
        file.write(f"Retrieval Time      : {baseline['retrieval_time']:.4f} seconds\n")
        file.write(f"Retrieved Documents : {baseline['retrieved_documents']}\n")
        file.write(f"Unique Pages        : {baseline['unique_pages']}\n")
        file.write(f"Duplicate Chunks    : {baseline['duplicate_chunks']}\n")
        file.write(f"Context Diversity   : {baseline['context_diversity']:.2f}\n\n")

        file.write("MMR + CROSS-ENCODER\n")
        file.write("-" * 50 + "\n")
        file.write(f"Retrieval Time      : {reranked['retrieval_time']:.4f} seconds\n")
        file.write(f"Reranking Time      : {reranked['rerank_time']:.4f} seconds\n")
        file.write(f"Total Pipeline Time : {reranked['total_time']:.4f} seconds\n")
        file.write(f"Retrieved Documents : {reranked['retrieved_documents']}\n")
        file.write(f"Unique Pages        : {reranked['unique_pages']}\n")
        file.write(f"Duplicate Chunks    : {reranked['duplicate_chunks']}\n")
        file.write(f"Context Diversity   : {reranked['context_diversity']:.2f}\n")

        file.write("\n")
        file.write("=" * 70 + "\n")
        file.write("ENGINEERING DECISION\n")
        file.write("=" * 70 + "\n")

        if reranked["total_time"] > baseline["retrieval_time"]:
            file.write(
                "✓ Cross-Encoder introduced additional inference latency.\n"
            )

        if reranked["context_diversity"] >= baseline["context_diversity"]:
            file.write(
                "✓ Context diversity was preserved after reranking.\n"
            )

        if reranked["duplicate_chunks"] <= baseline["duplicate_chunks"]:
            file.write(
                "✓ Reranking maintained low document redundancy.\n"
            )

        file.write("\nProduction Considerations:\n")
        file.write(
            "- MMR efficiently retrieves diverse candidate documents.\n"
        )
        file.write(
            "- Cross-Encoder performs semantic relevance refinement.\n"
        )
        file.write(
            "- Reranking increases latency but improves document ordering.\n"
        )
        file.write(
            "- Suitable when answer quality is prioritized over response speed.\n"
        )

        file.write("\nFinal Recommendation:\n")
        file.write(
            "Use MMR retrieval with Cross-Encoder reranking in production "
            "RAG systems where retrieval quality is more important than "
            "slightly higher latency.\n"
        )

        _write_documents(
            file,
            "MMR RETRIEVAL - DOCUMENTS",
            baseline["documents"],
        )

        _write_documents(
            file,
            "MMR + CROSS-ENCODER - DOCUMENTS",
            reranked["documents"],
        )