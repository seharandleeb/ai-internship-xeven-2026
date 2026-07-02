"""
Main entry point for Experiment 05.

This script compares Similarity Search and Maximal Marginal
Relevance (MMR) retrieval strategies for a production-level
Retrieval-Augmented Generation (RAG) pipeline.

Workflow:
1. Load PDF
2. Split documents into chunks
3. Load embedding model
4. Create ChromaDB vector store
5. Create Similarity Search retriever
6. Create MMR retriever
7. Compare retrieval strategies
8. Print results
9. Save results
"""

from config.settings import (
    DEFAULT_QUERY,
    PDF_PATH,
    RESULTS_FILE,
)

from embeddings.embedding_model import get_embedding_model

from evaluation.comparison import (
    compare_retrieval_strategies,
)

from loaders.pdf_loader import load_pdf

from splitters.text_splitter import split_documents

from utils.file_writer import save_results
from utils.printer import print_summary

from vectorstores.chroma_store import (
    create_chroma_vectorstore,
)

from retrieval.similarity import (
    get_similarity_retriever,
)

from retrieval.mmr import (
    get_mmr_retriever,
)


def main() -> None:
    """
    Execute Experiment 05.
    """

    # ---------------------------------------------------------
    # Step 1: Load PDF
    # ---------------------------------------------------------
    documents = load_pdf(PDF_PATH)

    # ---------------------------------------------------------
    # Step 2: Split documents
    # ---------------------------------------------------------
    chunks = split_documents(documents)

    # ---------------------------------------------------------
    # Step 3: Load embedding model
    # ---------------------------------------------------------
    embedding_model = get_embedding_model()

    # ---------------------------------------------------------
    # Step 4: Create ChromaDB vector store
    # ---------------------------------------------------------
    vectorstore = create_chroma_vectorstore(
        chunks,
        embedding_model,
    )

    # ---------------------------------------------------------
    # Step 5: Create retrievers
    # ---------------------------------------------------------
    similarity_retriever = get_similarity_retriever(
        vectorstore
    )

    mmr_retriever = get_mmr_retriever(
        vectorstore
    )

    # ---------------------------------------------------------
    # Step 6: Compare retrieval strategies
    # ---------------------------------------------------------
    results = compare_retrieval_strategies(
        similarity_retriever=similarity_retriever,
        mmr_retriever=mmr_retriever,
        query=DEFAULT_QUERY,
    )

    # ---------------------------------------------------------
    # Step 7: Print summary
    # ---------------------------------------------------------
    print_summary(
        results=results,
        total_chunks=len(chunks),
    )

    # ---------------------------------------------------------
    # Step 8: Save results
    # ---------------------------------------------------------
    save_results(
        results,
        RESULTS_FILE,
    )


if __name__ == "__main__":
    main()