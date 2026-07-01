# Experiments

This directory contains practical experiments conducted during the AI Engineer Internship to evaluate different components of a production-level Retrieval-Augmented Generation (RAG) pipeline.

Each experiment focuses on benchmarking multiple approaches, measuring their performance, and selecting the most suitable technology based on practical implementation instead of theoretical assumptions.

---

# Repository Structure

```text
experiments/
│
├── README.md
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
└── ...
```

---

# Experiment Status

| Experiment | Component | Status |
|------------|-----------|--------|
| Experiment 01 | PDF Loader Comparison | ✅ Completed |
| Experiment 02 | Chunking Strategy Comparison | ✅ Completed |
| Experiment 03 | Embedding Models Comparison | ⏳ Planned |
| Experiment 04 | Vector Database Comparison | ⏳ Planned |
| Experiment 05 | Retrieval Strategy Comparison | ⏳ Planned |
| Experiment 06 | Reranker Comparison | ⏳ Planned |

---

# Experiment 01: PDF Loader Comparison

## Objective

Compare two widely used PDF processing libraries to determine the most suitable PDF loader for a production-level RAG pipeline.

### Libraries Evaluated

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

## Decision

**Selected Library:** PyMuPDF

### Reasons

- Faster document loading
- Higher text extraction coverage
- Better scalability
- Lower processing latency
- Well suited for production document ingestion

---

## Key Learning

Practical benchmarking demonstrated that technology selection should be based on measurable performance rather than documentation alone. PyMuPDF consistently outperformed pdfplumber in extraction speed while preserving high-quality text.

---

# Experiment 02: Chunking Strategy Comparison

## Objective

Compare two commonly used chunking strategies to determine the most suitable approach for document chunking in a production RAG pipeline.

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

## Decision

**Selected Strategy:** Recursive Character Text Splitter

### Reasons

- Faster execution
- Smaller and more manageable chunks
- Better retrieval granularity
- Lower preprocessing overhead
- Widely adopted in production RAG systems

---

## Key Learning

This experiment highlighted how different chunking strategies affect preprocessing efficiency and chunk granularity. Recursive Character Text Splitter provided significantly faster execution while producing consistent chunk sizes suitable for downstream retrieval tasks.

---

# Summary

The experiments conducted in this directory provide practical evidence for selecting components of a production-level RAG pipeline. Each experiment measures performance, compares alternative implementations, and documents the engineering decisions used throughout the project.

Detailed implementation notes, observations, challenges, and technical learnings are documented separately in **LEARNINGS.md**.