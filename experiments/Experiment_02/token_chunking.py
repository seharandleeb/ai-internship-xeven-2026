from langchain_text_splitters import TokenTextSplitter
import tiktoken
import time


def token_chunking(text, chunk_size=500, chunk_overlap=50):
    """
    Split text using TokenTextSplitter and calculate
    both character-level and token-level statistics.
    """

    start_time = time.perf_counter()

    splitter = TokenTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )

    chunks = splitter.split_text(text)

    end_time = time.perf_counter()

    # Tokenizer used by modern OpenAI-compatible models
    encoding = tiktoken.get_encoding("cl100k_base")

    avg_characters = round(
        sum(len(chunk) for chunk in chunks) / len(chunks),
        2
    )

    avg_tokens = round(
        sum(len(encoding.encode(chunk)) for chunk in chunks) / len(chunks),
        2
    )

    return {
        "method": "Token Chunking",
        "chunks": chunks,
        "num_chunks": len(chunks),
        "avg_characters": avg_characters,
        "avg_tokens": avg_tokens,
        "time": round(end_time - start_time, 4)
    }