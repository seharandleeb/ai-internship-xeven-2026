"""
Cross-Encoder reranker for Experiment 06.

This module loads the configured Cross-Encoder reranker
used to rerank retrieved documents.
"""

from sentence_transformers import CrossEncoder

from config.settings import RERANKER_MODEL_NAME


def load_reranker(
    model_name: str | None = None,
) -> CrossEncoder:
    """
    Load and return the configured Cross-Encoder reranker.

    Parameters
    ----------
    model_name : str | None, optional
        Hugging Face model name.
        If None, the configured model from settings.py is used.

    Returns
    -------
    CrossEncoder
        Loaded Cross-Encoder model.
    """

    if model_name is None:
        model_name = RERANKER_MODEL_NAME

    return CrossEncoder(model_name)