"""Web search tool for the Day 26 LangChain ReAct agent.

Wraps a DuckDuckGo text search (via the `ddgs` package) with a retry
mechanism, since live search backends sometimes time out - we hit this
ourselves earlier today while setting up the environment. Formats
results as plain, readable text rather than raw dicts; the agent's own
LLM will reason over or further summarize this if needed, so we don't
make a second LLM call inside the tool itself.
"""
import time

from ddgs import DDGS
from ddgs.exceptions import DDGSException
from langchain_core.tools import tool

_MAX_RETRIES = 3
_RETRY_DELAY_SECONDS = 2
_MAX_RESULTS = 4


def _search_with_retry(query: str, max_results: int = _MAX_RESULTS) -> list[dict]:
    """Run a DDG text search, retrying on transient failures.

    Args:
        query: The search query string.
        max_results: How many results to fetch.

    Returns:
        A list of result dicts with 'title', 'href', 'body' keys.

    Raises:
        DDGSException: If every retry attempt fails. RatelimitException
            and TimeoutException both inherit from this, so catching
            DDGSException here covers both cases.
    """
    last_error = None
    for attempt in range(1, _MAX_RETRIES + 1):
        try:
            with DDGS() as ddgs:
                return list(ddgs.text(query, max_results=max_results))
        except DDGSException as exc:
            last_error = exc
            if attempt < _MAX_RETRIES:
                # Linear backoff: wait longer on each retry.
                time.sleep(_RETRY_DELAY_SECONDS * attempt)
    raise last_error


@tool
def web_search(query: str) -> str:
    """Search the web and return the top results as readable text.

    Use this tool when the user asks about something current, recent,
    or outside your own knowledge - for example "search for recent
    news on X" or "what's the latest version of Y". Do NOT use this
    for math (use the calculator tool) or for questions about the
    user's own uploaded documents (use the RAG search tool instead).

    Args:
        query: What to search for, e.g. "LangChain 1.0 release notes".

    Returns:
        A numbered list of the top results (title, short snippet,
        link), or a message starting with "Error:" if the search
        failed even after retries.
    """
    try:
        results = _search_with_retry(query)
    except DDGSException as exc:
        return f"Error: web search failed after retries ({exc})."
    except Exception as exc:
        # Tool must never raise and crash the agent loop - always
        # return a string the agent can reason about instead.
        return f"Error: unexpected web search failure ({exc})."

    if not results:
        return f"No results found for '{query}'."

    lines = [f"Top web results for '{query}':"]
    for i, result in enumerate(results, start=1):
        title = result.get("title", "Untitled")
        body = result.get("body", "").strip()
        href = result.get("href", "")
        lines.append(f"{i}. {title}\n   {body}\n   Source: {href}")
    return "\n".join(lines)


if __name__ == "__main__":
    # Live smoke test - needs real internet access, run on your machine.
    print(web_search.invoke({"query": "LangChain ReAct agent"}))