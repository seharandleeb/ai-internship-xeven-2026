"""
Embedding model configuration for Experiment 04.

This module loads and returns the embedding model selected in
Experiment 03 (BAAI/bge-m3). The same embedding model is shared
across all vector database implementations to ensure a fair comparison.
"""

from langchain_huggingface import HuggingFaceEmbeddings

from config.settings import EMBEDDING_MODEL_NAME


def get_embedding_model() -> HuggingFaceEmbeddings:
    """
    Load and return the configured embedding model.

    Returns
    -------
    HuggingFaceEmbeddings
        Configured HuggingFace embedding model.
    """
    embedding_model = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL_NAME,
        model_kwargs={
            "device": "cpu",
        },
        encode_kwargs={
            "normalize_embeddings": True,
        },
    )

    return embedding_model