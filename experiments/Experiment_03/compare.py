import fitz

from recursive_chunking import recursive_chunking
from minilm_embedding import generate_minilm_embeddings
from bge_embedding import generate_bge_embeddings
from retrieval import retrieve_top_k
from queries import QUERIES


PDF_PATH = "SBP-Act.pdf"


def load_pdf(pdf_path):
    """
    Load PDF using PyMuPDF.
    """

    document = fitz.open(pdf_path)

    text = ""

    for page in document:
        text += page.get_text()

    document.close()

    return text


def print_embedding_stats(result):
    """
    Print embedding statistics.
    """

    print(f"Model                 : {result['model']}")
    print(f"Embedding Dimension   : {result['embedding_dimension']}")
    print(f"Number of Embeddings  : {result['num_embeddings']}")
    print(f"Execution Time        : {result['time']} sec")


def print_retrieval_results(results):
    """
    Print retrieved chunks.
    """

    for item in results:

        print(f"\nChunk ID : {item['chunk_id']}")
        print(f"Score    : {item['score']}")

        preview = item["text"][:200].replace("\n", " ")

        print(f"Preview  : {preview}...")


if __name__ == "__main__":

    print("\n========== Experiment 03 ==========\n")

    text = load_pdf(PDF_PATH)

    chunk_result = recursive_chunking(text)

    chunks = chunk_result["chunks"]

    print("Document Statistics")
    print("----------------------------------------")
    print(f"Chunks               : {chunk_result['num_chunks']}")
    print(f"Average Characters   : {chunk_result['avg_characters']}")
    print(f"Average Tokens       : {chunk_result['avg_tokens']}")
    print()

    # MiniLM
    minilm = generate_minilm_embeddings(chunks)

    print("MiniLM")
    print("----------------------------------------")

    print_embedding_stats(minilm)

    print()

    # BGE
    bge = generate_bge_embeddings(chunks)

    print("BGE-M3")
    print("----------------------------------------")

    print_embedding_stats(bge)

    print()

    # Retrieval Comparison
    print("\n========== Retrieval Comparison ==========\n")

    for query in QUERIES:

        print("=" * 80)
        print(f"Query: {query}")

        print("\nMiniLM Results")

        minilm_results = retrieve_top_k(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            query=query,
            chunks=chunks,
            document_embeddings=minilm["embeddings"],
            top_k=3
        )

        print_retrieval_results(minilm_results)

        print("\nBGE-M3 Results")

        bge_results = retrieve_top_k(
            model_name="BAAI/bge-m3",
            query=query,
            chunks=chunks,
            document_embeddings=bge["embeddings"],
            top_k=3
        )

        print_retrieval_results(bge_results)

        print("\n")

    print("=" * 80)

    print("\nFinal Engineering Decision")

    print("- MiniLM provides faster embedding generation.")
    print("- BGE-M3 produces higher-dimensional semantic embeddings.")
    print("- MiniLM is suitable for latency-sensitive applications.")
    print("- BGE-M3 is preferred when semantic retrieval quality is the primary objective.")