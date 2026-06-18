"""
task3_multi_doc_rag.py
Day 23 - Task 3: Multi-Document RAG System
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
# Multi-source document definitions (auto-created)
# ---------------------------------------------------------------------------

MULTI_SOURCE_DOCS = {
    "pdf": {
        "ml_research.txt": (
            "Machine learning research has advanced significantly in recent "
            "years. Transformer architectures have revolutionized natural "
            "language processing tasks. BERT and GPT models use attention "
            "mechanisms to understand context in text. Reinforcement learning "
            "from human feedback (RLHF) is used to align language models "
            "with human preferences. Transfer learning allows models trained "
            "on large datasets to be fine-tuned for specific tasks."
        ),
        "deep_learning.txt": (
            "Deep learning uses multiple layers of neural networks to learn "
            "hierarchical representations of data. Convolutional neural "
            "networks (CNNs) excel at image recognition tasks. Recurrent "
            "neural networks (RNNs) process sequential data like time series "
            "and text. Batch normalization and dropout are techniques used "
            "to improve training stability and prevent overfitting. "
            "Gradient descent optimizes model weights during training."
        ),
    },
    "website": {
        "langchain_docs.txt": (
            "LangChain is a framework for developing applications powered "
            "by language models. It provides tools for chaining together "
            "different components like prompts, models, and output parsers. "
            "LangChain supports various vector stores including FAISS, "
            "Chroma, and Pinecone. The RetrievalQA chain combines a "
            "retriever with an LLM to answer questions from documents. "
            "LangChain agents can use tools to interact with external APIs."
        ),
        "openai_blog.txt": (
            "Large language models like GPT-4 demonstrate emergent "
            "capabilities not seen in smaller models. Chain-of-thought "
            "prompting helps models solve complex reasoning tasks step by "
            "step. Few-shot learning allows models to adapt to new tasks "
            "with only a few examples. Prompt engineering is the practice "
            "of designing inputs to get desired outputs from language "
            "models. Hallucination remains a key challenge where models "
            "generate plausible but incorrect information."
        ),
    },
    "text": {
        "python_ml.txt": (
            "Python is the dominant language for machine learning and "
            "data science. Libraries like TensorFlow and PyTorch provide "
            "frameworks for building and training neural networks. Scikit-"
            "learn offers classical machine learning algorithms including "
            "decision trees, random forests, and support vector machines. "
            "Pandas and NumPy are essential for data manipulation and "
            "numerical computing. Jupyter notebooks are widely used for "
            "interactive data exploration and model prototyping."
        ),
        "mlops_guide.txt": (
            "MLOps combines machine learning with DevOps practices to "
            "streamline model deployment and monitoring. Continuous "
            "integration and deployment pipelines automate model testing "
            "and release. Model versioning tracks changes to datasets, "
            "code, and model weights over time. Feature stores centralize "
            "and manage features used across different models. Model "
            "monitoring detects data drift and performance degradation "
            "in production systems."
        ),
    },
}


# ---------------------------------------------------------------------------
# Create documents with metadata
# ---------------------------------------------------------------------------

def create_multi_source_documents(doc_dir: str) -> list:
    """Create docs from multiple sources with metadata tags."""
    from langchain_core.documents import Document
    from datetime import datetime

    os.makedirs(doc_dir, exist_ok=True)
    all_documents = []
    today = datetime.now().strftime("%Y-%m-%d")

    for source_type, files in MULTI_SOURCE_DOCS.items():
        type_dir = os.path.join(doc_dir, source_type)
        os.makedirs(type_dir, exist_ok=True)

        for filename, content in files.items():
            filepath = os.path.join(type_dir, filename)
            if not os.path.exists(filepath):
                with open(filepath, "w", encoding="utf-8") as fh:
                    fh.write(content)

            all_documents.append(
                Document(
                    page_content=content,
                    metadata={
                        "source": filename,
                        "source_type": source_type,
                        "domain": filename.replace(".txt", ""),
                        "date": today,
                    },
                )
            )

    counts = {}
    for doc in all_documents:
        st = doc.metadata["source_type"]
        counts[st] = counts.get(st, 0) + 1

    print(f"[DOCS] Loaded {len(all_documents)} documents:")
    for src_type, count in counts.items():
        print(f"       {src_type}: {count} docs")

    return all_documents


# ---------------------------------------------------------------------------
# Chunking
# ---------------------------------------------------------------------------

def split_documents(documents: list) -> list:
    """Chunk documents preserving metadata."""
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
    """Embed all chunks into one FAISS store."""
    from langchain_community.vectorstores import FAISS

    start = time.perf_counter()
    store = FAISS.from_documents(chunks, embeddings)
    elapsed = (time.perf_counter() - start) * 1000
    print(f"[FAISS] Indexed {len(chunks)} chunks in {elapsed:.1f} ms")
    return store


# ---------------------------------------------------------------------------
# Filtered retrieval by source_type
# ---------------------------------------------------------------------------

def get_filtered_chunks(
    chunks: list, source_type: str
) -> list:
    """Filter chunks by source_type metadata."""
    filtered = [
        c for c in chunks
        if c.metadata.get("source_type") == source_type
    ]
    return filtered


def build_filtered_store(chunks: list, source_type: str):
    """Build FAISS store from filtered chunks only."""
    from langchain_community.vectorstores import FAISS

    filtered = get_filtered_chunks(chunks, source_type)
    if not filtered:
        return None
    store = FAISS.from_documents(filtered, embeddings)
    return store


# ---------------------------------------------------------------------------
# RAG chain
# ---------------------------------------------------------------------------

def build_chain(store, source_label: str):
    """Build RetrievalQA chain for a given store."""
    from langchain_groq import ChatGroq
    from langchain_core.prompts import PromptTemplate

    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=(
            f"You are answering from {source_label} sources.\n"
            "Use ONLY the context below. Include source names.\n"
            "If not in context, say: "
            "'I don't have that information.'\n\n"
            "Context:\n{context}\n\n"
            "Question: {question}\n\n"
            "Answer (with sources):"
        ),
    )

    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.1,
    )

    retriever = store.as_retriever(search_kwargs={"k": 4})
    from langchain.chains.retrieval_qa.base import RetrievalQA

    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt},
    )
    return chain


# ---------------------------------------------------------------------------
# Multi-source synthesis
# ---------------------------------------------------------------------------

def synthesize_answer(
    store, query: str, chunks: list
) -> dict:
    """Query all sources and combine results with scores."""
    from langchain_groq import ChatGroq

    start = time.perf_counter()

    # Get results per source type
    source_results = {}
    for source_type in MULTI_SOURCE_DOCS.keys():
        filtered_store = build_filtered_store(chunks, source_type)
        if filtered_store is None:
            continue
        docs = filtered_store.similarity_search(query, k=2)
        if docs:
            source_results[source_type] = docs

    # Build combined context
    context_parts = []
    all_sources = []
    for source_type, docs in source_results.items():
        for doc in docs:
            src = doc.metadata.get("source", "unknown")
            context_parts.append(
                f"[{source_type.upper()}] {src}:\n"
                f"{doc.page_content}"
            )
            all_sources.append({
                "source": src,
                "source_type": source_type,
                "relevance_score": round(
                    len(doc.page_content) / 500, 2
                ),
            })

    combined_context = "\n\n".join(context_parts)

    # Final synthesis with LLM
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.1,
    )

    synthesis_prompt = (
        "Synthesize a comprehensive answer from multiple sources below.\n"
        "Mention which source each piece of information comes from.\n\n"
        f"Sources:\n{combined_context}\n\n"
        f"Question: {query}\n\n"
        "Synthesized Answer:"
    )

    response = llm.invoke(synthesis_prompt)
    latency = (time.perf_counter() - start) * 1000

    return {
        "query": query,
        "answer": response.content,
        "sources": all_sources,
        "latency_ms": round(latency, 1),
    }


# ---------------------------------------------------------------------------
# Test queries
# ---------------------------------------------------------------------------

FILTER_QUERIES = [
    ("What are transformer architectures?", "pdf"),
    ("What does LangChain support?", "website"),
    ("What is MLOps?", "text"),
]

SYNTHESIS_QUERIES = [
    "How do neural networks relate to Python libraries?",
    "What are the key challenges in deploying language models?",
]


def run_filtered_queries(chunks: list) -> list:
    """Run source-filtered queries."""
    results = []
    print("\n" + "=" * 60)
    print("FILTERED RETRIEVAL (by source type)")
    print("=" * 60)

    for query, source_type in FILTER_QUERIES:
        filtered_store = build_filtered_store(chunks, source_type)
        if filtered_store is None:
            print(f"\n[SKIP] No docs for source_type={source_type}")
            continue

        chain = build_chain(filtered_store, source_type)

        start = time.perf_counter()
        response = chain.invoke({"query": query})
        latency = (time.perf_counter() - start) * 1000

        answer = response["result"]
        sources = list({
            doc.metadata.get("source", "unknown")
            for doc in response["source_documents"]
        })

        results.append({
            "query": query,
            "filter": source_type,
            "answer": answer,
            "sources": sources,
            "latency_ms": round(latency, 1),
        })

        print(f"\nQ: {query}")
        print(f"Filter: {source_type}")
        print(f"A: {answer[:200]}...")
        print(f"Sources: {', '.join(sources)}")
        print(f"Latency: {latency:.1f} ms")

    return results


def run_synthesis_queries(
    store, chunks: list
) -> list:
    """Run multi-source synthesis queries."""
    results = []
    print("\n" + "=" * 60)
    print("MULTI-SOURCE SYNTHESIS")
    print("=" * 60)

    for query in SYNTHESIS_QUERIES:
        result = synthesize_answer(store, query, chunks)
        results.append(result)

        print(f"\nQ: {query}")
        print(f"A: {result['answer'][:200]}...")
        print("Sources with relevance scores:")
        for src in result["sources"]:
            print(
                f"  [{src['source_type']}] "
                f"{src['source']} "
                f"(score: {src['relevance_score']})"
            )
        print(f"Latency: {result['latency_ms']} ms")

    return results


# ---------------------------------------------------------------------------
# Save results
# ---------------------------------------------------------------------------

def save_results(
    filtered: list, synthesis: list, out_dir: str
) -> None:
    """Write results to report file."""
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "task3_results.txt")

    with open(path, "w", encoding="utf-8") as fh:
        fh.write("Day 23 - Task 3: Multi-Document RAG Results\n")
        fh.write("=" * 60 + "\n\n")

        fh.write("FILTERED RETRIEVAL\n")
        fh.write("-" * 40 + "\n")
        for res in filtered:
            fh.write(f"Q: {res['query']}\n")
            fh.write(f"Filter: {res['filter']}\n")
            fh.write(f"A: {res['answer']}\n")
            fh.write(f"Sources: {', '.join(res['sources'])}\n")
            fh.write(f"Latency: {res['latency_ms']} ms\n\n")

        fh.write("SYNTHESIS QUERIES\n")
        fh.write("-" * 40 + "\n")
        for res in synthesis:
            fh.write(f"Q: {res['query']}\n")
            fh.write(f"A: {res['answer']}\n")
            fh.write("Sources:\n")
            for src in res["sources"]:
                fh.write(
                    f"  [{src['source_type']}] "
                    f"{src['source']} "
                    f"score={src['relevance_score']}\n"
                )
            fh.write(f"Latency: {res['latency_ms']} ms\n\n")

    print(f"\n[SAVED] Results written to {path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    """Run the Multi-Document RAG pipeline."""
    print("\n" + "=" * 60)
    print("Day 23 - Task 3: Multi-Document RAG System")
    print("=" * 60)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    doc_dir = os.path.join(base_dir, "sample_docs", "multi")
    out_dir = os.path.join(base_dir, "outputs")
    os.makedirs(out_dir, exist_ok=True)

    # Pipeline
    documents = create_multi_source_documents(doc_dir)
    chunks = split_documents(documents)
    store = build_vector_store(chunks)

    # Queries
    filtered_results = run_filtered_queries(chunks)
    synthesis_results = run_synthesis_queries(store, chunks)
    save_results(filtered_results, synthesis_results, out_dir)

    # Summary
    all_lat = (
        [r["latency_ms"] for r in filtered_results]
        + [r["latency_ms"] for r in synthesis_results]
    )
    avg_lat = sum(all_lat) / len(all_lat) if all_lat else 0

    print("\n[SUMMARY]")
    print(f"  Total documents  : {len(documents)}")
    print(f"  Total chunks     : {len(chunks)}")
    print(f"  Source types     : {len(MULTI_SOURCE_DOCS)}")
    print(f"  Filtered queries : {len(filtered_results)}")
    print(f"  Synthesis queries: {len(synthesis_results)}")
    print(f"  Avg latency      : {avg_lat:.1f} ms")
    print("\n[DONE] Task 3 complete.")


if __name__ == "__main__":
    main()