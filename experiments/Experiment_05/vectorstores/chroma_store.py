"""
ChromaDB vector store implementation for Experiment 05.

This module creates and configures the ChromaDB vector store selected
in Experiment 04. Both retrieval strategies operate on the same
vector database to ensure a fair comparison.
"""

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings

from config.settings import CHROMA_DB_DIR


def create_chroma_vectorstore(
    documents: list[Document],
    embedding_model: Embeddings,
) -> Chroma:
    """
    Create a persistent ChromaDB vector store.

    Parameters
    ----------
    documents : list[Document]
        Chunked LangChain documents.
    embedding_model : Embeddings
        Embedding model used to generate vector embeddings.

    Returns
    -------
    Chroma
        Initialized ChromaDB vector store.
    """
    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embedding_model,
        persist_directory=str(CHROMA_DB_DIR),
    )

    return vectorstore