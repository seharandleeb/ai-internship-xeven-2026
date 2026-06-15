# Week 3 Feedback & Week 4 Action Items

> Template — fill the feedback section after the Week 3 review / mentor
> check-in. The Week 4 action items are pre-seeded from my own reflection
> and the RAG research; confirm/adjust with Sir Mubashir's input.

## Feedback received
- Source (mentor / peer): _______________________________
- Date: _______________________________

| # | Feedback | Area | My response / fix |
|---|----------|------|-------------------|
| 1 |          |      |                   |
| 2 |          |      |                   |
| 3 |          |      |                   |

## What went well (per feedback)
-
-

## Areas to improve (per feedback)
-
-

## Week 4 action items (RAG & Vector Databases)
- [ ] Migrate the analyzer's FAISS-local index to a managed vector DB
      (Pinecone) and compare latency/quality.
- [ ] Add chunk metadata enrichment (source, section header) before
      embedding — cheap accuracy lift flagged in research.
- [ ] Replace the single test query with a small evaluation set
      (query → expected chunk) and report recall@k.
- [ ] Build a full RAG pipeline (retrieve → augment → generate) on top of
      the existing retriever.
- [ ] Add basic monitoring + a cost/token log for live Groq calls.

## Self-assessment (Week 3)
- Confidence with embeddings + semantic search (Day 17): __ / 5
- Confidence with chunking strategies (Day 18): __ / 5
- Confidence with Pydantic structured extraction (Day 20): __ / 5
- Confidence integrating components into one app (Day 21): __ / 5
