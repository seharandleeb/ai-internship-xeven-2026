"""
Configuration settings for Experiment 05.

This module centralizes all configurable parameters used throughout
the retrieval strategy comparison experiment.

Experiment Objective:
Compare Similarity Search and Maximal Marginal Relevance (MMR)
while keeping all other RAG pipeline components unchanged.
"""

from pathlib import Path


# ==========================================================
# Project Paths
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
INPUT_DIR = DATA_DIR / "input"
VECTORSTORE_DIR = DATA_DIR / "vectorstores"

OUTPUT_DIR = BASE_DIR / "outputs"

PDF_PATH = INPUT_DIR / "sample.pdf"

CHROMA_DB_DIR = VECTORSTORE_DIR / "chroma_db"

RESULTS_FILE = BASE_DIR / "comparison_results.txt"


# ==========================================================
# PDF Loader (Selected in Experiment 01)
# ==========================================================

PDF_LOADER = "PyMuPDF"


# ==========================================================
# Chunking Configuration (Selected in Experiment 02)
# ==========================================================

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200


# ==========================================================
# Embedding Model (Selected in Experiment 03)
# ==========================================================

EMBEDDING_MODEL_NAME = "BAAI/bge-m3"


# ==========================================================
# Vector Database (Selected in Experiment 04)
# ==========================================================

VECTOR_DATABASE = "ChromaDB"


# ==========================================================
# Retrieval Configuration
# ==========================================================

TOP_K = 5

DEFAULT_QUERY = (
    "What are the responsibilities of the State Bank of Pakistan?"
)

BENCHMARK_RUNS = 10


# ==========================================================
# Retrieval Strategies
# ==========================================================

SIMILARITY_SEARCH = "similarity"

MMR_SEARCH = "mmr"


# ==========================================================
# MMR Configuration
# ==========================================================

MMR_FETCH_K = 20
MMR_LAMBDA_MULT = 0.5