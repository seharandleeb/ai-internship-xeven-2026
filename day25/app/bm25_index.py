"""ScholarRAG - BM25 keyword index.

Sparse keyword search over chunk dicts, complementing FAISS semantic
search. Every chunk's text runs through the same tokenizer, so scores
stay comparable when blended with semantic scores later.
"""

import re

from rank_bm25 import BM25Okapi

STOPWORDS = {
    "a", "an", "the", "is", "are", "was", "were", "be", "been", "being",
    "of", "to", "in", "on", "for", "with", "as", "by", "at", "from",
    "and", "or", "but", "if", "then", "so", "that", "this", "these",
    "those", "it", "its", "we", "our", "they", "their", "can", "into",
}


def tokenize(text):
    """Lowercase, strip punctuation, split into words, drop stopwords."""
    words = re.findall(r"[a-z0-9]+", text.lower())
    return [word for word in words if word not in STOPWORDS]


class BM25Index:
    """Thin wrapper around BM25Okapi tied to a list of chunk dicts."""

    def __init__(self, chunks):
        self.chunks = list(chunks)
        self.corpus_tokens = [tokenize(c["text"]) for c in self.chunks]
        self.model = (
            BM25Okapi(self.corpus_tokens) if self.corpus_tokens else None
        )

    def search(self, query, top_k=5):
        """Return the top_k chunks by BM25 score for the query."""
        if not self.model:
            return []
        query_tokens = tokenize(query)
        scores = self.model.get_scores(query_tokens)
        ranked = sorted(
            range(len(self.chunks)), key=lambda i: scores[i], reverse=True
        )
        results = []
        for idx in ranked[:top_k]:
            chunk = dict(self.chunks[idx])
            chunk["score"] = float(scores[idx])
            results.append(chunk)
        return results


if __name__ == "__main__":
    demo_chunks = [
        {"chunk_id": "1", "text": "Self-attention relates positions."},
        {"chunk_id": "2", "text": "The Eiffel Tower is in Paris."},
        {"chunk_id": "3", "text": "Attention powers transformer models."},
    ]
    index = BM25Index(demo_chunks)
    hits = index.search("attention transformer", top_k=2)
    print("Top BM25 hits:")
    for hit in hits:
        print(" ", hit["chunk_id"], "score={0:.3f}".format(hit["score"]))