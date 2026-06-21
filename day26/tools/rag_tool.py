"""RAG search tool for the Day 26 LangChain ReAct agent.

Reuses the Day 25 ScholarRAG retrieval stack (GeminiEmbedder + FAISS
VectorStore + BM25Index + HybridRetriever, all wrapped by RagService)
directly as Python classes, instead of calling a separate running
server. The index is built ONCE - the first time this tool is
actually called, not on every call - so the agent can call it many
times in one session without re-embedding documents or repeatedly
paying for Gemini API calls.

NOTE: only one paper was actually loaded and tested during Day 25 -
arXiv:1706.03762 ("Attention Is All You Need"). This tool's index
only knows about that paper. To search other documents, add more
arXiv IDs to _PAPERS_TO_LOAD below.
"""
import sys
from pathlib import Path

from dotenv import load_dotenv
from langchain_core.tools import tool

# day25/app/ is a sibling folder, not an installed package, so Python
# won't find it automatically - we add it to sys.path before
# importing from it. This path is computed from this file's own
# location so it works regardless of the current working directory.
_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
_DAY25_APP_DIR = _REPO_ROOT / "day25" / "app"
sys.path.insert(0, str(_DAY25_APP_DIR))

from rag_service import RagService  # noqa: E402

# .env lives at the repo root and holds GEMINI_API_KEY / GROQ_API_KEY,
# which RagService needs internally when it builds its default
# embedder and LLM.
load_dotenv(dotenv_path=_REPO_ROOT / ".env")

# Papers actually ingested during Day 25 testing.
_PAPERS_TO_LOAD = ["1706.03762"]  # "Attention Is All You Need"

_SNIPPET_MAX_CHARS = 300

# Lazy singleton: stays None until the first real tool call, so that
# importing this file (e.g. for py_compile/pyflakes checks) never
# triggers a live Gemini API call on its own.
_service = None


def _get_service():
    """Build the RagService once and cache it for every later call."""
    global _service
    if _service is None:
        _service = RagService()
        for arxiv_id in _PAPERS_TO_LOAD:
            _service.add_paper(arxiv_id)
    return _service


@tool
def rag_search(query: str) -> str:
    """Search the indexed research papers and return relevant excerpts.

    Use this tool when the user asks about the content of their own
    indexed documents - currently this covers arXiv:1706.03762
    ("Attention Is All You Need"). Do NOT use this for general web
    questions (use web_search instead) or math (use calculator).

    Args:
        query: The question or topic to search for in the documents.

    Returns:
        A formatted list of the most relevant excerpts (paper title,
        section, snippet, relevance score), or a message starting
        with "Error:" if the search failed, or a message stating no
        results/papers were found.
    """
    try:
        service = _get_service()
        results = service.search(query, top_k=5, rerank=True)
    except Exception as exc:
        return f"Error: RAG search failed ({exc})."

    if not results:
        return f"No relevant document excerpts found for '{query}'."

    lines = [f"Top document excerpts for '{query}':"]
    for i, chunk in enumerate(results, start=1):
        title = chunk.get("title", "Unknown paper")
        section = chunk.get("section", "Unknown section")
        text = chunk.get("text", "").strip()
        score = chunk.get("score", 0)
        if len(text) > _SNIPPET_MAX_CHARS:
            text = text[:_SNIPPET_MAX_CHARS] + "..."
        lines.append(f"{i}. [{title} - {section}] (score={score:.3f})\n   {text}")
    return "\n".join(lines)


if __name__ == "__main__":
    # Live smoke test - needs real GEMINI_API_KEY and GROQ_API_KEY in
    # .env, and will make real API calls (embedding + LLM rerank).
    # Run this on your machine.
    print(rag_search.invoke({"query": "What is self-attention?"}))