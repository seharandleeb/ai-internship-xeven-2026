"""
FAISS vector store implementation for Experiment 04.

This module provides reusable functions to create and configure
a FAISS vector store for document retrieval.
"""

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings

from config.settings import TOP_K


def create_faiss_vectorstore(
    documents: list[Document],
    embedding_model: Embeddings,
) -> FAISS:
    """
    Create a FAISS vector store from document chunks.

    Parameters
    ----------
    documents : list[Document]
        List of chunked LangChain documents.
    embedding_model : Embeddings
        Embedding model used to convert text into vectors.

    Returns
    -------
    FAISS
        Initialized FAISS vector store.
    """
    vectorstore = FAISS.from_documents(
        documents=documents,
        embedding=embedding_model,
    )

    return vectorstore


def get_faiss_retriever(vectorstore: FAISS):
    """
    Create a retriever from a FAISS vector store.

    Parameters
    ----------
    vectorstore : FAISS
        Initialized FAISS vector store.

    Returns
    -------
    BaseRetriever
        Configured LangChain retriever.
    """
    return vectorstore.as_retriever(
        search_kwargs={"k": TOP_K}
    )