# Day 21 Reflection — Week 3 Consolidation

## What worked well
- **One concern per module.** Splitting into `document_loader`,
  `chunker`, `embeddings_index`, `entity_extraction`, `analyzer`, and
  `run_demo` made the pipeline easy to reason about and test. The
  offline ↔ live switch ended up being a single flag because the
  embedder and extractor each sit behind one interface.
- **Tuning to the data.** The chunk-size sweep gave me a real reason for
  400/60 instead of a guessed number, and the result (smaller = higher
  similarity but more fragments) matched the precision-vs-context
  trade-off I read about.
- **Honest metrics.** Injecting known errors into the offline stub means
  the 0.8947 micro-F1 actually exercises the scoring code, so I trust it.
- **End-to-end proof.** `verify_pipeline.py` asserts all six wiring
  gates (corpus auto-creates, chunk count, expected top-1, Pydantic
  validation, JSON round-trip, non-trivial accuracy) and passes.

## What I'd do differently
- **Add chunk metadata** (source title, section) before embedding — the
  research consensus says this is a cheap, high-ROI accuracy lift I
  skipped.
- **Write an eval set, not a single test query.** One query proves
  wiring; it doesn't measure retrieval quality. A handful of
  query→expected-chunk pairs would give a real recall@k number.
- **Stronger offline extractor.** My offline stub leans on gold to inject
  errors; a small regex/NER baseline would be a more realistic stand-in.

## Next steps (Week 4: RAG & vector databases)
- Move from FAISS-local to a managed store (Pinecone) and compare.
- Build a full RAG pipeline: retrieve → augment prompt → generate, with
  the retrieved chunks grounding the answer.
- Add metadata filtering, an evaluation harness, and basic monitoring.
- Explore agent workflows that combine retrieval with tool use.
