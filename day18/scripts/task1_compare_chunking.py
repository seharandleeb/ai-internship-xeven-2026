"""Day 18 - Task 1: Compare chunking methods.

Compares a blunt fixed-size splitter (CharacterTextSplitter with an
empty separator -> pure 500-char cuts, no overlap) against
RecursiveCharacterTextSplitter (500 chars, 50 overlap) which respects
natural boundaries (paragraphs -> lines -> sentences -> words).

The script auto-creates its sample document and output folder, so it
runs end to end with no manual setup.

Run from inside day18/scripts/:
    python task1_compare_chunking.py
"""

# Dependencies (install once, do NOT run pip inside a notebook):
#   uv pip install langchain-text-splitters

import os

from langchain_text_splitters import (
    CharacterTextSplitter,
    RecursiveCharacterTextSplitter,
)

OUTPUT_DIR = "outputs"
SAMPLE_PATH = os.path.join(OUTPUT_DIR, "sample_article.txt")

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
order-agnostic. Without them, the sentence "the cat sat on the mat"
would look identical to any shuffling of the same words. Sinusoidal or
learned position vectors give the model a sense of sequence so word
order is preserved.

Why does this matter for retrieval systems? Large language models have
a fixed context window. You cannot paste an entire book into a single
prompt. Retrieval-augmented generation solves this by storing document
chunks as embeddings, searching for the chunks most relevant to a
question, and feeding only those chunks to the model. The quality of
that pipeline depends heavily on how the document was split in the
first place.

If chunks are too large, a single chunk mixes several topics and the
embedding becomes a blurry average that matches nothing precisely. If
chunks are too small, each chunk is precise but loses the surrounding
context needed to answer real questions. Overlap between consecutive
chunks softens this trade-off by repeating a few sentences at every
boundary, so an idea that straddles two chunks survives in at least one
of them.

The practical takeaway is that chunking is a design decision, not a
preprocessing afterthought. A blunt fixed-size cut is fast but slices
sentences in half. A recursive splitter that prefers paragraph and
sentence boundaries keeps ideas intact and is the pragmatic default for
most documents.
"""


def build_sample(path):
    """Write the sample document to disk so we can 'load' it."""
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(SAMPLE_TEXT)


def load_text(path):
    """Read the document back from disk."""
    with open(path, "r", encoding="utf-8") as handle:
        return handle.read()


def breaks_word(chunk, source):
    """Return True if the chunk starts or ends in the middle of a word.

    We locate the chunk in the source and check whether an alphanumeric
    character sits immediately before its start or after its end. This
    is a precise "was a word cut?" test, independent of punctuation.
    """
    if not chunk:
        return False
    idx = source.find(chunk)
    if idx == -1:
        return False
    before = source[idx - 1] if idx > 0 else ""
    after_idx = idx + len(chunk)
    after = source[after_idx] if after_idx < len(source) else ""
    started_mid = before.isalnum() and chunk[0].isalnum()
    ended_mid = after.isalnum() and chunk[-1].isalnum()
    return started_mid or ended_mid


def summarize(name, chunks, source):
    """Compute simple quality metrics for a list of chunks."""
    lengths = [len(c) for c in chunks]
    broken = sum(1 for c in chunks if breaks_word(c, source))
    return {
        "name": name,
        "count": len(chunks),
        "avg_len": round(sum(lengths) / len(lengths), 1) if lengths else 0,
        "min_len": min(lengths) if lengths else 0,
        "max_len": max(lengths) if lengths else 0,
        "broken_boundaries": broken,
    }


def render_report(text, char_stats, rec_stats, char_chunks, rec_chunks):
    """Build a human-readable comparison report as a string."""
    lines = []
    lines.append("Day 18 - Task 1: Chunking Method Comparison")
    lines.append("=" * 48)
    lines.append("Source length: %d characters" % len(text))
    lines.append("")
    for stats in (char_stats, rec_stats):
        lines.append("[%s]" % stats["name"])
        lines.append("  chunks .............. %d" % stats["count"])
        lines.append("  avg chunk length .... %.1f chars" % stats["avg_len"])
        lines.append("  min / max length .... %d / %d"
                     % (stats["min_len"], stats["max_len"]))
        lines.append("  broken boundaries ... %d (chunks ending mid-word)"
                     % stats["broken_boundaries"])
        lines.append("")
    lines.append(
        "First chunk - CharacterTextSplitter (fixed 500, no overlap):")
    lines.append("  ...%s..." % repr(char_chunks[0][-60:]))
    lines.append("First chunk - RecursiveCharacterTextSplitter (500/50):")
    lines.append("  ...%s..." % repr(rec_chunks[0][-60:]))
    lines.append("")
    lines.append("Finding:")
    lines.append(
        "  The fixed-size splitter cuts at exactly 500 characters, so it")
    lines.append("  slices through words wherever they happen to fall. The")
    lines.append("  recursive splitter prefers paragraph/line/word breaks, so")
    lines.append("  no chunk is cut mid-word and meaning is preserved. The")
    lines.append("  50-char overlap also carries context across boundaries.")
    return "\n".join(lines)


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    build_sample(SAMPLE_PATH)
    text = load_text(SAMPLE_PATH)

    # Blunt fixed-size: empty separator forces exact 500-char cuts.
    char_splitter = CharacterTextSplitter(
        separator="",
        chunk_size=500,
        chunk_overlap=0,
    )
    # Structure-aware: tries \n\n, \n, " ", "" in order.
    rec_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
    )

    char_chunks = char_splitter.split_text(text)
    rec_chunks = rec_splitter.split_text(text)

    char_stats = summarize("CharacterTextSplitter (fixed 500, no overlap)",
                           char_chunks, text)
    rec_stats = summarize("RecursiveCharacterTextSplitter (500, 50 overlap)",
                          rec_chunks, text)

    report = render_report(text, char_stats, rec_stats,
                           char_chunks, rec_chunks)
    print(report)

    report_path = os.path.join(OUTPUT_DIR, "task1_chunking_comparison.txt")
    with open(report_path, "w", encoding="utf-8") as handle:
        handle.write(report + "\n")
    print("\nSaved report -> %s" % report_path)


if __name__ == "__main__":
    main()
