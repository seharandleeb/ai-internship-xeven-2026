"""Day 24 - Self-contained RAG core (offline, numpy-only).

Provides a deterministic embedder, an auto-built FAISS vector store,
and a simple retrieval helper. No torch / sentence-transformers, so it
runs without the PyTorch c10.dll crash seen on this machine.
"""

import hashlib
import re

import faiss
import numpy as np

USE_OFFLINE = True
EMBED_DIM = 512

# Ultra-common words that carry little meaning for retrieval.
STOPWORDS = {
    "a", "an", "the", "and", "or", "of", "to", "in", "on", "for",
    "is", "are", "it", "its", "that", "this", "with", "by", "as",
    "how", "do", "i", "my", "from", "you", "your", "what", "about",
}


def tokenize(text):
    """Lowercase, strip punctuation, and drop stopwords."""
    words = re.findall(r"[a-z0-9]+", text.lower())
    return [w for w in words if w not in STOPWORDS]

# Small knowledge base, auto-defined in code (no manual setup needed).
SAMPLE_DOCS = [
    "A neural network is a model made of layers of connected nodes "
    "that learn patterns from data by adjusting numeric weights.",
    "Gradient descent is the optimization method that updates a "
    "model's weights step by step to reduce its prediction error.",
    "Overfitting happens when a model memorizes the training data "
    "and performs poorly on new, unseen examples.",
    "Regularization techniques like dropout and weight decay help "
    "prevent overfitting by discouraging overly complex models.",
    "A transformer is a neural architecture built on attention that "
    "processes all tokens in a sequence in parallel.",
    "Attention lets a model weigh which other tokens matter most "
    "when building the representation of a given token.",
    "An embedding is a numeric vector that captures the meaning of "
    "text so that similar texts sit close together in vector space.",
    "Retrieval-augmented generation, or RAG, fetches relevant "
    "documents and feeds them to a language model to ground answers.",
]


class DeterministicEmbedder:
    """Hash-based bag-of-words embedder. Numpy only, no torch."""

    def __init__(self, dim=EMBED_DIM):
        self.dim = dim

    def embed(self, text):
        """Turn one string into an L2-normalized float32 vector."""
        vec = np.zeros(self.dim, dtype="float32")
        for token in tokenize(text):
            digest = hashlib.md5(token.encode("utf-8")).hexdigest()
            idx = int(digest, 16) % self.dim
            vec[idx] += 1.0
        norm = np.linalg.norm(vec)
        if norm > 0:
            vec = vec / norm
        return vec

    def embed_many(self, texts):
        """Embed a list of strings into a 2D float32 matrix."""
        rows = [self.embed(text) for text in texts]
        return np.vstack(rows).astype("float32")


def build_vector_store(docs, embedder):
    """Build a FAISS IndexFlatIP store from a list of documents."""
    matrix = embedder.embed_many(docs)
    index = faiss.IndexFlatIP(embedder.dim)
    index.add(matrix)
    return index, list(docs)


def retrieve(query, index, docs, embedder, k=3):
    """Return the top-k (score, document) pairs for a query."""
    query_vec = embedder.embed(query).reshape(1, -1)
    scores, ids = index.search(query_vec, k)
    results = []
    for score, doc_id in zip(scores[0], ids[0]):
        if doc_id == -1:
            continue
        results.append((float(score), docs[doc_id]))
    return results


def main():
    """Build the store and run one sample retrieval as a smoke test."""
    print("USE_OFFLINE:", USE_OFFLINE)
    print("Embedding dimension:", EMBED_DIM)

    embedder = DeterministicEmbedder()
    index, docs = build_vector_store(SAMPLE_DOCS, embedder)
    print("Documents indexed:", index.ntotal)

    question = "How do I stop my model from overfitting?"
    print("\nQuery:", question)
    print("-" * 60)
    for rank, (score, doc) in enumerate(
        retrieve(question, index, docs, embedder, k=3), start=1
    ):
        print(f"{rank}. score={score:.3f}  {doc[:70]}...")


if __name__ == "__main__":
    main()