"""
task1_simple_rag.py
Day 23 — Task 1: Simple RAG Pipeline
Xeven Solutions AI Engineering Internship
"""

import os
import time

from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# OFFLINE TOGGLE — set True in sandbox / False on your machine with .venv312
# ---------------------------------------------------------------------------
USE_OFFLINE = True  # Change to False on your machine

load_dotenv()

# ---------------------------------------------------------------------------
# Embeddings
# ---------------------------------------------------------------------------

if USE_OFFLINE:
    from langchain.embeddings.base import Embeddings
    import numpy as np

    class DeterministicEmbedder(Embeddings):
        """Deterministic 384-dim embedder for offline testing."""

        def _embed(self, text: str):
            rng = np.random.default_rng(abs(hash(text)) % (2 ** 32))
            vec = rng.random(384).astype(np.float32)
            vec /= np.linalg.norm(vec)
            return vec.tolist()

        def embed_documents(self, texts):
            return [self._embed(t) for t in texts]

        def embed_query(self, text):
            return self._embed(text)

    embeddings = DeterministicEmbedder()
    print("[OFFLINE] Using DeterministicEmbedder (384-dim)")

else:
    from langchain_community.embeddings import HuggingFaceEmbeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    print("[ONLINE] Using all-MiniLM-L6-v2 via HuggingFaceEmbeddings")


# ---------------------------------------------------------------------------
# Auto-create sample documents
# ---------------------------------------------------------------------------

SAMPLE_DOCS = {
    "ai_basics.txt": (
        "Artificial Intelligence (AI) is the simulation of human "
        "intelligence by machines. Machine learning is a subset of AI "
        "that enables systems to learn from data without being explicitly "
        "programmed. Deep learning uses neural networks with many layers "
        "to model complex patterns. Natural Language Processing (NLP) "
        "allows computers to understand and generate human language. "
        "Computer vision enables machines to interpret visual information "
        "from images and videos."
    ),
    "python_guide.txt": (
        "Python is a high-level, interpreted programming language known "
        "for its simplicity and readability. It supports multiple "
        "programming paradigms including procedural, object-oriented, "
        "and functional programming. Python has a rich ecosystem of "
        "libraries such as NumPy for numerical computing, Pandas for "
        "data manipulation, and Scikit-learn for machine learning. "
        "Virtual environments help manage project dependencies in "
        "Python. PEP 8 is the style guide for Python code."
    ),
    "rag_overview.txt": (
        "Retrieval-Augmented Generation (RAG) combines document "
        "retrieval with language model generation. A RAG pipeline first "
        "indexes documents into a vector store, then retrieves relevant "
        "chunks for a query, and finally passes them to an LLM to "
        "generate an answer. FAISS is a popular vector store for fast "
        "similarity search. Sentence transformers convert text into "
        "dense vector embeddings. RAG reduces hallucinations by "
        "grounding the LLM in retrieved context."
    ),
}


def create_sample_documents(doc_dir: str) -> list:
    """Write sample docs to disk and return LangChain Document objects."""
    from langchain_core.documents import Document

    os.makedirs(doc_dir, exist_ok=True)
    documents = []

    for filename, content in SAMPLE_DOCS.items():
        filepath = os.path.join(doc_dir, filename)
        if not os.path.exists(filepath):
            with open(filepath, "w", encoding="utf-8") as fh:
                fh.write(content)

        documents.append(
            Document(
                page_content=content,
                metadata={"source": filename, "type": "text"},
            )
        )

    print(f"[DOCS] Created/loaded {len(documents)} sample documents.")
    return documents


# ---------------------------------------------------------------------------
# Text splitter
# ---------------------------------------------------------------------------

def split_documents(documents: list) -> list:
    """Chunk documents with RecursiveCharacterTextSplitter."""
    from langchain_text_splitters import RecursiveCharacterTextSplitter

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,
        chunk_overlap=60,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks = splitter.split_documents(documents)
    print(
        f"[SPLIT] {len(documents)} docs -> {len(chunks)} chunks "
        f"(size=400, overlap=60)"
    )
    return chunks


# ---------------------------------------------------------------------------
# FAISS vector store
# ---------------------------------------------------------------------------

def build_vector_store(chunks: list):
    """Embed chunks and store in FAISS."""
    from langchain_community.vectorstores import FAISS

    start = time.perf_counter()
    store = FAISS.from_documents(chunks, embeddings)
    elapsed = (time.perf_counter() - start) * 1000

    print(f"[FAISS] Indexed {len(chunks)} chunks in {elapsed:.1f} ms")
    return store


# ---------------------------------------------------------------------------
# RAG chain
# ---------------------------------------------------------------------------

def build_rag_chain(store):
    """Build RetrievalQA chain with source attribution."""
    from langchain.chains.retrieval_qa.base import RetrievalQA
    from langchain_core.prompts import PromptTemplate
    from langchain_groq import ChatGroq

    prompt_template = PromptTemplate(
        input_variables=["context", "question"],
        template=(
            "You are a helpful assistant. Use the context below to answer "
            "the question accurately and concisely.\n\n"
            "Context:\n{context}\n\n"
            "Question: {question}\n\n"
            "Answer:"
        ),
    )

    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.1,
    )

    retriever = store.as_retriever(search_kwargs={"k": 4})

    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt_template},
    )

    return chain


# ---------------------------------------------------------------------------
# Run queries
# ---------------------------------------------------------------------------

TEST_QUERIES = [
    "What is Retrieval-Augmented Generation?",
    "What is PEP 8 in Python?",
    "How does deep learning work?",
]


def run_queries(chain) -> list:
    """Run test queries and return results with latency."""
    results = []

    for query in TEST_QUERIES:
        start = time.perf_counter()
        response = chain.invoke({"query": query})
        latency = (time.perf_counter() - start) * 1000

        answer = response["result"]
        sources = [
            doc.metadata.get("source", "unknown")
            for doc in response["source_documents"]
        ]

        results.append({
            "query": query,
            "answer": answer,
            "sources": sources,
            "latency_ms": round(latency, 1),
        })

        print(f"\n{'=' * 60}")
        print(f"Q: {query}")
        print(f"A: {answer}")
        print(f"Sources: {', '.join(set(sources))}")
        print(f"Latency: {latency:.1f} ms")

    return results


# ---------------------------------------------------------------------------
# Save results
# ---------------------------------------------------------------------------

def save_results(results: list, out_dir: str) -> None:
    """Write query results to a text report."""
    os.makedirs(out_dir, exist_ok=True)
    report_path = os.path.join(out_dir, "task1_results.txt")

    with open(report_path, "w", encoding="utf-8") as fh:
        fh.write("Day 23 - Task 1: Simple RAG Pipeline Results\n")
        fh.write("=" * 60 + "\n\n")

        for i, res in enumerate(results, 1):
            fh.write(f"Query {i}: {res['query']}\n")
            fh.write(f"Answer: {res['answer']}\n")
            fh.write(f"Sources: {', '.join(set(res['sources']))}\n")
            fh.write(f"Latency: {res['latency_ms']} ms\n")
            fh.write("-" * 40 + "\n\n")

    print(f"\n[SAVED] Results written to {report_path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    """Run the full Simple RAG pipeline."""
    print("\n" + "=" * 60)
    print("Day 23 - Task 1: Simple RAG Pipeline")
    print("=" * 60)

    # Paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    doc_dir = os.path.join(base_dir, "sample_docs")
    out_dir = os.path.join(base_dir, "outputs")
    os.makedirs(out_dir, exist_ok=True)

    # Pipeline
    documents = create_sample_documents(doc_dir)
    chunks = split_documents(documents)
    store = build_vector_store(chunks)
    chain = build_rag_chain(store)
    results = run_queries(chain)
    save_results(results, out_dir)

    # Summary
    avg_latency = sum(r["latency_ms"] for r in results) / len(results)
    print("\n[SUMMARY]")
    print(f"  Documents  : {len(documents)}")
    print(f"  Chunks     : {len(chunks)}")
    print(f"  Queries    : {len(results)}")
    print(f"  Avg latency: {avg_latency:.1f} ms")
    print("\n[DONE] Task 1 complete.")


if __name__ == "__main__":
    main()
