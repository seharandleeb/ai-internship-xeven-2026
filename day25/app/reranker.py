"""ScholarRAG - LLM reranking via Groq.

Takes a wider candidate pool from the hybrid retriever and asks the
LLM to score every candidate's relevance to the question in a single
JSON call (one call total, not one per candidate). A defensive parser
handles the messy ways LLMs sometimes wrap JSON output: code fences,
leading prose, or trailing commentary.
"""

import json
import os
import re

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq

load_dotenv()

MODEL_NAME = "llama-3.3-70b-versatile"

RERANK_SYSTEM = (
    "You are a relevance-scoring assistant for a research-paper search "
    "engine. You will be given a question and a numbered list of text "
    "passages. Score each passage's relevance to the question from 0 "
    "(irrelevant) to 10 (directly answers the question). "
    "Respond with ONLY a JSON array of integers, one score per passage, "
    "in the same order as the passages. No other text."
)


def build_llm():
    """Construct the Groq chat model used for reranking."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY not found. Check your .env file.")
    return ChatGroq(model=MODEL_NAME, temperature=0, api_key=api_key)


def parse_scores(raw_text, expected_count):
    """Defensively pull a JSON array of numbers out of an LLM reply.

    Handles: clean JSON, JSON wrapped in ```json fences, JSON with
    leading/trailing prose, and falls back to all-zero scores if
    nothing usable is found at all.
    """
    text = raw_text.strip()
    text = re.sub(r"^```(json)?", "", text).strip()
    text = re.sub(r"```$", "", text).strip()

    match = re.search(r"\[.*\]", text, re.DOTALL)
    candidate = match.group(0) if match else text

    try:
        scores = json.loads(candidate)
    except (json.JSONDecodeError, TypeError):
        return [0.0] * expected_count

    if not isinstance(scores, list):
        return [0.0] * expected_count

    cleaned = []
    for value in scores:
        try:
            cleaned.append(float(value))
        except (TypeError, ValueError):
            cleaned.append(0.0)

    if len(cleaned) < expected_count:
        cleaned.extend([0.0] * (expected_count - len(cleaned)))
    return cleaned[:expected_count]


def retrieve_then_rerank(query, candidates, llm, top_k=5):
    """Score every candidate's relevance in one LLM call, keep top_k.

    candidates: chunk dicts already retrieved by the hybrid retriever,
    each with a "text" field.
    """
    if not candidates:
        return []

    numbered = "\n\n".join(
        "[{0}] {1}".format(i + 1, chunk["text"])
        for i, chunk in enumerate(candidates)
    )
    prompt = "Question: {0}\n\nPassages:\n{1}".format(query, numbered)

    messages = [
        SystemMessage(content=RERANK_SYSTEM),
        HumanMessage(content=prompt),
    ]
    response = llm.invoke(messages)
    scores = parse_scores(response.content, len(candidates))

    scored = []
    for chunk, score in zip(candidates, scores):
        item = dict(chunk)
        item["rerank_score"] = score
        scored.append(item)

    scored.sort(key=lambda c: c["rerank_score"], reverse=True)
    return scored[:top_k]


if __name__ == "__main__":
    demo_candidates = [
        {"chunk_id": "1", "text": "The Eiffel Tower is in Paris, France."},
        {
            "chunk_id": "2",
            "text": "Self-attention computes a weighted sum over "
                    "all positions in a sequence.",
        },
        {
            "chunk_id": "3",
            "text": "Photosynthesis converts sunlight into chemical "
                    "energy in plants.",
        },
    ]
    chat_model = build_llm()
    rerank_results = retrieve_then_rerank(
        "How does self-attention work?",
        demo_candidates,
        chat_model,
        top_k=2,
    )
    print("Top reranked results:")
    for result_item in rerank_results:
        print(
            " ", result_item["chunk_id"],
            "rerank_score={0}".format(result_item["rerank_score"]),
        )