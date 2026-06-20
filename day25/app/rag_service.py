"""ScholarRAG - service core.

Ties ingestion, embeddings, hybrid retrieval, and reranking together:
add a paper, ask a question, get a grounded answer with citations.
Stays free of FastAPI so it can be tested directly with fake
components, with no web layer or live API calls required.

Embeddings are cached per paper - adding a second paper only embeds
that paper's new chunks, never re-embeds chunks already indexed.
"""

import numpy as np
from langchain_core.messages import HumanMessage, SystemMessage

from bm25_index import BM25Index
from embeddings import GeminiEmbedder
from hybrid_search import HybridRetriever
from ingestion import chunk_paper, load_paper
from reranker import build_llm, retrieve_then_rerank
from vector_store import VectorStore

ANSWER_SYSTEM = (
    "You are a research assistant. Answer the user's question using "
    "ONLY the provided passages from one or more papers. Always cite "
    "the paper title and section for any claim, like "
    "(Attention Is All You Need, Section 3 Model Architecture). "
    "If the passages don't contain the answer, say so plainly instead "
    "of guessing."
)


def _build_answer_prompt(query, chunks):
    blocks = []
    for chunk in chunks:
        blocks.append(
            "[{0} - {1}] {2}".format(
                chunk["title"], chunk["section"], chunk["text"]
            )
        )
    context = "\n\n".join(blocks)
    return "Context passages:\n{0}\n\nQuestion: {1}".format(context, query)


class RagService:
    """Holds loaded papers, the hybrid index, and the ask/search flow."""

    def __init__(self, embedder=None, llm=None):
        self.embedder = embedder or GeminiEmbedder()
        self.llm = llm or build_llm()
        self.papers = {}
        self.paper_chunks = {}
        self.paper_vectors = {}
        self.vector_store = VectorStore(dim=self.embedder.dim)
        self.bm25_index = BM25Index([])
        self.retriever = HybridRetriever(self.vector_store, self.bm25_index)

    def add_paper(self, reference):
        """Fetch, chunk, and embed a paper, then rebuild the indexes."""
        paper = load_paper(reference)
        arxiv_id = paper["arxiv_id"]

        chunks = chunk_paper(paper)
        texts = [chunk["text"] for chunk in chunks]
        vectors = self.embedder.embed_documents(texts)

        self.papers[arxiv_id] = paper
        self.paper_chunks[arxiv_id] = chunks
        self.paper_vectors[arxiv_id] = vectors
        self._rebuild_indexes()
        return {
            "arxiv_id": arxiv_id,
            "title": paper["title"],
            "source": paper["source"],
            "chunk_count": len(chunks),
        }

    def remove_paper(self, arxiv_id):
        """Drop a paper and rebuild the indexes without it."""
        if arxiv_id not in self.papers:
            return False
        del self.papers[arxiv_id]
        del self.paper_chunks[arxiv_id]
        del self.paper_vectors[arxiv_id]
        self._rebuild_indexes()
        return True

    def list_papers(self):
        """Return lightweight metadata for every loaded paper."""
        return [
            {
                "arxiv_id": arxiv_id,
                "title": paper["title"],
                "source": paper["source"],
                "chunk_count": len(self.paper_chunks[arxiv_id]),
            }
            for arxiv_id, paper in self.papers.items()
        ]

    def _rebuild_indexes(self):
        """Rebuild FAISS + BM25 over every currently-loaded paper.

        Cheap relative to embedding: no Gemini calls happen here, since
        every paper's vectors were already computed and cached when it
        was added. This just re-concatenates and rebuilds the search
        structures, which is fast even with several papers loaded.
        """
        all_chunks = []
        vector_blocks = []
        for arxiv_id in self.papers:
            all_chunks.extend(self.paper_chunks[arxiv_id])
            vector_blocks.append(self.paper_vectors[arxiv_id])

        if vector_blocks:
            all_vectors = np.vstack(vector_blocks)
        else:
            all_vectors = np.zeros((0, self.embedder.dim), dtype="float32")

        self.vector_store.build(all_chunks, all_vectors)
        self.bm25_index = BM25Index(all_chunks)
        self.retriever = HybridRetriever(self.vector_store, self.bm25_index)

    def search(self, query, top_k=5, rerank=True):
        """Retrieve (and optionally rerank) chunks for a query.

        Always returns chunks with a single 'score' field representing
        final relevance, whether that came from reranking or straight
        from the hybrid blend - callers never need to know which.
        """
        if not self.papers:
            return []
        query_vector = self.embedder.embed_query(query)
        candidates = self.retriever.search(query, query_vector, top_k=20)
        if rerank and self.llm:
            results = retrieve_then_rerank(
                query, candidates, self.llm, top_k=top_k
            )
            for result in results:
                result["score"] = result.pop("rerank_score")
            return results
        return candidates[:top_k]

    def ask(self, query, top_k=5):
        """Full pipeline: retrieve, rerank, generate a grounded answer."""
        if not self.papers:
            return {
                "answer": (
                    "No papers loaded yet. Add a paper before asking."
                ),
                "sources": [],
            }
        chunks = self.search(query, top_k=top_k, rerank=True)
        if not chunks:
            return {"answer": "No relevant passages found.", "sources": []}

        prompt = _build_answer_prompt(query, chunks)
        messages = [
            SystemMessage(content=ANSWER_SYSTEM),
            HumanMessage(content=prompt),
        ]
        response = self.llm.invoke(messages)
        return {
            "answer": response.content,
            "sources": [
                {
                    "arxiv_id": chunk["arxiv_id"],
                    "title": chunk["title"],
                    "section": chunk["section"],
                    "chunk_id": chunk["chunk_id"],
                }
                for chunk in chunks
            ],
        }

    def health(self):
        """Lightweight status for the API's /health endpoint."""
        return {
            "papers_loaded": len(self.papers),
            "total_chunks": sum(
                len(chunks) for chunks in self.paper_chunks.values()
            ),
        }


if __name__ == "__main__":
    service = RagService()
    print("Adding 'Attention Is All You Need' (1706.03762)...")
    print(service.add_paper("1706.03762"))

    print("\nHealth:", service.health())

    print("\nAsking a question...")
    result = service.ask("What is self-attention?")
    print("Answer:", result["answer"])
    print("Sources:")
    for source in result["sources"]:
        print(" ", source["title"], "-", source["section"])