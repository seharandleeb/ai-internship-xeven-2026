"""
Configuration settings for Experiment 04.

This module centralizes all configurable parameters used throughout the
vector database comparison experiment. Keeping configuration in one place
improves maintainability, readability, and reusability.
"""

from pathlib import Path


# =============================================================================
# Project Paths
# =============================================================================

# Root directory of Experiment_04
BASE_DIR = Path(__file__).resolve().parent.parent

# Data directories
DATA_DIR = BASE_DIR / "data"
INPUT_DIR = DATA_DIR / "input"
VECTORSTORE_DIR = DATA_DIR / "vectorstores"

# Input PDF
PDF_PATH = INPUT_DIR / "sample.pdf"

# Chroma persistence directory
CHROMA_DB_DIR = VECTORSTORE_DIR / "chroma_db"

# Output directory
OUTPUT_DIR = BASE_DIR / "outputs"
RESULTS_FILE = OUTPUT_DIR / "comparison_results.txt"


# =============================================================================
# Embedding Model Configuration
# =============================================================================

EMBEDDING_MODEL_NAME = "BAAI/bge-m3"


# =============================================================================
# Text Splitting Configuration
# =============================================================================

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200


# =============================================================================
# Retrieval Configuration
# =============================================================================

TOP_K = 5


# =============================================================================
# Experiment Query
# =============================================================================

DEFAULT_QUERY = (
    "What is the main topic discussed in the document?"
)


# =============================================================================
# Experiment Settings
# =============================================================================

RANDOM_SEED = 42

# =============================================================================
# Benchmark Configuration
# =============================================================================

NUM_RETRIEVAL_RUNS = 10