"""
Embedding model configuration for Experiment 05.

This module loads the embedding model selected in Experiment 03
(BAAI/bge-m3). The same embedding model is used throughout this
experiment to ensure a fair comparison between retrieval strategies.
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