"""
Reranking logic for Experiment 06.

Takes retrieved documents and reorders them using a cross-encoder
based relevance scoring model.
"""

from sentence_transformers import CrossEncoder
from langchain_core.documents import Document


def rerank_documents(
    query: str,
    documents: list[Document],
    reranker: CrossEncoder,
    top_k: int = 3,
) -> list[Document]:
    """
    Rerank retrieved documents based on query relevance.

    Parameters
    ----------
    query : str
        User query.
    documents : list[Document]
        Retrieved documents from MMR.
    reranker : CrossEncoder
        Loaded reranker model.
    top_k : int
        Number of final documents to return.

    Returns
    -------
    list[Document]
        Re-ranked top documents.
    """

    if not documents:
        return []

    pairs = [(query, doc.page_content) for doc in documents]

    scores = reranker.predict(pairs)

    scored_docs = list(zip(documents, scores))

    # Sort by relevance score (descending)
    scored_docs.sort(key=lambda x: x[1], reverse=True)

    # Return top-k documents
    return [doc for doc, _ in scored_docs[:top_k]]