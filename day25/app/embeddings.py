"""ScholarRAG - embeddings via the Gemini API.

Wraps Google's gemini-embedding-001 model so the rest of the app never
touches the Gemini SDK directly. Documents and queries are embedded
with different task types (RETRIEVAL_DOCUMENT vs RETRIEVAL_QUERY),
which measurably improves retrieval quality over using one mode for
both. Vectors are L2-normalized so a FAISS IndexFlatIP store can use
plain dot product as cosine similarity.
"""

import os

import numpy as np
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

MODEL_NAME = "gemini-embedding-001"
OUTPUT_DIM = 768
BATCH_SIZE = 50


def _normalize(vectors):
    """L2-normalize each row so dot product equals cosine similarity."""
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    return vectors / norms


class GeminiEmbedder:
    """Thin wrapper around the Gemini embed_content endpoint."""

    def __init__(self, api_key=None, dim=OUTPUT_DIM):
        key = api_key or os.getenv("GEMINI_API_KEY")
        if not key:
            raise RuntimeError(
                "GEMINI_API_KEY not found. Check your .env file."
            )
        self.client = genai.Client(api_key=key)
        self.dim = dim

    def _embed_batch(self, texts, task_type):
        config = types.EmbedContentConfig(
            task_type=task_type,
            output_dimensionality=self.dim,
        )
        response = self.client.models.embed_content(
            model=MODEL_NAME,
            contents=texts,
            config=config,
        )
        vectors = [item.values for item in response.embeddings]
        return np.array(vectors, dtype="float32")

    def embed_documents(self, texts):
        """Embed a list of chunk texts, for building the index."""
        all_vectors = []
        for start in range(0, len(texts), BATCH_SIZE):
            batch = texts[start:start + BATCH_SIZE]
            all_vectors.append(self._embed_batch(batch, "RETRIEVAL_DOCUMENT"))
        stacked = np.vstack(all_vectors)
        return _normalize(stacked)

    def embed_query(self, text):
        """Embed a single user question, for searching the index."""
        vectors = self._embed_batch([text], "RETRIEVAL_QUERY")
        return _normalize(vectors)[0]


if __name__ == "__main__":
    embedder = GeminiEmbedder()

    sample_texts = [
        "Self-attention relates different positions of a sequence.",
        "The Eiffel Tower is a landmark in Paris, France.",
        "Transformers rely on attention instead of recurrence.",
    ]
    doc_vectors = embedder.embed_documents(sample_texts)
    print("Doc embedding shape:", doc_vectors.shape)

    query_vector = embedder.embed_query("How does attention work?")
    print("Query embedding shape:", query_vector.shape)

    similarities = doc_vectors @ query_vector
    print("Similarities to query:", similarities)