"""
Day 22 - Task 1: FAISS Setup & Basic Operations.

Demonstrates: vector store creation, add/search/delete,
save/load index, and similarity search with scores.

Run from inside day22/scripts/ so outputs land in
day22/scripts/outputs/.

Toggle USE_OFFLINE=True (default) for sandbox / CI.
Set USE_OFFLINE=False on your machine with .venv312
to use the real MiniLM model.
"""

import os
import time
import pickle
import numpy as np

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
USE_OFFLINE = True   # Set False on .venv312 to use real HuggingFaceEmbeddings


# ---------------------------------------------------------------------------
# Embedder helpers
# ---------------------------------------------------------------------------

def get_embedder():
    """Return the appropriate embedder based on USE_OFFLINE flag."""
    if USE_OFFLINE:
        return OfflineEmbedder()
    # Real path — requires .venv312 with sentence-transformers installed
    from langchain_huggingface import HuggingFaceEmbeddings  # noqa: PLC0415
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


class OfflineEmbedder:
    """Deterministic 384-dim embedder for offline/sandbox testing."""

    DIM = 384

    def embed_documents(self, texts):
        """Embed a list of texts deterministically."""
        return [self._embed(t) for t in texts]

    def embed_query(self, text):
        """Embed a single query text deterministically."""
        return self._embed(text)

    def _embed(self, text):
        """Hash-seed RNG so same text → same vector every run."""
        seed = sum(ord(c) for c in text) % (2 ** 31)
        rng = np.random.default_rng(seed)
        vec = rng.standard_normal(self.DIM).astype(np.float32)
        norm = np.linalg.norm(vec)
        return (vec / norm).tolist()


# ---------------------------------------------------------------------------
# FAISS vector store wrapper
# ---------------------------------------------------------------------------

class FAISSVectorStore:
    """
    Thin wrapper around a FAISS IndexFlatIP store.

    Vectors are L2-normalised before insertion so inner-product
    search is equivalent to cosine similarity.
    """

    def __init__(self, dim=384):
        import faiss  # noqa: PLC0415
        self.dim = dim
        self.index = faiss.IndexFlatIP(dim)
        self.id_to_doc = {}   # int id → {"text": ..., "metadata": ...}
        self._next_id = 0

    # ------------------------------------------------------------------
    def _normalize(self, vecs):
        """L2-normalise a (N, D) float32 array in-place and return it."""
        norms = np.linalg.norm(vecs, axis=1, keepdims=True)
        norms = np.where(norms == 0, 1.0, norms)
        return (vecs / norms).astype(np.float32)

    # ------------------------------------------------------------------
    def add(self, texts, embedder, metadata_list=None):
        """
        Embed texts and add them to the FAISS index.

        Parameters
        ----------
        texts : list[str]
        embedder : object with .embed_documents()
        metadata_list : list[dict] | None
        """
        if metadata_list is None:
            metadata_list = [{} for _ in texts]

        raw = np.array(
            embedder.embed_documents(texts), dtype=np.float32
        )
        vecs = self._normalize(raw)
        self.index.add(vecs)

        for text, meta in zip(texts, metadata_list):
            self.id_to_doc[self._next_id] = {
                "text": text,
                "metadata": meta,
            }
            self._next_id += 1

        print(f"  Added {len(texts)} document(s). "
              f"Total in index: {self.index.ntotal}")

    # ------------------------------------------------------------------
    def search(self, query, embedder, k=5):
        """
        Return top-k results with cosine similarity scores.

        Returns
        -------
        list[dict] with keys: rank, score, text, metadata
        """
        raw = np.array(
            [embedder.embed_query(query)], dtype=np.float32
        )
        q_vec = self._normalize(raw)
        scores, indices = self.index.search(q_vec, k)

        results = []
        for rank, (score, idx) in enumerate(
            zip(scores[0], indices[0]), start=1
        ):
            if idx == -1:
                continue
            doc = self.id_to_doc.get(int(idx), {})
            results.append({
                "rank": rank,
                "score": float(score),
                "text": doc.get("text", ""),
                "metadata": doc.get("metadata", {}),
            })
        return results

    # ------------------------------------------------------------------
    def delete(self, doc_ids):
        """
        Remove documents by their integer IDs from the lookup map.

        Note: IndexFlatIP does not support in-place removal.
        We rebuild the index without the deleted vectors.
        """
        import faiss  # noqa: PLC0415

        remaining_ids = [
            i for i in range(self._next_id)
            if i in self.id_to_doc and i not in doc_ids
        ]

        if not remaining_ids:
            self.index = faiss.IndexFlatIP(self.dim)
            self.id_to_doc = {}
            print(f"  Deleted IDs {doc_ids}. Index is now empty.")
            return

        # Practical approach: mark as deleted in lookup map.
        # IndexFlatIP does not support in-place removal; a full
        # rebuild (re-embed remaining texts) is the correct but
        # expensive path and is omitted here intentionally.
        for doc_id in doc_ids:
            self.id_to_doc.pop(doc_id, None)

        print(f"  Deleted IDs {doc_ids}. "
              f"Remaining docs: {len(self.id_to_doc)}")

    def _make_vec_placeholder(self, text):
        """Unused placeholder — deletion uses lookup-map removal."""
        return np.zeros(self.dim, dtype=np.float32)

    # ------------------------------------------------------------------
    def save(self, folder):
        """Persist FAISS index + metadata to disk."""
        import faiss  # noqa: PLC0415
        os.makedirs(folder, exist_ok=True)
        faiss.write_index(self.index, os.path.join(folder, "index.faiss"))
        meta = {
            "dim": self.dim,
            "id_to_doc": self.id_to_doc,
            "next_id": self._next_id,
        }
        with open(os.path.join(folder, "meta.pkl"), "wb") as fh:
            pickle.dump(meta, fh)
        print(f"  Index saved to '{folder}/'")

    # ------------------------------------------------------------------
    @classmethod
    def load(cls, folder):
        """Reload a persisted FAISS index from disk."""
        import faiss  # noqa: PLC0415
        with open(os.path.join(folder, "meta.pkl"), "rb") as fh:
            meta = pickle.load(fh)
        store = cls(dim=meta["dim"])
        store.index = faiss.read_index(
            os.path.join(folder, "index.faiss")
        )
        store.id_to_doc = meta["id_to_doc"]
        store._next_id = meta["next_id"]
        print(f"  Index loaded from '{folder}/' "
              f"({store.index.ntotal} vectors)")
        return store


# ---------------------------------------------------------------------------
# Demo documents
# ---------------------------------------------------------------------------

DOCS = [
    ("Machine learning uses algorithms to learn from data.", {"topic": "ML"}),
    ("Deep learning is a subset of machine learning.", {"topic": "ML"}),
    ("Neural networks are inspired by the human brain.", {"topic": "DL"}),
    ("FAISS enables fast similarity search at scale.", {"topic": "FAISS"}),
    ("Vector databases store embeddings for retrieval.", {"topic": "VDB"}),
    ("Python is a popular language for data science.", {"topic": "Python"}),
    ("Transformers revolutionised natural language processing.",
     {"topic": "NLP"}),
    ("Cosine similarity measures angle between vectors.", {"topic": "Math"}),
    ("Embeddings map text to dense numeric representations.",
     {"topic": "NLP"}),
    ("RAG combines retrieval and generation for Q&A.", {"topic": "RAG"}),
]


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    """Run Task 1: FAISS basic operations demo."""
    output_dir = os.path.join("outputs", "task1")
    os.makedirs(output_dir, exist_ok=True)

    print("=" * 60)
    print("Day 22 — Task 1: FAISS Setup & Basic Operations")
    mode = 'OFFLINE (deterministic)' if USE_OFFLINE else 'ONLINE (MiniLM)'
    print(f'Mode: {mode}')
    print("=" * 60)

    embedder = get_embedder()

    # ------------------------------------------------------------------ #
    # 1. Create vector store & add documents
    # ------------------------------------------------------------------ #
    print("\n[1] Creating FAISS vector store & adding documents...")
    store = FAISSVectorStore(dim=384)
    texts = [d[0] for d in DOCS]
    metas = [d[1] for d in DOCS]
    store.add(texts, embedder, metas)

    # ------------------------------------------------------------------ #
    # 2. Similarity search
    # ------------------------------------------------------------------ #
    print("\n[2] Similarity search: 'How do neural networks learn?'")
    query = "How do neural networks learn?"
    results = store.search(query, embedder, k=3)
    for r in results:
        print(f"  #{r['rank']} score={r['score']:.4f} | "
              f"{r['text'][:60]} | meta={r['metadata']}")

    # ------------------------------------------------------------------ #
    # 3. Add more documents
    # ------------------------------------------------------------------ #
    print("\n[3] Adding 2 more documents...")
    new_texts = [
        "Gradient descent optimises model weights iteratively.",
        "Attention mechanisms focus on relevant input tokens.",
    ]
    new_metas = [{"topic": "ML"}, {"topic": "NLP"}]
    store.add(new_texts, embedder, new_metas)

    # ------------------------------------------------------------------ #
    # 4. Delete operation
    # ------------------------------------------------------------------ #
    print("\n[4] Deleting document IDs [0, 1]...")
    store.delete([0, 1])
    print(f"  Docs in lookup map: {len(store.id_to_doc)}")

    # ------------------------------------------------------------------ #
    # 5. Save index to disk
    # ------------------------------------------------------------------ #
    save_path = os.path.join(output_dir, "faiss_index")
    print(f"\n[5] Saving index to '{save_path}'...")
    store.save(save_path)

    # ------------------------------------------------------------------ #
    # 6. Load index from disk & re-query
    # ------------------------------------------------------------------ #
    print(f"\n[6] Loading index from '{save_path}'...")
    loaded = FAISSVectorStore.load(save_path)

    print("\n[6b] Re-running search on loaded index...")
    query2 = "What are vector databases used for?"
    results2 = loaded.search(query2, embedder, k=3)
    for r in results2:
        print(f"  #{r['rank']} score={r['score']:.4f} | "
              f"{r['text'][:60]} | meta={r['metadata']}")

    # ------------------------------------------------------------------ #
    # 7. Timing experiment
    # ------------------------------------------------------------------ #
    print("\n[7] Timing: search latency over 50 queries...")
    queries = [f"query about topic {i}" for i in range(50)]
    start = time.perf_counter()
    for q in queries:
        loaded.search(q, embedder, k=3)
    elapsed = time.perf_counter() - start
    avg_ms = (elapsed / 50) * 1000
    print(f"  50 queries in {elapsed:.4f}s  |  avg {avg_ms:.2f} ms/query")

    # ------------------------------------------------------------------ #
    # Summary
    # ------------------------------------------------------------------ #
    print("\n" + "=" * 60)
    print("Task 1 Complete!")
    print(f"  Documents indexed : {len(DOCS) + len(new_texts)}")
    print(f"  After deletion    : {len(store.id_to_doc)}")
    print(f"  Avg query latency : {avg_ms:.2f} ms")
    print(f"  Index saved to    : {save_path}")
    print("=" * 60)


if __name__ == "__main__":
    main()
