"""
Common retrieval utility for Experiment 06.

This ensures consistent retrieval interface across:
- MMR retriever
- future retrieval strategies
"""

from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever


def retrieve_documents(
    retriever: BaseRetriever,
    query: str,
) -> list[Document]:
    """
    Retrieve documents using any LangChain retriever.
    """

    return retriever.invoke(query)