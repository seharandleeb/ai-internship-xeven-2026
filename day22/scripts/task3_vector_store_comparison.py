"""
Day 22 - Task 3: Vector Store Comparison (FAISS vs Chroma).

Uses the same 60-document corpus from Task 2.
Measures indexing time, query latency, memory usage, and
result quality (top-5 topic overlap) for FAISS vs Chroma.
Writes a JSON report to outputs/task3/.

Run from inside day22/scripts/ so outputs land in
day22/scripts/outputs/.

Toggle USE_OFFLINE=True (default) for sandbox / CI.
Set USE_OFFLINE=False on your machine with .venv312
to use the real MiniLM model.

Dependencies (install in .venv312):
  uv pip install faiss-cpu chromadb sentence-transformers langchain
                 langchain-huggingface langchain-community
"""

import json
import os
import time
import tracemalloc
import numpy as np

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
USE_OFFLINE = True   # Set False on .venv312 to use real HuggingFaceEmbeddings


# ---------------------------------------------------------------------------
# Embedder helpers (same pattern as Task 1 & 2)
# ---------------------------------------------------------------------------

def get_embedder():
    """Return the appropriate embedder based on USE_OFFLINE flag."""
    if USE_OFFLINE:
        return OfflineEmbedder()
    from langchain_huggingface import HuggingFaceEmbeddings  # noqa: PLC0415
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


class OfflineEmbedder:
    """
    Deterministic 384-dim embedder for offline/sandbox testing.

    Works as a LangChain-compatible embeddings object so it can
    be passed directly to FAISS.from_texts() and Chroma().
    """

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
# Corpus helper (re-uses the same 60 docs as Task 2 for fair comparison)
# ---------------------------------------------------------------------------

def build_sample_corpus(n=60):
    """Return n auto-generated (text, metadata) pairs for benchmarking."""
    topics = [
        "machine learning", "deep learning", "NLP",
        "vector databases", "RAG", "AI ethics",
    ]
    corpus = []
    for i in range(n):
        topic = topics[i % len(topics)]
        text = (
            f"Document {i:03d} on {topic}. "
            f"This document discusses key concepts in {topic} including "
            f"algorithms, architectures, and best practices. "
            f"Understanding {topic} is essential for modern AI engineering. "
            f"Index: {i}. Topic seed: {topic[:4]}{i}."
        )
        meta = {
            "doc_id": str(i),
            "topic": topic,
            "source": f"source_{topic.replace(' ', '_')}",
        }
        corpus.append((text, meta))
    return corpus


# ---------------------------------------------------------------------------
# FAISS wrapper (IndexFlatIP + cosine via L2 normalisation)
# ---------------------------------------------------------------------------

class FAISSStore:
    """FAISS vector store wrapper for benchmarking."""

    DIM = 384

    def __init__(self):
        import faiss  # noqa: PLC0415
        self.index = faiss.IndexFlatIP(self.DIM)
        self.docs = []   # list of (text, metadata)

    def _norm(self, vecs):
        norms = np.linalg.norm(vecs, axis=1, keepdims=True)
        norms = np.where(norms == 0, 1.0, norms)
        return (vecs / norms).astype(np.float32)

    def add(self, corpus, embedder):
        """Embed and add corpus."""
        texts = [c[0] for c in corpus]
        raw = np.array(embedder.embed_documents(texts), dtype=np.float32)
        self.index.add(self._norm(raw))
        self.docs = corpus

    def search(self, query, embedder, k=5):
        """Return top-k results."""
        raw = np.array([embedder.embed_query(query)], dtype=np.float32)
        scores, idxs = self.index.search(self._norm(raw), k)
        return [
            {
                "score": float(scores[0][i]),
                "text": self.docs[int(idxs[0][i])][0],
                "metadata": self.docs[int(idxs[0][i])][1],
            }
            for i in range(k)
            if idxs[0][i] != -1
        ]


# ---------------------------------------------------------------------------
# Chroma wrapper
# ---------------------------------------------------------------------------

class ChromaStore:
    """Chroma vector store wrapper for benchmarking."""

    def __init__(self, embedder, persist_dir=None):
        from chromadb import EphemeralClient  # noqa: PLC0415

        self.embedder = embedder
        self.client = EphemeralClient()
        # Delete if exists (idempotent re-runs)
        try:
            self.client.delete_collection("bench")
        except Exception:
            pass
        self.collection = self.client.create_collection(
            name="bench",
            metadata={"hnsw:space": "cosine"},
        )

    def add(self, corpus, embedder):
        """Embed and add corpus to Chroma collection."""
        texts = [c[0] for c in corpus]
        metas = [c[1] for c in corpus]
        embeddings = embedder.embed_documents(texts)
        ids = [f"doc_{i}" for i in range(len(texts))]
        self.collection.add(
            ids=ids,
            documents=texts,
            embeddings=embeddings,
            metadatas=metas,
        )

    def search(self, query, embedder, k=5):
        """Return top-k results."""
        q_emb = embedder.embed_query(query)
        res = self.collection.query(
            query_embeddings=[q_emb],
            n_results=k,
            include=["documents", "metadatas", "distances"],
        )
        results = []
        for doc, meta, dist in zip(
            res["documents"][0],
            res["metadatas"][0],
            res["distances"][0],
        ):
            results.append({
                "score": 1.0 - float(dist),  # cosine dist → similarity
                "text": doc,
                "metadata": meta,
            })
        return results


# ---------------------------------------------------------------------------
# Benchmark helpers
# ---------------------------------------------------------------------------

def benchmark_indexing(store_cls, corpus, embedder, store_kwargs=None):
    """
    Measure peak memory and wall-clock time to build the index.

    Returns (store, elapsed_s, peak_mb).
    """
    kwargs = store_kwargs or {}
    tracemalloc.start()
    t0 = time.perf_counter()
    store = store_cls(**kwargs)
    store.add(corpus, embedder)
    elapsed = time.perf_counter() - t0
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return store, elapsed, peak / 1024 / 1024


def benchmark_queries(store, embedder, queries, k=5):
    """
    Measure average query latency over a list of queries.

    Returns (results_list, avg_latency_ms).
    """
    all_results = []
    t0 = time.perf_counter()
    for q in queries:
        all_results.append(store.search(q, embedder, k=k))
    elapsed = time.perf_counter() - t0
    avg_ms = (elapsed / len(queries)) * 1000
    return all_results, avg_ms


def topic_overlap(results_a, results_b):
    """
    Measure average Jaccard overlap of top-5 topic sets between
    two result lists (list of list of result dicts).

    Returns float in [0, 1].
    """
    scores = []
    for ra, rb in zip(results_a, results_b):
        ta = {r["metadata"].get("topic", "") for r in ra}
        tb = {r["metadata"].get("topic", "") for r in rb}
        if not ta and not tb:
            scores.append(1.0)
        else:
            scores.append(len(ta & tb) / len(ta | tb))
    return sum(scores) / len(scores) if scores else 0.0


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    """Run Task 3: FAISS vs Chroma benchmark."""
    output_dir = os.path.join("outputs", "task3")
    os.makedirs(output_dir, exist_ok=True)

    print("=" * 60)
    print("Day 22 — Task 3: Vector Store Comparison (FAISS vs Chroma)")
    mode = 'OFFLINE (deterministic)' if USE_OFFLINE else 'ONLINE (MiniLM)'
    print(f'Mode: {mode}')
    print("=" * 60)

    embedder = get_embedder()

    # ------------------------------------------------------------------ #
    # 1. Build shared corpus
    # ------------------------------------------------------------------ #
    n_docs = 60
    print(f"\n[1] Building shared corpus ({n_docs} documents)...")
    corpus = build_sample_corpus(n_docs)

    # ------------------------------------------------------------------ #
    # 2. Check Chroma availability
    # ------------------------------------------------------------------ #
    chroma_available = True
    try:
        import chromadb as _chromadb_check  # noqa: F401
        del _chromadb_check
    except ImportError:
        chroma_available = False
        print("\n  [!] chromadb not installed. "
              "FAISS benchmarks will run; Chroma will be skipped.")
        print("      Install with: uv pip install chromadb")

    # ------------------------------------------------------------------ #
    # 3. Benchmark FAISS
    # ------------------------------------------------------------------ #
    print("\n[2] Benchmarking FAISS indexing...")
    faiss_store, faiss_idx_time, faiss_mem = benchmark_indexing(
        FAISSStore, corpus, embedder
    )
    print(f"  FAISS index time : {faiss_idx_time:.4f}s")
    print(f"  FAISS peak mem   : {faiss_mem:.2f} MB")

    queries = [
        "How do neural networks learn representations?",
        "What is approximate nearest neighbour search?",
        "Explain transformer attention mechanisms.",
        "What are best practices for RAG pipelines?",
        "How does gradient descent optimise models?",
        "What is the difference between FAISS and Chroma?",
        "How do diffusion models generate images?",
        "What is federated learning?",
        "Explain the bias-variance tradeoff.",
        "What is RLHF and how does it work?",
    ]

    print("\n[3] Benchmarking FAISS query latency (10 queries × 5 runs)...")
    faiss_results_list = []
    latencies = []
    for _ in range(5):
        res, lat = benchmark_queries(faiss_store, embedder, queries, k=5)
        latencies.append(lat)
        faiss_results_list = res
    faiss_avg_lat = sum(latencies) / len(latencies)
    print(f"  FAISS avg latency: {faiss_avg_lat:.2f} ms/query")

    # ------------------------------------------------------------------ #
    # 4. Benchmark Chroma
    # ------------------------------------------------------------------ #
    chroma_idx_time = chroma_mem = chroma_avg_lat = None
    chroma_results_list = []

    if chroma_available:
        print("\n[4] Benchmarking Chroma indexing...")
        chroma_store, chroma_idx_time, chroma_mem = benchmark_indexing(
            ChromaStore, corpus, embedder,
            store_kwargs={"embedder": embedder},
        )
        print(f"  Chroma index time : {chroma_idx_time:.4f}s")
        print(f"  Chroma peak mem   : {chroma_mem:.2f} MB")

        print(
            "\n[5] Benchmarking Chroma query latency"
            " (10 queries × 5 runs)..."
        )
        latencies = []
        for _ in range(5):
            res, lat = benchmark_queries(
                chroma_store, embedder, queries, k=5
            )
            latencies.append(lat)
            chroma_results_list = res
        chroma_avg_lat = sum(latencies) / len(latencies)
        print(f"  Chroma avg latency: {chroma_avg_lat:.2f} ms/query")

    # ------------------------------------------------------------------ #
    # 5. Result quality (topic overlap between FAISS & Chroma)
    # ------------------------------------------------------------------ #
    overlap = None
    if chroma_available and chroma_results_list:
        overlap = topic_overlap(faiss_results_list, chroma_results_list)
        print(f"\n[6] Top-5 topic overlap (Jaccard): {overlap:.4f}")

    # ------------------------------------------------------------------ #
    # 6. Sample results display
    # ------------------------------------------------------------------ #
    print("\n[7] Sample FAISS results for query[0]:")
    for i, r in enumerate(faiss_results_list[0], start=1):
        print(f"  #{i} score={r['score']:.4f} "
              f"| topic={r['metadata'].get('topic')} "
              f"| {r['text'][:80]}...")

    if chroma_available and chroma_results_list:
        print("\n[7b] Sample Chroma results for query[0]:")
        for i, r in enumerate(chroma_results_list[0], start=1):
            print(f"  #{i} score={r['score']:.4f} "
                  f"| topic={r['metadata'].get('topic')} "
                  f"| {r['text'][:80]}...")

    # ------------------------------------------------------------------ #
    # 7. Comparison table
    # ------------------------------------------------------------------ #
    print("\n" + "=" * 60)
    print("COMPARISON TABLE")
    print("=" * 60)
    c_idx = f"{chroma_idx_time:.4f}" if chroma_idx_time else "N/A"
    c_mem = f"{chroma_mem:.2f}" if chroma_mem else "N/A"
    c_lat = f"{chroma_avg_lat:.2f}" if chroma_avg_lat else "N/A"
    o_str = f"{overlap:.4f}" if overlap is not None else "N/A"
    hdr = f"{'Metric':<30} {'FAISS':>12} {'Chroma':>12}"
    print(hdr)
    print("-" * 60)
    print(f"{'Index time (s)':<30} {faiss_idx_time:>12.4f} "
          f"{c_idx:>12}")
    print(f"{'Peak mem (MB)':<30} {faiss_mem:>12.2f} "
          f"{c_mem:>12}")
    print(f"{'Avg latency (ms/q)':<30} {faiss_avg_lat:>12.2f} "
          f"{c_lat:>12}")
    print(f"{'Topic overlap (Jaccard)':<30} "
          f"{'N/A':>12} {o_str:>12}")
    print("=" * 60)

    # ------------------------------------------------------------------ #
    # 8. Save report JSON
    # ------------------------------------------------------------------ #
    report = {
        "n_docs": n_docs,
        "faiss": {
            "index_time_s": round(faiss_idx_time, 4),
            "peak_memory_mb": round(faiss_mem, 2),
            "avg_query_latency_ms": round(faiss_avg_lat, 2),
            "index_type": "IndexFlatIP (cosine via L2 normalisation)",
            "persistence": "manual (faiss.write_index)",
            "metadata_support": "external dict / pickle",
        },
        "chroma": {
            "index_time_s": round(chroma_idx_time, 4)
            if chroma_idx_time is not None
            else None,
            "peak_memory_mb": round(chroma_mem, 2)
            if chroma_mem is not None
            else None,
            "avg_query_latency_ms": round(chroma_avg_lat, 2)
            if chroma_avg_lat is not None
            else None,
            "index_type": "HNSW via hnswlib",
            "persistence": "built-in (SQLite + Parquet)",
            "metadata_support": "native with MongoDB-style filters",
        },
        "topic_overlap_jaccard": round(overlap, 4)
        if overlap is not None
        else None,
        "findings": {
            "FAISS": (
                "Lower overhead, no persistent layer by default, "
                "best for in-process or research use. "
                "Manual index save/load via write_index. "
                "No built-in metadata filtering — requires external "
                "lookup map. Extremely fast for exact search on "
                "small-medium datasets."
            ),
            "Chroma": (
                "Full-featured vector database with native persistence, "
                "rich metadata filtering ($eq, $in, $gte), and "
                "LangChain/LlamaIndex integration out of the box. "
                "Uses HNSW for ANN search. Higher overhead than FAISS "
                "for pure vector ops but far simpler for RAG pipelines."
            ),
        },
    }
    report_path = os.path.join(output_dir, "comparison_report.json")
    with open(report_path, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2)
    print(f"\n  Report written to {report_path}")

    print("\nTask 3 Complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
