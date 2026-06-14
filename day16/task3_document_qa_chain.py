"""Day 16 - Task 3: Document Q&A chain.

Loads a document in any supported format, joins its pages into a single
context string, and answers questions about it with an LCEL chain:

    load_doc -> format_prompt -> model -> parse_answer

A simple character budget guards against overrunning the model's context
window: oversized documents are truncated and the user is warned.
"""

import os

from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

# Reuse the Task 2 loaders so the Q&A chain is format-agnostic.
from task2_document_loaders import SAMPLE_TXT, create_sample_files, load_any

MODEL_NAME = "llama-3.3-70b-versatile"

# Rough guard. ~4 chars/token, leaving headroom for the prompt and answer.
MAX_CONTEXT_CHARS = 24_000


def build_model(temperature: float = 0.2) -> ChatGroq:
    """Create the ChatGroq model, ensuring the API key is present."""
    load_dotenv()
    if not os.getenv("GROQ_API_KEY"):
        raise RuntimeError(
            "GROQ_API_KEY is not set. Add it to a .env file:\n"
            "    GROQ_API_KEY=your_key_here"
        )
    return ChatGroq(model=MODEL_NAME, temperature=temperature)


def documents_to_context(docs: list[Document]) -> str:
    """Join Documents into one context string, truncating if too long.

    Args:
        docs: Loaded documents.

    Returns:
        A single context string, truncated to ``MAX_CONTEXT_CHARS``.
    """
    full_text = "\n\n".join(doc.page_content for doc in docs)
    if len(full_text) > MAX_CONTEXT_CHARS:
        print(
            f"[warn] Document is {len(full_text):,} chars; truncating to "
            f"{MAX_CONTEXT_CHARS:,} to respect the context limit."
        )
        full_text = full_text[:MAX_CONTEXT_CHARS]
    return full_text


def build_qa_chain(model: ChatGroq):
    """Build the document Q&A LCEL chain.

    Returns:
        A runnable accepting ``{"context": ..., "question": ...}``.
    """
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You answer strictly from the provided document. "
                "If the answer is not in the document, say so plainly.",
            ),
            (
                "human",
                "Document:\n{context}\n\nQuestion: {question}",
            ),
        ]
    )
    return prompt | model | StrOutputParser()


def answer_questions(source: str, questions: list[str]) -> None:
    """Load a document and answer a list of questions about it.

    Args:
        source: Path or URL accepted by ``load_any``.
        questions: Questions to ask about the document.
    """
    docs = load_any(source)
    context = documents_to_context(docs)
    chain = build_qa_chain(build_model())

    for question in questions:
        print(f"Q: {question}")
        answer = chain.invoke({"context": context, "question": question})
        print(f"A: {answer}\n")


def main() -> None:
    """Run the Q&A chain against the auto-created sample text file."""
    print("=== Task 3: Document Q&A Chain ===\n")
    create_sample_files()
    answer_questions(
        SAMPLE_TXT,
        [
            "Summarize this document in one sentence.",
            "What are the key points?",
            "Does this document mention pricing?",
        ],
    )


if __name__ == "__main__":
    main()
