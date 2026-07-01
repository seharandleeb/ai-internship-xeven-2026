import numpy as np
from sentence_transformers import SentenceTransformer


def retrieve_top_k(
    model_name,
    query,
    chunks,
    document_embeddings,
    top_k=3
):
    """
    Retrieve the Top-K most relevant chunks using cosine similarity.

    Parameters
    ----------
    model_name : str
        SentenceTransformer model name.

    query : str
        User query.

    chunks : list
        Document chunks.

    document_embeddings : ndarray
        Embeddings of all document chunks.

    top_k : int
        Number of chunks to retrieve.

    Returns
    -------
    list
        List of retrieved chunks with similarity scores.
    """

    # Load embedding model
    model = SentenceTransformer(model_name)

    # Generate query embedding
    query_embedding = model.encode(
        query,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    # Cosine similarity
    similarities = np.dot(document_embeddings, query_embedding)

    # Get Top-K indices
    top_indices = np.argsort(similarities)[::-1][:top_k]

    results = []

    for index in top_indices:

        results.append({

            "chunk_id": index,

            "score": round(float(similarities[index]), 4),

            "text": chunks[index]

        })

    return results