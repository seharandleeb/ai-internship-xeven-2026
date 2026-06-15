"""Document Analyzer orchestration.

Wires the Week 3 pieces into one flow:
load -> chunk -> embed/index -> semantic search -> structured
extraction -> accuracy scoring -> JSON report (with round-trip reload).
"""
from __future__ import annotations

import json
import os

import chunker
import document_loader as dl
import embeddings_index as ei
import entity_extraction as ee


def _approx_tokens(text: str) -> int:
    """Rough token estimate (~4 chars/token). Labelled approximate."""
    return max(1, round(len(text) / 4))


def analyze(
    data_dir: str,
    output_dir: str,
    query: str = dl.TEST_QUERY,
    top_k: int = 3,
    use_offline: bool = True,
) -> dict:
    """Run the full pipeline and return the report dict."""
    os.makedirs(output_dir, exist_ok=True)

    dl.create_sample_corpus(data_dir)
    docs = dl.load_corpus(data_dir)

    chunks = chunker.chunk_corpus(docs)

    embedder = ei.get_embedder(use_offline=use_offline)
    index = ei.SemanticIndex(embedder).build(chunks)
    hits = index.search(query, k=top_k)

    per_doc = []
    agg_tp = agg_pred = agg_gold = 0
    total_tokens = 0
    for doc in docs:
        pred = ee.extract_entities(
            doc["text"], doc["gold"], use_offline=use_offline
        )
        score = ee.score_extraction(pred, doc["gold"])
        agg_tp += score["true_positives"]
        agg_pred += score["predicted"]
        agg_gold += score["gold"]
        total_tokens += _approx_tokens(doc["text"])
        per_doc.append(
            {
                "filename": doc["filename"],
                "entities": pred.model_dump(),
                "score": score,
            }
        )

    micro_p = agg_tp / agg_pred if agg_pred else 0.0
    micro_r = agg_tp / agg_gold if agg_gold else 0.0
    micro_f1 = (
        2 * micro_p * micro_r / (micro_p + micro_r)
        if (micro_p + micro_r)
        else 0.0
    )

    report = {
        "mode": "offline" if use_offline else "live",
        "corpus": {
            "num_documents": len(docs),
            "total_chars": sum(len(d["text"]) for d in docs),
            "num_chunks": len(chunks),
            "chunk_size": chunker.DEFAULT_CHUNK_SIZE,
            "chunk_overlap": chunker.DEFAULT_CHUNK_OVERLAP,
        },
        "semantic_search": {
            "query": query,
            "top_k": top_k,
            "results": [
                {
                    "rank": i + 1,
                    "source": h["source"],
                    "score": round(h["score"], 4),
                    "preview": h["text"][:120].replace("\n", " "),
                }
                for i, h in enumerate(hits)
            ],
        },
        "extraction": {
            "per_document": per_doc,
            "micro_precision": round(micro_p, 4),
            "micro_recall": round(micro_r, 4),
            "micro_f1": round(micro_f1, 4),
        },
        "cost_estimate": {
            "provider": "Groq free tier",
            "charge_usd": 0.0,
            "approx_input_tokens": total_tokens,
            "note": "Approximate; ~4 chars/token. Free tier = no $.",
        },
    }
    return report


def export_report(report: dict, output_dir: str) -> str:
    """Write the report to JSON and verify a reload round-trip."""
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "analysis_report.json")
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2, ensure_ascii=False)
    with open(path, "r", encoding="utf-8") as handle:
        reloaded = json.load(handle)
    if reloaded != report:
        raise RuntimeError("JSON round-trip mismatch.")
    return path
