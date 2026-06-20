"""ScholarRAG - hybrid retriever.

Blends FAISS semantic search and BM25 keyword search into one ranked
list. Each side's raw scores are min-max normalized to [0, 1] first
(cosine similarity and BM25 scores live on completely different
scales), then blended 70% semantic / 30% keyword - the same weighting
validated during the Day 25 recall@k evaluation.
"""

SEMANTIC_WEIGHT = 0.70
KEYWORD_WEIGHT = 0.30
CANDIDATE_POOL = 20


def _min_max_normalize(scored_items):
    """Rescale a {chunk_id: score} dict to [0, 1]. Empty/flat -> all 0."""
    if not scored_items:
        return {}
    values = list(scored_items.values())
    lo, hi = min(values), max(values)
    if hi == lo:
        return {key: 0.0 for key in scored_items}
    return {
        key: (value - lo) / (hi - lo)
        for key, value in scored_items.items()
    }


class HybridRetriever:
    """Combines a VectorStore and a BM25Index into one ranked search."""

    def __init__(self, vector_store, bm25_index,
                 semantic_weight=SEMANTIC_WEIGHT,
                 keyword_weight=KEYWORD_WEIGHT):
        self.vector_store = vector_store
        self.bm25_index = bm25_index
        self.semantic_weight = semantic_weight
        self.keyword_weight = keyword_weight

    def search(self, query_text, query_vector, top_k=5):
        """Return the top_k chunks by blended semantic + keyword score."""
        semantic_hits = self.vector_store.search(
            query_vector, top_k=CANDIDATE_POOL
        )
        keyword_hits = self.bm25_index.search(
            query_text, top_k=CANDIDATE_POOL
        )

        semantic_scores = {h["chunk_id"]: h["score"] for h in semantic_hits}
        keyword_scores = {h["chunk_id"]: h["score"] for h in keyword_hits}

        semantic_norm = _min_max_normalize(semantic_scores)
        keyword_norm = _min_max_normalize(keyword_scores)

        chunk_lookup = {h["chunk_id"]: h for h in semantic_hits}
        chunk_lookup.update({h["chunk_id"]: h for h in keyword_hits})

        blended = {}
        for chunk_id in chunk_lookup:
            s_score = semantic_norm.get(chunk_id, 0.0)
            k_score = keyword_norm.get(chunk_id, 0.0)
            blended[chunk_id] = (
                self.semantic_weight * s_score
                + self.keyword_weight * k_score
            )

        ranked_ids = sorted(
            blended, key=lambda cid: blended[cid], reverse=True
        )[:top_k]

        results = []
        for chunk_id in ranked_ids:
            chunk = dict(chunk_lookup[chunk_id])
            chunk["score"] = blended[chunk_id]
            results.append(chunk)
        return results


if __name__ == "__main__":
    import numpy as np

    from bm25_index import BM25Index
    from vector_store import VectorStore

    demo_chunks = [
        {"chunk_id": "sem", "text": "neural networks learn patterns"},
        {"chunk_id": "kw", "text": "attention transformer attention"},
        {"chunk_id": "neither", "text": "weather rain clouds today"},
    ]

    dim = 4
    demo_vectors = np.array([
        [1.0, 0.0, 0.0, 0.0],  # "sem": will match the query closely
        [0.0, 1.0, 0.0, 0.0],  # "kw": semantically unrelated to query
        [0.0, 0.0, 1.0, 0.0],  # "neither"
    ], dtype="float32")

    store = VectorStore(dim)
    store.build(demo_chunks, demo_vectors)
    bm25 = BM25Index(demo_chunks)
    retriever = HybridRetriever(store, bm25)

    query_text = "attention transformer"
    query_vector = np.array([1.0, 0.0, 0.0, 0.0], dtype="float32")

    print("Query is semantically close to 'sem' but keyword-matches 'kw'.")
    print("70/30 blend should still favor 'sem':")
    for hit in retriever.search(query_text, query_vector, top_k=3):
        print(" ", hit["chunk_id"], "score={0:.3f}".format(hit["score"]))