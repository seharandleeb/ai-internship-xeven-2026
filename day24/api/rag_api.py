"""Day 24 - Task 3: RAG API endpoint.

Wraps the conversational RAG system in a FastAPI service. The heavy
objects (embedder, FAISS index, Groq LLM) are built once at startup
via a lifespan handler and reused for every request. Run with:
    uvicorn rag_api:app --reload
from inside the day24/api/ folder, with the .venv312 environment.
"""

import os
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# The RAG modules live in day24/scripts/, one folder up then into
# scripts. Add that folder to the import path so we can import them.
SCRIPTS_DIR = os.path.join(os.path.dirname(__file__), "..", "scripts")
sys.path.insert(0, os.path.abspath(SCRIPTS_DIR))

from conversation_memory import ConversationMemory  # noqa: E402
from conversational_rag import (  # noqa: E402
    build_llm,
    chat_turn,
)
from rag_core import (  # noqa: E402
    DeterministicEmbedder,
    SAMPLE_DOCS,
    build_vector_store,
)

STATE = {}


@asynccontextmanager
async def lifespan(app):
    """Build heavy objects once at startup, clean up at shutdown."""
    embedder = DeterministicEmbedder()
    index, docs = build_vector_store(SAMPLE_DOCS, embedder)
    STATE["embedder"] = embedder
    STATE["index"] = index
    STATE["docs"] = docs
    STATE["llm"] = build_llm()
    STATE["memory"] = ConversationMemory()
    print("RAG system ready:", index.ntotal, "documents indexed.")
    yield
    STATE.clear()


app = FastAPI(title="Day 24 RAG API", version="0.1.0", lifespan=lifespan)


class Question(BaseModel):
    """Shape of an /ask request body."""

    question: str


@app.get("/health")
def health():
    """Report that the service is running."""
    return {"status": "ok"}


@app.post("/ask")
def ask(payload: Question):
    """Answer a question using the RAG system with memory."""
    question = payload.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question is empty.")

    try:
        answer, results = chat_turn(
            question,
            STATE["index"],
            STATE["docs"],
            STATE["embedder"],
            STATE["llm"],
            STATE["memory"],
        )
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(
            status_code=500, detail=f"LLM error: {exc}"
        )

    if not results:
        raise HTTPException(
            status_code=404, detail="No relevant documents found."
        )

    sources = [doc for _score, doc in results]
    confidence = round(results[0][0], 3)
    return {
        "answer": answer,
        "sources": sources,
        "confidence": confidence,
    }