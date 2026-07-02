"""
MMR (Maximal Marginal Relevance) retrieval for Experiment 06.

MMR improves retrieval diversity by reducing redundancy and
ensuring that returned documents are both relevant and diverse.
"""

from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever


def get_mmr_retriever(vectorstore, top_k: int) -> BaseRetriever:
    """
    Create an MMR-based retriever.

    Parameters
    ----------
    vectorstore :
        Chroma vector store.
    top_k : int
        Number of documents to retrieve.

    Returns
    -------
    BaseRetriever
        MMR retriever instance.
    """

    retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": top_k,
            "fetch_k": top_k * 4,   # broad candidate pool
            "lambda_mult": 0.5      # balance relevance vs diversity
        }
    )

    return retriever