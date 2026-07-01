# Experiments

This directory contains all practical experiments conducted during the AI Engineer Internship. Each experiment focuses on evaluating different components of a production-level Retrieval-Augmented Generation (RAG) pipeline using implementation, benchmarking, and comparative analysis.

The goal of these experiments is to make evidence-based engineering decisions instead of selecting technologies based solely on documentation or assumptions.

---

# Experiment 01: PDF Loader Comparison

## Objective

Compare two widely used PDF processing libraries to determine the most suitable PDF loader for a production-level RAG pipeline.

Libraries evaluated:

- PyMuPDF
- pdfplumber

---

## Dataset

- **Document:** `SBP-Act.pdf`
- **Type:** Regulatory PDF
- **Pages:** 63

---

## Evaluation Metrics

The comparison was performed using the following metrics:

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

## Observations

- Both libraries successfully processed all pages.
- PyMuPDF extracted more textual content.
- PyMuPDF completed extraction significantly faster.
- pdfplumber preserved readable formatting but required considerably more processing time.

---

## Decision

**Selected Library:** PyMuPDF

### Reasons

- Faster document loading
- Higher text extraction coverage
- Better scalability
- Lower processing latency
- Suitable for production-scale RAG document ingestion

---

## Files

```
Experiment_01/
│
├── SBP-Act.pdf
├── pymupdf_loader.py
├── pdfplumber_loader.py
├── compare.py
└── Experiment_01_PDF_Loader_Comparison.ipynb
```

---

## Key Learning

This experiment demonstrated that selecting technologies based on practical benchmarking is more reliable than relying solely on documentation. Performance evaluation helps identify the most suitable components for production AI systems.