"""
app.py
Day 23 - Flask Dashboard for RAG Pipeline Tasks
Xeven Solutions AI Engineering Internship
Run: cd day23/dashboard && python app.py
"""

import os
import sys
import time

from flask import Flask, jsonify, render_template, request
from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------------------------
# Add scripts folder to path so we can import task modules
# ---------------------------------------------------------------------------
SCRIPTS_DIR = os.path.join(os.path.dirname(__file__), "..", "scripts")
sys.path.insert(0, os.path.abspath(SCRIPTS_DIR))

# ---------------------------------------------------------------------------
# OFFLINE TOGGLE
# ---------------------------------------------------------------------------
USE_OFFLINE = True  # Change to False for real MiniLM embeddings

app = Flask(__name__)

# ---------------------------------------------------------------------------
# Shared embedder (created once)
# ---------------------------------------------------------------------------


def get_embeddings():
    """Return embedder based on USE_OFFLINE flag."""
    if USE_OFFLINE:
        from langchain.embeddings.base import Embeddings
        import numpy as np

        class DeterministicEmbedder(Embeddings):
            """Deterministic 384-dim embedder."""

            def _embed(self, text: str):
                rng = np.random.default_rng(
                    abs(hash(text)) % (2 ** 32)
                )
                vec = rng.random(384).astype(np.float32)
                vec /= np.linalg.norm(vec)
                return vec.tolist()

            def embed_documents(self, texts):
                return [self._embed(t) for t in texts]

            def embed_query(self, text):
                return self._embed(text)

        return DeterministicEmbedder()
    else:
        from langchain_huggingface import HuggingFaceEmbeddings
        return HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )


# ---------------------------------------------------------------------------
# Shared sample docs (same as task scripts)
# ---------------------------------------------------------------------------

SAMPLE_DOCS_CONTENT = {
    "ai_basics.txt": (
        "Artificial Intelligence (AI) is the simulation of human "
        "intelligence by machines. Machine learning is a subset of AI "
        "that enables systems to learn from data without being explicitly "
        "programmed. Deep learning uses neural networks with many layers "
        "to model complex patterns. Natural Language Processing (NLP) "
        "allows computers to understand and generate human language."
    ),
    "python_guide.txt": (
        "Python is a high-level, interpreted programming language known "
        "for its simplicity and readability. It supports multiple "
        "programming paradigms including procedural, object-oriented, "
        "and functional programming. Python has a rich ecosystem of "
        "libraries such as NumPy for numerical computing, Pandas for "
        "data manipulation, and Scikit-learn for machine learning. "
        "PEP 8 is the style guide for Python code."
    ),
    "rag_overview.txt": (
        "Retrieval-Augmented Generation (RAG) combines document "
        "retrieval with language model generation. A RAG pipeline first "
        "indexes documents into a vector store, then retrieves relevant "
        "chunks for a query, and finally passes them to an LLM to "
        "generate an answer. FAISS is a popular vector store for fast "
        "similarity search. RAG reduces hallucinations by grounding "
        "the LLM in retrieved context."
    ),
}


def build_base_store():
    """Build FAISS store from sample docs."""
    from langchain_core.documents import Document
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_community.vectorstores import FAISS

    emb = get_embeddings()
    docs = [
        Document(
            page_content=content,
            metadata={"source": fname, "type": "text"},
        )
        for fname, content in SAMPLE_DOCS_CONTENT.items()
    ]

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=400, chunk_overlap=60
    )
    chunks = splitter.split_documents(docs)
    store = FAISS.from_documents(chunks, emb)
    return store, len(docs), len(chunks)


def get_llm():
    """Return ChatGroq LLM."""
    from langchain_groq import ChatGroq
    return ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.1,
    )


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    """Render main dashboard."""
    return render_template("index.html")


# --- Task 1: Simple RAG ---

@app.route("/api/task1", methods=["POST"])
def task1_query():
    """Simple RAG: query -> answer + source chunks."""
    from langchain.chains.retrieval_qa.base import RetrievalQA
    from langchain_core.prompts import PromptTemplate

    data = request.get_json()
    query = data.get("query", "").strip()
    if not query:
        return jsonify({"error": "Query cannot be empty"}), 400

    try:
        start = time.perf_counter()
        store, doc_count, chunk_count = build_base_store()

        prompt = PromptTemplate(
            input_variables=["context", "question"],
            template=(
                "Use the context below to answer accurately.\n\n"
                "Context:\n{context}\n\n"
                "Question: {question}\n\nAnswer:"
            ),
        )

        chain = RetrievalQA.from_chain_type(
            llm=get_llm(),
            chain_type="stuff",
            retriever=store.as_retriever(
                search_kwargs={"k": 4}
            ),
            return_source_documents=True,
            chain_type_kwargs={"prompt": prompt},
        )

        response = chain.invoke({"query": query})
        latency = round(
            (time.perf_counter() - start) * 1000, 1
        )

        sources = [
            {
                "source": doc.metadata.get("source", "unknown"),
                "snippet": doc.page_content[:150] + "...",
            }
            for doc in response["source_documents"]
        ]

        return jsonify({
            "answer": response["result"],
            "sources": sources,
            "latency_ms": latency,
            "doc_count": doc_count,
            "chunk_count": chunk_count,
        })

    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


# --- Task 2: Enhanced RAG ---

@app.route("/api/task2", methods=["POST"])
def task2_query():
    """Enhanced RAG with strict or detailed prompt mode."""
    from langchain.chains.retrieval_qa.base import RetrievalQA
    from langchain_core.prompts import PromptTemplate

    data = request.get_json()
    query = data.get("query", "").strip()
    mode = data.get("mode", "strict")

    if not query:
        return jsonify({"error": "Query cannot be empty"}), 400

    if mode == "strict":
        template = (
            "Answer ONLY using the context below.\n"
            "If not in context, say: "
            "'I don't have that information in the provided "
            "context.'\n\n"
            "Context:\n{context}\n\n"
            "Question: {question}\n\nAnswer:"
        )
    else:
        template = (
            "Give a detailed answer using the context below.\n"
            "Mention which document the info came from.\n\n"
            "Context:\n{context}\n\n"
            "Question: {question}\n\nDetailed Answer:"
        )

    try:
        start = time.perf_counter()
        store, _, chunk_count = build_base_store()

        prompt = PromptTemplate(
            input_variables=["context", "question"],
            template=template,
        )

        chain = RetrievalQA.from_chain_type(
            llm=get_llm(),
            chain_type="stuff",
            retriever=store.as_retriever(
                search_kwargs={"k": 4}
            ),
            return_source_documents=True,
            chain_type_kwargs={"prompt": prompt},
        )

        response = chain.invoke({"query": query})
        latency = round(
            (time.perf_counter() - start) * 1000, 1
        )

        answer = response["result"]
        not_in_ctx = (
            "don't have" in answer.lower()
            or "not in" in answer.lower()
        )

        sources = list({
            doc.metadata.get("source", "unknown")
            for doc in response["source_documents"]
        })

        return jsonify({
            "answer": answer,
            "mode": mode,
            "sources": sources,
            "not_in_context": not_in_ctx,
            "latency_ms": latency,
            "chunk_count": chunk_count,
        })

    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


# --- Task 3: Multi-Doc RAG ---

MULTI_DOCS = {
    "pdf": {
        "ml_research.txt": (
            "Machine learning research has advanced significantly. "
            "Transformer architectures have revolutionized NLP tasks. "
            "BERT and GPT models use attention mechanisms. "
            "RLHF is used to align language models with human "
            "preferences. Transfer learning allows fine-tuning."
        ),
        "deep_learning.txt": (
            "Deep learning uses multiple layers of neural networks. "
            "CNNs excel at image recognition tasks. RNNs process "
            "sequential data. Batch normalization and dropout improve "
            "training stability. Gradient descent optimizes weights."
        ),
    },
    "website": {
        "langchain_docs.txt": (
            "LangChain is a framework for developing LLM applications. "
            "It supports FAISS, Chroma, and Pinecone vector stores. "
            "RetrievalQA combines retriever with LLM to answer "
            "questions. LangChain agents can use tools and APIs."
        ),
        "openai_blog.txt": (
            "GPT-4 demonstrates emergent capabilities. Chain-of-thought "
            "prompting helps solve complex reasoning tasks. Few-shot "
            "learning adapts models with few examples. Hallucination "
            "remains a key challenge in language models."
        ),
    },
    "text": {
        "python_ml.txt": (
            "Python is the dominant language for machine learning. "
            "TensorFlow and PyTorch provide neural network frameworks. "
            "Scikit-learn offers classical ML algorithms. Pandas and "
            "NumPy are essential for data manipulation."
        ),
        "mlops_guide.txt": (
            "MLOps combines ML with DevOps for model deployment. "
            "CI/CD pipelines automate model testing. Model versioning "
            "tracks changes to datasets and weights. Feature stores "
            "centralize features. Monitoring detects data drift."
        ),
    },
}


@app.route("/api/task3", methods=["POST"])
def task3_query():
    """Multi-doc RAG with optional source type filter."""
    from langchain_core.documents import Document
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_community.vectorstores import FAISS

    data = request.get_json()
    query = data.get("query", "").strip()
    source_filter = data.get("source_filter", "all")

    if not query:
        return jsonify({"error": "Query cannot be empty"}), 400

    try:
        start = time.perf_counter()
        emb = get_embeddings()

        all_docs = []
        for src_type, files in MULTI_DOCS.items():
            for fname, content in files.items():
                all_docs.append(Document(
                    page_content=content,
                    metadata={
                        "source": fname,
                        "source_type": src_type,
                    },
                ))

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=400, chunk_overlap=60
        )
        chunks = splitter.split_documents(all_docs)

        if source_filter != "all":
            chunks = [
                c for c in chunks
                if c.metadata.get("source_type") == source_filter
            ]

        if not chunks:
            return jsonify(
                {"error": f"No docs for filter: {source_filter}"}
            ), 400

        store = FAISS.from_documents(chunks, emb)
        retrieved = store.similarity_search(query, k=4)

        context = "\n\n".join([
            f"[{d.metadata.get('source_type', '').upper()}] "
            f"{d.metadata.get('source', '')}:\n{d.page_content}"
            for d in retrieved
        ])

        llm = get_llm()
        prompt_text = (
            f"Answer using these sources. Cite each one.\n\n"
            f"{context}\n\nQuestion: {query}\n\nAnswer:"
        )
        response = llm.invoke(prompt_text)
        latency = round(
            (time.perf_counter() - start) * 1000, 1
        )

        sources = [
            {
                "source": d.metadata.get("source", "unknown"),
                "source_type": d.metadata.get(
                    "source_type", "unknown"
                ),
                "relevance_score": round(
                    len(d.page_content) / 500, 2
                ),
                "snippet": d.page_content[:120] + "...",
            }
            for d in retrieved
        ]

        return jsonify({
            "answer": response.content,
            "sources": sources,
            "source_filter": source_filter,
            "chunk_count": len(chunks),
            "latency_ms": latency,
        })

    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 50)
    print("Day 23 RAG Dashboard")
    print("Visit: http://127.0.0.1:5000")
    print("=" * 50)
    app.run(debug=True, port=5000)