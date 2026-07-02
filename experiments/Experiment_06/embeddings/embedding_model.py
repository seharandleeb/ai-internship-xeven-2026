"""
Embedding model loader for Experiment 06.

We use the same embedding model across all experiments to ensure
fair comparison between retrieval + reranking strategies.
"""

from langchain_huggingface import HuggingFaceEmbeddings
from config.settings import EMBEDDING_MODEL_NAME


def get_embedding_model() -> HuggingFaceEmbeddings:
    """
    Load HuggingFace embedding model.

    Returns
    -------
    HuggingFaceEmbeddings
        Embedding model used for vector database creation.
    """

    model = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL_NAME,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )

    return model