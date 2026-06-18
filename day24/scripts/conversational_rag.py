"""Day 24 - Task 1: Conversational RAG with memory.

Combines the offline retriever, the Groq LLM, and the modern
message-list memory so that follow-up questions keep their context.
Old exchanges beyond the recent window are summarized by Groq.
"""

import os

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

from conversation_memory import ConversationMemory
from rag_core import (
    DeterministicEmbedder,
    SAMPLE_DOCS,
    build_vector_store,
    retrieve,
)

GROQ_MODEL = "llama-3.3-70b-versatile"

ANSWER_TEMPLATE = """You are a helpful assistant. Use the conversation \
history to understand follow-up questions, and answer using ONLY the \
context below. If the answer is not in the context, say you do not know.

{history}

Context:
{context}

Question: {question}

Answer:"""

SUMMARY_TEMPLATE = """Summarize the following conversation exchanges \
into a short paragraph that preserves key facts and topics. Combine it \
with the existing summary if one is given.

Existing summary:
{summary}

Exchanges to add:
{exchanges}

Updated summary:"""


def build_llm():
    """Create the ChatGroq model from the GROQ_API_KEY in .env."""
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY not found. Add it to your .env file."
        )
    return ChatGroq(model=GROQ_MODEL, api_key=api_key, temperature=0)


def make_summarizer(llm):
    """Return a summarizer(old_summary, pairs) backed by Groq."""
    prompt = ChatPromptTemplate.from_template(SUMMARY_TEMPLATE)
    chain = prompt | llm | StrOutputParser()

    def summarizer(old_summary, pairs):
        exchanges = "\n".join(
            f"User: {q}\nAssistant: {a}" for q, a in pairs
        )
        return chain.invoke(
            {"summary": old_summary or "(none)", "exchanges": exchanges}
        ).strip()

    return summarizer


def format_context(results):
    """Turn (score, doc) pairs into a numbered context block."""
    return "\n".join(
        f"[{i}] {doc}" for i, (_s, doc) in enumerate(results, start=1)
    )


def chat_turn(question, index, docs, embedder, llm, memory):
    """Answer one question with history, then record and prune."""
    results = retrieve(question, index, docs, embedder, k=3)
    context = format_context(results)
    history = memory.as_context() or "(no prior conversation)"

    prompt = ChatPromptTemplate.from_template(ANSWER_TEMPLATE)
    chain = prompt | llm | StrOutputParser()
    answer = chain.invoke(
        {"history": history, "context": context, "question": question}
    ).strip()

    memory.add(question, answer)
    if memory.needs_pruning():
        memory.prune(make_summarizer(llm))
    return answer, results


def main():
    """Run a short scripted conversation to prove follow-ups work."""
    embedder = DeterministicEmbedder()
    index, docs = build_vector_store(SAMPLE_DOCS, embedder)
    llm = build_llm()
    memory = ConversationMemory()

    questions = [
        "What is overfitting?",
        "How do I prevent it?",
        "What is a transformer?",
    ]
    for turn, question in enumerate(questions, start=1):
        answer, _results = chat_turn(
            question, index, docs, embedder, llm, memory
        )
        print(f"\n=== Turn {turn} ===")
        print("Q:", question)
        print("A:", answer)

    print("\n--- Memory state after conversation ---")
    print("Exchanges kept verbatim:", len(memory.recent))
    print("Summary:", memory.summary or "(empty)")


if __name__ == "__main__":
    main()