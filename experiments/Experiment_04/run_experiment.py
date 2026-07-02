"""
Main entry point for Experiment 04.

This script compares FAISS and ChromaDB as vector databases for a
Retrieval-Augmented Generation (RAG) pipeline.

Workflow:
1. Load PDF
2. Split into chunks
3. Load embedding model
4. Create FAISS index
5. Create ChromaDB index
6. Retrieve documents
7. Compare performance
8. Print results
"""

from config.settings import PDF_PATH
from config.settings import DEFAULT_QUERY, OUTPUT_DIR, RESULTS_FILE
from utils.file_writer import save_results
from embeddings.embedding_model import get_embedding_model
from evaluation.comparison import compare_vectorstores
from evaluation.metrics import measure_execution_time
from loaders.pdf_loader import load_pdf
from splitters.text_splitter import split_documents
from utils.printer import print_summary
from vectorstores.chroma_store import (
    create_chroma_vectorstore,
    get_chroma_retriever,
)
from vectorstores.faiss_store import (
    create_faiss_vectorstore,
    get_faiss_retriever,
)


def main() -> None:
    """
    Execute Experiment 04.
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
    # Step 4: Create FAISS vector store
    # -------------------------------------------------------------
    faiss_store, faiss_index_time = measure_execution_time(
        create_faiss_vectorstore,
        chunks,
        embedding_model,
    )

    # -------------------------------------------------------------
    # Step 5: Create Chroma vector store
    # -------------------------------------------------------------
    chroma_store, chroma_index_time = measure_execution_time(
        create_chroma_vectorstore,
        chunks,
        embedding_model,
    )

    # -------------------------------------------------------------
    # Step 6: Create retrievers
    # -------------------------------------------------------------
    faiss_retriever = get_faiss_retriever(faiss_store)
    chroma_retriever = get_chroma_retriever(chroma_store)

    # -------------------------------------------------------------
    # Step 7: Query
    # -------------------------------------------------------------
    from config.settings import DEFAULT_QUERY
    query = DEFAULT_QUERY
    # -------------------------------------------------------------
    # Step 8: Compare vector databases
    # -------------------------------------------------------------
    results = compare_vectorstores(
    faiss_retriever=faiss_retriever,
    chroma_retriever=chroma_retriever,
    query=DEFAULT_QUERY,
    faiss_index_time=faiss_index_time,
    chroma_index_time=chroma_index_time,
)

    # -------------------------------------------------------------
    # Step 9: Print summary
    # -------------------------------------------------------------
    print_summary(
    results=results,
    total_chunks=len(chunks),
)

    save_results(results, RESULTS_FILE)

if __name__ == "__main__":
    main()