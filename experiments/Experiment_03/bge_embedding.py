from sentence_transformers import SentenceTransformer
import time


MODEL_NAME = "BAAI/bge-m3"


def generate_bge_embeddings(chunks):
    """
    Generate embeddings using the BAAI/bge-m3 model.

    Parameters
    ----------
    chunks : list
        List of text chunks.

    Returns
    -------
    dict
        Embedding statistics and generated embeddings.
    """

    start_time = time.perf_counter()

    model = SentenceTransformer(MODEL_NAME)

    embeddings = model.encode(
        chunks,
        convert_to_numpy=True,
        show_progress_bar=True,
        normalize_embeddings=True
    )

    end_time = time.perf_counter()

    return {
        "model": MODEL_NAME,
        "embedding_dimension": embeddings.shape[1],
        "num_embeddings": len(embeddings),
        "embeddings": embeddings,
        "time": round(end_time - start_time, 4)
    }