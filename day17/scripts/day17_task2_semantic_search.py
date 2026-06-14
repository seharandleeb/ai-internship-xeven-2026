"""Day 17 - Task 2: Build a simple semantic search engine.

A knowledge base of 60 short sentences across several topics is created in-code
(no manual data files). Each sentence is embedded once; a query is embedded at
search time and ranked against the corpus by cosine similarity. This is the
"from scratch" version of what a vector database does under the hood.

Install (Windows + UV):
    uv pip install langchain-huggingface sentence-transformers numpy
"""

from __future__ import annotations

from typing import List, Sequence, Tuple

import numpy as np

EMBED_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

KNOWLEDGE_BASE: List[str] = [
    # Machine learning / AI
    "Gradient descent minimises a loss function by stepping down the gradient.",
    "A neural network learns weights through backpropagation.",
    "Random forests combine many decision trees to reduce overfitting.",
    "Support vector machines find the maximum-margin separating hyperplane.",
    "K-means clustering groups data points around centroids.",
    "Overfitting happens when a model memorises noise in the training data.",
    "Regularisation penalises large weights to improve generalisation.",
    "Transformers use self-attention to model long-range dependencies.",
    "Reinforcement learning trains agents through reward signals.",
    "Feature scaling helps gradient-based optimisers converge faster.",
    # Food / cooking
    "Roast the vegetables with olive oil, garlic, and rosemary.",
    "A balanced breakfast can include oats, fruit, and yoghurt.",
    "Simmer the lentils until they are soft and creamy.",
    "Grilled salmon pairs well with steamed asparagus.",
    "Use ripe tomatoes and fresh basil for the best pasta sauce.",
    "Quinoa is a protein-rich, gluten-free whole grain.",
    "Marinate the chicken overnight for deeper flavour.",
    "A green smoothie blends spinach, banana, and almond milk.",
    "Slow-cook the beans with cumin for a hearty stew.",
    "Steaming preserves more nutrients than deep frying.",
    # Space / astronomy
    "The James Webb telescope observes the infrared universe.",
    "A light-year measures distance, not time.",
    "Black holes have gravity so strong that light cannot escape.",
    "Mars has the largest volcano in the solar system.",
    "Comets develop glowing tails as they near the Sun.",
    "Galaxies are vast collections of stars, gas, and dust.",
    "The Moon's gravity drives the ocean tides on Earth.",
    "Neutron stars are incredibly dense stellar remnants.",
    "Saturn's rings are made mostly of ice and rock.",
    "Exoplanets orbit stars beyond our solar system.",
    # Health / fitness
    "Regular cardio strengthens the heart and lungs.",
    "Stretching improves flexibility and reduces injury risk.",
    "Drinking enough water supports concentration and energy.",
    "Strength training builds muscle and bone density.",
    "Sleep is essential for memory and recovery.",
    "Walking ten thousand steps a day improves cardiovascular health.",
    "Meditation can lower stress and improve focus.",
    "A rest day lets muscles repair after hard workouts.",
    "Good posture reduces back and neck strain.",
    "Warming up prepares the body before intense exercise.",
    # Finance / economics
    "Compound interest grows savings exponentially over time.",
    "Diversification spreads investment risk across assets.",
    "Inflation reduces the purchasing power of money.",
    "A bond pays periodic interest to the lender.",
    "Central banks adjust interest rates to manage the economy.",
    "An emergency fund covers several months of expenses.",
    "Index funds track a market benchmark at low cost.",
    "Supply and demand together determine market prices.",
    "A budget tracks income against monthly spending.",
    "Credit scores reflect a borrower's repayment history.",
    # Travel / geography
    "The Himalayas contain the tallest mountains on Earth.",
    "Venice is famous for its canals and gondolas.",
    "The Sahara is the largest hot desert in the world.",
    "Tokyo blends ancient temples with neon skyscrapers.",
    "The Amazon rainforest produces a fifth of Earth's oxygen.",
    "Iceland is known for geysers, glaciers, and volcanoes.",
    "The Great Barrier Reef hosts thousands of marine species.",
    "Petra is an ancient city carved into rose-coloured rock.",
    "The Nile is one of the longest rivers in the world.",
    "Norway's fjords were carved by ancient glaciers.",
]


def get_embedder():
    """Return a LangChain HuggingFace embedder."""
    from langchain_huggingface import HuggingFaceEmbeddings

    return HuggingFaceEmbeddings(model_name=EMBED_MODEL_NAME)


def cosine_similarity(vec_a: Sequence[float], vec_b: Sequence[float]) -> float:
    """Cosine similarity between two vectors (range -1 to 1)."""
    a = np.asarray(vec_a, dtype=np.float64)
    b = np.asarray(vec_b, dtype=np.float64)
    denom = np.linalg.norm(a) * np.linalg.norm(b)
    if denom == 0.0:
        return 0.0
    return float(np.dot(a, b) / denom)


def semantic_search(
    query_vec: Sequence[float],
    corpus_vecs: Sequence[Sequence[float]],
    texts: Sequence[str],
    top_k: int = 5,
) -> List[Tuple[str, float]]:
    """Rank corpus texts by cosine similarity to the query vector."""
    scored = [
        (texts[i], cosine_similarity(query_vec, corpus_vecs[i]))
        for i in range(len(corpus_vecs))
    ]
    scored.sort(key=lambda pair: pair[1], reverse=True)
    return scored[:top_k]


def main() -> None:
    embedder = get_embedder()
    corpus_vecs = embedder.embed_documents(KNOWLEDGE_BASE)
    print(
        f"Indexed {len(KNOWLEDGE_BASE)} sentences "
        f"(dimension {len(corpus_vecs[0])})."
    )

    queries = ["machine learning algorithms", "healthy food recipes"]
    for query in queries:
        query_vec = embedder.embed_query(query)
        results = semantic_search(query_vec, corpus_vecs, KNOWLEDGE_BASE, top_k=5)
        print(f"\nQuery: {query!r}")
        for rank, (text, score) in enumerate(results, start=1):
            print(f"  {rank}. ({score:.3f}) {text}")


if __name__ == "__main__":
    main()
