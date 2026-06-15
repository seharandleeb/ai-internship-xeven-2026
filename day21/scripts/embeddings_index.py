"""Embeddings + FAISS index + semantic search.

Two embedders behind one interface:

* LIVE: sentence-transformers ``all-MiniLM-L6-v2`` (384-dim, local, no
  API) via ``HuggingFaceEmbeddings``. First run downloads ~80 MB once,
  then caches. Used with ``--live``.
* OFFLINE: a deterministic, dependency-light hashed bag-of-words
  embedder, also 384-dim and L2-normalized. It lets the index and
  semantic search run with no model download (e.g. in CI / a sandbox)
  while preserving the property that lexically related text scores
  higher, so the "expected top-k" check is meaningful and repeatable.

The FAISS index itself is REAL in both modes: an ``IndexFlatIP`` over
L2-normalized vectors, which makes inner product equal cosine
similarity. Only the vectors' origin differs between modes.
"""
from __future__ import annotations

import hashlib
import re

import faiss
import numpy as np

EMBED_DIM = 384  # matches all-MiniLM-L6-v2
_TOKEN_RE = re.compile(r"[a-z0-9]+")


class OfflineHashEmbedder:
    """Deterministic hashed bag-of-words embedder (offline stand-in)."""

    def __init__(self, dim: int = EMBED_DIM) -> None:
        self.dim = dim

    def _tokens(self, text: str) -> list[str]:
        return _TOKEN_RE.findall(text.lower())

    def _vector(self, text: str) -> np.ndarray:
        vec = np.zeros(self.dim, dtype="float32")
        for tok in self._tokens(text):
            digest = hashlib.md5(tok.encode("utf-8")).hexdigest()
            bucket = int(digest, 16) % self.dim
            vec[bucket] += 1.0
        norm = float(np.linalg.norm(vec))
        if norm > 0.0:
            vec /= norm
        return vec

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [self._vector(t).tolist() for t in texts]

    def embed_query(self, text: str) -> list[float]:
        return self._vector(text).tolist()


def get_embedder(use_offline: bool = True):
    """Return the offline stand-in or the real MiniLM embedder."""
    if use_offline:
        return OfflineHashEmbedder()
    # LIVE path: real model, downloaded + cached on first use.
    from langchain_huggingface import HuggingFaceEmbeddings

    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        encode_kwargs={"normalize_embeddings": True},
    )


def _to_matrix(vectors: list[list[float]]) -> np.ndarray:
    matrix = np.asarray(vectors, dtype="float32")
    faiss.normalize_L2(matrix)  # safety: ensure unit norm for cosine
    return matrix


class SemanticIndex:
    """FAISS cosine-similarity index over text chunks."""

    def __init__(self, embedder) -> None:
        self.embedder = embedder
        self.index: faiss.Index | None = None
        self.chunks: list[dict] = []

    def build(self, chunks: list[dict]) -> "SemanticIndex":
        if not chunks:
            raise ValueError("Cannot build an index from zero chunks.")
        self.chunks = chunks
        vectors = self.embedder.embed_documents(
            [c["text"] for c in chunks]
        )
        matrix = _to_matrix(vectors)
        self.index = faiss.IndexFlatIP(matrix.shape[1])
        self.index.add(matrix)
        return self

    def search(self, query: str, k: int = 3) -> list[dict]:
        if self.index is None:
            raise RuntimeError("Index not built; call build() first.")
        k = min(k, len(self.chunks))
        q_vec = _to_matrix([self.embedder.embed_query(query)])
        scores, ids = self.index.search(q_vec, k)
        results = []
        for score, idx in zip(scores[0], ids[0]):
            if idx < 0:
                continue
            chunk = dict(self.chunks[int(idx)])
            chunk["score"] = float(score)
            results.append(chunk)
        return results
