"""CLI entry point for the Day 21 Document Analyzer.

Offline (default, no model download / no API):
    uv run python run_demo.py

Live (real MiniLM embeddings + real Groq extraction; needs GROQ_API_KEY
in a local .env and runs in the .venv312 environment):
    uv run python run_demo.py --live
"""
from __future__ import annotations

import argparse
import os

import analyzer
import document_loader as dl


def _print_summary(report: dict) -> None:
    corpus = report["corpus"]
    search = report["semantic_search"]
    extraction = report["extraction"]
    print(f"\nMode: {report['mode']}")
    print(
        f"Documents: {corpus['num_documents']}  "
        f"Chars: {corpus['total_chars']}  "
        f"Chunks: {corpus['num_chunks']} "
        f"(size={corpus['chunk_size']}, "
        f"overlap={corpus['chunk_overlap']})"
    )
    print(f"\nQuery: {search['query']}")
    for res in search["results"]:
        print(
            f"  #{res['rank']} [{res['score']:.4f}] "
            f"{res['source']}: {res['preview']}"
        )
    print(
        f"\nExtraction micro-F1: {extraction['micro_f1']:.4f} "
        f"(P={extraction['micro_precision']:.4f}, "
        f"R={extraction['micro_recall']:.4f})"
    )
    print(
        f"Approx input tokens: "
        f"{report['cost_estimate']['approx_input_tokens']} "
        f"(charge ${report['cost_estimate']['charge_usd']})"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Document Analyzer")
    parser.add_argument(
        "--live",
        action="store_true",
        help="Use real MiniLM embeddings + real Groq extraction.",
    )
    parser.add_argument("--query", default=dl.TEST_QUERY)
    parser.add_argument("--top-k", type=int, default=3)
    parser.add_argument("--data-dir", default="data")
    parser.add_argument("--output-dir", default="outputs")
    args = parser.parse_args()

    report = analyzer.analyze(
        data_dir=args.data_dir,
        output_dir=args.output_dir,
        query=args.query,
        top_k=args.top_k,
        use_offline=not args.live,
    )
    path = analyzer.export_report(report, args.output_dir)
    _print_summary(report)
    print(f"\nReport written to {os.path.relpath(path)}")


if __name__ == "__main__":
    main()
