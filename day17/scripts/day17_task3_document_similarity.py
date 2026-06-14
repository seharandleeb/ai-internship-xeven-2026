"""Day 17 - Task 3: Document similarity finder.

Fifteen short documents are created in-code (no manual files). Each document is
embedded as a whole, then:

* documents are grouped into clusters using a cosine-similarity threshold
  (single-linkage / connected-components style grouping),
* near-duplicates are flagged above a similarity threshold,
* all documents are projected to 2D with t-SNE and saved as a scatter plot.

A deliberate near-duplicate pair is included so the duplicate detector has
something to find.

Note on thresholds: cosine scores are *model-dependent*. The local 384-dim
all-MiniLM-L6-v2 model produces lower absolute scores than large API embedding
models, so the textbook 0.95 duplicate / 0.55 cluster cut-offs are tuned down
here (0.85 / 0.45) to suit this model. Tuning thresholds to the embedding model
is normal engineering, not a workaround.

Install (Windows + UV):
    uv pip install langchain-huggingface sentence-transformers numpy scikit-learn matplotlib
"""

from __future__ import annotations

import os
from typing import List, Sequence, Tuple

import matplotlib.pyplot as plt
import numpy as np
from sklearn.manifold import TSNE

plt.switch_backend("Agg")

EMBED_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# Thresholds tuned for the local MiniLM model (lower absolute cosine scores
# than large API embedding models). Raise these if you switch to a model that
# scores higher, e.g. OpenAI text-embedding-3-*.
CLUSTER_THRESHOLD = 0.45
DUPLICATE_THRESHOLD = 0.85

DOCUMENTS: List[str] = [
    "Researchers unveiled a new language model that improves reasoning on maths benchmarks.",
    "Researchers have unveiled a new language model that improves its "
    "reasoning on math benchmarks.",  # near-duplicate of #0 (trivial edits)
    "The central bank raised interest rates to fight stubborn inflation this quarter.",
    "Policymakers increased borrowing costs in an effort to cool rising consumer prices.",
    "The national team won the championship after a dramatic penalty shootout.",
    "Heavy rainfall caused severe flooding across several coastal towns this week.",
    "Scientists discovered a new exoplanet within the habitable zone of a nearby star.",
    "A breakthrough battery design promises faster charging for electric vehicles.",
    "The film festival awarded its top prize to an independent documentary.",
    "Health officials urged the public to get vaccinated ahead of flu season.",
    "Engineers tested a reusable rocket that landed safely after a high-altitude flight.",
    "Farmers reported lower yields this year due to an unusually dry summer.",
    "The museum opened a new exhibition featuring ancient Egyptian artefacts.",
    "A popular streaming service announced a price increase for premium subscribers.",
    "Volunteers planted thousands of trees to restore a fire-damaged forest.",
]


def get_embedder():
    """Return a LangChain HuggingFace embedder."""
    from langchain_huggingface import HuggingFaceEmbeddings

    return HuggingFaceEmbeddings(model_name=EMBED_MODEL_NAME)


def cosine_similarity(vec_a: Sequence[float], vec_b: Sequence[float]) -> float:
    """Cosine similarity between two vectors (range -1 to 1)."""
    a = np.asarray(vec_a, dtype=np.float64)
    b = np.asarray(vec_b, dtype=np.float64)
    denom = np.linalg.norm(a) * np.linalg.norm(b)
    if denom == 0.0:
        return 0.0
    return float(np.dot(a, b) / denom)


def cluster_by_threshold(
    vectors: Sequence[Sequence[float]], threshold: float = CLUSTER_THRESHOLD
) -> List[List[int]]:
    """Group vectors via single-linkage connected components.

    Two documents are linked if their cosine similarity is at least
    ``threshold``; transitive links form a cluster.
    """
    n = len(vectors)
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(x: int, y: int) -> None:
        parent[find(x)] = find(y)

    for i in range(n):
        for j in range(i + 1, n):
            if cosine_similarity(vectors[i], vectors[j]) >= threshold:
                union(i, j)

    groups: dict[int, List[int]] = {}
    for i in range(n):
        groups.setdefault(find(i), []).append(i)
    return list(groups.values())


def find_near_duplicates(
    vectors: Sequence[Sequence[float]],
    texts: Sequence[str],
    threshold: float = DUPLICATE_THRESHOLD,
) -> List[Tuple[int, int, float]]:
    """Return index pairs whose cosine similarity exceeds ``threshold``."""
    duplicates: List[Tuple[int, int, float]] = []
    n = len(vectors)
    for i in range(n):
        for j in range(i + 1, n):
            score = cosine_similarity(vectors[i], vectors[j])
            if score > threshold:
                duplicates.append((i, j, score))
    return duplicates


def save_tsne_plot(
    vectors: Sequence[Sequence[float]],
    clusters: Sequence[Sequence[int]],
    out_path: str,
) -> None:
    """Project documents to 2D with t-SNE and colour them by cluster."""
    data = np.asarray(vectors, dtype=np.float64)
    perplexity = min(5, max(2, len(data) - 1))
    coords = TSNE(
        n_components=2,
        perplexity=perplexity,
        init="pca",
        random_state=42,
    ).fit_transform(data)

    label_of = {}
    for cluster_id, members in enumerate(clusters):
        for idx in members:
            label_of[idx] = cluster_id

    colours = [label_of[i] for i in range(len(data))]
    fig, ax = plt.subplots(figsize=(8, 6))
    scatter = ax.scatter(
        coords[:, 0], coords[:, 1], c=colours, cmap="tab20", s=120
    )
    for i, (x, y) in enumerate(coords):
        ax.annotate(str(i), (x, y), fontsize=9, ha="center", va="center")
    ax.set_title("Documents projected to 2D (t-SNE), coloured by cluster")
    ax.set_xlabel("t-SNE 1")
    ax.set_ylabel("t-SNE 2")
    fig.colorbar(scatter, ax=ax, label="cluster id")
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def main() -> None:
    os.makedirs("outputs", exist_ok=True)
    embedder = get_embedder()
    vectors = embedder.embed_documents(DOCUMENTS)
    print(f"Embedded {len(DOCUMENTS)} documents -> dimension {len(vectors[0])}.")

    clusters = cluster_by_threshold(vectors, threshold=CLUSTER_THRESHOLD)
    print(f"\nFound {len(clusters)} cluster(s) at threshold {CLUSTER_THRESHOLD}:")
    for cluster_id, members in enumerate(clusters):
        print(f"  Cluster {cluster_id}: documents {members}")

    duplicates = find_near_duplicates(
        vectors, DOCUMENTS, threshold=DUPLICATE_THRESHOLD
    )
    print(
        f"\nNear-duplicates (> {DUPLICATE_THRESHOLD}): "
        f"{len(duplicates)} pair(s)"
    )
    for i, j, score in duplicates:
        print(f"  docs {i} & {j} -> {score:.3f}")
        print(f"    [{i}] {DOCUMENTS[i]}")
        print(f"    [{j}] {DOCUMENTS[j]}")

    out_path = "outputs/task3_tsne_clusters.png"
    save_tsne_plot(vectors, clusters, out_path)
    print(f"\nSaved t-SNE cluster plot -> {out_path}")


if __name__ == "__main__":
    main()