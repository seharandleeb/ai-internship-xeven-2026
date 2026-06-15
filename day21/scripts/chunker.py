"""Chunking via LangChain's ``RecursiveCharacterTextSplitter``.

Parameter choice (tuned for THIS corpus, not copied from a textbook):

On Day 18 I found that ~500-char chunks with ~50 overlap worked best for
longer continuous prose, because that kept a full paragraph-sized idea in
one chunk. The Day 21 sample corpus is different: short memos and notes
of 4-6 sentences where the answer to a query is usually a SINGLE
sentence. I swept [256, 400, 512] on the test query (see
``tune_chunk_size`` and the notebook). All three retrieved the correct
top-1 chunk, but smaller chunks scored HIGHER (256 -> 0.65, 400 -> 0.52,
512 -> 0.44) because there is less unrelated text diluting the chunk
vector -- at the cost of more fragments (7 vs 5 vs 3 chunks) and a higher
risk of splitting a fact across a boundary. I picked 400 as the balance:
it keeps a full sentence-plus-context intact, halves the fragment count
versus 256 (fewer vectors / fewer downstream LLM calls), and still
retrieves correctly. So I moved from Day 18's 500 down to 400 here.
Overlap of 60 (~15%) preserves a sentence that straddles a boundary
without duplicating whole chunks.
"""
from __future__ import annotations

from langchain_text_splitters import RecursiveCharacterTextSplitter

# Tuned for the Day 21 sample corpus (see module docstring).
DEFAULT_CHUNK_SIZE = 400
DEFAULT_CHUNK_OVERLAP = 60


def make_splitter(
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
) -> RecursiveCharacterTextSplitter:
    """Build a splitter with the chosen separators and sizes."""
    return RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
        length_function=len,
    )


def chunk_text(
    text: str,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
) -> list[str]:
    """Split one document's text into chunks."""
    splitter = make_splitter(chunk_size, chunk_overlap)
    return splitter.split_text(text)


def chunk_corpus(
    docs: list[dict],
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
) -> list[dict]:
    """Chunk every document, tagging each chunk with its source file."""
    chunks = []
    for doc in docs:
        for i, piece in enumerate(
            chunk_text(doc["text"], chunk_size, chunk_overlap)
        ):
            chunks.append(
                {
                    "source": doc["filename"],
                    "chunk_id": i,
                    "text": piece,
                }
            )
    return chunks


def tune_chunk_size(
    docs: list[dict],
    query: str,
    expected_phrase: str,
    candidate_sizes: list[int] | None = None,
) -> list[dict]:
    """Sweep candidate chunk sizes and report top-1 retrieval quality.

    Imported lazily to avoid a hard dependency cycle with the index
    module. Returns one row per candidate size with whether the expected
    phrase landed in the top-1 chunk and that chunk's similarity score.
    """
    from embeddings_index import SemanticIndex, get_embedder

    if candidate_sizes is None:
        candidate_sizes = [256, 400, 512]

    embedder = get_embedder(use_offline=True)
    results = []
    for size in candidate_sizes:
        overlap = max(1, size // 7)  # ~15% overlap
        chunks = chunk_corpus(docs, size, overlap)
        index = SemanticIndex(embedder)
        index.build(chunks)
        top = index.search(query, k=1)[0]
        results.append(
            {
                "chunk_size": size,
                "chunk_overlap": overlap,
                "num_chunks": len(chunks),
                "top1_hit": expected_phrase in top["text"],
                "top1_score": round(top["score"], 4),
            }
        )
    return results
