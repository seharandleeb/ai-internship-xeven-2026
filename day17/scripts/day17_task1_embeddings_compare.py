"""Day 17 - Task 1: Generate and compare text embeddings.

Stack notes
-----------
Groq exposes no embeddings endpoint, so embeddings are produced locally and
for free with sentence-transformers (all-MiniLM-L6-v2, 384 dimensions) via the
LangChain 1.x ``langchain-huggingface`` integration. No API key is required for
this task, and no data file needs to be created by hand.

Install (Windows + UV):
    uv pip install langchain-huggingface sentence-transformers numpy matplotlib

This module keeps the *maths* (cosine similarity built from scratch) separate
from the *model*, so the similarity logic can be unit-tested with plain vectors.
"""

from __future__ import annotations

from typing import List, Sequence

import matplotlib.pyplot as plt
import numpy as np

plt.switch_backend("Agg")  # headless-safe backend for saving figures

EMBED_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

SAMPLE_SENTENCES: List[str] = [
    "The dog ran across the green park.",
    "A puppy played happily in the yard.",
    "My car would not start this morning.",
    "The sedan needed a new battery.",
    "She cooked a delicious vegetable curry.",
    "We enjoyed a healthy home-made soup.",
    "The stock market fell sharply today.",
    "Investors worried about rising interest rates.",
    "The telescope revealed distant galaxies.",
    "Astronomers photographed a spiral nebula.",
]


def get_embedder():
    """Return a LangChain HuggingFace embedder (downloads model on first run)."""
    from langchain_huggingface import HuggingFaceEmbeddings

    return HuggingFaceEmbeddings(model_name=EMBED_MODEL_NAME)


def cosine_similarity(vec_a: Sequence[float], vec_b: Sequence[float]) -> float:
    """Cosine similarity implemented from scratch with NumPy.

    cos(a, b) = (a . b) / (||a|| * ||b||); ranges from -1 to 1, where 1 means
    the vectors point in the same direction (semantically very similar).
    """
    a = np.asarray(vec_a, dtype=np.float64)
    b = np.asarray(vec_b, dtype=np.float64)
    denom = np.linalg.norm(a) * np.linalg.norm(b)
    if denom == 0.0:
        return 0.0
    return float(np.dot(a, b) / denom)


def build_similarity_matrix(vectors: Sequence[Sequence[float]]) -> np.ndarray:
    """Return an N x N matrix of pairwise cosine similarities."""
    n = len(vectors)
    matrix = np.zeros((n, n), dtype=np.float64)
    for i in range(n):
        for j in range(n):
            matrix[i, j] = cosine_similarity(vectors[i], vectors[j])
    return matrix


def save_heatmap(matrix: np.ndarray, labels: Sequence[str], out_path: str) -> None:
    """Render the similarity matrix as an annotated heatmap PNG."""
    fig, ax = plt.subplots(figsize=(9, 7.5))
    image = ax.imshow(matrix, cmap="viridis", vmin=0.0, vmax=1.0)
    ax.set_xticks(range(len(labels)))
    ax.set_yticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=45, ha="right", fontsize=8)
    ax.set_yticklabels(labels, fontsize=8)
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            ax.text(
                j,
                i,
                f"{matrix[i, j]:.2f}",
                ha="center",
                va="center",
                color="white" if matrix[i, j] < 0.6 else "black",
                fontsize=7,
            )
    ax.set_title("Cosine similarity matrix (all-MiniLM-L6-v2)")
    fig.colorbar(image, ax=ax, label="cosine similarity")
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def main() -> None:
    embedder = get_embedder()
    vectors = embedder.embed_documents(SAMPLE_SENTENCES)
    print(f"Embedded {len(vectors)} sentences -> dimension {len(vectors[0])}.")

    # Similar pair: dog vs puppy (indices 0, 1) should score high.
    dog_puppy = cosine_similarity(vectors[0], vectors[1])
    # Different pair: dog vs car (indices 0, 2) should score low.
    dog_car = cosine_similarity(vectors[0], vectors[2])
    print(f"dog  vs puppy similarity: {dog_puppy:.3f}  (expected high)")
    print(f"dog  vs car   similarity: {dog_car:.3f}  (expected low)")

    matrix = build_similarity_matrix(vectors)
    labels = [f"S{i}" for i in range(len(SAMPLE_SENTENCES))]
    out_path = "outputs/task1_similarity_matrix.png"
    save_heatmap(matrix, labels, out_path)
    print(f"Saved similarity heatmap -> {out_path}")


if __name__ == "__main__":
    main()
