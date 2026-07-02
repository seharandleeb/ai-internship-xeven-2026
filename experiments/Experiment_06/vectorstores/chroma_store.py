"""
ChromaDB vector store implementation for Experiment 06.

This module creates a persistent vector database using ChromaDB
for document retrieval in a RAG pipeline.
"""

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings

from config.settings import CHROMA_DB_DIR, TOP_K


def create_chroma_vectorstore(
    documents: list[Document],
    embedding_model: Embeddings,
) -> Chroma:
    """
    Create a persistent Chroma vector database.

    Parameters
    ----------
    documents : list[Document]
        Chunked documents.
    embedding_model : Embeddings
        Embedding model for vectorization.

    Returns
    -------
    Chroma
        Persisted vector database.
    """

    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embedding_model,
        persist_directory=str(CHROMA_DB_DIR),
    )

    return vectorstore


def get_chroma_retriever(vectorstore: Chroma):
    """
    Convert Chroma vector store into retriever.

    Parameters
    ----------
    vectorstore : Chroma
        Initialized vector database.

    Returns
    -------
    BaseRetriever
        Retriever with top-k search capability.
    """

    return vectorstore.as_retriever(
        search_kwargs={"k": TOP_K}
    )