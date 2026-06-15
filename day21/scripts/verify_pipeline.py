"""Offline verification harness: proves each Day 21 wiring gate.

Run:  uv run python verify_pipeline.py
Every check raises AssertionError on failure; prints PASS lines on
success. All checks run offline (no model download, no Groq calls).
"""
from __future__ import annotations

import os
import tempfile

import analyzer
import chunker
import document_loader as dl
import embeddings_index as ei
import entity_extraction as ee
from pydantic import ValidationError


def main() -> None:
    tmp = tempfile.mkdtemp(prefix="day21_verify_")
    data_dir = os.path.join(tmp, "data")
    out_dir = os.path.join(tmp, "outputs")

    # 1. Sample corpus auto-creates (incl. a real, readable PDF).
    dl.create_sample_corpus(data_dir)
    for doc in dl.SAMPLE_DOCS:
        assert os.path.exists(os.path.join(data_dir, doc.filename))
    docs = dl.load_corpus(data_dir)
    pdf_doc = next(d for d in docs if d["filename"].endswith(".pdf"))
    assert "Globex Corporation" in pdf_doc["text"], "PDF text unreadable"
    print("PASS 1: sample corpus auto-creates; PDF text extracts")

    # 2. Chunker produces a sensible, deterministic chunk count.
    chunks = chunker.chunk_corpus(docs)
    assert 3 <= len(chunks) <= 12, f"unexpected chunk count {len(chunks)}"
    assert all(
        len(c["text"]) <= chunker.DEFAULT_CHUNK_SIZE + 5 for c in chunks
    )
    print(f"PASS 2: chunker produced {len(chunks)} chunks at "
          f"size={chunker.DEFAULT_CHUNK_SIZE}")

    # 3. Index returns the EXPECTED top-1 chunk, ranked by similarity.
    embedder = ei.get_embedder(use_offline=True)
    index = ei.SemanticIndex(embedder).build(chunks)
    hits = index.search(dl.TEST_QUERY, k=3)
    assert hits[0]["source"] == "memo_cloud.txt"
    assert dl.EXPECTED_TOP_PHRASE in hits[0]["text"], "wrong top-1 chunk"
    scores = [h["score"] for h in hits]
    assert scores == sorted(scores, reverse=True), "not ranked desc"
    rounded = [round(s, 3) for s in scores]
    print(f"PASS 3: expected top-1 returned; scores {rounded} desc")

    # 4. Pydantic validates good data and rejects a bad email.
    good = ee.DocumentEntities(emails=["a.b@example.com"])
    assert good.emails == ["a.b@example.com"]
    raised = False
    try:
        ee.DocumentEntities(emails=["not-an-email"])
    except ValidationError:
        raised = True
    assert raised, "invalid email should raise ValidationError"
    print("PASS 4: Pydantic accepts valid + rejects invalid email")

    # 5. Report exports to JSON and survives a reload round-trip.
    report = analyzer.analyze(data_dir, out_dir, use_offline=True)
    path = analyzer.export_report(report, out_dir)  # asserts internally
    assert os.path.exists(path)
    print("PASS 5: report exported to JSON; reload round-trip matches")

    # 6. Accuracy is computed vs gold and is NOT a trivial 100%.
    f1 = report["extraction"]["micro_f1"]
    assert 0.0 < f1 < 1.0, f"F1 {f1} should be non-trivial (0<F1<1)"
    print(f"PASS 6: extraction micro-F1 = {f1} (non-trivial, vs gold)")

    print("\nALL CHECKS PASSED")


if __name__ == "__main__":
    main()
