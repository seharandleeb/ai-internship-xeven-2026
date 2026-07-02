"""
Main entry point for Experiment 06: Reranker Comparison.

This experiment compares:
1. MMR Retrieval (baseline)
2. MMR + Cross-Encoder Reranking (improved pipeline)
"""

from config.settings import (
    PDF_PATH,
    DEFAULT_QUERY,
    RESULTS_FILE,
    TOP_K,
)

from embeddings.embedding_model import get_embedding_model
from loaders.pdf_loader import load_pdf
from splitters.text_splitter import split_documents

from vectorstores.chroma_store import (
    create_chroma_vectorstore,
    get_chroma_retriever,
)

from retrieval.mmr import get_mmr_retriever

from reranker.cross_encoder import load_reranker

from evaluation.comparison import compare_retrieval_strategies
from utils.printer import print_summary
from utils.file_writer import save_results


def main():
    """
    Execute Experiment 06 pipeline.
    """

    # -------------------------------------------------------------
    # Step 1: Load PDF
    # -------------------------------------------------------------
    documents = load_pdf(PDF_PATH)

    # -------------------------------------------------------------
    # Step 2: Split documents
    # -------------------------------------------------------------
    chunks = split_documents(documents)

    # -------------------------------------------------------------
    # Step 3: Load embedding model
    # -------------------------------------------------------------
    embedding_model = get_embedding_model()

    # -------------------------------------------------------------
    # Step 4: Create vector store
    # -------------------------------------------------------------
    vectorstore = create_chroma_vectorstore(chunks, embedding_model)

    # -------------------------------------------------------------
    # Step 5: Build MMR retriever
    # -------------------------------------------------------------
    mmr_retriever = get_mmr_retriever(vectorstore, TOP_K)

    # -------------------------------------------------------------
    # Step 6: Load reranker model
    # -------------------------------------------------------------
    reranker = load_reranker()

    # -------------------------------------------------------------
    # Step 7: Run comparison
    # -------------------------------------------------------------
    results = compare_retrieval_strategies(
        mmr_retriever=mmr_retriever,
        reranker=reranker,
        query=DEFAULT_QUERY,
        top_k=TOP_K,
    )

    # -------------------------------------------------------------
    # Step 8: Print results
    # -------------------------------------------------------------
    print_summary(
        results=results,
        total_chunks=len(chunks),
    )

    # -------------------------------------------------------------
    # Step 9: Save results
    # -------------------------------------------------------------
    save_results(results, RESULTS_FILE)


if __name__ == "__main__":
    main()