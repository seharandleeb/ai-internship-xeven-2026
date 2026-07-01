# AI Engineer Internship – Engineering Learnings

This document records the detailed technical learnings, implementation decisions, observations, comparisons, and engineering insights gained while building a production-level Retrieval-Augmented Generation (RAG) system.

Unlike the README, which provides a high-level overview of experiments, this document captures the reasoning behind each engineering decision and the lessons learned during implementation.

---

# Experiment 01: PDF Loader Comparison

## Objective

Evaluate different PDF loaders to identify the most suitable document loader for a production-level RAG pipeline.

---

## Technologies Evaluated

- PyMuPDF
- pdfplumber

---

## Implementation

Both loaders were implemented separately using the same PDF document. Each implementation extracted text from every page, measured execution time, counted pages, calculated the number of extracted characters and words, and generated a preview of the extracted content.

The same dataset and execution environment were used to ensure a fair comparison.

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
| Execution Time | 0.2977 sec | 4.7518 sec |

---

## Observations

### PyMuPDF

Advantages

- Very fast document loading
- Higher text extraction coverage
- Better handling of large PDF files
- Suitable for production document ingestion

Limitations

- Minor formatting inconsistencies may occur in complex layouts.

---

### pdfplumber

Advantages

- Better preservation of document layout
- Useful for table extraction
- Suitable for structured PDFs

Limitations

- Much slower than PyMuPDF
- Extracted fewer characters from the same document

---

## Engineering Decision

PyMuPDF was selected as the document loader for the RAG pipeline because it provides:

- Faster execution
- Better scalability
- Higher text extraction coverage
- Lower preprocessing latency

---

## Key Learning

Technology selection should always be supported by practical benchmarking instead of relying solely on documentation.

Although pdfplumber preserves formatting more effectively, PyMuPDF offers significantly better performance for large-scale document ingestion in production RAG systems.

---

# Experiment 02: Chunking Strategy Comparison

## Objective

Compare different chunking strategies to determine the most suitable approach for document preprocessing before embedding generation.

---

## Technologies Evaluated

- Recursive Character Text Splitter
- Token Text Splitter

---

## Why Chunking is Required

Large Language Models cannot process very large documents directly due to context window limitations.

Chunking divides long documents into smaller segments before generating embeddings.

The quality of chunking directly affects retrieval accuracy and final response quality.

---

## Implementation

The extracted PDF text was processed using two different chunking strategies.

Each strategy was evaluated using the same document and identical experimental conditions.

Performance was measured using execution time, number of generated chunks, average chunk size, and average token count.

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
| Execution Time | 0.0054 sec | 0.1794 sec |

---

## Understanding the Results

### Why did Recursive Character Splitter generate more chunks?

Recursive Character Text Splitter divides text based on character count. Since the chunk size was limited to approximately 500 characters, the document was split into a larger number of smaller chunks.

---

### Why did Token Text Splitter generate fewer chunks?

Token Text Splitter performs splitting based on tokens instead of characters.

Since a token usually represents multiple characters, each chunk became much larger, resulting in fewer total chunks.

---

### Why was Token Chunking slower?

Before splitting, Token Text Splitter first tokenizes the document using a tokenizer.

Tokenization introduces additional computation, making Token Chunking slower than character-based chunking.

---

## Observations

### Recursive Character Text Splitter

Advantages

- Extremely fast
- Simple implementation
- Smaller chunks
- Better retrieval granularity
- Most commonly used in LangChain-based RAG systems

Limitations

- Not aware of model token limits

---

### Token Text Splitter

Advantages

- Token-aware
- Better alignment with LLM context windows
- Useful when strict token limits are required

Limitations

- Slower preprocessing
- Larger chunks
- Additional tokenizer dependency

---

## Engineering Decision

Recursive Character Text Splitter was selected because:

- Faster execution
- Lower preprocessing overhead
- More manageable chunk sizes
- Better retrieval granularity
- Widely adopted in production RAG pipelines

Token Text Splitter remains a suitable option when precise tokenizer boundaries are required.

---

## Key Learning

Different chunking strategies significantly influence preprocessing performance and retrieval quality.

Character-based chunking provides excellent speed and practical chunk sizes, while token-based chunking offers greater control over LLM context windows at the cost of additional computational overhead.

Selecting a chunking strategy should depend on the target model, retrieval requirements, and production constraints.

---

# Future Experiments

- Experiment 03 — Embedding Model Comparison
- Experiment 04 — Vector Database Comparison
- Experiment 05 — Retrieval Strategy Comparison
- Experiment 06 — Reranker Comparison
- Experiment 07 — End-to-End RAG Evaluation

---

# Overall Engineering Insight

Building a production-level RAG system involves a series of engineering decisions rather than simply integrating available libraries.

Every component—including document loading, chunking, embedding generation, retrieval, reranking, and response generation—should be evaluated experimentally.

This internship focuses on selecting technologies based on measurable performance, scalability, and production suitability rather than assumptions or default implementations.