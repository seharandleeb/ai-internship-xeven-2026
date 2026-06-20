"""ScholarRAG - retrieval evaluation.

Compares semantic-only search against the hybrid (semantic + BM25)
retriever using recall@k: for each test question, did the correct
paper section show up anywhere in the top-k results? Mirrors the
Day 25 evaluation, now run against a real paper instead of synthetic
documents.
"""

import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "app"))

from bm25_index import BM25Index  # noqa: E402
from embeddings import GeminiEmbedder  # noqa: E402
from hybrid_search import HybridRetriever  # noqa: E402
from ingestion import chunk_paper, load_paper  # noqa: E402
from vector_store import VectorStore  # noqa: E402

EVAL_QUESTIONS_PATH = os.path.join(
    os.path.dirname(__file__), "eval_questions.json"
)
K_VALUES = (3, 5)


def load_eval_questions():
    """Load the {question, sections} test set from disk."""
    with open(EVAL_QUESTIONS_PATH, "r", encoding="utf-8") as handle:
        return json.load(handle)


def recall_at_k(hits, accepted_sections, k):
    """1.0 if any of the top-k hits land in an accepted section."""
    top_sections = {hit["section"] for hit in hits[:k]}
    return 1.0 if top_sections & set(accepted_sections) else 0.0


def evaluate(paper_reference):
    """Run the full recall@k comparison for one paper."""
    paper = load_paper(paper_reference)
    chunks = chunk_paper(paper)
    print("Loaded '{0}' ({1} chunks).".format(paper["title"], len(chunks)))

    embedder = GeminiEmbedder()
    texts = [chunk["text"] for chunk in chunks]
    vectors = embedder.embed_documents(texts)

    vector_store = VectorStore(dim=embedder.dim)
    vector_store.build(chunks, vectors)
    bm25_index = BM25Index(chunks)
    hybrid = HybridRetriever(vector_store, bm25_index)

    questions = load_eval_questions()
    scores = {k: {"semantic": [], "hybrid": []} for k in K_VALUES}

    for item in questions:
        query_vector = embedder.embed_query(item["question"])
        max_k = max(K_VALUES)

        semantic_hits = vector_store.search(query_vector, top_k=max_k)
        hybrid_hits = hybrid.search(
            item["question"], query_vector, top_k=max_k
        )

        for k in K_VALUES:
            scores[k]["semantic"].append(
                recall_at_k(semantic_hits, item["sections"], k)
            )
            scores[k]["hybrid"].append(
                recall_at_k(hybrid_hits, item["sections"], k)
            )

    print(
        "\n{0:<4} {1:>10} {2:>10} {3:>10}".format(
            "k", "semantic", "hybrid", "lift"
        )
    )
    for k in K_VALUES:
        semantic_recall = sum(scores[k]["semantic"]) / len(questions)
        hybrid_recall = sum(scores[k]["hybrid"]) / len(questions)
        lift_points = (hybrid_recall - semantic_recall) * 100
        print(
            "{0:<4} {1:>9.1%} {2:>9.1%} {3:>+8.1f}pp".format(
                k, semantic_recall, hybrid_recall, lift_points
            )
        )


if __name__ == "__main__":
    evaluate("1706.03762")