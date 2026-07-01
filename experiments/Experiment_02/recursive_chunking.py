from langchain_text_splitters import RecursiveCharacterTextSplitter
import tiktoken
import time


def recursive_chunking(text, chunk_size=500, chunk_overlap=50):
    """
    Split text using RecursiveCharacterTextSplitter
    and calculate character/token statistics.
    """

    start_time = time.perf_counter()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )

    chunks = splitter.split_text(text)

    end_time = time.perf_counter()

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
        "method": "Recursive Character Chunking",
        "chunks": chunks,
        "num_chunks": len(chunks),
        "avg_characters": avg_characters,
        "avg_tokens": avg_tokens,
        "time": round(end_time - start_time, 4)
    }