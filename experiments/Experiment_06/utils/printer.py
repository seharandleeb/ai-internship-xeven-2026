"""
Printing utilities for Experiment 06.

Displays a formatted comparison between baseline MMR retrieval
and MMR followed by Cross-Encoder reranking.
"""


def _print_documents(title: str, documents: list) -> None:
    """
    Print retrieved document previews.
    """

    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)

    for index, document in enumerate(documents, start=1):
        page = document.metadata.get("page", "Unknown")

        preview = document.page_content.replace("\n", " ")
        preview = " ".join(preview.split())
        preview = preview[:300]

        print(f"\nResult {index}")
        print("-" * 50)
        print(f"Page: {page}")
        print()
        print(preview + "...")


def print_summary(
    results: dict,
    total_chunks: int,
) -> None:
    """
    Print experiment summary.
    """

    baseline = results["MMR"]
    reranked = results["RERANKED"]

    print("\n" + "=" * 70)
    print("EXPERIMENT 06: RERANKER COMPARISON")
    print("MMR vs MMR + Cross-Encoder Reranker")
    print("=" * 70)

    print("\nExperiment Configuration")
    print("-" * 70)
    print(f"Total Chunks        : {total_chunks}")

    # ----------------------------------------------------------
    # Baseline
    # ----------------------------------------------------------

    print("\nMMR Retrieval")
    print("-" * 50)
    print(f"Retrieval Time      : {baseline['retrieval_time']:.4f} seconds")
    print(f"Retrieved Documents : {baseline['retrieved_documents']}")
    print(f"Unique Pages        : {baseline['unique_pages']}")
    print(f"Duplicate Chunks    : {baseline['duplicate_chunks']}")
    print(f"Context Diversity   : {baseline['context_diversity']:.2f}")

    # ----------------------------------------------------------
    # Reranked
    # ----------------------------------------------------------

    print("\nMMR + Cross-Encoder")
    print("-" * 50)
    print(f"Retrieval Time      : {reranked['retrieval_time']:.4f} seconds")
    print(f"Reranking Time      : {reranked['rerank_time']:.4f} seconds")
    print(f"Total Pipeline Time : {reranked['total_time']:.4f} seconds")
    print(f"Retrieved Documents : {reranked['retrieved_documents']}")
    print(f"Unique Pages        : {reranked['unique_pages']}")
    print(f"Duplicate Chunks    : {reranked['duplicate_chunks']}")
    print(f"Context Diversity   : {reranked['context_diversity']:.2f}")

    # ----------------------------------------------------------
    # Engineering Decision
    # ----------------------------------------------------------

    print("\n" + "=" * 70)
    print("ENGINEERING DECISION")
    print("=" * 70)

    if reranked["total_time"] > baseline["retrieval_time"]:
        print("✓ Cross-Encoder introduces additional inference latency.")

    if reranked["context_diversity"] >= baseline["context_diversity"]:
        print("✓ Context diversity was preserved after reranking.")

    if reranked["duplicate_chunks"] <= baseline["duplicate_chunks"]:
        print("✓ Reranking maintained low document redundancy.")

    print("\nProduction Considerations:")
    print("- MMR efficiently retrieves diverse candidate documents.")
    print("- Cross-Encoder performs semantic relevance refinement.")
    print("- Reranking increases latency but improves document ordering.")
    print("- Suitable when answer quality is prioritized over response speed.")

    print("\nFinal Recommendation:")
    print(
        "Use MMR retrieval with Cross-Encoder reranking in production "
        "RAG systems where retrieval quality is more important than "
        "slightly higher latency."
    )

    print("\n" + "=" * 70)

    # ----------------------------------------------------------
    # Retrieved Documents
    # ----------------------------------------------------------

    _print_documents(
        "MMR RETRIEVAL - DOCUMENTS",
        baseline["documents"],
    )

    _print_documents(
        "MMR + CROSS-ENCODER - DOCUMENTS",
        reranked["documents"],
    )