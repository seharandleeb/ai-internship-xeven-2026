"""ScholarRAG - FAISS vector store.

Wraps a FAISS IndexFlatIP index over chunk embeddings. Takes vectors
that are already computed (kept separate from the embedding step
itself), so this module can be built and tested with synthetic
vectors, with no network calls needed.
"""

import faiss
import numpy as np


class VectorStore:
    """FAISS inner-product index over a list of chunk dicts."""

    def __init__(self, dim):
        self.dim = dim
        self.index = faiss.IndexFlatIP(dim)
        self.chunks = []

    def build(self, chunks, vectors):
        """Replace the store with a new set of chunks/vectors.

        Rebuilding from scratch (instead of incremental add/remove) is
        deliberate: FAISS IndexFlatIP has no native delete, so whenever
        a paper is added or removed the whole index is rebuilt from the
        current chunk list. Simple, and fast enough at this scale.
        """
        if len(chunks) != len(vectors):
            raise ValueError("chunks and vectors must be the same length")
        self.index = faiss.IndexFlatIP(self.dim)
        if len(vectors) > 0:
            self.index.add(np.ascontiguousarray(vectors, dtype="float32"))
        self.chunks = list(chunks)

    def search(self, query_vector, top_k=5):
        """Return the top_k chunks by cosine similarity to query_vector."""
        if len(self.chunks) == 0:
            return []
        query = np.ascontiguousarray(
            query_vector.reshape(1, -1), dtype="float32"
        )
        k = min(top_k, len(self.chunks))
        scores, indices = self.index.search(query, k)
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue
            chunk = dict(self.chunks[idx])
            chunk["score"] = float(score)
            results.append(chunk)
        return results


if __name__ == "__main__":
    rng = np.random.default_rng(seed=42)
    dim = 8
    demo_chunks = [
        {"chunk_id": "a", "text": "alpha chunk"},
        {"chunk_id": "b", "text": "beta chunk"},
        {"chunk_id": "c", "text": "gamma chunk"},
    ]
    demo_vectors = rng.normal(size=(3, dim)).astype("float32")
    norms = np.linalg.norm(demo_vectors, axis=1, keepdims=True)
    demo_vectors = demo_vectors / norms

    store = VectorStore(dim)
    store.build(demo_chunks, demo_vectors)

    query_vector = demo_vectors[1]  # should match chunk "b" best
    hits = store.search(query_vector, top_k=2)
    print("Top hits for a query matching chunk b:")
    for hit in hits:
        print(" ", hit["chunk_id"], "score={0:.3f}".format(hit["score"]))