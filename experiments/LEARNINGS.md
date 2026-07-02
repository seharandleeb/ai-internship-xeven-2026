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

# Future Experiments

- Experiment 05 — Retrieval Strategy Comparison
- Experiment 06 — Reranker Comparison
- Experiment 07 — End-to-End RAG Evaluation

---
---

# Experiment 03 — Embedding Model Comparison

## Objective

The purpose of this experiment was to compare two widely used embedding models used in Retrieval-Augmented Generation (RAG) systems. The goal was to evaluate their performance and semantic representation capability before selecting an embedding model for the production pipeline.

---

## Technologies Used

- Sentence Transformers
- all-MiniLM-L6-v2
- BAAI/bge-m3
- PyMuPDF
- LangChain Recursive Character Text Splitter

---

## Methodology

The experiment followed the workflow below:

1. Load the PDF document using PyMuPDF.
2. Split the document into chunks using Recursive Character Text Splitter.
3. Generate embeddings using MiniLM.
4. Generate embeddings using BGE-M3.
5. Compare both models using execution time, embedding dimension, and semantic representation capability.
6. Select the most suitable embedding model for the RAG pipeline.

---

## Observations

### MiniLM

**Advantages**

- Fast embedding generation
- Lightweight model
- Lower computational cost
- Suitable for real-time applications

**Limitations**

- Lower embedding dimension (384)
- Less expressive semantic representation

---

### BGE-M3

**Advantages**

- Higher embedding dimension (1024)
- Rich semantic representation
- Better understanding of document context
- More suitable for semantic retrieval tasks

**Limitations**

- Higher embedding generation time
- Greater computational requirements

---

## Results

| Metric | MiniLM | BGE-M3 |
|---------|--------:|--------:|
| Embedding Dimension | 384 | 1024 |
| Number of Embeddings | 232 | 232 |
| Execution Time | 9.56 sec | 88.81 sec |

---

## Engineering Decision

Although MiniLM generated embeddings much faster, BGE-M3 was selected because retrieval quality is more important than embedding speed in a production Retrieval-Augmented Generation system. Higher-dimensional embeddings provide richer semantic representation, making BGE-M3 a better choice for regulatory document retrieval.

---

## Key Learnings

- Embeddings transform text into dense numerical vectors that capture semantic meaning.
- Embedding quality directly influences retrieval performance in RAG systems.
- Higher-dimensional embeddings generally preserve more semantic information.
- Practical benchmarking is essential before selecting components for production AI systems.
- Engineering decisions should be based on experimental evidence rather than assumptions or documentation alone.

--- 
# Experiment 04 — Vector Database Comparison

## Objective

The objective of this experiment was to compare two widely used vector databases, **FAISS** and **ChromaDB**, to determine the most suitable vector storage solution for a production Retrieval-Augmented Generation (RAG) pipeline.

To ensure a controlled comparison, all other pipeline components remained unchanged:

- PDF Loader: PyMuPDF
- Chunking Strategy: Recursive Character Text Splitter
- Embedding Model: BAAI/bge-m3

Only the vector database was changed throughout the experiment.

---

## Technologies Used

- LangChain
- FAISS
- ChromaDB
- BAAI/bge-m3
- PyMuPDF
- Recursive Character Text Splitter

---

## Why Vector Databases are Required

Large Language Models cannot efficiently search raw document collections.

After embeddings are generated, they must be stored in a vector database that supports efficient similarity search.

The vector database is responsible for:

- Storing document embeddings
- Performing nearest-neighbor similarity search
- Retrieving the most relevant document chunks
- Reducing retrieval latency
- Supporting scalable Retrieval-Augmented Generation pipelines

Choosing an appropriate vector database directly affects retrieval performance and production maintainability.

---

## Methodology

The experiment followed a controlled engineering workflow:

1. Load the PDF using PyMuPDF.
2. Split the document using Recursive Character Text Splitter.
3. Generate embeddings using BAAI/bge-m3.
4. Build a FAISS vector store.
5. Build a ChromaDB vector store.
6. Create retrievers for both vector databases.
7. Execute the same retrieval query against both systems.
8. Benchmark retrieval performance over multiple runs.
9. Compare the results and make an engineering decision.

---

## Evaluation Metrics

The following metrics were used during evaluation:

- Index Creation Time
- Average Retrieval Time
- Number of Retrieved Documents
- Persistence Support
- Ease of Integration
- Production Suitability

Average retrieval latency was measured over multiple benchmark runs to reduce the influence of one-time execution overhead.

---

## Observations

### FAISS

**Advantages**

- Lightweight implementation
- Fast similarity search
- Simple deployment
- Excellent in-memory performance
- Widely adopted in production AI systems

**Limitations**

- No built-in persistence
- External storage is required for long-term deployment
- Collection management must be implemented separately

---

### ChromaDB

**Advantages**

- Persistent vector storage
- Easy document collection management
- Native integration with LangChain
- Suitable for long-running applications
- Minimal configuration

**Limitations**

- Slightly higher storage overhead
- Additional persistence layer compared to FAISS

---

## Results

| Metric | FAISS | ChromaDB |
|---------|-------:|---------:|
| Index Creation Time | 95.13 sec | 92.96 sec |
| Average Retrieval Time | 0.1844 sec | 0.1947 sec |
| Retrieved Documents | 5 | 5 |

> **Note:** Execution times may vary slightly across different runs depending on hardware, operating system scheduling, model initialization, and caching effects.

---

## Understanding the Results

### Why were retrieval times so similar?

Both FAISS and ChromaDB indexed exactly the same document chunks using identical embeddings.

Because the document collection was relatively small, retrieval latency was naturally very close for both systems.

---

### Why benchmark multiple retrieval runs?

The first retrieval often includes initialization overhead such as cache warming.

Measuring average retrieval latency across multiple executions provides a more reliable estimate of real-world performance than relying on a single run.

---

### Why can index creation times vary?

Index creation involves embedding insertion, vector indexing, memory allocation, and disk operations.

These processes are influenced by system resources and background activity, resulting in small timing differences across executions.

---

## Engineering Decision

Both vector databases successfully supported semantic retrieval under identical experimental conditions.

### FAISS was preferred for:

- Lightweight deployment
- Fast in-memory retrieval
- Minimal overhead
- Applications where persistence is not required

### ChromaDB was preferred for:

- Persistent storage
- Long-running production systems
- Easier collection management
- Better maintainability

The final selection depends on deployment requirements rather than retrieval latency alone.

---

## Key Learnings

- Vector databases are fundamental components of Retrieval-Augmented Generation systems.
- Similarity search performance depends on both embeddings and vector indexing.
- Retrieval latency should be benchmarked over multiple runs to obtain reliable measurements.
- Small benchmark differences should not be overinterpreted, particularly for small datasets.
- Production engineering decisions should consider scalability, persistence, maintainability, and deployment requirements in addition to raw speed.
- Controlled experiments produce more reliable engineering decisions than assumptions or isolated benchmarks.

--- 


# Overall Engineering Insight

Every major component—including document loading, chunking, embedding generation, vector storage, retrieval, reranking, and response generation—should be evaluated experimentally before being integrated into a production pipeline.

Throughout these experiments, each component has been isolated, benchmarked, and selected using measurable performance metrics while keeping the remaining pipeline unchanged. This controlled engineering methodology ensures that design decisions are evidence-based, reproducible, and suitable for real-world AI applications.