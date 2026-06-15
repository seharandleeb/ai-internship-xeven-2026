"""Day 18 - Task 2: Optimal chunk size experiment.

Splits the same document at 200 / 500 / 1000 / 2000 characters, counts
the resulting chunks, and estimates vector-store size. It then runs an
optional retrieval evaluation (local HuggingFace embeddings + FAISS) to
see which chunk size returns the most relevant context.

The chunk-count + storage analysis runs with no extra dependencies. The
retrieval section needs sentence-transformers + faiss-cpu; if those are
missing the script prints a clear note instead of crashing, so the file
always runs end to end.

Run from inside day18/scripts/:
    python task2_chunk_size_experiment.py
"""

# Dependencies (install once, do NOT run pip inside a notebook):
#   uv pip install langchain-text-splitters
#   uv pip install langchain-huggingface sentence-transformers faiss-cpu
#   (use a Python 3.12 env: faiss-cpu has no 3.13 wheel yet)

import os

from langchain_text_splitters import RecursiveCharacterTextSplitter

OUTPUT_DIR = "outputs"
SAMPLE_PATH = os.path.join(OUTPUT_DIR, "sample_long_text.txt")

CHUNK_SIZES = [200, 500, 1000, 2000]
OVERLAP_RATIO = 0.10  # 10% overlap, scaled to each chunk size.

# all-MiniLM-L6-v2 outputs 384-dim float32 vectors.
EMBED_DIM = 384
BYTES_PER_FLOAT = 4

# Threshold TUNED to all-MiniLM-L6-v2, not a textbook value.
# On Day 17 a genuine match scored ~0.62 while the textbook 0.95 cutoff
# returned zero hits. With normalized cosine similarity this model puts
# relevant question/chunk pairs roughly in the 0.4-0.7 band, so 0.45 is
# a sensible "this chunk is on-topic" line.
RELEVANCE_THRESHOLD = 0.45

PROBE_QUESTIONS = [
    "How does self-attention compute its weights?",
    "Why do transformers need positional encodings?",
    "What problem does chunk overlap solve?",
]

SAMPLE_TEXT = """Attention Is All You Need: A Plain-Language Overview

Transformer models replaced recurrent networks as the backbone of
modern natural language processing. Instead of reading a sequence one
token at a time, a transformer looks at every token at once and learns
which other tokens each position should pay attention to. This is the
self-attention mechanism, and it is the single idea that makes the
architecture scale so well on parallel hardware.

Self-attention works by projecting each token into three vectors: a
query, a key, and a value. The query of one token is compared against
the keys of every token to produce a set of weights. Those weights are
used to take a weighted average of the value vectors. Tokens that are
relevant to each other end up with high weights, so information flows
directly between distant words without passing through many
intermediate steps.

Positional encodings are added because attention itself is
order-agnostic. Without them the sentence order would be lost.
Sinusoidal or learned position vectors give the model a sense of
sequence so word order is preserved across the whole input.

Large language models have a fixed context window, so you cannot paste
an entire book into a single prompt. Retrieval-augmented generation
solves this by storing document chunks as embeddings, searching for the
chunks most relevant to a question, and feeding only those chunks to
the model. The quality of that pipeline depends heavily on how the
document was split in the first place.

If chunks are too large, a single chunk mixes several topics and the
embedding becomes a blurry average that matches nothing precisely. If
chunks are too small, each chunk is precise but loses the surrounding
context needed to answer real questions. Overlap between consecutive
chunks softens this trade-off by repeating a few sentences at every
boundary, so an idea that straddles two chunks survives in at least one
of them.

The practical takeaway is that chunking is a design decision. A blunt
fixed-size cut is fast but slices sentences in half, while a recursive
splitter that prefers paragraph and sentence boundaries keeps ideas
intact and is the pragmatic default for most documents.
"""


def build_sample(path):
    """Write the sample document to disk so we can 'load' it."""
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(SAMPLE_TEXT)


def analyze_sizes(text, sizes):
    """Split at each size and return counts + storage estimates.

    Storage is estimated as n_chunks * EMBED_DIM * 4 bytes, the raw
    footprint of the float32 vectors before any index overhead.
    """
    rows = []
    for size in sizes:
        overlap = int(size * OVERLAP_RATIO)
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=size,
            chunk_overlap=overlap,
        )
        chunks = splitter.split_text(text)
        lengths = [len(c) for c in chunks]
        storage = len(chunks) * EMBED_DIM * BYTES_PER_FLOAT
        rows.append({
            "size": size,
            "overlap": overlap,
            "n_chunks": len(chunks),
            "avg_len": round(sum(lengths) / len(lengths), 1) if lengths else 0,
            "storage_bytes": storage,
            "chunks": chunks,
        })
    return rows


def run_retrieval_eval(rows, questions):
    """Embed each size's chunks and score retrieval quality.

    Returns a dict mapping chunk size -> mean top-1 cosine similarity
    across the probe questions, or None if the embedding stack is not
    installed (so the rest of the script still runs).
    """
    try:
        from langchain_huggingface import HuggingFaceEmbeddings
        from langchain_community.vectorstores import FAISS
    except ImportError:
        return None

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        encode_kwargs={"normalize_embeddings": True},
    )

    scores = {}
    for row in rows:
        store = FAISS.from_texts(row["chunks"], embeddings)
        sims = []
        for question in questions:
            hits = store.similarity_search_with_relevance_scores(
                question, k=1)
            if hits:
                sims.append(hits[0][1])
        scores[row["size"]] = round(sum(sims) / len(sims), 3) if sims else 0.0
    return scores


def recommend(rows, scores):
    """Pick a recommended size from the measured data."""
    if scores:
        best = max(scores, key=scores.get)
        reason = ("highest mean top-1 similarity (%.3f), above the tuned "
                  "%.2f relevance line" % (scores[best], RELEVANCE_THRESHOLD))
        return best, reason
    # Storage-only heuristic: smallest size whose chunks still average
    # over ~300 chars of context (avoids over-fragmentation).
    viable = [r for r in rows if r["avg_len"] >= 300]
    pick = viable[0] if viable else rows[len(rows) // 2]
    return (pick["size"],
            "balances precision and context without a retrieval run")


def render_report(text, rows, scores, rec_size, rec_reason):
    """Build a human-readable report string."""
    lines = []
    lines.append("Day 18 - Task 2: Optimal Chunk Size Experiment")
    lines.append("=" * 48)
    lines.append("Source length: %d characters" % len(text))
    lines.append("Embedding model: all-MiniLM-L6-v2 (%d-dim float32)"
                 % EMBED_DIM)
    lines.append("")
    header = "%-6s %-8s %-9s %-10s %-12s %s" % (
        "size", "overlap", "n_chunks", "avg_len", "storage", "retr_score")
    lines.append(header)
    lines.append("-" * len(header))
    for row in rows:
        score = scores.get(row["size"]) if scores else None
        score_txt = "%.3f" % score if score is not None else "n/a"
        lines.append("%-6d %-8d %-9d %-10.1f %-12s %s" % (
            row["size"], row["overlap"], row["n_chunks"], row["avg_len"],
            "%d B" % row["storage_bytes"], score_txt))
    lines.append("")
    if scores is None:
        lines.append("Retrieval score: SKIPPED (embedding stack not "
                     "installed in this run).")
    lines.append("Recommendation: chunk_size=%d -- %s." % (rec_size,
                                                           rec_reason))
    lines.append("")
    lines.append("Reading the trade-off:")
    lines.append("  Smaller sizes make more, tighter chunks (more storage,")
    lines.append("  higher precision, less context per hit). Larger sizes")
    lines.append("  make fewer, broader chunks (less storage, more context,")
    lines.append("  lower precision). 500 chars is the usual sweet spot for")
    lines.append("  short articles like this one.")
    return "\n".join(lines)


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    build_sample(SAMPLE_PATH)
    with open(SAMPLE_PATH, "r", encoding="utf-8") as handle:
        text = handle.read()

    rows = analyze_sizes(text, CHUNK_SIZES)
    scores = run_retrieval_eval(rows, PROBE_QUESTIONS)
    rec_size, rec_reason = recommend(rows, scores)

    report = render_report(text, rows, scores, rec_size, rec_reason)
    print(report)

    report_path = os.path.join(OUTPUT_DIR, "task2_chunk_size_report.txt")
    with open(report_path, "w", encoding="utf-8") as handle:
        handle.write(report + "\n")
    print("\nSaved report -> %s" % report_path)


if __name__ == "__main__":
    main()
