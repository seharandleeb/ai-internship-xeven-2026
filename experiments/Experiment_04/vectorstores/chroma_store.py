"""
ChromaDB vector store implementation for Experiment 04.

This module provides reusable functions to create and configure
a Chroma vector store for document retrieval.
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
    Create a persistent Chroma vector store from document chunks.

    Parameters
    ----------
    documents : list[Document]
        List of chunked LangChain documents.
    embedding_model : Embeddings
        Embedding model used to convert text into vectors.

    Returns
    -------
    Chroma
        Initialized persistent Chroma vector store.
    """
    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embedding_model,
        persist_directory=str(CHROMA_DB_DIR),
    )

    return vectorstore


def get_chroma_retriever(vectorstore: Chroma):
    """
    Create a retriever from a Chroma vector store.

    Parameters
    ----------
    vectorstore : Chroma
        Initialized Chroma vector store.

    Returns
    -------
    BaseRetriever
        Configured LangChain retriever.
    """
    return vectorstore.as_retriever(
        search_kwargs={"k": TOP_K}
    )