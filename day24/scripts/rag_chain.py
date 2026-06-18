"""Day 24 - RAG answer layer: retrieval + Groq LLM (no memory yet).

Loads the Groq API key from a local .env file, retrieves context with
the offline core, and asks llama-3.3-70b-versatile to answer using only
that context.
"""

import os

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

from rag_core import (
    DeterministicEmbedder,
    SAMPLE_DOCS,
    build_vector_store,
    retrieve,
)

GROQ_MODEL = "llama-3.3-70b-versatile"

PROMPT_TEMPLATE = """You are a helpful assistant. Answer the question \
using ONLY the context below. If the answer is not in the context, \
say you do not know.

Context:
{context}

Question: {question}

Answer:"""


def build_llm():
    """Create the ChatGroq model from the GROQ_API_KEY in .env."""
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY not found. Add it to your .env file."
        )
    return ChatGroq(model=GROQ_MODEL, api_key=api_key, temperature=0)


def format_context(results):
    """Turn (score, doc) pairs into a numbered context block."""
    lines = []
    for i, (_score, doc) in enumerate(results, start=1):
        lines.append(f"[{i}] {doc}")
    return "\n".join(lines)


def answer_question(question, index, docs, embedder, llm):
    """Retrieve context, then generate a grounded answer."""
    results = retrieve(question, index, docs, embedder, k=3)
    context = format_context(results)

    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    chain = prompt | llm | StrOutputParser()
    answer = chain.invoke({"context": context, "question": question})
    return answer, results


def main():
    """Smoke test: build everything and answer one question."""
    embedder = DeterministicEmbedder()
    index, docs = build_vector_store(SAMPLE_DOCS, embedder)
    llm = build_llm()
    print("Model:", GROQ_MODEL)
    print("Documents indexed:", index.ntotal)

    question = "How do I stop my model from overfitting?"
    answer, results = answer_question(
        question, index, docs, embedder, llm
    )
    print("\nQuestion:", question)
    print("\nAnswer:\n", answer)
    print("\nTop sources:")
    for score, doc in results:
        print(f"  score={score:.3f}  {doc[:60]}...")


if __name__ == "__main__":
    main()