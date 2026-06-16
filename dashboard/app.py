"""
Xeven Solutions — AI Internship Dashboard
Sehar Andleeb | Day 22

Run from inside the dashboard/ folder:
    python app.py

Then open http://127.0.0.1:5000 in your browser.
"""

import json
import os
import random
import time
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# ---------------------------------------------------------------------------
# All 22 days of internship data
# Each day has: day number, topic, tasks, status, key numbers
# ---------------------------------------------------------------------------

DAYS = [
    {
        "day": 1,
        "topic": "Python Fundamentals",
        "tasks": ["Variables & data types", "Control flow", "Functions"],
        "status": "done",
        "highlight": "Python basics recap — foundation for everything ahead",
    },
    {
        "day": 2,
        "topic": "OOP in Python",
        "tasks": ["Classes & objects", "Inheritance", "Magic methods"],
        "status": "done",
        "highlight": "Built a class hierarchy for ML model abstraction",
    },
    {
        "day": 3,
        "topic": "File Handling & Modules",
        "tasks": ["Read/write files", "os & pathlib", "Custom modules"],
        "status": "done",
        "highlight": "Automated file processing with pathlib",
    },
    {
        "day": 4,
        "topic": "NumPy & Data Structures",
        "tasks": ["ndarray ops", "Broadcasting", "Linear algebra"],
        "status": "done",
        "highlight": "Matrix multiplication from scratch with NumPy",
    },
    {
        "day": 5,
        "topic": "Pandas for Data Analysis",
        "tasks": ["DataFrames", "GroupBy", "Merge & pivot"],
        "status": "done",
        "highlight": "Analysed a real CSV dataset end-to-end",
    },
    {
        "day": 6,
        "topic": "Data Visualisation",
        "tasks": ["Matplotlib", "Seaborn", "Plot types"],
        "status": "done",
        "highlight": "Built correlation heatmaps and distribution plots",
    },
    {
        "day": 7,
        "topic": "Machine Learning Basics",
        "tasks": ["Scikit-learn pipeline", "Train/test split", "Metrics"],
        "status": "done",
        "highlight": "Trained first classifier with 89% accuracy",
    },
    {
        "day": 8,
        "topic": "Regression & Classification",
        "tasks": ["Linear regression", "Logistic regression", "SVM"],
        "status": "done",
        "highlight": "Compared 3 classifiers on the same dataset",
    },
    {
        "day": 9,
        "topic": "Ensemble Methods",
        "tasks": ["Random Forest", "Gradient Boosting", "XGBoost"],
        "status": "done",
        "highlight": "XGBoost achieved best F1-score of 0.92",
    },
    {
        "day": 10,
        "topic": "Feature Engineering",
        "tasks": ["Feature selection", "Encoding", "Scaling"],
        "status": "done",
        "highlight": "Reduced feature set from 120 to 28 without accuracy loss",
    },
    {
        "day": 11,
        "topic": "Deep Learning Intro",
        "tasks": ["Neural networks", "Backpropagation", "Activation functions"],
        "status": "done",
        "highlight": "Built a 3-layer network from scratch with NumPy",
    },
    {
        "day": 12,
        "topic": "PyTorch Basics",
        "tasks": ["Tensors", "Autograd", "Training loop"],
        "status": "done",
        "highlight": "First PyTorch model trained on MNIST",
    },
    {
        "day": 13,
        "topic": "CNNs for Image Classification",
        "tasks": ["Conv layers", "Pooling", "ResNet architecture"],
        "status": "done",
        "highlight": "CNN reached 96% accuracy on CIFAR-10 subset",
    },
    {
        "day": 14,
        "topic": "NLP Fundamentals",
        "tasks": ["Tokenisation", "TF-IDF", "Text preprocessing"],
        "status": "done",
        "highlight": "Built a spam classifier with TF-IDF + Naive Bayes",
    },
    {
        "day": 15,
        "topic": "Transformers & BERT",
        "tasks": ["Attention mechanism", "BERT fine-tuning", "HuggingFace"],
        "status": "done",
        "highlight": "Fine-tuned DistilBERT for sentiment analysis",
    },
    {
        "day": 16,
        "topic": "LLM APIs & Groq",
        "tasks": ["Groq API", "Prompt engineering", "ChatGroq via LangChain"],
        "status": "done",
        "highlight": "First LLM app: Q&A chatbot with llama-3.3-70b-versatile",
    },
    {
        "day": 17,
        "topic": "Embeddings & Semantic Search",
        "tasks": [
            "all-MiniLM-L6-v2 embeddings",
            "Cosine similarity from scratch",
            "60-sentence search engine",
        ],
        "status": "done",
        "highlight": "Semantic search engine with t-SNE cluster visualisation",
    },
    {
        "day": 18,
        "topic": "Text Chunking Strategies",
        "tasks": [
            "RecursiveCharacterTextSplitter",
            "Chunk size sweep 200–2000",
            "Overlap analysis",
        ],
        "status": "done",
        "highlight": "Found 400 chars / 60 overlap as optimal for retrieval",
    },
    {
        "day": 19,
        "topic": "LangChain Chains & Memory",
        "tasks": [
            "LLMChain & LCEL",
            "ConversationBufferMemory",
            "Multi-turn chatbot",
        ],
        "status": "done",
        "highlight": "Built a multi-turn chatbot with persistent memory",
    },
    {
        "day": 20,
        "topic": "RAG Pipeline",
        "tasks": [
            "Retrieval-Augmented Generation",
            "RetrievalQA chain",
            "Source citation",
        ],
        "status": "done",
        "highlight": "Full RAG pipeline: PDF → chunks → FAISS → LLM answer",
    },
    {
        "day": 21,
        "topic": "Document Analyzer App",
        "tasks": [
            "Streamlit UI",
            "FAISS + Pydantic extraction",
            "End-to-end pipeline",
        ],
        "status": "done",
        "highlight": (
            "Integrated Document Analyzer: upload → chunk → "
            "FAISS → structured extraction"
        ),
    },
    {
        "day": 22,
        "topic": "Vector Stores & Databases",
        "tasks": [
            "FAISS operations (add/search/delete/save)",
            "Document library — 70 docs, 83 chunks, metadata filter",
            "FAISS vs Chroma benchmark",
        ],
        "status": "done",
        "highlight": (
            "FAISS: 0.10 ms/query. Chroma: 0.98 ms/query. "
            "Topic overlap Jaccard: 1.00"
        ),
    },
]

# Benchmark data from actual Day 22 runs
BENCHMARK = {
    "task1": {
        "label": "FAISS Basic Operations",
        "docs": 12,
        "index_time_ms": 0.8,
        "avg_latency_ms": 0.13,
        "queries_tested": 50,
        "total_time_ms": 6.6,
        "status": "passed",
    },
    "task2": {
        "label": "Document Library",
        "docs": 70,
        "chunks": 83,
        "chunk_size": 800,
        "overlap": 100,
        "index_time_ms": 12,
        "avg_latency_ms": 0.08,
        "queries_tested": 50,
        "topics": 7,
        "status": "passed",
    },
    "task3": {
        "label": "FAISS vs Chroma",
        "docs": 60,
        "faiss_index_s": 0.21,
        "faiss_latency_ms": 0.10,
        "faiss_memory_mb": 5.49,
        "chroma_index_s": 0.29,
        "chroma_latency_ms": 0.98,
        "chroma_memory_mb": 1.19,
        "jaccard_overlap": 1.00,
        "status": "passed",
    },
}

# ---------------------------------------------------------------------------
# Simple offline document corpus for the search demo
# (mirrors the 7 topics from task2_document_library.py)
# ---------------------------------------------------------------------------

CORPUS = [
    {"topic": "Machine Learning",
     "text": "Supervised learning trains a model on labelled examples to "
             "predict outputs for unseen inputs."},
    {"topic": "Machine Learning",
     "text": "Gradient descent minimises the loss by iteratively moving "
             "parameters in the direction of the negative gradient."},
    {"topic": "Machine Learning",
     "text": "Ensemble methods like Random Forest and XGBoost combine "
             "multiple models to improve prediction accuracy."},
    {"topic": "Deep Learning",
     "text": "Convolutional neural networks learn spatial hierarchies of "
             "features from grid-structured data like images."},
    {"topic": "Deep Learning",
     "text": "Transformers use self-attention to model dependencies across "
             "all positions in a sequence simultaneously."},
    {"topic": "Deep Learning",
     "text": "Diffusion models generate data by learning to reverse a "
             "gradual Gaussian noising process."},
    {"topic": "NLP",
     "text": "BERT pre-trains a bidirectional Transformer encoder using "
             "masked language modelling on large text corpora."},
    {"topic": "NLP",
     "text": "Word embeddings map words to dense vectors where semantic "
             "similarity correlates with geometric proximity."},
    {"topic": "NLP",
     "text": "Large language models are trained on trillions of tokens via "
             "next-token prediction, developing emergent capabilities."},
    {"topic": "Vector Databases",
     "text": "FAISS provides fast similarity search using IndexFlatIP with "
             "L2-normalised vectors for cosine similarity."},
    {"topic": "Vector Databases",
     "text": "HNSW (Hierarchical Navigable Small World) achieves high "
             "recall at low latency via a multi-layer proximity graph."},
    {"topic": "Vector Databases",
     "text": "Chroma is an open-source vector database with native "
             "persistence, metadata filtering, and LangChain integration."},
    {"topic": "RAG",
     "text": "Retrieval-Augmented Generation grounds LLM responses in "
             "retrieved document chunks, reducing hallucination."},
    {"topic": "RAG",
     "text": "Chunking splits documents into pieces using "
             "RecursiveCharacterTextSplitter for optimal retrieval."},
    {"topic": "RAG",
     "text": "Hybrid search combines dense vector retrieval with BM25 "
             "keyword search for better coverage across query types."},
    {"topic": "AI Ethics",
     "text": "AI bias arises from historical, representation, and "
             "measurement biases present in training data."},
    {"topic": "AI Ethics",
     "text": "Differential privacy adds calibrated noise during training "
             "to prevent individual records from being inferred."},
    {"topic": "AI Tools",
     "text": "LangChain provides composable components — chains, "
             "retrievers, memory, and agents — for LLM applications."},
    {"topic": "AI Tools",
     "text": "FastAPI serves ML models as REST endpoints with automatic "
             "validation and async support for high throughput."},
]


def simple_search(query, topic_filter="all", top_k=5):
    """
    Deterministic keyword-overlap search over CORPUS.
    Returns top_k results sorted by relevance score.
    This runs without FAISS or any ML model installed.
    """
    query_words = set(query.lower().split())
    results = []

    pool = CORPUS
    if topic_filter != "all":
        pool = [d for d in CORPUS if d["topic"] == topic_filter]

    for doc in pool:
        text_words = set(doc["text"].lower().split())
        overlap = len(query_words & text_words)
        # Small random jitter so ties break differently each query
        score = overlap / max(len(query_words), 1) + random.uniform(0, 0.05)
        results.append({
            "topic": doc["topic"],
            "text": doc["text"],
            "score": round(score, 4),
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_k]


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    """Main dashboard page."""
    done = sum(1 for d in DAYS if d["status"] == "done")
    total = len(DAYS)
    return render_template(
        "index.html",
        days=DAYS,
        done=done,
        total=total,
        benchmark=BENCHMARK,
    )


@app.route("/api/search", methods=["POST"])
def api_search():
    """
    POST /api/search
    Body: { "query": "...", "topic": "..." }
    Returns: { "results": [...], "latency_ms": ... }
    """
    data = request.get_json()
    query = data.get("query", "").strip()
    topic = data.get("topic", "all")

    if not query:
        return jsonify({"error": "Query cannot be empty"}), 400

    start = time.perf_counter()
    results = simple_search(query, topic_filter=topic)
    elapsed_ms = round((time.perf_counter() - start) * 1000, 2)

    return jsonify({
        "results": results,
        "latency_ms": elapsed_ms,
        "query": query,
        "topic_filter": topic,
    })


@app.route("/api/day/<int:day_num>")
def api_day(day_num):
    """GET /api/day/22 — returns details for a specific day."""
    day = next((d for d in DAYS if d["day"] == day_num), None)
    if not day:
        return jsonify({"error": "Day not found"}), 404
    return jsonify(day)


@app.route("/api/benchmark")
def api_benchmark():
    """GET /api/benchmark — returns Day 22 benchmark numbers."""
    return jsonify(BENCHMARK)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("  Xeven AI Internship Dashboard")
    print("  Sehar Andleeb — Day 22")
    print("  http://127.0.0.1:5000")
    print("=" * 50 + "\n")
    app.run(debug=True)