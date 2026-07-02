# Experiments

This directory contains practical engineering experiments conducted during the AI Engineer Internship to evaluate individual components of a production-level Retrieval-Augmented Generation (RAG) pipeline.

Each experiment benchmarks two alternative technologies under identical conditions, measures their performance using objective metrics, and documents the engineering decision based on experimental evidence rather than theoretical assumptions.

---

# Repository Structure

```text
experiments/
│
├── README.md
├── LEARNINGS.md
│
├── Experiment_01/
│   ├── compare.py
│   ├── pymupdf_loader.py
│   ├── pdfplumber_loader.py
│   └── Experiment_01_PDF_Loader_Comparison.ipynb
│
├── Experiment_02/
│   ├── compare.py
│   ├── recursive_chunking.py
│   ├── token_chunking.py
│   └── Experiment_02_Chunking_Comparison.ipynb
│
├── Experiment_03/
│   ├── compare.py
│   ├── minilm_embedding.py
│   ├── bge_embedding.py
│   ├── queries.py
│   ├── retrieval.py
│   └── Experiment_03_Embedding_Comparison.ipynb
│
└── Experiment_04/
    ├── config/
    ├── data/
    ├── embeddings/
    ├── evaluation/
    ├── loaders/
    ├── retrieval/
    ├── splitters/
    ├── utils/
    ├── vectorstores/
    ├── run_experiment.py
    ├── comparison_results.txt
    └── Experiment_04_Vector_Database_Comparison.ipynb
```

---

# Experiment Status

| Experiment | Component | Status |
|------------|-----------|--------|
| Experiment 01 | PDF Loader Comparison | ✅ Completed |
| Experiment 02 | Chunking Strategy Comparison | ✅ Completed |
| Experiment 03 | Embedding Model Comparison | ✅ Completed |
| Experiment 04 | Vector Database Comparison | ✅ Completed |
| Experiment 05 | Retrieval Strategy Comparison | ⏳ Planned |
| Experiment 06 | Reranker Comparison | ⏳ Planned |

---

# Experiment 01: PDF Loader Comparison

## Objective

Compare two widely used PDF processing libraries to determine the most suitable PDF loader for a production-level Retrieval-Augmented Generation (RAG) pipeline.

### Technologies Evaluated

- PyMuPDF
- pdfplumber

---

## Evaluation Metrics

- PDF Loading Time
- Text Extraction Time
- Number of Pages
- Characters Extracted
- Words Extracted
- Text Extraction Quality

---

## Results

| Metric | PyMuPDF | pdfplumber |
|---------|---------:|-----------:|
| Pages | 63 | 63 |
| Characters | 105,293 | 95,136 |
| Words | 16,011 | 15,949 |
| Extraction Time | **0.2977 sec** | **4.7518 sec** |

---

## Engineering Decision

**Selected Library:** PyMuPDF

### Reasons

- Faster document loading
- Higher text extraction coverage
- Better scalability
- Lower preprocessing latency
- Better suited for production document ingestion

---

## Key Learning

Practical benchmarking demonstrated that technology selection should be based on measurable performance rather than documentation alone. PyMuPDF consistently outperformed pdfplumber in extraction speed while preserving high-quality text, making it the preferred choice for production document ingestion.

---

# Experiment 02: Chunking Strategy Comparison

## Objective

Compare two commonly used document chunking strategies to determine the most suitable preprocessing approach for a production Retrieval-Augmented Generation (RAG) pipeline.

### Technologies Evaluated

- Recursive Character Text Splitter
- Token Text Splitter

---

## Evaluation Metrics

- Number of Chunks
- Average Characters per Chunk
- Average Tokens per Chunk
- Execution Time

---

## Results

| Metric | Recursive Character | Token |
|---------|--------------------:|------:|
| Number of Chunks | 232 | 75 |
| Average Characters | 457.78 | 1557.12 |
| Average Tokens | 107.94 | 362.19 |
| Execution Time | **0.0054 sec** | **0.1794 sec** |

---

## Engineering Decision

**Selected Strategy:** Recursive Character Text Splitter

### Reasons

- Faster preprocessing
- Smaller and more manageable chunks
- Better retrieval granularity
- Lower computational overhead
- Widely adopted in production RAG systems

---

## Key Learning

The chunking strategy has a direct impact on preprocessing efficiency and retrieval quality. Recursive Character Text Splitter generated consistent chunk sizes while significantly reducing preprocessing time, making it the preferred choice for downstream semantic retrieval tasks.
---

# Experiment 03: Embedding Model Comparison

## Objective

Compare two state-of-the-art embedding models to identify the most suitable embedding model for a production-level Retrieval-Augmented Generation (RAG) pipeline.

### Technologies Evaluated

- all-MiniLM-L6-v2
- BAAI/bge-m3

---

## Evaluation Metrics

- Embedding Generation Time
- Embedding Dimension
- Number of Generated Embeddings
- Semantic Representation Capability

---

## Results

| Metric | MiniLM | BGE-M3 |
|---------|--------:|--------:|
| Embedding Dimension | 384 | 1024 |
| Number of Embeddings | 232 | 232 |
| Execution Time | 9.56 sec | 88.81 sec |

---

## Engineering Decision

**Selected Model:** BAAI/bge-m3

### Reasons

- Higher-dimensional embeddings
- Richer semantic representation
- Better contextual understanding
- Improved semantic retrieval capability
- Better suited for production RAG systems where retrieval quality is prioritized over embedding speed

---

## Key Learning

Embedding models significantly influence retrieval quality in Retrieval-Augmented Generation systems. Although BGE-M3 requires more time to generate embeddings, its richer semantic representation makes it a better choice for production environments where retrieval accuracy is more important than preprocessing speed.

---

# Experiment 04: Vector Database Comparison

## Objective

Compare two widely used vector databases to determine the most suitable vector storage solution for a production-level Retrieval-Augmented Generation (RAG) pipeline.

To ensure a controlled and fair comparison, all previously selected pipeline components remained unchanged:

- PDF Loader: PyMuPDF
- Chunking Strategy: Recursive Character Text Splitter
- Embedding Model: BAAI/bge-m3

Only the vector database was changed throughout the experiment.

### Technologies Evaluated

- FAISS
- ChromaDB

---

## Evaluation Metrics

- Index Creation Time
- Average Retrieval Time (10 benchmark runs)
- Number of Retrieved Documents
- Persistence Support
- Ease of Integration
- Production Suitability

---

## Results

| Metric | FAISS | ChromaDB |
|---------|-------:|---------:|
| Index Creation Time | Varies per execution* | Varies per execution* |
| Average Retrieval Time | Varies per execution* | Varies per execution* |
| Retrieved Documents | 5 | 5 |

> **Note:** Execution times vary slightly between runs depending on hardware, operating system scheduling, caching, and model initialization. The comparison is based on average benchmark measurements rather than a single execution.

---

## Engineering Decision

Both vector databases performed well under identical experimental conditions.

### FAISS

- Lightweight implementation
- Fast in-memory similarity search
- Minimal deployment overhead
- Excellent choice for applications where persistence is not required

### ChromaDB

- Built-in persistence
- Easy collection management
- Native LangChain integration
- Better suited for long-running production systems

---

## Final Recommendation

Both FAISS and ChromaDB are suitable vector databases for Retrieval-Augmented Generation systems.

- Choose **FAISS** for lightweight deployments and high-performance in-memory retrieval.
- Choose **ChromaDB** when persistent storage, maintainability, and long-term document management are important.

The final engineering decision should be based on production requirements rather than benchmark speed alone.

---

## Key Learning

This experiment demonstrated that vector databases with identical embeddings and document chunks produce very similar retrieval performance on moderate-sized datasets. While benchmark timings are useful, production engineering decisions should also consider persistence, scalability, maintainability, and deployment requirements.

---

# Summary

This directory documents a series of controlled engineering experiments conducted during the AI Engineer Internship to evaluate the core components of a production-level Retrieval-Augmented Generation (RAG) pipeline.

Each experiment isolates a single pipeline component while keeping the remaining components unchanged, ensuring fair and reproducible comparisons. Engineering decisions are based on practical benchmarking rather than theoretical assumptions.

The completed experiments cover:

- PDF Loader Comparison
- Chunking Strategy Comparison
- Embedding Model Comparison
- Vector Database Comparison

Together, these experiments establish the foundation of a production-oriented RAG pipeline by selecting each major component through measurable performance evaluation and reproducible engineering practices.

Detailed implementation notes, observations, engineering decisions, and technical learnings are documented separately in **LEARNINGS.md**.