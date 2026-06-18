"""
task2_enhanced_rag.py
Day 23 - Task 2: Enhanced RAG with Custom Prompts
Xeven Solutions AI Engineering Internship
"""

import os
import time

from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# OFFLINE TOGGLE
# ---------------------------------------------------------------------------
USE_OFFLINE = True  # Change to False on your machine with .venv312

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
    from langchain_huggingface import HuggingFaceEmbeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    print("[ONLINE] Using all-MiniLM-L6-v2 via HuggingFaceEmbeddings")


# ---------------------------------------------------------------------------
# Sample documents (auto-created)
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

    print(f"[DOCS] Loaded {len(documents)} documents.")
    return documents


# ---------------------------------------------------------------------------
# Chunking
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
    print(f"[SPLIT] {len(documents)} docs -> {len(chunks)} chunks")
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
# Custom prompt template
# ---------------------------------------------------------------------------

STRICT_PROMPT_TEMPLATE = (
    "You are a precise assistant. Answer ONLY using the context below.\n"
    "If the answer is not in the context, respond with exactly:\n"
    "'I don't have that information in the provided context.'\n\n"
    "Context:\n{context}\n\n"
    "Question: {question}\n\n"
    "Answer:"
)

DETAILED_PROMPT_TEMPLATE = (
    "You are a helpful and detailed assistant.\n"
    "Use the context below to give a thorough answer.\n"
    "Always mention which document the information came from.\n\n"
    "Context:\n{context}\n\n"
    "Question: {question}\n\n"
    "Detailed Answer:"
)


# ---------------------------------------------------------------------------
# Build enhanced chain
# ---------------------------------------------------------------------------

def build_enhanced_chain(store, prompt_template: str):
    """Build RetrievalQA with a custom prompt."""
    from langchain.chains.retrieval_qa.base import RetrievalQA
    from langchain_core.prompts import PromptTemplate
    from langchain_groq import ChatGroq

    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=prompt_template,
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
        chain_type_kwargs={"prompt": prompt},
    )
    return chain


# ---------------------------------------------------------------------------
# Test cases
# ---------------------------------------------------------------------------

NORMAL_QUERIES = [
    "What is RAG and how does it reduce hallucinations?",
    "What programming paradigms does Python support?",
]

EDGE_CASE_QUERIES = [
    "What is the capital city of France?",
    "Who invented the telephone?",
    "What is the price of Bitcoin today?",
]


def run_normal_queries(chain) -> list:
    """Run normal queries with strict prompt."""
    results = []
    print("\n" + "=" * 60)
    print("NORMAL QUERIES (strict prompt)")
    print("=" * 60)

    for query in NORMAL_QUERIES:
        start = time.perf_counter()
        response = chain.invoke({"query": query})
        latency = (time.perf_counter() - start) * 1000

        answer = response["result"]
        sources = list({
            doc.metadata.get("source", "unknown")
            for doc in response["source_documents"]
        })

        results.append({
            "type": "normal",
            "query": query,
            "answer": answer,
            "sources": sources,
            "latency_ms": round(latency, 1),
        })

        print(f"\nQ: {query}")
        print(f"A: {answer}")
        print(f"Sources: {', '.join(sources)}")
        print(f"Latency: {latency:.1f} ms")

    return results


def run_edge_cases(chain) -> list:
    """Run edge case queries — expect 'not in context' responses."""
    results = []
    print("\n" + "=" * 60)
    print("EDGE CASE QUERIES (out-of-context test)")
    print("=" * 60)

    for query in EDGE_CASE_QUERIES:
        start = time.perf_counter()
        response = chain.invoke({"query": query})
        latency = (time.perf_counter() - start) * 1000

        answer = response["result"]
        not_in_ctx = (
            "don't have" in answer.lower()
            or "not in" in answer.lower()
            or "no information" in answer.lower()
        )

        results.append({
            "type": "edge_case",
            "query": query,
            "answer": answer,
            "not_in_context": not_in_ctx,
            "latency_ms": round(latency, 1),
        })

        status = "CORRECTLY REFUSED" if not_in_ctx else "ANSWERED (check)"
        print(f"\nQ: {query}")
        print(f"A: {answer}")
        print(f"Status: {status} | Latency: {latency:.1f} ms")

    return results


# ---------------------------------------------------------------------------
# Save results
# ---------------------------------------------------------------------------

def save_results(
    normal: list, edge: list, out_dir: str
) -> None:
    """Write all results to a report file."""
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "task2_results.txt")

    with open(path, "w", encoding="utf-8") as fh:
        fh.write("Day 23 - Task 2: Enhanced RAG Results\n")
        fh.write("=" * 60 + "\n\n")

        fh.write("NORMAL QUERIES\n")
        fh.write("-" * 40 + "\n")
        for res in normal:
            fh.write(f"Q: {res['query']}\n")
            fh.write(f"A: {res['answer']}\n")
            fh.write(f"Sources: {', '.join(res['sources'])}\n")
            fh.write(f"Latency: {res['latency_ms']} ms\n\n")

        fh.write("EDGE CASE QUERIES\n")
        fh.write("-" * 40 + "\n")
        for res in edge:
            refused = res["not_in_context"]
            fh.write(f"Q: {res['query']}\n")
            fh.write(f"A: {res['answer']}\n")
            fh.write(
                f"Correctly refused: {refused} | "
                f"Latency: {res['latency_ms']} ms\n\n"
            )

    print(f"\n[SAVED] Results written to {path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    """Run the Enhanced RAG pipeline."""
    print("\n" + "=" * 60)
    print("Day 23 - Task 2: Enhanced RAG with Custom Prompts")
    print("=" * 60)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    doc_dir = os.path.join(base_dir, "sample_docs")
    out_dir = os.path.join(base_dir, "outputs")
    os.makedirs(out_dir, exist_ok=True)

    # Pipeline
    documents = create_sample_documents(doc_dir)
    chunks = split_documents(documents)
    store = build_vector_store(chunks)

    # Two chains — strict and detailed
    strict_chain = build_enhanced_chain(store, STRICT_PROMPT_TEMPLATE)
    detailed_chain = build_enhanced_chain(
        store, DETAILED_PROMPT_TEMPLATE
    )

    # Run queries
    normal_results = run_normal_queries(detailed_chain)
    edge_results = run_edge_cases(strict_chain)
    save_results(normal_results, edge_results, out_dir)

    # Summary
    refused = sum(
        1 for r in edge_results if r["not_in_context"]
    )
    all_latencies = (
        [r["latency_ms"] for r in normal_results]
        + [r["latency_ms"] for r in edge_results]
    )
    avg_lat = sum(all_latencies) / len(all_latencies)

    print("\n[SUMMARY]")
    print(f"  Normal queries   : {len(normal_results)}")
    print(f"  Edge case queries: {len(edge_results)}")
    print(
        f"  Correctly refused: {refused}/{len(edge_results)}"
    )
    print(f"  Avg latency      : {avg_lat:.1f} ms")
    print("\n[DONE] Task 2 complete.")


if __name__ == "__main__":
    main()