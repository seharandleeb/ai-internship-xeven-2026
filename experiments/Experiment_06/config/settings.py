"""
Configuration settings for Experiment 06: Reranker Comparison

This module centralizes all configurable parameters used
throughout the experiment.
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
# Selected Components from Previous Experiments
# ==========================================================

# Selected in Experiment 01
PDF_LOADER = "PyMuPDF"

# Selected in Experiment 02
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Selected in Experiment 03
EMBEDDING_MODEL_NAME = "BAAI/bge-m3"

# Selected in Experiment 04
VECTOR_DATABASE = "ChromaDB"

# ==========================================================
# Reranker Configuration
# ==========================================================

# Lightweight Cross-Encoder used for local benchmarking.
# This can later be replaced with any stronger reranker.
RERANKER_MODEL_NAME = "cross-encoder/ms-marco-MiniLM-L-6-v2"

# ==========================================================
# Retrieval Configuration
# ==========================================================

TOP_K = 5

FINAL_TOP_K = 3

BENCHMARK_RUNS = 10

DEFAULT_QUERY = (
    "What are the main functions of the State Bank of Pakistan?"
)